"use client";

import { useState } from "react";

const agents = [
  {
    slug: "legal",
    name: "Legal Agent",
    description: "Contracts, risky clauses, obligations, and recommendations.",
    credits: 12,
    gradient: "from-slate-950 to-blue-700",
  },
  {
    slug: "finance",
    name: "Finance Agent",
    description: "Bank statements, spending patterns, waste, and savings.",
    credits: 7,
    gradient: "from-emerald-700 to-teal-500",
  },
  {
    slug: "study",
    name: "Study Agent",
    description: "Summaries, quizzes, flashcards, audio, and study plans.",
    credits: 5,
    gradient: "from-indigo-700 to-violet-500",
  },
  {
    slug: "business",
    name: "Business Agent",
    description: "Business data, risks, opportunities, and action plans.",
    credits: 30,
    gradient: "from-amber-700 to-orange-500",
  },
];

const creditPacks = [
  {
    name: "Starter",
    credits: 50,
    price: "€9",
    description: "Perfect for testing multiple Runexa agents.",
  },
  {
    name: "Growth",
    credits: 150,
    price: "€24",
    description: "Best value for regular multi-agent usage.",
    highlighted: true,
  },
  {
    name: "Scale",
    credits: 500,
    price: "€89",
    description: "Built for professionals and advanced workloads.",
  },
];

