import type { Metadata } from "next";
import SecurityClient from "../../security/SecurityClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Sécurité et infrastructure | Runexa",

  description:
    "Découvrez les pratiques de sécurité de Runexa, le chiffrement, les protections d’infrastructure, les contrôles d’accès, la sécurité des paiements, les téléchargements responsables et la protection de la plateforme IA.",

  keywords: [
    "sécurité de l'intelligence artificielle",
    "sécurité IA pour entreprises",
    "infrastructure IA",
    "sécurité Runexa",
    "sécurité des plateformes IA",
    "chiffrement IA",
    "protection des données IA",
    "conformité IA pour entreprises",
    "documents téléversés de manière responsable",
    "workflows IA sécurisés",

    "sécurité de l'information",
    "sécurité des données",
    "protection des données",
    "cybersécurité",
    "sécurité cloud",
    "chiffrement des données",
    "chiffrement en transit",
    "chiffrement au repos",
    "gestion des accès",
    "contrôle d'accès",
    "authentification multifacteur",
    "gestion des identités",
    "sécurité applicative",
    "sécurité des plateformes cloud",
    "conformité en matière de sécurité",
    "gouvernance de la sécurité",
    "confidentialité des données",
    "protection des documents",
    "sécurité des fichiers téléversés",
    "gestion des risques de sécurité",
    "sécurité d'entreprise",
    "IA responsable et sécurité",
    "traitement sécurisé des documents",
    "infrastructure IA sécurisée",
    "protection des données d'entreprise",
    "Enterprise AI Security",
    "AI Data Security",
    "Runexa Security",
    "Runexa Data Protection",
    "Secure AI Workflows",
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
