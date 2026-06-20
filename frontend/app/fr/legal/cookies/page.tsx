import type { Metadata } from "next";
import CookiePolicyClient from "../../../legal/cookies/CookiePolicyClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Politique relative aux cookies | Runexa",

  description:
    "Politique relative aux cookies expliquant comment Runexa Systems LLC utilise les cookies, l’analytics, l’authentification, les technologies de sécurité et les services associés sur ses plateformes IA.",

  keywords: [
    "politique relative aux cookies",
    "cookies Runexa",
    "cookies plateforme IA",
    "cookies du site web",
    "cookies d'analyse",
    "cookies de confidentialité",
    "cookies de sécurité",
    "conformité IA pour entreprises",

    "cookies",
    "paramètres des cookies",
    "gestion des cookies",
    "cookies essentiels",
    "cookies fonctionnels",
    "cookies statistiques",
    "cookies marketing",
    "cookies de performance",
    "cookies de session",
    "suivi de l'utilisation du site",
    "analyse du trafic web",
    "protection de la vie privée",
    "confidentialité des utilisateurs",
    "sécurité des données",
    "gestion du consentement aux cookies",
    "conformité à la vie privée",
    "conformité RGPD",
    "conformité UK GDPR",
    "politique de confidentialité",
    "sécurité de la plateforme IA",
    "plateforme IA pour entreprises",
    "Runexa Cookie Policy",
    "Runexa Privacy",
    "Runexa Security",
    "gestion des préférences de cookies",
    "transparence des données",
    "politique de suivi",
    "cookies tiers",
    "cookies analytiques",
    "politique de données Runexa",
  ],

  alternates: {
    canonical: "https://runexa.ai/fr/legal/cookies",
    languages: {
      en: `${siteUrl}/en/legal/cookies`,
      fr: `${siteUrl}/fr/legal/cookies`,
      ar: `${siteUrl}/ar/legal/cookies`,
      "x-default": `${siteUrl}/legal/cookies`,
    },
  },

  openGraph: {
    title: "Politique relative aux cookies | Runexa",

    description:
      "Découvrez comment Runexa Systems LLC utilise les cookies, l’analytics, l’authentification et les technologies de sécurité sur ses plateformes IA.",

    url: "https://runexa.ai/fr/legal/cookies",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Cookie Policy",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Politique relative aux cookies | Runexa",

    description:
      "Consultez l’usage des cookies, technologies analytics, systèmes d’authentification et services de sécurité utilisés par Runexa.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function CookiePolicyPage() {
  return (
    <>
      <CookiePolicyClient initialLocale="fr" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "Politique relative aux cookies Runexa",

            description:
              "Informations sur l’usage des cookies, technologies analytics, systèmes d’authentification et suivi navigateur pour les services IA et plateformes entreprise Runexa.",

            url: "https://runexa.ai/fr/legal/cookies",

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
