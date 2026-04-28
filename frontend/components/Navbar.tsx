"use client";

import Link from "next/link";
import Image from "next/image";
import { useEffect, useState } from "react";
import { getSavedLocale, translations } from "../lib/i18n";

export default function Navbar() {
  const [isLogged, setIsLogged] = useState(false);
  const [role, setRole] = useState("");
  const [locale, setLocale] = useState("en");

  const checkAuth = () => {
    const token = localStorage.getItem("token");

    // ✅ FIX role propre
    const savedRole = (localStorage.getItem("role") || "")
      .toLowerCase()
      .trim();

    setIsLogged(!!token);
    setRole(savedRole);
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
    setIsLogged(false);
    setRole("");
    window.location.href = "/login";
  };

  const t = translations[locale] || translations.en;

  const isAdmin = role === "admin";
  const isBusiness = role === "business";
  const canSeeDashboard = isAdmin || isBusiness;

  return (
    <header
      dir={locale === "ar" ? "rtl" : "ltr"}
      className="sticky top-0 z-50 w-full border-b border-slate-200/70 bg-white/70 backdrop-blur-md"
    >
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">
        <Link href="/" className="flex items-center gap-3">
           <span className="text-xl font-bold tracking-tight text-slate-900">
            RUNEXA
           </span>

          <div className="leading-tight">
            <div className="text-xs text-slate-500">{t.slogan}</div>
          </div>
        </Link>

        <div className="flex items-center gap-5">
          {/* ✅ Dashboard seulement business/admin */}
          {canSeeDashboard && (
            <Link
              href="/dashboard"
              className="text-sm font-medium text-slate-600 hover:text-slate-900 transition"
            >
              {t.dashboard || "Dashboard"}
            </Link>
          )}

          {/* ✅ Admin seulement */}
          {isAdmin && (
            <Link
              href="/admin"
              className="text-sm font-medium text-slate-600 hover:text-slate-900 transition"
            >
              {t.admin || "Admin"}
            </Link>
          )}

          {/* Toujours visibles */}
          <Link
            href="/login"
            className="text-sm font-medium text-slate-600 hover:text-slate-900 transition"
          >
            {t.login || "Login"}
          </Link>

          <Link
            href="/register"
            className="rounded-xl bg-slate-900 px-5 py-2 text-sm font-semibold text-white shadow-sm hover:bg-slate-800 transition"
          >
            {t.register || "Register"}
          </Link>

          {/* Logout seulement si connecté */}
          {isLogged && (
            <button
              onClick={handleLogout}
              className="rounded-xl bg-slate-100 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-200 transition"
            >
              {t.logout || "Logout"}
            </button>
          )}
        </div>
      </div>
    </header>
  );
}