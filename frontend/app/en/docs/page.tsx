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
