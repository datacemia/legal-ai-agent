import type { Metadata } from "next";
import FinanceAIClient from "../../finance-ai/FinanceAIClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Analyse financière IA et coach de finances personnelles | Runexa",

  description:
    "Analysez des relevés bancaires, détectez les abonnements, identifiez des opportunités d’économies et améliorez vos habitudes financières avec Runexa Finance AI.",

  keywords: [
    "IA financière",
    "analyse financière par IA",
    "analyse de relevé bancaire",
    "détection d'abonnements par IA",
    "IA pour la finance personnelle",
    "analyse de l'épargne par IA",
    "Runexa Finance AI",
    "coach financier IA",

    "Runexa Finance Coach",
    "intelligence artificielle financière",
    "gestion du budget personnel",
    "assistant financier intelligent",
    "conseiller financier IA",
    "analyse des dépenses",
    "analyse des dépenses mensuelles",
    "analyse des revenus et dépenses",
    "gestion des finances personnelles",
    "planification financière intelligente",
    "amélioration des habitudes financières",
    "analyse des habitudes financières",
    "gestion des abonnements",
    "détection des dépenses récurrentes",
    "identification des opportunités d'épargne",
    "gestion des dépenses personnelles",
    "surveillance des dépenses",
    "analyse des comptes bancaires",
    "analyse des données financières",
    "analyse des flux de trésorerie",
    "tableau de bord financier intelligent",
    "éducation financière",
    "planification budgétaire",
    "optimisation des décisions financières",
    "gestion de patrimoine personnel",
    "finance intelligente",
    "analyse financière personnelle",
    "gestion financière intelligente",
    "assistant d'épargne intelligent",
    "automatisation financière",
    "plateforme financière IA",
    "outil d'analyse financière",
    "Finance AI",
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
