import type { Metadata } from "next";
import AIStudyAssistantArticle from "../../../blog/ai-study-assistant/AIStudyAssistantArticle";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Assistant d’étude par IA : construire des workflows d’apprentissage plus efficaces | Runexa",

  description:
    "Découvrez comment les assistants d’étude par IA aident à générer des résumés, quiz, flashcards et workflows d’apprentissage structurés.",

  keywords: [
    "assistant d'étude IA",
    "parcours d'apprentissage IA",
    "résumés par IA",
    "cartes mémoire IA",
    "quiz IA",
    "planification d'étude IA",
    "Runexa Study Agent",
    "IA dans l'éducation",

    "apprentissage intelligent",
    "apprentissage personnalisé",
    "assistant pédagogique IA",
    "plateforme éducative IA",
    "amélioration des résultats scolaires",
    "organisation des études",
    "gestion des études",
    "plan d'étude intelligent",
    "création de résumés de cours",
    "résumé de leçons par IA",
    "génération de questions d'examen",
    "quiz interactifs",
    "révision des cours",
    "apprendre plus rapidement",
    "apprentissage efficace",
    "analyse de contenu éducatif",
    "transformation de documents en résumés",
    "assistant pour étudiants",
    "outil éducatif pour étudiants",
    "éducation numérique",
    "éducation assistée par IA",
    "e-learning",
    "études universitaires",
    "auto-apprentissage",
    "préparation aux examens",
    "flashcards intelligentes",
    "quiz de révision",
    "parcours d'apprentissage personnalisés",
    "agent d'étude intelligent",
    "Runexa Study AI",
    "intelligence artificielle pour l'éducation",
  ],
  alternates: {
    canonical: "https://runexa.ai/fr/blog/ai-study-assistant",
    languages: {
      en: `${siteUrl}/en/blog/ai-study-assistant`,
      fr: `${siteUrl}/fr/blog/ai-study-assistant`,
      ar: `${siteUrl}/ar/blog/ai-study-assistant`,
      "x-default": `${siteUrl}/blog/ai-study-assistant`,
    },
  },

  openGraph: {
    title: "Assistant d’étude par IA : construire des workflows d’apprentissage plus efficaces | Runexa",

    description:
      "Découvrez comment les assistants d’étude par IA aident à générer des résumés, quiz, flashcards et workflows d’apprentissage structurés.",

    url: "https://runexa.ai/fr/blog/ai-study-assistant",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa AI Study Assistant",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "article",
  },

  twitter: {
    card: "summary_large_image",

    title: "Assistant d’étude par IA : construire des workflows d’apprentissage plus efficaces | Runexa",

    description:
      "Découvrez comment les assistants d’étude par IA aident à générer des résumés, quiz, flashcards et workflows d’apprentissage structurés.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function AIStudyAssistantPage() {
  return (
    <>
      <AIStudyAssistantArticle initialLocale="fr" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "Article",

            mainEntityOfPage: {
              "@type": "WebPage",
              "@id": "https://runexa.ai/fr/blog/ai-study-assistant",
            },

            headline:
              "Assistant d’étude par IA : construire des workflows d’apprentissage plus efficaces",

            description:
              "Découvrez comment les assistants d’étude par IA aident à générer des résumés, quiz, flashcards et workflows d’apprentissage structurés.",

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
