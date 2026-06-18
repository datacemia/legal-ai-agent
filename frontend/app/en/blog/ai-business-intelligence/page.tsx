import type { Metadata } from "next";
import AIBusinessIntelligenceArticle from "../../../blog/ai-business-intelligence/AIBusinessIntelligenceArticle";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "AI Business Intelligence: Turning Data into Better Decisions | Runexa",

  description:
    "Learn how AI business intelligence helps teams analyze data, detect risks, identify opportunities, and improve strategic decision-making.",

  keywords: [
    "AI business intelligence",
    "business intelligence AI",
    "AI decision support",
    "AI KPI analysis",
    "business data analysis",
    "AI executive summaries",
    "Runexa Business Agent",
    "AI business workflows",
  ],

  alternates: {
    canonical: "https://runexa.ai/en/blog/ai-business-intelligence",
    languages: {
      en: `${siteUrl}/en/blog/ai-business-intelligence`,
      fr: `${siteUrl}/fr/blog/ai-business-intelligence`,
      ar: `${siteUrl}/ar/blog/ai-business-intelligence`,
      "x-default": `${siteUrl}/blog/ai-business-intelligence`,
    },
  },

  openGraph: {
    title: "AI Business Intelligence: Turning Data into Better Decisions | Runexa",

    description:
      "Learn how AI business intelligence helps teams analyze data, detect risks, identify opportunities, and improve strategic decision-making.",

    url: "https://runexa.ai/en/blog/ai-business-intelligence",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa AI Business Intelligence",
      },
    ],

    locale: "en_US",

    alternateLocale: ["fr_FR", "ar_AR"],

    type: "article",
  },

  twitter: {
    card: "summary_large_image",

    title: "AI Business Intelligence: Turning Data into Better Decisions | Runexa",

    description:
      "Learn how AI business intelligence helps teams analyze data, detect risks, identify opportunities, and improve strategic decision-making.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function AIBusinessIntelligencePage() {
  return (
    <>
      <AIBusinessIntelligenceArticle initialLocale="en" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "Article",

            headline:
              "AI Business Intelligence: Turning Data into Better Decisions",

            description:
              "Learn how AI business intelligence helps teams analyze data, detect risks, identify opportunities, and improve strategic decision-making.",

            datePublished: "2026-05-24",

            dateModified: "2026-05-24",

            inLanguage: "en",

            mainEntityOfPage: {
              "@type": "WebPage",
              "@id": "https://runexa.ai/en/blog/ai-business-intelligence",
            },

            author: {
              "@type": "Person",
              name: "Dr. Rachid Ejjami",
            },

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: siteUrl,
            },
          }),
        }}
      />
    </>
  );
}
