"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getSavedLocale } from "../../../lib/i18n";

const translations = {
  en: {
    back: "← Back to Business",

    title: "Contact Runexa Sales",

    subtitle:
        "Tell us about your business needs. Our team can help design custom AI agents and workflows tailored to your organization.",

    fullName: "Full Name",

    workEmail: "Work Email",

    companyName: "Company Name",

    companySize: "Company Size",

    selectSize: "Select Company Size",

    size1: "1–10 employees",
    size2: "11–50 employees",
    size3: "51–200 employees",
    size4: "200+ employees",

    useCase: "What would you like to build with Runexa?",

    useCasePlaceholder:
        "Examples: contract review, financial reporting, document processing, CV screening, business intelligence dashboards, compliance workflows...",

    success:
        "Your request has been submitted successfully. A member of our team will contact you shortly.",

    businessEmailError:
        "Please use a business email address.",

    submitError:
        "Unable to submit your request. Please try again.",

    submit: "Contact Sales",
    },

fr: {
    back: "← Retour à Business",

    title: "Contacter l’équipe commerciale Runexa",

    subtitle:
        "Parlez-nous de vos besoins. Notre équipe peut concevoir des agents IA et des workflows adaptés à votre organisation.",

    fullName: "Nom complet",

    workEmail: "Adresse e-mail professionnelle",

    companyName: "Nom de l’entreprise",

    companySize: "Taille de l’entreprise",

    selectSize: "Sélectionner la taille de l’entreprise",

    size1: "1–10 employés",
    size2: "11–50 employés",
    size3: "51–200 employés",
    size4: "200+ employés",

    useCase: "Que souhaitez-vous construire avec Runexa ?",

    useCasePlaceholder:
        "Exemples : revue de contrats, reporting financier, traitement documentaire, tri de CV, tableaux de bord de business intelligence, workflows de conformité...",

    success:
        "Votre demande a été envoyée avec succès. Un membre de notre équipe vous contactera prochainement.",

    businessEmailError:
        "Veuillez utiliser une adresse e-mail professionnelle.",

    submitError:
        "Impossible d’envoyer votre demande. Veuillez réessayer.",

    submit: "Contacter l’équipe commerciale",
    },

  ar: {
    back: "← العودة إلى الأعمال",

    title: "التواصل مع فريق مبيعات Runexa",

    subtitle:
        "أخبرنا باحتياجات مؤسستك. يمكن لفريقنا تصميم وكلاء ذكاء اصطناعي وتدفقات عمل مخصصة تناسب أعمالك.",

    fullName: "الاسم الكامل",

    workEmail: "البريد الإلكتروني المهني",

    companyName: "اسم الشركة",

    companySize: "حجم الشركة",

    selectSize: "اختر حجم الشركة",

    size1: "1–10 موظفين",
    size2: "11–50 موظفًا",
    size3: "51–200 موظف",
    size4: "أكثر من 200 موظف",

    useCase: "ما الذي ترغب في بنائه باستخدام Runexa؟",

    useCasePlaceholder:
        "أمثلة: مراجعة العقود، التقارير المالية، معالجة المستندات، فرز السير الذاتية، لوحات ذكاء الأعمال، سير عمل الامتثال...",

    success:
        "تم إرسال طلبك بنجاح. سيتواصل معك أحد أعضاء فريقنا قريبًا.",

    businessEmailError:
        "يرجى استخدام بريد إلكتروني مهني تابع للشركة.",

    submitError:
        "تعذر إرسال الطلب. يرجى المحاولة مرة أخرى.",

    submit: "التواصل مع فريق المبيعات",
    },
};

export default function EnterpriseContactClient() {
  const [locale, setLocale] =
    useState<"en" | "fr" | "ar">("en");

  const [form, setForm] = useState({
    name: "",
    email: "",
    company: "",
    size: "",
    useCase: "",
  });

  const [success, setSuccess] = useState(false);
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

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
    >
  ) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
    setSuccess(false);
    setErrorMsg("");
  };

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

  const handleSubmit = async (
    e: React.FormEvent<HTMLFormElement>
  ) => {
    e.preventDefault();

    if (!isBusinessEmail(form.email)) {
      setErrorMsg(t.businessEmailError);
      setSuccess(false);
      return;
    }

    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/contact/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            full_name: form.name,
            email: form.email,
            company_name: form.company,
            company_size: form.size,
            use_case: form.useCase,
          }),
        }
      );

      if (!res.ok) {
        throw new Error("Failed to send request");
      }

      setSuccess(true);
      setErrorMsg("");

      setForm({
        name: "",
        email: "",
        company: "",
        size: "",
        useCase: "",
      });
    } catch {
      setErrorMsg(t.submitError);
      setSuccess(false);
    }
  };

  return (
    <main
      dir={locale === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-6 py-16 text-slate-900"
    >
      <div className="mx-auto max-w-3xl">
        <div className="mb-6">
          <Link
            href="/enterprise"
            className="text-sm text-blue-600"
          >
            {t.back}
          </Link>
        </div>

        <div className="mb-10 space-y-3 text-center">
          <h1 className="text-3xl font-bold">
            {t.title}
          </h1>

          <p className="text-slate-600">
            {t.subtitle}
          </p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="space-y-6 rounded-2xl border bg-white p-8"
        >
          <div>
            <label className="mb-2 block text-sm font-medium">
              {t.fullName}
            </label>

            <input
              type="text"
              name="name"
              value={form.name}
              onChange={handleChange}
              className="w-full rounded-xl border px-4 py-3"
              required
            />
          </div>

          <div>
            <label className="mb-2 block text-sm font-medium">
              {t.workEmail}
            </label>

            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              className="w-full rounded-xl border px-4 py-3"
              required
            />
          </div>

          <div>
            <label className="mb-2 block text-sm font-medium">
              {t.companyName}
            </label>

            <input
              type="text"
              name="company"
              value={form.company}
              onChange={handleChange}
              className="w-full rounded-xl border px-4 py-3"
            />
          </div>

          <div>
            <label className="mb-2 block text-sm font-medium">
              {t.companySize}
            </label>

            <select
              name="size"
              value={form.size}
              onChange={handleChange}
              className="w-full rounded-xl border px-4 py-3"
            >
              <option value="">
                {t.selectSize}
              </option>

              <option>
                {t.size1}
              </option>

              <option>
                {t.size2}
              </option>

              <option>
                {t.size3}
              </option>

              <option>
                {t.size4}
              </option>
            </select>
          </div>

          <div>
            <label className="mb-2 block text-sm font-medium">
              {t.useCase}
            </label>

            <textarea
              name="useCase"
              value={form.useCase}
              onChange={handleChange}
              rows={5}
              placeholder={t.useCasePlaceholder}
              className="w-full rounded-xl border px-4 py-3"
            />
          </div>

          {success && (
            <div className="rounded-xl border border-green-200 bg-green-50 px-4 py-3 text-sm text-green-700">
              {t.success}
            </div>
          )}

          {errorMsg && (
            <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
              {errorMsg}
            </div>
          )}

          <button
            type="submit"
            className="w-full rounded-xl bg-blue-600 py-3 font-semibold text-white transition hover:bg-blue-700"
          >
            {t.submit}
          </button>
        </form>
      </div>
    </main>
  );
}
