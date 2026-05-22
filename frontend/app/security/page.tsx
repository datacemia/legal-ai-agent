export default function SecurityPage() {
  return (
    <main className="min-h-screen bg-slate-50 px-4 py-12">
      <div className="max-w-3xl mx-auto bg-white p-8 rounded-3xl border shadow-sm space-y-8">

        <div>
          <h1 className="text-3xl font-bold text-slate-900">
            Security
          </h1>

          <p className="text-sm text-slate-500 mt-2">
            Last updated: April 2026
          </p>
        </div>

        <section>
          <h2 className="text-xl font-semibold">1. Overview</h2>

          <p className="mt-2 text-slate-600">
            Runexa Systems LLC is committed to maintaining reasonable technical,
            organizational, and administrative safeguards designed to protect
            user information, platform integrity, and AI infrastructure.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            2. Infrastructure and Hosting
          </h2>

          <p className="mt-2 text-slate-600">
            Runexa services may use secure cloud infrastructure providers,
            hosting providers, database providers, AI providers, and payment
            processors to operate the platform.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            3. Encryption and Secure Connections
          </h2>

          <p className="mt-2 text-slate-600">
            Data transmitted between users and the platform may be protected
            using encrypted communication protocols such as HTTPS and TLS where
            applicable.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            4. Access Controls
          </h2>

          <p className="mt-2 text-slate-600">
            Access to systems, accounts, infrastructure, and operational tools
            may be restricted to authorized personnel and protected through
            authentication and security controls.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            5. Monitoring and Abuse Prevention
          </h2>

          <p className="mt-2 text-slate-600">
            Runexa Systems LLC may monitor platform activity, logs, access
            attempts, and system behavior to detect abuse, fraud, unauthorized
            access, or security threats.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            6. Payment Security
          </h2>

          <p className="mt-2 text-slate-600">
            Payments may be processed by trusted third-party payment providers.
            Runexa Systems LLC does not store full payment card information on
            its own servers.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            7. User Responsibility
          </h2>

          <p className="mt-2 text-slate-600">
            Users are responsible for maintaining the confidentiality of their
            accounts, passwords, devices, and uploaded information.
          </p>

          <p className="mt-2 text-slate-600">
            Users should avoid uploading highly sensitive information unless
            necessary and appropriate safeguards are in place.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            8. No Absolute Security Guarantee
          </h2>

          <p className="mt-2 text-slate-600">
            While Runexa Systems LLC implements reasonable safeguards, no
            internet-based platform, software, AI system, or storage system can
            be guaranteed to be completely secure.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            9. Reporting Security Issues
          </h2>

          <p className="mt-2 text-slate-600">
            Security concerns, vulnerabilities, or suspected abuse may be
            reported to:
          </p>

          <p className="mt-2 text-slate-600">
            contact@runexa.ai
          </p>
        </section>

      </div>
    </main>
  );
}