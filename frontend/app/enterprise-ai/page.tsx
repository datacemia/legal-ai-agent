import type { Metadata } from "next";
import EnterpriseAIClient from "./EnterpriseAIClient";

export const metadata: Metadata = {
  title: "Enterprise AI Workspace & Custom AI Systems | Runexa",

  description:
    "Secure enterprise AI workflows for legal analysis, financial reporting, business intelligence, learning operations, and organizational decision support.",

  keywords: [
    "enterprise AI",
    "custom AI systems",
    "AI workspace",
    "enterprise AI workflows",
    "business intelligence AI",
    "organizational AI",
    "Runexa enterprise AI",
    "AI decision support",
  ],

  alternates: {
    canonical: "https://runexa.ai/enterprise-ai",
  },

  openGraph: {
    title: "Enterprise AI Workspace & Custom AI Systems | Runexa",

    description:
      "Secure enterprise AI workflows for legal analysis, financial reporting, business intelligence, learning operations, and organizational decision support.",

    url: "https://runexa.ai/enterprise-ai",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Enterprise AI",
      },
    ],

    locale: "en_US",

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Enterprise AI Workspace & Custom AI Systems | Runexa",

    description:
      "Enterprise AI workflows for document analysis, finance intelligence, learning operations, and business decision support.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function EnterpriseAIPage() {
  return <EnterpriseAIClient />;
}
