import type { Metadata } from "next";
import DevelopersClient from "../../developers/DevelopersClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Développeurs et API IA | Runexa",

  description:
    "Créez des workflows alimentés par l’IA avec les API Runexa pour l’analyse juridique, l’intelligence financière, l’automatisation de l’apprentissage et l’aide à la décision business.",

  keywords: [
    "développeurs Runexa",
    "API IA",
    "API IA juridique",
    "API IA finance",
    "API IA étude",
    "API IA business",
    "API workflow IA",
    "outils IA développeurs",
    "API IA entreprise",
  ],

  alternates: {
    canonical: "https://runexa.ai/fr/developers",
    languages: {
      en: `${siteUrl}/en/developers`,
      fr: `${siteUrl}/fr/developers`,
      ar: `${siteUrl}/ar/developers`,
      "x-default": `${siteUrl}/developers`,
    },
  },

  openGraph: {
    title: "Développeurs et API IA | Runexa",

    description:
      "Créez des workflows alimentés par l’IA avec les API Runexa pour l’analyse juridique, l’intelligence financière, l’automatisation de l’apprentissage et l’aide à la décision business.",

    url: "https://runexa.ai/fr/developers",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Developers",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Développeurs et API IA | Runexa",

    description:
      "Créez des workflows alimentés par l’IA avec les API Runexa pour l’analyse juridique, l’intelligence financière, l’automatisation de l’apprentissage et l’aide à la décision business.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function DevelopersPage() {
  return (
    <>
      <DevelopersClient initialLocale="fr" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "TechArticle",

            headline: "Développeurs et API IA | Runexa",

            name: "Runexa Developers",

            description:
              "Plateforme développeur pour créer des workflows alimentés par l’IA avec les API Runexa pour l’analyse juridique, l’intelligence financière, l’automatisation de l’apprentissage et l’aide à la décision business.",

            url: "https://runexa.ai/fr/developers",

            inLanguage: "fr",

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: siteUrl,
            },

            about: [
              "API IA",
              "API développeurs",
              "API IA juridique",
              "API IA finance",
              "API IA étude",
              "API IA business",
              "Automatisation workflow IA",
            ],
          }),
        }}
      />
    </>
  );
}
