import type { Metadata } from "next";
import StudyAIClient from "./StudyAIClient";

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
  ],

  alternates: {
    canonical: "https://runexa.ai/study-ai",
  },

  openGraph: {
    title: "AI Study Assistant & Learning Workspace | Runexa",

    description:
      "Generate summaries, quizzes, flashcards, study plans, and structured learning workflows with Runexa Study AI.",

    url: "https://runexa.ai/study-ai",

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
  return <StudyAIClient />;
}
