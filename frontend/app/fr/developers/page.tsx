import type { Metadata } from "next";
import DevelopersClient from "../../developers/DevelopersClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Développeurs et API IA | Runexa",

  description:
    "Créez des workflows alimentés par l’IA avec les API Runexa pour l’analyse juridique, l’intelligence financière, l’automatisation de l’apprentissage et l’aide à la décision business.",

  keywords: [
    "développeurs Runexa",
    "API d'intelligence artificielle",
    "API juridique IA",
    "API finance IA",
    "API étude intelligente",
    "API business intelligence",
    "API de workflow IA",
    "outils IA pour développeurs",
    "API IA pour entreprises",

    "Runexa API",
    "plateforme développeur Runexa",
    "intégration IA",
    "API pour entreprises",
    "services IA pour développeurs",
    "plateforme API IA",
    "API d'analyse de contrats",
    "API d'analyse juridique",
    "API d'analyse financière",
    "API d'analyse des dépenses",
    "API d'apprentissage intelligent",
    "API de génération de quiz",
    "API de résumés éducatifs",
    "API d'aide à la décision",
    "API d'analyse métier",
    "API KPI",
    "API business intelligence",
    "traitement de documents par IA",
    "automatisation des workflows",
    "agents IA",
    "API agents IA",
    "infrastructure IA",
    "traitement asynchrone IA",
    "intégration SaaS IA",
    "REST API IA",
    "plateforme pour développeurs",
    "solutions IA pour entreprises",
    "modèles IA spécialisés",
    "Runexa Developers",
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
