import type { Metadata } from "next";
import AIContractAnalysisArticle from "../../../blog/ai-contract-analysis/AIContractAnalysisArticle";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "AI Contract Analysis: How AI Helps Review Legal Documents | Runexa",

  description:
    "Learn how AI contract analysis helps identify risky clauses, summarize obligations, and support legal document review workflows.",

  keywords: [
    "AI contract analysis",
    "AI contract review",
    "legal document analysis",
    "legal AI",
    "contract risk detection",
    "AI legal assistant",
    "contract summaries",
    "Runexa Legal Agent",
  ],

  alternates: {
    canonical: "https://runexa.ai/en/blog/ai-contract-analysis",
    languages: {
      en: `${siteUrl}/en/blog/ai-contract-analysis`,
      fr: `${siteUrl}/fr/blog/ai-contract-analysis`,
      ar: `${siteUrl}/ar/blog/ai-contract-analysis`,
      "x-default": `${siteUrl}/blog/ai-contract-analysis`,
    },
  },

  openGraph: {
    title: "AI Contract Analysis: How AI Helps Review Legal Documents | Runexa",

    description:
      "Learn how AI contract analysis helps identify risky clauses, summarize obligations, and support legal document review workflows.",

    url: "https://runexa.ai/en/blog/ai-contract-analysis",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa AI Contract Analysis",
      },
    ],

    locale: "en_US",

    alternateLocale: ["fr_FR", "ar_AR"],

    type: "article",
  },

  twitter: {
    card: "summary_large_image",

    title: "AI Contract Analysis: How AI Helps Review Legal Documents | Runexa",

    description:
      "Learn how AI contract analysis helps identify risky clauses, summarize obligations, and support legal document review workflows.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function AIContractAnalysisPage() {
  return (
    <>
      <AIContractAnalysisArticle initialLocale="en" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "Article",

            mainEntityOfPage: {
              "@type": "WebPage",
              "@id": "https://runexa.ai/en/blog/ai-contract-analysis",
            },

            headline:
              "AI Contract Analysis: How AI Helps Review Legal Documents",

            description:
              "Learn how AI contract analysis helps identify risky clauses, summarize obligations, and support legal document review workflows.",

            datePublished: "2026-05-24",

            dateModified: "2026-05-24",

            inLanguage: "en",

            author: {
              "@type": "Person",
              name: "Dr. Rachid Ejjami",
            },

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: siteUrl,
            },
          }),
        }}
      />
    </>
  );
}
