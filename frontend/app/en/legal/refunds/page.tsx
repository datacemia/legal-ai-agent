import type { Metadata } from "next";
import RefundPolicyClient from "../../../legal/refunds/RefundPolicyClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Refund Policy | Runexa",

  description:
    "Refund policy for Runexa Systems LLC covering AI credits, subscriptions, billing disputes, chargebacks, and enterprise services.",

  keywords: [
    "refund policy",
    "AI subscription refunds",
    "Runexa billing",
    "AI credits refund",
    "enterprise AI billing",
    "SaaS refund policy",
    "AI billing disputes",
    "subscription cancellation",
  ],

  alternates: {
    canonical: "https://runexa.ai/en/legal/refunds",
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
      "Refund and billing policy for Runexa AI services, subscriptions, credits, enterprise plans, and intelligent workflows.",

    url: "https://runexa.ai/en/legal/refunds",

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
      "Review refund eligibility, billing terms, subscriptions, AI credits, and enterprise billing policies for Runexa Systems LLC.",

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
      <RefundPolicyClient initialLocale="en" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "Runexa Refund Policy",

            description:
              "Refund and billing policy for Runexa AI services, subscriptions, AI credits, enterprise workflows, and intelligent platforms.",

            url: "https://runexa.ai/en/legal/refunds",

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
