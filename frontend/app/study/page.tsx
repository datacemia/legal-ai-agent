import type { Metadata } from "next";
import StudyClient from "./StudyClient";

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
  ],

  alternates: {
    canonical: "https://runexa.ai/study",
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
      <StudyClient />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "SoftwareApplication",

            name: "Runexa Study Agent",

            applicationCategory:
              "EducationalApplication",

            operatingSystem: "Web",

            description:
              "AI-powered study workspace with summaries, quizzes, flashcards, visual learning, and adaptive study plans.",

            url: "https://runexa.ai/study",

            creator: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
            },

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: "https://runexa.ai",
            },
          }),
        }}
      />
    </>
  );
}
