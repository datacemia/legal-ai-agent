import type { Metadata } from "next";
import RefundPolicyClient from "../../../legal/refunds/RefundPolicyClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Politique de remboursement | Runexa",

  description:
    "Politique de remboursement de Runexa Systems LLC couvrant les crédits IA, abonnements, litiges de facturation, rétrofacturations et services entreprise.",

  keywords: [
    "politique de remboursement",
    "remboursement abonnement IA",
    "facturation Runexa",
    "remboursement crédits IA",
    "facturation IA entreprise",
    "politique remboursement SaaS",
    "litiges facturation IA",
    "annulation abonnement",
  ],

  alternates: {
    canonical: "https://runexa.ai/fr/legal/refunds",
    languages: {
      en: `${siteUrl}/en/legal/refunds`,
      fr: `${siteUrl}/fr/legal/refunds`,
      ar: `${siteUrl}/ar/legal/refunds`,
      "x-default": `${siteUrl}/legal/refunds`,
    },
  },

  openGraph: {
    title: "Politique de remboursement | Runexa",

    description:
      "Politique de remboursement et de facturation pour les services IA Runexa, abonnements, crédits, plans entreprise et workflows intelligents.",

    url: "https://runexa.ai/fr/legal/refunds",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Refund Policy",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Politique de remboursement | Runexa",

    description:
      "Consultez l’éligibilité aux remboursements, les conditions de facturation, les abonnements, crédits IA et politiques entreprise de Runexa Systems LLC.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function RefundPolicyPage() {
  return (
    <>
      <RefundPolicyClient initialLocale="fr" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "Politique de remboursement Runexa",

            description:
              "Politique de remboursement et de facturation pour les services IA Runexa, abonnements, crédits IA, workflows entreprise et plateformes intelligentes.",

            url: "https://runexa.ai/fr/legal/refunds",

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
