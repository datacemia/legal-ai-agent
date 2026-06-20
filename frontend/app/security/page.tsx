import type { Metadata } from "next";
import SecurityClient from "./SecurityClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Security & Infrastructure | Runexa",

  description:
    "Learn about Runexa security practices, encryption, infrastructure safeguards, access controls, payment security, responsible uploads, and AI platform protections.",

  keywords: [
    "AI security",
    "enterprise AI security",
    "AI infrastructure",
    "Runexa security",
    "AI platform security",
    "AI encryption",
    "AI data protection",
    "enterprise AI compliance",
    "responsible uploads",
    "secure AI workflows",
  ],

  alternates: {
    canonical: "https://runexa.ai/security",
    languages: {
      en: `${siteUrl}/en/security`,
      fr: `${siteUrl}/fr/security`,
      ar: `${siteUrl}/ar/security`,
      "x-default": `${siteUrl}/security`,
    },
  },

  openGraph: {
    title: "Security & Infrastructure | Runexa",

    description:
      "Learn about Runexa security practices, encryption, infrastructure safeguards, access controls, payment security, responsible uploads, and AI platform protections.",

    url: "https://runexa.ai/security",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Security",
      },
    ],

    locale: "en_US",

    alternateLocale: ["fr_FR", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Security & Infrastructure | Runexa",

    description:
      "Learn about Runexa security practices, encryption, infrastructure safeguards, access controls, payment security, responsible uploads, and AI platform protections.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function SecurityPage() {
  return (
    <>
      <SecurityClient initialLocale="en" />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "Runexa Security",

            description:
              "Security practices, responsible upload guidance, and infrastructure protections for Runexa AI systems and enterprise AI workflows.",

            url: "https://runexa.ai/security",

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
