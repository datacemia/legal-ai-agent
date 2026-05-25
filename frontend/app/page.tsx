import type { Metadata } from "next";
import HomeClient from "./HomeClient";

export const metadata: Metadata = {
  title: "Runexa | Enterprise AI Workspace & Specialized AI Agents",

  description:
    "Runexa is an AI workspace platform with specialized AI agents for legal analysis, finance intelligence, study workflows, and business decision support.",

  keywords: [
    "AI workspace",
    "AI agents",
    "legal AI",
    "finance AI",
    "study AI",
    "business AI",
    "enterprise AI",
    "AI workflow automation",
    "AI business intelligence",
    "Runexa",
  ],

  alternates: {
    canonical: "https://runexa.ai",
  },

  openGraph: {
    title: "Runexa AI Workspace",
    description:
      "Specialized AI agents for legal, finance, study, and business workflows.",
    url: "https://runexa.ai",
    siteName: "Runexa",
    type: "website",
  },

  twitter: {
    card: "summary_large_image",
    title: "Runexa AI Workspace",
    description:
      "AI workspace platform for legal analysis, finance intelligence, study assistance, and business workflows.",
  },
};

export default function Page() {
  return (
    <>
      <HomeClient />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "Organization",

            name: "Runexa Systems LLC",

            url: "https://runexa.ai",

            logo: "https://runexa.ai/logo.png",

            sameAs: [],

            description:
              "AI workspace platform with specialized AI agents for legal analysis, finance intelligence, study assistance, and business workflows.",

            knowsAbout: [
              "Artificial Intelligence",
              "Legal AI",
              "Finance AI",
              "Business Intelligence",
              "Study AI",
              "Enterprise AI Workflows",
            ],
          }),
        }}
      />
    </>
  );
}
