import type { Metadata } from "next";
import UploadClient from "./UploadClient";

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
  ],

  alternates: {
    canonical: "https://runexa.ai/upload",
  },

  openGraph: {
    title: "Runexa Legal AI",

    description:
      "AI-powered contract analysis, legal risk detection, obligation extraction, and structured legal intelligence.",

    url: "https://runexa.ai/upload",

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
      <UploadClient />

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

            url: "https://runexa.ai/upload",

            provider: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: "https://runexa.ai",
            },

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: "https://runexa.ai",
            },

            offers: {
              "@type": "Offer",
              price: "1",
              priceCurrency: "USD",
            },
          }),
        }}
      />
    </>
  );
}
