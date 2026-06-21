import type { Metadata } from "next";
import ApiDashboardClient from "./ApiDashboardClient";

export const metadata: Metadata = {
  title: "API Dashboard & Usage Analytics | Runexa",

  description:
    "Manage Runexa API keys, monitor AI usage, track credits, and control enterprise AI infrastructure from the Runexa API dashboard.",

  keywords: [
  "Runexa API dashboard",
  "AI API analytics",
  "API usage monitoring",
  "AI infrastructure dashboard",
  "API key management",
  "AI usage analytics",
  "enterprise AI dashboard",
  "Runexa developer platform",

  "Runexa developer dashboard",
  "API dashboard",
  "developer portal",
  "developer console",
  "API management platform",
  "API monitoring",
  "API observability",
  "API performance monitoring",
  "API metrics",
  "API insights",
  "API reporting",
  "usage analytics",
  "real-time analytics",
  "AI analytics dashboard",
  "AI platform analytics",
  "enterprise analytics",
  "AI infrastructure monitoring",
  "system monitoring",
  "service monitoring",
  "request tracking",
  "API request logs",
  "API health monitoring",
  "API status dashboard",
  "API consumption tracking",
  "AI usage tracking",
  "token usage analytics",
  "credit usage analytics",
  "AI credits dashboard",
  "billing analytics",
  "developer billing dashboard",
  "API cost tracking",
  "enterprise usage reporting",
  "API key management",
  "API credential management",
  "API access control",
  "developer account management",
  "webhook monitoring",
  "integration monitoring",
  "AI workflow monitoring",
  "developer tools",
  "enterprise developer platform",
  "Runexa APIs",
  "AI infrastructure platform",
  "developer experience",
  "DX platform",
  "API governance",
  "enterprise API management",
],

  alternates: {
    canonical: "https://runexa.ai/api-dashboard",
  },

  openGraph: {
    title: "API Dashboard & Usage Analytics | Runexa",

    description:
      "Manage API keys, monitor AI requests, track credits, and control Runexa AI infrastructure.",

    url: "https://runexa.ai/api-dashboard",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa API Dashboard",
      },
    ],

    locale: "en_US",

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "API Dashboard & Usage Analytics | Runexa",

    description:
      "Monitor AI API usage, credits, requests, and enterprise integrations.",

    images: ["/og-image.png"],
  },

  robots: {
    index: false,
    follow: false,
  },
};

export default function ApiDashboardPage() {
  return <ApiDashboardClient />;
}
