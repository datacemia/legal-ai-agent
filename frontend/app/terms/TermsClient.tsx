"use client";

import { useEffect, useState } from "react";
import {
  defaultLocale,
  getSavedLocale,
  getTranslations,
} from "../../lib/i18n";

type Locale = "en" | "fr" | "ar";

type TermsTranslations = Record<string, string>;

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

const termsEligibilityText: Record<Locale, string> = {
  en:
    "The Services are not intended for children under 13. Individuals aged 13 to 17 may use the Services only with consent and supervision of a parent or legal guardian.",

  fr:
    "Les Services ne sont pas destinés aux enfants de moins de 13 ans. Les personnes âgées de 13 à 17 ans peuvent utiliser les Services uniquement avec le consentement et la supervision d’un parent ou tuteur légal.",

  ar:
    "الخدمات غير مخصصة للأطفال دون سن 13 عاماً. يمكن للأفراد الذين تتراوح أعمارهم بين 13 و17 عاماً استخدام الخدمات فقط بموافقة وإشراف أحد الوالدين أو الوصي القانوني.",
};

const termsDataUsageText: Record<Locale, string> = {
  en:
    "You retain ownership of the data and content you upload. Runexa Systems LLC processes your data to provide, secure, operate, maintain, and support the services, as described in the Privacy Policy.",

  fr:
    "Vous conservez la propriété des données et contenus que vous téléchargez. Runexa Systems LLC traite vos données afin de fournir, sécuriser, exploiter, maintenir et soutenir les services, comme décrit dans la Politique de confidentialité.",

  ar:
    "تحتفظ بملكية البيانات والمحتوى الذي ترفعه. تقوم Runexa Systems LLC بمعالجة بياناتك لتقديم الخدمات وتأمينها وتشغيلها وصيانتها ودعمها، كما هو موضح في سياسة الخصوصية.",
};

export default function TermsClient({
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

  const t = getTranslations(locale) as TermsTranslations;

  return (
    <main
      dir={locale === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-4 py-12"
    >
      <div className="max-w-3xl mx-auto bg-white p-8 rounded-3xl border shadow-sm space-y-8">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">
            {t.termsTitle || "Terms of Service"}
          </h1>

          <p className="text-sm text-slate-500 mt-2">
            {t.termsUpdated || "Last updated: May 2026"}
          </p>
        </div>

        <section>
          <h2 className="text-xl font-semibold">
            {t.termsOverviewTitle || "1. Overview"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.termsOverviewText1 ||
              "Runexa Systems LLC provides access to AI-powered tools designed to assist users in analyzing documents, generating insights, and using specialized AI agents."}
          </p>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.termsOverviewText2 ||
              "By accessing or using Runexa, you agree to these Terms of Service."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.termsEligibilityTitle || "2. Eligibility"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {termsEligibilityText[locale]}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.termsAccountTitle || "3. Account"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.termsAccountText ||
              "You are responsible for maintaining the security of your account, your login credentials, and all activity under your account."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.termsUseTitle || "4. Use of Services"}
          </h2>

          <ul className="mt-2 list-disc pl-5 text-slate-600 space-y-1">
            <li>
              {t.termsUse1 ||
                "You may not use the services for illegal, harmful, or fraudulent activity."}
            </li>
            <li>
              {t.termsUse2 ||
                "You may not upload data, documents, or content that you do not have the right to use."}
            </li>
            <li>
              {t.termsUse3 ||
                "You may not abuse, disrupt, reverse engineer, or attempt to bypass the platform."}
            </li>
            <li>
              {t.termsUse4 ||
                "You may not use the services to infringe intellectual property, privacy, or third-party rights."}
            </li>
          </ul>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.termsAiTitle || "5. AI Services"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.termsAiText1 ||
              "AI-generated outputs may be inaccurate, incomplete, outdated, or misleading. Outputs may contain errors or omissions."}
          </p>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.termsAiText2 ||
              "You are responsible for independently reviewing and verifying all outputs before relying on them or taking action."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.termsBillingTitle || "6. Payments, Credits, and Billing"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.termsBillingText ||
              "Paid trials, credits, subscriptions, and plans are subject to the pricing shown at the time of purchase. Credits are non-refundable unless required by law."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.termsDataTitle || "7. Data Usage"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {termsDataUsageText[locale]}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.termsIpTitle || "8. Intellectual Property"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.termsIpText ||
              "Runexa Systems LLC owns all rights, title, and interest in the platform, software, interfaces, designs, branding, AI agent workflows, and related technology."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.termsLiabilityTitle || "9. Limitation of Liability"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.termsLiabilityText ||
              "To the maximum extent permitted by law, Runexa Systems LLC is not liable for indirect, incidental, special, consequential, or punitive damages, including business losses, financial losses, legal disputes, loss of data, or consequences resulting from misuse or reliance on AI outputs."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.termsTerminationTitle || "10. Termination"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.termsTerminationText ||
              "Runexa Systems LLC may suspend or terminate access to the services if these Terms are violated or if use of the services creates legal, security, operational, or reputational risk."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.termsLawTitle || "11. Governing Law"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.termsLawText ||
              "These Terms are governed by the laws of the State of Wyoming, United States, without regard to conflict of law principles."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.termsChangesTitle || "12. Changes"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.termsChangesText ||
              "Runexa Systems LLC may update these Terms from time to time. Updated Terms will be posted on this page with a revised “Last updated” date."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.termsContactTitle || "13. Contact"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            contact@runexa.ai
          </p>
        </section>
      </div>
    </main>
  );
}
