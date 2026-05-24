import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Runexa Blog | Enterprise AI Insights",
  description:
    "Insights about AI contract analysis, finance AI, business intelligence, AI workflows, and enterprise AI systems.",
};

const articles = [
  {
    title: "AI Contract Analysis",
    href: "/blog/ai-contract-analysis",
    description:
      "How AI helps analyze contracts, risky clauses, and legal obligations.",
  },
  {
    title: "AI Finance Analysis",
    href: "/blog/ai-finance-analysis",
    description:
      "Using AI to understand spending patterns, subscriptions, and financial habits.",
  },
  {
    title: "AI Study Assistant",
    href: "/blog/ai-study-assistant",
    description:
      "How AI improves summaries, quizzes, flashcards, and learning workflows.",
  },
  {
    title: "Enterprise AI Workflows",
    href: "/blog/enterprise-ai-workflows",
    description:
      "How organizations build AI workflows for business operations and decision support.",
  },
  {
    title: "AI Business Intelligence",
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
              <h2 className="text-2xl font-bold">
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
      </section>
    </main>
  );
}