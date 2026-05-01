"use client";

import Link from "next/link";

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
          <Link href="/contact" className="px-6 py-3 bg-blue-600 text-white rounded-xl font-semibold">
            Request a demo
          </Link>

          <Link href="/contact" className="px-6 py-3 border rounded-xl font-semibold">
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
        <h2 className="text-2xl font-bold text-center mb-10">
          What we build for your business
        </h2>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">

          <div className="bg-white p-6 rounded-2xl border">
            <h3 className="font-semibold">Legal AI Agent</h3>
            <p className="text-sm text-slate-600 mt-3">
              Analyze internal contracts, detect risks, and ensure compliance.
            </p>
          </div>

          <div className="bg-white p-6 rounded-2xl border">
            <h3 className="font-semibold">Finance AI Agent</h3>
            <p className="text-sm text-slate-600 mt-3">
              Automate financial analysis and generate internal reports.
            </p>
          </div>

          <div className="bg-white p-6 rounded-2xl border">
            <h3 className="font-semibold">HR AI Agent</h3>
            <p className="text-sm text-slate-600 mt-3">
              Screen CVs and streamline recruitment.
            </p>
          </div>

          <div className="bg-white p-6 rounded-2xl border">
            <h3 className="font-semibold">Business Decision Agent</h3>
            <p className="text-sm text-slate-600 mt-3">
              Analyze business data and support strategic decisions.
            </p>
          </div>

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
          <div>Understand your needs</div>
          <div>Build your agents</div>
          <div>Deploy & integrate</div>
          <div>Scale with AI</div>
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

        <Link href="/contact" className="inline-block mt-6 px-6 py-3 bg-white text-blue-600 rounded-xl font-semibold">
          Get started
        </Link>
      </section>

    </main>
  );
}