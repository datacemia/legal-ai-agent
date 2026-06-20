import type { Metadata } from "next";
import StudyClient from "../../study/StudyClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Espace d’étude IA et assistant d’apprentissage | Runexa",

  description:
    "Générez des résumés IA, quiz, flashcards, explications audio, cartes mentales et plans d’étude personnalisés avec Runexa Study Agent.",

  keywords: [
    "assistant d'étude IA",
    "espace d'apprentissage IA",
    "flashcards IA",
    "quiz IA",
    "plan d'étude IA",
    "éducation par IA",
    "résumés par IA",
    "plateforme d'apprentissage IA",
    "Runexa Study AI",
    "apprentissage adaptatif par IA",

    "Runexa Study Agent",
    "apprentissage intelligent",
    "apprentissage personnalisé",
    "assistant pédagogique IA",
    "plateforme éducative intelligente",
    "amélioration des résultats scolaires",
    "gestion des études",
    "organisation des études",
    "plan d'apprentissage personnalisé",
    "résumé de cours par IA",
    "création de résumés de cours",
    "génération de questions d'examen",
    "quiz interactifs",
    "révision des cours",
    "flashcards intelligentes",
    "préparation aux examens",
    "assistant pour étudiants",
    "outil éducatif pour étudiants",
    "éducation numérique",
    "éducation assistée par IA",
    "e-learning",
    "auto-apprentissage",
    "études universitaires",
    "analyse de contenu éducatif",
    "transformation de documents en résumés",
    "génération de plans d'étude",
    "création de quiz de révision",
    "parcours d'apprentissage personnalisés",
    "intelligence artificielle pour l'éducation",
    "AI Education Platform",
    "Enterprise Learning AI",
  ],
  alternates: {
    canonical: "https://runexa.ai/fr/study",
    languages: {
      en: `${siteUrl}/en/study`,
      fr: `${siteUrl}/fr/study`,
      ar: `${siteUrl}/ar/study`,
      "x-default": `${siteUrl}/study`,
    },
  },

  openGraph: {
    title: "Runexa Study Agent",

    description:
      "Espace d’étude IA avec résumés, quiz, flashcards et apprentissage adaptatif.",

    url: "https://runexa.ai/fr/study",

    siteName: "Runexa Systems",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Study Agent",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Runexa Study Agent",

    description:
      "Résumés IA, quiz, flashcards, explications audio et workflows d’apprentissage adaptatif.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function StudyPage() {
  return (
    <>
      <StudyClient initialLocale="fr" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "SoftwareApplication",

            name: "Runexa Study Agent",

            applicationCategory: "EducationalApplication",

            operatingSystem: "Web",

            description:
              "Espace d’étude alimenté par l’IA avec résumés, quiz, flashcards, apprentissage visuel et plans d’étude adaptatifs.",

            url: "https://runexa.ai/fr/study",

            inLanguage: "fr",

            creator: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
            },

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: siteUrl,
            },

            knowsAbout: [
              "Assistant d’étude IA",
              "Espace d’apprentissage IA",
              "Flashcards IA",
              "Quiz IA",
              "Plans d’étude IA",
              "Apprentissage adaptatif IA",
            ],
          }),
        }}
      />
    </>
  );
}
