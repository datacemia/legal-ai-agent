import type { Metadata } from "next";
import ApiClient from "./ApiClient";

export const metadata: Metadata = {
  title: "AI APIs & Agent Infrastructure | Runexa",

  description:
    "Integrate Runexa AI APIs for legal analysis, finance intelligence, study automation, and business decision support workflows.",

  keywords: [
    "Runexa API",
    "AI APIs",
    "legal AI API",
    "finance AI API",
    "study AI API",
    "business AI API",
    "async AI processing",
    "AI infrastructure",
  ],

  alternates: {
    canonical: "https://runexa.ai/api",
  },

  openGraph: {
    title: "AI APIs & Agent Infrastructure | Runexa",

    description:
      "Integrate Runexa AI APIs for legal analysis, finance intelligence, study automation, and business decision support workflows.",

    url: "https://runexa.ai/api",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa API Platform",
      },
    ],

    locale: "en_US",

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "AI APIs & Agent Infrastructure | Runexa",

    description:
      "AI APIs for legal, finance, study, and business automation workflows.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function ApiPage() {
  return <ApiClient />;
}
