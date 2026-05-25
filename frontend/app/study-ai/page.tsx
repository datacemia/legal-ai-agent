import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AI Study Assistant & Learning Workspace | Runexa",
  description:
    "Generate summaries, quizzes, flashcards, study plans, and learning insights with Runexa Study Agent.",
  keywords: [
    "AI study assistant",
    "AI learning workspace",
    "AI flashcards",
    "AI quiz generator",
    "AI study plan",
    "AI learning platform",
  ],
  alternates: {
    canonical: "https://runexa.ai/study-ai",
  },
};

export default function StudyAIPage() {
  return (
    <main className="min-h-screen bg-slate-50 px-6 py-20 text-slate-900">
      <section className="mx-auto max-w-6xl text-center">
        <p className="font-semibold text-violet-600">
          Runexa Study Agent
        </p>

        <h1 className="mt-4 text-5xl font-bold tracking-tight">
          AI Study Assistant & Learning Workspace
        </h1>

        <p className="mx-auto mt-6 max-w-3xl text-lg text-slate-600">
          Runexa Study Agent helps students and professionals generate summaries,
          quizzes, flashcards, study plans, and structured learning workflows
          with AI.
        </p>

        <div className="mt-8 flex flex-wrap justify-center gap-3">
          <Link
            href="/study"
            className="rounded-xl bg-violet-600 px-6 py-3 text-sm font-semibold text-white hover:bg-violet-700"
          >
            Start Studying
          </Link>

          <Link
            href="/pricing"
            className="rounded-xl border border-slate-200 bg-white px-6 py-3 text-sm font-semibold text-slate-900 hover:bg-slate-50"
          >
            View Pricing
          </Link>
        </div>
      </section>

      <section className="mx-auto mt-16 grid max-w-6xl gap-6 md:grid-cols-4">
        {[
          [
            "AI summaries",
            "Generate structured summaries from study materials and documents.",
          ],
          [
            "Flashcards & quizzes",
            "Create interactive learning material automatically with AI.",
          ],
          [
            "Study plans",
            "Organize revision sessions and learning goals more efficiently.",
          ],
          [
            "Learning workflows",
            "Build faster and more structured study workflows with AI assistance.",
          ],
        ].map(([title, desc]) => (
          <div
            key={title}
            className="rounded-2xl border bg-white p-6 shadow-sm"
          >
            <h2 className="font-bold">{title}</h2>
            <p className="mt-3 text-sm leading-6 text-slate-600">
              {desc}
            </p>
          </div>
        ))}
      </section>

      <section className="mx-auto mt-16 max-w-6xl rounded-3xl border bg-white p-8 shadow-sm md:p-12">
        <h2 className="text-3xl font-bold">
          How Runexa study AI works
        </h2>

        <div className="mt-8 grid gap-4 md:grid-cols-3">
          {[
            "Upload study material or notes",
            "Runexa generates summaries, quizzes, and study tools",
            "Learn faster with structured AI learning workflows",
          ].map((step, index) => (
            <div key={step} className="rounded-2xl bg-slate-50 p-6">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-violet-600 text-sm font-bold text-white">
                {index + 1}
              </div>

              <p className="mt-4 font-semibold">{step}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto mt-16 max-w-6xl rounded-3xl border bg-white p-8 shadow-sm md:p-12">
        <h2 className="text-3xl font-bold">Study AI FAQ</h2>

        <div className="mt-8 grid gap-4 md:grid-cols-2">
          {[
            [
              "Can Runexa replace a teacher?",
              "No. Runexa supports learning and revision, but it does not replace teachers, official materials, or academic guidance.",
            ],
            [
              "What can the Study Agent generate?",
              "Runexa can generate summaries, quizzes, flashcards, study plans, visual summaries, and learning workflows.",
            ],
            [
              "Can Runexa help with exam preparation?",
              "Yes. Runexa can help organize revision, identify key points, and create practice questions for study sessions.",
            ],
            [
              "Does Runexa support different education levels?",
              "Yes. Runexa Study Agent can adapt explanations and questions based on the selected education level.",
            ],
          ].map(([q, a]) => (
            <div key={q} className="rounded-2xl bg-slate-50 p-6">
              <h3 className="font-bold">{q}</h3>
              <p className="mt-2 text-sm leading-6 text-slate-600">
                {a}
              </p>
            </div>
          ))}
        </div>
      </section>

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
              "AI study assistant for summaries, quizzes, flashcards, study plans, and structured learning workflows.",
            url: "https://runexa.ai/study-ai",
            publisher: {
              "@type": "Organization",
              name: "Runexa Systems",
            },
          }),
        }}
      />
    </main>
  );
}
