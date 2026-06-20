import type { Metadata } from "next";
import StudyClient from "./StudyClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "AI Study Workspace & Learning Assistant | Runexa",

  description:
    "Generate AI summaries, quizzes, flashcards, audio explanations, mind maps, and personalized study plans with Runexa Study Agent.",

 keywords: [
  "AI study assistant",
  "AI learning workspace",
  "AI flashcards",
  "AI quizzes",
  "AI study plan",
  "AI education",
  "AI summaries",
  "AI learning platform",
  "Runexa study AI",
  "adaptive learning AI",

  "Runexa Study Agent",
  "AI learning assistant",
  "AI-powered learning",
  "personalized learning AI",
  "adaptive education technology",
  "smart learning platform",
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
  "education technology",
  "AI-powered education",
  "learning workflow automation",
  "student learning platform",
  "Study AI Platform",
  "Education AI",
  "Enterprise Learning AI",
],

  alternates: {
    canonical: "https://runexa.ai/study",
    languages: {
      en: `${siteUrl}/en/study`,
      fr: `${siteUrl}/fr/study`,
      ar: `${siteUrl}/ar/study`,
      "x-default": `${siteUrl}/study`,
    },
  },

  openGraph: {
    title: "Runexa Study Agent",

    description:
      "AI-powered study workspace with summaries, quizzes, flashcards, and adaptive learning.",

    url: "https://runexa.ai/study",

    siteName: "Runexa Systems",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Study Agent",
      },
    ],

    locale: "en_US",

    alternateLocale: ["fr_FR", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Runexa Study Agent",

    description:
      "AI summaries, quizzes, flashcards, audio explanations, and adaptive learning workflows.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function StudyPage() {
  return (
    <>
      <StudyClient initialLocale="en" />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "SoftwareApplication",

            name: "Runexa Study Agent",

            applicationCategory: "EducationalApplication",

            operatingSystem: "Web",

            description:
              "AI-powered study workspace with summaries, quizzes, flashcards, visual learning, and adaptive study plans.",

            url: "https://runexa.ai/study",

            inLanguage: "en",

            creator: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
            },

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: siteUrl,
            },

            knowsAbout: [
              "AI Study Assistant",
              "AI Learning Workspace",
              "AI Flashcards",
              "AI Quizzes",
              "AI Study Plans",
              "Adaptive Learning AI",
            ],
          }),
        }}
      />
    </>
  );
}
