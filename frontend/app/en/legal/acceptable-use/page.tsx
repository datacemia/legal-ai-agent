import type { Metadata } from "next";
import AcceptableUseClient from "../../../legal/acceptable-use/AcceptableUseClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Acceptable Use Policy | Runexa",

  description:
    "Runexa acceptable use policy governing lawful, responsible, and authorized use of AI systems, APIs, uploads, workflows, and enterprise services.",

  keywords: [
  "acceptable use policy",
  "AI policy",
  "AI compliance",
  "enterprise AI policy",
  "AI usage rules",
  "Runexa policy",
  "authorized uploads",
  "responsible AI use",
  "AI platform rules",

  "Runexa acceptable use policy",
  "AI governance",
  "responsible AI",
  "AI safety policy",
  "enterprise AI governance",
  "AI risk management",
  "AI platform compliance",
  "AI usage guidelines",
  "AI platform terms",
  "AI content policy",
  "AI user responsibilities",
  "permitted use policy",
  "prohibited activities",
  "authorized content uploads",
  "document upload policy",
  "acceptable AI workflows",
  "enterprise compliance",
  "regulatory compliance",
  "ethical AI use",
  "AI security policy",
  "AI transparency",
  "AI accountability",
  "AI misuse prevention",
  "AI abuse prevention",
  "platform integrity",
  "user conduct policy",
  "AI service rules",
  "AI platform standards",
  "business AI compliance",
  "enterprise AI standards",
  "AI operational policy",
  "responsible technology use",
  "AI system governance",
  "data upload rules",
  "AI compliance framework",
  "organizational AI policy",
  "secure AI usage",
  "Runexa compliance",
  "AI platform governance",
  "enterprise AI controls",
],

  alternates: {
    canonical: "https://runexa.ai/en/legal/acceptable-use",
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
      "Runexa acceptable use policy governing lawful, responsible, and authorized use of AI systems, APIs, uploads, workflows, and enterprise services.",

    url: "https://runexa.ai/en/legal/acceptable-use",

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
      "Runexa acceptable use policy governing lawful, responsible, and authorized use of AI systems, APIs, uploads, workflows, and enterprise services.",

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
              "Acceptable use policy for lawful, responsible, and authorized use of Runexa AI services, APIs, uploads, enterprise workflows, and intelligent systems.",

            url: "https://runexa.ai/en/legal/acceptable-use",

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
