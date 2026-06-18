import type { Metadata } from "next";
import AcceptableUseClient from "../../../legal/acceptable-use/AcceptableUseClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Politique d’utilisation acceptable | Runexa",

  description:
    "Politique d’utilisation acceptable Runexa encadrant l’usage légal et responsable des systèmes IA, API, workflows et services entreprise.",

  keywords: [
    "politique d’utilisation acceptable",
    "politique IA",
    "conformité IA",
    "politique IA entreprise",
    "règles usage IA",
    "politique Runexa",
  ],

  alternates: {
    canonical: "https://runexa.ai/fr/legal/acceptable-use",
    languages: {
      en: `${siteUrl}/en/legal/acceptable-use`,
      fr: `${siteUrl}/fr/legal/acceptable-use`,
      ar: `${siteUrl}/ar/legal/acceptable-use`,
      "x-default": `${siteUrl}/legal/acceptable-use`,
    },
  },

  openGraph: {
    title: "Politique d’utilisation acceptable | Runexa",

    description:
      "Politique d’utilisation acceptable Runexa pour les systèmes IA, API, workflows entreprise et services intelligents.",

    url: "https://runexa.ai/fr/legal/acceptable-use",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Acceptable Use Policy",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Politique d’utilisation acceptable | Runexa",

    description:
      "Consultez les exigences d’utilisation acceptable des services IA et systèmes entreprise Runexa.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function AcceptableUsePage() {
  return (
    <>
      <AcceptableUseClient initialLocale="fr" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "Politique d’utilisation acceptable Runexa",

            description:
              "Politique d’utilisation acceptable pour les services IA Runexa, API, workflows entreprise et systèmes intelligents.",

            url: "https://runexa.ai/fr/legal/acceptable-use",

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
