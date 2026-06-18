"use client";

import { useEffect, useState } from "react";
import {
  defaultLocale,
  getSavedLocale,
  getTranslations,
} from "../../lib/i18n";

type Locale = "en" | "fr" | "ar";

type PrivacyTranslations = Record<string, string>;

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

export default function PrivacyClient({
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

  const t = getTranslations(locale) as PrivacyTranslations;

  return (
    <main
      dir={locale === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-4 py-12"
    >
      <div className="max-w-3xl mx-auto bg-white p-8 rounded-3xl border shadow-sm space-y-8">

        <div>
          <h1 className="text-3xl font-bold text-slate-900">
            {t.privacyTitle || "Privacy Policy"}
          </h1>

          <p className="text-sm text-slate-500 mt-2">
            {t.privacyUpdated || "Last updated: May 2026"}
          </p>
        </div>

        <section>
          <h2 className="text-xl font-semibold">
            {t.privacyIntroTitle || "1. Introduction"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.privacyIntroText ||
              "Runexa Systems LLC (“we”, “our”, “us”) respects your privacy. This Privacy Policy explains how we collect, use, store, share, and protect information when you use Runexa and its AI-powered services."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.privacyCollectTitle || "2. Information We Collect"}
          </h2>

          <h3 className="mt-4 font-medium">
            {t.privacyAccountTitle || "2.1 Account Information"}
          </h3>

          <p className="text-slate-600 mt-1 break-words whitespace-normal">
            {t.privacyAccountText ||
              "We may collect your email address, encrypted password, account status, billing status, and authentication-related information."}
          </p>

          <h3 className="mt-4 font-medium">
            {t.privacyUploadTitle || "2.2 Uploaded Content"}
          </h3>

          <p className="text-slate-600 mt-1 break-words whitespace-normal">
            {t.privacyUploadText ||
              "We may process documents, files, text, financial information, study materials, business data, and other content you upload for analysis."}
          </p>

          <h3 className="mt-4 font-medium">
            {t.privacyUsageTitle || "2.3 Usage Data"}
          </h3>

          <p className="text-slate-600 mt-1 break-words whitespace-normal">
            {t.privacyUsageText ||
              "We may collect IP address, browser type, device information, pages visited, feature usage, logs, error reports, and security-related data."}
          </p>

          <h3 className="mt-4 font-medium">
            {t.privacyPaymentTitle || "2.4 Payment Information"}
          </h3>

          <p className="text-slate-600 mt-1 break-words whitespace-normal">
            {t.privacyPaymentText ||
              "Payments may be processed by third-party payment providers. We do not store full payment card details on our servers."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.privacyUseTitle || "3. How We Use Your Data"}
          </h2>

          <ul className="mt-2 list-disc pl-5 text-slate-600 space-y-1">
            <li>
              {t.privacyUse1 ||
                "Provide, operate, and maintain the services"}
            </li>

            <li>
              {t.privacyUse2 ||
                "Analyze documents and generate AI-powered outputs"}
            </li>

            <li>
              {t.privacyUse3 ||
                "Manage accounts, credits, payments, and access"}
            </li>

            <li>
              {t.privacyUse4 ||
                "Improve product performance, reliability, and user experience"}
            </li>

            <li>
              {t.privacyUse5 ||
                "Detect abuse, prevent fraud, and protect platform security"}
            </li>

            <li>
              {t.privacyUse6 ||
                "Comply with legal, tax, accounting, and regulatory obligations"}
            </li>
          </ul>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.privacyAiTitle || "4. AI Processing"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.privacyAiText ||
              "Uploaded content may be processed by AI systems and infrastructure providers for extraction, analysis, summarization, classification, and generation of outputs. AI-generated outputs may be inaccurate or incomplete and should be independently verified."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.privacyStorageTitle || "5. Data Storage and Providers"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.privacyStorageText ||
              "Data may be stored and processed using secure third-party infrastructure, hosting, analytics, payment, database, and AI service providers that help us operate the services."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.privacySharingTitle || "6. Data Sharing"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.privacySharingText ||
              "We do not sell your personal information. We may share information only with service providers, payment processors, infrastructure providers, legal authorities when required by law, or in connection with a business transaction such as a merger, acquisition, or asset transfer."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.privacyRetentionTitle || "7. Data Retention"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.privacyRetentionText ||
              "We retain information only as long as reasonably necessary to provide the services, comply with legal obligations, resolve disputes, prevent abuse, and enforce our agreements. You may request deletion of your data, subject to legal and operational retention requirements."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.privacySecurityTitle || "8. Security"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.privacySecurityText ||
              "We implement reasonable technical, administrative, and organizational measures designed to protect your information. However, no method of transmission or storage is completely secure, and we cannot guarantee absolute security."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.privacyInternationalTitle || "9. International Users"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.privacyInternationalText ||
              "If you access the services from outside the United States, your information may be transferred to, stored in, or processed in the United States or other jurisdictions where our service providers operate."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.privacyRightsTitle || "10. Your Rights"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.privacyRightsText ||
              "Depending on your location, you may have rights to access, correct, delete, export, restrict, or object to certain processing of your personal information. You may contact us to exercise these rights."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.privacyCookiesTitle || "11. Cookies"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.privacyCookiesText ||
              "Cookies and similar technologies may be used to maintain sessions, remember preferences, secure accounts, analyze usage, and improve the user experience."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.privacyChildrenTitle || "12. Children"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.privacyChildrenText ||
              "The services are not intended for users under 18 years old. We do not knowingly collect personal information from children under 18."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.privacyChangesTitle || "13. Changes"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.privacyChangesText ||
              "We may update this Privacy Policy from time to time. Updated versions will be posted on this page with a revised “Last updated” date."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.privacyContactTitle || "14. Contact"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            contact@runexa.ai
          </p>
        </section>

      </div>
    </main>
  );
}
