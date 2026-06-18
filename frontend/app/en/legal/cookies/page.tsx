import type { Metadata } from "next";
import CookiePolicyClient from "../../../legal/cookies/CookiePolicyClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Cookie Policy | Runexa",

  description:
    "Cookie policy explaining how Runexa Systems LLC uses cookies, analytics, authentication, security technologies, and related services across our AI platforms and enterprise infrastructure.",

  keywords: [
    "cookie policy",
    "Runexa cookies",
    "AI platform cookies",
    "website cookies",
    "analytics cookies",
    "privacy cookies",
    "security cookies",
    "enterprise AI compliance",
  ],

  alternates: {
    canonical: "https://runexa.ai/en/legal/cookies",
    languages: {
      en: `${siteUrl}/en/legal/cookies`,
      fr: `${siteUrl}/fr/legal/cookies`,
      ar: `${siteUrl}/ar/legal/cookies`,
      "x-default": `${siteUrl}/legal/cookies`,
    },
  },

  openGraph: {
    title: "Cookie Policy | Runexa",

    description:
      "Review how Runexa Systems LLC uses cookies, analytics, authentication, and security technologies across AI platforms and enterprise services.",

    url: "https://runexa.ai/en/legal/cookies",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Cookie Policy",
      },
    ],

    locale: "en_US",

    alternateLocale: ["fr_FR", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Cookie Policy | Runexa",

    description:
      "Review cookie usage, analytics technologies, authentication systems, and security-related services used by Runexa.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function CookiePolicyPage() {
  return (
    <>
      <CookiePolicyClient initialLocale="en" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "Runexa Cookie Policy",

            description:
              "Cookie usage, analytics technologies, authentication systems, and browser tracking disclosures for Runexa AI services and enterprise platforms.",

            url: "https://runexa.ai/en/legal/cookies",

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
