import type { Metadata } from "next";
import EnterpriseAIClient from "../../enterprise-ai/EnterpriseAIClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Espace IA entreprise et systèmes IA personnalisés | Runexa",

  description:
    "Workflows IA sécurisés pour l’analyse juridique, le reporting financier, la business intelligence, les opérations d’apprentissage et l’aide à la décision organisationnelle.",

  keywords: [
    "IA entreprise",
    "systèmes IA personnalisés",
    "espace IA",
    "workflows IA entreprise",
    "business intelligence IA",
    "IA organisationnelle",
    "Runexa enterprise AI",
    "aide à la décision IA",
  ],

  alternates: {
    canonical: "https://runexa.ai/fr/enterprise-ai",
    languages: {
      en: `${siteUrl}/en/enterprise-ai`,
      fr: `${siteUrl}/fr/enterprise-ai`,
      ar: `${siteUrl}/ar/enterprise-ai`,
      "x-default": `${siteUrl}/enterprise-ai`,
    },
  },

  openGraph: {
    title: "Espace IA entreprise et systèmes IA personnalisés | Runexa",

    description:
      "Workflows IA sécurisés pour l’analyse juridique, le reporting financier, la business intelligence, les opérations d’apprentissage et l’aide à la décision organisationnelle.",

    url: "https://runexa.ai/fr/enterprise-ai",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Enterprise AI",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Espace IA entreprise et systèmes IA personnalisés | Runexa",

    description:
      "Workflows IA entreprise pour l’analyse documentaire, l’intelligence financière, l’apprentissage et l’aide à la décision business.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function EnterpriseAIPage() {
  return (
    <>
      <EnterpriseAIClient initialLocale="fr" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify([
            {
              "@context": "https://schema.org",

              "@type": "SoftwareApplication",

              name: "Runexa Enterprise AI",

              applicationCategory: "BusinessApplication",

              operatingSystem: "Web",

              url: "https://runexa.ai/fr/enterprise-ai",

              inLanguage: "fr",

              description:
                "Espace IA entreprise pour l’analyse documentaire, le reporting financier, les workflows d’apprentissage, la business intelligence et l’aide à la décision.",

              publisher: {
                "@type": "Organization",
                name: "Runexa Systems LLC",
                url: siteUrl,
              },

              knowsAbout: [
                "IA entreprise",
                "Systèmes IA personnalisés",
                "Espace IA",
                "Workflows IA entreprise",
                "Business Intelligence IA",
                "Aide à la décision IA",
              ],
            },
          ]),
        }}
      />
    </>
  );
}