export default function Pricing() {
  const [message, setMessage] = useState("");

  const requireAuth = () => {
    const token = localStorage.getItem("token");

    if (!token) {
      window.location.href = "/register";
      return false;
    }

    return true;
  };

  const handleStartTrial = (agentSlug: string) => {
    if (!requireAuth()) return;

    setMessage(
      `$1 trial payment for ${agentSlug} is not configured yet. Stripe integration will be activated soon.`
    );
  };

  const handleBuyCredits = () => {
    if (!requireAuth()) return;

    setMessage(
      "Stripe is not configured yet. Global credits will be available soon."
    );
  };

  const handleUpgradePro = () => {
    if (!requireAuth()) return;

    setMessage(
      "Pro subscription is not configured yet. Stripe will be activated soon."
    );
  };

  return (
    <main className="min-h-screen bg-white text-slate-950">
      <section className="relative overflow-hidden border-b border-slate-200 bg-gradient-to-br from-slate-950 via-blue-950 to-slate-900">
        <div className="absolute left-1/2 top-0 h-72 w-72 -translate-x-1/2 rounded-full bg-blue-500/20 blur-3xl" />
        <div className="absolute bottom-0 right-10 h-72 w-72 rounded-full bg-cyan-400/10 blur-3xl" />

        <div className="relative mx-auto max-w-6xl px-6 py-20 text-center sm:py-24">
          <span className="inline-flex rounded-full border border-white/15 bg-white/10 px-4 py-2 text-sm font-semibold text-blue-100 backdrop-blur">
            Global pricing for every Runexa AI agent
          </span>

          <h1 className="mx-auto mt-7 max-w-4xl text-4xl font-bold tracking-tight text-white sm:text-6xl">
            One account. All agents. Simple global billing.
          </h1>

          <p className="mx-auto mt-6 max-w-3xl text-lg leading-8 text-blue-100">
            One Runexa account gives access to all agents. Activate any agent
            with a one-time $1 trial, or skip trials and continue with global
            credits or a Pro/Premium plan.
          </p>

          <div className="mt-10 flex flex-col items-center justify-center gap-3 sm:flex-row">
            <a
              href="#trials"
              className="w-full rounded-xl bg-white px-6 py-3 text-center text-sm font-bold text-slate-950 shadow-lg shadow-blue-950/30 transition hover:bg-blue-50 sm:w-auto"
            >
              Activate any agent with a one-time $1 trial
            </a>

            <a
              href="#plans"
              className="w-full rounded-xl border border-white/20 bg-white/10 px-6 py-3 text-center text-sm font-bold text-white backdrop-blur transition hover:bg-white/15 sm:w-auto"
            >
              View Pro & Premium
            </a>
          </div>
        </div>
      </section>

      <div className="mx-auto max-w-6xl px-6 py-16">
        {message && (
          <div className="mb-8 rounded-2xl border border-amber-200 bg-amber-50 px-5 py-4 text-center text-sm font-medium text-amber-800">
            {message}
          </div>
        )}

        <section id="trials" className="space-y-8">
          <div className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
            <div>
              <p className="text-sm font-bold uppercase tracking-[0.25em] text-blue-600">
                Section 1
              </p>
              <h2 className="mt-2 text-3xl font-bold tracking-tight">
                $1 Trials by Agent
              </h2>
              <p className="mt-3 max-w-2xl text-slate-600">
                Each agent has its own one-time $1 activation. Try exactly the
                agent you need before using global credits or a plan.
              </p>
            </div>

            <div className="rounded-2xl border border-blue-100 bg-blue-50 px-4 py-3 text-sm font-semibold text-blue-700">
              $1 trial per agent · one-time activation
            </div>
          </div>

          <div className="grid gap-5 md:grid-cols-4">
            {agents.map((agent) => (
              <div
                key={agent.slug}
                className="group overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm transition hover:-translate-y-1 hover:shadow-xl"
              >
                <div className={`h-2 bg-gradient-to-r ${agent.gradient}`} />

                <div className="flex h-full flex-col p-6">
                  <div
                    className={`mb-5 flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br ${agent.gradient} text-sm font-bold text-white shadow-lg`}
                  >
                    AI
                  </div>

                  <h3 className="text-lg font-bold text-slate-950">
                    {agent.name}
                  </h3>

                  <p className="mt-2 min-h-[72px] text-sm leading-6 text-slate-600">
                    {agent.description}
                  </p>

                  <div className="mt-5">
                    <span className="text-4xl font-bold">$1</span>
                    <span className="ml-2 text-sm text-slate-500">
                      one-time trial
                    </span>
                  </div>

                  <p className="mt-2 text-sm text-slate-500">
                    1 trial analysis for this agent
                  </p>

                  <button
                    onClick={() => handleStartTrial(agent.slug)}
                    className="mt-6 rounded-xl bg-slate-950 px-5 py-3 text-sm font-bold text-white transition hover:bg-slate-800"
                  >
                    Start {agent.name.split(" ")[0]} Trial
                  </button>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="mt-20 space-y-8">
          <div>
            <p className="text-sm font-bold uppercase tracking-[0.25em] text-blue-600">
              Section 2
            </p>
            <div className="mt-2 flex flex-wrap items-center gap-3">
              <h2 className="text-3xl font-bold tracking-tight">
                Global Credits
              </h2>
              <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-bold text-emerald-700 ring-1 ring-emerald-100">
                Most flexible
              </span>
            </div>
            <p className="mt-3 max-w-2xl text-slate-600">
              Buy credits once and use them on all Runexa agents. Credits are
              the flexible option for users who do not need a monthly plan.
            </p>
          </div>

          <div className="grid gap-6 md:grid-cols-3">
            {creditPacks.map((pack) => (
              <div
                key={pack.name}
                className={`relative rounded-3xl border bg-white p-8 shadow-sm ${
                  pack.highlighted
                    ? "border-blue-600 shadow-xl shadow-blue-100"
                    : "border-slate-200"
                }`}
              >
                {pack.highlighted && (
                  <span className="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full bg-blue-600 px-3 py-1 text-xs font-bold text-white">
                    Best value
                  </span>
                )}

                <h3 className="text-lg font-bold">{pack.name}</h3>
                <p className="mt-2 text-sm leading-6 text-slate-600">
                  {pack.description}
                </p>

                <div className="mt-6 flex items-end gap-2">
                  <span className="text-4xl font-bold">{pack.price}</span>
                  <span className="pb-1 text-sm text-slate-500">
                    one-time
                  </span>
                </div>

                <p className="mt-2 text-sm font-semibold text-slate-700">
                  {pack.credits} global credits
                </p>

                <button
                  onClick={handleBuyCredits}
                  className={`mt-7 w-full rounded-xl px-5 py-3 text-sm font-bold transition ${
                    pack.highlighted
                      ? "bg-blue-600 text-white hover:bg-blue-700"
                      : "bg-slate-950 text-white hover:bg-slate-800"
                  }`}
                >
                  Buy credits
                </button>
              </div>
            ))}
          </div>
        </section>

        <section id="plans" className="mt-20">
          <div>
            <p className="text-sm font-bold uppercase tracking-[0.25em] text-blue-600">
              Section 3
            </p>
            <h2 className="mt-2 text-3xl font-bold tracking-tight">
              Pro / Premium Plans
            </h2>
            <p className="mt-3 max-w-2xl text-slate-600">
              One global subscription covers all agents. No separate Pro plan
              per agent.
            </p>
          </div>

          <div className="mt-8 grid gap-6 lg:grid-cols-2">
            <div className="relative overflow-hidden rounded-3xl border-2 border-slate-950 bg-slate-950 p-8 text-white shadow-2xl shadow-slate-200">
              <div className="absolute right-0 top-0 h-48 w-48 rounded-full bg-blue-500/20 blur-3xl" />

              <div className="relative">
                <div className="flex flex-wrap gap-2">
                  <span className="rounded-full bg-white/10 px-3 py-1 text-xs font-bold text-blue-100">
                    Global Pro
                  </span>
                  <span className="rounded-full bg-blue-400/20 px-3 py-1 text-xs font-bold text-blue-100">
                    Best for professionals
                  </span>
                </div>

                <h3 className="mt-5 text-2xl font-bold">Pro</h3>
                <p className="mt-2 text-slate-300">
                  For individuals and professionals who use multiple agents regularly.
                </p>

                <div className="mt-7 flex items-end gap-2">
                  <span className="text-5xl font-bold">€49</span>
                  <span className="pb-2 text-slate-300">/month</span>
                </div>

                <ul className="mt-8 space-y-4 text-sm text-slate-100">
                  <li>✔ 200 credits/month</li>
                  <li>✔ Usable on all agents</li>
                  <li>✔ Priority processing</li>
                  <li>✔ Access to Legal, Study, Finance, and Business agents</li>
                  <li>✔ Future agents included when available</li>
                </ul>

                <button
                  onClick={handleUpgradePro}
                  className="mt-8 w-full rounded-xl bg-white px-5 py-3 text-sm font-bold text-slate-950 transition hover:bg-blue-50"
                >
                  Upgrade to Pro
                </button>
              </div>
            </div>

            <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
              <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-bold text-slate-700">
                Enterprise
              </span>

              <h3 className="mt-5 text-2xl font-bold">Premium</h3>
              <p className="mt-2 text-slate-600">
                For teams, companies, schools, and multi-user organizations.
              </p>

              <div className="mt-7 text-5xl font-bold">Custom</div>
              <p className="mt-2 text-sm text-slate-500">tailored pricing</p>

              <ul className="mt-8 space-y-4 text-sm text-slate-700">
                <li>✔ Team access</li>
                <li>✔ Custom credits</li>
                <li>✔ Admin dashboard</li>
                <li>✔ Future agents</li>
                <li>✔ Priority support</li>
              </ul>

              <a
                href="/contact"
                className="mt-8 block w-full rounded-xl border border-slate-300 px-5 py-3 text-center text-sm font-bold text-slate-950 transition hover:bg-slate-50"
              >
                Contact sales
              </a>
            </div>
          </div>
        </section>

        <section className="mt-20">
          <div className="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">
            <div className="border-b border-slate-200 bg-slate-50 p-6">
              <p className="text-sm font-bold uppercase tracking-[0.25em] text-blue-600">
                Section 4
              </p>
              <h2 className="mt-2 text-3xl font-bold tracking-tight">
                Agent credit costs
              </h2>
              <p className="mt-3 text-slate-600">
                Credits are global. The same balance works across every agent.
              </p>
            </div>

            <div className="divide-y divide-slate-100">
              {agents.map((agent) => (
                <div
                  key={agent.slug}
                  className="grid gap-4 p-6 sm:grid-cols-[1fr_auto] sm:items-center"
                >
                  <div>
                    <h3 className="font-bold text-slate-950">{agent.name}</h3>
                    <p className="mt-1 text-sm text-slate-500">
                      {agent.description}
                    </p>
                  </div>

                  <div className="rounded-2xl bg-slate-950 px-5 py-3 text-center text-sm font-bold text-white">
                    {agent.credits} credits / analysis
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="mt-16 grid gap-4 md:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-slate-50 p-5 text-sm text-slate-600">
            <strong className="block text-slate-950">Trials are optional</strong>
            You can activate a $1 trial for one agent or skip directly to
            credits or Pro.
          </div>

          <div className="rounded-2xl border border-slate-200 bg-slate-50 p-5 text-sm text-slate-600">
            <strong className="block text-slate-950">Credits are global</strong>
            Buy once and use the same balance for Legal, Study, Finance, or
            Business.
          </div>

          <div className="rounded-2xl border border-slate-200 bg-slate-50 p-5 text-sm text-slate-600">
            <strong className="block text-slate-950">Pro is global</strong>
            One monthly Pro plan includes credits usable across all agents.
          </div>
        </section>

        <div className="mt-16 rounded-2xl border border-amber-200 bg-amber-50 p-5 text-center text-sm text-amber-800">
          ⚠️ Runexa AI agents provide informational and decision-support output.
          Always verify important legal, financial, academic, or business
          decisions with qualified professionals or official sources.
        </div>
      </div>
    </main>
  );
}
