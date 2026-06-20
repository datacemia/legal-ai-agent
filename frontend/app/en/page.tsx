import type { Metadata } from "next";
import HomeClient from "../HomeClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Runexa | Enterprise AI Workspace & Specialized AI Agents",

  description:
    "Runexa is an AI workspace platform with specialized AI agents for legal analysis, finance intelligence, study workflows, and business decision support.",

  keywords: [
  "AI workspace",
  "AI agents",
  "legal AI",
  "finance AI",
  "study AI",
  "business AI",
  "enterprise AI",
  "AI workflow automation",
  "AI business intelligence",
  "Runexa",
  "AI infrastructure",

  "Runexa AI",
  "Runexa Systems",
  "specialized AI agents",
  "AI agents platform",
  "enterprise AI platform",
  "AI platform",
  "AI solutions",
  "AI-powered productivity",
  "AI automation",
  "business process automation",
  "AI knowledge management",
  "AI document processing",
  "AI document analysis",
  "AI decision support",
  "AI-powered decision making",
  "business analytics AI",
  "enterprise business intelligence",
  "digital transformation",
  "organizational AI",
  "intelligent agents",
  "AI assistants",
  "responsible AI",
  "AI governance",
  "enterprise AI compliance",
  "secure AI platform",
  "cloud AI infrastructure",
  "scalable AI systems",
  "enterprise AI workflows",
  "workflow intelligence",
  "AI operations platform",
  "AI transformation",
  "corporate AI platform",
  "AI for enterprises",
  "AI for professionals",
  "Legal AI",
  "Finance AI",
  "Study AI",
  "Business AI",
  "Runexa Legal Agent",
  "Runexa Finance Coach",
  "Runexa Study Agent",
  "Runexa Business Decision Agent",
  "Enterprise AI Platform",
  "AI Workspace Platform",
  "AI Productivity Platform",
],

  alternates: {
    canonical: `${siteUrl}/en`,
    languages: {
      en: `${siteUrl}/en`,
      fr: `${siteUrl}/fr`,
      ar: `${siteUrl}/ar`,
      "x-default": siteUrl,
    },
  },

  openGraph: {
    title: "Runexa AI Workspace",

    description:
      "Specialized AI agents for legal, finance, study, and business workflows.",

    url: `${siteUrl}/en`,

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa AI Workspace",
      },
    ],

    locale: "en_US",

    alternateLocale: ["fr_FR", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Runexa AI Workspace",

    description:
      "AI workspace platform for legal analysis, finance intelligence, study assistance, and business workflows.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function Page() {
  return (
    <>
      <HomeClient initialLanguage="en" lockInitialLanguage />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify([
            {
              "@context": "https://schema.org",

              "@type": "Organization",

              name: "Runexa Systems LLC",

              url: siteUrl,

              logo: `${siteUrl}/logo.png`,

              sameAs: [],

              description:
                "AI workspace platform with specialized AI agents for legal analysis, finance intelligence, study assistance, and business workflows.",

              knowsAbout: [
                "Artificial Intelligence",
                "Legal AI",
                "Finance AI",
                "Business Intelligence",
                "Study AI",
                "Enterprise AI Workflows",
              ],
            },

            {
              "@context": "https://schema.org",

              "@type": "WebSite",

              name: "Runexa",

              url: `${siteUrl}/en`,

              inLanguage: "en",

              publisher: {
                "@type": "Organization",
                name: "Runexa Systems LLC",
                url: siteUrl,
              },
            },
          ]),
        }}
      />
    </>
  );
}
