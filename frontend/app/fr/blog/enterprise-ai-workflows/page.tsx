import type { Metadata } from "next";
import EnterpriseAIWorkflowsArticle from "../../../blog/enterprise-ai-workflows/EnterpriseAIWorkflowsArticle";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Workflows IA d’entreprise : construire des opérations augmentées par l’IA | Runexa",

  description:
    "Découvrez comment les workflows IA d’entreprise aident les organisations à automatiser l’analyse, améliorer la prise de décision, réduire les tâches répétitives et développer l’intelligence opérationnelle.",

  keywords: [
    "workflows IA entreprise",
    "IA d’entreprise",
    "opérations augmentées par IA",
    "automatisation workflow IA",
    "intelligence documentaire IA",
    "aide à la décision IA",
    "Runexa enterprise AI",
    "workflows business IA",
  ],

  alternates: {
    canonical: "https://runexa.ai/fr/blog/enterprise-ai-workflows",
    languages: {
      en: `${siteUrl}/en/blog/enterprise-ai-workflows`,
      fr: `${siteUrl}/fr/blog/enterprise-ai-workflows`,
      ar: `${siteUrl}/ar/blog/enterprise-ai-workflows`,
      "x-default": `${siteUrl}/blog/enterprise-ai-workflows`,
    },
  },

  openGraph: {
    title: "Workflows IA d’entreprise : construire des opérations augmentées par l’IA | Runexa",

    description:
      "Découvrez comment les workflows IA d’entreprise aident les organisations à automatiser l’analyse, améliorer la prise de décision, réduire les tâches répétitives et développer l’intelligence opérationnelle.",

    url: "https://runexa.ai/fr/blog/enterprise-ai-workflows",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Enterprise AI Workflows",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "article",
  },

  twitter: {
    card: "summary_large_image",

    title: "Workflows IA d’entreprise : construire des opérations augmentées par l’IA | Runexa",

    description:
      "Découvrez comment les workflows IA d’entreprise aident les organisations à automatiser l’analyse, améliorer la prise de décision, réduire les tâches répétitives et développer l’intelligence opérationnelle.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function EnterpriseAIWorkflowsPage() {
  return (
    <>
      <EnterpriseAIWorkflowsArticle initialLocale="fr" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "Article",

            mainEntityOfPage: {
              "@type": "WebPage",
              "@id": "https://runexa.ai/fr/blog/enterprise-ai-workflows",
            },

            headline:
              "Workflows IA d’entreprise : comment les organisations construisent des opérations augmentées par l’IA",

            description:
              "Découvrez comment les workflows IA d’entreprise aident les organisations à automatiser l’analyse, améliorer la prise de décision, réduire les tâches répétitives et développer l’intelligence opérationnelle.",

            datePublished: "2026-05-24",

            dateModified: "2026-05-24",

            inLanguage: "fr",

            author: {
              "@type": "Person",
              name: "Dr. Rachid Ejjami",
            },

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
