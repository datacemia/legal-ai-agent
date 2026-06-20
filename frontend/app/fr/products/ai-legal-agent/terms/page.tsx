import type { Metadata } from "next";
import ProductTermsClient from "../../../../products/ai-legal-agent/terms/ProductTermsClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Conditions produit IA | Runexa Systems LLC",

  description:
    "Conditions spécifiques, limites, avertissements, exigences de vérification humaine, notices de traitement des données et informations de responsabilité pour les agents IA Runexa.",

  keywords: [
    "conditions d’utilisation de l’IA",
    "clause de non-responsabilité IA",
    "clause de non-responsabilité juridique IA",
    "clause de non-responsabilité financière IA",
    "clause de non-responsabilité pour les études IA",
    "clause de non-responsabilité commerciale IA",
    "conditions Runexa",
    "limitation de responsabilité IA",
    "validation humaine de l’IA",
    "transparence de l’IA",
    "traitement des données IA",
    "conformité IA pour entreprises",

    "avertissement IA",
    "politique IA",
    "politique d’intelligence artificielle",
    "utilisation responsable de l’IA",
    "IA responsable",
    "gouvernance de l’IA",
    "gestion des risques IA",
    "supervision humaine",
    "contrôle humain des systèmes IA",
    "révision humaine des résultats IA",
    "vérification des résultats IA",
    "limites de l’intelligence artificielle",
    "risques liés à l’IA",
    "erreurs de l’intelligence artificielle",
    "précision de l’IA",
    "fiabilité de l’IA",
    "contenu généré par IA",
    "aide à la décision par IA",
    "analyse juridique non professionnelle",
    "informations financières non professionnelles",
    "contenu éducatif généré par IA",
    "décisions commerciales assistées par IA",
    "divulgation de l’utilisation de l’IA",
    "transparence algorithmique",
    "conformité réglementaire IA",
    "politiques IA pour entreprises",
    "Runexa AI Disclaimer",
    "Runexa AI Policy",
    "Responsible AI",
    "Enterprise AI Governance",
  ],

  alternates: {
    canonical: "https://runexa.ai/fr/products/ai-legal-agent/terms",
    languages: {
      en: `${siteUrl}/en/products/ai-legal-agent/terms`,
      fr: `${siteUrl}/fr/products/ai-legal-agent/terms`,
      ar: `${siteUrl}/ar/products/ai-legal-agent/terms`,
      "x-default": `${siteUrl}/products/ai-legal-agent/terms`,
    },
  },

  openGraph: {
    title: "Conditions produit IA | Runexa Systems LLC",

    description:
      "Conditions spécifiques, limites, avertissements, exigences de vérification humaine, notices de traitement des données et informations de responsabilité pour les agents IA Runexa.",

    url: "https://runexa.ai/fr/products/ai-legal-agent/terms",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa AI Product Terms",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Conditions produit IA | Runexa Systems LLC",

    description:
      "AI product limitations, human review requirements, data-processing notices, and operational terms for Runexa AI systems.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function ProductTermsPage() {
  return (
    <>
      <ProductTermsClient initialLocale="fr" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "Conditions produit IA Runexa",

            description:
              "Conditions produit, divulgations des limites IA, exigences de vérification humaine, notices de traitement des données, clarification de l’entraînement des modèles et absence de conseil professionnel pour les agents IA Runexa.",

            url: "https://runexa.ai/fr/products/ai-legal-agent/terms",

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
