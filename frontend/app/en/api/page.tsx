import type { Metadata } from "next";
import ApiClient from "../../api/ApiClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "AI APIs & Agent Infrastructure | Runexa",

  description:
    "Integrate Runexa AI APIs for legal analysis, finance intelligence, study automation, and business decision support workflows.",

  keywords: [
    "Runexa API",
    "AI APIs",
    "legal AI API",
    "finance AI API",
    "study AI API",
    "business AI API",
    "async AI processing",
    "AI infrastructure",
  ],

  alternates: {
    canonical: "https://runexa.ai/en/api",
    languages: {
      en: `${siteUrl}/en/api`,
      fr: `${siteUrl}/fr/api`,
      ar: `${siteUrl}/ar/api`,
      "x-default": `${siteUrl}/api`,
    },
  },

  openGraph: {
    title: "AI APIs & Agent Infrastructure | Runexa",

    description:
      "Integrate Runexa AI APIs for legal analysis, finance intelligence, study automation, and business decision support workflows.",

    url: "https://runexa.ai/en/api",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa API Platform",
      },
    ],

    locale: "en_US",

    alternateLocale: ["fr_FR", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "AI APIs & Agent Infrastructure | Runexa",

    description:
      "AI APIs for legal, finance, study, and business automation workflows.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function ApiPage() {
  return (
    <>
      <ApiClient initialLocale="en" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "SoftwareApplication",

            name: "Runexa API Platform",

            applicationCategory: "DeveloperApplication",

            operatingSystem: "Web",

            description:
              "Runexa AI API platform for legal analysis, finance intelligence, study automation, business decision support, asynchronous processing, and agent infrastructure.",

            url: "https://runexa.ai/en/api",

            inLanguage: "en",

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: siteUrl,
            },

            knowsAbout: [
              "AI APIs",
              "Legal AI API",
              "Finance AI API",
              "Study AI API",
              "Business AI API",
              "Async AI Processing",
              "AI Infrastructure",
            ],
          }),
        }}
      />
    </>
  );
}
