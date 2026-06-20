import type { Metadata } from "next";
import DocsClient from "../../docs/DocsClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "AI API Documentation | Runexa",

  description:
    "Technical documentation for Runexa AI APIs including legal analysis, finance intelligence, business workflows, asynchronous jobs, authentication, and enterprise integrations.",

  keywords: [
  "Runexa docs",
  "AI API documentation",
  "legal AI API docs",
  "finance AI API docs",
  "business AI API docs",
  "developer documentation",
  "async AI APIs",
  "enterprise AI integration",

  "Runexa documentation",
  "Runexa developer docs",
  "Runexa API documentation",
  "Runexa Developers",
  "API reference",
  "API guides",
  "developer guides",
  "developer portal",
  "developer resources",
  "REST API documentation",
  "API integration guide",
  "API authentication",
  "API keys",
  "webhooks documentation",
  "SDK documentation",
  "AI SDK",
  "AI developer tools",
  "enterprise API documentation",
  "AI integration documentation",
  "asynchronous processing API",
  "async document processing",
  "document analysis API docs",
  "legal AI API documentation",
  "contract analysis API docs",
  "contract review API documentation",
  "finance AI API documentation",
  "bank statement analysis API docs",
  "study AI API documentation",
  "quiz generation API docs",
  "learning AI API documentation",
  "business intelligence API docs",
  "decision support API documentation",
  "KPI analysis API docs",
  "AI workflow API documentation",
  "AI agents API docs",
  "enterprise automation API docs",
  "cloud AI infrastructure",
  "secure AI APIs",
  "enterprise AI platform",
  "developer documentation portal",
  "technical documentation",
  "API examples",
  "API tutorials",
  "AI platform documentation",
  "enterprise AI integration guide",
],

  alternates: {
    canonical: "https://runexa.ai/en/docs",
    languages: {
      en: `${siteUrl}/en/docs`,
      fr: `${siteUrl}/fr/docs`,
      ar: `${siteUrl}/ar/docs`,
      "x-default": `${siteUrl}/docs`,
    },
  },

  openGraph: {
    title: "AI API Documentation | Runexa",

    description:
      "Technical documentation for Runexa AI APIs including legal analysis, finance intelligence, business workflows, asynchronous jobs, authentication, and enterprise integrations.",

    url: "https://runexa.ai/en/docs",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa API Documentation",
      },
    ],

    locale: "en_US",

    alternateLocale: ["fr_FR", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "AI API Documentation | Runexa",

    description:
      "Technical developer documentation for Runexa asynchronous AI APIs.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function DocsPage() {
  return (
    <>
      <DocsClient initialLocale="en" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "TechArticle",

            headline: "AI API Documentation | Runexa",

            name: "Runexa API Documentation",

            description:
              "Technical documentation for Runexa asynchronous AI APIs, authentication, jobs, legal analysis, finance intelligence, study automation, business workflows, and enterprise integrations.",

            url: "https://runexa.ai/en/docs",

            inLanguage: "en",

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: siteUrl,
            },

            about: [
              "AI API Documentation",
              "Async AI APIs",
              "Legal AI API Docs",
              "Finance AI API Docs",
              "Business AI API Docs",
              "Enterprise AI Integration",
            ],
          }),
        }}
      />
    </>
  );
}
