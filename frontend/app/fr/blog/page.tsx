import type { Metadata } from "next";
import BlogClient from "../../blog/BlogClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Blog IA entreprise et insights | Runexa",

  description:
    "Insights sur l’IA juridique, la finance IA, les workflows IA entreprise, la business intelligence et les systèmes opérationnels alimentés par l’IA.",

 keywords: [
    "blog intelligence artificielle",
    "IA pour entreprises",
    "intelligence artificielle juridique",
    "intelligence artificielle financière",
    "workflows IA",
    "business intelligence IA",
    "blog Runexa",
    "insights sur l’automatisation par IA",

    "actualités de l’intelligence artificielle",
    "articles sur l’intelligence artificielle",
    "transformation numérique",
    "automatisation des entreprises",
    "productivité grâce à l’IA",
    "agents IA",
    "intelligence artificielle responsable",
    "gouvernance de l’IA",
    "utilisation de l’IA en entreprise",
    "solutions IA pour entreprises",
    "Legal AI",
    "Finance AI",
    "Study AI",
    "Business AI",
    "analyse de contrats par IA",
    "révision de contrats par IA",
    "analyse financière par IA",
    "éducation assistée par IA",
    "apprentissage intelligent",
    "aide à la décision par IA",
    "analyse des KPI",
    "analyse stratégique par IA",
    "automatisation documentaire",
    "traitement de documents par IA",
    "outils d’intelligence artificielle",
    "meilleures pratiques IA",
    "conformité IA",
    "sécurité de l’IA",
    "confidentialité des données IA",
    "Runexa AI",
    "Runexa Systems",
  ],

  alternates: {
    canonical: "https://runexa.ai/fr/blog",
    languages: {
      en: `${siteUrl}/en/blog`,
      fr: `${siteUrl}/fr/blog`,
      ar: `${siteUrl}/ar/blog`,
      "x-default": `${siteUrl}/blog`,
    },
  },

  openGraph: {
    title: "Blog IA entreprise et insights | Runexa",

    description:
      "Insights sur l’IA juridique, la finance IA, les workflows IA entreprise, la business intelligence et les systèmes opérationnels alimentés par l’IA.",

    url: "https://runexa.ai/fr/blog",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa AI Blog",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Blog IA entreprise et insights | Runexa",

    description:
      "Insights sur l’IA juridique, la finance IA, les workflows IA entreprise, la business intelligence et les systèmes opérationnels alimentés par l’IA.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function BlogPage() {
  return (
    <>
      <BlogClient initialLocale="fr" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "Blog",

            name: "Blog IA Runexa",

            description:
              "Insights sur l’IA juridique, la finance IA, les workflows IA entreprise, la business intelligence et les systèmes opérationnels alimentés par l’IA.",

            url: "https://runexa.ai/fr/blog",

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
