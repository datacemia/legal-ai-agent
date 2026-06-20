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

  "Runexa Terms of Service",
  "Runexa Terms",
  "AI terms and conditions",
  "AI service agreement",
  "AI platform agreement",
  "AI usage terms",
  "AI user agreement",
  "enterprise AI agreement",
  "AI software terms",
  "SaaS terms and conditions",
  "API terms of use",
  "developer terms",
  "enterprise subscription terms",
  "subscription terms",
  "billing and payment terms",
  "AI credit usage",
  "AI credit policy",
  "account management terms",
  "service eligibility",
  "authorized use",
  "acceptable use",
  "AI platform policies",
  "uploaded content terms",
  "document upload policy",
  "user content policy",
  "intellectual property rights",
  "software license terms",
  "limitation of liability",
  "disclaimer of warranties",
  "service availability",
  "termination of service",
  "account suspension",
  "cancellation terms",
  "refund terms",
  "minor users",
  "children and teens",
  "parental consent",
  "student users",
  "AI governance",
  "responsible AI use",
  "enterprise compliance",
  "AI platform rules",
  "digital services terms",
  "online service agreement",
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
