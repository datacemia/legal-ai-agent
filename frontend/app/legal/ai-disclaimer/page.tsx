import type { Metadata } from "next";
import AIDisclaimerClient from "./AIDisclaimerClient";

export const metadata: Metadata = {
  title: "AI Disclaimer & Transparency | Runexa",

  description:
    "Transparency and AI limitation disclosures for Runexa AI systems, APIs, workflows, and intelligent agents.",

  keywords: [
    "AI disclaimer",
    "AI transparency",
    "AI limitations",
    "AI policy",
    "AI compliance",
    "enterprise AI disclaimer",
  ],

  alternates: {
    canonical: "https://runexa.ai/ai-disclaimer",
  },
};

export default function AIDisclaimerPage() {
  return (
    <>
      <AIDisclaimerClient />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "WebPage",
            name: "Runexa AI Disclaimer & Transparency",
            description:
              "AI transparency and limitation disclosures for Runexa AI systems and enterprise AI workflows.",
          }),
        }}
      />
    </>
  );
}
