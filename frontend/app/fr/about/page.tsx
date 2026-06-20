import type { Metadata } from "next";
import AboutClient from "../../about/AboutClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "À propos de Runexa | Histoire du fondateur et agents IA spécialisés",

  description:
    "Découvrez pourquoi Dr. Rachid Ejjami a créé Runexa Systems LLC et comment des défis réels ont inspiré le Study Agent, Legal Agent, Finance Coach et Business Decision Agent.",

  keywords: [
    "Runexa",
    "Runexa Systems LLC",
    "Dr. Rachid Ejjami",
    "créé par le Dr. Rachid Ejjami",
    "agents IA",
    "agents IA spécialisés",
    "espace de travail IA",
    "agent juridique IA",
    "coach financier IA",
    "agent IA pour les études",
    "IA d'aide à la décision commerciale",
    "IA responsable",
    "IA d'entreprise",
  ],

  alternates: {
    canonical: "https://runexa.ai/fr/about",
    languages: {
      en: `${siteUrl}/en/about`,
      fr: `${siteUrl}/fr/about`,
      ar: `${siteUrl}/ar/about`,
      "x-default": `${siteUrl}/about`,
    },
  },

  openGraph: {
    title: "À propos de Runexa | Histoire du fondateur et agents IA spécialisés",

    description:
      "Découvrez pourquoi Dr. Rachid Ejjami a créé Runexa Systems LLC et comment des défis réels ont inspiré le Study Agent, Legal Agent, Finance Coach et Business Decision Agent.",

    url: "https://runexa.ai/fr/about",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "About Runexa Systems",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "À propos de Runexa | Histoire du fondateur et agents IA spécialisés",

    description:
      "Découvrez pourquoi Dr. Rachid Ejjami a créé Runexa Systems LLC et comment des défis réels ont inspiré le Study Agent, Legal Agent, Finance Coach et Business Decision Agent.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function AboutPage() {
  return (
    <>
      <AboutClient initialLocale="fr" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify([
            {
              "@context": "https://schema.org",

              "@type": "AboutPage",

              name: "À propos de Runexa | Histoire du fondateur et agents IA spécialisés",

              description:
                "Découvrez pourquoi Dr. Rachid Ejjami a créé Runexa Systems LLC et comment des défis réels ont inspiré le Study Agent, Legal Agent, Finance Coach et Business Decision Agent.",

              url: "https://runexa.ai/fr/about",

              inLanguage: "fr",

              publisher: {
                "@type": "Organization",
                name: "Runexa Systems LLC",
                url: siteUrl,
              },
            },
            {
              "@context": "https://schema.org",

              "@type": "Organization",

              name: "Runexa Systems LLC",

              url: siteUrl,

              founder: {
                "@type": "Person",
                name: "Dr. Rachid Ejjami",
                jobTitle: "Founder and Managing Member",
              },

              address: {
                "@type": "PostalAddress",
                streetAddress: "1309 Coffeen Avenue, Suite 1200",
                addressLocality: "Sheridan",
                addressRegion: "WY",
                postalCode: "82801",
                addressCountry: "US",
              },

              description:
                "Runexa Systems LLC builds specialized AI agents for legal document analysis, learning support, personal finance coaching, business decision support, and responsible AI workflows.",

              knowsAbout: [
                "Artificial Intelligence",
                "Legal AI",
                "Study AI",
                "Finance Coach AI",
                "Business Intelligence",
                "Responsible AI",
                "Enterprise AI Workflows"
              ],
            },
          ]),
        }}
      />
    </>
  );
}
