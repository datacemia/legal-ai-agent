import type { Metadata } from "next";
import CompanyClient from "../../../legal/company/CompanyClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Informations sur l’entreprise | Runexa",

  description:
    "Informations officielles sur Runexa Systems LLC, y compris l’adresse enregistrée, les coordonnées, les services et la loi applicable.",

  keywords: [
    "Runexa Systems LLC",
    "informations entreprise Runexa",
    "contact Runexa",
    "adresse enregistrée Runexa",
    "informations société IA",
    "entreprise IA",
    "informations légales Runexa",
  ],

  alternates: {
    canonical: "https://runexa.ai/fr/legal/company",
    languages: {
      en: `${siteUrl}/en/legal/company`,
      fr: `${siteUrl}/fr/legal/company`,
      ar: `${siteUrl}/ar/legal/company`,
      "x-default": `${siteUrl}/legal/company`,
    },
  },

  openGraph: {
    title: "Informations sur l’entreprise | Runexa",

    description:
      "Informations officielles sur Runexa Systems LLC, y compris l’adresse enregistrée, les coordonnées, les services et la loi applicable.",

    url: "https://runexa.ai/fr/legal/company",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Systems LLC",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Informations sur l’entreprise | Runexa",

    description:
      "Coordonnées officielles, adresse, loi applicable et contact de Runexa Systems LLC.",

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
      <CompanyClient initialLocale="fr" lockInitialLocale />

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
              "Runexa Systems LLC développe et exploite des outils alimentés par l’IA, des agents IA, des workflows entreprise et des services logiciels intelligents.",
          }),
        }}
      />
    </>
  );
}
