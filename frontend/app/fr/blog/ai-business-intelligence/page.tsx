import type { Metadata } from "next";
import AIBusinessIntelligenceArticle from "../../../blog/ai-business-intelligence/AIBusinessIntelligenceArticle";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Business Intelligence IA : transformer les données en meilleures décisions | Runexa",

  description:
    "Découvrez comment la business intelligence IA aide les équipes à analyser les données, détecter les risques, identifier les opportunités et améliorer la prise de décision stratégique.",

  keywords: [
    "Business intelligence IA",
    "aide à la décision par IA",
    "analyse KPI par IA",
    "analyse des données d'entreprise",
    "résumés exécutifs par IA",
    "Runexa Business Agent",
    "workflow métier IA",

    "agent IA pour les entreprises",
    "analyse stratégique par IA",
    "analyse des performances",
    "prise de décision commerciale",
    "analyse des risques business",
    "prévisions commerciales par IA",
    "business intelligence pour entreprises",
    "analyse des tendances du marché",
    "tableaux de bord intelligents",
    "rapports exécutifs IA",
    "analyse des opportunités commerciales",
    "analyse concurrentielle IA",
    "optimisation des performances",
    "assistant décisionnel IA",
    "gestion intelligente des entreprises",
    "analyse de données d'entreprise",
    "transformation numérique",
    "IA pour dirigeants",
    "automatisation de l'analyse métier",
    "Runexa Business Decision Agent",
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
