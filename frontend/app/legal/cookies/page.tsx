import type { Metadata } from "next";
import CookiePolicyClient from "./CookiePolicyClient";

export const metadata: Metadata = {
  title: "Cookie Policy | Runexa",

  description:
    "Cookie policy explaining how Runexa Systems LLC uses cookies, analytics, authentication, and related technologies.",

  keywords: [
    "cookie policy",
    "Runexa cookies",
    "AI platform cookies",
    "website cookies",
    "analytics cookies",
    "privacy cookies",
  ],

  alternates: {
    canonical: "https://runexa.ai/cookie-policy",
  },
};

export default function CookiePolicyPage() {
  return (
    <>
      <CookiePolicyClient />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "WebPage",
            name: "Runexa Cookie Policy",
            description:
              "Cookie usage and browser tracking disclosures for Runexa AI services and enterprise platforms.",
          }),
        }}
      />
    </>
  );
}
