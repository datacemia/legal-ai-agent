import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AI Study Assistant: Smarter Learning With AI Workflows | Runexa",
  description:
    "Learn how AI study assistants help generate summaries, quizzes, flashcards, and structured learning workflows.",

  keywords: [
    "AI study assistant",
    "AI learning assistant",
    "AI flashcards",
    "AI quiz generation",
    "AI study workflows",
    "AI learning platform",
  ],

  alternates: {
    canonical:
      "https://runexa.ai/blog/ai-study-assistant",
  },

  openGraph: {
    title:
      "AI Study Assistant: Smarter Learning With AI Workflows",

    description:
      "Learn how AI study assistants help generate summaries, quizzes, flashcards, and structured learning workflows.",

    url:
      "https://runexa.ai/blog/ai-study-assistant",

    siteName: "Runexa",

    type: "article",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Study AI",
      },
    ],
  },

  twitter: {
    card: "summary_large_image",

    title:
      "AI Study Assistant: Smarter Learning With AI Workflows",

    description:
      "Learn how AI study assistants help generate summaries, quizzes, flashcards, and structured learning workflows.",

    images: ["/og-image.png"],
  },
};

export default function AIStudyAssistantArticle() {
  return (
    <main className="min-h-screen bg-slate-50 px-6 py-20 text-slate-900">
      <article className="mx-auto max-w-4xl">
        <Link href="/blog" className="text-sm font-semibold text-violet-600">
          ← Back to Blog
        </Link>

        <p className="mt-8 text-sm font-semibold uppercase tracking-wide text-violet-600">
          Study AI
        </p>

        <h1 className="mt-4 text-5xl font-bold tracking-tight">
          AI Study Assistant: Smarter Learning With AI Workflows
        </h1>

        <p className="mt-6 text-lg leading-8 text-slate-600">
          Learning large amounts of information can be difficult, repetitive,
          and time-consuming. AI study assistants help students and
          professionals organize knowledge, generate summaries, create quizzes,
          and build more efficient learning workflows.
        </p>

        <div className="mt-10 rounded-3xl border bg-white p-8 shadow-sm">
          <h2 className="text-2xl font-bold">
            What is an AI study assistant?
          </h2>

          <p className="mt-4 leading-8 text-slate-600">
            An AI study assistant uses artificial intelligence to analyze study
            materials and generate structured educational support such as
            summaries, flashcards, quizzes, explanations, revision plans, and
            learning recommendations.
          </p>
        </div>

        <section className="mt-10 space-y-8">
          <div>
            <h2 className="text-3xl font-bold">
              Why traditional studying is inefficient
            </h2>

            <p className="mt-4 leading-8 text-slate-600">
              Many learners spend hours manually summarizing documents,
              organizing notes, rewriting concepts, and preparing revision
              material. This often creates cognitive overload and reduces
              learning efficiency. AI can automate repetitive study tasks and
              improve learning structure.
            </p>
          </div>

          <div className="grid gap-6 md:grid-cols-2">
            {[
              [
                "AI summaries",
                "AI can transform long study documents into concise and structured summaries.",
              ],
              [
                "Flashcards & quizzes",
                "AI can generate learning exercises automatically for revision and memory reinforcement.",
              ],
              [
                "Study planning",
                "AI can help organize learning sessions, revision schedules, and educational priorities.",
              ],
              [
                "Knowledge organization",
                "AI can structure complex information into more understandable learning flows.",
              ],
            ].map(([title, text]) => (
              <div
                key={title}
                className="rounded-2xl border bg-white p-6 shadow-sm"
              >
                <h3 className="font-bold">{title}</h3>

                <p className="mt-3 text-sm leading-6 text-slate-600">
                  {text}
                </p>
              </div>
            ))}
          </div>

          <div>
            <h2 className="text-3xl font-bold">
              AI learning workflows for modern education
            </h2>

            <p className="mt-4 leading-8 text-slate-600">
              AI-powered learning systems can support students, professionals,
              researchers, and organizations by simplifying content review,
              accelerating knowledge acquisition, and improving educational
              productivity.
            </p>
          </div>

          <div className="rounded-3xl border bg-white p-8 shadow-sm">
            <h2 className="text-2xl font-bold">
              How Runexa Study Agent helps
            </h2>

            <p className="mt-4 leading-8 text-slate-600">
              Runexa Study Agent helps users upload study materials and generate
              AI-powered summaries, quizzes, flashcards, study plans, and
              structured learning workflows designed to improve productivity and
              understanding.
            </p>

            <div className="mt-6 grid gap-3 sm:grid-cols-2">
              {[
                "AI study summaries",
                "Flashcard generation",
                "Quiz generation",
                "Study planning",
                "Learning workflows",
                "Educational productivity tools",
              ].map((item) => (
                <div
                  key={item}
                  className="rounded-xl bg-slate-50 px-4 py-3 text-sm font-semibold text-slate-700"
                >
                  {item}
                </div>
              ))}
            </div>
          </div>

          <div>
            <h2 className="text-3xl font-bold">
              AI should support learning, not replace thinking
            </h2>

            <p className="mt-4 leading-8 text-slate-600">
              The best educational AI systems help learners understand concepts
              more efficiently while keeping human reasoning, critical thinking,
              and active learning at the center of the process.
            </p>
          </div>
        </section>

        <section className="mt-12 rounded-3xl bg-violet-600 p-8 text-white">
          <h2 className="text-3xl font-bold">
            Learn faster with AI study workflows
          </h2>

          <p className="mt-4 text-violet-100">
            Use Runexa Study Agent to generate summaries, quizzes,
            flashcards, and structured learning workflows with AI.
          </p>

          <Link
            href="/study"
            className="mt-6 inline-block rounded-xl bg-white px-6 py-3 text-sm font-semibold text-violet-600"
          >
            Start Studying
          </Link>
        </section>

        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "Article",

              mainEntityOfPage: {
                "@type": "WebPage",
                "@id":
                  "https://runexa.ai/blog/ai-study-assistant",
              },

              headline:
                "AI Study Assistant: Smarter Learning With AI Workflows",

              description:
                "Learn how AI study assistants help generate summaries, quizzes, flashcards, and structured learning workflows.",

              datePublished: "2026-05-24",

              dateModified: "2026-05-24",

              author: {
                "@type": "Person",
                name: "Dr. Rachid Ejjami",
              },
              publisher: {
                "@type": "Organization",
                name: "Runexa Systems",
              },
            }),
          }}
        />
      </article>
    </main>
  );
}