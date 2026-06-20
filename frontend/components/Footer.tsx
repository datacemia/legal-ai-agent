"use client";

import Link from "next/link";
import Image from "next/image";
import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";
import { getSavedLocale, translations } from "../lib/i18n";

type Locale = "en" | "fr" | "ar";

type LegalLabels = {
  terms: string;
  privacy: string;
  productTerms: string;
  acceptableUse: string;
  aiDisclaimer: string;
  cookies: string;
  refunds: string;
  security: string;
  company: string;
};

const getLocaleFromPathname = (pathname: string | null): Locale | null => {
  if (!pathname) {
    return null;
  }

  if (pathname === "/en" || pathname.startsWith("/en/")) {
    return "en";
  }

  if (pathname === "/fr" || pathname.startsWith("/fr/")) {
    return "fr";
  }

  if (pathname === "/ar" || pathname.startsWith("/ar/")) {
    return "ar";
  }

  return null;
};

const normalizeLocale = (
  value: string | null | undefined,
  fallback: Locale = "en"
): Locale => {
  if (value === "en" || value === "fr" || value === "ar") {
    return value;
  }

  return fallback;
};

export default function Footer() {
  const pathname = usePathname();

  const [locale, setLocale] = useState<Locale>("en");
  const [apiEnabled, setApiEnabled] = useState(false);

  const resolveLocale = (): Locale => {
    const pathLocale = getLocaleFromPathname(pathname);

    if (pathLocale) {
      return pathLocale;
    }

    return normalizeLocale(getSavedLocale(), "en");
  };

  useEffect(() => {
    setLocale(resolveLocale());

    const savedApiEnabled =
      localStorage.getItem("api_enabled") === "true";

    setApiEnabled(savedApiEnabled);

    const handleLocaleChange = () => {
      setLocale(resolveLocale());
    };

    window.addEventListener("locale-change", handleLocaleChange);

    return () => {
      window.removeEventListener("locale-change", handleLocaleChange);
    };
  }, [pathname]);

  const t = translations[locale] || translations.en;

  const legalLabels: Record<Locale, LegalLabels> = {
    en: {
      terms: "Terms of Service",
      privacy: "Privacy Policy",
      productTerms: "Product Terms",
      acceptableUse: "Acceptable Use Policy",
      aiDisclaimer: "AI Disclaimer",
      cookies: "Cookie Policy",
      refunds: "Refund Policy",
      security: "Security",
      company: "Company Information",
    },
    fr: {
      terms: "Conditions d’utilisation",
      privacy: "Politique de confidentialité",
      productTerms: "Conditions du produit",
      acceptableUse: "Politique d’utilisation acceptable",
      aiDisclaimer: "Avertissement relatif à l’IA",
      cookies: "Politique relative aux cookies",
      refunds: "Politique de remboursement",
      security: "Sécurité",
      company: "Informations sur l’entreprise",
    },
    ar: {
      terms: "شروط الاستخدام",
      privacy: "سياسة الخصوصية",
      productTerms: "شروط المنتج",
      acceptableUse: "سياسة الاستخدام المقبول",
      aiDisclaimer: "إخلاء مسؤولية الذكاء الاصطناعي",
      cookies: "سياسة ملفات تعريف الارتباط",
      refunds: "سياسة الاسترداد",
      security: "الأمان",
      company: "معلومات الشركة",
    },
  };

  const legal = legalLabels[locale] || legalLabels.en;

  const demoLabels: Record<Locale, string> = {
    en: "Study Agent Demo",
    fr: "Démo Agent d’Étude",
    ar: "عرض وكيل الدراسة",
  };

  const demoLabel = demoLabels[locale] || demoLabels.en;

  const localizedHref = (href: string) => {
    if (pathname === "/en" || pathname?.startsWith("/en/")) {
      return `/en${href}`;
    }

    if (pathname === "/fr" || pathname?.startsWith("/fr/")) {
      return `/fr${href}`;
    }

    if (pathname === "/ar" || pathname?.startsWith("/ar/")) {
      return `/ar${href}`;
    }

    return href;
  };

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
            <h4 className="font-semibold">{t.resources}</h4>

            <div className="mt-4 space-y-3 text-sm text-slate-400">
              <Link href="/legal-ai" className="block hover:text-white transition">
                {t.legalAi}
              </Link>

              <Link href="/finance-ai" className="block hover:text-white transition">
                {t.financeAi}
              </Link>

              <Link href="/study-ai" className="block hover:text-white transition">
                {t.studyAi}
              </Link>

              <Link href="/business-ai" className="block hover:text-white transition">
                {t.businessAi}
              </Link>

              <Link
                href="/blog"
                className="block hover:text-white transition"
              >
                {t.blog}
              </Link>

              <Link
                href={localizedHref("/demo/study-agent")}
                className="block hover:text-white transition"
              >
                {demoLabel}
              </Link>

              <Link
                href="/developers"
                className="block hover:text-white transition"
              >
                {t.developers}
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
                {t.docs}
              </Link>

              {apiEnabled && (
                <Link
                  href="/api-dashboard"
                  className="block hover:text-white transition"
                >
                  {t.apiDashboard}
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
              {t.builtBy}
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
