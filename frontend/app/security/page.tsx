import type { Metadata } from "next";
import SecurityClient from "./SecurityClient";

export const metadata: Metadata = {
  title: "Security & Infrastructure | Runexa",

  description:
    "Learn about Runexa security practices, encryption, infrastructure safeguards, access controls, payment security, and AI platform protections.",

  keywords: [
    "AI security",
    "enterprise AI security",
    "AI infrastructure",
    "Runexa security",
    "AI platform security",
    "AI encryption",
    "AI data protection",
  ],

  alternates: {
    canonical: "https://runexa.ai/security",
  },
};

export default function SecurityPage() {
  return (
    <>
      <SecurityClient />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "WebPage",
            name: "Runexa Security",
            description:
              "Security practices and infrastructure protections for Runexa AI systems and enterprise AI workflows.",
          }),
        }}
      />
    </>
  );
}
