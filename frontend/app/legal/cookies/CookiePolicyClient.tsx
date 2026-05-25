"use client";

import { useEffect, useState } from "react";
import {
  defaultLocale,
  getSavedLocale,
  getTranslations,
} from "../../../lib/i18n";

export default function CookiePolicyClient() {
  const [locale, setLocale] = useState(defaultLocale);

  useEffect(() => {
    setLocale(getSavedLocale());
  }, []);

  const t = getTranslations(locale);

  return (
    <main
      dir={locale === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-4 py-12"
    >
      <div className="max-w-3xl mx-auto bg-white p-8 rounded-3xl border shadow-sm space-y-8">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">
            {t.cookiesTitle || "Cookie Policy"}
          </h1>

          <p className="text-sm text-slate-500 mt-2">
            {t.cookiesUpdated || "Last updated: May 2026"}
          </p>
        </div>

        <section>
          <h2 className="text-xl font-semibold">
            {t.cookiesOverviewTitle || "1. Overview"}
          </h2>

          <p className="mt-2 text-slate-600">
            {t.cookiesOverviewText ||
              "This Cookie Policy explains how Runexa Systems LLC (“Runexa”, “we”, “our”, or “us”) uses cookies and similar technologies when you access or use our services, websites, and AI platforms."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.cookiesWhatTitle || "2. What Are Cookies"}
          </h2>

          <p className="mt-2 text-slate-600">
            {t.cookiesWhatText ||
              "Cookies are small text files stored on your device by your web browser. Cookies help websites recognize users, maintain sessions, remember preferences, and improve functionality and security."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.cookiesTypesTitle || "3. Types of Cookies We Use"}
          </h2>

          <h3 className="mt-4 font-medium">
            {t.cookiesEssentialTitle || "3.1 Essential Cookies"}
          </h3>

          <p className="text-slate-600 mt-1">
            {t.cookiesEssentialText ||
              "These cookies are necessary for the operation of the services, including authentication, account access, security, and session management."}
          </p>

          <h3 className="mt-4 font-medium">
            {t.cookiesAnalyticsTitle ||
              "3.2 Performance and Analytics Cookies"}
          </h3>

          <p className="text-slate-600 mt-1">
            {t.cookiesAnalyticsText ||
              "These cookies help us understand how users interact with the platform, improve reliability, monitor performance, and detect technical issues."}
          </p>

          <h3 className="mt-4 font-medium">
            {t.cookiesPreferenceTitle || "3.3 Preference Cookies"}
          </h3>

          <p className="text-slate-600 mt-1">
            {t.cookiesPreferenceText ||
              "These cookies may store user preferences such as language settings, interface preferences, or session-related choices."}
          </p>

          <h3 className="mt-4 font-medium">
            {t.cookiesSecurityTitle || "3.4 Security Cookies"}
          </h3>

          <p className="text-slate-600 mt-1">
            {t.cookiesSecurityText ||
              "Security-related cookies may be used to prevent fraud, abuse, unauthorized access, and suspicious activity."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.cookiesThirdPartyTitle || "4. Third-Party Services"}
          </h2>

          <p className="mt-2 text-slate-600">
            {t.cookiesThirdPartyText ||
              "Some cookies may be placed by third-party providers that support infrastructure, analytics, authentication, hosting, AI processing, or payment services used by Runexa Systems LLC."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.cookiesManagingTitle || "5. Managing Cookies"}
          </h2>

          <p className="mt-2 text-slate-600">
            {t.cookiesManagingText ||
              "Most web browsers allow users to control, disable, or delete cookies through browser settings. Disabling cookies may affect functionality, availability, or performance of certain services."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.cookiesTrackTitle || "6. Do Not Track"}
          </h2>

          <p className="mt-2 text-slate-600">
            {t.cookiesTrackText ||
              "Some browsers offer “Do Not Track” settings. Because there is no universally accepted standard for these signals, our services may not respond to all Do Not Track requests."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.cookiesChangesTitle || "7. Changes"}
          </h2>

          <p className="mt-2 text-slate-600">
            {t.cookiesChangesText ||
              "Runexa Systems LLC may update this Cookie Policy from time to time. Updated versions will be posted with a revised “Last updated” date."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.cookiesContactTitle || "8. Contact"}
          </h2>

          <p className="mt-2 text-slate-600">
            contact@runexa.ai
          </p>
        </section>
      </div>
    </main>
  );
}