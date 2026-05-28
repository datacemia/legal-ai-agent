import type { Metadata } from "next";
import BusinessAIClient from "./BusinessAIClient";

export const metadata: Metadata = {
  title: "AI Business Intelligence & Decision Support | Runexa",

  description:
    "Analyze business data, detect risks, discover opportunities, and improve strategic decisions with Runexa Business AI.",

  keywords: [
    "business AI",
    "AI business intelligence",
    "business decision support",
    "AI KPI analysis",
    "business risk analysis",
    "AI forecasting",
    "Runexa business AI",
    "AI business workflows",
  ],

  alternates: {
    canonical: "https://runexa.ai/business-ai",
  },

  openGraph: {
    title: "AI Business Intelligence & Decision Support | Runexa",

    description:
      "Analyze business data, detect risks, discover opportunities, and improve strategic decisions with Runexa Business AI.",

    url: "https://runexa.ai/business-ai",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Business AI",
      },
    ],

    locale: "en_US",

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "AI Business Intelligence & Decision Support | Runexa",

    description:
      "AI-powered business intelligence for KPI analysis, strategic insights, forecasting, and operational decision support.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function BusinessAIPage() {
  return <BusinessAIClient />;
}
