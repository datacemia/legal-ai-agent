import type { Metadata } from "next";
import UploadClient from "../../upload/UploadClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "AI Contract Review & Legal Document Analysis | Runexa",

  description:
    "Analyze contracts, detect risky clauses, understand obligations, and receive structured legal intelligence with Runexa AI Legal Agent.",

  keywords: [
  "AI contract review",
  "legal AI",
  "contract analysis AI",
  "legal document analysis",
  "AI legal assistant",
  "contract risk analysis",
  "enterprise legal AI",
  "Runexa legal agent",
  "AI contract intelligence",

  "Runexa Legal Agent",
  "AI contract analysis",
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
  "contract summaries",
  "legal document summaries",
  "AI legal technology",
  "LegalTech",
  "legal workflow automation",
  "legal workflow AI",
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
],

  alternates: {
    canonical: "https://runexa.ai/en/upload",
    languages: {
      en: `${siteUrl}/en/upload`,
      fr: `${siteUrl}/fr/upload`,
      ar: `${siteUrl}/ar/upload`,
      "x-default": `${siteUrl}/upload`,
    },
  },

  openGraph: {
    title: "Runexa Legal AI",

    description:
      "AI-powered contract analysis, legal risk detection, obligation extraction, and structured legal intelligence.",

    url: "https://runexa.ai/en/upload",

    siteName: "Runexa Systems",

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

    title: "Runexa Legal AI",

    description:
      "Analyze contracts and legal documents with AI-powered legal intelligence.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function UploadPage() {
  return (
    <>
      <UploadClient initialLocale="en" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "SoftwareApplication",

            name: "Runexa Legal AI",

            applicationCategory: "BusinessApplication",

            operatingSystem: "Web",

            description:
              "AI-powered legal document analysis platform for contracts, obligations, risk detection, and negotiation insights.",

            url: "https://runexa.ai/en/upload",

            inLanguage: "en",

            provider: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: siteUrl,
            },

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: siteUrl,
            },

            offers: {
              "@type": "Offer",
              price: "1",
              priceCurrency: "USD",
            },

            knowsAbout: [
              "AI Contract Review",
              "Legal AI",
              "Contract Analysis",
              "Legal Document Analysis",
              "Contract Risk Analysis",
              "Obligation Extraction",
            ],
          }),
        }}
      />
    </>
  );
}
