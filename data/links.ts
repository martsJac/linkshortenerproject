import { db } from "@/db";
import { links } from "@/db/schema";
import { and, count, desc, eq, gte } from "drizzle-orm";

export async function getLinksByUserId(userId: string) {
  return db
    .select()
    .from(links)
    .where(eq(links.userId, userId))
    .orderBy(desc(links.updatedAt));
}

export async function createLink({
  userId,
  originalUrl,
  shortCode,
}: {
  userId: string;
  originalUrl: string;
  shortCode: string;
}) {
  const [link] = await db
    .insert(links)
    .values({ userId, originalUrl, shortCode })
    .returning();
  return link;
}

export async function updateLink({
  id,
  userId,
  originalUrl,
  shortCode,
}: {
  id: number;
  userId: string;
  originalUrl: string;
  shortCode: string;
}) {
  const [link] = await db
    .update(links)
    .set({ originalUrl, shortCode, updatedAt: new Date() })
    .where(and(eq(links.id, id), eq(links.userId, userId)))
    .returning();
  return link;
}

export async function deleteLink({
  id,
  userId,
}: {
  id: number;
  userId: string;
}) {
  await db.delete(links).where(and(eq(links.id, id), eq(links.userId, userId)));
}

export async function countRecentLinksByUserId(userId: string): Promise<number> {
  const oneHourAgo = new Date(Date.now() - 60 * 60 * 1000);
  const [result] = await db
    .select({ count: count() })
    .from(links)
    .where(and(eq(links.userId, userId), gte(links.createdAt, oneHourAgo)));
  return result?.count ?? 0;
}

export async function getLinkByShortCode(shortCode: string) {
  const [link] = await db
    .select()
    .from(links)
    .where(eq(links.shortCode, shortCode))
    .limit(1);
  return link ?? null;
}
