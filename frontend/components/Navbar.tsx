"use client";

import Link from "next/link";
import Image from "next/image";
import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";
import { getSavedLocale, translations } from "../lib/i18n";

type Locale = "en" | "fr" | "ar";

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

export default function Navbar() {
  const pathname = usePathname();

  const [isLogged, setIsLogged] = useState(false);
  const [role, setRole] = useState("");
  const [plan, setPlan] = useState("");
  const [credits, setCredits] = useState<string | null>(null);
  const [isEnterpriseMember, setIsEnterpriseMember] = useState(false);
  const [apiEnabled, setApiEnabled] = useState(false);
  const [locale, setLocale] = useState<Locale>("en");
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

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

    const savedApiEnabled =
      localStorage.getItem("api_enabled") === "true";

    setIsLogged(!!token);
    setRole(savedRole);
    setPlan(savedPlan);
    setCredits(savedCredits);
    setIsEnterpriseMember(savedEnterpriseMember);
    setApiEnabled(savedApiEnabled);
  };

  const resolveLocale = (): Locale => {
    const pathLocale = getLocaleFromPathname(pathname);

    if (pathLocale) {
      return pathLocale;
    }

    return normalizeLocale(getSavedLocale(), "en");
  };

  useEffect(() => {
    checkAuth();
    setLocale(resolveLocale());

    window.addEventListener("storage", checkAuth);

    const handleLocaleChange = () => {
      setLocale(resolveLocale());
    };

    window.addEventListener("locale-change", handleLocaleChange);

    return () => {
      window.removeEventListener("storage", checkAuth);
      window.removeEventListener("locale-change", handleLocaleChange);
    };
  }, [pathname]);

  const closeMobileMenu = () => {
    setIsMobileMenuOpen(false);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    localStorage.removeItem("plan");
    localStorage.removeItem("credits_balance");
    localStorage.removeItem("enterprise_member");
    localStorage.removeItem("api_enabled");

    setIsLogged(false);
    setRole("");
    setPlan("");
    setCredits(null);
    setIsEnterpriseMember(false);
    setApiEnabled(false);
    closeMobileMenu();

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

  const mobileLinkClass =
    "block rounded-xl px-4 py-3 text-sm font-medium text-slate-700 transition hover:bg-slate-50 hover:text-slate-950";

  return (
    <header
      dir={locale === "ar" ? "rtl" : "ltr"}
      className="sticky top-0 z-50 w-full border-b border-slate-200/70 bg-white/70 backdrop-blur-md"
    >
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">

        {/* LOGO */}
        <Link href="/" className="flex shrink-0 items-center gap-1.5">
          <Image
            src="/runexa.svg"
            alt="Runexa AI Workspace"
            width={300}
            height={90}
            priority
            className="h-12 w-auto object-contain"
          />

          <span className="hidden lg:block pr-6 text-xs font-medium text-slate-500">
            {navbarSlogan}
          </span>
        </Link>

        <div className="hidden items-center gap-5 lg:flex">

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
            href="/developers"
            className="hidden xl:flex items-center rounded-full border border-blue-200 bg-blue-50 px-3 py-1.5 text-xs font-semibold text-blue-700 shadow-sm transition hover:bg-blue-100"
          >
            {locale === "fr"
              ? "Plateforme développeur"
              : locale === "ar"
              ? "منصة المطورين"
              : "Developer Platform"}
          </Link>

          <Link
            href="/api-dashboard"
            className="hidden xl:flex items-center rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-700 shadow-sm transition hover:bg-slate-100"
          >
            {locale === "fr"
              ? "Dashboard API"
              : locale === "ar"
              ? "لوحة API"
              : "API Dashboard"}
          </Link>

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

        <button
          type="button"
          onClick={() => setIsMobileMenuOpen((value) => !value)}
          aria-label={isMobileMenuOpen ? "Close navigation menu" : "Open navigation menu"}
          aria-expanded={isMobileMenuOpen}
          className="inline-flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 bg-white text-slate-700 shadow-sm transition hover:bg-slate-50 lg:hidden"
        >
          <span className="text-2xl leading-none">
            {isMobileMenuOpen ? "×" : "☰"}
          </span>
        </button>
      </div>

      {isMobileMenuOpen && (
        <div className="border-t border-slate-200 bg-white px-4 py-4 shadow-lg lg:hidden">
          <nav className="mx-auto flex max-w-7xl flex-col gap-1 text-sm font-medium text-slate-700">
            {canSeeDashboard && !canSeeEnterprise && (
              <Link
                href="/dashboard"
                onClick={closeMobileMenu}
                className={mobileLinkClass}
              >
                {t.dashboard || "Dashboard"}
              </Link>
            )}

            {canSeeEnterprise && (
              <Link
                href="/entreprises/dashboard"
                onClick={closeMobileMenu}
                className={mobileLinkClass}
              >
                {t.dashboard || "Dashboard"}
              </Link>
            )}

            {isAdmin && (
              <Link
                href="/admin"
                onClick={closeMobileMenu}
                className={mobileLinkClass}
              >
                {t.admin || "Admin"}
              </Link>
            )}

            <Link
              href="/developers"
              onClick={closeMobileMenu}
              className={mobileLinkClass}
            >
              {locale === "fr"
                ? "Plateforme développeur"
                : locale === "ar"
                ? "منصة المطورين"
                : "Developer Platform"}
            </Link>

            <Link
              href="/api-dashboard"
              onClick={closeMobileMenu}
              className={mobileLinkClass}
            >
              {locale === "fr"
                ? "Dashboard API"
                : locale === "ar"
                ? "لوحة API"
                : "API Dashboard"}
            </Link>

            <Link
              href="/labs/agent-0"
              onClick={closeMobileMenu}
              className={mobileLinkClass}
            >
              {t.labs || "Labs"}
            </Link>

            <Link
              href="/enterprise"
              onClick={closeMobileMenu}
              className={mobileLinkClass}
            >
              {t.enterprise || "Enterprise"}
            </Link>

            <Link
              href="/pricing"
              onClick={closeMobileMenu}
              className={mobileLinkClass}
            >
              {t.pricing || "Pricing"}
            </Link>

            {!isLogged && (
              <div className="mt-2 grid gap-2 border-t border-slate-100 pt-3">
                <Link
                  href="/login"
                  onClick={closeMobileMenu}
                  className={mobileLinkClass}
                >
                  {t.login || "Login"}
                </Link>

                <Link
                  href="/register"
                  onClick={closeMobileMenu}
                  className="block rounded-xl bg-slate-900 px-4 py-3 text-center text-sm font-semibold text-white shadow-sm transition hover:bg-slate-800"
                >
                  {t.register || "Register"}
                </Link>
              </div>
            )}

            {isLogged && credits !== null && !canSeeEnterprise && (
              <div className="mt-2 flex items-center justify-between rounded-2xl border bg-white px-4 py-3 text-sm text-slate-700">
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
                className="mt-2 rounded-xl bg-slate-100 px-4 py-3 text-left text-sm font-medium text-slate-700 transition hover:bg-slate-200"
              >
                {t.logout || "Logout"}
              </button>
            )}
          </nav>
        </div>
      )}
    </header>
  );
}
