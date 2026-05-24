"use client";

import Link from "next/link";
import Image from "next/image";
import { useEffect, useState } from "react";
import { getSavedLocale, translations } from "../lib/i18n";

export default function Footer() {
  const [locale, setLocale] = useState("en");
  const [apiEnabled, setApiEnabled] = useState(false);

  useEffect(() => {
    setLocale(getSavedLocale());

    const savedApiEnabled =
      localStorage.getItem("api_enabled") === "true";

    setApiEnabled(savedApiEnabled);

    const handleLocaleChange = () => {
      setLocale(getSavedLocale());
    };

    window.addEventListener("locale-change", handleLocaleChange);

    return () => {
      window.removeEventListener("locale-change", handleLocaleChange);
    };
  }, []);

  const t = translations[locale] || translations.en;

  const legalLabels: any = {
    en: {
      terms: "Terms",
      privacy: "Privacy Policy",
      productTerms: "Product Terms",
      acceptableUse: "Acceptable Use",
      aiDisclaimer: "AI Disclaimer",
      cookies: "Cookie Policy",
      refunds: "Refund Policy",
      security: "Security",
      company: "Company Information",
    },
    fr: {
      terms: "Conditions",
      privacy: "Confidentialité",
      productTerms: "Conditions produit",
      acceptableUse: "Utilisation acceptable",
      aiDisclaimer: "Avertissement IA",
      cookies: "Politique cookies",
      refunds: "Remboursements",
      security: "Sécurité",
      company: "Informations société",
    },
    ar: {
      terms: "الشروط",
      privacy: "الخصوصية",
      productTerms: "شروط المنتج",
      acceptableUse: "الاستخدام المقبول",
      aiDisclaimer: "إخلاء مسؤولية الذكاء الاصطناعي",
      cookies: "سياسة ملفات تعريف الارتباط",
      refunds: "سياسة الاسترداد",
      security: "الأمان",
      company: "معلومات الشركة",
    },
  };

  const legal = legalLabels[locale] || legalLabels.en;

  return (
    <footer
      dir={locale === "ar" ? "rtl" : "ltr"}
      className="bg-slate-950 text-white px-6 py-14"
    >
      <div className="max-w-7xl mx-auto">
        <div className="grid gap-10 md:grid-cols-2 lg:grid-cols-5">
          <div>
            <Link href="/" className="inline-flex">
              <Image
                src="/runexa.svg"
                alt="Runexa Systems"
                width={300}
                height={90}
                className="h-14 w-auto object-contain brightness-0 invert opacity-95"
              />
            </Link>

            <p className="mt-3 text-xs font-medium text-slate-400">
              {t.slogan}
            </p>

            <p className="mt-4 text-sm text-slate-400 leading-6">
              {t.footerDesc}
            </p>

            <p className="mt-4 text-xs text-slate-500 leading-5 whitespace-pre-line">
              {t.companyAddress}
            </p>
          </div>

          <div>
            <h4 className="font-semibold">{t.products}</h4>

            <div className="mt-4 space-y-3 text-sm text-slate-400">
              <Link href="/upload" className="block hover:text-white transition">
                {t.legalAgent}{" "}
                <span className="text-green-400">· {t.available}</span>
              </Link>

              <Link href="/study" className="block hover:text-white transition">
                {(t.studyAgent || "Study Agent")}{" "}
                <span className="text-green-400">· {t.available}</span>
              </Link>

              <Link href="/finance" className="block hover:text-white transition">
                {(t.financeAgent === t.studyAgent
                  ? "Personal Finance Coach Agent"
                  : t.financeAgent || "Personal Finance Coach Agent")}{" "}
                <span className="text-green-400">· {t.available}</span>
              </Link>

              {/* ✅ UPDATED BUSINESS */}
              <Link href="/business" className="block hover:text-white transition">
                {t.businessAgent}{" "}
                <span className="text-green-400">· {t.available}</span>
              </Link>
            </div>
          </div>

          <div>
            <h4 className="font-semibold">Resources</h4>

            <div className="mt-4 space-y-3 text-sm text-slate-400">
              <Link href="/legal-ai" className="block hover:text-white transition">
                Legal AI
              </Link>

              <Link href="/finance-ai" className="block hover:text-white transition">
                Finance AI
              </Link>

              <Link href="/study-ai" className="block hover:text-white transition">
                Study AI
              </Link>

              <Link href="/business-ai" className="block hover:text-white transition">
                Business AI
              </Link>

              <Link
                href="/blog"
                className="block hover:text-white transition"
              >
                Blog
              </Link>

              <Link
                href="/developers"
                className="block hover:text-white transition"
              >
                Developers
              </Link>

              <Link
                href="/api"
                className="block hover:text-white transition"
              >
                API
              </Link>

              <Link
                href="/docs"
                className="block hover:text-white transition"
              >
                Docs
              </Link>

              {apiEnabled && (
                <Link
                  href="/api-dashboard"
                  className="block hover:text-white transition"
                >
                  {locale === "fr"
                    ? "Dashboard API"
                    : locale === "ar"
                    ? "لوحة API"
                    : "API Dashboard"}
                </Link>
              )}
            </div>
          </div>

          <div>
            <h4 className="font-semibold">{t.platform}</h4>

            <div className="mt-4 space-y-3 text-sm text-slate-400">
              <a href="#agents" className="block hover:text-white transition">
                {t.exploreAgents}
              </a>

              <Link href="/upload" className="block hover:text-white transition">
                {t.tryLegalAgent}
              </Link>

              <Link href="/study" className="block hover:text-white transition">
                {t.tryStudyAgent || "Try Study Agent"}
              </Link>

              <Link href="/finance" className="block hover:text-white transition">
                {t.tryFinanceAgent || "Try Finance Coach"}
              </Link>

              <Link href="/login" className="block hover:text-white transition">
                {t.login}
              </Link>

              <Link href="/register" className="block hover:text-white transition">
                {t.register}
              </Link>
            </div>
          </div>

          <div>
            <h4 className="font-semibold">{t.about}</h4>

            <p className="mt-4 text-sm text-slate-400 leading-6">
              {t.aboutText}
            </p>

            <p className="mt-4 text-sm font-medium text-blue-400">
              {t.developedBy}
            </p>
          </div>
        </div>

        <div className="mt-12 border-t border-slate-800 pt-6 flex flex-col gap-4 text-sm text-slate-500 md:flex-row md:items-center md:justify-between">
          <p>{t.copyright}</p>

          <div className="flex flex-wrap gap-5">
            <Link href="/terms" className="hover:text-white transition">
              {legal.terms}
            </Link>

            <Link href="/privacy" className="hover:text-white transition">
              {legal.privacy}
            </Link>

            <Link
              href="/products/ai-legal-agent/terms"
              className="hover:text-white transition"
            >
              {legal.productTerms}
            </Link>

            <Link href="/legal/acceptable-use" className="hover:text-white transition">
              {legal.acceptableUse}
            </Link>

            <Link href="/legal/ai-disclaimer" className="hover:text-white transition">
              {legal.aiDisclaimer}
            </Link>

            <Link href="/legal/cookies" className="hover:text-white transition">
              {legal.cookies}
            </Link>

            <Link href="/legal/refunds" className="hover:text-white transition">
              {legal.refunds}
            </Link>

            <Link href="/security" className="hover:text-white transition">
              {legal.security}
            </Link>

            <Link href="/legal/company" className="hover:text-white transition">
              {legal.company}
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}