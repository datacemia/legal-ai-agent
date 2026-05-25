"use client";

import { useEffect, useState } from "react";
import {
  defaultLocale,
  getSavedLocale,
  getTranslations,
} from "../../../lib/i18n";

export default function RefundPolicyClient() {
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
            {t.refundTitle || "Refund Policy"}
          </h1>

          <p className="text-sm text-slate-500 mt-2">
            {t.refundUpdated || "Last updated: May 2026"}
          </p>
        </div>

        <section>
          <h2 className="text-xl font-semibold">
            {t.refundOverviewTitle || "1. Overview"}
          </h2>

          <p className="mt-2 text-slate-600">
            {t.refundOverviewText ||
              "This Refund Policy applies to purchases, credits, subscriptions, trials, and other paid services offered by Runexa Systems LLC."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.refundTrialsTitle || "2. Trials and Credits"}
          </h2>

          <p className="mt-2 text-slate-600">
            {t.refundTrialsText1 ||
              "Trial purchases, activation fees, AI credits, and usage-based purchases are generally non-refundable unless required by applicable law."}
          </p>

          <p className="mt-2 text-slate-600">
            {t.refundTrialsText2 ||
              "Users are responsible for reviewing product descriptions and pricing before purchasing."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.refundSubscriptionTitle || "3. Subscription Services"}
          </h2>

          <p className="mt-2 text-slate-600">
            {t.refundSubscriptionText1 ||
              "Subscription plans may renew automatically unless canceled before the next billing cycle."}
          </p>

          <p className="mt-2 text-slate-600">
            {t.refundSubscriptionText2 ||
              "Users may cancel subscriptions at any time, but fees already paid are generally non-refundable."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.refundChargesTitle || "4. Failed or Duplicate Charges"}
          </h2>

          <p className="mt-2 text-slate-600">
            {t.refundChargesText ||
              "If you believe you were charged incorrectly, charged multiple times, or experienced a billing error, please contact us for review."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.refundAbuseTitle || "5. Chargebacks and Abuse"}
          </h2>

          <p className="mt-2 text-slate-600">
            {t.refundAbuseText ||
              "Fraudulent chargebacks, payment abuse, or attempts to improperly reverse payments may result in suspension or termination of access to the services."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.refundAvailabilityTitle || "6. Service Availability"}
          </h2>

          <p className="mt-2 text-slate-600">
            {t.refundAvailabilityText ||
              "Temporary outages, AI inaccuracies, delays, model limitations, or feature changes do not automatically qualify for refunds."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.refundExceptionsTitle || "7. Exceptions"}
          </h2>

          <p className="mt-2 text-slate-600">
            {t.refundExceptionsText ||
              "Runexa Systems LLC may, at its sole discretion, provide refunds, credits, or account adjustments in exceptional situations."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.refundChangesTitle || "8. Changes"}
          </h2>

          <p className="mt-2 text-slate-600">
            {t.refundChangesText ||
              "Runexa Systems LLC may update this Refund Policy from time to time. Updated versions will be posted with a revised “Last updated” date."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.refundContactTitle || "9. Contact"}
          </h2>

          <p className="mt-2 text-slate-600">
            contact@runexa.ai
          </p>
        </section>
      </div>
    </main>
  );
}
