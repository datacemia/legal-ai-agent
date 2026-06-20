import type { Metadata } from "next";
import StudyAIClient from "../../study-ai/StudyAIClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "AI Study Assistant & Learning Workspace | Runexa",

  description:
    "Generate summaries, quizzes, flashcards, study plans, and structured learning workflows with Runexa Study AI.",

  keywords: [
  "study AI",
  "AI study assistant",
  "AI flashcards",
  "AI quizzes",
  "AI summaries",
  "AI study plans",
  "learning workflows AI",
  "Runexa study AI",

  "Runexa Study Agent",
  "AI learning assistant",
  "AI-powered learning",
  "personalized learning AI",
  "adaptive learning AI",
  "smart learning platform",
  "AI education",
  "education AI",
  "AI tutoring",
  "AI tutor",
  "AI for students",
  "student productivity AI",
  "AI exam preparation",
  "AI revision tools",
  "study management AI",
  "learning management AI",
  "AI-generated quizzes",
  "interactive quizzes AI",
  "AI flashcard generator",
  "smart flashcards",
  "course summary AI",
  "document-to-summary AI",
  "lesson summaries AI",
  "lecture notes AI",
  "AI note taking",
  "study organization AI",
  "custom study plans",
  "personalized study plans",
  "AI learning paths",
  "academic productivity AI",
  "AI educational content",
  "AI knowledge extraction",
  "e-learning AI",
  "digital learning AI",
  "self-paced learning AI",
  "AI for schools",
  "AI for universities",
  "AI learning platform",
  "AI-powered education",
  "Study AI Platform",
],

  alternates: {
    canonical: "https://runexa.ai/en/study-ai",
    languages: {
      en: `${siteUrl}/en/study-ai`,
      fr: `${siteUrl}/fr/study-ai`,
      ar: `${siteUrl}/ar/study-ai`,
      "x-default": `${siteUrl}/study-ai`,
    },
  },

  openGraph: {
    title: "AI Study Assistant & Learning Workspace | Runexa",

    description:
      "Generate summaries, quizzes, flashcards, study plans, and structured learning workflows with Runexa Study AI.",

    url: "https://runexa.ai/en/study-ai",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Study AI",
      },
    ],

    locale: "en_US",

    alternateLocale: ["fr_FR", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "AI Study Assistant & Learning Workspace | Runexa",

    description:
      "AI-powered study assistant for summaries, quizzes, flashcards, study plans, and structured learning workflows.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function StudyAIPage() {
  return (
    <>
      <StudyAIClient initialLocale="en" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify([
            {
              "@context": "https://schema.org",

              "@type": "SoftwareApplication",

              name: "Runexa Study AI",

              applicationCategory: "EducationalApplication",

              operatingSystem: "Web",

              url: "https://runexa.ai/en/study-ai",

              inLanguage: "en",

              description:
                "AI study assistant for summaries, quizzes, flashcards, study plans, and structured learning workflows.",

              publisher: {
                "@type": "Organization",
                name: "Runexa Systems LLC",
                url: siteUrl,
              },

              knowsAbout: [
                "Study AI",
                "AI Study Assistant",
                "AI Flashcards",
                "AI Quizzes",
                "AI Summaries",
                "AI Study Plans",
                "Learning Workflows AI",
              ],
            },
          ]),
        }}
      />
    </>
  );
}
