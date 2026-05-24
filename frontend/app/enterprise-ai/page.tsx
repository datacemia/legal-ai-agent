import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Enterprise AI Workspace & Custom AI Systems | Runexa",
  description:
    "Runexa helps organizations build enterprise AI workflows for document analysis, business intelligence, finance, learning, and decision support.",
  keywords: [
    "enterprise AI workspace",
    "custom AI systems",
    "enterprise AI workflows",
    "AI document analysis",
    "business intelligence AI",
    "AI decision support",
  ],
  alternates: {
    canonical: "https://runexa.ai/enterprise-ai",
  },
};

export default function EnterpriseAIPage() {
  return (
    <main className="min-h-screen bg-slate-50 px-6 py-20 text-slate-900">
      <section className="mx-auto max-w-6xl text-center">
        <p className="font-semibold text-blue-600">Runexa Enterprise AI</p>

        <h1 className="mt-4 text-5xl font-bold tracking-tight">
          Enterprise AI Workspace & Custom AI Systems
        </h1>

        <p className="mx-auto mt-6 max-w-3xl text-lg text-slate-600">
          Runexa helps teams and organizations create secure AI workflows for
          document analysis, financial reporting, learning operations, business
          intelligence, and strategic decision support.
        </p>

        <div className="mt-8 flex flex-wrap justify-center gap-3">
          <Link
            href="/contact-entreprise/contact"
            className="rounded-xl bg-blue-600 px-6 py-3 text-sm font-semibold text-white hover:bg-blue-700"
          >
            Request a Demo
          </Link>

          <Link
            href="/enterprise"
            className="rounded-xl border border-slate-200 bg-white px-6 py-3 text-sm font-semibold text-slate-900 hover:bg-slate-50"
          >
            Explore Enterprise
          </Link>
        </div>
      </section>

      <section className="mx-auto mt-16 grid max-w-6xl gap-6 md:grid-cols-4">
        {[
          [
            "Team workspaces",
            "Create shared AI workspaces for teams, departments, and organizations.",
          ],
          [
            "Custom AI workflows",
            "Design AI systems for document analysis, reporting, learning, and decisions.",
          ],
          [
            "Organization dashboard",
            "Manage users, usage, credits, and AI workflows in one place.",
          ],
          [
            "Enterprise support",
            "Support for custom credits, priority workflows, and organization needs.",
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
        <h2 className="text-3xl font-bold">Enterprise AI use cases</h2>

        <div className="mt-8 grid gap-4 md:grid-cols-3">
          {[
            "Legal document analysis and contract workflows",
            "Financial reporting and business intelligence",
            "Training, learning, and internal knowledge workflows",
          ].map((item) => (
            <div key={item} className="rounded-2xl bg-slate-50 p-6">
              <p className="font-semibold">{item}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto mt-16 max-w-6xl rounded-3xl border bg-white p-8 shadow-sm md:p-12">
        <h2 className="text-3xl font-bold">Enterprise AI FAQ</h2>

        <div className="mt-8 grid gap-4 md:grid-cols-2">
          {[
            [
              "Can Runexa support teams?",
              "Yes. Runexa is designed to support team workspaces, organization dashboards, multi-user access, and custom AI workflows.",
            ],
            [
              "What enterprise workflows can Runexa automate?",
              "Runexa can support legal analysis, financial reporting, business intelligence, learning operations, and internal decision-support workflows.",
            ],
            [
              "Is Runexa suitable for organizations?",
              "Yes. Runexa is positioned as a secure AI workspace for individuals, professionals, and organizations.",
            ],
            [
              "Can Runexa build custom AI systems?",
              "Runexa can support custom AI systems and workflows for teams and enterprise use cases.",
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
            name: "Runexa Enterprise AI",
            applicationCategory: "BusinessApplication",
            operatingSystem: "Web",
            description:
              "Enterprise AI workspace for document analysis, financial reporting, learning workflows, business intelligence, and decision support.",
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
