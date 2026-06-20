import type { Metadata } from "next";
import DocsClient from "../../docs/DocsClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Documentation API IA | Runexa",

  description:
    "Documentation technique des API IA Runexa pour l’analyse juridique, l’intelligence financière, les workflows business, les jobs asynchrones, l’authentification et les intégrations entreprise.",

  keywords: [
    "documentation Runexa",
    "documentation API IA",
    "documentation API juridique IA",
    "documentation API finance IA",
    "documentation API business intelligence",
    "documentation développeurs",
    "API IA asynchrones",
    "intégration IA pour entreprises",

    "documentation développeur",
    "référence API",
    "guide API",
    "API d'intelligence artificielle",
    "Runexa API Documentation",
    "plateforme développeur Runexa",
    "documentation REST API",
    "documentation Webhook",
    "documentation SDK",
    "exemples API",
    "clés API",
    "authentification API",
    "intégration REST API",
    "intégration SaaS",
    "API d'analyse de contrats",
    "API d'analyse juridique",
    "API financière",
    "API d'analyse des dépenses",
    "API d'apprentissage intelligent",
    "API de génération de résumés",
    "API de génération de quiz",
    "API d'aide à la décision",
    "API d'analyse métier",
    "API KPI",
    "agents IA",
    "API agents IA",
    "automatisation des workflows",
    "traitement documentaire par IA",
    "infrastructure IA",
    "solutions IA pour entreprises",
    "services IA pour développeurs",
    "plateforme API pour entreprises",
    "Runexa Developers",
  ],
  alternates: {
    canonical: "https://runexa.ai/fr/docs",
    languages: {
      en: `${siteUrl}/en/docs`,
      fr: `${siteUrl}/fr/docs`,
      ar: `${siteUrl}/ar/docs`,
      "x-default": `${siteUrl}/docs`,
    },
  },

  openGraph: {
    title: "Documentation API IA | Runexa",

    description:
      "Documentation technique des API IA Runexa pour l’analyse juridique, l’intelligence financière, les workflows business, les jobs asynchrones, l’authentification et les intégrations entreprise.",

    url: "https://runexa.ai/fr/docs",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa API Documentation",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Documentation API IA | Runexa",

    description:
      "Documentation technique développeur pour les API IA asynchrones de Runexa.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function DocsPage() {
  return (
    <>
      <DocsClient initialLocale="fr" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "TechArticle",

            headline: "Documentation API IA | Runexa",

            name: "Runexa API Documentation",

            description:
              "Documentation technique des API IA asynchrones Runexa, authentification, jobs, analyse juridique, intelligence financière, automatisation de l’étude, workflows business et intégrations entreprise.",

            url: "https://runexa.ai/fr/docs",

            inLanguage: "fr",

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: siteUrl,
            },

            about: [
              "Documentation API IA",
              "API IA asynchrones",
              "Documentation API IA juridique",
              "Documentation API IA finance",
              "Documentation API IA business",
              "Intégration IA entreprise",
            ],
          }),
        }}
      />
    </>
  );
}
