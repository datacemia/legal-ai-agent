import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AI Business Intelligence & Decision Support | Runexa",
  description:
    "Analyze business data, risks, opportunities, and strategic decisions with Runexa Business Agent.",
};

export default function BusinessAIPage() {
  return (
    <main className="min-h-screen bg-slate-50 px-6 py-20 text-slate-900">
      <section className="mx-auto max-w-6xl text-center">
        <p className="font-semibold text-amber-600">
          Runexa Business Agent
        </p>

        <h1 className="mt-4 text-5xl font-bold tracking-tight">
          AI Business Intelligence & Decision Support
        </h1>

        <p className="mx-auto mt-6 max-w-3xl text-lg text-slate-600">
          Runexa Business Agent helps founders, professionals, and organizations
          analyze business data, identify risks, discover opportunities, and
          improve strategic decision-making with AI.
        </p>

        <div className="mt-8 flex flex-wrap justify-center gap-3">
          <Link
            href="/business"
            className="rounded-xl bg-amber-600 px-6 py-3 text-sm font-semibold text-white hover:bg-amber-700"
          >
            Analyze Business Data
          </Link>

          <Link
            href="/pricing"
            className="rounded-xl border border-slate-200 bg-white px-6 py-3 text-sm font-semibold text-slate-900 hover:bg-slate-50"
          >
            View Pricing
          </Link>
        </div>
      </section>

      <section className="mx-auto mt-16 grid max-w-6xl gap-6 md:grid-cols-4">
        {[
          ["Business intelligence", "Transform business data into structured insights and recommendations."],
          ["Risk analysis", "Identify operational, strategic, and financial risk signals."],
          ["Opportunity detection", "Discover growth opportunities and strategic improvements."],
          ["AI decision support", "Receive practical AI-assisted business recommendations."],
        ].map(([title, desc]) => (
          <div key={title} className="rounded-2xl border bg-white p-6 shadow-sm">
            <h2 className="font-bold">{title}</h2>
            <p className="mt-3 text-sm leading-6 text-slate-600">{desc}</p>
          </div>
        ))}
      </section>

      <section className="mx-auto mt-16 max-w-6xl rounded-3xl border bg-white p-8 shadow-sm md:p-12">
        <h2 className="text-3xl font-bold">
          How Runexa business AI works
        </h2>

        <div className="mt-8 grid gap-4 md:grid-cols-3">
          {[
            "Upload business files or reports",
            "Runexa analyzes risks, opportunities, and strategic signals",
            "Receive structured business intelligence insights",
          ].map((step, index) => (
            <div key={step} className="rounded-2xl bg-slate-50 p-6">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-amber-600 text-sm font-bold text-white">
                {index + 1}
              </div>

              <p className="mt-4 font-semibold">{step}</p>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}