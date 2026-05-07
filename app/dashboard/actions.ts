"use server";

import { z } from "zod";
import { auth } from "@clerk/nextjs/server";
import { nanoid } from "nanoid";
import { createLink, updateLink, deleteLink } from "@/data/links";

const schema = z.object({
  url: z.string().url(),
  shortCode: z
    .string()
    .min(2)
    .max(20)
    .regex(/^[a-zA-Z0-9_-]+$/, {
      message: "Only letters, numbers, hyphens, and underscores are allowed",
    })
    .optional(),
});

const updateSchema = z.object({
  id: z.number().int().positive(),
  url: z.string().url(),
  shortCode: z
    .string()
    .min(2)
    .max(20)
    .regex(/^[a-zA-Z0-9_-]+$/, {
      message: "Only letters, numbers, hyphens, and underscores are allowed",
    }),
});

export async function createLinkAction(input: {
  url: string;
  shortCode?: string;
}) {
  const { userId } = await auth();
  if (!userId) return { error: "Unauthorized" };

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
