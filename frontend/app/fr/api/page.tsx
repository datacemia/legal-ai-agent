import type { Metadata } from "next";
import ApiClient from "../../api/ApiClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "API IA et infrastructure d’agents | Runexa",

  description:
    "Intégrez les API IA Runexa pour l’analyse juridique, l’intelligence financière, l’automatisation de l’étude et les workflows d’aide à la décision business.",

  keywords: [
    "Runexa API",
    "API d'intelligence artificielle",
    "API juridique IA",
    "API finance IA",
    "API étude intelligente",
    "API intelligence d'affaires",
    "traitement IA asynchrone",
    "infrastructure IA",

    "API pour développeurs",
    "intégration IA",
    "plateforme API IA",
    "API Runexa",
    "API d'analyse de contrats",
    "API d'analyse juridique",
    "API de gestion financière",
    "API d'analyse des dépenses",
    "API d'apprentissage intelligent",
    "API de quiz éducatifs",
    "API d'aide à la décision",
    "API business intelligence",
    "traitement de documents par IA",
    "automatisation des workflows IA",
    "services IA pour entreprises",
    "API IA pour entreprises",
    "infrastructure d'intelligence artificielle",
    "intégration SaaS IA",
    "modèles IA spécialisés",
    "agents IA",
    "API agents IA",
    "Runexa Systems API",
    "plateforme développeur Runexa",
  ],

  alternates: {
    canonical: "https://runexa.ai/fr/api",
    languages: {
      en: `${siteUrl}/en/api`,
      fr: `${siteUrl}/fr/api`,
      ar: `${siteUrl}/ar/api`,
      "x-default": `${siteUrl}/api`,
    },
  },

  openGraph: {
    title: "API IA et infrastructure d’agents | Runexa",

    description:
      "Intégrez les API IA Runexa pour l’analyse juridique, l’intelligence financière, l’automatisation de l’étude et les workflows d’aide à la décision business.",

    url: "https://runexa.ai/fr/api",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa API Platform",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "API IA et infrastructure d’agents | Runexa",

    description:
      "API IA pour les workflows d’automatisation juridique, finance, étude et business.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function ApiPage() {
  return (
    <>
      <ApiClient initialLocale="fr" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "SoftwareApplication",

            name: "Runexa API Platform",

            applicationCategory: "DeveloperApplication",

            operatingSystem: "Web",

            description:
              "Plateforme API IA Runexa pour l’analyse juridique, l’intelligence financière, l’automatisation de l’étude, l’aide à la décision business, le traitement asynchrone et l’infrastructure d’agents.",

            url: "https://runexa.ai/fr/api",

            inLanguage: "fr",

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: siteUrl,
            },

            knowsAbout: [
              "API IA",
              "API IA juridique",
              "API IA finance",
              "API IA étude",
              "API IA business",
              "Traitement IA asynchrone",
              "Infrastructure IA",
            ],
          }),
        }}
      />
    </>
  );
}
