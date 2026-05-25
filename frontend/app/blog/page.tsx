import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title:
    "Runexa AI Blog | Legal AI, Finance AI, Business Intelligence & Study AI",
  description:
    "Insights about AI contract analysis, finance AI, business intelligence, AI workflows, and enterprise AI systems.",
  keywords: [
    "AI blog",
    "legal AI",
    "finance AI",
    "AI business intelligence",
    "AI study assistant",
    "enterprise AI",
    "AI workflows",
  ],
  alternates: {
    canonical: "https://runexa.ai/blog",
  },
  openGraph: {
    title:
      "Runexa AI Blog | Legal AI, Finance AI, Business Intelligence & Study AI",
    description:
      "Insights about AI contract analysis, finance AI, business intelligence, AI workflows, and enterprise AI systems.",
    url: "https://runexa.ai/blog",
    siteName: "Runexa",
    type: "website",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa AI Blog",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title:
      "Runexa AI Blog | Legal AI, Finance AI, Business Intelligence & Study AI",
    description:
      "Insights about AI contract analysis, finance AI, business intelligence, AI workflows, and enterprise AI systems.",
    images: ["/og-image.png"],
  },
};

const articles = [
  {
    title: "AI Contract Analysis",
    category: "Legal AI",
    href: "/blog/ai-contract-analysis",
    description:
      "How AI helps analyze contracts, risky clauses, and legal obligations.",
  },
  {
    title: "AI Finance Analysis",
    category: "Finance AI",
    href: "/blog/ai-finance-analysis",
    description:
      "Using AI to understand spending patterns, subscriptions, and financial habits.",
  },
  {
    title: "AI Study Assistant",
    category: "Study AI",
    href: "/blog/ai-study-assistant",
    description:
      "How AI improves summaries, quizzes, flashcards, and learning workflows.",
  },
  {
    title: "Enterprise AI Workflows",
    category: "Enterprise AI",
    href: "/blog/enterprise-ai-workflows",
    description:
      "How organizations build AI workflows for business operations and decision support.",
  },
  {
    title: "AI Business Intelligence",
    category: "Business AI",
    href: "/blog/ai-business-intelligence",
    description:
      "Using AI to analyze business data, risks, and strategic opportunities.",
  },
];

export default function BlogPage() {
  return (
    <main className="min-h-screen bg-slate-50 px-6 py-20 text-slate-900">
      <section className="mx-auto max-w-6xl">
        <p className="font-semibold text-blue-600">
          Runexa Blog
        </p>

        <h1 className="mt-4 text-5xl font-bold tracking-tight">
          Enterprise AI Insights & Workflows
        </h1>

        <p className="mt-6 max-w-3xl text-lg text-slate-600">
          Insights about AI document analysis, finance AI, legal AI,
          business intelligence, enterprise AI systems, and intelligent workflows.
        </p>

        <div className="mt-12 grid gap-6 md:grid-cols-2">
          {articles.map((article) => (
            <Link
              key={article.href}
              href={article.href}
              className="rounded-3xl border bg-white p-8 shadow-sm transition hover:-translate-y-1 hover:shadow-md"
            >
              <p className="text-sm font-semibold text-blue-600">
                {article.category}
              </p>

              <h2 className="mt-3 text-2xl font-bold">
                {article.title}
              </h2>

              <p className="mt-4 leading-7 text-slate-600">
                {article.description}
              </p>

              <div className="mt-6 text-sm font-semibold text-blue-600">
                Read article →
              </div>
            </Link>
          ))}
        </div>

        <section className="mt-20 rounded-3xl bg-blue-600 p-10 text-white">
          <h2 className="text-3xl font-bold">
            Explore enterprise AI workflows with Runexa
          </h2>

          <p className="mt-4 max-w-2xl text-blue-100">
            Analyze contracts, financial statements, business data,
            and study materials with specialized AI agents.
          </p>

          <div className="mt-8 flex flex-wrap gap-4">
            <Link
              href="/pricing"
              className="rounded-xl bg-white px-6 py-3 text-sm font-semibold text-blue-600"
            >
              View Pricing
            </Link>

            <Link
              href="/developers"
              className="rounded-xl border border-blue-300 px-6 py-3 text-sm font-semibold text-white"
            >
              Developers
            </Link>
          </div>
        </section>
      </section>

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "Blog",
            name: "Runexa AI Blog",
            description:
              "Insights about legal AI, finance AI, enterprise AI workflows, business intelligence, and AI-powered operational systems.",
            url: "https://runexa.ai/blog",
            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
            },
          }),
        }}
      />
    </main>
  );
}
