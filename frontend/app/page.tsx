import Link from "next/link";

const agents = [
  {
    name: "Legal Agent",
    description: "Analyze contracts, detect risky clauses, and get clear recommendations before you sign.",
    href: "/upload",
    status: "Available",
  },
  {
    name: "Finance Agent",
    description: "Review invoices, budgets, expenses, and financial documents faster.",
    href: "#",
    status: "Coming soon",
  },
  {
    name: "HR Agent",
    description: "Analyze CVs, job descriptions, HR policies, and employee documents.",
    href: "#",
    status: "Coming soon",
  },
  {
    name: "Business Agent",
    description: "Generate summaries, reports, strategies, and business insights.",
    href: "#",
    status: "Coming soon",
  },
];

export default function HomePage() {
  return (
    <main className="min-h-screen bg-slate-50 text-slate-900">
      <section className="px-6 py-20">
        <div className="max-w-6xl mx-auto text-center space-y-8">
          <p className="text-blue-600 font-semibold">
            Runexa AI Agents Platform
          </p>

          <h1 className="text-5xl font-bold leading-tight">
            AI agents that help you get work done faster.
          </h1>

          <p className="text-lg text-slate-600 max-w-3xl mx-auto">
            Runexa brings specialized AI agents for legal, finance, HR,
            business, and more — all in one simple platform.
          </p>

          <div className="flex justify-center gap-4">
            <a
              href="#agents"
              className="px-6 py-3 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition"
            >
              Explore agents
            </a>

            <Link
              href="/upload"
              className="px-6 py-3 bg-white border border-slate-200 rounded-xl font-semibold hover:bg-slate-100 transition"
            >
              Try Legal Agent
            </Link>
          </div>
        </div>
      </section>

      <section id="agents" className="px-6 py-12">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-10">
            <h2 className="text-3xl font-bold">Choose your AI agent</h2>
            <p className="mt-3 text-slate-600">
              Start with Legal Agent today. More specialized agents are coming soon.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {agents.map((agent) => (
              <div
                key={agent.name}
                className="bg-white p-6 rounded-2xl border shadow-sm flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between gap-3">
                    <h3 className="text-xl font-bold">{agent.name}</h3>
                    <span className="text-xs bg-slate-100 text-slate-600 px-3 py-1 rounded-full">
                      {agent.status}
                    </span>
                  </div>

                  <p className="mt-4 text-slate-600">
                    {agent.description}
                  </p>
                </div>

                {agent.status === "Available" ? (
                  <Link
                    href={agent.href}
                    className="inline-block mt-6 text-center px-4 py-2 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition"
                  >
                    Open agent
                  </Link>
                ) : (
                  <button
                    disabled
                    className="mt-6 px-4 py-2 bg-slate-100 text-slate-400 rounded-xl font-semibold cursor-not-allowed"
                  >
                    Coming soon
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="px-6 py-16">
        <div className="max-w-5xl mx-auto bg-blue-600 text-white rounded-3xl p-10 text-center">
          <h2 className="text-3xl font-bold">
            One platform. Multiple AI agents. Real business outcomes.
          </h2>

          <p className="mt-4 text-blue-100">
            Start with contract analysis today, then expand into finance, HR,
            operations, and business automation as your needs grow.
          </p>

          <Link
            href="/upload"
            className="inline-block mt-6 px-6 py-3 bg-white text-blue-600 rounded-xl font-semibold"
          >
            Start with Legal Agent
          </Link>
        </div>
      </section>

      <footer className="px-6 py-8 text-center text-sm text-slate-500">
        Runexa AI · Specialized agents for modern teams
      </footer>
    </main>
  );
}