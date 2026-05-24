import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Runexa Docs | AI Agent API Documentation",
  description:
    "Developer documentation for Runexa AI agent APIs, async jobs, authentication, endpoints, and structured analysis responses.",
};

export default function DocsPage() {
  return (
    <main className="min-h-screen bg-slate-50 px-6 py-20 text-slate-900">
      <section className="mx-auto max-w-7xl">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <p className="font-semibold text-blue-600">Runexa Docs</p>

            <h1 className="mt-4 text-5xl font-bold tracking-tight">
              AI Agent API Documentation
            </h1>

            <p className="mt-6 max-w-3xl text-lg leading-8 text-slate-600">
              Build AI-powered workflows using Runexa asynchronous APIs for
              legal, finance, business intelligence, and study automation.
            </p>
          </div>

          <div className="rounded-2xl border border-blue-200 bg-blue-50 px-5 py-4">
            <p className="text-xs font-semibold uppercase tracking-[0.25em] text-blue-700">
              Developer Platform
            </p>

            <p className="mt-2 text-sm text-blue-900">
              Async AI infrastructure for enterprise workflows
            </p>
          </div>
        </div>
      </section>

      <section className="mx-auto mt-12 grid max-w-7xl gap-6 lg:grid-cols-[280px_1fr]">
        <aside className="sticky top-10 h-fit rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <p className="text-sm font-bold text-slate-900">Contents</p>

          <nav className="mt-5 space-y-3 text-sm text-slate-600">
            {[
              ["Introduction", "#introduction"],
              ["Authentication", "#authentication"],
              ["Async jobs", "#jobs"],
              ["Finance AI", "#finance"],
              ["Legal AI", "#legal"],
              ["Business AI", "#business"],
              ["Jobs API", "#jobs-api"],
              ["Errors", "#errors"],
              ["Rate limits", "#rate-limits"],
              ["Security", "#security"],
            ].map(([label, href]) => (
              <a
                key={href}
                href={href}
                className="block transition hover:text-blue-600"
              >
                {label}
              </a>
            ))}
          </nav>
        </aside>

        <div className="space-y-8">
          <section
            id="introduction"
            className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm"
          >
            <p className="text-sm font-semibold text-blue-600">
              Introduction
            </p>

            <h2 className="mt-3 text-3xl font-bold">
              Runexa AI infrastructure
            </h2>

            <p className="mt-5 leading-8 text-slate-600">
              Runexa API allows developers and enterprises to integrate advanced
              AI analysis workflows directly into products, dashboards, internal
              tools, and enterprise systems.
            </p>

            <div className="mt-8 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              {[
                "Legal AI analysis",
                "Finance AI analysis",
                "Business AI analysis",
                "Study AI analysis",
              ].map((item) => (
                <div
                  key={item}
                  className="rounded-2xl border border-slate-200 bg-slate-50 p-5"
                >
                  <p className="font-semibold text-slate-900">{item}</p>
                </div>
              ))}
            </div>

            <div className="mt-8 rounded-2xl bg-slate-950 p-6 text-sm text-slate-100">
              <p className="text-slate-400">Base URL</p>

              <pre className="mt-4 overflow-x-auto text-blue-300">
{`https://api.runexa.ai

Local:
http://127.0.0.1:8000`}
              </pre>
            </div>
          </section>

          <section
            id="authentication"
            className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm"
          >
            <h2 className="text-3xl font-bold">Authentication</h2>

            <p className="mt-5 leading-8 text-slate-600">
              All API requests require a bearer API key.
            </p>

            <pre className="mt-6 overflow-x-auto rounded-2xl bg-slate-950 p-5 text-sm text-slate-100">
{`Authorization: Bearer rk_live_xxxxxxxxx`}
            </pre>

            <pre className="mt-6 overflow-x-auto rounded-2xl bg-slate-950 p-5 text-sm text-slate-100">
{`curl -X GET "http://127.0.0.1:8000/v1/test-api-key" \\
  -H "Authorization: Bearer rk_live_xxxxxxxxx"`}
            </pre>
          </section>

          <section
            id="jobs"
            className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm"
          >
            <h2 className="text-3xl font-bold">Async Architecture</h2>

            <p className="mt-5 leading-8 text-slate-600">
              Runexa APIs use asynchronous AI processing powered by queue-based
              workers.
            </p>

            <div className="mt-8 grid gap-4 md:grid-cols-4">
              {[
                "Upload file",
                "Create AI job",
                "Worker processing",
                "Retrieve results",
              ].map((item, index) => (
                <div
                  key={item}
                  className="rounded-2xl border border-slate-200 bg-slate-50 p-5"
                >
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-600 text-sm font-bold text-white">
                    {index + 1}
                  </div>

                  <p className="mt-4 font-semibold text-slate-900">{item}</p>
                </div>
              ))}
            </div>

            <pre className="mt-8 overflow-x-auto rounded-2xl bg-slate-950 p-5 text-sm text-slate-100">
{`Frontend
→ Runexa API
→ Job Queue
→ AI Workers
→ Persistent Storage
→ Async Result Retrieval`}
            </pre>
          </section>

          <section
            id="finance"
            className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm"
          >
            <div className="flex items-center justify-between">
              <h2 className="text-3xl font-bold">Finance AI</h2>

              <span className="rounded-full bg-emerald-100 px-3 py-1 text-xs font-bold text-emerald-700">
                POST /v1/finance/analyze
              </span>
            </div>

            <div className="mt-6 grid gap-4 md:grid-cols-3">
              {[
                "Bank statements",
                "Subscriptions",
                "Savings opportunities",
              ].map((item) => (
                <div
                  key={item}
                  className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4"
                >
                  <p className="font-semibold text-emerald-900">{item}</p>
                </div>
              ))}
            </div>

            <pre className="mt-8 overflow-x-auto rounded-2xl bg-slate-950 p-5 text-sm text-slate-100">
{`curl -X POST "http://127.0.0.1:8000/v1/finance/analyze" \\
  -H "Authorization: Bearer rk_live_xxxxxxxxx" \\
  -F "file=@statement.pdf" \\
  -F "output_language=en"`}
            </pre>

            <pre className="mt-6 overflow-x-auto rounded-2xl bg-slate-950 p-5 text-sm text-slate-100">
{`{
  "job_id": 9,
  "status": "pending",
  "progress": 0,
  "status_message": "Finance API analysis queued...",
  "credits_used": 7,
  "remaining_api_credits": 88
}`}
            </pre>
          </section>

          <section
            id="legal"
            className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm"
          >
            <div className="flex items-center justify-between">
              <h2 className="text-3xl font-bold">Legal AI</h2>

              <span className="rounded-full bg-amber-100 px-3 py-1 text-xs font-bold text-amber-700">
                POST /v1/legal/analyze
              </span>
            </div>

            <div className="mt-6 grid gap-4 md:grid-cols-3">
              {[
                "Contract analysis",
                "Risk detection",
                "Clause extraction",
              ].map((item) => (
                <div
                  key={item}
                  className="rounded-2xl border border-amber-200 bg-amber-50 p-4"
                >
                  <p className="font-semibold text-amber-900">{item}</p>
                </div>
              ))}
            </div>

            <pre className="mt-8 overflow-x-auto rounded-2xl bg-slate-950 p-5 text-sm text-slate-100">
{`curl -X POST "http://127.0.0.1:8000/v1/legal/analyze" \\
  -H "Authorization: Bearer rk_live_xxxxxxxxx" \\
  -F "file=@contract.pdf" \\
  -F "output_language=en"`}
            </pre>

            <pre className="mt-6 overflow-x-auto rounded-2xl bg-slate-950 p-5 text-sm text-slate-100">
{`{
  "job_id": 10,
  "status": "pending",
  "credits_used": 12,
  "remaining_api_credits": 76
}`}
            </pre>
          </section>

          <section
            id="business"
            className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm"
          >
            <div className="flex items-center justify-between">
              <h2 className="text-3xl font-bold">Business AI</h2>

              <span className="rounded-full bg-blue-100 px-3 py-1 text-xs font-bold text-blue-700">
                POST /v1/business/analyze
              </span>
            </div>

            <div className="mt-6 grid gap-4 md:grid-cols-3">
              {[
                "KPI dashboards",
                "Forecasting",
                "Executive reporting",
              ].map((item) => (
                <div
                  key={item}
                  className="rounded-2xl border border-blue-200 bg-blue-50 p-4"
                >
                  <p className="font-semibold text-blue-900">{item}</p>
                </div>
              ))}
            </div>

            <pre className="mt-8 overflow-x-auto rounded-2xl bg-slate-950 p-5 text-sm text-slate-100">
{`curl -X POST "http://127.0.0.1:8000/v1/business/analyze" \\
  -H "Authorization: Bearer rk_live_xxxxxxxxx" \\
  -F "file=@business.xlsx" \\
  -F "output_language=en"`}
            </pre>

            <pre className="mt-6 overflow-x-auto rounded-2xl bg-slate-950 p-5 text-sm text-slate-100">
{`{
  "job_id": 13,
  "status": "pending",
  "credits_used": 30,
  "remaining_api_credits": 22
}`}
            </pre>
          </section>

          <section
            id="jobs-api"
            className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm"
          >
            <h2 className="text-3xl font-bold">Jobs API</h2>

            <p className="mt-5 leading-8 text-slate-600">
              Retrieve asynchronous AI analysis results.
            </p>

            <pre className="mt-8 overflow-x-auto rounded-2xl bg-slate-950 p-5 text-sm text-slate-100">
{`GET /v1/jobs/{job_id}

{
  "id": 15,
  "status": "completed",
  "progress": 100,
  "result": {}
}`}
            </pre>
          </section>

          <section
            id="errors"
            className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm"
          >
            <h2 className="text-3xl font-bold">Error Responses</h2>

            <div className="mt-8 space-y-4">
              {[
                [
                  "401 Unauthorized",
                  "Missing or invalid API key.",
                ],
                [
                  "402 Payment Required",
                  "Insufficient credits or API access disabled.",
                ],
                [
                  "413 Payload Too Large",
                  "Uploaded file exceeds allowed limits.",
                ],
                [
                  "429 Too Many Requests",
                  "Rate limit exceeded.",
                ],
                [
                  "500 Server Error",
                  "Unexpected AI processing error.",
                ],
              ].map(([code, desc]) => (
                <div
                  key={code}
                  className="rounded-2xl border border-slate-200 bg-slate-50 p-5"
                >
                  <p className="font-bold text-slate-900">{code}</p>

                  <p className="mt-2 text-sm text-slate-600">{desc}</p>
                </div>
              ))}
            </div>
          </section>

          <section
            id="rate-limits"
            className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm"
          >
            <h2 className="text-3xl font-bold">Rate Limits</h2>

            <div className="mt-8 overflow-hidden rounded-2xl border border-slate-200">
              <table className="min-w-full divide-y divide-slate-200 text-sm">
                <thead className="bg-slate-100">
                  <tr>
                    <th className="px-5 py-4 text-left font-bold">
                      Plan
                    </th>
                    <th className="px-5 py-4 text-left font-bold">
                      Requests
                    </th>
                  </tr>
                </thead>

                <tbody className="divide-y divide-slate-200 bg-white">
                  {[
                    ["API Starter", "10 requests/minute"],
                    ["API Pro", "60 requests/minute"],
                    ["Enterprise API", "Custom"],
                  ].map(([plan, limit]) => (
                    <tr key={plan}>
                      <td className="px-5 py-4">{plan}</td>
                      <td className="px-5 py-4">{limit}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          <section
            id="security"
            className="rounded-3xl bg-slate-950 p-8 text-white"
          >
            <h2 className="text-3xl font-bold">
              Security & Enterprise Support
            </h2>

            <div className="mt-6 grid gap-4 md:grid-cols-2">
              {[
                "Never expose API keys publicly",
                "Store API keys server-side",
                "Rotate compromised keys immediately",
                "Use HTTPS only",
              ].map((item) => (
                <div
                  key={item}
                  className="rounded-2xl bg-white/5 p-4"
                >
                  <p className="text-slate-100">{item}</p>
                </div>
              ))}
            </div>

            <div className="mt-8 rounded-2xl border border-white/10 bg-white/5 p-6">
              <p className="text-sm uppercase tracking-[0.25em] text-blue-300">
                Enterprise Support
              </p>

              <p className="mt-3 text-lg font-semibold">
                support@runexa.ai
              </p>
            </div>

            <Link
              href="/api"
              className="mt-8 inline-flex items-center rounded-2xl bg-white px-6 py-3 text-sm font-semibold text-slate-900 transition hover:-translate-y-0.5"
            >
              Explore API Platform
            </Link>
          </section>
        </div>
      </section>
    </main>
  );
}
