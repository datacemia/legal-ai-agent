import type { Metadata } from "next";
import BusinessClient from "../../business/BusinessClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Business Decision Intelligence | Runexa",

  description:
    "Analyze business data with Runexa Business Agent. Get KPIs, risks, opportunities, forecasts, charts, and executive decision support powered by AI.",

  keywords: [
    "business AI",
    "business intelligence AI",
    "AI KPI analysis",
    "business decision intelligence",
    "AI business analysis",
    "business forecasting AI",
    "AI executive dashboard",
    "Runexa Business Agent",
  ],

  alternates: {
    canonical: "https://runexa.ai/en/business",
    languages: {
      en: `${siteUrl}/en/business`,
      fr: `${siteUrl}/fr/business`,
      ar: `${siteUrl}/ar/business`,
      "x-default": `${siteUrl}/business`,
    },
  },

  openGraph: {
    title: "Business Decision Intelligence | Runexa",

    description:
      "Upload business data and receive AI-powered executive analysis with KPIs, risks, opportunities, forecasts, and priority decisions.",

    url: "https://runexa.ai/en/business",

    siteName: "Runexa Systems",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Business Agent",
      },
    ],

    locale: "en_US",

    alternateLocale: ["fr_FR", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Business Decision Intelligence | Runexa",

    description:
      "AI-powered business intelligence for KPIs, risks, opportunities, forecasts, and executive decisions.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function BusinessPage() {
  return (
    <>
      <BusinessClient initialLocale="en" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "SoftwareApplication",

            name: "Runexa Business Agent",

            applicationCategory: "BusinessApplication",

            operatingSystem: "Web",

            description:
              "AI-powered business intelligence platform for KPI analysis, business risks, opportunities, forecasts, charts, and executive decision support.",

            url: "https://runexa.ai/en/business",

            inLanguage: "en",

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems",
              url: siteUrl,
            },

            knowsAbout: [
              "Business AI",
              "Business Intelligence AI",
              "KPI Analysis",
              "Business Forecasting AI",
              "Executive Dashboard",
              "Decision Support",
            ],
          }),
        }}
      />
    </>
  );
}
