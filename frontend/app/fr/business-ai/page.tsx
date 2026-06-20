import type { Metadata } from "next";
import BusinessAIClient from "../../business-ai/BusinessAIClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Business Intelligence IA et aide à la décision | Runexa",

  description:
    "Analysez vos données d’entreprise, détectez les risques, découvrez les opportunités et améliorez vos décisions stratégiques avec Runexa Business AI.",

  keywords: [
    "IA pour les entreprises",
    "business intelligence IA",
    "aide à la décision",
    "analyse des KPI par IA",
    "analyse des risques commerciaux",
    "prévisions par IA",
    "Runexa business AI",
    "workflows métier IA",

    "Runexa Business Decision Agent",
    "agent IA pour les entreprises",
    "analyse des données commerciales",
    "analyse de la performance d'entreprise",
    "analyse stratégique par IA",
    "gestion de la performance",
    "indicateurs clés de performance",
    "tableaux de bord exécutifs",
    "rapports exécutifs intelligents",
    "analyse des tendances du marché",
    "analyse concurrentielle",
    "analyse des opportunités commerciales",
    "gestion des risques par IA",
    "planification stratégique",
    "prévision des revenus",
    "analyse de rentabilité",
    "optimisation des performances",
    "automatisation de l'analyse métier",
    "analyse d'entreprise par IA",
    "IA pour dirigeants",
    "business intelligence pour entreprises",
    "gestion intelligente des entreprises",
    "analyse de données d'entreprise",
    "insights business par IA",
    "transformation numérique",
    "plateforme de business intelligence",
    "assistant décisionnel IA",
    "aide à la direction d'entreprise",
    "IA d'entreprise",
    "Business Intelligence AI",
  ],
  alternates: {
    canonical: "https://runexa.ai/fr/business-ai",
    languages: {
      en: `${siteUrl}/en/business-ai`,
      fr: `${siteUrl}/fr/business-ai`,
      ar: `${siteUrl}/ar/business-ai`,
      "x-default": `${siteUrl}/business-ai`,
    },
  },

  openGraph: {
    title: "Business Intelligence IA et aide à la décision | Runexa",

    description:
      "Analysez vos données d’entreprise, détectez les risques, découvrez les opportunités et améliorez vos décisions stratégiques avec Runexa Business AI.",

    url: "https://runexa.ai/fr/business-ai",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Business AI",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Business Intelligence IA et aide à la décision | Runexa",

    description:
      "Business intelligence par IA pour l’analyse des KPI, les insights stratégiques, les prévisions et l’aide à la décision opérationnelle.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function BusinessAIPage() {
  return (
    <>
      <BusinessAIClient initialLocale="fr" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify([
            {
              "@context": "https://schema.org",

              "@type": "SoftwareApplication",

              name: "Runexa Business AI",

              applicationCategory: "BusinessApplication",

              operatingSystem: "Web",

              url: "https://runexa.ai/fr/business-ai",

              inLanguage: "fr",

              description:
                "Logiciel de Business Intelligence IA et d’aide à la décision pour l’analyse des KPI, la détection des risques, les opportunités, les prévisions et les insights opérationnels.",

              publisher: {
                "@type": "Organization",
                name: "Runexa Systems LLC",
                url: siteUrl,
              },

              knowsAbout: [
                "Business Intelligence IA",
                "IA business",
                "Aide à la décision",
                "Analyse KPI",
                "Analyse des risques business",
                "Prévision IA",
              ],
            },
          ]),
        }}
      />
    </>
  );
}
