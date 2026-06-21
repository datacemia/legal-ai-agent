import type { Metadata } from "next";
import ApiClient from "./ApiClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "AI APIs & Agent Infrastructure | Runexa",

  description:
    "Integrate Runexa AI APIs for legal analysis, finance intelligence, study automation, and business decision support workflows.",

  keywords: [
  "Runexa API",
  "AI APIs",
  "legal AI API",
  "finance AI API",
  "study AI API",
  "business AI API",
  "async AI processing",
  "AI infrastructure",

  "Runexa developer API",
  "Runexa APIs",
  "enterprise AI API",
  "AI workflow API",
  "AI automation API",
  "AI integration API",
  "AI platform API",
  "REST API",
  "RESTful API",
  "developer platform",
  "developer tools",
  "developer documentation",
  "API documentation",
  "API reference",
  "API authentication",
  "API keys",
  "webhooks",
  "asynchronous processing",
  "async API",
  "background AI processing",
  "AI job processing",
  "AI infrastructure",
  "AI backend infrastructure",
  "enterprise integrations",
  "enterprise AI integrations",
  "custom AI integrations",
  "workflow automation API",
  "document analysis API",
  "document intelligence API",
  "contract analysis API",
  "legal document API",
  "legal AI API",
  "finance AI API",
  "bank statement analysis API",
  "financial intelligence API",
  "study AI API",
  "learning AI API",
  "business AI API",
  "business intelligence API",
  "decision support API",
  "AI agents API",
  "specialized AI APIs",
  "AI microservices",
  "scalable AI APIs",
  "cloud AI infrastructure",
  "enterprise developer platform",
  "Runexa API documentation",
  "AI SDK",
  "enterprise AI architecture",
],

  alternates: {
    canonical: "https://runexa.ai/api",
    languages: {
      en: `${siteUrl}/en/api`,
      fr: `${siteUrl}/fr/api`,
      ar: `${siteUrl}/ar/api`,
      "x-default": `${siteUrl}/api`,
    },
  },

  openGraph: {
    title: "AI APIs & Agent Infrastructure | Runexa",

    description:
      "Integrate Runexa AI APIs for legal analysis, finance intelligence, study automation, and business decision support workflows.",

    url: "https://runexa.ai/api",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa API Platform",
      },
    ],

    locale: "en_US",

    alternateLocale: ["fr_FR", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "AI APIs & Agent Infrastructure | Runexa",

    description:
      "AI APIs for legal, finance, study, and business automation workflows.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function ApiPage() {
  return (
    <>
      <ApiClient initialLocale="en" />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "SoftwareApplication",

            name: "Runexa API Platform",

            applicationCategory: "DeveloperApplication",

            operatingSystem: "Web",

            description:
              "Runexa AI API platform for legal analysis, finance intelligence, study automation, business decision support, asynchronous processing, and agent infrastructure.",

            url: "https://runexa.ai/api",

            inLanguage: "en",

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: siteUrl,
            },

            knowsAbout: [
              "AI APIs",
              "Legal AI API",
              "Finance AI API",
              "Study AI API",
              "Business AI API",
              "Async AI Processing",
              "AI Infrastructure",
            ],
          }),
        }}
      />
    </>
  );
}
