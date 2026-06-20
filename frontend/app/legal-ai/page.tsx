import type { Metadata } from "next";
import LegalAIClient from "./LegalAIClient";

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

  "Runexa Legal Agent",
  "AI contract analysis",
  "contract intelligence AI",
  "contract clause analysis",
  "contract risk detection",
  "legal risk assessment",
  "legal document review",
  "commercial contract review",
  "business contract analysis",
  "contract compliance analysis",
  "AI-powered legal review",
  "legal obligations analysis",
  "contract responsibilities analysis",
  "legal agreement analysis",
  "terms and conditions analysis",
  "legal document summaries",
  "AI legal technology",
  "LegalTech",
  "legal workflow automation",
  "legal document processing",
  "AI document analysis",
  "enterprise contract review",
  "AI contract assistant",
  "AI for lawyers",
  "AI for legal teams",
  "legal operations AI",
  "contract lifecycle management",
  "contract management AI",
  "AI clause extraction",
  "AI compliance review",
  "contract due diligence",
  "legal decision support",
  "document intelligence",
  "business legal intelligence",
  "legal risk detection",
  "legal automation platform",
  "AI legal platform",
  "contract automation",
  "Enterprise Legal AI",
  "Contract Intelligence Platform",
],

  alternates: {
    canonical: "https://runexa.ai/legal-ai",
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
      <LegalAIClient initialLocale="en" />

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

              url: "https://runexa.ai/legal-ai",

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
