"use client";

import { useEffect, useState } from "react";
import {
  defaultLocale,
  getSavedLocale,
  getTranslations,
} from "../../lib/i18n";

type Locale = "en" | "fr" | "ar";

type SecurityTranslations = Record<string, string>;

const normalizeLocale = (
  value: string | null | undefined,
  fallback: Locale = "en"
): Locale => {
  if (value === "en" || value === "fr" || value === "ar") {
    return value;
  }

  return fallback;
};

const getDefaultLocale = (): Locale => {
  return normalizeLocale(defaultLocale, "en");
};

export default function SecurityClient({
  initialLocale,
  lockInitialLocale = false,
}: {
  initialLocale?: Locale;
  lockInitialLocale?: boolean;
}) {
  const resolvedInitialLocale = initialLocale || getDefaultLocale();

  const [locale, setLocale] = useState<Locale>(resolvedInitialLocale);

  useEffect(() => {
    if (lockInitialLocale) {
      setLocale(resolvedInitialLocale);
      return;
    }

    setLocale(normalizeLocale(getSavedLocale(), resolvedInitialLocale));
  }, [resolvedInitialLocale, lockInitialLocale]);

  const t = getTranslations(locale) as SecurityTranslations;

  return (
    <main
      dir={locale === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-4 py-12"
    >
      <div className="max-w-3xl mx-auto bg-white p-8 rounded-3xl border shadow-sm space-y-8">

        <div>
          <h1 className="text-3xl font-bold text-slate-900">
            {t.securityTitle || "Security"}
          </h1>

          <p className="text-sm text-slate-500 mt-2">
            {t.securityUpdated || "Last updated: May 2026"}
          </p>
        </div>

        <section>
          <h2 className="text-xl font-semibold">
            {t.securityOverviewTitle || "1. Overview"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.securityOverviewText ||
              "Runexa Systems LLC is committed to maintaining reasonable technical, organizational, and administrative safeguards designed to protect user information, platform integrity, and AI infrastructure."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.securityInfrastructureTitle ||
              "2. Infrastructure and Hosting"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.securityInfrastructureText ||
              "Runexa services may use secure cloud infrastructure providers, hosting providers, database providers, AI providers, and payment processors to operate the platform."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.securityEncryptionTitle ||
              "3. Encryption and Secure Connections"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.securityEncryptionText ||
              "Data transmitted between users and the platform may be protected using encrypted communication protocols such as HTTPS and TLS where applicable."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.securityAccessTitle || "4. Access Controls"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.securityAccessText ||
              "Access to systems, accounts, infrastructure, and operational tools may be restricted to authorized personnel and protected through authentication and security controls."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.securityMonitoringTitle ||
              "5. Monitoring and Abuse Prevention"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.securityMonitoringText ||
              "Runexa Systems LLC may monitor platform activity, logs, access attempts, and system behavior to detect abuse, fraud, unauthorized access, or security threats."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.securityPaymentTitle || "6. Payment Security"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.securityPaymentText ||
              "Payments may be processed by trusted third-party payment providers. Runexa Systems LLC does not store full payment card information on its own servers."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.securityUserTitle || "7. User Responsibility"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.securityUserText1 ||
              "Users are responsible for maintaining the confidentiality of their accounts, passwords, devices, and uploaded information."}
          </p>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.securityUserText2 ||
              "Users should avoid uploading highly sensitive information unless necessary and appropriate safeguards are in place."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.securityGuaranteeTitle ||
              "8. No Absolute Security Guarantee"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.securityGuaranteeText ||
              "While Runexa Systems LLC implements reasonable safeguards, no internet-based platform, software, AI system, or storage system can be guaranteed to be completely secure."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.securityReportTitle ||
              "9. Reporting Security Issues"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.securityReportText ||
              "Security concerns, vulnerabilities, or suspected abuse may be reported to:"}
          </p>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            contact@runexa.ai
          </p>
        </section>

      </div>
    </main>
  );
}
