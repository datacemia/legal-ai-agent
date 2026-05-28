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
    "AI uploads privacy",
    "AI compliance",
  ],

  alternates: {
    canonical: "https://runexa.ai/privacy",
  },

  openGraph: {
    title: "Privacy Policy | Runexa",

    description:
      "Privacy Policy explaining how Runexa Systems LLC collects, uses, stores, protects, and processes personal information and uploaded content.",

    url: "https://runexa.ai/privacy",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Privacy Policy",
      },
    ],

    locale: "en_US",

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Privacy Policy | Runexa",

    description:
      "Privacy and data processing disclosures for Runexa AI services, APIs, uploads, and enterprise workflows.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
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

            url: "https://runexa.ai/privacy",

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
