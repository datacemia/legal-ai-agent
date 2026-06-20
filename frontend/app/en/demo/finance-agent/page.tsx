import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Runexa Finance Coach Demo",

  description:
    "See a complete demonstration of the Runexa Finance Coach. Analyze financial documents, spending patterns, subscriptions, savings opportunities, and personal finance insights using AI.",

  keywords: [
  "Runexa Finance Coach",
  "finance AI demo",
  "AI finance analysis",
  "personal finance AI",
  "subscription detection AI",
  "spending analysis AI",
  "AI savings analysis",
  "financial coaching AI",

  "finance AI",
  "AI financial assistant",
  "AI personal finance coach",
  "AI money management",
  "expense analysis AI",
  "monthly spending analysis",
  "income and expense analysis",
  "bank statement analysis",
  "bank account analysis AI",
  "financial insights AI",
  "financial planning AI",
  "budget planning AI",
  "budget management AI",
  "AI budgeting assistant",
  "smart budgeting",
  "AI savings recommendations",
  "subscription management AI",
  "recurring expense detection",
  "cash flow analysis",
  "financial behavior analysis",
  "financial habits AI",
  "financial wellness AI",
  "financial education AI",
  "AI spending tracker",
  "personal finance management",
  "AI wealth management",
  "expense categorization AI",
  "financial dashboard AI",
  "AI financial reports",
  "AI money insights",
  "AI financial analytics",
  "consumer finance AI",
  "household budget AI",
  "AI finance platform",
  "financial decision support",
  "AI-powered budgeting",
  "AI financial coaching",
  "Finance AI",
  "Personal Finance AI",
  "AI Financial Assistant",
],

  alternates: {
    canonical: "https://runexa.ai/en/demo/finance-agent",
    languages: {
      en: "https://runexa.ai/en/demo/finance-agent",
      fr: "https://runexa.ai/fr/demo/finance-agent",
      ar: "https://runexa.ai/ar/demo/finance-agent",
      "x-default": "https://runexa.ai/demo/finance-agent",
    },
  },

  openGraph: {
    title: "Runexa Finance Coach Demo",

    description:
      "See a complete demonstration of the Runexa Finance Coach. Analyze financial documents, spending patterns, subscriptions, savings opportunities, and personal finance insights using AI.",

    url: "https://runexa.ai/en/demo/finance-agent",

    siteName: "Runexa Systems",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Finance Coach Demo",
      },
    ],

    locale: "en_US",

    alternateLocale: ["fr_FR", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Runexa Finance Coach Demo",

    description:
      "See a complete demonstration of the Runexa Finance Coach. Analyze financial documents, spending patterns, subscriptions, savings opportunities, and personal finance insights using AI.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

const jsonLd = {
  "@context": "https://schema.org",

  "@type": "SoftwareApplication",

  name: "Runexa Finance Coach",

  applicationCategory: "FinanceApplication",

  operatingSystem: "Web",

  url: "https://runexa.ai/en/demo/finance-agent",

  inLanguage: "en",

  description:
    "See a complete demonstration of the Runexa Finance Coach. Analyze financial documents, spending patterns, subscriptions, savings opportunities, and personal finance insights using AI.",

  publisher: {
    "@type": "Organization",
    name: "Runexa Systems LLC",
    url: "https://runexa.ai",
  },
};

export default function FinanceAgentDemoPage() {
  return (
    <main
      dir="ltr"
      className="min-h-screen bg-slate-50 px-6 py-16"
    >
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(jsonLd),
        }}
      />

      <div className="mx-auto max-w-6xl">
        <h1 className="text-5xl font-bold tracking-tight text-slate-900">
          Runexa Finance Coach Demo
        </h1>

        <p className="mt-6 max-w-3xl text-lg text-slate-600">
          Upload financial documents, statements, expense files, and personal finance data to generate AI-powered spending insights, subscription detection, savings opportunities, and personalized financial coaching.
        </p>

        <div className="mt-10">
          <Image
            src="/demo/finance-agent-demo-en.png"
            alt="Runexa Finance Coach Demo"
            width={1440}
            height={5000}
            priority
            className="rounded-3xl border border-slate-200 shadow-lg"
          />
        </div>

        <div className="mt-10 rounded-3xl border bg-white p-8 shadow-sm">
          <h2 className="text-2xl font-bold text-slate-900">
            What can the Finance Coach do?
          </h2>

          <ul className="mt-4 space-y-3 text-slate-600">
            <li>✓ Detect recurring subscriptions</li>
            <li>✓ Analyze spending patterns</li>
            <li>✓ Identify savings opportunities</li>
            <li>✓ Summarize financial activity</li>
            <li>✓ Highlight unusual or risky expenses</li>
            <li>✓ Generate personalized finance insights</li>
          </ul>
        </div>

        <div className="mt-10 text-center">
          <p className="mb-6 text-lg text-slate-600">
            Ready to analyze your own financial documents?
          </p>

          <Link
            href="/en/finance"
            className="inline-flex rounded-xl bg-blue-600 px-8 py-4 text-lg font-semibold text-white transition hover:bg-blue-700"
          >
            Try Finance Coach
          </Link>
        </div>
      </div>
    </main>
  );
}
