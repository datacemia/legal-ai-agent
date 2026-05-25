import type { Metadata } from "next";
import PrivacyClient from "./PrivacyClient";

export const metadata: Metadata = {
  title: "Privacy Policy | Runexa",
  description:
    "Privacy Policy explaining how Runexa Systems LLC collects, uses, stores, protects, and processes personal information and uploaded content.",
  keywords: [
    "privacy policy",
    "AI privacy",
    "Runexa privacy",
    "AI data processing",
    "enterprise AI privacy",
    "AI platform privacy",
  ],
  alternates: {
    canonical: "https://runexa.ai/privacy",
  },
};

export default function PrivacyPage() {
  return (
    <>
      <PrivacyClient />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "WebPage",
            name: "Runexa Privacy Policy",
            description:
              "Privacy and data processing disclosures for Runexa AI services, APIs, uploads, and enterprise workflows.",
          }),
        }}
      />
    </>
  );
}
