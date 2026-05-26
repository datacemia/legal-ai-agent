import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AI Financial Analysis & Personal Finance Coach | Runexa",

  description:
    "Analyze bank statements, spending patterns, subscriptions, savings opportunities, and financial habits with Runexa Finance Coach.",

  keywords: [
    "AI financial analysis",
    "personal finance AI",
    "AI finance coach",
    "bank statement analysis AI",
    "AI budgeting assistant",
    "subscription detection AI",
  ],

  alternates: {
    canonical: "https://runexa.ai/finance-ai",
  },

  openGraph: {
    title: "AI Financial Analysis & Personal Finance Coach | Runexa",
    description:
      "Analyze bank statements, subscriptions, savings opportunities, and financial habits with Runexa Finance Coach.",
    url: "https://runexa.ai/finance-ai",
    siteName: "Runexa Systems",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Finance Coach",
      },
    ],
    locale: "en_US",
    type: "website",
  },

  twitter: {
    card: "summary_large_image",
    title: "AI Financial Analysis & Personal Finance Coach | Runexa",
    description:
      "AI finance coach for bank statement analysis, subscriptions, savings opportunities, and budgeting.",
    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function FinanceAIPage() {
  return (
    <main className="min-h-screen bg-slate-50 px-6 py-20 text-slate-900">
      <section className="mx-auto max-w-6xl text-center">
        <p className="font-semibold text-emerald-600">
          Runexa Finance Coach
        </p>

        <h1 className="mt-4 text-5xl font-bold tracking-tight">
          AI Financial Analysis & Personal Finance Coach
        </h1>

        <p className="mx-auto mt-6 max-w-3xl text-lg text-slate-600">
          Runexa Finance Coach helps users analyze PDF bank statements,
          understand spending patterns, detect subscriptions, identify
          savings opportunities, and improve financial habits.
        </p>

        <div className="mt-8 flex flex-wrap justify-center gap-3">
          <Link
            href="/finance"
            className="rounded-xl bg-emerald-600 px-6 py-3 text-sm font-semibold text-white hover:bg-emerald-700"
          >
            Try Finance Coach
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
            "Bank statement analysis",
            "Upload PDF bank statements and receive structured financial insights.",
          ],
          [
            "Subscription detection",
            "Find recurring charges and review possible subscription waste.",
          ],
          [
            "Savings opportunities",
            "Identify practical ways to reduce expenses and improve cashflow.",
          ],
          [
            "AI finance coach",
            "Ask follow-up questions and get personalized explanations from your analysis.",
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
          How Runexa finance AI works
        </h2>

        <div className="mt-8 grid gap-4 md:grid-cols-3">
          {[
            "Upload a PDF bank statement",
            "Runexa analyzes transactions, subscriptions, spending, and cashflow",
            "Receive insights, charts, budget recommendations, and coaching",
          ].map((step, index) => (
            <div
              key={step}
              className="rounded-2xl bg-slate-50 p-6"
            >
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-600 text-sm font-bold text-white">
                {index + 1}
              </div>

              <p className="mt-4 font-semibold">{step}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto mt-16 max-w-6xl rounded-3xl border bg-white p-8 shadow-sm md:p-12">
        <h2 className="text-3xl font-bold">
          Finance AI FAQ
        </h2>

        <div className="mt-8 grid gap-4 md:grid-cols-2">
          {[
            [
              "Does Runexa replace a financial advisor?",
              "No. Runexa provides informational financial analysis and decision-support output. It does not replace professional financial advice.",
            ],
            [
              "What files can the Finance Coach analyze?",
              "Runexa Finance Coach is designed for PDF bank statements.",
            ],
            [
              "Can Runexa detect subscriptions?",
              "Yes. Runexa can identify recurring charges and highlight potential subscription spending patterns.",
            ],
            [
              "Can I ask questions after the analysis?",
              "Yes. The Finance Coach includes a conversational AI assistant for follow-up questions based on your analysis.",
            ],
          ].map(([q, a]) => (
            <div
              key={q}
              className="rounded-2xl bg-slate-50 p-6"
            >
              <h3 className="font-bold">{q}</h3>

              <p className="mt-2 text-sm leading-6 text-slate-600">
                {a}
              </p>
            </div>
          ))}
        </div>
      </section>

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            name: "Runexa Finance Coach",
            applicationCategory: "FinanceApplication",
            operatingSystem: "Web",
            description:
              "AI finance coach for bank statement analysis, subscription detection, savings opportunities, and financial habits.",
            url: "https://runexa.ai/finance-ai",
            publisher: {
              "@type": "Organization",
              name: "Runexa Systems",
              url: "https://runexa.ai",
            },
          }),
        }}
      />
    </main>
  );
}
