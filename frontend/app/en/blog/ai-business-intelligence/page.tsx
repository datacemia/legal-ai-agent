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

  "Runexa Business Decision Agent",
  "business analytics AI",
  "AI business insights",
  "AI-powered decision making",
  "executive decision support",
  "AI strategy analysis",
  "business performance analysis",
  "AI performance dashboards",
  "KPI monitoring AI",
  "AI forecasting",
  "business forecasting AI",
  "AI risk analysis",
  "business risk assessment",
  "AI market analysis",
  "AI operational intelligence",
  "enterprise business intelligence",
  "business process optimization",
  "AI productivity insights",
  "AI management reporting",
  "executive dashboards",
  "business reporting AI",
  "data-driven decision making",
  "AI business recommendations",
  "AI for executives",
  "AI for managers",
  "business operations AI",
  "enterprise analytics platform",
  "AI business automation",
  "workflow intelligence",
  "AI workflow optimization",
  "AI data visualization",
  "AI trend analysis",
  "AI strategic planning",
  "business intelligence platform",
  "enterprise AI insights",
  "AI corporate intelligence",
  "AI business platform",
  "AI enterprise workflows",
  "Business AI",
  "Enterprise Business Intelligence",
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
