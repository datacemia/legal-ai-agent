import type { Metadata } from "next";
import RefundPolicyClient from "./RefundPolicyClient";

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
    canonical: "https://runexa.ai/legal/refunds",
  },

  openGraph: {
    title: "Refund Policy | Runexa",

    description:
      "Refund and billing policy for Runexa AI services, subscriptions, credits, enterprise plans, and intelligent workflows.",

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
      <RefundPolicyClient />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "Runexa Refund Policy",

            description:
              "Refund and billing policy for Runexa AI services, subscriptions, AI credits, enterprise workflows, and intelligent platforms.",

            url: "https://runexa.ai/legal/refunds",

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
