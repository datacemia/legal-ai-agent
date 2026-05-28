import type { Metadata } from "next";
import ProductTermsClient from "./ProductTermsClient";

export const metadata: Metadata = {
  title: "AI Product Terms | Runexa Systems LLC",

  description:
    "Product-specific terms, limitations, disclaimers, and liability information for Runexa AI agents including legal, finance, study, and business AI systems.",

  keywords: [
    "AI product terms",
    "AI legal disclaimer",
    "AI finance disclaimer",
    "AI study disclaimer",
    "AI business disclaimer",
    "Runexa terms",
    "AI liability limitation",
    "enterprise AI compliance",
  ],

  alternates: {
    canonical: "https://runexa.ai/products/ai-legal-agent/terms",
  },

  openGraph: {
    title: "AI Product Terms | Runexa Systems LLC",

    description:
      "Product-specific terms, limitations, disclaimers, and liability information for Runexa AI agents including legal, finance, study, and business AI systems.",

    url: "https://runexa.ai/products/ai-legal-agent/terms",

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

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "AI Product Terms | Runexa Systems LLC",

    description:
      "AI product limitations, liability disclosures, and operational terms for Runexa AI systems.",

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
      <ProductTermsClient />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "Runexa AI Product Terms",

            description:
              "Product terms and AI limitation disclosures for Runexa AI agents and enterprise AI services.",

            url: "https://runexa.ai/products/ai-legal-agent/terms",

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: "https://runexa.ai",
            },
          }),
        }}
      />
    </>
  );
}
