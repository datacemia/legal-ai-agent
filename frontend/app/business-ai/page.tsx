import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AI Business Intelligence & KPI Analysis Platform | Runexa",
  description:
    "Use Runexa Business Agent to analyze KPIs, business risks, opportunities, forecasts, and executive insights with AI-powered business intelligence.",
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
          [
            "Business intelligence",
            "Transform business data into structured insights and recommendations.",
          ],
          [
            "Risk analysis",
            "Identify operational, strategic, and financial risk signals.",
          ],
          [
            "Opportunity detection",
            "Discover growth opportunities and strategic improvements.",
          ],
          [
            "AI decision support",
            "Receive practical AI-assisted business recommendations.",
          ],
        ].map(([title, desc]) => (
          <div
            key={title}
            className="rounded-2xl border bg-white p-6 shadow-sm"
          >
            <h2 className="font-bold">{title}</h2>
            <p className="mt-3 text-sm leading-6 text-slate-600">
              {desc}
            </p>
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

      <section className="mx-auto mt-16 max-w-6xl">
        <h2 className="text-3xl font-bold">
          AI business intelligence for modern teams
        </h2>

        <p className="mt-5 max-w-4xl text-lg leading-8 text-slate-600">
          Runexa Business Agent is designed for business owners, founders,
          analysts, consultants, and teams that need faster insight from
          business data. Instead of manually reviewing spreadsheets, reports,
          KPIs, and operational signals, Runexa turns business information into
          structured analysis, risk detection, opportunities, forecasts, and
          decision recommendations.
        </p>

        <p className="mt-5 max-w-4xl text-lg leading-8 text-slate-600">
          The platform helps users understand revenue performance, expense
          trends, profitability, business health, operational risks, customer
          signals, and strategic priorities. It is built for practical business
          decision support, not generic chatbot responses.
        </p>
      </section>

      <section className="mx-auto mt-16 max-w-6xl rounded-3xl border bg-white p-8 shadow-sm md:p-12">
        <h2 className="text-3xl font-bold">
          Business AI use cases
        </h2>

        <div className="mt-8 grid gap-6 md:grid-cols-2">
          {[
            [
              "KPI analysis",
              "Analyze revenue, expenses, profit, growth, cashflow, and operational performance indicators.",
            ],
            [
              "Business risk detection",
              "Identify weak margins, poor data quality, cashflow issues, declining performance, or operational warning signs.",
            ],
            [
              "AI business reports",
              "Generate executive-style business summaries that explain what is happening and what actions matter most.",
            ],
            [
              "Decision support",
              "Turn business data into practical recommendations for pricing, cost control, growth, and strategy.",
            ],
          ].map(([title, desc]) => (
            <div key={title} className="rounded-2xl bg-slate-50 p-6">
              <h3 className="font-bold">{title}</h3>
              <p className="mt-3 text-sm leading-6 text-slate-600">
                {desc}
              </p>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto mt-16 max-w-6xl">
        <h2 className="text-3xl font-bold">
          Frequently asked questions
        </h2>

        <div className="mt-8 space-y-4">
          {[
            [
              "What is AI business intelligence?",
              "AI business intelligence uses artificial intelligence to analyze business data, detect patterns, identify risks, and generate decision-ready insights.",
            ],
            [
              "Can Runexa analyze spreadsheets?",
              "Yes. Runexa Business Agent can analyze business files and transform them into structured KPI analysis, risks, opportunities, and recommendations.",
            ],
            [
              "Who should use Runexa Business Agent?",
              "It is useful for founders, business owners, consultants, finance teams, analysts, and organizations that need faster business decision support.",
            ],
            [
              "Does Runexa replace business consultants?",
              "No. Runexa provides decision support and analysis. Important business, legal, financial, or strategic decisions should still be reviewed by qualified professionals.",
            ],
          ].map(([question, answer]) => (
            <div
              key={question}
              className="rounded-2xl border bg-white p-6 shadow-sm"
            >
              <h3 className="font-bold">{question}</h3>
              <p className="mt-3 text-sm leading-6 text-slate-600">
                {answer}
              </p>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
