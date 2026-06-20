import type { Metadata } from "next";
import ProductTermsClient from "../../../../products/ai-legal-agent/terms/ProductTermsClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "AI Product Terms | Runexa Systems LLC",

  description:
    "Product-specific terms, limitations, disclaimers, human review requirements, data-processing notices, and liability information for Runexa AI agents including legal, finance, study, and business AI systems.",

 keywords: [
  "AI product terms",
  "AI legal disclaimer",
  "AI finance disclaimer",
  "AI study disclaimer",
  "AI business disclaimer",
  "Runexa terms",
  "AI liability limitation",
  "AI human review",
  "AI transparency",
  "AI data processing",
  "enterprise AI compliance",

  "Runexa Product Terms",
  "AI terms and conditions",
  "AI service terms",
  "AI platform terms",
  "AI usage terms",
  "enterprise AI terms",
  "AI governance",
  "responsible AI",
  "AI safety",
  "AI risk disclosure",
  "AI limitations",
  "limitations of artificial intelligence",
  "AI output verification",
  "human review of AI outputs",
  "human oversight",
  "human-in-the-loop AI",
  "AI accuracy limitations",
  "AI reliability",
  "AI-generated content",
  "AI-assisted decision making",
  "AI compliance policy",
  "enterprise AI governance",
  "AI risk management",
  "AI transparency policy",
  "AI operational guidelines",
  "AI usage guidelines",
  "legal AI disclaimer",
  "financial AI disclaimer",
  "educational AI disclaimer",
  "business AI disclaimer",
  "professional judgment",
  "independent verification",
  "AI legal limitations",
  "AI financial limitations",
  "AI educational limitations",
  "AI decision support",
  "enterprise compliance",
  "Runexa Legal Agent Terms",
  "Runexa Finance Coach Terms",
  "Runexa Study Agent Terms",
  "Runexa Business Decision Agent Terms",
],

  alternates: {
    canonical: "https://runexa.ai/en/products/ai-legal-agent/terms",
    languages: {
      en: `${siteUrl}/en/products/ai-legal-agent/terms`,
      fr: `${siteUrl}/fr/products/ai-legal-agent/terms`,
      ar: `${siteUrl}/ar/products/ai-legal-agent/terms`,
      "x-default": `${siteUrl}/products/ai-legal-agent/terms`,
    },
  },

  openGraph: {
    title: "AI Product Terms | Runexa Systems LLC",

    description:
      "Product-specific terms, limitations, disclaimers, human review requirements, data-processing notices, and liability information for Runexa AI agents including legal, finance, study, and business AI systems.",

    url: "https://runexa.ai/en/products/ai-legal-agent/terms",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa AI Product Terms",
      },
    ],

    locale: "en_US",

    alternateLocale: ["fr_FR", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "AI Product Terms | Runexa Systems LLC",

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
      <ProductTermsClient initialLocale="en" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "Runexa AI Product Terms",

            description:
              "Product terms, AI limitation disclosures, human review requirements, data-processing notices, model-training clarification, and non-professional-advice notices for Runexa AI agents and enterprise AI services.",

            url: "https://runexa.ai/en/products/ai-legal-agent/terms",

            inLanguage: "en",

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
