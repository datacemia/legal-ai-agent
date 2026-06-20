import type { Metadata } from "next";
import EnterpriseAIClient from "./EnterpriseAIClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Enterprise AI Workspace & Custom AI Systems | Runexa",

  description:
    "Secure enterprise AI workflows for legal analysis, financial reporting, business intelligence, learning operations, and organizational decision support.",

  keywords: [
  "enterprise AI",
  "custom AI systems",
  "AI workspace",
  "enterprise AI workflows",
  "business intelligence AI",
  "organizational AI",
  "Runexa enterprise AI",
  "AI decision support",

  "Runexa AI",
  "Runexa enterprise platform",
  "enterprise AI platform",
  "enterprise AI solutions",
  "AI platform for enterprises",
  "specialized AI agents",
  "custom AI agents",
  "AI automation",
  "workflow automation AI",
  "business process automation",
  "AI-powered productivity",
  "AI-powered decision making",
  "enterprise business intelligence",
  "business analytics AI",
  "organizational intelligence",
  "AI knowledge management",
  "AI document processing",
  "AI document analysis",
  "enterprise workflow automation",
  "digital transformation",
  "AI transformation",
  "corporate AI platform",
  "AI operations platform",
  "enterprise AI infrastructure",
  "cloud AI infrastructure",
  "scalable AI systems",
  "secure AI platform",
  "enterprise AI compliance",
  "responsible AI",
  "AI governance",
  "AI strategy platform",
  "enterprise automation platform",
  "data-driven decision making",
  "AI assistants for enterprises",
  "AI agents platform",
  "business decision intelligence",
  "workflow intelligence",
  "enterprise productivity AI",
  "organizational automation",
  "Enterprise AI Platform",
],

  alternates: {
    canonical: "https://runexa.ai/enterprise-ai",
    languages: {
      en: `${siteUrl}/en/enterprise-ai`,
      fr: `${siteUrl}/fr/enterprise-ai`,
      ar: `${siteUrl}/ar/enterprise-ai`,
      "x-default": `${siteUrl}/enterprise-ai`,
    },
  },

  openGraph: {
    title: "Enterprise AI Workspace & Custom AI Systems | Runexa",

    description:
      "Secure enterprise AI workflows for legal analysis, financial reporting, business intelligence, learning operations, and organizational decision support.",

    url: "https://runexa.ai/enterprise-ai",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Enterprise AI",
      },
    ],

    locale: "en_US",

    alternateLocale: ["fr_FR", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Enterprise AI Workspace & Custom AI Systems | Runexa",

    description:
      "Enterprise AI workflows for document analysis, finance intelligence, learning operations, and business decision support.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function EnterpriseAIPage() {
  return (
    <>
      <EnterpriseAIClient initialLocale="en" />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify([
            {
              "@context": "https://schema.org",

              "@type": "SoftwareApplication",

              name: "Runexa Enterprise AI",

              applicationCategory: "BusinessApplication",

              operatingSystem: "Web",

              url: "https://runexa.ai/enterprise-ai",

              inLanguage: "en",

              description:
                "Enterprise AI workspace for document analysis, financial reporting, learning workflows, business intelligence, and decision support.",

              publisher: {
                "@type": "Organization",
                name: "Runexa Systems LLC",
                url: siteUrl,
              },

              knowsAbout: [
                "Enterprise AI",
                "Custom AI Systems",
                "AI Workspace",
                "Enterprise AI Workflows",
                "Business Intelligence AI",
                "AI Decision Support",
              ],
            },
          ]),
        }}
      />
    </>
  );
}
