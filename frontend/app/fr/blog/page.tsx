import type { Metadata } from "next";
import BlogClient from "../../blog/BlogClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Blog IA entreprise et insights | Runexa",

  description:
    "Insights sur l’IA juridique, la finance IA, les workflows IA entreprise, la business intelligence et les systèmes opérationnels alimentés par l’IA.",

  keywords: [
    "blog IA",
    "IA entreprise",
    "IA juridique",
    "finance IA",
    "workflows IA",
    "business intelligence IA",
    "blog Runexa",
    "insights automatisation IA",
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
