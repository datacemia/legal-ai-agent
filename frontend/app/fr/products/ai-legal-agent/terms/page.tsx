import type { Metadata } from "next";
import ProductTermsClient from "../../../../products/ai-legal-agent/terms/ProductTermsClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Conditions produit IA | Runexa Systems LLC",

  description:
    "Conditions spécifiques, limites, avertissements, exigences de vérification humaine, notices de traitement des données et informations de responsabilité pour les agents IA Runexa.",

  keywords: [
    "شروط استخدام الذكاء الاصطناعي",
    "إخلاء مسؤولية الذكاء الاصطناعي",
    "إخلاء المسؤولية القانونية للذكاء الاصطناعي",
    "إخلاء المسؤولية المالية للذكاء الاصطناعي",
    "إخلاء المسؤولية للدراسة باستخدام الذكاء الاصطناعي",
    "إخلاء المسؤولية التجارية للذكاء الاصطناعي",
    "شروط Runexa",
    "تحديد مسؤولية الذكاء الاصطناعي",
    "المراجعة البشرية لنتائج الذكاء الاصطناعي",
    "شفافية الذكاء الاصطناعي",
    "معالجة بيانات الذكاء الاصطناعي",
    "امتثال الذكاء الاصطناعي للمؤسسات",
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
