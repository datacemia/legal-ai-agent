import type { Metadata } from "next";
import AcceptableUseClient from "../../../legal/acceptable-use/AcceptableUseClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Politique d’utilisation acceptable | Runexa",

  description:
    "Politique d’utilisation acceptable de Runexa régissant l’utilisation légale, responsable et autorisée des systèmes IA, API, téléchargements, workflows et services entreprise.",

  keywords: [
    "politique d'utilisation acceptable",
    "politique IA",
    "conformité IA",
    "politique IA pour entreprises",
    "règles d'utilisation de l'IA",
    "politique Runexa",
    "fichiers autorisés",
    "utilisation responsable de l'IA",
    "règles de la plateforme IA",

    "conditions d'utilisation de l'IA",
    "politique d'utilisation Runexa",
    "directives d'utilisation de l'IA",
    "gouvernance de l'IA",
    "conformité réglementaire IA",
    "sécurité de l'IA",
    "confidentialité de l'IA",
    "contenu interdit",
    "utilisation autorisée",
    "documents autorisés",
    "téléversement de documents",
    "analyse documentaire par IA",
    "politique de contenu",
    "utilisation commerciale de l'IA",
    "utilisation professionnelle de l'IA",
    "plateforme IA pour entreprises",
    "agents IA",
    "intelligence artificielle responsable",
    "gestion des risques IA",
    "conformité juridique IA",
    "politiques IA pour entreprises",
    "conditions d'utilisation Runexa",
    "Runexa Acceptable Use Policy",
    "Runexa AI Policy",
    "Enterprise AI Compliance",
  ],

  alternates: {
    canonical: "https://runexa.ai/fr/legal/acceptable-use",
    languages: {
      en: `${siteUrl}/en/legal/acceptable-use`,
      fr: `${siteUrl}/fr/legal/acceptable-use`,
      ar: `${siteUrl}/ar/legal/acceptable-use`,
      "x-default": `${siteUrl}/legal/acceptable-use`,
    },
  },

  openGraph: {
    title: "Politique d’utilisation acceptable | Runexa",

    description:
      "Politique d’utilisation acceptable de Runexa régissant l’utilisation légale, responsable et autorisée des systèmes IA, API, téléchargements, workflows et services entreprise.",

    url: "https://runexa.ai/fr/legal/acceptable-use",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Acceptable Use Policy",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Politique d’utilisation acceptable | Runexa",

    description:
      "Politique d’utilisation acceptable de Runexa régissant l’utilisation légale, responsable et autorisée des systèmes IA, API, téléchargements, workflows et services entreprise.",

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
      <AcceptableUseClient initialLocale="fr" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "Runexa Acceptable Use Policy",

            description:
              "Politique d’utilisation acceptable pour l’utilisation légale, responsable et autorisée des services IA Runexa, API, téléchargements, workflows entreprise et systèmes intelligents.",

            url: "https://runexa.ai/fr/legal/acceptable-use",

            inLanguage: "fr",

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
