"use client";

import { useEffect, useState } from "react";
import type { Metadata } from "next";
import {
  defaultLocale,
  getSavedLocale,
  getTranslations,
} from "../../../lib/i18n";

export const metadata: Metadata = {
  title: "Cookie Policy | Runexa Systems",

  description:
    "Review the Cookie Policy for Runexa Systems LLC, including how cookies, analytics, security technologies, and related services are used across our AI platforms and enterprise infrastructure.",

  keywords: [
    "cookie policy",
    "Runexa cookies",
    "AI platform cookies",
    "analytics cookies",
    "security cookies",
    "enterprise AI compliance",
    "Runexa privacy",
  ],

  alternates: {
    canonical: "https://runexa.ai/legal/cookies",
  },

  openGraph: {
    title: "Cookie Policy | Runexa Systems",

    description:
      "Review the Cookie Policy governing cookies, analytics, and security technologies used by Runexa Systems LLC.",

    url: "https://runexa.ai/legal/cookies",

    siteName: "Runexa Systems",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Cookie Policy",
      },
    ],

    locale: "en_US",

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Cookie Policy | Runexa Systems",

    description:
      "Review how cookies, analytics, and security technologies are used across Runexa AI services and platforms.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

const jsonLd = {
  "@context": "https://schema.org",

  "@type": "WebPage",

  name: "Runexa Cookie Policy",

  description:
    "Cookie Policy governing cookies, analytics technologies, and security-related technologies used by Runexa Systems LLC.",

  url: "https://runexa.ai/legal/cookies",

  publisher: {
    "@type": "Organization",
    name: "Runexa Systems LLC",
    url: "https://runexa.ai",
  },
};

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
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(jsonLd),
        }}
      />

      <div className="mx-auto max-w-3xl space-y-8 rounded-3xl border bg-white p-8 shadow-sm">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">
            {t.cookiesTitle || "Cookie Policy"}
          </h1>

          <p className="mt-2 text-sm text-slate-500">
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

          <p className="mt-1 text-slate-600">
            {t.cookiesEssentialText ||
              "These cookies are necessary for the operation of the services, including authentication, account access, security, and session management."}
          </p>

          <h3 className="mt-4 font-medium">
            {t.cookiesAnalyticsTitle ||
              "3.2 Performance and Analytics Cookies"}
          </h3>

          <p className="mt-1 text-slate-600">
            {t.cookiesAnalyticsText ||
              "These cookies help us understand how users interact with the platform, improve reliability, monitor performance, and detect technical issues."}
          </p>

          <h3 className="mt-4 font-medium">
            {t.cookiesPreferenceTitle || "3.3 Preference Cookies"}
          </h3>

          <p className="mt-1 text-slate-600">
            {t.cookiesPreferenceText ||
              "These cookies may store user preferences such as language settings, interface preferences, or session-related choices."}
          </p>

          <h3 className="mt-4 font-medium">
            {t.cookiesSecurityTitle || "3.4 Security Cookies"}
          </h3>

          <p className="mt-1 text-slate-600">
            {t.cookiesSecurityText ||
              "Security-related cookies may be used to prevent fraud, abuse, unauthorized access, suspicious activity, rate limiting, and platform reliability."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.cookiesThirdPartyTitle || "4. Third-Party Services"}
          </h2>

          <p className="mt-2 text-slate-600">
            {t.cookiesThirdPartyText ||
              "Some cookies may be placed by third-party providers that support infrastructure, analytics, authentication, hosting, AI processing, payment services, security, or operational reliability used by Runexa Systems LLC."}
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
