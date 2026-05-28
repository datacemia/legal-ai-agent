"use client";

import { useEffect, useState } from "react";
import { getSavedLocale } from "../../lib/i18n";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "https://api.runexa.ai";

const translations = {
  en: {
    title: "Contact Sales",
    subtitle: "Get a tailored solution for your business",
    fullName: "Full name",
    workEmail: "Work email",
    companyName: "Company name",
    companySize: "Company size",
    useCase: "How will you use Runexa?",
    contactSales: "Contact sales",
    businessEmailError: "Please use a company email address.",
    submitError: "Failed to send request. Please try again.",
    submitted: "Submitted",
  },

  fr: {
    title: "Contacter l’équipe commerciale",
    subtitle: "Obtenez une solution adaptée à votre entreprise",
    fullName: "Nom complet",
    workEmail: "Email professionnel",
    companyName: "Nom de l’entreprise",
    companySize: "Taille de l’entreprise",
    useCase: "Comment allez-vous utiliser Runexa ?",
    contactSales: "Contacter l’équipe commerciale",
    businessEmailError:
      "Veuillez utiliser une adresse email professionnelle.",
    submitError:
      "Échec de l’envoi de la demande. Veuillez réessayer.",
    submitted: "Demande envoyée",
  },

  ar: {
    title: "التواصل مع فريق المبيعات",
    subtitle: "احصل على حل مخصص لعملك",
    fullName: "الاسم الكامل",
    workEmail: "البريد الإلكتروني المهني",
    companyName: "اسم الشركة",
    companySize: "حجم الشركة",
    useCase: "كيف ستستخدم Runexa؟",
    contactSales: "التواصل مع المبيعات",
    businessEmailError:
      "يرجى استخدام بريد إلكتروني خاص بالشركة.",
    submitError:
      "فشل إرسال الطلب. يرجى المحاولة مرة أخرى.",
    submitted: "تم الإرسال",
  },
};

export default function ContactClient() {
  const [locale, setLocale] =
    useState<"en" | "fr" | "ar">("en");

  const [form, setForm] = useState({
    full_name: "",
    email: "",
    company_name: "",
    company_size: "",
    use_case: "",
  });

  const [message, setMessage] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  useEffect(() => {
    const saved = getSavedLocale();

    if (saved === "fr" || saved === "ar") {
      setLocale(saved);
    } else {
      setLocale("en");
    }

    const handleLocaleChange = () => {
      const updated = getSavedLocale();

      if (updated === "fr" || updated === "ar") {
        setLocale(updated);
      } else {
        setLocale("en");
      }
    };

    window.addEventListener(
      "locale-change",
      handleLocaleChange
    );

    return () => {
      window.removeEventListener(
        "locale-change",
        handleLocaleChange
      );
    };
  }, []);

  const t = translations[locale];

  const isBusinessEmail = (email: string) => {
    const blockedDomains = [
      "gmail.com",
      "yahoo.com",
      "hotmail.com",
      "outlook.com",
      "live.com",
      "icloud.com",
      "aol.com",
      "protonmail.com",
      "proton.me",
      "mail.com",
      "gmx.com",
      "yandex.com",
    ];

    const domain = email.split("@")[1]?.toLowerCase();

    if (!domain) return false;

    return !blockedDomains.includes(domain);
  };

  const handleSubmit = async () => {
    setMessage("");
    setErrorMsg("");

    if (!isBusinessEmail(form.email)) {
      setErrorMsg(t.businessEmailError);
      return;
    }

    try {
      const res = await fetch(`${API_URL}/contact/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error("Failed");
      }

      setMessage(data.message || t.submitted);

      setForm({
        full_name: "",
        email: "",
        company_name: "",
        company_size: "",
        use_case: "",
      });
    } catch {
      setErrorMsg(t.submitError);
    }
  };

  return (
    <main
      dir={locale === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-white px-4 py-20"
    >
      <div className="mx-auto max-w-2xl space-y-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold">
            {t.title}
          </h1>

          <p className="mt-2 text-slate-600">
            {t.subtitle}
          </p>
        </div>

        <div className="space-y-4">
          <input
            placeholder={t.fullName}
            className="w-full rounded-xl border p-3"
            value={form.full_name}
            onChange={(e) =>
              setForm({
                ...form,
                full_name: e.target.value,
              })
            }
          />

          <input
            placeholder={t.workEmail}
            className="w-full rounded-xl border p-3"
            value={form.email}
            onChange={(e) =>
              setForm({
                ...form,
                email: e.target.value,
              })
            }
          />

          <input
            placeholder={t.companyName}
            className="w-full rounded-xl border p-3"
            value={form.company_name}
            onChange={(e) =>
              setForm({
                ...form,
                company_name: e.target.value,
              })
            }
          />

          <select
            className="w-full rounded-xl border p-3"
            value={form.company_size}
            onChange={(e) =>
              setForm({
                ...form,
                company_size: e.target.value,
              })
            }
          >
            <option value="">
              {t.companySize}
            </option>

            <option>1-10</option>
            <option>10-50</option>
            <option>50-200</option>
            <option>200+</option>
          </select>

          <textarea
            placeholder={t.useCase}
            className="w-full rounded-xl border p-3"
            value={form.use_case}
            onChange={(e) =>
              setForm({
                ...form,
                use_case: e.target.value,
              })
            }
          />

          {message && (
            <div className="rounded-xl border border-green-200 bg-green-50 px-4 py-3 text-center text-sm text-green-700">
              {message}
            </div>
          )}

          {errorMsg && (
            <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-center text-sm text-red-700">
              {errorMsg}
            </div>
          )}

          <button
            onClick={handleSubmit}
            className="w-full rounded-xl bg-black py-3 text-white"
          >
            {t.contactSales}
          </button>
        </div>
      </div>
    </main>
  );
}
