import type { Metadata } from "next";
import EnterpriseAIWorkflowsArticle from "../../../blog/enterprise-ai-workflows/EnterpriseAIWorkflowsArticle";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Enterprise AI Workflows: How Organizations Build AI-Powered Operations | Runexa",

  description:
    "Learn how enterprise AI workflows help organizations automate analysis, improve decision-making, reduce repetitive work, and scale operational intelligence.",

  keywords: [
    "enterprise AI workflows",
    "enterprise AI",
    "AI-powered operations",
    "AI workflow automation",
    "AI document intelligence",
    "AI decision support",
    "Runexa enterprise AI",
    "business AI workflows",
  ],

  alternates: {
    canonical: "https://runexa.ai/en/blog/enterprise-ai-workflows",
    languages: {
      en: `${siteUrl}/en/blog/enterprise-ai-workflows`,
      fr: `${siteUrl}/fr/blog/enterprise-ai-workflows`,
      ar: `${siteUrl}/ar/blog/enterprise-ai-workflows`,
      "x-default": `${siteUrl}/blog/enterprise-ai-workflows`,
    },
  },

  openGraph: {
    title: "Enterprise AI Workflows: How Organizations Build AI-Powered Operations | Runexa",

    description:
      "Learn how enterprise AI workflows help organizations automate analysis, improve decision-making, reduce repetitive work, and scale operational intelligence.",

    url: "https://runexa.ai/en/blog/enterprise-ai-workflows",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Enterprise AI Workflows",
      },
    ],

    locale: "en_US",

    alternateLocale: ["fr_FR", "ar_AR"],

    type: "article",
  },

  twitter: {
    card: "summary_large_image",

    title: "Enterprise AI Workflows: How Organizations Build AI-Powered Operations | Runexa",

    description:
      "Learn how enterprise AI workflows help organizations automate analysis, improve decision-making, reduce repetitive work, and scale operational intelligence.",

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
      <EnterpriseAIWorkflowsArticle initialLocale="en" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "Article",

            mainEntityOfPage: {
              "@type": "WebPage",
              "@id": "https://runexa.ai/en/blog/enterprise-ai-workflows",
            },

            headline:
              "Enterprise AI Workflows: How Organizations Build AI-Powered Operations",

            description:
              "Learn how enterprise AI workflows help organizations automate analysis, improve decision-making, reduce repetitive work, and scale operational intelligence.",

            datePublished: "2026-05-24",

            dateModified: "2026-05-24",

            inLanguage: "en",

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
