import type { Metadata } from "next";
import AIFinanceAnalysisArticle from "../../../blog/ai-finance-analysis/AIFinanceAnalysisArticle";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "AI Finance Analysis: Understanding Spending, Subscriptions, and Savings | Runexa",

  description:
    "Learn how AI finance analysis helps users understand spending patterns, subscriptions, savings opportunities, and financial habits.",

  keywords: [
    "AI finance analysis",
    "personal finance AI",
    "bank statement analysis",
    "subscription detection AI",
    "AI savings analysis",
    "financial habits AI",
    "Runexa Finance Coach",
    "AI budgeting assistant",
  ],

  alternates: {
    canonical: "https://runexa.ai/en/blog/ai-finance-analysis",
    languages: {
      en: `${siteUrl}/en/blog/ai-finance-analysis`,
      fr: `${siteUrl}/fr/blog/ai-finance-analysis`,
      ar: `${siteUrl}/ar/blog/ai-finance-analysis`,
      "x-default": `${siteUrl}/blog/ai-finance-analysis`,
    },
  },

  openGraph: {
    title: "AI Finance Analysis: Understanding Spending, Subscriptions, and Savings | Runexa",

    description:
      "Learn how AI finance analysis helps users understand spending patterns, subscriptions, savings opportunities, and financial habits.",

    url: "https://runexa.ai/en/blog/ai-finance-analysis",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa AI Finance Analysis",
      },
    ],

    locale: "en_US",

    alternateLocale: ["fr_FR", "ar_AR"],

    type: "article",
  },

  twitter: {
    card: "summary_large_image",

    title: "AI Finance Analysis: Understanding Spending, Subscriptions, and Savings | Runexa",

    description:
      "Learn how AI finance analysis helps users understand spending patterns, subscriptions, savings opportunities, and financial habits.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function AIFinanceAnalysisPage() {
  return (
    <>
      <AIFinanceAnalysisArticle initialLocale="en" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "Article",

            mainEntityOfPage: {
              "@type": "WebPage",
              "@id": "https://runexa.ai/en/blog/ai-finance-analysis",
            },

            headline:
              "AI Finance Analysis: Understanding Spending, Subscriptions, and Savings",

            description:
              "Learn how AI finance analysis helps users understand spending patterns, subscriptions, savings opportunities, and financial habits.",

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
