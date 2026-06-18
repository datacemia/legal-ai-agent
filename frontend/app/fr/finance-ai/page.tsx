import type { Metadata } from "next";
import FinanceAIClient from "../../finance-ai/FinanceAIClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Analyse financière IA et coach de finances personnelles | Runexa",

  description:
    "Analysez des relevés bancaires, détectez les abonnements, identifiez des opportunités d’économies et améliorez vos habitudes financières avec Runexa Finance AI.",

  keywords: [
    "IA finance",
    "analyse financière IA",
    "analyse relevé bancaire",
    "détection abonnements IA",
    "finance personnelle IA",
    "analyse économies IA",
    "Runexa finance AI",
    "coach financier IA",
  ],

  alternates: {
    canonical: "https://runexa.ai/fr/finance-ai",
    languages: {
      en: `${siteUrl}/en/finance-ai`,
      fr: `${siteUrl}/fr/finance-ai`,
      ar: `${siteUrl}/ar/finance-ai`,
      "x-default": `${siteUrl}/finance-ai`,
    },
  },

  openGraph: {
    title: "Analyse financière IA et coach de finances personnelles | Runexa",

    description:
      "Analysez des relevés bancaires, détectez les abonnements, identifiez des opportunités d’économies et améliorez vos habitudes financières avec Runexa Finance AI.",

    url: "https://runexa.ai/fr/finance-ai",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Finance AI",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Analyse financière IA et coach de finances personnelles | Runexa",

    description:
      "Analyse financière par IA pour les relevés bancaires, les abonnements, les économies et le coaching financier personnel.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function FinanceAIPage() {
  return (
    <>
      <FinanceAIClient initialLocale="fr" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify([
            {
              "@context": "https://schema.org",

              "@type": "SoftwareApplication",

              name: "Runexa Finance AI",

              applicationCategory: "FinanceApplication",

              operatingSystem: "Web",

              url: "https://runexa.ai/fr/finance-ai",

              inLanguage: "fr",

              description:
                "Coach financier IA pour l’analyse des relevés bancaires, la détection des abonnements, les opportunités d’économies et les habitudes financières.",

              publisher: {
                "@type": "Organization",
                name: "Runexa Systems LLC",
                url: siteUrl,
              },

              knowsAbout: [
                "IA finance",
                "Analyse financière IA",
                "Analyse de relevés bancaires",
                "Détection des abonnements",
                "Finance personnelle IA",
                "Coach financier IA",
              ],
            },
          ]),
        }}
      />
    </>
  );
}
