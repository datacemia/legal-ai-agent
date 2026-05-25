import type { Metadata } from "next";
import PricingClient from "./PricingClient";

export const metadata: Metadata = {
  title: "Runexa Pricing | AI Agents, Credits & API Plans",

  description:
    "Compare Runexa AI pricing plans including AI trials, global credits, Pro subscriptions, and enterprise API workflows.",

  keywords: [
    "AI pricing",
    "AI agents pricing",
    "legal AI pricing",
    "finance AI pricing",
    "AI API pricing",
    "enterprise AI pricing",
    "Runexa pricing",
  ],

  alternates: {
    canonical: "https://runexa.ai/pricing",
  },
};

export default function PricingPage() {
  return (
    <>
      <PricingClient />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            name: "Runexa",
            applicationCategory: "BusinessApplication",
            operatingSystem: "Web",
            description:
              "AI platform for legal analysis, finance intelligence, study workflows, and business decision support.",
            offers: [
              {
                "@type": "Offer",
                name: "Pro",
                price: "49",
                priceCurrency: "USD",
              },
            ],
          }),
        }}
      />
    </>
  );
}
