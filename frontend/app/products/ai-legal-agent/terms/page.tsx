export default function AILegalAgentTermsPage() {
  return (
    <main className="min-h-screen bg-slate-50 px-4 py-12">
      <div className="max-w-3xl mx-auto bg-white p-8 rounded-3xl border shadow-sm space-y-8">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">
            AI Legal Agent — Product Terms
          </h1>
          <p className="text-sm text-slate-500 mt-2">
            Last updated: April 2026
          </p>
        </div>

        <section>
          <h2 className="text-xl font-semibold">1. Description</h2>
          <p className="mt-2 text-slate-600">
            The AI Legal Agent is an AI-powered tool designed to assist users in
            reviewing legal documents, identifying potential risks, and generating
            simplified explanations.
          </p>
          <p className="mt-2 text-slate-600">
            It is part of the Runexa platform of specialized AI agents.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">2. No Legal Advice</h2>
          <p className="mt-2 text-slate-600">
            The AI Legal Agent is not a law firm and does not provide legal
            advice.
          </p>
          <p className="mt-2 text-slate-600">
            Outputs should not be considered a substitute for professional legal
            counsel.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">3. Accuracy Disclaimer</h2>
          <ul className="mt-2 list-disc pl-5 text-slate-600 space-y-1">
            <li>May misinterpret clauses</li>
            <li>May miss important risks</li>
            <li>May provide incomplete summaries</li>
          </ul>
        </section>

        <section>
          <h2 className="text-xl font-semibold">4. User Responsibility</h2>
          <p className="mt-2 text-slate-600">
            You are responsible for reviewing all outputs, making your own legal
            decisions, and consulting qualified professionals when necessary.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">5. High-Risk Use</h2>
          <p className="mt-2 text-slate-600">
            Do not rely solely on this tool for signing contracts, legal
            disputes, financial decisions, or other high-impact decisions.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">6. Liability Limitation</h2>
          <p className="mt-2 text-slate-600">
            Runexa is not responsible for contract issues, financial losses, or
            legal consequences resulting from use of AI outputs.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">7. Data Handling</h2>
          <p className="mt-2 text-slate-600">
            Documents are processed for analysis purposes. Users are responsible
            for ensuring they have the right to upload documents.
          </p>
        </section>
      </div>
    </main>
  );
}