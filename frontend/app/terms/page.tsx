export default function TermsPage() {
  return (
    <main className="min-h-screen bg-slate-50 px-4 py-12">
      <div className="max-w-3xl mx-auto bg-white p-8 rounded-3xl border shadow-sm space-y-8">

        <div>
          <h1 className="text-3xl font-bold text-slate-900">
            Terms of Service
          </h1>
          <p className="text-sm text-slate-500 mt-2">
            Last updated: April 2026
          </p>
        </div>

        <section>
          <h2 className="text-xl font-semibold">1. Overview</h2>
          <p className="mt-2 text-slate-600">
            Runexa provides access to AI-powered tools designed to assist users
            in analyzing documents and generating insights.
          </p>
          <p className="mt-2 text-slate-600">
            By using Runexa, you agree to these Terms.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">2. Account</h2>
          <p className="mt-2 text-slate-600">
            You are responsible for maintaining the security of your account and
            all activity under your account.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">3. Use of Services</h2>
          <ul className="mt-2 list-disc pl-5 text-slate-600 space-y-1">
            <li>No illegal use</li>
            <li>No unauthorized data upload</li>
            <li>No abuse of the platform</li>
          </ul>
        </section>

        <section>
          <h2 className="text-xl font-semibold">4. AI Services</h2>
          <p className="mt-2 text-slate-600">
            AI outputs may be inaccurate or incomplete. They should not be
            relied upon as the sole source of truth.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">5. Payments</h2>
          <p className="mt-2 text-slate-600">
            Credits are non-refundable unless required by law.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">6. Data Usage</h2>
          <p className="mt-2 text-slate-600">
            You retain ownership of your data. We process data only to provide
            the service.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">7. Limitation of Liability</h2>
          <p className="mt-2 text-slate-600">
            Runexa is not liable for business losses, legal disputes, or misuse
            of AI outputs.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">8. Termination</h2>
          <p className="mt-2 text-slate-600">
            Accounts may be suspended if Terms are violated.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">9. Changes</h2>
          <p className="mt-2 text-slate-600">
            Terms may be updated at any time.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">10. Contact</h2>
          <p className="mt-2 text-slate-600">
            contact@runexa.ai
          </p>
        </section>

      </div>
    </main>
  );
}