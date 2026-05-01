"use client";

import Link from "next/link";

const agentCategories = [
  {
    title: "Legal AI Agents",
    description: "Support legal, compliance, and risk teams with AI-powered document analysis.",
    agents: [
      {
        name: "Legal AI Agent",
        desc: "Analyze internal contracts, detect risks, and ensure compliance.",
      },
      {
        name: "Contract Review Agent",
        desc: "Review agreements, highlight key clauses, and identify negotiation points.",
      },
      {
        name: "Compliance Agent",
        desc: "Check documents and processes against internal rules and compliance requirements.",
      },
      {
        name: "Risk Detection Agent",
        desc: "Detect operational, legal, and contractual risks before they become costly.",
      },
    ],
  },
  {
    title: "Finance AI Agents",
    description: "Automate financial reporting, expense analysis, and decision support.",
    agents: [
      {
        name: "Finance AI Agent",
        desc: "Automate financial analysis and generate internal reports.",
      },
      {
        name: "Expense Optimization Agent",
        desc: "Detect unnecessary spending and suggest cost-saving opportunities.",
      },
      {
        name: "Cashflow Forecast Agent",
        desc: "Forecast cashflow trends and identify future liquidity risks.",
      },
      {
        name: "Financial Reporting Agent",
        desc: "Generate summaries, dashboards, and financial insights from business data.",
      },
    ],
  },
  {
    title: "HR AI Agents",
    description: "Improve hiring, screening, and employee management workflows.",
    agents: [
      {
        name: "HR AI Agent",
        desc: "Screen CVs and streamline recruitment.",
      },
      {
        name: "CV Screening Agent",
        desc: "Rank candidates based on role requirements, skills, and experience.",
      },
      {
        name: "Interview Assistant Agent",
        desc: "Generate interview questions and summarize candidate evaluations.",
      },
      {
        name: "Employee Performance Agent",
        desc: "Analyze employee feedback, performance notes, and development plans.",
      },
    ],
  },
  {
    title: "Business AI Agents",
    description: "Help leadership teams analyze data, monitor KPIs, and make better decisions.",
    agents: [
      {
        name: "Business Decision Agent",
        desc: "Analyze business data and support strategic decisions.",
      },
      {
        name: "Market Analysis Agent",
        desc: "Analyze market signals, competitors, and opportunities.",
      },
      {
        name: "KPI Monitoring Agent",
        desc: "Track business KPIs and highlight performance changes.",
      },
      {
        name: "Strategy Recommendation Agent",
        desc: "Generate strategic recommendations based on business data and goals.",
      },
    ],
  },
  {
    title: "Document AI Agents",
    description: "Process documents, invoices, reports, and operational files faster.",
    agents: [
      {
        name: "Document Analysis Agent",
        desc: "Extract key information from documents and summarize important points.",
      },
      {
        name: "Invoice Processing Agent",
        desc: "Read invoices, extract totals, detect anomalies, and support accounting workflows.",
      },
    ],
  },
  {
    title: "Sales & Marketing AI Agents",
    description: "Support growth teams with customer, sales, and campaign intelligence.",
    agents: [
      {
        name: "Sales Insights Agent",
        desc: "Analyze sales data, detect opportunities, and support pipeline decisions.",
      },
      {
        name: "Customer Behavior Agent",
        desc: "Understand customer patterns and identify growth opportunities.",
      },
    ],
  },
];

