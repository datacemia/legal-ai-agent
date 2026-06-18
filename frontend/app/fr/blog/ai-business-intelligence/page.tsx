import type { Metadata } from "next";
import AIBusinessIntelligenceArticle from "../../../blog/ai-business-intelligence/AIBusinessIntelligenceArticle";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Business Intelligence IA : transformer les données en meilleures décisions | Runexa",

  description:
    "Découvrez comment la business intelligence IA aide les équipes à analyser les données, détecter les risques, identifier les opportunités et améliorer la prise de décision stratégique.",

  keywords: [
    "business intelligence IA",
    "intelligence d’affaires IA",
    "aide à la décision IA",
    "analyse KPI IA",
    "analyse données business",
    "résumés exécutifs IA",
    "Runexa Business Agent",
    "workflows business IA",
  ],

  alternates: {
    canonical: "https://runexa.ai/fr/blog/ai-business-intelligence",
    languages: {
      en: `${siteUrl}/en/blog/ai-business-intelligence`,
      fr: `${siteUrl}/fr/blog/ai-business-intelligence`,
      ar: `${siteUrl}/ar/blog/ai-business-intelligence`,
      "x-default": `${siteUrl}/blog/ai-business-intelligence`,
    },
  },

  openGraph: {
    title: "Business Intelligence IA : transformer les données en meilleures décisions | Runexa",

    description:
      "Découvrez comment la business intelligence IA aide les équipes à analyser les données, détecter les risques, identifier les opportunités et améliorer la prise de décision stratégique.",

    url: "https://runexa.ai/fr/blog/ai-business-intelligence",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa AI Business Intelligence",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "article",
  },

  twitter: {
    card: "summary_large_image",

    title: "Business Intelligence IA : transformer les données en meilleures décisions | Runexa",

    description:
      "Découvrez comment la business intelligence IA aide les équipes à analyser les données, détecter les risques, identifier les opportunités et améliorer la prise de décision stratégique.",

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
      <AIBusinessIntelligenceArticle initialLocale="fr" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "Article",

            headline:
              "Business Intelligence IA : transformer les données en meilleures décisions",

            description:
              "Découvrez comment la business intelligence IA aide les équipes à analyser les données, détecter les risques, identifier les opportunités et améliorer la prise de décision stratégique.",

            datePublished: "2026-05-24",

            dateModified: "2026-05-24",

            inLanguage: "fr",

            mainEntityOfPage: {
              "@type": "WebPage",
              "@id": "https://runexa.ai/fr/blog/ai-business-intelligence",
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
