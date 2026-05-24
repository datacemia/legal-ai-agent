import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Runexa Developers | Build With AI Agents",
  description:
    "Build with Runexa AI agents for legal analysis, finance intelligence, study workflows, and business decision support.",
  keywords: [
    "Runexa API",
    "AI agents API",
    "legal AI API",
    "finance AI API",
    "business AI API",
    "study AI API",
    "AI workflow API",
  ],
  alternates: {
    canonical: "https://runexa.ai/developers",
  },
};

export default function DevelopersPage() {
  return (
    <main className="min-h-screen bg-slate-50 px-6 py-20 text-slate-900">
      <section className="mx-auto max-w-6xl text-center">
        <p className="font-semibold text-blue-600">Runexa Developers</p>

        <h1 className="mt-4 text-5xl font-bold tracking-tight">
          Build AI workflows with specialized Runexa agents
        </h1>

        <p className="mx-auto mt-6 max-w-3xl text-lg leading-8 text-slate-600">
          Runexa is evolving into an AI workspace and API platform for legal
          analysis, finance intelligence, study automation, and business
          decision support.
        </p>

        <div className="mt-8 flex flex-wrap justify-center gap-3">
          <Link
            href="/api"
            className="rounded-xl bg-blue-600 px-6 py-3 text-sm font-semibold text-white hover:bg-blue-700"
          >
            Explore API
          </Link>

          <Link
            href="/docs"
            className="rounded-xl border border-slate-200 bg-white px-6 py-3 text-sm font-semibold text-slate-900 hover:bg-slate-50"
          >
            View Docs
          </Link>
        </div>
      </section>

      <section className="mx-auto mt-16 grid max-w-6xl gap-6 md:grid-cols-4">
        {[
          [
            "Legal AI",
            "Analyze contracts, risky clauses, obligations, and recommendations.",
          ],
          [
            "Finance AI",
            "Analyze statements, subscriptions, spending, and savings opportunities.",
          ],
          [
            "Study AI",
            "Generate summaries, quizzes, flashcards, and study plans.",
          ],
          [
            "Business AI",
            "Analyze KPIs, risks, opportunities, and strategic decisions.",
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

      <section className="mx-auto mt-16 max-w-6xl rounded-3xl border bg-slate-950 p-8 text-white shadow-sm md:p-12">
        <p className="text-sm font-semibold text-blue-300">
          Developer workflow
        </p>

        <h2 className="mt-3 text-3xl font-bold">
          Async AI jobs designed for real workloads
        </h2>

        <div className="mt-8 grid gap-4 md:grid-cols-3">
          {[
            ["1", "Send a file or structured data to a Runexa agent endpoint."],
            ["2", "Receive a job ID while Runexa processes the AI workflow."],
            ["3", "Poll the job status and retrieve structured analysis results."],
          ].map(([num, text]) => (
            <div
              key={num}
              className="rounded-2xl border border-white/10 bg-white/5 p-5"
            >
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-600 text-sm font-bold">
                {num}
              </div>
              <p className="mt-4 text-sm leading-6 text-slate-200">
                {text}
              </p>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto mt-16 max-w-6xl rounded-3xl border bg-white p-8 shadow-sm md:p-12">
        <h2 className="text-3xl font-bold">Authentication</h2>

        <p className="mt-4 max-w-3xl leading-8 text-slate-600">
          Runexa API requests use bearer token authentication. Include your API
          key in the Authorization header for every request.
        </p>

        <pre className="mt-6 overflow-x-auto rounded-2xl bg-slate-950 p-5 text-sm text-slate-100">
{`Authorization: Bearer rk_live_xxx`}
        </pre>
      </section>

      <section className="mx-auto mt-16 max-w-6xl rounded-3xl border bg-white p-8 shadow-sm md:p-12">
        <h2 className="text-3xl font-bold">Example API flow</h2>

        <pre className="mt-6 overflow-x-auto rounded-2xl bg-slate-950 p-5 text-sm text-slate-100">
{`POST /v1/legal/analyze
Authorization: Bearer RUNEXA_API_KEY

Response:
{
  "job_id": 123,
  "status": "pending"
}

GET /v1/jobs/123

Response:
{
  "status": "completed",
  "result": {
    "risk_score": 82,
    "summary": "...",
    "recommendations": []
  }
}`}
        </pre>
      </section>

      <section className="mx-auto mt-16 max-w-6xl rounded-3xl bg-blue-600 p-8 text-center text-white md:p-12">
        <h2 className="text-3xl font-bold">Start with Runexa AI agents</h2>
        <p className="mx-auto mt-4 max-w-2xl text-blue-100">
          Explore Runexa APIs, review endpoint examples, and prepare AI workflows
          for legal, finance, study, and business use cases.
        </p>

        <Link
          href="/docs"
          className="mt-6 inline-block rounded-xl bg-white px-6 py-3 text-sm font-semibold text-blue-600"
        >
          Read Developer Docs
        </Link>
      </section>
    </main>
  );
}
