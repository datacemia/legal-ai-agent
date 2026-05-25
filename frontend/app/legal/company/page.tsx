import type { Metadata } from "next";
import CompanyClient from "./CompanyClient";

export const metadata: Metadata = {
  title: "Company Information | Runexa Systems LLC",
  description:
    "Company information, registered address, contact details, services, and governing law for Runexa Systems LLC.",
  keywords: [
    "Runexa Systems LLC",
    "Runexa company information",
    "Runexa contact",
    "Runexa registered address",
    "AI company information",
  ],
  alternates: {
    canonical: "https://runexa.ai/company-information",
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
          }),
        }}
      />
    </>
  );
}
