import type { Metadata } from "next";
import AgentZeroClient from "../../../labs/agent-0/AgentZeroClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title:
    "Runexa Agent 0 | Infrastructure de sécurité IA et maison intelligente",

  description:
    "Runexa Agent 0 est un concept futur de sécurité IA et de surveillance intelligente combinant caméras, capteurs, GPS et systèmes de raisonnement intelligent.",

  keywords: [
    "système sécurité IA",
    "maison intelligente IA",
    "surveillance IA",
    "capteurs IA",
    "intelligence caméra IA",
    "automatisation maison IA",
    "infrastructure sécurité IA",
    "Runexa Labs",
    "Agent 0",
  ],

  alternates: {
    canonical: "https://runexa.ai/fr/labs/agent-0",
    languages: {
      en: `${siteUrl}/en/labs/agent-0`,
      fr: `${siteUrl}/fr/labs/agent-0`,
      ar: `${siteUrl}/ar/labs/agent-0`,
      "x-default": `${siteUrl}/labs/agent-0`,
    },
  },

  openGraph: {
    title:
      "Runexa Agent 0 | Infrastructure de sécurité IA et maison intelligente",

    description:
      "Infrastructure future de sécurité IA combinant caméras, capteurs, GPS et raisonnement intelligent pour la surveillance intelligente.",

    url: "https://runexa.ai/fr/labs/agent-0",

    siteName: "Runexa Systems",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Agent 0",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title:
      "Runexa Agent 0 | Infrastructure de sécurité IA et maison intelligente",

    description:
      "Infrastructure expérimentale de sécurité IA combinant caméras, capteurs, GPS et systèmes de raisonnement intelligent.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function AgentZeroPage() {
  return (
    <>
      <AgentZeroClient initialLanguage="fr" lockInitialLanguage />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "ResearchProject",

            name: "Runexa Agent 0",

            description:
              "Concept expérimental d’infrastructure de sécurité IA combinant caméras, capteurs, GPS et systèmes de raisonnement intelligent.",

            url: "https://runexa.ai/fr/labs/agent-0",

            inLanguage: "fr",

            creator: {
              "@type": "Organization",
              name: "Runexa Labs",
            },

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems",
              url: siteUrl,
            },
          }),
        }}
      />
    </>
  );
}
