import type { Metadata } from "next";
import AIDisclaimerClient from "../../../legal/ai-disclaimer/AIDisclaimerClient";

export const revalidate = 3600;

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "AI Disclaimer & Transparency | Runexa",

  description:
    "Review Runexa Systems AI disclaimer and transparency information regarding AI-generated outputs, limitations, human review requirements, non-professional advice, and responsible AI usage.",

  keywords: [
    "AI disclaimer",
    "AI transparency",
    "AI limitations",
    "AI compliance",
    "enterprise AI disclaimer",
    "AI governance",
    "AI risk disclosure",
    "Runexa AI policy",
    "responsible AI usage",
    "non-professional advice",
    "human review AI",
  ],

  alternates: {
    canonical: "https://runexa.ai/en/legal/ai-disclaimer",
    languages: {
      en: `${siteUrl}/en/legal/ai-disclaimer`,
      fr: `${siteUrl}/fr/legal/ai-disclaimer`,
      ar: `${siteUrl}/ar/legal/ai-disclaimer`,
      "x-default": `${siteUrl}/legal/ai-disclaimer`,
    },
  },

  openGraph: {
    title: "AI Disclaimer & Transparency | Runexa",

    description:
      "Review Runexa Systems AI disclaimer and transparency information regarding AI-generated outputs, limitations, human review requirements, non-professional advice, and responsible AI usage.",

    url: "https://runexa.ai/en/legal/ai-disclaimer",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa AI Disclaimer",
      },
    ],

    locale: "en_US",

    alternateLocale: ["fr_FR", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "AI Disclaimer & Transparency | Runexa",

    description:
      "Review Runexa Systems AI disclaimer and transparency information regarding AI-generated outputs, limitations, human review requirements, non-professional advice, and responsible AI usage.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function AIDisclaimerPage() {
  return (
    <>
      <AIDisclaimerClient initialLocale="en" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "Runexa AI Disclaimer & Transparency",

            description:
              "AI disclaimer and transparency information covering AI-generated outputs, limitations, human review requirements, non-professional advice, and responsible AI usage.",

            url: "https://runexa.ai/en/legal/ai-disclaimer",

            inLanguage: "en",

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: siteUrl,
            },
          }),
        }}
      />
    </>
  );
}
