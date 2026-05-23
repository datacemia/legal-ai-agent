"use client";

import Link from "next/link";
import Image from "next/image";
import { useEffect, useState } from "react";
import { getSavedLocale, translations } from "../lib/i18n";

export default function Navbar() {
  const [isLogged, setIsLogged] = useState(false);
  const [role, setRole] = useState("");
  const [plan, setPlan] = useState("");
  const [credits, setCredits] = useState<string | null>(null);
  const [isEnterpriseMember, setIsEnterpriseMember] = useState(false);
  const [locale, setLocale] = useState("en");

  const checkAuth = () => {
    const token = localStorage.getItem("token");

    const savedRole = (localStorage.getItem("role") || "")
      .toLowerCase()
      .trim();

    const savedPlan = (localStorage.getItem("plan") || "trial")
      .toLowerCase()
      .trim();

    const savedCredits = localStorage.getItem("credits_balance");

    const savedEnterpriseMember =
      localStorage.getItem("enterprise_member") === "true";

    setIsLogged(!!token);
    setRole(savedRole);
    setPlan(savedPlan);
    setCredits(savedCredits);
    setIsEnterpriseMember(savedEnterpriseMember);
  };

  useEffect(() => {
    checkAuth();
    setLocale(getSavedLocale());

    window.addEventListener("storage", checkAuth);

    const handleLocaleChange = () => {
      setLocale(getSavedLocale());
    };

    window.addEventListener("locale-change", handleLocaleChange);

    return () => {
      window.removeEventListener("storage", checkAuth);
      window.removeEventListener("locale-change", handleLocaleChange);
    };
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    localStorage.removeItem("plan");
    localStorage.removeItem("credits_balance");
    localStorage.removeItem("enterprise_member");

    setIsLogged(false);
    setRole("");
    setPlan("");
    setCredits(null);
    setIsEnterpriseMember(false);

    window.location.href = "/login";
  };

  const t = translations[locale] || translations.en;

  const navbarSlogan =
    locale === "fr"
      ? "Des agents IA spécialisés pour le travail réel"
      : locale === "ar"
      ? "وكلاء ذكاء اصطناعي متخصصون للعمل الواقعي"
      : "Specialized AI agents for real-world work";

  const enterpriseLabel =
    locale === "fr"
      ? "Entreprise"
      : locale === "ar"
      ? "المؤسسات"
      : "Enterprise";

  const solutionsLabel =
    locale === "fr"
      ? "Solutions"
      : locale === "ar"
      ? "الحلول"
      : "Solutions";

  const solutionLinks = [
    {
      label:
        locale === "fr"
          ? "IA juridique"
          : locale === "ar"
          ? "الذكاء القانوني"
          : "Legal AI",
      href: "/legal-ai",
    },
    {
      label:
        locale === "fr"
          ? "IA finance"
          : locale === "ar"
          ? "الذكاء المالي"
          : "Finance AI",
      href: "/finance-ai",
    },
    {
      label:
        locale === "fr"
          ? "IA étude"
          : locale === "ar"
          ? "ذكاء الدراسة"
          : "Study AI",
      href: "/study-ai",
    },
    {
      label:
        locale === "fr"
          ? "IA business"
          : locale === "ar"
          ? "ذكاء الأعمال"
          : "Business AI",
      href: "/business-ai",
    },
  ];

  const isAdmin = role === "admin";
  const isEnterpriseAdmin = role === "enterprise_admin";
  const canSeeEnterprise = isEnterpriseAdmin || isEnterpriseMember;

  const isPaid = plan === "paid";
  const isPro = plan === "pro";
  const isPremium = plan === "premium";

  const canSeeDashboard =
    isAdmin ||
    canSeeEnterprise ||
    isPaid ||
    isPro ||
    isPremium;

  return (
    <header
      dir={locale === "ar" ? "rtl" : "ltr"}
      className="sticky top-0 z-50 w-full border-b border-slate-200/70 bg-white/70 backdrop-blur-md"
    >
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">

        {/* LOGO */}
        <Link href="/" className="flex items-center gap-3">
          <Image
            src="/runexa.svg"
            alt="Runexa AI Workspace"
            width={300}
            height={90}
            priority
            className="h-12 w-auto object-contain"
          />

          <span className="hidden lg:block text-xs font-medium text-slate-500">
            {navbarSlogan}
          </span>
        </Link>

        <div className="flex items-center gap-5">

          {canSeeDashboard && !canSeeEnterprise && (
            <Link
              href="/dashboard"
              className="text-sm font-medium text-slate-600 transition hover:text-slate-900"
            >
              {t.dashboard || "Dashboard"}
            </Link>
          )}

          {/* ✅ ENTERPRISE DASHBOARD */}
          {canSeeEnterprise && (
            <Link
              href="/entreprises/dashboard"
              className="text-sm font-semibold text-blue-600 transition hover:text-blue-700"
            >
              {t.dashboard || "Dashboard"}
            </Link>
          )}

          {isAdmin && (
            <Link
              href="/admin"
              className="text-sm font-medium text-slate-600 transition hover:text-slate-900"
            >
              {t.admin || "Admin"}
            </Link>
          )}

          <Link
            href="/#agents"
            className="text-sm font-medium text-slate-600 transition hover:text-slate-900"
          >
            {t.agents || "Agents"}
          </Link>

          <div className="group relative">
            <button
              type="button"
              className="inline-flex items-center gap-1 text-sm font-medium text-slate-600 transition hover:text-slate-900"
            >
              {solutionsLabel}
              <span className="text-xs transition group-hover:rotate-180">▾</span>
            </button>

            <div
              className={`invisible absolute top-full z-50 mt-3 w-56 rounded-2xl border border-slate-200 bg-white p-2 opacity-0 shadow-xl transition-all duration-200 group-hover:visible group-hover:opacity-100 ${
                locale === "ar" ? "right-0" : "left-0"
              }`}
            >
              {solutionLinks.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className="block rounded-xl px-4 py-3 text-sm font-medium text-slate-600 transition hover:bg-slate-50 hover:text-slate-900"
                >
                  {item.label}
                </Link>
              ))}
            </div>
          </div>

          <Link
            href="/labs/agent-0"
            className="text-sm font-medium text-slate-600 transition hover:text-slate-900"
          >
            {t.labs || "Labs"}
          </Link>

          <Link
            href="/enterprise"
            className="text-sm font-medium text-slate-600 transition hover:text-slate-900"
          >
            {t.enterprise || "Enterprise"}
          </Link>

          {/* PRICING */}
          <Link
            href="/pricing"
            className="text-sm font-medium text-slate-600 transition hover:text-slate-900"
          >
            {t.pricing || "Pricing"}
          </Link>

          {!isLogged && (
            <>
              <Link
                href="/login"
                className="text-sm font-medium text-slate-600 transition hover:text-slate-900"
              >
                {t.login || "Login"}
              </Link>

              <Link
                href="/register"
                className="rounded-xl bg-slate-900 px-5 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-slate-800"
              >
                {t.register || "Register"}
              </Link>
            </>
          )}

          {isLogged &&
            credits !== null &&
            !canSeeEnterprise && (
              <div className="hidden items-center gap-2 rounded-full border bg-white px-4 py-2 text-sm font-medium text-slate-700 md:flex">

                <span className="rounded-full bg-slate-100 px-2 py-1 text-[10px] font-semibold uppercase text-slate-700">
                  {plan || "trial"}
                </span>

                <span>
                  {credits} {t.credits || "credits"}
                </span>
              </div>
            )}

          {isLogged && (
            <button
              onClick={handleLogout}
              className="rounded-xl bg-slate-100 px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-200"
            >
              {t.logout || "Logout"}
            </button>
          )}
        </div>
      </div>
    </header>
  );
}
