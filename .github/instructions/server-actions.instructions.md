---
description: Read this before implementing or modifying any server actions or data mutations in the project.
applyTo: "**/actions.ts"
---

# Server Actions

## File Conventions

- Server action files **must** be named `actions.ts` and colocated in the same directory as the component that calls them.
- Server actions must be called from **Client Components** only.

## Type Safety & Validation

- All data passed to server actions must have explicit TypeScript types — **never use `FormData`**.
- All incoming data **must** be validated with **Zod** before use.

## Authentication

- Every server action must **first** verify a logged-in user via `await auth()` before performing any database operation. Return early (or throw) if no `userId` is present.

## Error Handling

- Server actions **must not throw errors**. Instead, return a typed object with either a `success` or `error` property.
- Callers should check the returned object to determine the outcome.

```ts
// success
return { success: true, data: result };

// failure
return { error: "Unauthorized" };
```

## Database Access

- Server actions **must not** use Drizzle queries directly.
- All database operations must go through **helper functions** located in the `/data` directory.

## Example Structure

```ts
"use server";

import { z } from "zod";
import { auth } from "@clerk/nextjs/server";
import { createLink } from "@/data/links";

const schema = z.object({
  url: z.string().url(),
});

export async function createLinkAction(input: { url: string }) {
  const { userId } = await auth();
  if (!userId) return { error: "Unauthorized" };

  const parsed = schema.safeParse(input);
  if (!parsed.success) return { error: "Invalid input" };

  const result = await createLink({ userId, url: parsed.data.url });
  return { success: true, data: result };
}
```
