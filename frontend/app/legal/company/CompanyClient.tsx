"use client";

import { useEffect, useState } from "react";
import type { Metadata } from "next";
import {
  defaultLocale,
  getSavedLocale,
  getTranslations,
} from "../../../lib/i18n";

export const metadata: Metadata = {
  title: "Company Information | Runexa Systems",

  description:
    "Official company information for Runexa Systems LLC, including registered address, contact details, services, and governing law.",

  keywords: [
    "Runexa Systems LLC",
    "Runexa company information",
    "Runexa contact",
    "Runexa registered address",
    "Runexa legal information",
    "AI company information",
  ],

  alternates: {
    canonical: "https://runexa.ai/legal/company",
  },

  openGraph: {
    title: "Company Information | Runexa Systems",

    description:
      "Official company information for Runexa Systems LLC, including registered address, contact details, services, and governing law.",

    url: "https://runexa.ai/legal/company",

    siteName: "Runexa Systems",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Systems Company Information",
      },
    ],

    locale: "en_US",

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Company Information | Runexa Systems",

    description:
      "Official company details, registered address, contact information, and governing law for Runexa Systems LLC.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

const jsonLd = {
  "@context": "https://schema.org",

  "@type": "Organization",

  name: "Runexa Systems LLC",

  url: "https://runexa.ai",

  email: "contact@runexa.ai",

  address: {
    "@type": "PostalAddress",
    streetAddress: "1309 Coffeen Avenue, Suite 1200",
    addressLocality: "Sheridan",
    addressRegion: "WY",
    postalCode: "82801",
    addressCountry: "US",
  },

  description:
    "Runexa Systems LLC develops and operates AI-powered tools, applications, AI agents, and related software services.",
};

export default function CompanyClient() {
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
