import type { Metadata } from "next";
import StudyAgentDemoClient from "./StudyAgentDemoClient";

export const metadata: Metadata = {
  title: "Runexa Study Agent Demo",
  description:
    "See Runexa Study Agent in action. Generate AI summaries, quizzes, flashcards, visual learning maps, audio support, and personalized study plans.",

  alternates: {
    canonical: "https://runexa.ai/demo/study-agent",
    languages: {
      en: "https://runexa.ai/en/demo/study-agent",
      fr: "https://runexa.ai/fr/demo/study-agent",
      ar: "https://runexa.ai/ar/demo/study-agent",
      "x-default": "https://runexa.ai/demo/study-agent",
    },
  },

  openGraph: {
    title: "Runexa Study Agent Demo",
    description:
      "Turn study materials into summaries, quizzes, flashcards, learning maps, audio, and personalized revision plans with AI.",
    url: "https://runexa.ai/demo/study-agent",
    siteName: "Runexa Systems",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Study Agent Demo",
      },
    ],
    locale: "en_US",
    type: "website",
  },

  twitter: {
    card: "summary_large_image",
    title: "Runexa Study Agent Demo",
    description:
      "Turn study materials into summaries, quizzes, flashcards, learning maps, audio, and personalized revision plans with AI.",
    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

const jsonLd = {
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  name: "Runexa Study Agent",
  applicationCategory: "EducationalApplication",
  operatingSystem: "Web",
  url: "https://runexa.ai/demo/study-agent",
  description:
    "AI study assistant for summaries, quizzes, flashcards, visual learning maps, audio learning support, and personalized study plans.",
};

export default function StudyAgentDemoPage() {
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(jsonLd),
        }}
      />

      <StudyAgentDemoClient />
    </>
  );
}
