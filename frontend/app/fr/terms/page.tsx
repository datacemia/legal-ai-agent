import type { Metadata } from "next";
import TermsClient from "../../terms/TermsClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Conditions d’utilisation | Runexa",

  description:
    "Conditions d’utilisation régissant les agents IA Runexa, les API, les workflows entreprise, les crédits, les abonnements et les services alimentés par l’IA.",

  keywords: [
    "conditions d’utilisation",
    "conditions plateforme IA",
    "conditions Runexa",
    "conditions SaaS IA",
    "conditions API IA",
    "conditions IA entreprise",
    "abonnements IA",
    "crédits IA",
  ],

  alternates: {
    canonical: "https://runexa.ai/fr/terms",
    languages: {
      en: `${siteUrl}/en/terms`,
      fr: `${siteUrl}/fr/terms`,
      ar: `${siteUrl}/ar/terms`,
      "x-default": `${siteUrl}/terms`,
    },
  },

  openGraph: {
    title: "Conditions d’utilisation | Runexa",

    description:
      "Conditions régissant l’utilisation des systèmes IA Runexa, des API et des workflows IA entreprise.",

    url: "https://runexa.ai/fr/terms",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Terms of Service",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Conditions d’utilisation Runexa",

    description:
      "Conditions régissant l’utilisation des systèmes IA Runexa, des API et des workflows entreprise.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function TermsPage() {
  return (
    <>
      <TermsClient initialLocale="fr" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "Conditions d’utilisation Runexa",

            description:
              "Conditions régissant les agents IA Runexa, les API, les workflows entreprise et les services alimentés par l’IA.",

            url: "https://runexa.ai/fr/terms",

            inLanguage: "fr",

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: siteUrl,
            },
          }),
        }}
      />
    </>
  );
}
