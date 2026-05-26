"use client";

import { useEffect, useState } from "react";
import type { Metadata } from "next";
import {
  defaultLocale,
  getSavedLocale,
  getTranslations,
} from "../../../lib/i18n";

export const metadata: Metadata = {
  title: "Acceptable Use Policy | Runexa Systems",

  description:
    "Review the Acceptable Use Policy governing the use of Runexa Systems AI services, platforms, software, APIs, and enterprise infrastructure.",

  keywords: [
    "acceptable use policy",
    "Runexa policy",
    "AI acceptable use",
    "AI compliance",
    "AI platform rules",
    "enterprise AI policy",
    "AI service terms",
  ],

  alternates: {
    canonical: "https://runexa.ai/legal/acceptable-use",
  },

  openGraph: {
    title: "Acceptable Use Policy | Runexa Systems",

    description:
      "Review the Acceptable Use Policy governing Runexa Systems AI services, APIs, and enterprise platforms.",

    url: "https://runexa.ai/legal/acceptable-use",

    siteName: "Runexa Systems",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Acceptable Use Policy",
      },
    ],

    locale: "en_US",

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Acceptable Use Policy | Runexa Systems",

    description:
      "Review the acceptable use requirements for Runexa AI services and enterprise infrastructure.",

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

  name: "Runexa Acceptable Use Policy",

  description:
    "Acceptable Use Policy governing access to and usage of Runexa Systems AI services, APIs, and enterprise infrastructure.",

  url: "https://runexa.ai/legal/acceptable-use",

  publisher: {
    "@type": "Organization",
    name: "Runexa Systems LLC",
    url: "https://runexa.ai",
  },
};

export default function AcceptableUseClient() {
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
            {t.acceptableUseTitle || "Acceptable Use Policy"}
          </h1>

          <p className="mt-2 text-sm text-slate-500">
            {t.acceptableUseUpdated || "Last updated: May 2026"}
          </p>
        </div>

        <section>
          <h2 className="text-xl font-semibold">
            {t.acceptableUseOverviewTitle || "1. Overview"}
          </h2>

          <p className="mt-2 text-slate-600">
            {t.acceptableUseOverviewText1 ||
              "This Acceptable Use Policy (“Policy”) governs the use of services, products, software, AI agents, and platforms operated by Runexa Systems LLC (“Runexa”)."}
          </p>

          <p className="mt-2 text-slate-600">
            {t.acceptableUseOverviewText2 ||
              "By using Runexa services, you agree to comply with this Policy."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.acceptableUseComplianceTitle || "2. Compliance With Laws"}
          </h2>

          <p className="mt-2 text-slate-600">
            {t.acceptableUseComplianceText ||
              "You may only use the services in compliance with applicable laws, regulations, and third-party rights."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.acceptableUseProhibitedTitle || "3. Prohibited Activities"}
          </h2>

          <p className="mt-2 text-slate-600">
            {t.acceptableUseProhibitedIntro ||
              "You may not use Runexa services for:"}
          </p>

          <ul className="mt-4 list-disc space-y-2 pl-5 text-slate-600">
            <li>
              {t.acceptableUseProhibited1 ||
                "Illegal, fraudulent, or deceptive activity"}
            </li>

            <li>
              {t.acceptableUseProhibited2 ||
                "Malware, phishing, hacking, unauthorized access, or cyber abuse"}
            </li>

            <li>
              {t.acceptableUseProhibited3 ||
                "Harassment, threats, abuse, discrimination, or harmful conduct"}
            </li>

            <li>
              {t.acceptableUseProhibited4 ||
                "Uploading or processing content that violates intellectual property, privacy, confidentiality, or contractual rights"}
            </li>

            <li>
              {t.acceptableUseProhibited5 ||
                "Impersonation, identity fraud, or misleading representations"}
            </li>

            <li>
              {t.acceptableUseProhibited6 ||
                "Unauthorized surveillance, monitoring, or tracking of individuals"}
            </li>

            <li>
              {t.acceptableUseProhibited7 ||
                "Generating harmful, dangerous, or unlawful content"}
            </li>

            <li>
              {t.acceptableUseProhibited8 ||
                "Attempting to reverse engineer, disrupt, overload, or bypass the platform or security protections"}
            </li>

            <li>
              {t.acceptableUseProhibited9 ||
                "Using automated systems to abuse, scrape, spam, or excessively overload the services"}
            </li>
          </ul>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.acceptableUseAiTitle || "4. AI Usage Restrictions"}
          </h2>

          <p className="mt-2 text-slate-600">
            {t.acceptableUseAiText1 ||
              "AI-generated outputs may not be used as the sole basis for legal, financial, medical, employment, security, or other high-impact decisions without independent human review."}
          </p>

          <p className="mt-2 text-slate-600">
            {t.acceptableUseAiText2 ||
              "Users remain fully responsible for verifying outputs before relying on them."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.acceptableUseResponsibilityTitle || "5. User Responsibility"}
          </h2>

          <p className="mt-2 text-slate-600">
            {t.acceptableUseResponsibilityText ||
              "Users are responsible for all content uploaded, processed, generated, or shared through the services and for ensuring they have the legal right to use such content."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.acceptableUseEnforcementTitle || "6. Enforcement"}
          </h2>

          <p className="mt-2 text-slate-600">
            {t.acceptableUseEnforcementText ||
              "Runexa Systems LLC may investigate suspected violations of this Policy and may suspend, restrict, or terminate access to the services at its sole discretion."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.acceptableUseReportingTitle || "7. Reporting Violations"}
          </h2>

          <p className="mt-2 text-slate-600">
            {t.acceptableUseReportingText ||
              "Suspected violations or abuse may be reported to:"}
          </p>

          <p className="mt-2 text-slate-600">
            contact@runexa.ai
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.acceptableUseChangesTitle || "8. Changes"}
          </h2>

          <p className="mt-2 text-slate-600">
            {t.acceptableUseChangesText ||
              "Runexa Systems LLC may update this Policy at any time. Updated versions will be posted with a revised “Last updated” date."}
          </p>
        </section>
      </div>
    </main>
  );
}
