import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Runexa Study Agent Demo | Runexa Systems",
  description:
    "See Runexa Study Agent in action. Turn study materials into AI summaries, quizzes, flashcards, visual learning maps, audio support, and personalized revision plans.",

  alternates: {
    canonical: "https://runexa.ai/en/demo/study-agent",
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
      "See how Runexa Study transforms study materials into a complete AI-powered learning workspace.",
    url: "https://runexa.ai/en/demo/study-agent",
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
      "AI summaries, quizzes, flashcards, visual learning maps, audio support, and personalized revision plans.",
    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

const STUDY_DEMO_VIDEO =
  "https://drive.google.com/file/d/1KRkbdt21_81RSDWnsLZ9Um3FY5j2TRDX/preview";

const jsonLd = {
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  name: "Runexa Study Agent",
  applicationCategory: "EducationalApplication",
  operatingSystem: "Web",
  url: "https://runexa.ai/en/demo/study-agent",
  inLanguage: "en",
  description:
    "AI study assistant for summaries, quizzes, flashcards, visual learning maps, audio learning support, and personalized study plans.",
};

export default function StudyAgentDemoPage() {
  return (
    <main
      lang="en"
      className="min-h-screen bg-slate-50 px-4 py-14 sm:px-6 sm:py-16"
    >
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(jsonLd),
        }}
      />

      <div className="mx-auto max-w-6xl">
        {/* Hero */}
        <div className="text-center">
          <span className="inline-flex rounded-full border border-blue-200 bg-blue-50 px-4 py-1.5 text-xs font-bold uppercase tracking-[0.18em] text-blue-700">
            Demonstration
          </span>

          <h1 className="mx-auto mt-5 max-w-4xl text-4xl font-black tracking-tight text-slate-950 sm:text-5xl">
            Runexa Study Agent Demo
          </h1>

          <p className="mx-auto mt-5 max-w-3xl text-base leading-7 text-slate-600 sm:text-lg">
            See how Runexa Study transforms study materials into a complete
            AI-powered learning workspace.
          </p>
        </div>

        {/* Video */}
        <section className="mt-10 overflow-hidden rounded-[2rem] border border-slate-200 bg-white shadow-xl">
          <div className="border-b border-slate-100 px-6 py-5 sm:px-8">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h2 className="text-xl font-black text-slate-950 sm:text-2xl">
                  Runexa Study Agent — English Demo
                </h2>

                <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-600">
                  Watch Runexa Study analyze learning material and generate
                  summaries, quizzes, flashcards, visual learning maps, audio
                  support, and personalized revision plans.
                </p>
              </div>

              <span className="inline-flex w-fit rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-bold text-slate-600">
                English
              </span>
            </div>
          </div>

          <div className="bg-slate-950 p-2 sm:p-4">
            <iframe
              src={STUDY_DEMO_VIDEO}
              title="Runexa Study Agent English Demo"
              className="aspect-video w-full rounded-2xl bg-black"
              allow="autoplay; fullscreen"
              referrerPolicy="strict-origin-when-cross-origin"
              allowFullScreen
            />
          </div>
        </section>

        {/* Capabilities */}
        <section className="mt-10 rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
          <h2 className="text-2xl font-black text-slate-950">
            What can Runexa Study Agent do?
          </h2>

          <div className="mt-6 grid gap-3 sm:grid-cols-2">
            {[
              "Generate structured summaries and detailed explanations",
              "Create theoretical and practical quizzes",
              "Build flashcards automatically",
              "Generate visual learning maps",
              "Provide audio learning support",
              "Create personalized revision plans",
              "Identify weak learning areas after quizzes",
            ].map((item) => (
              <div
                key={item}
                className="flex items-start gap-3 rounded-2xl border border-slate-100 bg-slate-50 px-4 py-3"
              >
                <span className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-green-100 text-sm font-black text-green-700">
                  ✓
                </span>

                <span className="text-sm font-medium leading-6 text-slate-700">
                  {item}
                </span>
              </div>
            ))}
          </div>
        </section>

        {/* CTA */}
        <section className="mt-10 rounded-[2rem] bg-slate-950 px-6 py-10 text-center text-white sm:px-10">
          <p className="text-lg font-semibold text-slate-200">
            Ready to analyze your own study materials?
          </p>

          <Link
            href="/en/study"
            className="mt-6 inline-flex rounded-2xl bg-blue-600 px-8 py-4 text-base font-black text-white transition hover:-translate-y-0.5 hover:bg-blue-500"
          >
            Try Runexa Study
          </Link>
        </section>
      </div>
    </main>
  );
}