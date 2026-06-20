import type { Metadata } from "next";
import FinanceAIClient from "./FinanceAIClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "AI Financial Analysis & Personal Finance Coach | Runexa",

  description:
    "Analyze bank statements, detect subscriptions, identify savings opportunities, and improve financial habits using Runexa Finance AI.",

 keywords: [
  "finance AI",
  "AI financial analysis",
  "bank statement analysis",
  "subscription detection AI",
  "personal finance AI",
  "AI savings analysis",
  "Runexa finance AI",
  "financial coaching AI",

  "Runexa Finance Coach",
  "AI finance coach",
  "AI financial assistant",
  "AI personal finance coach",
  "AI money management",
  "expense analysis AI",
  "spending analysis AI",
  "monthly spending analysis",
  "income and expense analysis",
  "bank account analysis",
  "financial insights AI",
  "financial planning AI",
  "budget planning AI",
  "budget management AI",
  "AI budgeting assistant",
  "smart budgeting",
  "AI savings recommendations",
  "subscription management AI",
  "recurring expense detection",
  "cash flow analysis",
  "financial behavior analysis",
  "financial habits AI",
  "financial wellness AI",
  "financial education AI",
  "AI spending tracker",
  "personal finance management",
  "expense categorization AI",
  "financial dashboard AI",
  "AI financial reports",
  "AI money insights",
  "AI financial analytics",
  "consumer finance AI",
  "household budget AI",
  "financial decision support",
  "AI-powered budgeting",
  "AI financial coaching",
  "AI wealth insights",
  "personal budgeting software",
  "finance workflow automation",
  "Finance AI",
  "Personal Finance AI",
],
  alternates: {
    canonical: "https://runexa.ai/finance-ai",
    languages: {
      en: `${siteUrl}/en/finance-ai`,
      fr: `${siteUrl}/fr/finance-ai`,
      ar: `${siteUrl}/ar/finance-ai`,
      "x-default": `${siteUrl}/finance-ai`,
    },
  },

  openGraph: {
    title: "AI Financial Analysis & Personal Finance Coach | Runexa",

    description:
      "Analyze bank statements, detect subscriptions, identify savings opportunities, and improve financial habits using Runexa Finance AI.",

    url: "https://runexa.ai/finance-ai",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Finance AI",
      },
    ],

    locale: "en_US",

    alternateLocale: ["fr_FR", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "AI Financial Analysis & Personal Finance Coach | Runexa",

    description:
      "AI-powered financial analysis for bank statements, subscriptions, savings opportunities, and personal finance coaching.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function FinanceAIPage() {
  return (
    <>
      <FinanceAIClient initialLocale="en" />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify([
            {
              "@context": "https://schema.org",

              "@type": "SoftwareApplication",

              name: "Runexa Finance AI",

              applicationCategory: "FinanceApplication",

              operatingSystem: "Web",

              url: "https://runexa.ai/finance-ai",

              inLanguage: "en",

              description:
                "AI finance coach for bank statement analysis, subscription detection, savings opportunities, and financial habits.",

              publisher: {
                "@type": "Organization",
                name: "Runexa Systems LLC",
                url: siteUrl,
              },

              knowsAbout: [
                "Finance AI",
                "AI Financial Analysis",
                "Bank Statement Analysis",
                "Subscription Detection",
                "Personal Finance AI",
                "Financial Coaching AI",
              ],
            },
          ]),
        }}
      />
    </>
  );
}
