import type { Metadata } from "next";
import CompanyClient from "../../../legal/company/CompanyClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Informations sur l’entreprise | Runexa",

  description:
    "Informations officielles sur Runexa Systems LLC, y compris l’adresse enregistrée, les coordonnées, les services et la loi applicable.",

  keywords: [
    "Runexa Systems LLC",
    "informations sur Runexa",
    "contacter Runexa",
    "adresse enregistrée Runexa",
    "entreprise d'intelligence artificielle",
    "IA pour entreprises",
    "informations légales Runexa",

    "à propos de Runexa",
    "Runexa Systems",
    "siège social Runexa",
    "adresse Runexa",
    "coordonnées Runexa",
    "informations de l'entreprise",
    "société d'intelligence artificielle",
    "entreprise technologique IA",
    "solutions IA pour entreprises",
    "agents IA",
    "plateforme d'intelligence artificielle",
    "éditeur de logiciels IA",
    "informations d'enregistrement",
    "société à responsabilité limitée",
    "Runexa AI",
    "Runexa Systems AI",
    "Dr. Rachid Ejjami",
    "fondateur de Runexa",
    "Runexa Legal Agent",
    "Runexa Finance Coach",
    "Runexa Study Agent",
    "Runexa Business Decision Agent",
    "informations juridiques de l'entreprise",
    "adresse légale de l'entreprise",
    "adresse Runexa aux États-Unis",
    "entreprise IA américaine",
    "Runexa Wyoming",
    "Runexa Sheridan Wyoming",
    "Runexa Contact",
    "Runexa Company Information",
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
