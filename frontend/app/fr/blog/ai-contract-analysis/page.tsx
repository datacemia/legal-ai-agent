import type { Metadata } from "next";
import AIContractAnalysisArticle from "../../../blog/ai-contract-analysis/AIContractAnalysisArticle";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Analyse de contrats par IA : comment l’IA aide à examiner les documents juridiques | Runexa",

  description:
    "Découvrez comment l’analyse de contrats par IA aide à identifier les clauses risquées, résumer les obligations et soutenir les workflows d’examen juridique.",

  keywords: [
    "analyse de contrats IA",
    "examen de contrats IA",
    "analyse documents juridiques",
    "IA juridique",
    "détection risques contrat",
    "assistant juridique IA",
    "résumés de contrats",
    "Runexa Legal Agent",
  ],

  alternates: {
    canonical: "https://runexa.ai/fr/blog/ai-contract-analysis",
    languages: {
      en: `${siteUrl}/en/blog/ai-contract-analysis`,
      fr: `${siteUrl}/fr/blog/ai-contract-analysis`,
      ar: `${siteUrl}/ar/blog/ai-contract-analysis`,
      "x-default": `${siteUrl}/blog/ai-contract-analysis`,
    },
  },

  openGraph: {
    title: "Analyse de contrats par IA : comment l’IA aide à examiner les documents juridiques | Runexa",

    description:
      "Découvrez comment l’analyse de contrats par IA aide à identifier les clauses risquées, résumer les obligations et soutenir les workflows d’examen juridique.",

    url: "https://runexa.ai/fr/blog/ai-contract-analysis",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa AI Contract Analysis",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "article",
  },

  twitter: {
    card: "summary_large_image",

    title: "Analyse de contrats par IA : comment l’IA aide à examiner les documents juridiques | Runexa",

    description:
      "Découvrez comment l’analyse de contrats par IA aide à identifier les clauses risquées, résumer les obligations et soutenir les workflows d’examen juridique.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function AIContractAnalysisPage() {
  return (
    <>
      <AIContractAnalysisArticle initialLocale="fr" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "Article",

            mainEntityOfPage: {
              "@type": "WebPage",
              "@id": "https://runexa.ai/fr/blog/ai-contract-analysis",
            },

            headline:
              "Analyse de contrats par IA : comment l’IA aide à examiner les documents juridiques",

            description:
              "Découvrez comment l’analyse de contrats par IA aide à identifier les clauses risquées, résumer les obligations et soutenir les workflows d’examen juridique.",

            datePublished: "2026-05-24",

            dateModified: "2026-05-24",

            inLanguage: "fr",

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
