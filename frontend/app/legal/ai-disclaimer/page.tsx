export default function AIDisclaimerPage() {
  return (
    <main className="min-h-screen bg-slate-50 px-4 py-12">
      <div className="max-w-3xl mx-auto bg-white p-8 rounded-3xl border shadow-sm space-y-8">

        <div>
          <h1 className="text-3xl font-bold text-slate-900">
            AI Disclaimer & Transparency
          </h1>

          <p className="text-sm text-slate-500 mt-2">
            Last updated: May 2026
          </p>
        </div>

        <section>
          <h2 className="text-xl font-semibold">1. Overview</h2>

          <p className="mt-2 text-slate-600">
            Runexa Systems LLC provides AI-powered tools and agents designed to
            assist users with document analysis, learning support, financial
            insights, business analysis, and related tasks.
          </p>

          <p className="mt-2 text-slate-600">
            AI systems are probabilistic technologies and may produce inaccurate,
            incomplete, inconsistent, or misleading outputs.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">2. No Professional Advice</h2>

          <p className="mt-2 text-slate-600">
            Runexa AI agents do not provide legal, financial, accounting, tax,
            medical, investment, security, or other regulated professional
            advice.
          </p>

          <p className="mt-2 text-slate-600">
            AI-generated outputs should not be considered a substitute for
            qualified professionals or independent human judgment.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">3. AI Limitations</h2>

          <ul className="mt-2 list-disc pl-5 text-slate-600 space-y-2">
            <li>AI outputs may contain factual inaccuracies or hallucinations</li>

            <li>AI systems may omit important context, risks, or details</li>

            <li>
              AI-generated summaries, recommendations, or classifications may be
              incomplete or misleading
            </li>

            <li>
              AI systems may generate outdated information or incorrect
              interpretations
            </li>

            <li>
              AI outputs may vary between requests and are not guaranteed to be
              consistent
            </li>
          </ul>
        </section>

        <section>
          <h2 className="text-xl font-semibold">4. Human Review Required</h2>

          <p className="mt-2 text-slate-600">
            Users are solely responsible for independently reviewing, verifying,
            and validating all outputs before relying on them or taking action.
          </p>

          <p className="mt-2 text-slate-600">
            AI outputs should not be used as the sole basis for legal, financial,
            employment, educational, medical, security, compliance, or other
            high-impact decisions.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">5. User Responsibility</h2>

          <p className="mt-2 text-slate-600">
            Users remain fully responsible for how they use AI-generated outputs,
            including any decisions, actions, interpretations, or consequences
            resulting from use of the services.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">6. No Guarantees</h2>

          <p className="mt-2 text-slate-600">
            Runexa Systems LLC does not guarantee the accuracy, completeness,
            reliability, legality, availability, or fitness of AI-generated
            outputs for any purpose.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">7. Continuous Improvement</h2>

          <p className="mt-2 text-slate-600">
            AI systems may evolve, change, improve, or behave differently over
            time as models, infrastructure, and safety systems are updated.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">8. Contact</h2>

          <p className="mt-2 text-slate-600">
            contact@runexa.ai
          </p>
        </section>

      </div>
    </main>
  );
}