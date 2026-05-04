# Authentication — Clerk

## Rules

- **Clerk is the only authentication method.** Never implement custom auth, NextAuth, or any other auth library.
- Always `await auth()` — it returns a Promise in Clerk v7.
- Always scope database queries to the `userId` returned by `auth()`.
- The middleware file is `proxy.ts` (not `middleware.ts`) — never create or modify `middleware.ts`.

## Redirect Rules

- **Authenticated user visits `/`** → redirect to `/dashboard`.
- **Unauthenticated user visits `/dashboard`** → redirect to `/` (homepage). Do **not** use `auth.protect()` (which redirects to a sign-in page).

### Homepage redirect (`app/page.tsx`)

```ts
import { auth } from '@clerk/nextjs/server'
import { redirect } from 'next/navigation'

const { userId } = await auth()
if (userId) redirect('/dashboard')
```

### Dashboard protection (`proxy.ts`)

```ts
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server'
import { NextResponse } from 'next/server'

const isProtectedRoute = createRouteMatcher(['/dashboard(.*)'])

export default clerkMiddleware(async (auth, req) => {
  if (isProtectedRoute(req)) {
    const { userId } = await auth()
    if (!userId) {
      return NextResponse.redirect(new URL('/', req.url))
    }
  }
})
```

## Sign In / Sign Up — Modal Only

- Always use Clerk's `<SignInButton mode="modal">` and `<SignUpButton mode="modal">`.
- **Never** navigate to a dedicated `/sign-in` or `/sign-up` page.
- Use `<SignedIn>` / `<SignedOut>` to conditionally render auth controls.

```tsx
import { SignInButton, SignUpButton, SignedIn, SignedOut, UserButton } from '@clerk/nextjs'

<SignedOut>
  <SignInButton mode="modal"><button>Sign in</button></SignInButton>
  <SignUpButton mode="modal"><button>Sign up</button></SignUpButton>
</SignedOut>
<SignedIn>
  <UserButton />
</SignedIn>
```

## Forbidden Patterns

- No custom session handling, JWT parsing, or cookie-based auth.
- No `middleware.ts` — use `proxy.ts` only.
- No dedicated sign-in/sign-up pages or routes.
- Never access `userId` without `await`ing `auth()`.
