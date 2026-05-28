import type { Metadata } from "next";
import FinanceAIClient from "./FinanceAIClient";

export const metadata: Metadata = {
  title: "AI Financial Analysis & Personal Finance Coach | Runexa",

  description:
    "Analyze bank statements, detect subscriptions, identify savings opportunities, and improve financial habits using Runexa Finance AI.",

  keywords: [
    "finance AI",
    "AI financial analysis",
    "bank statement analysis",
    "subscription detection AI",
    "personal finance AI",
    "AI savings analysis",
    "Runexa finance AI",
    "financial coaching AI",
  ],

  alternates: {
    canonical: "https://runexa.ai/finance-ai",
  },

  openGraph: {
    title: "AI Financial Analysis & Personal Finance Coach | Runexa",

    description:
      "Analyze bank statements, detect subscriptions, identify savings opportunities, and improve financial habits using Runexa Finance AI.",

    url: "https://runexa.ai/finance-ai",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Finance AI",
      },
    ],

    locale: "en_US",

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "AI Financial Analysis & Personal Finance Coach | Runexa",

    description:
      "AI-powered financial analysis for bank statements, subscriptions, savings opportunities, and personal finance coaching.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function FinanceAIPage() {
  return <FinanceAIClient />;
}
