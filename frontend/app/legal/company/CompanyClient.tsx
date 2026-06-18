"use client";

import { useEffect, useState } from "react";
import {
  defaultLocale,
  getSavedLocale,
  getTranslations,
} from "../../../lib/i18n";

type Locale = "en" | "fr" | "ar";

type LegalTranslations = Record<string, string>;

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

export default function CompanyClient({
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

  const t = getTranslations(locale) as LegalTranslations;

  return (
    <main
      dir={locale === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-4 py-12"
    >
      <div className="mx-auto max-w-3xl space-y-8 rounded-3xl border bg-white p-8 shadow-sm">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">
            {t.companyInfoTitle || "Company Information"}
          </h1>

          <p className="mt-2 text-sm text-slate-500">
            {t.companyInfoUpdated || "Last updated: May 2026"}
          </p>
        </div>

        <section>
          <h2 className="text-xl font-semibold">
            {t.companySectionTitle || "1. Company"}
          </h2>

          <p className="mt-2 text-slate-600">
            Runexa Systems LLC
          </p>

          <p className="mt-2 text-slate-600">
            {t.companySectionText ||
              "AI agents platform providing AI-powered tools and services."}
          </p>

          <p className="mt-2 text-slate-600">
            Website: https://runexa.ai
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.companyAddressTitle || "2. Registered Address"}
          </h2>

          <p className="mt-2 text-slate-600">
            1309 Coffeen Avenue, Suite 1200
            <br />
            Sheridan, WY 82801
            <br />
            {locale === "fr"
              ? "États-Unis"
              : locale === "ar"
              ? "الولايات المتحدة"
              : "United States"}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.companyContactTitle || "3. Contact Information"}
          </h2>

          <p className="mt-2 text-slate-600">
            {t.companyContactText || "General Contact"}: contact@runexa.ai
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.companyServicesTitle || "4. Services"}
          </h2>

          <p className="mt-2 text-slate-600">
            {t.companyServicesText ||
              "Runexa Systems LLC develops and operates AI-powered tools, applications, AI agents, and related software services."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.companyLawTitle || "5. Governing Law"}
          </h2>

          <p className="mt-2 text-slate-600">
            {t.companyLawText ||
              "Services provided by Runexa Systems LLC are governed by the laws of the State of Wyoming, United States."}
          </p>
        </section>
      </div>
    </main>
  );
}
