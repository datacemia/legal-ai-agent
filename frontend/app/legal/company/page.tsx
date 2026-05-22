export default function CompanyPage() {
  return (
    <main className="min-h-screen bg-slate-50 px-4 py-12">
      <div className="max-w-3xl mx-auto bg-white p-8 rounded-3xl border shadow-sm space-y-8">

        <div>
          <h1 className="text-3xl font-bold text-slate-900">
            Company Information
          </h1>

          <p className="text-sm text-slate-500 mt-2">
            Last updated: April 2026
          </p>
        </div>

        <section>
          <h2 className="text-xl font-semibold">1. Company</h2>

          <p className="mt-2 text-slate-600">
            Runexa Systems LLC
          </p>

          <p className="mt-2 text-slate-600">
            AI agents platform providing AI-powered tools and services.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            2. Registered Address
          </h2>

          <p className="mt-2 text-slate-600">
            1309 Coffeen Avenue, Suite 1200
            <br />
            Sheridan, WY 82801
            <br />
            United States
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            3. Contact Information
          </h2>

          <p className="mt-2 text-slate-600">
            General Contact: contact@runexa.ai
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            4. Services
          </h2>

          <p className="mt-2 text-slate-600">
            Runexa Systems LLC develops and operates AI-powered tools,
            applications, AI agents, and related software services.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            5. Governing Law
          </h2>

          <p className="mt-2 text-slate-600">
            Services provided by Runexa Systems LLC are governed by the laws of
            the State of Wyoming, United States.
          </p>
        </section>

      </div>
    </main>
  );
}