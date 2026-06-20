import type { Metadata } from "next";
import StudyAIClient from "../../study-ai/StudyAIClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Assistant d’étude IA et espace d’apprentissage | Runexa",

  description:
    "Générez des résumés, quiz, flashcards, plans d’étude et workflows d’apprentissage structurés avec Runexa Study AI.",

  keywords: [
    "IA pour les études",
    "assistant d'étude IA",
    "flashcards IA",
    "quiz IA",
    "résumés par IA",
    "plans d'étude IA",
    "workflows d'apprentissage IA",
    "Runexa Study AI",

    "Runexa Study Agent",
    "apprentissage intelligent",
    "apprentissage assisté par IA",
    "apprentissage personnalisé",
    "apprentissage adaptatif",
    "assistant pédagogique IA",
    "plateforme éducative IA",
    "éducation intelligente",
    "éducation numérique",
    "e-learning",
    "amélioration des résultats scolaires",
    "gestion des études",
    "organisation des études",
    "création de résumés de cours",
    "résumé de leçons par IA",
    "génération de questions d'examen",
    "quiz interactifs",
    "quiz de révision",
    "flashcards intelligentes",
    "révision des cours",
    "préparation aux examens",
    "assistant pour étudiants",
    "outil éducatif pour étudiants",
    "études universitaires",
    "auto-apprentissage",
    "parcours d'apprentissage personnalisés",
    "génération de plans d'étude",
    "analyse de contenu éducatif",
    "transformation de documents en résumés",
    "plateforme d'apprentissage intelligente",
    "intelligence artificielle pour l'éducation",
    "AI Education",
    "AI Learning Platform",
    "Enterprise Learning AI",
  ],

  alternates: {
    canonical: "https://runexa.ai/fr/study-ai",
    languages: {
      en: `${siteUrl}/en/study-ai`,
      fr: `${siteUrl}/fr/study-ai`,
      ar: `${siteUrl}/ar/study-ai`,
      "x-default": `${siteUrl}/study-ai`,
    },
  },

  openGraph: {
    title: "Assistant d’étude IA et espace d’apprentissage | Runexa",

    description:
      "Générez des résumés, quiz, flashcards, plans d’étude et workflows d’apprentissage structurés avec Runexa Study AI.",

    url: "https://runexa.ai/fr/study-ai",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Study AI",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Assistant d’étude IA et espace d’apprentissage | Runexa",

    description:
      "Assistant d’étude IA pour générer des résumés, quiz, flashcards, plans d’étude et workflows d’apprentissage structurés.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function StudyAIPage() {
  return (
    <>
      <StudyAIClient initialLocale="fr" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify([
            {
              "@context": "https://schema.org",

              "@type": "SoftwareApplication",

              name: "Runexa Study AI",

              applicationCategory: "EducationalApplication",

              operatingSystem: "Web",

              url: "https://runexa.ai/fr/study-ai",

              inLanguage: "fr",

              description:
                "Assistant d’étude IA pour générer résumés, quiz, flashcards, plans d’étude et workflows d’apprentissage structurés.",

              publisher: {
                "@type": "Organization",
                name: "Runexa Systems LLC",
                url: siteUrl,
              },

              knowsAbout: [
                "IA étude",
                "Assistant d’étude IA",
                "Flashcards IA",
                "Quiz IA",
                "Résumés IA",
                "Plans d’étude IA",
                "Workflows d’apprentissage IA",
              ],
            },
          ]),
        }}
      />
    </>
  );
}
