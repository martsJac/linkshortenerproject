import { auth } from '@clerk/nextjs/server'
import { redirect } from 'next/navigation'
import { getLinksByUserId } from '@/data/links'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { ExternalLink } from 'lucide-react'

export default async function DashboardPage() {
  const { userId } = await auth()
  if (!userId) redirect('/')

  const links = await getLinksByUserId(userId)

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-2xl font-bold mb-6">Your Links</h1>
      {links.length === 0 ? (
        <p className="text-muted-foreground">You have no links yet.</p>
      ) : (
        <div className="flex flex-col gap-4">
          {links.map((link) => (
            <Card key={link.id}>
              <CardHeader className="pb-2">
                <CardTitle className="text-base flex items-center gap-2">
                  <Badge variant="secondary">{link.shortCode}</Badge>
                  <span className="text-muted-foreground font-normal truncate">
                    {link.originalUrl}
                  </span>
                </CardTitle>
              </CardHeader>
              <CardContent className="flex items-center gap-2 text-sm text-muted-foreground">
                <a
                  href={link.originalUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-1 hover:underline"
                >
                  <ExternalLink className="h-4 w-4" />
                  Visit original
                </a>
                <span>·</span>
                <span>Created {link.createdAt.toLocaleDateString()}</span>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
