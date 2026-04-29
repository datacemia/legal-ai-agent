"use client";

import Link from "next/link";
import { useState } from "react";

export default function Pricing() {
  const [message, setMessage] = useState("");

  const handleStartFree = () => {
    const token = localStorage.getItem("token");

    if (!token) {
      window.location.href = "/register";
      return;
    }

    window.location.href = "/upload";
  };

  const handleBuyCredits = () => {
    const token = localStorage.getItem("token");

    if (!token) {
      window.location.href = "/register";
      return;
    }

    setMessage("Payment is not configured yet.");
  };

  return (
    <main className="bg-white">
      <div className="mx-auto max-w-6xl px-6 py-20">
        <div className="mx-auto max-w-2xl text-center">
          <h1 className="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
            Simple pricing
          </h1>
          <p className="mt-4 text-slate-600">
            Start with the Legal Agent. More specialized agents are coming soon, each with clear and transparent pricing.
          </p>
        </div>

        {/* NEW SECTION TITLE */}
        <div className="text-center mt-16">
          <h2 className="text-xl font-semibold text-slate-900">
            Legal Agent Pricing
          </h2>
          <p className="mt-2 text-sm text-slate-500">
            Analyze contracts, detect risky clauses, and get clear recommendations before you sign.
          </p>
        </div>

        <div className="grid gap-8 md:grid-cols-3 mt-12">

          {/* FREE */}
          <div className="rounded-3xl border bg-white p-8 shadow-sm flex flex-col">
            <h2 className="text-lg font-semibold text-slate-900">Free</h2>

            <span className="mt-2 text-xs text-slate-500">
              Limited preview
            </span>

            <p className="mt-2 text-sm text-slate-500">
              Get started and explore the Legal Agent.
            </p>

            <div className="mt-6 text-4xl font-bold text-slate-900">€0</div>

            <p className="text-sm text-slate-500">1 contract analysis</p>

            <ul className="mt-6 space-y-3 text-sm text-slate-700">
              <li>✔ AI Legal Agent access</li>
              <li>✔ Contract summary</li>
              <li>✔ Risk score</li>
              <li>✔ Full simplified version</li>
              <li>✔ Full contract analysis</li>
              <li className="text-slate-400">✖ Only 2 clauses displayed</li>
              <li className="text-slate-400">
                ✖ Recommendations for 2 clauses
              </li>
            </ul>

            <button
              onClick={handleStartFree}
              className="mt-auto block rounded-xl bg-slate-900 px-5 py-3 text-center font-semibold text-white hover:bg-slate-800 transition"
            >
              Start for free
            </button>
          </div>

          {/* PAY PER USE */}
          <div className="relative rounded-3xl border-2 border-blue-600 bg-white p-8 shadow-lg flex flex-col">
            <span className="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full bg-blue-600 px-3 py-1 text-xs font-semibold text-white">
              Most popular
            </span>

            <h2 className="text-lg font-semibold text-slate-900">
              Pay per contract
            </h2>

            <span className="mt-2 text-xs text-blue-600 font-medium">
              Full access
            </span>

            <p className="mt-2 text-sm text-slate-500">
              Ideal for freelancers and growing teams.
            </p>

            <div className="mt-6 text-4xl font-bold text-slate-900">€5</div>

            <p className="text-sm text-slate-500">
              per contract analysis
            </p>

            <ul className="mt-6 space-y-3 text-sm text-slate-700">
              <li>✔ Everything in Free</li>
              <li>✔ All clauses displayed</li>
              <li>✔ Recommendations for all clauses</li>
            </ul>

            <button
              onClick={handleBuyCredits}
              className="mt-auto block rounded-xl bg-blue-600 px-5 py-3 text-center font-semibold text-white hover:bg-blue-700 transition"
            >
              Buy credits
            </button>

            {message && (
              <div className="mt-4 rounded-xl border border-red-200 bg-red-50 p-3 text-center text-sm text-red-700">
                {message}
              </div>
            )}
          </div>

          {/* BUSINESS */}
          <div className="rounded-3xl border bg-white p-8 shadow-sm flex flex-col">
            <h2 className="text-lg font-semibold text-slate-900">
              Business
            </h2>

            <p className="mt-2 text-sm text-slate-500">
              For teams and companies with advanced needs.
            </p>

            <div className="mt-6 text-4xl font-bold text-slate-900">
              Custom
            </div>

            <p className="text-sm text-slate-500">tailored pricing</p>

            <ul className="mt-6 space-y-3 text-sm text-slate-700">
              <li>✔ Multiple users</li>
              <li>✔ Higher usage limits</li>
              <li>✔ Admin dashboard</li>
              <li>✔ Future AI agents access</li>
              <li>✔ Priority support</li>
            </ul>

            <a
              href="/contact"
              className="mt-auto block rounded-xl border px-5 py-3 text-center font-semibold text-slate-900 hover:bg-slate-100 transition"
            >
              Contact sales
            </a>
          </div>

        </div>

        <div className="mx-auto max-w-3xl rounded-2xl border border-amber-200 bg-amber-50 p-5 text-center text-sm text-amber-800 mt-16">
          ⚠️ Runexa does not replace a lawyer. The AI Legal Agent provides
          contract understanding and risk insights for informational purposes
          only.
        </div>
      </div>
    </main>
  );
}