import type { Metadata } from "next";
import SecurityClient from "../../security/SecurityClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Sécurité et infrastructure | Runexa",

  description:
    "Découvrez les pratiques de sécurité de Runexa, le chiffrement, les protections d’infrastructure, les contrôles d’accès, la sécurité des paiements, les téléchargements responsables et la protection de la plateforme IA.",

  keywords: [
    "sécurité de l’IA",
    "sécurité de l’IA pour entreprises",
    "infrastructure IA",
    "sécurité Runexa",
    "sécurité de la plateforme IA",
    "chiffrement de l’IA",
    "protection des données IA",
    "conformité IA pour entreprises",
    "téléversements responsables",
    "flux de travail IA sécurisés",
  ],
  alternates: {
    canonical: "https://runexa.ai/fr/security",
    languages: {
      en: `${siteUrl}/en/security`,
      fr: `${siteUrl}/fr/security`,
      ar: `${siteUrl}/ar/security`,
      "x-default": `${siteUrl}/security`,
    },
  },

  openGraph: {
    title: "Sécurité et infrastructure | Runexa",

    description:
      "Découvrez les pratiques de sécurité de Runexa, le chiffrement, les protections d’infrastructure, les contrôles d’accès, la sécurité des paiements, les téléchargements responsables et la protection de la plateforme IA.",

    url: "https://runexa.ai/fr/security",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Security",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Sécurité et infrastructure | Runexa",

    description:
      "Découvrez les pratiques de sécurité de Runexa, le chiffrement, les protections d’infrastructure, les contrôles d’accès, la sécurité des paiements, les téléchargements responsables et la protection de la plateforme IA.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function SecurityPage() {
  return (
    <>
      <SecurityClient initialLocale="fr" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "Runexa Security",

            description:
              "Pratiques de sécurité, recommandations de téléchargement responsable et protections d’infrastructure pour les systèmes IA Runexa et les workflows IA entreprise.",

            url: "https://runexa.ai/fr/security",

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
