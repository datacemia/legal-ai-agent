import type { Metadata } from "next";
import AIDisclaimerClient from "../../../legal/ai-disclaimer/AIDisclaimerClient";

export const revalidate = 3600;

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Avertissement IA et transparence | Runexa",

  description:
    "Consultez l’avertissement IA et les informations de transparence de Runexa Systems concernant les résultats générés par IA, les limites, la revue humaine et l’usage IA en entreprise.",

  keywords: [
    "avertissement IA",
    "transparence IA",
    "limites IA",
    "conformité IA",
    "avertissement IA entreprise",
    "gouvernance IA",
    "divulgation risques IA",
    "politique IA Runexa",
  ],

  alternates: {
    canonical: "https://runexa.ai/fr/legal/ai-disclaimer",
    languages: {
      en: `${siteUrl}/en/legal/ai-disclaimer`,
      fr: `${siteUrl}/fr/legal/ai-disclaimer`,
      ar: `${siteUrl}/ar/legal/ai-disclaimer`,
      "x-default": `${siteUrl}/legal/ai-disclaimer`,
    },
  },

  openGraph: {
    title: "Avertissement IA et transparence | Runexa",

    description:
      "Consultez la transparence IA, les limites et les exigences de revue humaine pour les services IA et plateformes entreprise Runexa Systems.",

    url: "https://runexa.ai/fr/legal/ai-disclaimer",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa AI Disclaimer",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Avertissement IA et transparence | Runexa",

    description:
      "Consultez les limites IA, notices de transparence et exigences de revue humaine pour les systèmes IA Runexa.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function AIDisclaimerPage() {
  return (
    <>
      <AIDisclaimerClient initialLocale="fr" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "Avertissement IA et transparence Runexa",

            description:
              "Avertissement IA et informations de transparence régissant l’usage des systèmes IA Runexa, plateformes entreprise, API et services intelligents.",

            url: "https://runexa.ai/fr/legal/ai-disclaimer",

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
