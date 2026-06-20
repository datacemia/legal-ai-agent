import type { Metadata } from "next";
import CompanyClient from "./CompanyClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Company Information | Runexa",

  description:
    "Official company information, registered address, contact details, services, and governing law for Runexa Systems LLC.",

  keywords: [
  "Runexa Systems LLC",
  "Runexa company information",
  "Runexa contact",
  "Runexa registered address",
  "AI company information",
  "enterprise AI company",
  "Runexa legal information",

  "Runexa",
  "Runexa Systems",
  "Runexa AI",
  "Runexa company profile",
  "Runexa business information",
  "Runexa corporate information",
  "Runexa contact information",
  "Runexa headquarters",
  "Runexa address",
  "Runexa registered office",
  "Runexa Wyoming",
  "Runexa Sheridan Wyoming",
  "Sheridan Wyoming AI company",
  "US AI company",
  "American AI company",
  "AI technology company",
  "artificial intelligence company",
  "enterprise AI platform company",
  "AI software company",
  "AI solutions company",
  "enterprise software company",
  "AI startup",
  "specialized AI agents company",
  "AI agents platform",
  "enterprise AI solutions",
  "responsible AI company",
  "AI governance company",
  "business intelligence company",
  "legal AI company",
  "finance AI company",
  "education AI company",
  "Runexa Legal Agent",
  "Runexa Finance Coach",
  "Runexa Study Agent",
  "Runexa Business Decision Agent",
  "Dr. Rachid Ejjami",
  "founder of Runexa",
  "created by Dr. Rachid Ejjami",
  "AI innovation company",
  "AI infrastructure company",
  "enterprise AI provider",
  "Runexa legal entity",
  "Runexa corporate address",
],

  alternates: {
    canonical: "https://runexa.ai/legal/company",
    languages: {
      en: `${siteUrl}/en/legal/company`,
      fr: `${siteUrl}/fr/legal/company`,
      ar: `${siteUrl}/ar/legal/company`,
      "x-default": `${siteUrl}/legal/company`,
    },
  },

  openGraph: {
    title: "Company Information | Runexa",

    description:
      "Official company information, registered address, contact details, services, and governing law for Runexa Systems LLC.",

    url: "https://runexa.ai/legal/company",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Systems LLC",
      },
    ],

    locale: "en_US",

    alternateLocale: ["fr_FR", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Company Information | Runexa",

    description:
      "Official company details, address, governing law, and contact information for Runexa Systems LLC.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function CompanyPage() {
  return (
    <>
      <CompanyClient initialLocale="en" />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "Organization",

            name: "Runexa Systems LLC",

            url: siteUrl,

            email: "contact@runexa.ai",

            address: {
              "@type": "PostalAddress",
              streetAddress: "1309 Coffeen Avenue, Suite 1200",
              addressLocality: "Sheridan",
              addressRegion: "WY",
              postalCode: "82801",
              addressCountry: "US",
            },

            sameAs: [siteUrl],

            description:
              "Runexa Systems LLC develops and operates AI-powered tools, AI agents, enterprise workflows, and intelligent software services.",
          }),
        }}
      />
    </>
  );
}
