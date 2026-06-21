import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Runexa Study Agent Demo",
  description:
    "See a complete demonstration of the Runexa Study Agent. Analyze PDFs, notes, textbooks, quizzes, flashcards, and study materials using AI.",

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
      "Analyze PDFs, notes, textbooks, quizzes, flashcards, and study materials using AI.",
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
      "Analyze PDFs, notes, textbooks, quizzes, flashcards, and study materials using AI.",
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
    "AI study assistant capable of analyzing notes, PDFs, textbooks, quizzes, flashcards, and study materials.",
};

export default function StudyAgentDemoPage() {
  return (
    <main className="min-h-screen bg-slate-50 px-6 py-16">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(jsonLd),
        }}
      />

      <div className="mx-auto max-w-6xl">
        <h1 className="text-5xl font-bold tracking-tight text-slate-900">
          Runexa Study Agent Demo
        </h1>

        <p className="mt-6 max-w-3xl text-lg text-slate-600">
          Upload study materials, notes, PDFs, textbooks, and educational
          documents to generate AI-powered summaries, quizzes, flashcards, key
          concepts, and personalized study plans.
        </p>

        <div className="mt-10">
          <Image
            src="/demo/study-agent-demo-en.png"
            alt="Runexa Study Agent Demo"
            width={1440}
            height={5000}
            sizes="(max-width: 768px) 100vw, (max-width: 1280px) 90vw, 1152px"
            className="h-auto w-full rounded-3xl border border-slate-200 shadow-lg"
          />
        </div>

        <div className="mt-10 rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
          <h2 className="text-2xl font-bold text-slate-900">
            What can the Study Agent do?
          </h2>

          <ul className="mt-4 space-y-3 text-slate-600">
            <li>✓ Generate concise study summaries</li>
            <li>✓ Create quizzes automatically</li>
            <li>✓ Build flashcards from documents</li>
            <li>✓ Extract key concepts and topics</li>
            <li>✓ Generate personalized study plans</li>
            <li>✓ Analyze PDFs, notes, and educational materials</li>
          </ul>
        </div>

        <div className="mt-10 text-center">
          <p className="mb-6 text-lg text-slate-600">
            Ready to analyze your own study materials?
          </p>

          <Link
            href="/study"
            className="inline-flex rounded-xl bg-blue-600 px-8 py-4 text-lg font-semibold text-white transition hover:bg-blue-700"
          >
            Try Study Agent
          </Link>
        </div>
      </div>
    </main>
  );
}