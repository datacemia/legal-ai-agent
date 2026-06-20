import type { Metadata } from "next";
import PrivacyClient from "../../privacy/PrivacyClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Politique de confidentialité | Runexa",

  description:
    "Politique de confidentialité expliquant comment Runexa Systems LLC collecte, utilise, stocke, protège, traite, transfère et sécurise les informations personnelles, les contenus téléchargés et la confidentialité des mineurs pour les utilisateurs internationaux.",

  keywords: [
    "politique de confidentialité",
    "confidentialité de l'intelligence artificielle",
    "confidentialité Runexa",
    "traitement des données par IA",
    "confidentialité IA pour entreprises",
    "confidentialité de la plateforme IA",
    "confidentialité des fichiers téléversés",
    "conformité IA",
    "entraînement des modèles d'IA",
    "transferts internationaux de données",
    "traitement automatisé",
    "RGPD",
    "UK GDPR",

    "protection des données personnelles",
    "confidentialité des utilisateurs",
    "sécurité des données",
    "sécurité de l'information",
    "collecte de données",
    "utilisation des données",
    "conservation des données",
    "droits à la vie privée",
    "droits des personnes concernées",
    "conformité à la confidentialité",
    "conformité RGPD",
    "conformité UK GDPR",
    "réglementation sur la protection des données",
    "traitement légal des données",
    "transfert transfrontalier de données",
    "traitement documentaire par IA",
    "documents téléversés",
    "confidentialité des documents",
    "données d'entreprise",
    "confidentialité des entreprises",
    "IA responsable",
    "gouvernance de l'IA",
    "transparence de l'IA",
    "sécurité des plateformes IA",
    "conformité réglementaire",
    "privacy by design",
    "Runexa Privacy Policy",
    "Runexa Data Protection",
    "Enterprise AI Privacy",
    "AI Data Protection",
  ],
  alternates: {
    canonical: "https://runexa.ai/fr/privacy",
    languages: {
      en: `${siteUrl}/en/privacy`,
      fr: `${siteUrl}/fr/privacy`,
      ar: `${siteUrl}/ar/privacy`,
      "x-default": `${siteUrl}/privacy`,
    },
  },

  openGraph: {
    title: "Politique de confidentialité | Runexa",

    description:
      "Politique de confidentialité expliquant comment Runexa Systems LLC collecte, utilise, stocke, protège, traite, transfère et sécurise les informations personnelles, les contenus téléchargés et la confidentialité des mineurs pour les utilisateurs internationaux.",

    url: "https://runexa.ai/fr/privacy",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Privacy Policy",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Politique de confidentialité | Runexa",

    description:
      "Politique de confidentialité expliquant comment Runexa Systems LLC collecte, utilise, stocke, protège, traite, transfère et sécurise les informations personnelles, les contenus téléchargés et la confidentialité des mineurs pour les utilisateurs internationaux.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function PrivacyPage() {
  return (
    <>
      <PrivacyClient initialLocale="fr" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "PrivacyPolicy",

            name: "Runexa Privacy Policy",

            description:
              "Politique de confidentialité expliquant comment Runexa Systems LLC collecte, utilise, stocke, protège, traite, transfère et sécurise les informations personnelles, les contenus téléchargés et la confidentialité des mineurs pour les utilisateurs internationaux.",

            url: "https://runexa.ai/fr/privacy",

            inLanguage: "fr",

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: siteUrl,
            },

            jurisdiction: [
              "United States",
              "European Union",
              "United Kingdom",
              "International",
            ],
          }),
        }}
      />
    </>
  );
}
