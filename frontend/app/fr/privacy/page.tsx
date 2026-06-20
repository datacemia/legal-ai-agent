import type { Metadata } from "next";
import PrivacyClient from "../../privacy/PrivacyClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Politique de confidentialité | Runexa",

  description:
    "Politique de confidentialité expliquant comment Runexa Systems LLC collecte, utilise, stocke, protège, traite, transfère et sécurise les informations personnelles, les contenus téléchargés et la confidentialité des mineurs pour les utilisateurs internationaux.",

  keywords: [
    "politique de confidentialité",
    "confidentialité IA",
    "confidentialité Runexa",
    "traitement des données IA",
    "confidentialité IA pour entreprises",
    "confidentialité plateforme IA",
    "confidentialité des fichiers téléversés IA",
    "conformité IA",
    "entraînement des modèles IA",
    "transferts internationaux de données",
    "traitement automatisé",
    "RGPD",
    "RGPD Royaume-Uni",
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
