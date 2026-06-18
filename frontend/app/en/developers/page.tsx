import type { Metadata } from "next";
import DevelopersClient from "../../developers/DevelopersClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Developers & AI APIs | Runexa",

  description:
    "Build AI-powered workflows with Runexa APIs for legal analysis, finance intelligence, study automation, and business decision support.",

  keywords: [
    "Runexa developers",
    "AI API",
    "legal AI API",
    "finance AI API",
    "study AI API",
    "business AI API",
    "AI workflow API",
    "developer AI tools",
    "enterprise AI API",
  ],

  alternates: {
    canonical: "https://runexa.ai/en/developers",
    languages: {
      en: `${siteUrl}/en/developers`,
      fr: `${siteUrl}/fr/developers`,
      ar: `${siteUrl}/ar/developers`,
      "x-default": `${siteUrl}/developers`,
    },
  },

  openGraph: {
    title: "Developers & AI APIs | Runexa",

    description:
      "Build AI-powered workflows with Runexa APIs for legal analysis, finance intelligence, study automation, and business decision support.",

    url: "https://runexa.ai/en/developers",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Developers",
      },
    ],

    locale: "en_US",

    alternateLocale: ["fr_FR", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Developers & AI APIs | Runexa",

    description:
      "Build AI-powered workflows with Runexa APIs for legal analysis, finance intelligence, study automation, and business decision support.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function DevelopersPage() {
  return (
    <>
      <DevelopersClient initialLocale="en" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "TechArticle",

            headline: "Developers & AI APIs | Runexa",

            name: "Runexa Developers",

            description:
              "Developer platform for building AI-powered workflows with Runexa APIs for legal analysis, finance intelligence, study automation, and business decision support.",

            url: "https://runexa.ai/en/developers",

            inLanguage: "en",

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: siteUrl,
            },

            about: [
              "AI APIs",
              "Developer APIs",
              "Legal AI API",
              "Finance AI API",
              "Study AI API",
              "Business AI API",
              "AI Workflow Automation",
            ],
          }),
        }}
      />
    </>
  );
}
