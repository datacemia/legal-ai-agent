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
