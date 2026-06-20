import type { Metadata } from "next";
import AboutClient from "../../about/AboutClient";

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
  ],

  alternates: {
    canonical: "https://runexa.ai/en/about",
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

    url: "https://runexa.ai/en/about",

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
      <AboutClient initialLocale="en" lockInitialLocale />

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

              url: "https://runexa.ai/en/about",

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
