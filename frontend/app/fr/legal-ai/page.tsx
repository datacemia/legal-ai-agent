import type { Metadata } from "next";
import LegalAIClient from "../../legal-ai/LegalAIClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Analyse de contrats IA et documents juridiques | Runexa",

  description:
    "Analysez des contrats, détectez les clauses à risque, extrayez les obligations et générez des résumés juridiques avec Runexa Legal AI.",

  keywords: [
    "IA juridique",
    "analyse de contrat IA",
    "analyse document juridique",
    "analyse risque contrat",
    "assistant juridique IA",
    "résumés de contrats",
    "Runexa legal AI",
    "workflow juridique IA",
  ],

  alternates: {
    canonical: "https://runexa.ai/fr/legal-ai",
    languages: {
      en: `${siteUrl}/en/legal-ai`,
      fr: `${siteUrl}/fr/legal-ai`,
      ar: `${siteUrl}/ar/legal-ai`,
      "x-default": `${siteUrl}/legal-ai`,
    },
  },

  openGraph: {
    title: "Analyse de contrats IA et documents juridiques | Runexa",

    description:
      "Analysez des contrats, détectez les clauses à risque, extrayez les obligations et générez des résumés juridiques avec Runexa Legal AI.",

    url: "https://runexa.ai/fr/legal-ai",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Legal AI",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Analyse de contrats IA et documents juridiques | Runexa",

    description:
      "Analyse de contrats par IA, détection des risques juridiques, extraction des obligations et analyse des workflows juridiques.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function LegalAIPage() {
  return (
    <>
      <LegalAIClient initialLocale="fr" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify([
            {
              "@context": "https://schema.org",

              "@type": "SoftwareApplication",

              name: "Runexa Legal AI",

              applicationCategory: "BusinessApplication",

              operatingSystem: "Web",

              url: "https://runexa.ai/fr/legal-ai",

              inLanguage: "fr",

              description:
                "Logiciel d’analyse de contrats IA et de documents juridiques pour détecter les clauses à risque, extraire les obligations, générer des résumés et recommandations.",

              publisher: {
                "@type": "Organization",
                name: "Runexa Systems LLC",
                url: siteUrl,
              },

              knowsAbout: [
                "IA juridique",
                "Analyse de contrats",
                "Analyse de documents juridiques",
                "Détection des risques contractuels",
                "Extraction des obligations",
                "Workflows juridiques IA",
              ],
            },
          ]),
        }}
      />
    </>
  );
}
