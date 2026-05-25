import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AI Contract Review & Legal Document Analysis | Runexa",
  description:
    "Analyze contracts, detect risky clauses, understand obligations, and get practical recommendations with Runexa Legal Agent.",
  keywords: [
    "AI contract review",
    "AI legal document analysis",
    "AI contract analyzer",
    "legal AI software",
    "contract risk analysis",
    "AI legal review",
  ],
  alternates: {
    canonical: "https://runexa.ai/legal-ai",
  },
};

export default function LegalAIPage() {
  return (
    <main className="min-h-screen bg-slate-50 px-6 py-20 text-slate-900">
      <section className="mx-auto max-w-6xl text-center">
        <p className="font-semibold text-blue-600">Runexa Legal Agent</p>

        <h1 className="mt-4 text-5xl font-bold tracking-tight">
          AI Contract Review & Legal Document Analysis
        </h1>

        <p className="mx-auto mt-6 max-w-3xl text-lg text-slate-600">
          Runexa helps individuals and professionals analyze contracts, detect
          risky clauses, understand obligations, and receive practical legal
          document insights before signing.
        </p>

        <div className="mt-8 flex flex-wrap justify-center gap-3">
          <Link
            href="/upload"
            className="rounded-xl bg-blue-600 px-6 py-3 text-sm font-semibold text-white hover:bg-blue-700"
          >
            Try Legal Agent
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
            "Risky clause detection",
            "Identify clauses that may create legal, financial, or operational risk.",
          ],
          [
            "Obligation extraction",
            "Understand payment terms, deadlines, duties, renewals, and termination rules.",
          ],
          [
            "Executive summaries",
            "Get plain-language summaries of complex contracts and agreements.",
          ],
          [
            "Practical recommendations",
            "Receive suggested next steps and negotiation points before signing.",
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
        <h2 className="text-3xl font-bold">How Runexa legal AI works</h2>

        <div className="mt-8 grid gap-4 md:grid-cols-3">
          {[
            "Upload a contract or legal document",
            "Runexa AI analyzes clauses, obligations, and risk signals",
            "Receive a structured legal intelligence report",
          ].map((step, index) => (
            <div key={step} className="rounded-2xl bg-slate-50 p-6">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-600 text-sm font-bold text-white">
                {index + 1}
              </div>
              <p className="mt-4 font-semibold">{step}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto mt-16 max-w-6xl rounded-3xl border bg-white p-8 shadow-sm md:p-12">
        <h2 className="text-3xl font-bold">Legal AI FAQ</h2>

        <div className="mt-8 grid gap-4 md:grid-cols-2">
          {[
            [
              "Is Runexa a law firm?",
              "No. Runexa provides informational AI analysis and decision-support output. It does not replace professional legal advice.",
            ],
            [
              "Can AI review contracts?",
              "Runexa can help review contracts by highlighting clauses, obligations, risks, and recommendations for further review.",
            ],
            [
              "What documents can the Legal Agent analyze?",
              "Runexa Legal Agent is designed for contracts and legal agreements such as NDAs, service agreements, employment contracts, and vendor agreements.",
            ],
            [
              "Is legal document processing private?",
              "Runexa is designed as a secure AI workspace for private document analysis and professional workflows.",
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
            name: "Runexa Legal Agent",
            applicationCategory: "BusinessApplication",
            operatingSystem: "Web",
            description:
              "AI contract review and legal document analysis software for risky clause detection, obligation extraction, summaries, and recommendations.",
            url: "https://runexa.ai/legal-ai",
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
