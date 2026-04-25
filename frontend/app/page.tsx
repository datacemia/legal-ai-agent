import Link from "next/link";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-slate-50 text-slate-900">
      <section className="px-6 py-20">
        <div className="max-w-6xl mx-auto text-center space-y-8">
          <p className="text-blue-600 font-semibold">
            Legal AI Agent
          </p>

          <h1 className="text-5xl font-bold leading-tight">
            Understand your contracts before you sign.
          </h1>

          <p className="text-lg text-slate-600 max-w-3xl mx-auto">
            Upload a PDF or DOCX contract and get an AI-powered analysis:
            risk score, simplified summary, dangerous clauses, and practical
            recommendations.
          </p>

          <div className="flex justify-center gap-4">
            <Link
              href="/upload"
              className="px-6 py-3 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition"
            >
              Analyze a contract
            </Link>

            <a
              href="#features"
              className="px-6 py-3 bg-white border border-slate-200 rounded-xl font-semibold hover:bg-slate-100 transition"
            >
              See features
            </a>
          </div>
        </div>
      </section>

      <section id="features" className="px-6 py-12">
        <div className="max-w-6xl mx-auto grid md:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-2xl border shadow-sm">
            <h3 className="text-xl font-bold">Risk Score</h3>
            <p className="mt-3 text-slate-600">
              Instantly see if your contract contains low, medium, or high-risk
              clauses.
            </p>
          </div>

          <div className="bg-white p-6 rounded-2xl border shadow-sm">
            <h3 className="text-xl font-bold">Simple Summary</h3>
            <p className="mt-3 text-slate-600">
              Get a clear explanation of the contract without complex legal
              language.
            </p>
          </div>

          <div className="bg-white p-6 rounded-2xl border shadow-sm">
            <h3 className="text-xl font-bold">Clause Analysis</h3>
            <p className="mt-3 text-slate-600">
              Detect sensitive clauses like penalties, liability,
              non-compete, and intellectual property.
            </p>
          </div>
        </div>
      </section>

      <section className="px-6 py-16">
        <div className="max-w-5xl mx-auto bg-blue-600 text-white rounded-3xl p-10 text-center">
          <h2 className="text-3xl font-bold">
            Built for freelancers, startups, SMEs, and individuals.
          </h2>
          <p className="mt-4 text-blue-100">
            Legal AI Agent helps you understand important documents faster,
            before making decisions.
          </p>

          <Link
            href="/upload"
            className="inline-block mt-6 px-6 py-3 bg-white text-blue-600 rounded-xl font-semibold"
          >
            Start analysis
          </Link>
        </div>
      </section>

      <footer className="px-6 py-8 text-center text-sm text-slate-500">
        Built by Dr. Rachid Ejjami · Legal AI Agent 
      </footer>
    </main>
  );
}