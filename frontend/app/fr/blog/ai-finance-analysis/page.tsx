import type { Metadata } from "next";
import AIFinanceAnalysisArticle from "../../../blog/ai-finance-analysis/AIFinanceAnalysisArticle";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Analyse financière par IA : comprendre les dépenses, les abonnements et les économies | Runexa",

  description:
    "Découvrez comment l’analyse financière par IA aide à comprendre les habitudes de dépenses, les abonnements, les opportunités d’économies et les comportements financiers.",

  keywords: [
    "analyse financière IA",
    "finance personnelle IA",
    "analyse relevé bancaire",
    "détection abonnements IA",
    "analyse économies IA",
    "habitudes financières IA",
    "Runexa Finance Coach",
    "assistant budget IA",
  ],

  alternates: {
    canonical: "https://runexa.ai/fr/blog/ai-finance-analysis",
    languages: {
      en: `${siteUrl}/en/blog/ai-finance-analysis`,
      fr: `${siteUrl}/fr/blog/ai-finance-analysis`,
      ar: `${siteUrl}/ar/blog/ai-finance-analysis`,
      "x-default": `${siteUrl}/blog/ai-finance-analysis`,
    },
  },

  openGraph: {
    title: "Analyse financière par IA : comprendre les dépenses, les abonnements et les économies | Runexa",

    description:
      "Découvrez comment l’analyse financière par IA aide à comprendre les habitudes de dépenses, les abonnements, les opportunités d’économies et les comportements financiers.",

    url: "https://runexa.ai/fr/blog/ai-finance-analysis",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa AI Finance Analysis",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "article",
  },

  twitter: {
    card: "summary_large_image",

    title: "Analyse financière par IA : comprendre les dépenses, les abonnements et les économies | Runexa",

    description:
      "Découvrez comment l’analyse financière par IA aide à comprendre les habitudes de dépenses, les abonnements, les opportunités d’économies et les comportements financiers.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function AIFinanceAnalysisPage() {
  return (
    <>
      <AIFinanceAnalysisArticle initialLocale="fr" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "Article",

            mainEntityOfPage: {
              "@type": "WebPage",
              "@id": "https://runexa.ai/fr/blog/ai-finance-analysis",
            },

            headline:
              "Analyse financière par IA : comprendre les dépenses, les abonnements et les opportunités d’économies",

            description:
              "Découvrez comment l’analyse financière par IA aide à comprendre les habitudes de dépenses, les abonnements, les opportunités d’économies et les comportements financiers.",

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
