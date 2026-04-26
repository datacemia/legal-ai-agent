"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getSavedLocale, translations } from "../lib/i18n";

export default function Footer() {
  const [locale, setLocale] = useState("en");

  useEffect(() => {
    setLocale(getSavedLocale());

    const handleLocaleChange = () => {
      setLocale(getSavedLocale());
    };

    window.addEventListener("locale-change", handleLocaleChange);

    return () => {
      window.removeEventListener("locale-change", handleLocaleChange);
    };
  }, []);

  const t = translations[locale] || translations.en;

  return (
    <footer
      dir={locale === "ar" ? "rtl" : "ltr"}
      className="bg-slate-950 text-white px-6 py-14"
    >
      <div className="max-w-7xl mx-auto">
        <div className="grid gap-10 md:grid-cols-4">
          <div>
            <h3 className="text-2xl font-bold">Runexa</h3>
            <p className="mt-4 text-sm text-slate-400 leading-6">
              {t.footerDesc}
            </p>
          </div>

          <div>
            <h4 className="font-semibold">{t.products}</h4>
            <div className="mt-4 space-y-3 text-sm text-slate-400">
              <p>
                {t.legalAgent}{" "}
                <span className="text-green-400">· {t.available}</span>
              </p>
              <p>
                {t.financeAgent}{" "}
                <span className="text-slate-500">· {t.comingSoon}</span>
              </p>
              <p>
                {t.hrAgent}{" "}
                <span className="text-slate-500">· {t.comingSoon}</span>
              </p>
              <p>
                {t.businessAgent}{" "}
                <span className="text-slate-500">· {t.comingSoon}</span>
              </p>
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

          <div className="flex gap-5">
            <a href="#" className="hover:text-white transition">
              {t.privacy}
            </a>
            <a href="#" className="hover:text-white transition">
              {t.terms}
            </a>
            <a href="#" className="hover:text-white transition">
              {t.contact}
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}