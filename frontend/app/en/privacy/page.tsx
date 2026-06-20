import type { Metadata } from "next";
import PrivacyClient from "../../privacy/PrivacyClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Privacy Policy | Runexa",

  description:
    "Privacy Policy explaining how Runexa Systems LLC collects, uses, stores, protects, processes, transfers, and safeguards personal information, uploaded content, and minors’ privacy for international users.",

  keywords: [
  "privacy policy",
  "AI privacy",
  "Runexa privacy",
  "AI data processing",
  "enterprise AI privacy",
  "AI platform privacy",
  "AI uploads privacy",
  "AI compliance",
  "AI model training",
  "international data transfers",
  "automated processing",
  "GDPR",
  "UK GDPR",
  "children privacy",
  "minors privacy",

  "Runexa Privacy Policy",
  "data protection",
  "personal data protection",
  "AI data protection",
  "enterprise data privacy",
  "user privacy",
  "data security",
  "information security",
  "privacy compliance",
  "GDPR compliance",
  "UK GDPR compliance",
  "data subject rights",
  "privacy rights",
  "personal information",
  "data collection",
  "data usage",
  "data retention",
  "data deletion",
  "data access requests",
  "cross-border data transfers",
  "international data processing",
  "lawful basis for processing",
  "AI document privacy",
  "uploaded document privacy",
  "document security",
  "enterprise data governance",
  "privacy by design",
  "AI governance",
  "responsible AI",
  "AI transparency",
  "AI platform security",
  "enterprise AI compliance",
  "children's privacy",
  "privacy for minors",
  "parental consent",
  "student privacy",
  "online privacy protection",
  "Runexa data protection",
  "AI privacy compliance",
  "enterprise privacy policy",
],

  alternates: {
    canonical: "https://runexa.ai/en/privacy",
    languages: {
      en: `${siteUrl}/en/privacy`,
      fr: `${siteUrl}/fr/privacy`,
      ar: `${siteUrl}/ar/privacy`,
      "x-default": `${siteUrl}/privacy`,
    },
  },

  openGraph: {
    title: "Privacy Policy | Runexa",

    description:
      "Privacy Policy explaining how Runexa Systems LLC collects, uses, stores, protects, processes, transfers, and safeguards personal information, uploaded content, and minors’ privacy for international users.",

    url: "https://runexa.ai/en/privacy",

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

    alternateLocale: ["fr_FR", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Privacy Policy | Runexa",

    description:
      "Privacy Policy explaining how Runexa Systems LLC collects, uses, stores, protects, processes, transfers, and safeguards personal information, uploaded content, and minors’ privacy for international users.",

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
      <PrivacyClient initialLocale="en" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "PrivacyPolicy",

            name: "Runexa Privacy Policy",

            description:
              "Privacy Policy explaining how Runexa Systems LLC collects, uses, stores, protects, processes, transfers, and safeguards personal information, uploaded content, and minors’ privacy for international users.",

            url: "https://runexa.ai/en/privacy",

            inLanguage: "en",

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: siteUrl,
            },

            jurisdiction: [
              "United States",
              "European Union",
              "United Kingdom",
              "International",
            ],
          }),
        }}
      />
    </>
  );
}
