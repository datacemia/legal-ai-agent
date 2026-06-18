import type { Metadata } from "next";
import PrivacyClient from "../../privacy/PrivacyClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Politique de confidentialité | Runexa",

  description:
    "Politique de confidentialité expliquant comment Runexa Systems LLC collecte, utilise, stocke, protège et traite les informations personnelles et contenus importés.",

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
    canonical: "https://runexa.ai/fr/privacy",
    languages: {
      en: `${siteUrl}/en/privacy`,
      fr: `${siteUrl}/fr/privacy`,
      ar: `${siteUrl}/ar/privacy`,
      "x-default": `${siteUrl}/privacy`,
    },
  },

  openGraph: {
    title: "Politique de confidentialité | Runexa",

    description:
      "Politique de confidentialité expliquant comment Runexa Systems LLC collecte, utilise, stocke, protège et traite les informations personnelles et contenus importés.",

    url: "https://runexa.ai/fr/privacy",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Privacy Policy",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Politique de confidentialité | Runexa",

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
      <PrivacyClient initialLocale="fr" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "Politique de confidentialité Runexa",

            description:
              "Privacy and data processing disclosures for Runexa AI services, APIs, uploads, and enterprise workflows.",

            url: "https://runexa.ai/fr/privacy",

            inLanguage: "fr",

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
