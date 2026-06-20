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

  "AI learning assistant",
  "AI-powered learning",
  "AI education platform",
  "AI study tools",
  "AI study planner",
  "personalized learning AI",
  "adaptive learning AI",
  "AI tutoring",
  "AI for students",
  "student productivity AI",
  "AI exam preparation",
  "AI revision tools",
  "smart study assistant",
  "course summary AI",
  "document-to-summary AI",
  "lecture notes AI",
  "AI note taking",
  "AI-generated quizzes",
  "AI test preparation",
  "interactive learning AI",
  "AI flashcard generator",
  "AI knowledge extraction",
  "learning management AI",
  "study organization AI",
  "academic productivity AI",
  "AI educational content",
  "AI learning platform",
  "digital learning AI",
  "self-paced learning AI",
  "AI learning paths",
  "custom study plans",
  "AI academic assistant",
  "education technology AI",
  "e-learning AI",
  "AI for schools",
  "AI for universities",
  "AI-powered education",
  "Study AI",
  "Education AI",
  "AI Learning Platform",
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
