import type { Metadata } from "next";
import ProductTermsClient from "../../../../products/ai-legal-agent/terms/ProductTermsClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Conditions produit IA | Runexa Systems LLC",

  description:
    "Conditions spécifiques, limites, avertissements et informations de responsabilité pour les agents IA Runexa, notamment les systèmes juridique, finance, étude et business.",

  keywords: [
    "conditions produit IA",
    "avertissement IA juridique",
    "avertissement IA finance",
    "avertissement IA étude",
    "avertissement IA business",
    "conditions Runexa",
    "limitation responsabilité IA",
    "conformité IA entreprise",
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
      "Conditions spécifiques, limites, avertissements et informations de responsabilité pour les agents IA Runexa, notamment juridique, finance, étude et business.",

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
      "Limites produit IA, divulgations de responsabilité et conditions opérationnelles pour les systèmes IA Runexa.",

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
              "Conditions produit et divulgations des limites IA pour les agents IA Runexa et services IA entreprise.",

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
