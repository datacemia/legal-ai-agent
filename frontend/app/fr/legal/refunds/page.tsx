import type { Metadata } from "next";
import RefundPolicyClient from "../../../legal/refunds/RefundPolicyClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Politique de remboursement | Runexa",

  description:
    "Politique de remboursement de Runexa Systems LLC couvrant les crédits IA, abonnements, litiges de facturation, chargebacks, droits des consommateurs lorsque applicables et services entreprise.",

  keywords: [
    "politique de remboursement",
    "remboursement des abonnements IA",
    "facturation Runexa",
    "remboursement des crédits IA",
    "facturation IA pour entreprises",
    "politique de remboursement SaaS",
    "litiges de facturation IA",
    "résiliation d’abonnement",
    "protection des consommateurs",
    "droit de rétractation",
    "transparence de la facturation",
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
      "Politique de remboursement de Runexa Systems LLC couvrant les crédits IA, abonnements, litiges de facturation, chargebacks, droits des consommateurs lorsque applicables et services entreprise.",

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
      "Politique de remboursement de Runexa Systems LLC couvrant les crédits IA, abonnements, litiges de facturation, chargebacks, droits des consommateurs lorsque applicables et services entreprise.",

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

            name: "Runexa Refund Policy",

            description:
              "Politique de remboursement et de facturation pour les services IA Runexa, abonnements, crédits IA, workflows entreprise, litiges de facturation, annulations et droits des consommateurs lorsque applicables.",

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
