import type { Metadata } from "next";
import LegalAIClient from "../../legal-ai/LegalAIClient";

const siteUrl = "https://runexa.ai";

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
    canonical: "https://runexa.ai/en/legal-ai",
    languages: {
      en: `${siteUrl}/en/legal-ai`,
      fr: `${siteUrl}/fr/legal-ai`,
      ar: `${siteUrl}/ar/legal-ai`,
      "x-default": `${siteUrl}/legal-ai`,
    },
  },

  openGraph: {
    title: "AI Contract Review & Legal Document Analysis | Runexa",

    description:
      "Analyze contracts, detect risky clauses, extract obligations, and generate legal document summaries with Runexa Legal AI.",

    url: "https://runexa.ai/en/legal-ai",

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

    alternateLocale: ["fr_FR", "ar_AR"],

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
  return (
    <>
      <LegalAIClient initialLocale="en" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify([
            {
              "@context": "https://schema.org",

              "@type": "SoftwareApplication",

              name: "Runexa Legal AI",

              applicationCategory: "BusinessApplication",

              operatingSystem: "Web",

              url: "https://runexa.ai/en/legal-ai",

              inLanguage: "en",

              description:
                "AI contract review and legal document analysis software for risky clause detection, obligation extraction, summaries, and recommendations.",

              publisher: {
                "@type": "Organization",
                name: "Runexa Systems LLC",
                url: siteUrl,
              },

              knowsAbout: [
                "Legal AI",
                "AI Contract Review",
                "Legal Document Analysis",
                "Contract Risk Analysis",
                "Obligation Extraction",
                "Legal Workflow AI",
              ],
            },
          ]),
        }}
      />
    </>
  );
}
