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
  ],

  alternates: {
    canonical: "https://runexa.ai/refund-policy",
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
              "Refund and billing policy for Runexa AI services, subscriptions, credits, and enterprise workflows.",
          }),
        }}
      />
    </>
  );
}
