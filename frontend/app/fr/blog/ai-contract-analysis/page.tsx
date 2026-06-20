import type { Metadata } from "next";
import AIContractAnalysisArticle from "../../../blog/ai-contract-analysis/AIContractAnalysisArticle";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Analyse de contrats par IA : comment l’IA aide à examiner les documents juridiques | Runexa",

  description:
    "Découvrez comment l’analyse de contrats par IA aide à identifier les clauses risquées, résumer les obligations et soutenir les workflows d’examen juridique.",

  keywords: [
    "analyse de contrats par IA",
    "révision de contrats par IA",
    "analyse de documents juridiques",
    "intelligence artificielle juridique",
    "détection des risques contractuels",
    "assistant juridique IA",
    "résumés de contrats",
    "Runexa Legal Agent",

    "analyse des clauses contractuelles",
    "détection des clauses à risque",
    "évaluation des risques juridiques",
    "revue de documents juridiques",
    "analyse d'accords juridiques",
    "vérification de contrats",
    "lecture intelligente de contrats",
    "analyse des conditions contractuelles",
    "résumé de documents juridiques",
    "gestion des contrats",
    "conformité contractuelle",
    "analyse des obligations juridiques",
    "analyse des responsabilités contractuelles",
    "analyse des risques commerciaux",
    "contrôle de contrats",
    "aide à la décision juridique",
    "automatisation juridique",
    "workflow juridique IA",
    "LegalTech",
    "IA pour juristes",
    "outil d'analyse juridique",
    "analyse documentaire IA",
    "revue de contrats commerciaux",
    "compréhension des contrats juridiques",
    "Runexa Legal AI",
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
