import type { Metadata } from "next";
import TermsClient from "./TermsClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Terms of Service | Runexa",

  description:
    "Terms of Service governing Runexa AI agents, APIs, uploads, credits, subscriptions, minors’ use, billing, and AI-powered services.",

  keywords: [
    "terms of service",
    "AI platform terms",
    "Runexa terms",
    "AI SaaS terms",
    "AI API terms",
    "enterprise AI terms",
    "AI subscriptions",
    "AI credits",
    "minors use",
    "AI uploads",
    "billing terms",
  ],

  alternates: {
    canonical: "https://runexa.ai/terms",
    languages: {
      en: `${siteUrl}/en/terms`,
      fr: `${siteUrl}/fr/terms`,
      ar: `${siteUrl}/ar/terms`,
      "x-default": `${siteUrl}/terms`,
    },
  },

  openGraph: {
    title: "Terms of Service | Runexa",

    description:
      "Terms of Service governing Runexa AI agents, APIs, uploads, credits, subscriptions, minors’ use, billing, and AI-powered services.",

    url: "https://runexa.ai/terms",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Terms of Service",
      },
    ],

    locale: "en_US",

    alternateLocale: ["fr_FR", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Terms of Service | Runexa",

    description:
      "Terms of Service governing Runexa AI agents, APIs, uploads, credits, subscriptions, minors’ use, billing, and AI-powered services.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function TermsPage() {
  return (
    <>
      <TermsClient initialLocale="en" />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "Runexa Terms of Service",

            description:
              "Terms governing Runexa AI agents, APIs, uploads, enterprise workflows, credits, subscriptions, minors’ use, billing, and AI-powered services.",

            url: "https://runexa.ai/terms",

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
