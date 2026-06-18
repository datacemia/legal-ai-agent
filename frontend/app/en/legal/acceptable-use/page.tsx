import type { Metadata } from "next";
import AcceptableUseClient from "../../../legal/acceptable-use/AcceptableUseClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Acceptable Use Policy | Runexa",

  description:
    "Runexa acceptable use policy governing the lawful and responsible use of AI systems, APIs, workflows, and enterprise services.",

  keywords: [
    "acceptable use policy",
    "AI policy",
    "AI compliance",
    "enterprise AI policy",
    "AI usage rules",
    "Runexa policy",
  ],

  alternates: {
    canonical: "https://runexa.ai/legal/acceptable-use",
    languages: {
      en: `${siteUrl}/en/legal/acceptable-use`,
      fr: `${siteUrl}/fr/legal/acceptable-use`,
      ar: `${siteUrl}/ar/legal/acceptable-use`,
      "x-default": `${siteUrl}/legal/acceptable-use`,
    },
  },

  openGraph: {
    title: "Acceptable Use Policy | Runexa",

    description:
      "Runexa acceptable use policy governing AI systems, APIs, enterprise workflows, and intelligent services.",

    url: "https://runexa.ai/legal/acceptable-use",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Acceptable Use Policy",
      },
    ],

    locale: "en_US",

    alternateLocale: ["fr_FR", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Acceptable Use Policy | Runexa",

    description:
      "Review the acceptable use requirements for Runexa AI services and enterprise systems.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function AcceptableUsePage() {
  return (
    <>
      <AcceptableUseClient initialLocale="en" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "Runexa Acceptable Use Policy",

            description:
              "Acceptable use policy for Runexa AI services, APIs, enterprise workflows, and intelligent systems.",

            url: "https://runexa.ai/legal/acceptable-use",

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
