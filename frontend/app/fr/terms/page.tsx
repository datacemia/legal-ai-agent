import type { Metadata } from "next";
import TermsClient from "../../terms/TermsClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Conditions d’utilisation | Runexa",

  description:
    "Conditions d’utilisation régissant les agents IA Runexa, API, téléchargements, crédits, abonnements, utilisation par les mineurs, facturation et services alimentés par l’IA.",

  keywords: [
    "conditions d'utilisation",
    "conditions de la plateforme IA",
    "conditions Runexa",
    "conditions SaaS IA",
    "conditions d'utilisation API IA",
    "conditions IA pour entreprises",
    "abonnements IA",
    "crédits IA",
    "utilisation par les mineurs",
    "documents téléversés",
    "conditions de facturation",

    "conditions de service",
    "accord utilisateur",
    "accord d'utilisation de la plateforme",
    "conditions générales Runexa",
    "conditions de la plateforme Runexa",
    "conditions d'abonnement",
    "conditions de paiement",
    "facturation et abonnements",
    "gestion du compte",
    "annulation d'abonnement",
    "utilisation des API",
    "conditions développeurs",
    "conditions pour entreprises",
    "licence logicielle",
    "droits de propriété intellectuelle",
    "contenu téléversé",
    "documents téléversés",
    "utilisation responsable de l'IA",
    "politiques de la plateforme",
    "conditions d'utilisation des agents IA",
    "Runexa Legal Agent Terms",
    "Runexa Finance Coach Terms",
    "Runexa Study Agent Terms",
    "Runexa Business Decision Agent Terms",
    "limitations et responsabilités",
    "limitation de responsabilité",
    "conditions des services numériques",
    "plateforme IA pour entreprises",
    "Runexa Terms of Service",
    "Enterprise AI Terms",
  ],

  alternates: {
    canonical: "https://runexa.ai/fr/terms",
    languages: {
      en: `${siteUrl}/en/terms`,
      fr: `${siteUrl}/fr/terms`,
      ar: `${siteUrl}/ar/terms`,
      "x-default": `${siteUrl}/terms`,
    },
  },

  openGraph: {
    title: "Conditions d’utilisation | Runexa",

    description:
      "Conditions d’utilisation régissant les agents IA Runexa, API, téléchargements, crédits, abonnements, utilisation par les mineurs, facturation et services alimentés par l’IA.",

    url: "https://runexa.ai/fr/terms",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Terms of Service",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Conditions d’utilisation | Runexa",

    description:
      "Conditions d’utilisation régissant les agents IA Runexa, API, téléchargements, crédits, abonnements, utilisation par les mineurs, facturation et services alimentés par l’IA.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function TermsPage() {
  return (
    <>
      <TermsClient initialLocale="fr" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "Runexa Terms of Service",

            description:
              "Conditions régissant les agents IA Runexa, API, téléchargements, workflows entreprise, crédits, abonnements, utilisation par les mineurs, facturation et services alimentés par l’IA.",

            url: "https://runexa.ai/fr/terms",

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
