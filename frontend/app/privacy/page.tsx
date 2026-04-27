export default function PrivacyPage() {
  return (
    <main className="min-h-screen bg-slate-50 px-4 py-12">
      <div className="max-w-3xl mx-auto bg-white p-8 rounded-3xl border shadow-sm space-y-8">

        <div>
          <h1 className="text-3xl font-bold text-slate-900">
            Privacy Policy
          </h1>
          <p className="text-sm text-slate-500 mt-2">
            Last updated: April 2026
          </p>
        </div>

        <section>
          <h2 className="text-xl font-semibold">1. Introduction</h2>
          <p className="mt-2 text-slate-600">
            Runexa ("we", "our", "us") respects your privacy. This Privacy Policy
            explains how we collect, use, and protect your information.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">2. Information We Collect</h2>

          <h3 className="mt-4 font-medium">2.1 Account Information</h3>
          <p className="text-slate-600 mt-1">
            Email address and encrypted password.
          </p>

          <h3 className="mt-4 font-medium">2.2 Uploaded Documents</h3>
          <p className="text-slate-600 mt-1">
            Contracts, legal documents, and other files processed for analysis.
          </p>

          <h3 className="mt-4 font-medium">2.3 Usage Data</h3>
          <p className="text-slate-600 mt-1">
            IP address, browser type, device info, and usage activity.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">3. How We Use Your Data</h2>
          <ul className="mt-2 list-disc pl-5 text-slate-600 space-y-1">
            <li>Provide and operate our services</li>
            <li>Analyze documents</li>
            <li>Improve product performance</li>
            <li>Ensure security</li>
          </ul>
        </section>

        <section>
          <h2 className="text-xl font-semibold">4. AI Processing</h2>
          <p className="mt-2 text-slate-600">
            Documents may be processed by AI systems for extraction, analysis,
            and summary generation. Accuracy is not guaranteed.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">5. Data Storage</h2>
          <p className="mt-2 text-slate-600">
            Data may be stored using secure third-party infrastructure providers.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">6. Data Sharing</h2>
          <p className="mt-2 text-slate-600">
            We do not sell your data. We only share data with service providers
            necessary to operate the service (e.g., hosting, AI, payments).
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">7. Data Retention</h2>
          <p className="mt-2 text-slate-600">
            Data is retained only as long as necessary. You may request deletion.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">8. Security</h2>
          <p className="mt-2 text-slate-600">
            We implement reasonable security measures, but no system is fully secure.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">9. Your Rights</h2>
          <p className="mt-2 text-slate-600">
            You may have rights to access, correct, or delete your data.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">10. Cookies</h2>
          <p className="mt-2 text-slate-600">
            Cookies may be used to maintain sessions and improve experience.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">11. Children</h2>
          <p className="mt-2 text-slate-600">
            This service is not intended for users under 18.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">12. Changes</h2>
          <p className="mt-2 text-slate-600">
            We may update this policy at any time.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">13. Contact</h2>
          <p className="mt-2 text-slate-600">
            contact@runexa.ai
          </p>
        </section>

      </div>
    </main>
  );
}