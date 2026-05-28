import type { Metadata } from "next";
import LegalAIClient from "./LegalAIClient";

export const metadata: Metadata = {
  title: "AI Contract Review & Legal Document Analysis | Runexa",

  description:
    "Analyze contracts, detect risky clauses, extract obligations, and generate legal document summaries with Runexa Legal AI.",

  keywords: [
    "legal AI",
    "AI contract review",
    "legal document analysis",
    "contract risk analysis",
    "AI legal assistant",
    "contract summaries",
    "Runexa legal AI",
    "legal workflow AI",
  ],

  alternates: {
    canonical: "https://runexa.ai/legal-ai",
  },

  openGraph: {
    title: "AI Contract Review & Legal Document Analysis | Runexa",

    description:
      "Analyze contracts, detect risky clauses, extract obligations, and generate legal document summaries with Runexa Legal AI.",

    url: "https://runexa.ai/legal-ai",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Legal AI",
      },
    ],

    locale: "en_US",

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "AI Contract Review & Legal Document Analysis | Runexa",

    description:
      "AI-powered contract review, legal risk detection, obligation extraction, and legal workflow analysis.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function LegalAIPage() {
  return <LegalAIClient />;
}
