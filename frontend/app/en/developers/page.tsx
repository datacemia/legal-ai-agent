import type { Metadata } from "next";
import DevelopersClient from "../../developers/DevelopersClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Developers & AI APIs | Runexa",

  description:
    "Build AI-powered workflows with Runexa APIs for legal analysis, finance intelligence, study automation, and business decision support.",

  keywords: [
  "Runexa developers",
  "AI API",
  "legal AI API",
  "finance AI API",
  "study AI API",
  "business AI API",
  "AI workflow API",
  "developer AI tools",
  "enterprise AI API",

  "Runexa API",
  "Runexa developer platform",
  "Runexa API documentation",
  "AI developer platform",
  "AI integration",
  "enterprise AI integration",
  "AI services API",
  "AI platform API",
  "REST API",
  "developer API",
  "API documentation",
  "API reference",
  "AI SDK",
  "developer SDK",
  "AI developer tools",
  "API authentication",
  "API keys",
  "webhooks",
  "asynchronous AI processing",
  "async document processing",
  "document analysis API",
  "AI document processing API",
  "contract analysis API",
  "contract review API",
  "legal document API",
  "financial analysis API",
  "bank statement analysis API",
  "personal finance API",
  "learning AI API",
  "education AI API",
  "quiz generation API",
  "study assistant API",
  "business intelligence API",
  "decision support API",
  "KPI analysis API",
  "enterprise automation API",
  "AI agents API",
  "specialized AI agents API",
  "AI infrastructure",
  "scalable AI APIs",
  "secure AI APIs",
  "cloud AI infrastructure",
  "SaaS AI API",
  "enterprise developer tools",
  "AI processing platform",
  "developer documentation",
  "enterprise AI platform",
],

  alternates: {
    canonical: "https://runexa.ai/en/developers",
    languages: {
      en: `${siteUrl}/en/developers`,
      fr: `${siteUrl}/fr/developers`,
      ar: `${siteUrl}/ar/developers`,
      "x-default": `${siteUrl}/developers`,
    },
  },

  openGraph: {
    title: "Developers & AI APIs | Runexa",

    description:
      "Build AI-powered workflows with Runexa APIs for legal analysis, finance intelligence, study automation, and business decision support.",

    url: "https://runexa.ai/en/developers",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Developers",
      },
    ],

    locale: "en_US",

    alternateLocale: ["fr_FR", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Developers & AI APIs | Runexa",

    description:
      "Build AI-powered workflows with Runexa APIs for legal analysis, finance intelligence, study automation, and business decision support.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function DevelopersPage() {
  return (
    <>
      <DevelopersClient initialLocale="en" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "TechArticle",

            headline: "Developers & AI APIs | Runexa",

            name: "Runexa Developers",

            description:
              "Developer platform for building AI-powered workflows with Runexa APIs for legal analysis, finance intelligence, study automation, and business decision support.",

            url: "https://runexa.ai/en/developers",

            inLanguage: "en",

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: siteUrl,
            },

            about: [
              "AI APIs",
              "Developer APIs",
              "Legal AI API",
              "Finance AI API",
              "Study AI API",
              "Business AI API",
              "AI Workflow Automation",
            ],
          }),
        }}
      />
    </>
  );
}
