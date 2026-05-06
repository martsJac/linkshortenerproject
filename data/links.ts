import { db } from '@/db'
import { links } from '@/db/schema'
import { and, desc, eq } from 'drizzle-orm'

export async function getLinksByUserId(userId: string) {
  return db.select().from(links).where(eq(links.userId, userId)).orderBy(desc(links.updatedAt))
}

export async function createLink({
  userId,
  originalUrl,
  shortCode,
}: {
  userId: string
  originalUrl: string
  shortCode: string
}) {
  const [link] = await db
    .insert(links)
    .values({ userId, originalUrl, shortCode })
    .returning()
  return link
}

export async function updateLink({
  id,
  userId,
  originalUrl,
  shortCode,
}: {
  id: number
  userId: string
  originalUrl: string
  shortCode: string
}) {
  const [link] = await db
    .update(links)
    .set({ originalUrl, shortCode, updatedAt: new Date() })
    .where(and(eq(links.id, id), eq(links.userId, userId)))
    .returning()
  return link
}

export async function deleteLink({ id, userId }: { id: number; userId: string }) {
  await db.delete(links).where(and(eq(links.id, id), eq(links.userId, userId)))
}
