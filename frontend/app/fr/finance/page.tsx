import type { Metadata } from "next";
import FinanceClient from "../../finance/FinanceClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Coach financier IA et intelligence financière | Runexa",

  description:
    "Analysez vos relevés bancaires, détectez les abonnements, surveillez les dépenses, découvrez des opportunités d’économies et recevez un coaching financier IA avec Runexa Finance AI.",

  keywords: [
    "coach financier IA",
    "analyse financière IA",
    "analyse relevé bancaire",
    "finance personnelle IA",
    "assistant budget IA",
    "détection abonnements IA",
    "intelligence financière",
    "analyse économies IA",
  ],

  alternates: {
    canonical: "https://runexa.ai/fr/finance",
    languages: {
      en: `${siteUrl}/en/finance`,
      fr: `${siteUrl}/fr/finance`,
      ar: `${siteUrl}/ar/finance`,
      "x-default": `${siteUrl}/finance`,
    },
  },

  openGraph: {
    title: "Coach financier IA et intelligence financière | Runexa",

    description:
      "Analysez vos relevés bancaires, détectez les abonnements, surveillez les dépenses, découvrez des opportunités d’économies et recevez un coaching financier IA avec Runexa Finance AI.",

    url: "https://runexa.ai/fr/finance",

    siteName: "Runexa Systems",

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

    title: "Coach financier IA et intelligence financière | Runexa",

    description:
      "Intelligence financière IA pour l’analyse de relevés bancaires, le budget, la détection d’abonnements et l’optimisation des économies.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function FinancePage() {
  return (
    <>
      <FinanceClient initialLocale="fr" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "SoftwareApplication",

            name: "Runexa Finance AI",

            applicationCategory: "FinanceApplication",

            operatingSystem: "Web",

            description:
              "Plateforme d’intelligence financière IA pour l’analyse des relevés bancaires, la détection des abonnements, le budget et l’optimisation des économies.",

            url: "https://runexa.ai/fr/finance",

            inLanguage: "fr",

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems",
              url: siteUrl,
            },

            knowsAbout: [
              "Coach financier IA",
              "Analyse financière",
              "Analyse de relevés bancaires",
              "Finance personnelle IA",
              "Budget IA",
              "Optimisation des économies",
            ],
          }),
        }}
      />
    </>
  );
}
