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
  ],

  alternates: {
    canonical: "https://runexa.ai/product-terms",
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
          }),
        }}
      />
    </>
  );
}
