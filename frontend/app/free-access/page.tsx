"use client";

import { FormEvent, useMemo, useState } from "react";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "https://api.runexa.ai";

type Language = "en" | "fr" | "ar";
type Agent = "legal" | "study" | "business" | "finance";

type FormData = {
  first_name: string;
  last_name: string;
  email: string;
  country: string;
  agent: Agent | "";
};

const translations = {
  en: {
    language: "English",
    badge: "Free Access Request",
    title: "Try Runexa for Free",
    subtitle:
      "Create your Runexa account, then request complimentary credits to explore our specialized AI agents.",
    accountRequired: "A Runexa account is required.",
    accountText:
      "Use the same email address as your Runexa account so we can identify your request.",
    createAccount: "Create account",

    firstName: "First name",
    firstNamePlaceholder: "Your first name",

    lastName: "Last name",
    lastNamePlaceholder: "Your last name",

    email: "Runexa account email",
    emailPlaceholder: "you@example.com",

    country: "Country",
    countryPlaceholder: "Your country",

    agent: "AI Agent",
    agentPlaceholder: "Select an agent",
    legalAgent: "Legal",
    studyAgent: "Study",
    businessAgent: "Business",
    financeAgent: "Finance",

    submit: "Request Free Access",
    submitting: "Sending request...",

    successTitle: "Request received",
    success:
      "Your free access request has been received. If approved, complimentary credits will be added to your Runexa account.",

    error:
      "We could not submit your request. Please verify your information and try again.",

    alreadySubmitted:
      "A free access request has already been submitted with this email address.",

    privacy:
      "Your information is used only to review and process your free access request.",

    existingAccount: "Already have a Runexa account?",
    login: "Log in",
    backHome: "Back to Runexa",
  },

  fr: {
    language: "Français",
    badge: "Demande d'accès gratuit",
    title: "Essayez Runexa gratuitement",
    subtitle:
      "Créez votre compte Runexa, puis demandez des crédits offerts pour découvrir nos agents IA spécialisés.",
    accountRequired: "Un compte Runexa est requis.",
    accountText:
      "Utilisez la même adresse e-mail que celle de votre compte Runexa afin que nous puissions identifier votre demande.",
    createAccount: "Créer un compte",

    firstName: "Prénom",
    firstNamePlaceholder: "Votre prénom",

    lastName: "Nom",
    lastNamePlaceholder: "Votre nom",

    email: "E-mail du compte Runexa",
    emailPlaceholder: "vous@exemple.com",

    country: "Pays",
    countryPlaceholder: "Votre pays",

    agent: "Agent IA",
    agentPlaceholder: "Sélectionnez un agent",
    legalAgent: "Juridique",
    studyAgent: "Études",
    businessAgent: "Business",
    financeAgent: "Finance",

    submit: "Demander un accès gratuit",
    submitting: "Envoi de la demande...",

    successTitle: "Demande reçue",
    success:
      "Votre demande d'accès gratuit a bien été reçue. Si elle est approuvée, des crédits offerts seront ajoutés à votre compte Runexa.",

    error:
      "Impossible d'envoyer votre demande. Vérifiez vos informations et réessayez.",

    alreadySubmitted:
      "Une demande d'accès gratuit a déjà été envoyée avec cette adresse e-mail.",

    privacy:
      "Vos informations sont utilisées uniquement pour examiner et traiter votre demande d'accès gratuit.",

    existingAccount: "Vous avez déjà un compte Runexa ?",
    login: "Se connecter",
    backHome: "Retour à Runexa",
  },

  ar: {
    language: "العربية",
    badge: "طلب وصول مجاني",
    title: "جرّب Runexa مجانًا",
    subtitle:
      "أنشئ حساب Runexa، ثم اطلب رصيدًا مجانيًا لتجربة وكلاء الذكاء الاصطناعي المتخصصين لدينا.",
    accountRequired: "يلزم وجود حساب Runexa.",
    accountText:
      "استخدم نفس عنوان البريد الإلكتروني المرتبط بحساب Runexa حتى نتمكن من تحديد طلبك.",
    createAccount: "إنشاء حساب",

    firstName: "الاسم الأول",
    firstNamePlaceholder: "الاسم الأول",

    lastName: "اسم العائلة",
    lastNamePlaceholder: "اسم العائلة",

    email: "البريد الإلكتروني لحساب Runexa",
    emailPlaceholder: "you@example.com",

    country: "البلد",
    countryPlaceholder: "بلدك",

    agent: "وكيل الذكاء الاصطناعي",
    agentPlaceholder: "اختر وكيلاً",
    legalAgent: "القانون",
    studyAgent: "الدراسة",
    businessAgent: "الأعمال",
    financeAgent: "المالية",

    submit: "طلب وصول مجاني",
    submitting: "جارٍ إرسال الطلب...",

    successTitle: "تم استلام الطلب",
    success:
      "تم استلام طلب الوصول المجاني. في حال الموافقة عليه، ستتم إضافة رصيد مجاني إلى حساب Runexa الخاص بك.",

    error:
      "تعذر إرسال طلبك. يرجى التحقق من المعلومات والمحاولة مرة أخرى.",

    alreadySubmitted:
      "تم بالفعل إرسال طلب وصول مجاني باستخدام عنوان البريد الإلكتروني هذا.",

    privacy:
      "تُستخدم معلوماتك فقط لمراجعة طلب الوصول المجاني ومعالجته.",

    existingAccount: "لديك حساب Runexa بالفعل؟",
    login: "تسجيل الدخول",
    backHome: "العودة إلى Runexa",
  },
};

