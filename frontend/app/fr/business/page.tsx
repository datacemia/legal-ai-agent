import type { Metadata } from "next";
import BusinessClient from "../../business/BusinessClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Intelligence décisionnelle d’entreprise | Runexa",

  description:
    "Analysez vos données business avec Runexa Business Agent. Obtenez KPIs, risques, opportunités, prévisions, graphiques et aide à la décision exécutive par IA.",

  keywords: [
    "IA business",
    "business intelligence IA",
    "analyse KPI IA",
    "intelligence décisionnelle business",
    "analyse business IA",
    "prévision business IA",
    "dashboard exécutif IA",
    "Runexa Business Agent",
  ],

  alternates: {
    canonical: "https://runexa.ai/fr/business",
    languages: {
      en: `${siteUrl}/en/business`,
      fr: `${siteUrl}/fr/business`,
      ar: `${siteUrl}/ar/business`,
      "x-default": `${siteUrl}/business`,
    },
  },

  openGraph: {
    title: "Intelligence décisionnelle d’entreprise | Runexa",

    description:
      "Importez vos données business et recevez une analyse exécutive IA avec KPIs, risques, opportunités, prévisions et décisions prioritaires.",

    url: "https://runexa.ai/fr/business",

    siteName: "Runexa Systems",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Business Agent",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Intelligence décisionnelle d’entreprise | Runexa",

    description:
      "Business intelligence IA pour KPIs, risques, opportunités, prévisions et décisions exécutives.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function BusinessPage() {
  return (
    <>
      <BusinessClient initialLocale="fr" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "SoftwareApplication",

            name: "Runexa Business Agent",

            applicationCategory: "BusinessApplication",

            operatingSystem: "Web",

            description:
              "Plateforme de business intelligence par IA pour l’analyse des KPIs, risques, opportunités, prévisions, graphiques et aide à la décision exécutive.",

            url: "https://runexa.ai/fr/business",

            inLanguage: "fr",

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems",
              url: siteUrl,
            },

            knowsAbout: [
              "IA business",
              "Business Intelligence IA",
              "Analyse KPI",
              "Prévision business IA",
              "Tableau de bord exécutif",
              "Aide à la décision",
            ],
          }),
        }}
      />
    </>
  );
}