export default function EnterprisePage() {
  return (
    <main className="min-h-screen bg-slate-50 text-slate-900 px-6 py-16">

      {/* HERO */}
      <section className="max-w-5xl mx-auto text-center space-y-6">
        <h1 className="text-4xl font-bold">
          Runexa for Business
        </h1>

        <p className="text-lg text-slate-600">
          Custom AI agents built for your company.
        </p>

        <p className="text-slate-600 max-w-2xl mx-auto">
          We design AI agents tailored to your workflows, data, and business needs — helping your teams analyze faster, reduce risks, and make better decisions.
        </p>

        <div className="flex justify-center gap-4 pt-4">
          <Link href="/contact-entreprise/contact" className="px-6 py-3 bg-blue-600 text-white rounded-xl font-semibold">
            Request a demo
          </Link>

          <Link href="/contact-entreprise/contact" className="px-6 py-3 border rounded-xl font-semibold">
            Contact sales
          </Link>
        </div>
      </section>

      {/* BENEFITS */}
      <section className="max-w-5xl mx-auto mt-20 grid md:grid-cols-2 gap-6 text-sm text-slate-600">
        <div>✔ Reduce manual work</div>
        <div>✔ Improve decision quality</div>
        <div>✔ Scale operations with AI</div>
        <div>✔ Centralize analysis across teams</div>
      </section>

      {/* AGENTS */}
      <section className="max-w-6xl mx-auto mt-20">
        <h2 className="text-2xl font-bold text-center mb-4">
          What we build for your business
        </h2>

        <p className="text-center text-slate-600 max-w-3xl mx-auto mb-10">
          Runexa Systems builds custom AI agents for legal, finance, HR, business, document processing, sales, and marketing workflows.
        </p>

        <div className="space-y-10">
          {agentCategories.map((category) => (
            <div key={category.title} className="bg-white rounded-3xl border p-6 shadow-sm">
              <div className="mb-6">
                <h3 className="text-xl font-semibold text-slate-900">
                  {category.title}
                </h3>

                <p className="text-sm text-slate-600 mt-2">
                  {category.description}
                </p>
              </div>

              <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                {category.agents.map((agent) => (
                  <div key={agent.name} className="rounded-2xl border bg-slate-50 p-5">
                    <h4 className="font-semibold text-slate-900">
                      {agent.name}
                    </h4>

                    <p className="text-sm text-slate-600 mt-3">
                      {agent.desc}
                    </p>

                    <span className="inline-block mt-4 rounded-full bg-blue-50 px-3 py-1 text-xs font-medium text-blue-700 border border-blue-100">
                      Custom agent
                    </span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* CUSTOM */}
      <section className="max-w-5xl mx-auto mt-20 text-center space-y-4">
        <h2 className="text-2xl font-bold">
          We build AI agents tailored to your business
        </h2>

        <p className="text-slate-600">
          Each company is different. That’s why we create custom AI agents adapted to your data, workflows, and internal processes.
        </p>
      </section>

      {/* HOW IT WORKS */}
      <section className="max-w-5xl mx-auto mt-20">
        <h2 className="text-2xl font-bold text-center mb-10">
          How it works
        </h2>

        <div className="grid md:grid-cols-4 gap-6 text-sm text-slate-600 text-center">
          <div className="bg-white rounded-2xl border p-5">Understand your needs</div>
          <div className="bg-white rounded-2xl border p-5">Build your agents</div>
          <div className="bg-white rounded-2xl border p-5">Deploy & integrate</div>
          <div className="bg-white rounded-2xl border p-5">Scale with AI</div>
        </div>
      </section>

      {/* FEATURES */}
      <section className="max-w-5xl mx-auto mt-20">
        <h2 className="text-2xl font-bold text-center mb-10">
          Enterprise features
        </h2>

        <div className="grid md:grid-cols-2 gap-4 text-sm text-slate-600">
          <div>✔ Multi-user access</div>
          <div>✔ Team management</div>
          <div>✔ Secure data processing</div>
          <div>✔ Custom dashboards</div>
          <div>✔ API access</div>
          <div>✔ Priority support</div>
        </div>
      </section>

      {/* CTA */}
      <section className="max-w-4xl mx-auto mt-20 bg-blue-600 text-white rounded-3xl p-10 text-center">
        <h2 className="text-2xl font-bold">
          Ready to bring AI into your business?
        </h2>

        <p className="mt-3 text-blue-100">
          Let’s build your custom AI agents.
        </p>

        <Link href="/contact-entreprise/contact" className="inline-block mt-6 px-6 py-3 bg-white text-blue-600 rounded-xl font-semibold">
          Get started
        </Link>
      </section>

    </main>
  );
}