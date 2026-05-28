import type { Metadata } from "next";
import BlogClient from "./BlogClient";

export const metadata: Metadata = {
  title: "Enterprise AI Blog & Insights | Runexa",

  description:
    "Insights about legal AI, finance AI, enterprise AI workflows, business intelligence, and AI-powered operational systems.",

  keywords: [
    "AI blog",
    "enterprise AI",
    "legal AI",
    "finance AI",
    "AI workflows",
    "business intelligence AI",
    "Runexa blog",
    "AI automation insights",
  ],

  alternates: {
    canonical: "https://runexa.ai/blog",
  },

  openGraph: {
    title: "Enterprise AI Blog & Insights | Runexa",

    description:
      "Insights about legal AI, finance AI, enterprise AI workflows, business intelligence, and AI-powered operational systems.",

    url: "https://runexa.ai/blog",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa AI Blog",
      },
    ],

    locale: "en_US",

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Enterprise AI Blog & Insights | Runexa",

    description:
      "AI insights covering legal analysis, finance intelligence, enterprise automation, and business workflows.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function BlogPage() {
  return <BlogClient />;
}
