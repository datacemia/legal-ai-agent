import type { Metadata } from "next";
import AboutClient from "./AboutClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "About Runexa | Founder Story & Specialized AI Agents",

  description:
    "Learn why Dr. Rachid Ejjami created Runexa Systems LLC and how real-world challenges inspired the Study Agent, Legal Agent, Finance Coach, and Business Decision Agent.",

  keywords: [
  "Runexa",
  "Runexa Systems LLC",
  "Dr. Rachid Ejjami",
  "AI agents",
  "specialized AI agents",
  "AI workspace",
  "legal AI agent",
  "finance coach AI",
  "study AI agent",
  "business decision AI",
  "responsible AI",
  "enterprise AI",

  "Runexa AI",
  "Runexa platform",
  "Runexa enterprise AI",
  "Runexa Systems",
  "AI platform",
  "enterprise AI platform",
  "AI workspace platform",
  "specialized AI agents platform",
  "AI solutions",
  "custom AI agents",
  "intelligent AI agents",
  "AI assistants",
  "AI automation",
  "AI workflow automation",
  "business process automation",
  "AI-powered productivity",
  "AI-powered decision making",
  "AI decision support",
  "organizational AI",
  "enterprise automation",
  "business intelligence AI",
  "AI business intelligence",
  "AI infrastructure",
  "enterprise AI infrastructure",
  "cloud AI platform",
  "scalable AI systems",
  "secure AI platform",
  "responsible AI platform",
  "AI governance",
  "AI compliance",
  "enterprise AI compliance",
  "AI knowledge management",
  "AI document analysis",
  "AI document processing",
  "AI workflow platform",
  "digital transformation AI",
  "AI transformation",
  "Legal AI",
  "Finance AI",
  "Study AI",
  "Business AI",
  "Runexa Legal Agent",
  "Runexa Finance Coach",
  "Runexa Study Agent",
  "Runexa Business Decision Agent",
  "AI for enterprises",
  "AI for professionals",
  "artificial intelligence platform",
],

  alternates: {
    canonical: "https://runexa.ai/about",
    languages: {
      en: `${siteUrl}/en/about`,
      fr: `${siteUrl}/fr/about`,
      ar: `${siteUrl}/ar/about`,
      "x-default": `${siteUrl}/about`,
    },
  },

  openGraph: {
    title: "About Runexa | Founder Story & Specialized AI Agents",

    description:
      "Learn why Dr. Rachid Ejjami created Runexa Systems LLC and how real-world challenges inspired the Study Agent, Legal Agent, Finance Coach, and Business Decision Agent.",

    url: "https://runexa.ai/about",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "About Runexa Systems",
      },
    ],

    locale: "en_US",

    alternateLocale: ["fr_FR", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "About Runexa | Founder Story & Specialized AI Agents",

    description:
      "Learn why Dr. Rachid Ejjami created Runexa Systems LLC and how real-world challenges inspired the Study Agent, Legal Agent, Finance Coach, and Business Decision Agent.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function AboutPage() {
  return (
    <>
      <AboutClient initialLocale="en" />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify([
            {
              "@context": "https://schema.org",

              "@type": "AboutPage",

              name: "About Runexa | Founder Story & Specialized AI Agents",

              description:
                "Learn why Dr. Rachid Ejjami created Runexa Systems LLC and how real-world challenges inspired the Study Agent, Legal Agent, Finance Coach, and Business Decision Agent.",

              url: "https://runexa.ai/about",

              inLanguage: "en",

              publisher: {
                "@type": "Organization",
                name: "Runexa Systems LLC",
                url: siteUrl,
              },
            },
            {
              "@context": "https://schema.org",

              "@type": "Organization",

              name: "Runexa Systems LLC",

              url: siteUrl,

              founder: {
                "@type": "Person",
                name: "Dr. Rachid Ejjami",
                jobTitle: "Founder and Managing Member",
              },

              address: {
                "@type": "PostalAddress",
                streetAddress: "1309 Coffeen Avenue, Suite 1200",
                addressLocality: "Sheridan",
                addressRegion: "WY",
                postalCode: "82801",
                addressCountry: "US",
              },

              description:
                "Runexa Systems LLC builds specialized AI agents for legal document analysis, learning support, personal finance coaching, business decision support, and responsible AI workflows.",

              knowsAbout: [
                "Artificial Intelligence",
                "Legal AI",
                "Study AI",
                "Finance Coach AI",
                "Business Intelligence",
                "Responsible AI",
                "Enterprise AI Workflows"
              ],
            },
          ]),
        }}
      />
    </>
  );
}
