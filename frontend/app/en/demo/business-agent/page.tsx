import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Runexa Business Decision Agent Demo",

  description:
    "See a complete demonstration of the Runexa Business Decision Agent. Analyze business data, KPIs, risks, opportunities, forecasts, and executive decision insights using AI.",

  keywords: [
    "Runexa Business Decision Agent",
    "business AI demo",
    "AI business intelligence",
    "business decision support",
    "AI KPI analysis",
    "business risk analysis",
    "AI forecasting",
    "executive decision AI",
  ],

  alternates: {
    canonical: "https://runexa.ai/en/demo/business-agent",
    languages: {
      en: "https://runexa.ai/en/demo/business-agent",
      fr: "https://runexa.ai/fr/demo/business-agent",
      ar: "https://runexa.ai/ar/demo/business-agent",
      "x-default": "https://runexa.ai/demo/business-agent",
    },
  },

  openGraph: {
    title: "Runexa Business Decision Agent Demo",

    description:
      "See a complete demonstration of the Runexa Business Decision Agent. Analyze business data, KPIs, risks, opportunities, forecasts, and executive decision insights using AI.",

    url: "https://runexa.ai/en/demo/business-agent",

    siteName: "Runexa Systems",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Business Decision Agent Demo",
      },
    ],

    locale: "en_US",

    alternateLocale: ["fr_FR", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Runexa Business Decision Agent Demo",

    description:
      "See a complete demonstration of the Runexa Business Decision Agent. Analyze business data, KPIs, risks, opportunities, forecasts, and executive decision insights using AI.",

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

  name: "Runexa Business Decision Agent",

  applicationCategory: "BusinessApplication",

  operatingSystem: "Web",

  url: "https://runexa.ai/en/demo/business-agent",

  inLanguage: "en",

  description:
    "See a complete demonstration of the Runexa Business Decision Agent. Analyze business data, KPIs, risks, opportunities, forecasts, and executive decision insights using AI.",

  publisher: {
    "@type": "Organization",
    name: "Runexa Systems LLC",
    url: "https://runexa.ai",
  },
};

export default function BusinessAgentDemoPage() {
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
          Runexa Business Decision Agent Demo
        </h1>

        <p className="mt-6 max-w-3xl text-lg text-slate-600">
          Upload business reports, KPI files, sales data, operational documents, and strategic notes to generate AI-powered executive summaries, risks, opportunities, forecasts, and decision support.
        </p>

        <div className="mt-10">
          <Image
            src="/demo/business-agent-demo-en.png"
            alt="Runexa Business Decision Agent Demo"
            width={1440}
            height={5000}
            priority
            className="rounded-3xl border border-slate-200 shadow-lg"
          />
        </div>

        <div className="mt-10 rounded-3xl border bg-white p-8 shadow-sm">
          <h2 className="text-2xl font-bold text-slate-900">
            What can the Business Decision Agent do?
          </h2>

          <ul className="mt-4 space-y-3 text-slate-600">
            <li>✓ Analyze KPIs and business performance</li>
            <li>✓ Detect risks and operational issues</li>
            <li>✓ Identify strategic opportunities</li>
            <li>✓ Generate executive summaries</li>
            <li>✓ Support forecasting and decision-making</li>
            <li>✓ Transform business data into clear insights</li>
          </ul>
        </div>

        <div className="mt-10 text-center">
          <p className="mb-6 text-lg text-slate-600">
            Ready to analyze your own business data?
          </p>

          <Link
            href="/en/business"
            className="inline-flex rounded-xl bg-blue-600 px-8 py-4 text-lg font-semibold text-white transition hover:bg-blue-700"
          >
            Try Business Agent
          </Link>
        </div>
      </div>
    </main>
  );
}
