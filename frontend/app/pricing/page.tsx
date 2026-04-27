import Link from "next/link";

export default function PricingPage() {
  return (
    <main className="min-h-screen bg-slate-50 px-6 py-20">
      <div className="mx-auto max-w-6xl space-y-16">
        
        {/* HEADER */}
        <div className="text-center max-w-2xl mx-auto">
          <p className="text-sm font-semibold text-blue-600">
            Pricing
          </p>

          <h1 className="mt-4 text-4xl font-bold text-slate-950">
            Simple, transparent pricing
          </h1>

          <p className="mt-4 text-slate-600">
            Start free and scale as you grow. Runexa begins with the AI Legal
            Agent — more specialized agents are coming soon.
          </p>
        </div>

        {/* CARDS */}
        <div className="grid gap-8 md:grid-cols-3">
          
          {/* FREE */}
          <div className="rounded-3xl border bg-white p-8 shadow-sm flex flex-col">
            <h2 className="text-lg font-semibold text-slate-900">Free</h2>

            <p className="mt-2 text-sm text-slate-500">
              Get started and explore the Legal Agent.
            </p>

            <div className="mt-6 text-4xl font-bold text-slate-900">
              €0
            </div>

            <p className="text-sm text-slate-500">
              1 contract analysis
            </p>

            <ul className="mt-6 space-y-3 text-sm text-slate-700">
              <li>✔ AI Legal Agent access</li>
              <li>✔ Contract summary</li>
              <li>✔ Risk detection</li>
              <li>✔ Simplified explanation</li>
              <li>✔ EN / FR / AR support</li>
            </ul>

            <Link
              href="/register"
              className="mt-auto block rounded-xl bg-slate-900 px-5 py-3 text-center font-semibold text-white hover:bg-slate-800 transition"
            >
              Start for free
            </Link>
          </div>

          {/* PAY PER USE */}
          <div className="relative rounded-3xl border-2 border-blue-600 bg-white p-8 shadow-lg flex flex-col">

            <span className="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full bg-blue-600 px-3 py-1 text-xs font-semibold text-white">
              Most popular
            </span>

            <h2 className="text-lg font-semibold text-slate-900">
              Pay per contract
            </h2>

            <p className="mt-2 text-sm text-slate-500">
              Ideal for freelancers and growing teams.
            </p>

            <div className="mt-6 text-4xl font-bold text-slate-900">
              €5
            </div>

            <p className="text-sm text-slate-500">
              per contract analysis
            </p>

            <ul className="mt-6 space-y-3 text-sm text-slate-700">
              <li>✔ Everything in Free</li>
              <li>✔ Full contract analysis</li>
              <li>✔ Risk score</li>
              <li>✔ Clause-by-clause insights</li>
              <li>✔ Clear recommendations</li>
            </ul>

            <Link
              href="/upload"
              className="mt-auto block rounded-xl bg-blue-600 px-5 py-3 text-center font-semibold text-white hover:bg-blue-700 transition"
            >
              Analyze a contract
            </Link>
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

            <p className="text-sm text-slate-500">
              tailored pricing
            </p>

            <ul className="mt-6 space-y-3 text-sm text-slate-700">
              <li>✔ Multiple users</li>
              <li>✔ Higher usage limits</li>
              <li>✔ Admin dashboard</li>
              <li>✔ Future AI agents access</li>
              <li>✔ Priority support</li>
            </ul>

            <a
              href="mailto:contact@runexa.ai"
              className="mt-auto block rounded-xl border px-5 py-3 text-center font-semibold text-slate-900 hover:bg-slate-100 transition"
            >
              Contact sales
            </a>
          </div>
        </div>

        {/* DISCLAIMER */}
        <div className="mx-auto max-w-3xl rounded-2xl border border-amber-200 bg-amber-50 p-5 text-center text-sm text-amber-800">
          ⚠️ Runexa does not replace a lawyer. The AI Legal Agent provides
          contract understanding and risk insights for informational purposes only.
        </div>

      </div>
    </main>
  );
}