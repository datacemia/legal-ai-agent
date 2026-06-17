import type { Metadata } from "next";
import HomeClient from "../HomeClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Runexa | Plateforme IA pour agents spécialisés",

  description:
    "Runexa est une plateforme IA avec des agents spécialisés pour l’analyse juridique, la finance, l’apprentissage et l’aide à la décision business.",

  keywords: [
    "plateforme IA",
    "agents IA",
    "IA juridique",
    "IA finance",
    "IA étude",
    "IA business",
    "IA entreprise",
    "automatisation IA",
    "business intelligence IA",
    "Runexa",
    "infrastructure IA",
  ],

  alternates: {
    canonical: `${siteUrl}/fr`,
    languages: {
      en: `${siteUrl}/en`,
      fr: `${siteUrl}/fr`,
      ar: `${siteUrl}/ar`,
      "x-default": siteUrl,
    },
  },

  openGraph: {
    title: "Runexa | Plateforme IA pour agents spécialisés",

    description:
      "Des agents IA spécialisés pour l’analyse juridique, la finance, l’apprentissage et les décisions business.",

    url: `${siteUrl}/fr`,

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa AI Workspace",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Runexa | Plateforme IA pour agents spécialisés",

    description:
      "Plateforme IA pour l’analyse juridique, la finance, l’apprentissage et les workflows business.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function Page() {
  return (
    <>
      <HomeClient initialLanguage="fr" lockInitialLanguage />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify([
            {
              "@context": "https://schema.org",

              "@type": "Organization",

              name: "Runexa Systems LLC",

              url: siteUrl,

              logo: `${siteUrl}/logo.png`,

              sameAs: [],

              description:
                "Plateforme IA avec des agents spécialisés pour l’analyse juridique, la finance, l’apprentissage et l’aide à la décision business.",

              knowsAbout: [
                "Intelligence artificielle",
                "IA juridique",
                "IA finance",
                "Business Intelligence",
                "IA étude",
                "Workflows IA entreprise",
              ],
            },

            {
              "@context": "https://schema.org",

              "@type": "WebSite",

              name: "Runexa",

              url: `${siteUrl}/fr`,

              inLanguage: "fr",

              publisher: {
                "@type": "Organization",
                name: "Runexa Systems LLC",
                url: siteUrl,
              },
            },
          ]),
        }}
      />
    </>
  );
}
