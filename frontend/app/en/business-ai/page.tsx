import type { Metadata } from "next";
import BusinessAIClient from "../../business-ai/BusinessAIClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "AI Business Intelligence & Decision Support | Runexa",

  description:
    "Analyze business data, detect risks, discover opportunities, and improve strategic decisions with Runexa Business AI.",

 keywords: [
  "business AI",
  "AI business intelligence",
  "business decision support",
  "AI KPI analysis",
  "business risk analysis",
  "AI forecasting",
  "Runexa business AI",
  "AI business workflows",

  "Runexa Business Decision Agent",
  "enterprise business intelligence",
  "business analytics AI",
  "AI-powered decision making",
  "business performance analysis",
  "AI business insights",
  "executive decision support",
  "AI executive summaries",
  "AI executive dashboard",
  "KPI monitoring AI",
  "AI performance dashboards",
  "business data analysis",
  "AI operational intelligence",
  "AI strategy analysis",
  "AI market analysis",
  "AI trend analysis",
  "predictive analytics AI",
  "business forecasting",
  "AI risk assessment",
  "enterprise analytics platform",
  "business process optimization",
  "AI workflow automation",
  "AI workflow optimization",
  "data-driven decision making",
  "AI recommendations",
  "business operations AI",
  "corporate intelligence AI",
  "AI for executives",
  "AI for managers",
  "AI productivity analytics",
  "business growth intelligence",
  "strategic planning AI",
  "AI business reporting",
  "management intelligence platform",
  "business intelligence software",
  "enterprise AI insights",
  "Business Intelligence Platform",
  "Enterprise Business Intelligence",
  "Business Decision Intelligence",
],
  alternates: {
    canonical: "https://runexa.ai/en/business-ai",
    languages: {
      en: `${siteUrl}/en/business-ai`,
      fr: `${siteUrl}/fr/business-ai`,
      ar: `${siteUrl}/ar/business-ai`,
      "x-default": `${siteUrl}/business-ai`,
    },
  },

  openGraph: {
    title: "AI Business Intelligence & Decision Support | Runexa",

    description:
      "Analyze business data, detect risks, discover opportunities, and improve strategic decisions with Runexa Business AI.",

    url: "https://runexa.ai/en/business-ai",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Business AI",
      },
    ],

    locale: "en_US",

    alternateLocale: ["fr_FR", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "AI Business Intelligence & Decision Support | Runexa",

    description:
      "AI-powered business intelligence for KPI analysis, strategic insights, forecasting, and operational decision support.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function BusinessAIPage() {
  return (
    <>
      <BusinessAIClient initialLocale="en" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify([
            {
              "@context": "https://schema.org",

              "@type": "SoftwareApplication",

              name: "Runexa Business AI",

              applicationCategory: "BusinessApplication",

              operatingSystem: "Web",

              url: "https://runexa.ai/en/business-ai",

              inLanguage: "en",

              description:
                "AI business intelligence and decision support software for KPI analysis, risk detection, opportunity discovery, forecasting, and operational insights.",

              publisher: {
                "@type": "Organization",
                name: "Runexa Systems LLC",
                url: siteUrl,
              },

              knowsAbout: [
                "Business AI",
                "AI Business Intelligence",
                "Decision Support",
                "KPI Analysis",
                "Business Risk Analysis",
                "AI Forecasting",
              ],
            },
          ]),
        }}
      />
    </>
  );
}
