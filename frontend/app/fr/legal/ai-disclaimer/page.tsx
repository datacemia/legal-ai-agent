import type { Metadata } from "next";
import AIDisclaimerClient from "../../../legal/ai-disclaimer/AIDisclaimerClient";

export const revalidate = 3600;

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Avertissement IA et transparence | Runexa",

  description:
    "Consultez l’avertissement et les informations de transparence IA de Runexa Systems concernant les résultats générés par l’IA, les limitations, les exigences de vérification humaine, l’absence de conseil professionnel et l’usage responsable de l’IA.",

 keywords: [
    "avertissement IA",
    "transparence de l’IA",
    "limites de l’IA",
    "conformité IA",
    "avertissement IA pour entreprises",
    "gouvernance de l’IA",
    "divulgation des risques liés à l’IA",
    "politique IA de Runexa",
    "utilisation responsable de l’IA",
    "conseils non professionnels",
    "validation humaine des résultats IA",
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
      "Consultez l’avertissement et les informations de transparence IA de Runexa Systems concernant les résultats générés par l’IA, les limitations, les exigences de vérification humaine, l’absence de conseil professionnel et l’usage responsable de l’IA.",

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
      "Consultez l’avertissement et les informations de transparence IA de Runexa Systems concernant les résultats générés par l’IA, les limitations, les exigences de vérification humaine, l’absence de conseil professionnel et l’usage responsable de l’IA.",

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

            name: "Runexa AI Disclaimer & Transparency",

            description:
              "Informations d’avertissement et de transparence IA couvrant les résultats générés par l’IA, les limitations, les exigences de vérification humaine, l’absence de conseil professionnel et l’usage responsable de l’IA.",

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
