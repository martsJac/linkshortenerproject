# UI Standards — shadcn/ui

All UI in this project is built exclusively with **shadcn/ui** components. Custom components are forbidden.

## Rules

- **Always** use an existing shadcn/ui component. Never build a custom one.
- Install missing components via `npx shadcn@latest add <component>` — do not hand-roll them.
- Style with **Tailwind CSS v4** utility classes only. No inline styles, no CSS modules.
- Icons must come from **lucide-react** exclusively.
- The configured style is **radix-nova** — do not change `components.json`.

## Forbidden Patterns

```tsx
// ❌ Custom button — forbidden
export function MyButton({ children }) {
  return <button className="bg-blue-500 px-4 py-2">{children}</button>;
}

// ❌ Raw HTML form elements — forbidden
<input type="text" className="border p-2" />

// ❌ Inline styles — forbidden
<div style={{ color: "red" }} />
```

## Canonical Usage

```tsx
// ✅ Import from @/components/ui
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ExternalLink } from "lucide-react";

export function MyCard() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Short Link</CardTitle>
      </CardHeader>
      <CardContent className="flex gap-2">
        <Input placeholder="https://example.com" />
        <Button>
          <ExternalLink className="mr-2 h-4 w-4" />
          Shorten
        </Button>
      </CardContent>
    </Card>
  );
}
```

## Available Components

Check `components/ui/` for already-installed components before running the add command.
