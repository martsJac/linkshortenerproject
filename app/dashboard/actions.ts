"use server";

import { z } from "zod";
import { auth } from "@clerk/nextjs/server";
import { nanoid } from "nanoid";
import { createLink, updateLink, deleteLink, countRecentLinksByUserId } from "@/data/links";

const RESERVED_SHORT_CODES = new Set([
  "dashboard", "api", "l", "login", "signup", "register",
  "admin", "settings", "account", "profile", "help", "about",
  "terms", "privacy", "contact", "home", "index",
]);

const schema = z.object({
  url: z.string().url().refine(
    (url) => {
      try {
        const { protocol } = new URL(url);
        return protocol === "http:" || protocol === "https:";
      } catch {
        return false;
      }
    },
    { message: "Only http and https URLs are allowed" }
  ),
  shortCode: z
    .string()
    .min(2)
    .max(20)
    .regex(/^[a-zA-Z0-9_-]+$/, {
      message: "Only letters, numbers, hyphens, and underscores are allowed",
    })
    .refine(
      (code) => !RESERVED_SHORT_CODES.has(code.toLowerCase()),
      { message: "This short code is reserved and cannot be used" }
    )
    .optional(),
});

const updateSchema = z.object({
  id: z.number().int().positive(),
  url: z.string().url().refine(
    (url) => {
      try {
        const { protocol } = new URL(url);
        return protocol === "http:" || protocol === "https:";
      } catch {
        return false;
      }
    },
    { message: "Only http and https URLs are allowed" }
  ),
  shortCode: z
    .string()
    .min(2)
    .max(20)
    .regex(/^[a-zA-Z0-9_-]+$/, {
      message: "Only letters, numbers, hyphens, and underscores are allowed",
    })
    .refine(
      (code) => !RESERVED_SHORT_CODES.has(code.toLowerCase()),
      { message: "This short code is reserved and cannot be used" }
    ),
});

export async function createLinkAction(input: {
  url: string;
  shortCode?: string;
}) {
  const { userId } = await auth();
  if (!userId) return { error: "Unauthorized" };

  const recentCount = await countRecentLinksByUserId(userId);
  if (recentCount >= 10) {
    return { error: "Rate limit exceeded. You can create at most 10 links per hour." };
  }

  const parsed = schema.safeParse(input);
  if (!parsed.success) return { error: parsed.error.issues[0].message };

  try {
    const result = await createLink({
      userId,
      originalUrl: parsed.data.url,
      shortCode: parsed.data.shortCode ?? nanoid(8),
    });
    return { success: true, data: result };
  } catch {
    return { error: "Short code already taken. Please choose another." };
  }
}

export async function updateLinkAction(input: {
  id: number;
  url: string;
  shortCode: string;
}) {
  const { userId } = await auth();
  if (!userId) return { error: "Unauthorized" };

  const parsed = updateSchema.safeParse(input);
  if (!parsed.success) return { error: parsed.error.issues[0].message };

  try {
    const result = await updateLink({
      id: parsed.data.id,
      userId,
      originalUrl: parsed.data.url,
      shortCode: parsed.data.shortCode,
    });
    return { success: true, data: result };
  } catch {
    return { error: "Short code already taken. Please choose another." };
  }
}

export async function deleteLinkAction(input: { id: number }) {
  const { userId } = await auth();
  if (!userId) return { error: "Unauthorized" };

  const parsed = z.object({ id: z.number().int().positive() }).safeParse(input);
  if (!parsed.success) return { error: "Invalid input" };

  await deleteLink({ id: parsed.data.id, userId });
  return { success: true };
}
