<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.

<!-- END:nextjs-agent-rules -->

# Agent Instructions — Link Shortener Project

This is a **URL shortener** application. Users authenticate, submit long URLs, and receive short slugs. Visiting a short URL redirects the browser to the original destination. Authenticated users can manage their links from a dashboard.

## Quick Reference

- **Framework**: Next.js 16.2.4, React 19, TypeScript 5 (strict)
- **Database**: Drizzle ORM + Neon PostgreSQL (`db/schema.ts` is the source of truth)
- **Auth**: Clerk v7 — always scope DB queries to `userId` from `auth()`
- **UI**: shadcn/ui (radix-nova style) + Radix UI + Tailwind CSS v4 + lucide-react
- **Path alias**: `@/*` → project root — always use it, never use relative `../../` imports
- **`params` and `searchParams`** are Promises in Next.js 16 — always `await` them
- **`auth()`** returns a Promise in Clerk v7 — always `await` it

## General Rules

1. All data mutations must go through Server Actions or API route handlers — never mutate from Client Components directly.
2. All user-owned database operations must be guarded by the authenticated `userId`.
3. TypeScript strict mode is on — no `any`, no `@ts-ignore` without a documented reason.
4. **NEVER use `middleware.ts`** — it is deprecated and removed in this version of Next.js. Use `proxy.ts` instead for any logic that would traditionally live in middleware (e.g. auth guards, redirects, request rewriting).
