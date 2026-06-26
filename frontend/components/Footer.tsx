"use client";

import Link from "next/link";
import Image from "next/image";
import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";
import { getSavedLocale } from "../lib/i18n";

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

type FooterCopy = {
  slogan: string;
  footerDesc: string;
  companyAddress: string;
  products: string;
  resources: string;
  developers: string;
  docs: string;
  apiDashboard: string;
  platform: string;
  about: string;
  available: string;
  legalAgent: string;
  studyAgent: string;
  financeAgent: string;
  businessAgent: string;
  legalResource: string;
  financeResource: string;
  studyResource: string;
  businessResource: string;
  blog: string;
  studyDemo: string;
  financeDemo: string;
  legalDemo: string;
  businessDemo: string;
  exploreAgents: string;
  tryLegalAgent: string;
  tryStudyAgent: string;
  tryFinanceAgent: string;
  login: string;
  register: string;
  aboutText: string;
  builtBy: string;
  aboutPage: string;
  copyright: string;
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

const footerCopy: Record<Locale, FooterCopy> = {
  en: {
    slogan: "Specialized AI agents for real-world work",
    footerDesc:
      "Specialized AI agents for legal analysis, financial intelligence, learning, and enterprise decision support.",
    companyAddress:
      "Runexa Systems LLC\n1309 Coffeen Avenue, Suite 1200\nSheridan, WY 82801, USA",
    products: "Products",
    resources: "Resources",
    developers: "Developers",
    docs: "Docs",
    apiDashboard: "API Dashboard",
    platform: "Platform",
    about: "About",
    available: "Available",
    legalAgent: "Runexa Legal Agent",
    studyAgent: "Runexa Study Workspace",
    financeAgent: "Runexa Finance Intelligence Agent",
    businessAgent: "Runexa Business Decision Intelligence",
    legalResource: "Runexa Legal Agent",
    financeResource: "Runexa Finance Intelligence Agent",
    studyResource: "Runexa Study Workspace",
    businessResource: "Runexa Business Decision Intelligence",
    blog: "Blog",
    studyDemo: "Runexa Study Workspace Demo",
    financeDemo: "Runexa Finance Intelligence Demo",
    legalDemo: "Runexa Legal Agent Demo",
    businessDemo: "Runexa Business Decision Intelligence Demo",
    exploreAgents: "Explore agents",
    tryLegalAgent: "Try Runexa Legal Agent",
    tryStudyAgent: "Try Runexa Study Workspace",
    tryFinanceAgent: "Try Runexa Finance Intelligence Agent",
    login: "Login",
    register: "Register",
    aboutText:
      "Runexa Systems is an AI platform that provides specialized AI agents to help users analyze documents, learn faster, gain financial intelligence, and make smarter business decisions.",
    builtBy: "Built by Dr. Rachid Ejjami",
    aboutPage: "About Runexa",
    copyright: "© 2026 Runexa Systems LLC. All rights reserved.",
  },
  fr: {
    slogan: "Des agents IA spécialisés pour le travail réel",
    footerDesc:
      "Des agents IA spécialisés pour l’analyse juridique, l’intelligence financière, l’apprentissage et l’aide à la décision en entreprise.",
    companyAddress:
      "Runexa Systems LLC\n1309 Coffeen Avenue, Suite 1200\nSheridan, WY 82801, États-Unis",
    products: "Produits",
    resources: "Ressources",
    developers: "Développeurs",
    docs: "Documentation",
    apiDashboard: "Tableau de bord API",
    platform: "Plateforme",
    about: "À propos",
    available: "Disponible",
    legalAgent: "Runexa Legal Agent",
    studyAgent: "Runexa Study Workspace",
    financeAgent: "Runexa Finance Intelligence Agent",
    businessAgent: "Runexa Business Decision Intelligence",
    legalResource: "Runexa Legal Agent",
    financeResource: "Runexa Finance Intelligence Agent",
    studyResource: "Runexa Study Workspace",
    businessResource: "Runexa Business Decision Intelligence",
    blog: "Blog",
    studyDemo: "Démo Runexa Study Workspace",
    financeDemo: "Démo Runexa Finance Intelligence",
    legalDemo: "Démo Runexa Legal Agent",
    businessDemo: "Démo Runexa Business Decision Intelligence",
    exploreAgents: "Explorer les agents",
    tryLegalAgent: "Tester Runexa Legal Agent",
    tryStudyAgent: "Tester Runexa Study Workspace",
    tryFinanceAgent: "Tester Runexa Finance Intelligence Agent",
    login: "Connexion",
    register: "Inscription",
    aboutText:
      "Runexa Systems est une plateforme d’IA proposant des agents spécialisés pour aider les utilisateurs à analyser leurs documents, apprendre plus vite, mieux comprendre leurs données financières et prendre de meilleures décisions.",
    builtBy: "Développé par le Dr Rachid Ejjami",
    aboutPage: "À propos de Runexa",
    copyright: "© 2026 Runexa Systems LLC. Tous droits réservés.",
  },
  ar: {
    slogan: "وكلاء ذكاء اصطناعي متخصصون للعمل الواقعي",
    footerDesc:
      "وكلاء ذكاء اصطناعي متخصصون للتحليل القانوني والذكاء المالي والتعلم ودعم اتخاذ القرار في المؤسسات.",
    companyAddress:
      "Runexa Systems LLC\n1309 Coffeen Avenue, Suite 1200\nSheridan, WY 82801, الولايات المتحدة",
    products: "المنتجات",
    resources: "الموارد",
    developers: "المطورون",
    docs: "التوثيق",
    apiDashboard: "لوحة تحكم API",
    platform: "المنصة",
    about: "حول",
    available: "متاح",
    legalAgent: "Runexa Legal Agent",
    studyAgent: "Runexa Study Workspace",
    financeAgent: "Runexa Finance Intelligence Agent",
    businessAgent: "Runexa Business Decision Intelligence",
    legalResource: "Runexa Legal Agent",
    financeResource: "Runexa Finance Intelligence Agent",
    studyResource: "Runexa Study Workspace",
    businessResource: "Runexa Business Decision Intelligence",
    blog: "المدونة",
    studyDemo: "عرض Runexa Study Workspace",
    financeDemo: "عرض Runexa Finance Intelligence",
    legalDemo: "عرض Runexa Legal Agent",
    businessDemo: "عرض Runexa Business Decision Intelligence",
    exploreAgents: "استكشاف الوكلاء",
    tryLegalAgent: "تجربة Runexa Legal Agent",
    tryStudyAgent: "تجربة Runexa Study Workspace",
    tryFinanceAgent: "تجربة Runexa Finance Intelligence Agent",
    login: "تسجيل الدخول",
    register: "إنشاء حساب",
    aboutText:
      "Runexa Systems منصة ذكاء اصطناعي توفر وكلاء متخصصين لمساعدة المستخدمين على تحليل المستندات والتعلم بشكل أسرع وفهم البيانات المالية واتخاذ قرارات أكثر ذكاءً.",
    builtBy: "من تطوير الدكتور رشيد الجامعي",
    aboutPage: "عن Runexa",
    copyright: "© 2026 Runexa Systems LLC. جميع الحقوق محفوظة.",
  },
};

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

    const savedApiEnabled = localStorage.getItem("api_enabled") === "true";
    setApiEnabled(savedApiEnabled);

    const handleLocaleChange = () => {
      setLocale(resolveLocale());
    };

    window.addEventListener("locale-change", handleLocaleChange);

    return () => {
      window.removeEventListener("locale-change", handleLocaleChange);
    };
  }, [pathname]);

  const t = footerCopy[locale] || footerCopy.en;
  const legal = legalLabels[locale] || legalLabels.en;

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
                {t.studyAgent}{" "}
                <span className="text-green-400">· {t.available}</span>
              </Link>

              <Link href="/finance" className="block hover:text-white transition">
                {t.financeAgent}{" "}
                <span className="text-green-400">· {t.available}</span>
              </Link>

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
                {t.legalResource}
              </Link>

              <Link href="/finance-ai" className="block hover:text-white transition">
                {t.financeResource}
              </Link>

              <Link href="/study-ai" className="block hover:text-white transition">
                {t.studyResource}
              </Link>

              <Link href="/business-ai" className="block hover:text-white transition">
                {t.businessResource}
              </Link>

              <Link href="/blog" className="block hover:text-white transition">
                {t.blog}
              </Link>

              <Link
                href={localizedHref("/demo/study-agent")}
                className="block hover:text-white transition"
              >
                {t.studyDemo}
              </Link>

              <Link
                href={localizedHref("/demo/finance-agent")}
                className="block hover:text-white transition"
              >
                {t.financeDemo}
              </Link>

              <Link
                href={localizedHref("/demo/legal-agent")}
                className="block hover:text-white transition"
              >
                {t.legalDemo}
              </Link>

              <Link
                href={localizedHref("/demo/business-agent")}
                className="block hover:text-white transition"
              >
                {t.businessDemo}
              </Link>

              <Link href="/developers" className="block hover:text-white transition">
                {t.developers}
              </Link>

              <Link href="/api" className="block hover:text-white transition">
                API
              </Link>

              <Link href="/docs" className="block hover:text-white transition">
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
                {t.tryStudyAgent}
              </Link>

              <Link href="/finance" className="block hover:text-white transition">
                {t.tryFinanceAgent}
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

            <Link
              href={localizedHref("/about")}
              className="mt-5 inline-block text-sm font-semibold text-blue-400 hover:text-blue-300 transition"
            >
              {t.aboutPage}
            </Link>
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
