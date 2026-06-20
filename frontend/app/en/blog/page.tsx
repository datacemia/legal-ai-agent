import type { Metadata } from "next";
import BlogClient from "../../blog/BlogClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Enterprise AI Blog & Insights | Runexa",

  description:
    "Insights about legal AI, finance AI, enterprise AI workflows, business intelligence, and AI-powered operational systems.",

  keywords: [
  "AI blog",
  "enterprise AI",
  "legal AI",
  "finance AI",
  "AI workflows",
  "business intelligence AI",
  "Runexa blog",
  "AI automation insights",

  "AI insights",
  "AI articles",
  "AI news",
  "AI trends",
  "artificial intelligence blog",
  "enterprise AI insights",
  "AI strategy",
  "AI governance",
  "responsible AI",
  "AI best practices",
  "AI transformation",
  "digital transformation",
  "AI productivity",
  "AI innovation",
  "AI technology",
  "AI business insights",
  "AI decision making",
  "AI for enterprises",
  "AI adoption",
  "AI implementation",
  "AI automation",
  "workflow automation",
  "AI document analysis",
  "contract analysis AI",
  "legal technology",
  "Legal AI insights",
  "Finance AI insights",
  "Business AI insights",
  "Study AI insights",
  "AI education technology",
  "enterprise automation",
  "business intelligence platform",
  "data-driven decision making",
  "AI-powered workflows",
  "AI software trends",
  "generative AI",
  "specialized AI agents",
  "Runexa AI",
  "Runexa Systems",
  "AI thought leadership",
],

  alternates: {
    canonical: "https://runexa.ai/en/blog",
    languages: {
      en: `${siteUrl}/en/blog`,
      fr: `${siteUrl}/fr/blog`,
      ar: `${siteUrl}/ar/blog`,
      "x-default": `${siteUrl}/blog`,
    },
  },

  openGraph: {
    title: "Enterprise AI Blog & Insights | Runexa",

    description:
      "Insights about legal AI, finance AI, enterprise AI workflows, business intelligence, and AI-powered operational systems.",

    url: "https://runexa.ai/en/blog",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa AI Blog",
      },
    ],

    locale: "en_US",

    alternateLocale: ["fr_FR", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Enterprise AI Blog & Insights | Runexa",

    description:
      "Insights about legal AI, finance AI, enterprise AI workflows, business intelligence, and AI-powered operational systems.",

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
      <BlogClient initialLocale="en" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "Blog",

            name: "Runexa AI Blog",

            description:
              "Insights about legal AI, finance AI, enterprise AI workflows, business intelligence, and AI-powered operational systems.",

            url: "https://runexa.ai/en/blog",

            inLanguage: "en",

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
