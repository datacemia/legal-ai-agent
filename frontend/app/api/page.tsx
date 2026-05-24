import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Runexa API | AI Agents for Documents, Finance & Business",
  description:
    "Runexa API provides specialized AI agent endpoints for legal document analysis, finance intelligence, study workflows, and business decision support.",
};

export default function ApiPage() {
  return (
    <main className="min-h-screen bg-slate-50 px-6 py-20 text-slate-900">
      <section className="mx-auto max-w-6xl text-center">
        <p className="font-semibold text-blue-600">Runexa API</p>

        <h1 className="mt-4 text-5xl font-bold tracking-tight">
          AI agent APIs for real-world workflows
        </h1>

        <p className="mx-auto mt-6 max-w-3xl text-lg leading-8 text-slate-600">
          Connect applications, dashboards, and internal tools to Runexa AI
          agents for contract analysis, finance intelligence, learning
          automation, and business decision support.
        </p>

        <div className="mt-8 flex flex-wrap justify-center gap-3">
          <Link
            href="/docs"
            className="rounded-xl bg-blue-600 px-6 py-3 text-sm font-semibold text-white hover:bg-blue-700"
          >
            View API Docs
          </Link>

          <Link
            href="/developers"
            className="rounded-xl border border-slate-200 bg-white px-6 py-3 text-sm font-semibold text-slate-900 hover:bg-slate-50"
          >
            Developers
          </Link>
        </div>
      </section>

      <section className="mx-auto mt-16 grid max-w-6xl gap-6 md:grid-cols-2">
        {[
          [
            "Legal Analysis API",
            "Submit legal documents and receive risk scores, clause analysis, obligations, and recommendations.",
            "POST /v1/legal/analyze",
          ],
          [
            "Finance Analysis API",
            "Submit bank statements and receive spending insights, subscriptions, savings opportunities, and financial scores.",
            "POST /v1/finance/analyze",
          ],
          [
            "Study Agent API",
            "Submit learning material and generate summaries, quizzes, flashcards, and study plans.",
            "POST /v1/study/analyze",
          ],
          [
            "Business Intelligence API",
            "Submit business files and receive KPIs, risks, opportunities, charts, and executive recommendations.",
            "POST /v1/business/analyze",
          ],
        ].map(([title, desc, endpoint]) => (
          <div key={title} className="rounded-3xl border bg-white p-8 shadow-sm">
            <h2 className="text-2xl font-bold">{title}</h2>
            <p className="mt-4 leading-7 text-slate-600">{desc}</p>

            <div className="mt-6 rounded-2xl bg-slate-950 px-4 py-3 font-mono text-sm text-slate-100">
              {endpoint}
            </div>
          </div>
        ))}
      </section>

      <section className="mx-auto mt-16 max-w-6xl rounded-3xl border bg-white p-8 shadow-sm md:p-12">
        <p className="text-sm font-semibold text-blue-600">API architecture</p>

        <h2 className="mt-3 text-3xl font-bold">
          Built around asynchronous AI jobs
        </h2>

        <p className="mt-4 max-w-4xl leading-7 text-slate-600">
          AI analysis can take time depending on file size and workflow
          complexity. Runexa API is designed around job-based processing:
          submit a request, receive a job ID, poll for progress, and retrieve
          structured results when complete.
        </p>

        <div className="mt-8 grid gap-4 md:grid-cols-4">
          {[
            "Upload file",
            "Create AI job",
            "Poll job status",
            "Receive JSON result",
          ].map((item, index) => (
            <div key={item} className="rounded-2xl bg-slate-50 p-5">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-600 text-sm font-bold text-white">
                {index + 1}
              </div>
              <p className="mt-4 font-semibold">{item}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto mt-16 max-w-6xl rounded-3xl border bg-slate-950 p-8 text-white shadow-sm md:p-12">
        <h2 className="text-3xl font-bold">Example response</h2>

        <pre className="mt-6 overflow-x-auto rounded-2xl border border-white/10 bg-white/5 p-5 text-sm text-slate-100">
{`{
  "job_id": "job_123",
  "status": "completed",
  "result": {
    "agent": "legal",
    "risk_score": 82,
    "summary": "The contract contains several medium-risk clauses.",
    "recommendations": [
      "Clarify termination notice periods.",
      "Review liability limitation language."
    ]
  }
}`}
        </pre>
      </section>

      <section className="mx-auto mt-16 max-w-6xl rounded-3xl bg-blue-600 p-8 text-center text-white md:p-12">
        <h2 className="text-3xl font-bold">
          Build with Runexa AI infrastructure
        </h2>

        <p className="mx-auto mt-4 max-w-2xl text-blue-100">
          Use Runexa APIs to power document intelligence, finance analysis,
          learning automation, and business decision support inside your own
          products.
        </p>

        <Link
          href="/docs"
          className="mt-6 inline-block rounded-xl bg-white px-6 py-3 text-sm font-semibold text-blue-600"
        >
          Read API Docs
        </Link>
      </section>
    </main>
  );
}