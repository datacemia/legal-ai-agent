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
    "documentation API IA juridique",
    "documentation API IA finance",
    "documentation API IA business",
    "documentation développeur",
    "API IA asynchrones",
    "intégration IA entreprise",
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
