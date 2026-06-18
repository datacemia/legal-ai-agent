import type { Metadata } from "next";
import FinanceClient from "../../finance/FinanceClient";

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
  ],

  alternates: {
    canonical: "https://runexa.ai/en/finance",
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

    url: "https://runexa.ai/en/finance",

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
      <FinanceClient initialLocale="en" lockInitialLocale />

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

            url: "https://runexa.ai/en/finance",

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
