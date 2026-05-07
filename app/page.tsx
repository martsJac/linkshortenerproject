import { auth } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import { SignUpButton, SignInButton } from "@clerk/nextjs";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Link2,
  BarChart3,
  Shield,
  Zap,
  ArrowRight,
  Copy,
  MousePointerClick,
} from "lucide-react";

const features = [
  {
    icon: Zap,
    title: "Instant Shortening",
    description:
      "Paste any long URL and get a clean, shareable short link in one click.",
  },
  {
    icon: BarChart3,
    title: "Click Analytics",
    description:
      "Track how many times your links are clicked and measure your reach.",
  },
  {
    icon: Shield,
    title: "Secure & Private",
    description:
      "Your links are tied to your account — only you can manage or delete them.",
  },
  {
    icon: Copy,
    title: "Easy to Share",
    description:
      "Copy your short link with a single click and share it anywhere.",
  },
];

const steps = [
  {
    number: "1",
    icon: Link2,
    title: "Paste your URL",
    description: "Drop any long link into the input field on your dashboard.",
  },
  {
    number: "2",
    icon: Zap,
    title: "Get your short link",
    description: "We generate a compact slug you can share instantly.",
  },
  {
    number: "3",
    icon: MousePointerClick,
    title: "Track & manage",
    description: "Monitor clicks and manage all your links from one place.",
  },
];

export default async function Home() {
  const { userId } = await auth();
  if (userId) redirect("/dashboard");

  return (
    <div className="flex flex-col flex-1">
      {/* Hero */}
      <section className="flex flex-col items-center justify-center text-center py-24 px-4 gap-6">
        <Badge variant="secondary" className="text-sm px-4 py-1">
          Free URL Shortener
        </Badge>
        <h1 className="text-5xl font-bold tracking-tight leading-tight max-w-2xl">
          Shorten URLs.
          <br />
          Share Smarter.
        </h1>
        <p className="text-xl text-muted-foreground max-w-xl leading-relaxed">
          Transform long, unwieldy links into short, shareable URLs in seconds.
          Track your clicks and manage all your links from one dashboard.
        </p>
        <div className="flex gap-4 mt-2">
          <SignUpButton mode="modal">
            <Button size="lg">
              <span className="flex items-center gap-2">
                Get Started Free
                <ArrowRight className="h-4 w-4" />
              </span>
            </Button>
          </SignUpButton>
        </div>
      </section>

      {/* Features */}
      <section className="py-16 px-4">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-3">
            Everything you need
          </h2>
          <p className="text-center text-muted-foreground mb-12">
            A simple, powerful toolkit for managing your links.
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature) => (
              <Card key={feature.title}>
                <CardHeader className="pb-2">
                  <feature.icon className="h-8 w-8 mb-2 text-primary" />
                  <CardTitle className="text-base">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    {feature.description}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-16 px-4 bg-muted/30">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-3">How it works</h2>
          <p className="text-center text-muted-foreground mb-12">
            Three steps to a shorter, smarter link.
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-8">
            {steps.map((step) => (
              <div
                key={step.number}
                className="flex flex-col items-center text-center gap-3"
              >
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary text-primary-foreground text-lg font-bold">
                  {step.number}
                </div>
                <step.icon className="h-6 w-6 text-muted-foreground" />
                <h3 className="font-semibold">{step.title}</h3>
                <p className="text-sm text-muted-foreground">
                  {step.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="flex flex-col items-center justify-center text-center py-20 px-4 gap-6">
        <h2 className="text-3xl font-bold">Ready to get started?</h2>
        <p className="text-muted-foreground max-w-md">
          Create a free account and start shortening links in under a minute.
        </p>
        <SignUpButton mode="modal">
          <Button size="lg">
            Create Free Account
            <ArrowRight className="ml-2 h-4 w-4" />
          </Button>
        </SignUpButton>
      </section>
    </div>
  );
}
