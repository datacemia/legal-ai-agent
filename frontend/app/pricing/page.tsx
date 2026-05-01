"use client";

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
            Start with the Legal Agent. More specialized agents are coming soon,
            each with clear and transparent pricing.
          </p>
        </div>

        {/* LEGAL AGENT SECTION */}
        <div className="text-center mt-16">
          <h2 className="text-xl font-semibold text-slate-900">
            Legal Agent Pricing
          </h2>
          <p className="mt-2 text-sm text-slate-500">
            Analyze contracts, detect risky clauses, and get clear
            recommendations before you sign.
          </p>
        </div>

        <div className="grid gap-8 md:grid-cols-4 mt-12">
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

            <p className="text-sm text-slate-500">per contract analysis</p>

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

          {/* PRO */}
          <div className="rounded-3xl border bg-white p-8 shadow-sm flex flex-col">
            <h2 className="text-lg font-semibold text-slate-900">Pro</h2>

            <span className="mt-2 text-xs text-slate-500">
              For professionals
            </span>

            <p className="mt-2 text-sm text-slate-500">
              Best for users who analyze contracts regularly.
            </p>

            <div className="mt-6 text-4xl font-bold text-slate-900">€19</div>

            <p className="text-sm text-slate-500">per month</p>

            <ul className="mt-6 space-y-3 text-sm text-slate-700">
              <li>✔ Everything in Pay per contract</li>
              <li>✔ 20 contract analyses per month</li>
              <li>✔ Full clause recommendations</li>
              <li>✔ Priority processing</li>
            </ul>

            <button
              onClick={handleBuyCredits}
              className="mt-auto block rounded-xl bg-slate-900 px-5 py-3 text-center font-semibold text-white hover:bg-slate-800 transition"
            >
              Upgrade to Pro
            </button>
          </div>

          {/* PREMIUM */}
          <div className="rounded-3xl border bg-white p-8 shadow-sm flex flex-col">
            <h2 className="text-lg font-semibold text-slate-900">Premium</h2>

            <p className="mt-2 text-sm text-slate-500">
              For teams and companies with advanced needs.
            </p>

            <div className="mt-6 text-4xl font-bold text-slate-900">
              Custom
            </div>

            <p className="text-sm text-slate-500">tailored pricing</p>

            <ul className="mt-6 space-y-3 text-sm text-slate-700">
              <li>✔ Multiple users</li>
              <li>✔ Custom usage limits</li>
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

        {/* LEGAL DISCLAIMER */}
        <div className="mx-auto max-w-3xl rounded-2xl border border-amber-200 bg-amber-50 p-5 text-center text-sm text-amber-800 mt-16">
          ⚠️ Runexa does not replace a lawyer. The AI Legal Agent provides
          contract understanding and risk information for informational purposes
          only.
        </div>

        {/* FINANCE AGENT SECTION */}
        <div className="text-center mt-20">
          <h2 className="text-xl font-semibold text-slate-900">
            Finance Agent Pricing
          </h2>
          <p className="mt-2 text-sm text-slate-500">
            Analyze bank statements, detect spending patterns, and get clear
            financial insights.
          </p>
        </div>

        <div className="grid gap-8 md:grid-cols-4 mt-12">
          {/* FREE */}
          <div className="rounded-3xl border bg-white p-8 shadow-sm flex flex-col">
            <h2 className="text-lg font-semibold text-slate-900">Free</h2>

            <span className="mt-2 text-xs text-slate-500">
              Limited preview
            </span>

            <p className="mt-2 text-sm text-slate-500">
              Explore the Finance Agent.
            </p>

            <div className="mt-6 text-4xl font-bold text-slate-900">€0</div>

            <p className="text-sm text-slate-500">1 statement analysis</p>

            <ul className="mt-6 space-y-3 text-sm text-slate-700">
              <li>✔ AI Finance Agent access</li>
              <li>✔ Spending summary</li>
              <li>✔ Financial score</li>
              <li className="text-slate-400">✖ Limited recommendations</li>
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
              Pay per statement
            </h2>

            <span className="mt-2 text-xs text-blue-600 font-medium">
              Full access
            </span>

            <p className="mt-2 text-sm text-slate-500">
              Ideal for personal finance tracking.
            </p>

            <div className="mt-6 text-4xl font-bold text-slate-900">€3</div>

            <p className="text-sm text-slate-500">per statement analysis</p>

            <ul className="mt-6 space-y-3 text-sm text-slate-700">
              <li>✔ Everything in Free</li>
              <li>✔ Full spending breakdown</li>
              <li>✔ All categories</li>
              <li>✔ Full recommendations</li>
            </ul>

            <button
              onClick={handleBuyCredits}
              className="mt-auto block rounded-xl bg-blue-600 px-5 py-3 text-center font-semibold text-white hover:bg-blue-700 transition"
            >
              Buy credits
            </button>
          </div>

          {/* PRO */}
          <div className="rounded-3xl border bg-white p-8 shadow-sm flex flex-col">
            <h2 className="text-lg font-semibold text-slate-900">Pro</h2>

            <span className="mt-2 text-xs text-slate-500">
              For regular users
            </span>

            <p className="mt-2 text-sm text-slate-500">
              Best for tracking finances monthly.
            </p>

            <div className="mt-6 text-4xl font-bold text-slate-900">€15</div>

            <p className="text-sm text-slate-500">per month</p>

            <ul className="mt-6 space-y-3 text-sm text-slate-700">
              <li>✔ Everything in Pay per statement</li>
              <li>✔ 20 analyses per month</li>
              <li>✔ Advanced insights</li>
              <li>✔ Priority processing</li>
            </ul>

            <button
              onClick={handleBuyCredits}
              className="mt-auto block rounded-xl bg-slate-900 px-5 py-3 text-center font-semibold text-white hover:bg-slate-800 transition"
            >
              Upgrade to Pro
            </button>
          </div>

          {/* PREMIUM */}
          <div className="rounded-3xl border bg-white p-8 shadow-sm flex flex-col">
            <h2 className="text-lg font-semibold text-slate-900">Premium</h2>

            <p className="mt-2 text-sm text-slate-500">
              For teams and advanced users.
            </p>

            <div className="mt-6 text-4xl font-bold text-slate-900">
              Custom
            </div>

            <p className="text-sm text-slate-500">tailored pricing</p>

            <ul className="mt-6 space-y-3 text-sm text-slate-700">
              <li>✔ Multiple users</li>
              <li>✔ Custom limits</li>
              <li>✔ Future AI agents</li>
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

        {/* FINANCE DISCLAIMER */}
        <div className="mx-auto max-w-3xl rounded-2xl border border-amber-200 bg-amber-50 p-5 text-center text-sm text-amber-800 mt-16">
          ⚠️ Runexa does not replace a financial advisor. The AI Finance Agent
          provides financial insights for informational purposes only.
        </div>

        {/* STUDY AGENT SECTION */}
        <div className="text-center mt-20">
          <h2 className="text-xl font-semibold text-slate-900">
            Study Agent Pricing
          </h2>
          <p className="mt-2 text-sm text-slate-500">
            Transform your study materials into summaries, quizzes, flashcards,
            and personalized learning plans.
          </p>
        </div>

        <div className="grid gap-8 md:grid-cols-4 mt-12">
          {/* FREE */}
          <div className="rounded-3xl border bg-white p-8 shadow-sm flex flex-col">
            <h2 className="text-lg font-semibold text-slate-900">Free</h2>

            <span className="mt-2 text-xs text-slate-500">
              Limited preview
            </span>

            <p className="mt-2 text-sm text-slate-500">
              Discover how the Study Agent helps you learn faster.
            </p>

            <div className="mt-6 text-4xl font-bold text-slate-900">€0</div>

            <p className="text-sm text-slate-500">1 study analysis</p>

            <ul className="mt-6 space-y-3 text-sm text-slate-700">
              <li>✔ Summary</li>
              <li>✔ Key learning points</li>
              <li className="text-slate-400">✖ Full quiz (limited)</li>
              <li className="text-slate-400">✖ Flashcards</li>
              <li className="text-slate-400">✖ Study plan</li>
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
              Pay per study
            </h2>

            <span className="mt-2 text-xs text-blue-600 font-medium">
              Full learning experience
            </span>

            <p className="mt-2 text-sm text-slate-500">
              Ideal for occasional study sessions.
            </p>

            <div className="mt-6 text-4xl font-bold text-slate-900">€2</div>

            <p className="text-sm text-slate-500">per analysis</p>

            <ul className="mt-6 space-y-3 text-sm text-slate-700">
              <li>✔ Everything in Free</li>
              <li>✔ Full quiz (theory + practice)</li>
              <li>✔ Flashcards</li>
              <li>✔ Study plan</li>
            </ul>

            <button
              onClick={handleBuyCredits}
              className="mt-auto block rounded-xl bg-blue-600 px-5 py-3 text-center font-semibold text-white hover:bg-blue-700 transition"
            >
              Buy credits
            </button>
          </div>

          {/* STUDENT PRO */}
          <div className="rounded-3xl border bg-white p-8 shadow-sm flex flex-col">
            <h2 className="text-lg font-semibold text-slate-900">
              Student Pro
            </h2>

            <span className="mt-2 text-xs text-slate-500">
              For regular learners
            </span>

            <p className="mt-2 text-sm text-slate-500">
              Best for students who study frequently.
            </p>

            <div className="mt-6 text-4xl font-bold text-slate-900">€9</div>

            <p className="text-sm text-slate-500">per month</p>

            <ul className="mt-6 space-y-3 text-sm text-slate-700">
              <li>✔ 30 analyses per month</li>
              <li>✔ Full quiz access</li>
              <li>✔ Flashcards & study plans</li>
              <li>✔ Quiz retry & feedback</li>
              <li>✔ Faster processing</li>
            </ul>

            <button
              onClick={handleBuyCredits}
              className="mt-auto block rounded-xl bg-slate-900 px-5 py-3 text-center font-semibold text-white hover:bg-slate-800 transition"
            >
              Upgrade to Pro
            </button>
          </div>

          {/* PREMIUM */}
          <div className="rounded-3xl border bg-white p-8 shadow-sm flex flex-col">
            <h2 className="text-lg font-semibold text-slate-900">Premium</h2>

            <p className="mt-2 text-sm text-slate-500">
              For advanced users and multi-agent access.
            </p>

            <div className="mt-6 text-4xl font-bold text-slate-900">
              Custom
            </div>

            <p className="text-sm text-slate-500">tailored pricing</p>

            <ul className="mt-6 space-y-3 text-sm text-slate-700">
              <li>✔ Multi-agents access</li>
              <li>✔ Learning dashboard (future)</li>
              <li>✔ Progress tracking</li>
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

        {/* STUDY DISCLAIMER */}
        <div className="mx-auto max-w-3xl rounded-2xl border border-amber-200 bg-amber-50 p-5 text-center text-sm text-amber-800 mt-16">
          ⚠️ The Study Agent is for educational support only. Always verify
          important academic content with your teacher or official materials.
        </div>

        {/* BUSINESS AGENT SECTION */}
        <div className="text-center mt-20">
          <h2 className="text-xl font-semibold text-slate-900">
            Business Decision Agent Pricing
          </h2>
          <p className="mt-2 text-sm text-slate-500">
            Analyze business data, detect trends, and get clear strategic action plans.
          </p>
        </div>

        <div className="grid gap-8 md:grid-cols-4 mt-12">
          {/* FREE */}
          <div className="rounded-3xl border bg-white p-8 shadow-sm flex flex-col">
            <h2 className="text-lg font-semibold text-slate-900">Free</h2>

            <span className="mt-2 text-xs text-slate-500">
              Limited preview
            </span>

            <p className="mt-2 text-sm text-slate-500">
              Discover how the Business Agent works.
            </p>

            <div className="mt-6 text-4xl font-bold text-slate-900">€0</div>

            <p className="text-sm text-slate-500">1 business analysis</p>

            <ul className="mt-6 space-y-3 text-sm text-slate-700">
              <li>✔ Business summary</li>
              <li>✔ Basic metrics (revenue, expenses)</li>
              <li className="text-slate-400">✖ Limited insights</li>
              <li className="text-slate-400">✖ No action plan</li>
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
              Most valuable
            </span>

            <h2 className="text-lg font-semibold text-slate-900">
              Pay per analysis
            </h2>

            <span className="mt-2 text-xs text-blue-600 font-medium">
              Full strategic insights
            </span>

            <p className="mt-2 text-sm text-slate-500">
              Ideal for entrepreneurs and small businesses.
            </p>

            <div className="mt-6 text-4xl font-bold text-slate-900">€7</div>

            <p className="text-sm text-slate-500">per analysis</p>

            <ul className="mt-6 space-y-3 text-sm text-slate-700">
              <li>✔ Everything in Free</li>
              <li>✔ Full business metrics</li>
              <li>✔ Risks detection</li>
              <li>✔ Opportunities</li>
              <li>✔ Action plan</li>
            </ul>

            <button
              onClick={handleBuyCredits}
              className="mt-auto block rounded-xl bg-blue-600 px-5 py-3 text-center font-semibold text-white hover:bg-blue-700 transition"
            >
              Buy credits
            </button>
          </div>

          {/* PRO */}
          <div className="rounded-3xl border bg-white p-8 shadow-sm flex flex-col">
            <h2 className="text-lg font-semibold text-slate-900">Pro</h2>

            <span className="mt-2 text-xs text-slate-500">
              For regular business tracking
            </span>

            <p className="mt-2 text-sm text-slate-500">
              Best for founders and growing teams.
            </p>

            <div className="mt-6 text-4xl font-bold text-slate-900">€25</div>

            <p className="text-sm text-slate-500">per month</p>

            <ul className="mt-6 space-y-3 text-sm text-slate-700">
              <li>✔ Everything in Pay per analysis</li>
              <li>✔ 30 analyses per month</li>
              <li>✔ Advanced insights</li>
              <li>✔ Priority processing</li>
            </ul>

            <button
              onClick={handleBuyCredits}
              className="mt-auto block rounded-xl bg-slate-900 px-5 py-3 text-center font-semibold text-white hover:bg-slate-800 transition"
            >
              Upgrade to Pro
            </button>
          </div>

          {/* PREMIUM */}
          <div className="rounded-3xl border bg-white p-8 shadow-sm flex flex-col">
            <h2 className="text-lg font-semibold text-slate-900">Premium</h2>

            <p className="mt-2 text-sm text-slate-500">
              For companies and advanced analytics needs.
            </p>

            <div className="mt-6 text-4xl font-bold text-slate-900">
              Custom
            </div>

            <p className="text-sm text-slate-500">tailored pricing</p>

            <ul className="mt-6 space-y-3 text-sm text-slate-700">
              <li>✔ Multi-user access</li>
              <li>✔ Custom limits</li>
              <li>✔ Business dashboards (future)</li>
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

        {/* BUSINESS DISCLAIMER */}
        <div className="mx-auto max-w-3xl rounded-2xl border border-amber-200 bg-amber-50 p-5 text-center text-sm text-amber-800 mt-16">
          ⚠️ The Business Agent provides decision support insights. Always verify important decisions with a qualified professional.
        </div>

      </div>
    </main>
  );
}