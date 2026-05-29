"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "https://api.runexa.ai";

const labels: any = {
 en: {
    back: "← Back to Agent 0",

    badge: "Runexa Labs · Agent 0 Early Access",

    title: "Join the Agent 0 waitlist",

    subtitle:
      "Get early updates on Runexa’s future AI safety system for homes, cameras, sensors, GPS, and autonomous monitoring.",

    success:
      "Thank you. Your request has been recorded. Runexa will contact selected early-access users as Agent 0 moves forward.",

    submitError:
      "Unable to submit the waitlist form. Please try again.",

    fullName: "Full Name",

    fullNamePlaceholder: "Your name",

    email: "Email Address",

    emailPlaceholder: "you@example.com",

    country: "Country",

    countryPlaceholder: "United States, Morocco, France...",

    profile: "Profile",

    interestLevel: "Interest Level",

    protectTarget: "What would you like Agent 0 to protect?",

    message: "Message / Use Case",

    messagePlaceholder:
      "Tell us what safety or monitoring challenge you would like Agent 0 to help solve.",

    consent:
      "I agree to be contacted by Runexa Systems about Agent 0 updates, early access, and related product information.",

    submit:
      "Request Early Access",

    disclaimer:
      "Agent 0 is a concept and research initiative. It is not publicly available yet.",

    profiles: [
      "Homeowner",
      "Parent / Family",
      "Property Manager",
      "Smart Home Enthusiast",
      "Security Company",
      "Investor / Partner",
      "Other",
    ],

    interestLevels: [
      "Early Access",
      "Beta Testing",
      "Partnership",
      "Investment / Business Inquiry",
      "Following Updates",
    ],

    protectTargets: [
      "Home",
      "Apartment",
      "Office",
      "Warehouse",
      "Vacation Property",
      "Multiple Properties",
    ],
  },
  fr: {
    back: "← Retour à Agent 0",

    badge: "Runexa Labs · Accès anticipé Agent 0",

    title: "Rejoindre la liste d’attente Agent 0",

    subtitle:
      "Recevez les premières informations sur Agent 0, le futur système de sécurité autonome de Runexa pour les habitations, les capteurs, les caméras et la surveillance intelligente.",

    success:
      "Merci. Votre demande a été enregistrée. Runexa contactera les participants sélectionnés lors des prochaines phases d’accès anticipé.",

    submitError:
      "Impossible d’envoyer votre demande. Veuillez réessayer.",

    fullName: "Nom complet",

    fullNamePlaceholder: "Votre nom",

    email: "Adresse e-mail",

    emailPlaceholder: "vous@exemple.com",

    country: "Pays",

    countryPlaceholder: "France, Maroc, Canada...",

    profile: "Profil",

    interestLevel: "Type d’intérêt",

    protectTarget:
      "Que souhaitez-vous protéger avec Agent 0 ?",

    message: "Message / Cas d’usage",

    messagePlaceholder:
      "Décrivez le problème de sécurité, de surveillance ou d’automatisation que vous souhaiteriez résoudre avec Agent 0.",

    consent:
      "J’accepte d’être contacté par Runexa Systems concernant Agent 0, les accès anticipés et les futures communications produit.",

    submit:
      "Demander un accès anticipé",

    disclaimer:
      "Agent 0 est actuellement un projet de recherche et développement. Il n’est pas encore disponible au public.",

    profiles: [
      "Propriétaire",
      "Parent / Famille",
      "Gestionnaire immobilier",
      "Passionné de maison connectée",
      "Entreprise de sécurité",
      "Investisseur / Partenaire",
      "Autre",
    ],

    interestLevels: [
      "Accès anticipé",
      "Programme bêta",
      "Partenariat",
      "Investissement / Opportunité commerciale",
      "Suivre les actualités",
    ],

    protectTargets: [
      "Maison",
      "Appartement",
      "Bureau",
      "Entrepôt",
      "Résidence secondaire",
      "Plusieurs propriétés",
    ],
  },

 ar: {
    back:
      "← العودة إلى Agent 0",

    badge:
      "Runexa Labs · الوصول المبكر إلى Agent 0",

    title:
      "الانضمام إلى قائمة انتظار Agent 0",

    subtitle:
      "احصل على أحدث المعلومات حول Agent 0، نظام الأمان الذاتي المستقبلي من Runexa للمنازل وأجهزة الاستشعار والكاميرات والمراقبة الذكية.",

    success:
      "شكراً لك. تم تسجيل طلبك. ستتواصل Runexa مع المشاركين الذين يتم اختيارهم خلال المراحل القادمة من الوصول المبكر.",

    submitError:
      "تعذر إرسال الطلب. يرجى المحاولة مرة أخرى.",

    fullName:
      "الاسم الكامل",

    fullNamePlaceholder:
      "اسمك",

    email:
      "البريد الإلكتروني",

    emailPlaceholder:
      "you@example.com",

    country:
      "الدولة",

    countryPlaceholder:
      "المغرب، فرنسا، الولايات المتحدة...",

    profile:
      "الملف الشخصي",

    interestLevel:
      "نوع الاهتمام",

    protectTarget:
      "ما الذي ترغب في أن يحميه Agent 0؟",

    message:
      "رسالة / حالة استخدام",

    messagePlaceholder:
      "صف التحدي الأمني أو مشكلة المراقبة أو الأتمتة التي ترغب في أن يساعد Agent 0 في حلها.",

    consent:
      "أوافق على أن تتواصل معي Runexa Systems بشأن Agent 0 وبرامج الوصول المبكر والتحديثات المستقبلية المتعلقة بالمنتج.",

    submit:
      "طلب الوصول المبكر",

    disclaimer:
      "Agent 0 مشروع بحث وتطوير قيد الدراسة حالياً، وهو غير متاح للعامة في الوقت الحالي.",

    profiles: [
      "مالك منزل",
      "والد / عائلة",
      "مدير عقارات",
      "مهتم بالمنازل الذكية",
      "شركة أمنية",
      "مستثمر / شريك",
      "أخرى",
    ],

    interestLevels: [
      "وصول مبكر",
      "برنامج تجريبي",
      "شراكة",
      "استثمار / فرصة تجارية",
      "متابعة التحديثات",
    ],

    protectTargets: [
      "منزل",
      "شقة",
      "مكتب",
      "مستودع",
      "منزل للعطلات",
      "عدة عقارات",
    ],
  },
};

