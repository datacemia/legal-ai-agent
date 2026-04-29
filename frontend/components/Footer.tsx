"use client";

import Link from "next/link";
import Image from "next/image";
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

  const legalLabels: any = {
    en: {
      terms: "Terms",
      privacy: "Privacy Policy",
      productTerms: "Product Terms",
    },
    fr: {
      terms: "Conditions",
      privacy: "Confidentialité",
      productTerms: "Conditions produit",
    },
    ar: {
      terms: "الشروط",
      privacy: "الخصوصية",
      productTerms: "شروط المنتج",
    },
  };

  const legal = legalLabels[locale] || legalLabels.en;

  return (
    <footer
      dir={locale === "ar" ? "rtl" : "ltr"}
      className="bg-slate-950 text-white px-6 py-14"
    >
      <div className="max-w-7xl mx-auto">
        <div className="grid gap-10 md:grid-cols-4">
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

            {/* ✅ MULTILANGUAGE ADDRESS */}
            <p className="mt-4 text-xs text-slate-500 leading-5 whitespace-pre-line">
              {t.companyAddress}
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

          <div className="flex flex-wrap gap-5">
            <Link href="/terms" className="hover:text-white transition">
              {legal.terms}
            </Link>

            <a href="/privacy" className="hover:text-white transition">
              {legal.privacy}
            </a>

            <Link
              href="/products/ai-legal-agent/terms"
              className="hover:text-white transition"
            >
              {legal.productTerms}
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}