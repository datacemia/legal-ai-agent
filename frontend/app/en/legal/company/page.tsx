import type { Metadata } from "next";
import CompanyClient from "../../../legal/company/CompanyClient";

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
  ],

  alternates: {
    canonical: "https://runexa.ai/en/legal/company",
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

    url: "https://runexa.ai/en/legal/company",

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
      <CompanyClient initialLocale="en" lockInitialLocale />

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
