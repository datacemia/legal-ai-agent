import type { Metadata } from "next";
import RefundPolicyClient from "./RefundPolicyClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Refund Policy | Runexa",

  description:
    "Refund policy for Runexa Systems LLC covering AI credits, subscriptions, billing disputes, chargebacks, consumer rights where applicable, and enterprise services.",

  keywords: [
  "refund policy",
  "AI subscription refunds",
  "Runexa billing",
  "AI credits refund",
  "enterprise AI billing",
  "SaaS refund policy",
  "AI billing disputes",
  "subscription cancellation",
  "consumer protection",
  "cooling-off rights",
  "billing transparency",

  "Runexa Refund Policy",
  "Runexa billing policy",
  "subscription refunds",
  "AI subscription billing",
  "AI service refunds",
  "subscription management",
  "subscription terms",
  "monthly subscription cancellation",
  "annual subscription cancellation",
  "service cancellation",
  "account cancellation",
  "billing and payments",
  "payment policy",
  "refund eligibility",
  "refund requests",
  "billing disputes",
  "payment disputes",
  "charge disputes",
  "billing support",
  "account billing",
  "digital services refunds",
  "SaaS billing",
  "SaaS subscriptions",
  "AI platform subscriptions",
  "AI credits",
  "AI credit purchases",
  "AI credit usage",
  "AI credit refunds",
  "enterprise subscriptions",
  "enterprise billing",
  "business billing",
  "online payments",
  "electronic billing",
  "pricing transparency",
  "consumer rights",
  "digital consumer protection",
  "right of withdrawal",
  "cooling-off period",
  "Runexa subscriptions",
  "subscription billing policy",
],

  alternates: {
    canonical: "https://runexa.ai/legal/refunds",
    languages: {
      en: `${siteUrl}/en/legal/refunds`,
      fr: `${siteUrl}/fr/legal/refunds`,
      ar: `${siteUrl}/ar/legal/refunds`,
      "x-default": `${siteUrl}/legal/refunds`,
    },
  },

  openGraph: {
    title: "Refund Policy | Runexa",

    description:
      "Refund policy for Runexa Systems LLC covering AI credits, subscriptions, billing disputes, chargebacks, consumer rights where applicable, and enterprise services.",

    url: "https://runexa.ai/legal/refunds",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Refund Policy",
      },
    ],

    locale: "en_US",

    alternateLocale: ["fr_FR", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Refund Policy | Runexa",

    description:
      "Refund policy for Runexa Systems LLC covering AI credits, subscriptions, billing disputes, chargebacks, consumer rights where applicable, and enterprise services.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function RefundPolicyPage() {
  return (
    <>
      <RefundPolicyClient initialLocale="en" />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "Runexa Refund Policy",

            description:
              "Refund and billing policy for Runexa AI services, subscriptions, AI credits, enterprise workflows, billing disputes, cancellations, and consumer protection rights where applicable.",

            url: "https://runexa.ai/legal/refunds",

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
