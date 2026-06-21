import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Runexa Legal Agent Demo",

  description:
    "See a complete demonstration of the Runexa Legal Agent. Analyze contracts, detect risky clauses, extract obligations, summarize legal documents, and review compliance materials using AI.",

  keywords: [
    "Runexa Legal Agent",
    "legal AI demo",
    "AI contract analysis",
    "AI contract review",
    "legal document analysis",
    "contract risk detection",
    "AI legal assistant",
    "legal workflow AI",
    "legal AI",
    "contract analysis AI",
    "AI contract intelligence",
    "legal document review",
    "contract clause analysis",
    "contract risk analysis",
    "legal risk assessment",
    "AI legal technology",
    "LegalTech",
    "legal workflow automation",
    "legal document processing",
    "AI document analysis",
    "commercial contract review",
    "business contract analysis",
    "contract compliance analysis",
    "AI-powered legal review",
    "legal obligations analysis",
    "contract responsibilities analysis",
    "legal agreement analysis",
    "terms and conditions analysis",
    "contract insights",
    "contract summaries",
    "legal document summaries",
    "AI legal workflows",
    "enterprise legal AI",
    "legal operations AI",
    "AI for legal teams",
    "AI for lawyers",
    "AI for contract management",
    "contract lifecycle management",
    "legal risk detection",
    "document intelligence",
    "AI clause extraction",
    "AI compliance review",
    "contract due diligence",
    "legal decision support",
    "enterprise contract review",
    "AI contract assistant",
    "AI legal platform",
    "contract automation",
    "business legal intelligence",
    "Enterprise Legal AI",
  ],

  alternates: {
    canonical: "https://runexa.ai/en/demo/legal-agent",
    languages: {
      en: "https://runexa.ai/en/demo/legal-agent",
      fr: "https://runexa.ai/fr/demo/legal-agent",
      ar: "https://runexa.ai/ar/demo/legal-agent",
      "x-default": "https://runexa.ai/demo/legal-agent",
    },
  },

  openGraph: {
    title: "Runexa Legal Agent Demo",
    description:
      "See a complete demonstration of the Runexa Legal Agent. Analyze contracts, detect risky clauses, extract obligations, summarize legal documents, and review compliance materials using AI.",
    url: "https://runexa.ai/en/demo/legal-agent",
    siteName: "Runexa Systems",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Legal Agent Demo",
      },
    ],
    locale: "en_US",
    alternateLocale: ["fr_FR", "ar_AR"],
    type: "website",
  },

  twitter: {
    card: "summary_large_image",
    title: "Runexa Legal Agent Demo",
    description:
      "See a complete demonstration of the Runexa Legal Agent. Analyze contracts, detect risky clauses, extract obligations, summarize legal documents, and review compliance materials using AI.",
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
  name: "Runexa Legal Agent",
  applicationCategory: "BusinessApplication",
  operatingSystem: "Web",
  url: "https://runexa.ai/en/demo/legal-agent",
  inLanguage: "en",
  description:
    "See a complete demonstration of the Runexa Legal Agent. Analyze contracts, detect risky clauses, extract obligations, summarize legal documents, and review compliance materials using AI.",
  publisher: {
    "@type": "Organization",
    name: "Runexa Systems LLC",
    url: "https://runexa.ai",
  },
};

export default function LegalAgentDemoPage() {
  return (
    <main dir="ltr" className="min-h-screen bg-slate-50 px-6 py-16">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(jsonLd),
        }}
      />

      <div className="mx-auto max-w-6xl">
        <h1 className="text-5xl font-bold tracking-tight text-slate-900">
          Runexa Legal Agent Demo
        </h1>

        <p className="mt-6 max-w-3xl text-lg text-slate-600">
          Upload contracts, agreements, policies, and legal documents to
          generate AI-powered summaries, risky clause detection, obligation
          extraction, deadline insights, and structured legal analysis.
        </p>

        <div className="mt-10">
          <Image
            src="/demo/legal-agent-demo-en.png"
            alt="Runexa Legal Agent Demo"
            width={1440}
            height={5000}
            sizes="(max-width: 768px) 100vw, (max-width: 1280px) 90vw, 1152px"
            className="h-auto w-full rounded-3xl border border-slate-200 shadow-lg"
          />
        </div>

        <div className="mt-10 rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
          <h2 className="text-2xl font-bold text-slate-900">
            What can the Legal Agent do?
          </h2>

          <ul className="mt-4 space-y-3 text-slate-600">
            <li>✓ Analyze contracts and agreements</li>
            <li>✓ Detect risky clauses</li>
            <li>✓ Extract obligations and deadlines</li>
            <li>✓ Summarize legal documents</li>
            <li>✓ Review policies and compliance documents</li>
            <li>✓ Generate structured legal insights</li>
          </ul>
        </div>

        <div className="mt-10 text-center">
          <p className="mb-6 text-lg text-slate-600">
            Ready to analyze your own legal documents?
          </p>

          <Link
            href="/en/upload"
            className="inline-flex rounded-xl bg-blue-600 px-8 py-4 text-lg font-semibold text-white transition hover:bg-blue-700"
          >
            Try Legal Agent
          </Link>
        </div>
      </div>
    </main>
  );
}