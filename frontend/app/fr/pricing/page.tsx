import type { Metadata } from "next";
import PricingClient from "../../pricing/PricingClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Tarifs Runexa | Agents IA, crédits et plans API",

  description:
    "Comparez les offres Runexa AI : essais IA, crédits globaux, abonnements Pro et workflows API entreprise.",

  keywords: [
    "tarifs IA",
    "prix agents IA",
    "tarif IA juridique",
    "tarif IA finance",
    "tarif API IA",
    "tarif IA entreprise",
    "tarifs Runexa",
    "crédits IA",
    "abonnements IA",
  ],

  alternates: {
    canonical: "https://runexa.ai/fr/pricing",
    languages: {
      en: `${siteUrl}/en/pricing`,
      fr: `${siteUrl}/fr/pricing`,
      ar: `${siteUrl}/ar/pricing`,
      "x-default": `${siteUrl}/pricing`,
    },
  },

  openGraph: {
    title: "Tarifs Runexa | Agents IA, crédits et plans API",

    description:
      "Comparez les offres Runexa AI : essais IA, crédits globaux, abonnements Pro et workflows API entreprise.",

    url: "https://runexa.ai/fr/pricing",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Pricing",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Tarifs Runexa | Agents IA, crédits et plans API",

    description:
      "Comparez les abonnements IA, crédits globaux, workflows API et offres entreprise de Runexa.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function PricingPage() {
  return (
    <>
      <PricingClient initialLanguage="fr" lockInitialLanguage />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "SoftwareApplication",

            name: "Runexa Pricing",

            applicationCategory: "BusinessApplication",

            operatingSystem: "Web",

            description:
              "Plateforme IA pour l’analyse juridique, l’intelligence financière, les workflows d’étude et l’aide à la décision business.",

            url: "https://runexa.ai/fr/pricing",

            inLanguage: "fr",

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: siteUrl,
            },

            offers: [
              {
                "@type": "Offer",

                name: "Pro",

                price: "49",

                priceCurrency: "USD",
              },
            ],

            knowsAbout: [
              "Tarifs IA",
              "Prix agents IA",
              "Crédits IA",
              "Plans API IA",
              "Tarifs IA entreprise",
              "Abonnements IA",
            ],
          }),
        }}
      />
    </>
  );
}