export default function FreeAccessPage() {
  const [language, setLanguage] = useState<Language>("en");

  const [form, setForm] = useState<FormData>({
    first_name: "",
    last_name: "",
    email: "",
    country: "",
    agent: "",
  });

  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [message, setMessage] = useState("");

  const t = translations[language];
  const isArabic = language === "ar";

  const canSubmit = useMemo(() => {
    return (
      form.first_name.trim().length > 0 &&
      form.last_name.trim().length > 0 &&
      form.email.trim().length > 0 &&
      form.country.trim().length > 0 &&
      form.agent !== ""
    );
  }, [form]);

  function updateField(field: keyof FormData, value: string) {
    setForm((current) => ({
      ...current,
      [field]: value,
    }));

    if (message) {
      setMessage("");
    }
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!canSubmit || loading) {
      return;
    }

    setLoading(true);
    setMessage("");
    setSuccess(false);

    try {
      const response = await fetch(`${API_URL}/free-access-request/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          first_name: form.first_name.trim(),
          last_name: form.last_name.trim(),
          email: form.email.trim().toLowerCase(),
          country: form.country.trim(),
          agent: form.agent,
        }),
      });

      let data: any = null;

      try {
        data = await response.json();
      } catch {
        data = null;
      }

      if (!response.ok) {
        const detail =
          typeof data?.detail === "string"
            ? data.detail.toLowerCase()
            : "";

        if (
          response.status === 409 ||
          detail.includes("already") ||
          detail.includes("exist")
        ) {
          throw new Error("ALREADY_SUBMITTED");
        }

        throw new Error("SUBMISSION_FAILED");
      }

      setSuccess(true);

      setForm({
        first_name: "",
        last_name: "",
        email: "",
        country: "",
        agent: "",
      });
    } catch (error) {
      if (
        error instanceof Error &&
        error.message === "ALREADY_SUBMITTED"
      ) {
        setMessage(t.alreadySubmitted);
      } else {
        setMessage(t.error);
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <main
      dir={isArabic ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-4 py-10 sm:px-6 lg:px-8"
    >
      <div className="mx-auto max-w-3xl">
        <div className="mb-8 flex flex-wrap items-center justify-between gap-4">
          <a
            href="/"
            className="text-xl font-bold tracking-tight text-slate-950"
          >
            Runexa
          </a>

          <div className="flex items-center gap-2 rounded-xl border border-slate-200 bg-white p-1 shadow-sm">
            {(["en", "fr", "ar"] as Language[]).map((lang) => (
              <button
                key={lang}
                type="button"
                onClick={() => {
                  setLanguage(lang);
                  setMessage("");
                }}
                className={`rounded-lg px-3 py-2 text-sm font-semibold transition ${
                  language === lang
                    ? "bg-slate-950 text-white"
                    : "text-slate-600 hover:bg-slate-100"
                }`}
              >
                {translations[lang].language}
              </button>
            ))}
          </div>
        </div>

        <div className="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">
          <div className="border-b border-slate-100 px-6 py-8 sm:px-10 sm:py-10">
            <div className="inline-flex rounded-full bg-blue-50 px-3 py-1 text-sm font-semibold text-blue-700">
              {t.badge}
            </div>

            <h1 className="mt-5 text-3xl font-bold tracking-tight text-slate-950 sm:text-4xl">
              {t.title}
            </h1>

            <p className="mt-4 max-w-2xl text-base leading-7 text-slate-600">
              {t.subtitle}
            </p>
          </div>

          <div className="px-6 py-8 sm:px-10">
            <div className="mb-8 rounded-2xl border border-blue-100 bg-blue-50/70 p-5">
              <p className="font-semibold text-slate-950">
                {t.accountRequired}
              </p>

              <p className="mt-1 text-sm leading-6 text-slate-600">
                {t.accountText}
              </p>

              <a
                href="/register"
                className="mt-3 inline-flex text-sm font-semibold text-blue-700 hover:text-blue-800"
              >
                {t.createAccount} →
              </a>
            </div>

            {success ? (
              <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-6">
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-100 text-lg font-bold text-emerald-700">
                  ✓
                </div>

                <h2 className="mt-4 text-xl font-bold text-slate-950">
                  {t.successTitle}
                </h2>

                <p className="mt-2 leading-7 text-slate-600">
                  {t.success}
                </p>

                <div className="mt-6 flex flex-wrap gap-3">
                  <a
                    href="/login"
                    className="inline-flex items-center justify-center rounded-xl bg-slate-950 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-800"
                  >
                    {t.login}
                  </a>

                  <a
                    href="/"
                    className="inline-flex items-center justify-center rounded-xl border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-slate-700 transition hover:bg-slate-50"
                  >
                    {t.backHome}
                  </a>
                </div>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid gap-6 sm:grid-cols-2">
                  <div>
                    <label
                      htmlFor="first_name"
                      className="mb-2 block text-sm font-semibold text-slate-800"
                    >
                      {t.firstName}
                    </label>

                    <input
                      id="first_name"
                      name="first_name"
                      type="text"
                      autoComplete="given-name"
                      required
                      maxLength={100}
                      value={form.first_name}
                      onChange={(e) =>
                        updateField("first_name", e.target.value)
                      }
                      placeholder={t.firstNamePlaceholder}
                      className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-slate-950 outline-none transition placeholder:text-slate-400 focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                    />
                  </div>

                  <div>
                    <label
                      htmlFor="last_name"
                      className="mb-2 block text-sm font-semibold text-slate-800"
                    >
                      {t.lastName}
                    </label>

                    <input
                      id="last_name"
                      name="last_name"
                      type="text"
                      autoComplete="family-name"
                      required
                      maxLength={100}
                      value={form.last_name}
                      onChange={(e) =>
                        updateField("last_name", e.target.value)
                      }
                      placeholder={t.lastNamePlaceholder}
                      className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-slate-950 outline-none transition placeholder:text-slate-400 focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                    />
                  </div>
                </div>

                <div>
                  <label
                    htmlFor="email"
                    className="mb-2 block text-sm font-semibold text-slate-800"
                  >
                    {t.email}
                  </label>

                  <input
                    id="email"
                    name="email"
                    type="email"
                    dir="ltr"
                    autoComplete="email"
                    required
                    maxLength={255}
                    value={form.email}
                    onChange={(e) =>
                      updateField("email", e.target.value)
                    }
                    placeholder={t.emailPlaceholder}
                    className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-left text-slate-950 outline-none transition placeholder:text-slate-400 focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                  />
                </div>

                <div>
                  <label
                    htmlFor="country"
                    className="mb-2 block text-sm font-semibold text-slate-800"
                  >
                    {t.country}
                  </label>

                  <input
                    id="country"
                    name="country"
                    type="text"
                    autoComplete="country-name"
                    required
                    maxLength={100}
                    value={form.country}
                    onChange={(e) =>
                      updateField("country", e.target.value)
                    }
                    placeholder={t.countryPlaceholder}
                    className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-slate-950 outline-none transition placeholder:text-slate-400 focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                  />
                </div>

                <div>
                  <label
                    htmlFor="agent"
                    className="mb-2 block text-sm font-semibold text-slate-800"
                  >
                    {t.agent}
                  </label>

                  <select
                    id="agent"
                    name="agent"
                    required
                    value={form.agent}
                    onChange={(e) =>
                      updateField("agent", e.target.value)
                    }
                    className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-slate-950 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                  >
                    <option value="">
                      {t.agentPlaceholder}
                    </option>

                    <option value="legal">
                      {t.legalAgent}
                    </option>

                    <option value="study">
                      {t.studyAgent}
                    </option>

                    <option value="business">
                      {t.businessAgent}
                    </option>

                    <option value="finance">
                      {t.financeAgent}
                    </option>
                  </select>
                </div>

                {message && (
                  <div
                    role="alert"
                    className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700"
                  >
                    {message}
                  </div>
                )}

                <button
                  type="submit"
                  disabled={!canSubmit || loading}
                  className="inline-flex w-full items-center justify-center rounded-xl bg-slate-950 px-6 py-3.5 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {loading ? t.submitting : t.submit}
                </button>

                <p className="text-center text-xs leading-5 text-slate-500">
                  {t.privacy}
                </p>
              </form>
            )}

            {!success && (
              <div className="mt-8 border-t border-slate-100 pt-6 text-center text-sm text-slate-600">
                {t.existingAccount}{" "}
                <a
                  href="/login"
                  className="font-semibold text-blue-700 hover:text-blue-800"
                >
                  {t.login}
                </a>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}