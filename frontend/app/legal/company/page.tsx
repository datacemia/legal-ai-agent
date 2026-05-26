import type { Metadata } from "next";
import CompanyClient from "./CompanyClient";

export const metadata: Metadata = {
  title: "Company Information | Runexa Systems LLC",

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
    canonical: "https://runexa.ai/legal/company",
  },

  openGraph: {
    title: "Company Information | Runexa Systems LLC",

    description:
      "Official company information, registered address, contact details, services, and governing law for Runexa Systems LLC.",

    url: "https://runexa.ai/legal/company",

    siteName: "Runexa Systems",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Systems LLC",
      },
    ],

    locale: "en_US",

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Company Information | Runexa Systems LLC",

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
      <CompanyClient />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "Organization",

            name: "Runexa Systems LLC",

            url: "https://runexa.ai",

            email: "contact@runexa.ai",

            address: {
              "@type": "PostalAddress",
              streetAddress: "1309 Coffeen Avenue, Suite 1200",
              addressLocality: "Sheridan",
              addressRegion: "WY",
              postalCode: "82801",
              addressCountry: "US",
            },

            sameAs: ["https://runexa.ai"],

            description:
              "Runexa Systems LLC develops and operates AI-powered tools, AI agents, enterprise workflows, and intelligent software services.",
          }),
        }}
      />
    </>
  );
}