const optionValues = {
  profiles: [
    "Homeowner",
    "Parent / Family",
    "Property manager",
    "Smart home enthusiast",
    "Security company",
    "Investor / Partner",
    "Other",
  ],
  interestLevels: [
    "Early access",
    "Beta tester",
    "Partnership",
    "Investment / Business inquiry",
    "Just following updates",
  ],
  protectTargets: [
    "Home",
    "Apartment",
    "Office",
    "Warehouse",
    "Vacation property",
    "Multiple properties",
  ],
};

export default function AgentZeroWaitlistPage() {
  const [language, setLanguage] = useState("en");
  const t = labels[language] || labels.en;

  const [submitted, setSubmitted] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem("locale");

    if (saved && labels[saved]) {
      setLanguage(saved);
    }

    const handleLocaleChange = () => {
      const nextLocale = localStorage.getItem("locale");

      if (nextLocale && labels[nextLocale]) {
        setLanguage(nextLocale);
      }
    };

    window.addEventListener("locale-change", handleLocaleChange);

    return () => {
      window.removeEventListener("locale-change", handleLocaleChange);
    };
  }, []);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const form = e.currentTarget;
    const formData = new FormData(form);

    const payload = {
      full_name: String(formData.get("full_name") || ""),
      email: String(formData.get("email") || ""),
      country: String(formData.get("country") || ""),
      profile: String(formData.get("profile") || ""),
      interest_level: String(formData.get("interest_level") || ""),
      protect_target: String(formData.get("protect_target") || ""),
      message: String(formData.get("message") || ""),
      consent: true,
    };

    const res = await fetch(`${API_URL}/agent0-waitlist/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const data = await res.json();

    if (!res.ok) {
      alert(data.detail || t.submitError);
      return;
    }

    setSubmitted(true);
  };

  return (
    <main
      dir={language === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-950 px-6 py-20 text-white"
    >
      <div className="mx-auto max-w-4xl">
        <Link
          href="/labs/agent-0"
          className="text-sm font-medium text-cyan-300 hover:text-cyan-200"
        >
          {t.back}
        </Link>

        <div className="mt-10 rounded-3xl border border-white/10 bg-white/[0.04] p-8 shadow-2xl">
          <span className="inline-flex rounded-full border border-cyan-300/20 bg-cyan-400/10 px-4 py-2 text-sm font-semibold text-cyan-200">
            {t.badge}
          </span>

          <h1 className="mt-6 text-4xl font-bold tracking-tight md:text-5xl">
            {t.title}
          </h1>

          <p className="mt-5 max-w-2xl text-slate-300">
            {t.subtitle}
          </p>

          {submitted ? (
            <div className="mt-8 rounded-2xl border border-emerald-400/20 bg-emerald-500/10 p-6 text-emerald-100">
              {t.success}
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="mt-8 grid gap-5">
              <div className="grid gap-5 md:grid-cols-2">
                <div>
                  <label className="mb-2 block text-sm font-medium text-slate-300">
                    {t.fullName}
                  </label>
                  <input
                    required
                    name="full_name"
                    className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3 text-white outline-none focus:border-cyan-300"
                    placeholder={t.fullNamePlaceholder}
                  />
                </div>

                <div>
                  <label className="mb-2 block text-sm font-medium text-slate-300">
                    {t.email}
                  </label>
                  <input
                    required
                    type="email"
                    name="email"
                    className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3 text-white outline-none focus:border-cyan-300"
                    placeholder={t.emailPlaceholder}
                  />
                </div>
              </div>

              <div className="grid gap-5 md:grid-cols-2">
                <div>
                  <label className="mb-2 block text-sm font-medium text-slate-300">
                    {t.country}
                  </label>
                  <input
                    name="country"
                    className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3 text-white outline-none focus:border-cyan-300"
                    placeholder={t.countryPlaceholder}
                  />
                </div>

                <div>
                  <label className="mb-2 block text-sm font-medium text-slate-300">
                    {t.profile}
                  </label>
                  <select
                    name="profile"
                    className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3 text-white outline-none focus:border-cyan-300"
                  >
                    {optionValues.profiles.map((value, index) => (
                      <option key={value} value={value}>
                        {t.profiles[index]}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="grid gap-5 md:grid-cols-2">
                <div>
                  <label className="mb-2 block text-sm font-medium text-slate-300">
                    {t.interestLevel}
                  </label>
                  <select
                    name="interest_level"
                    className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3 text-white outline-none focus:border-cyan-300"
                  >
                    {optionValues.interestLevels.map((value, index) => (
                      <option key={value} value={value}>
                        {t.interestLevels[index]}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="mb-2 block text-sm font-medium text-slate-300">
                    {t.protectTarget}
                  </label>
                  <select
                    name="protect_target"
                    className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3 text-white outline-none focus:border-cyan-300"
                  >
                    {optionValues.protectTargets.map((value, index) => (
                      <option key={value} value={value}>
                        {t.protectTargets[index]}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                <label className="mb-2 block text-sm font-medium text-slate-300">
                  {t.message}
                </label>
                <textarea
                  name="message"
                  rows={5}
                  className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3 text-white outline-none focus:border-cyan-300"
                  placeholder={t.messagePlaceholder}
                />
              </div>

              <label className="flex gap-3 text-sm text-slate-300">
                <input required type="checkbox" className="mt-1" />
                <span>{t.consent}</span>
              </label>

              <button
                type="submit"
                className="rounded-xl bg-cyan-300 px-6 py-3 font-semibold text-slate-950 hover:bg-cyan-200"
              >
                {t.submit}
              </button>

              <p className="text-xs text-slate-500">
                {t.disclaimer}
              </p>
            </form>
          )}
        </div>
      </div>
    </main>
  );
}
