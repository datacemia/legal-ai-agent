import type { Metadata } from "next";
import UploadClient from "../../upload/UploadClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Analyse de contrats IA et documents juridiques | Runexa",

  description:
    "Analysez des contrats, détectez les clauses à risque, comprenez les obligations et recevez une intelligence juridique structurée avec Runexa AI Legal Agent.",

  keywords: [
    "analyse contrat IA",
    "IA juridique",
    "analyse de contrat IA",
    "analyse document juridique",
    "assistant juridique IA",
    "analyse risque contrat",
    "IA juridique entreprise",
    "Runexa legal agent",
    "intelligence contractuelle IA",
  ],

  alternates: {
    canonical: "https://runexa.ai/fr/upload",
    languages: {
      en: `${siteUrl}/en/upload`,
      fr: `${siteUrl}/fr/upload`,
      ar: `${siteUrl}/ar/upload`,
      "x-default": `${siteUrl}/upload`,
    },
  },

  openGraph: {
    title: "Runexa Legal AI",

    description:
      "Analyse de contrats par IA, détection des risques juridiques, extraction des obligations et intelligence juridique structurée.",

    url: "https://runexa.ai/fr/upload",

    siteName: "Runexa Systems",

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

    title: "Runexa Legal AI",

    description:
      "Analysez des contrats et documents juridiques avec une intelligence juridique alimentée par l’IA.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function UploadPage() {
  return (
    <>
      <UploadClient initialLocale="fr" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "SoftwareApplication",

            name: "Runexa Legal AI",

            applicationCategory: "BusinessApplication",

            operatingSystem: "Web",

            description:
              "Plateforme d’analyse de documents juridiques par IA pour les contrats, obligations, détection des risques et conseils de négociation.",

            url: "https://runexa.ai/fr/upload",

            inLanguage: "fr",

            provider: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: siteUrl,
            },

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: siteUrl,
            },

            offers: {
              "@type": "Offer",
              price: "1",
              priceCurrency: "USD",
            },

            knowsAbout: [
              "Analyse de contrat IA",
              "IA juridique",
              "Analyse de contrats",
              "Analyse de documents juridiques",
              "Risques contractuels",
              "Extraction des obligations",
            ],
          }),
        }}
      />
    </>
  );
}
