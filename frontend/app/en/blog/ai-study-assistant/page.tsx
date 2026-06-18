import type { Metadata } from "next";
import AIStudyAssistantArticle from "../../../blog/ai-study-assistant/AIStudyAssistantArticle";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "AI Study Assistant: Building Smarter Learning Workflows | Runexa",

  description:
    "Learn how AI study assistants help generate summaries, quizzes, flashcards, and structured learning workflows.",

  keywords: [
    "AI study assistant",
    "AI learning workflows",
    "AI summaries",
    "AI flashcards",
    "AI quizzes",
    "study planning AI",
    "Runexa Study Agent",
    "education AI",
  ],

  alternates: {
    canonical: "https://runexa.ai/en/blog/ai-study-assistant",
    languages: {
      en: `${siteUrl}/en/blog/ai-study-assistant`,
      fr: `${siteUrl}/fr/blog/ai-study-assistant`,
      ar: `${siteUrl}/ar/blog/ai-study-assistant`,
      "x-default": `${siteUrl}/blog/ai-study-assistant`,
    },
  },

  openGraph: {
    title: "AI Study Assistant: Building Smarter Learning Workflows | Runexa",

    description:
      "Learn how AI study assistants help generate summaries, quizzes, flashcards, and structured learning workflows.",

    url: "https://runexa.ai/en/blog/ai-study-assistant",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa AI Study Assistant",
      },
    ],

    locale: "en_US",

    alternateLocale: ["fr_FR", "ar_AR"],

    type: "article",
  },

  twitter: {
    card: "summary_large_image",

    title: "AI Study Assistant: Building Smarter Learning Workflows | Runexa",

    description:
      "Learn how AI study assistants help generate summaries, quizzes, flashcards, and structured learning workflows.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function AIStudyAssistantPage() {
  return (
    <>
      <AIStudyAssistantArticle initialLocale="en" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "Article",

            mainEntityOfPage: {
              "@type": "WebPage",
              "@id": "https://runexa.ai/en/blog/ai-study-assistant",
            },

            headline:
              "AI Study Assistant: Building Smarter Learning Workflows",

            description:
              "Learn how AI study assistants help generate summaries, quizzes, flashcards, and structured learning workflows.",

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
