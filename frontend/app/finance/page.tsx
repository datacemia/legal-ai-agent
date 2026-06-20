import type { Metadata } from "next";
import FinanceClient from "./FinanceClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "AI Personal Finance Coach & Financial Intelligence | Runexa",

  description:
    "Analyze bank statements, detect subscriptions, monitor spending, discover savings opportunities, and receive AI financial coaching with Runexa Finance AI.",

 keywords: [
  "AI finance coach",
  "AI financial analysis",
  "bank statement analysis",
  "personal finance AI",
  "AI budgeting assistant",
  "subscription detection AI",
  "financial intelligence",
  "AI savings analysis",

  "Runexa Finance Coach",
  "finance AI",
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
    canonical: "https://runexa.ai/finance",
    languages: {
      en: `${siteUrl}/en/finance`,
      fr: `${siteUrl}/fr/finance`,
      ar: `${siteUrl}/ar/finance`,
      "x-default": `${siteUrl}/finance`,
    },
  },

  openGraph: {
    title: "AI Personal Finance Coach & Financial Intelligence | Runexa",

    description:
      "Analyze bank statements, detect subscriptions, monitor spending, discover savings opportunities, and receive AI financial coaching with Runexa Finance AI.",

    url: "https://runexa.ai/finance",

    siteName: "Runexa Systems",

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

    title: "AI Personal Finance Coach & Financial Intelligence | Runexa",

    description:
      "AI-powered financial intelligence for bank statement analysis, budgeting, subscription detection, and savings optimization.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function FinancePage() {
  return (
    <>
      <FinanceClient initialLocale="en" />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "SoftwareApplication",

            name: "Runexa Finance AI",

            applicationCategory: "FinanceApplication",

            operatingSystem: "Web",

            description:
              "AI financial intelligence platform for bank statement analysis, subscription detection, budgeting, and savings optimization.",

            url: "https://runexa.ai/finance",

            inLanguage: "en",

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems",
              url: siteUrl,
            },

            knowsAbout: [
              "AI Finance Coach",
              "Financial Analysis",
              "Bank Statement Analysis",
              "Personal Finance AI",
              "Budgeting AI",
              "Savings Optimization",
            ],
          }),
        }}
      />
    </>
  );
}
