import type { Metadata } from "next";
import DocsClient from "./DocsClient";

export const metadata: Metadata = {
  title: "AI API Documentation | Runexa",

  description:
    "Technical documentation for Runexa AI APIs including legal analysis, finance intelligence, business workflows, asynchronous jobs, authentication, and enterprise integrations.",

  keywords: [
    "Runexa docs",
    "AI API documentation",
    "legal AI API docs",
    "finance AI API docs",
    "business AI API docs",
    "developer documentation",
    "async AI APIs",
    "enterprise AI integration",
  ],

  alternates: {
    canonical: "https://runexa.ai/docs",
  },

  openGraph: {
    title: "AI API Documentation | Runexa",

    description:
      "Technical documentation for Runexa AI APIs including legal analysis, finance intelligence, business workflows, asynchronous jobs, authentication, and enterprise integrations.",

    url: "https://runexa.ai/docs",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa API Documentation",
      },
    ],

    locale: "en_US",

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "AI API Documentation | Runexa",

    description:
      "Technical developer documentation for Runexa asynchronous AI APIs.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function DocsPage() {
  return <DocsClient />;
}
