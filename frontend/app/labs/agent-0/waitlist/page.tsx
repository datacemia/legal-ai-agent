"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

const labels: any = {
  en: {
    back: "← Back to Agent 0 concept",
    badge: "Runexa Labs · Agent 0 Waitlist",
    title: "Join the Runexa Agent 0 waitlist",
    subtitle:
      "Get early updates on Runexa’s future AI safety system for homes, cameras, sensors, GPS, and autonomous monitoring.",
    success:
      "Thank you. Your interest has been recorded. Runexa will contact selected early-access users when Agent 0 moves forward.",
    submitError: "Failed to submit waitlist form.",

    fullName: "Full name",
    fullNamePlaceholder: "Your name",
    email: "Email address",
    emailPlaceholder: "you@example.com",
    country: "Country",
    countryPlaceholder: "United States, Morocco, France...",
    profile: "Profile",
    interestLevel: "Interest level",
    protectTarget: "What would you like Agent 0 to protect?",
    message: "Message / use case",
    messagePlaceholder:
      "Tell us what kind of safety or monitoring problem you would like Agent 0 to solve.",
    consent:
      "I agree to be contacted by Runexa Systems about Agent 0 updates, early access, and related product information.",
    submit: "Request early access",
    disclaimer:
      "Agent 0 is a concept and research initiative. It is not publicly available yet.",

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
  },

  fr: {
    back: "← Retour au concept Agent 0",
    badge: "Runexa Labs · Liste d’attente Agent 0",
    title: "Rejoignez la liste d’attente Runexa Agent 0",
    subtitle:
      "Recevez les premières mises à jour sur le futur système d’IA sécurité de Runexa pour maisons, caméras, capteurs, GPS et surveillance autonome.",
    success:
      "Merci. Votre intérêt a bien été enregistré. Runexa contactera certains utilisateurs en accès anticipé lorsque Agent 0 avancera.",
    submitError: "Échec de l’envoi du formulaire de liste d’attente.",

    fullName: "Nom complet",
    fullNamePlaceholder: "Votre nom",
    email: "Adresse e-mail",
    emailPlaceholder: "vous@exemple.com",
    country: "Pays",
    countryPlaceholder: "États-Unis, Maroc, France...",
    profile: "Profil",
    interestLevel: "Niveau d’intérêt",
    protectTarget: "Que souhaitez-vous protéger avec Agent 0 ?",
    message: "Message / cas d’usage",
    messagePlaceholder:
      "Expliquez le problème de sécurité ou de surveillance que vous aimeriez qu’Agent 0 résolve.",
    consent:
      "J’accepte d’être contacté par Runexa Systems au sujet des mises à jour d’Agent 0, de l’accès anticipé et des informations produit associées.",
    submit: "Demander un accès anticipé",
    disclaimer:
      "Agent 0 est une initiative conceptuelle et de recherche. Il n’est pas encore disponible publiquement.",

    profiles: [
      "Propriétaire",
      "Parent / Famille",
      "Gestionnaire immobilier",
      "Passionné de Smart Home",
      "Entreprise de sécurité",
      "Investisseur / Partenaire",
      "Autre",
    ],
    interestLevels: [
      "Accès anticipé",
      "Bêta-testeur",
      "Partenariat",
      "Investissement / demande business",
      "Suivre les mises à jour",
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
    back: "← الرجوع إلى مفهوم Agent 0",
    badge: "Runexa Labs · قائمة انتظار Agent 0",
    title: "انضم إلى قائمة انتظار Runexa Agent 0",
    subtitle:
      "احصل على تحديثات مبكرة حول نظام الأمان المستقبلي من Runexa بالذكاء الاصطناعي للمنازل والكاميرات والحساسات وGPS والمراقبة الذاتية.",
    success:
      "شكراً لك. تم تسجيل اهتمامك. ستتواصل Runexa مع بعض مستخدمي الوصول المبكر عندما يتقدم Agent 0.",
    submitError: "فشل إرسال نموذج قائمة الانتظار.",

    fullName: "الاسم الكامل",
    fullNamePlaceholder: "اسمك",
    email: "البريد الإلكتروني",
    emailPlaceholder: "you@example.com",
    country: "البلد",
    countryPlaceholder: "الولايات المتحدة، المغرب، فرنسا...",
    profile: "الملف الشخصي",
    interestLevel: "مستوى الاهتمام",
    protectTarget: "ماذا تريد أن يحمي Agent 0؟",
    message: "رسالة / حالة استخدام",
    messagePlaceholder:
      "أخبرنا بنوع مشكلة الأمان أو المراقبة التي تريد من Agent 0 حلها.",
    consent:
      "أوافق على أن تتواصل معي Runexa Systems بخصوص تحديثات Agent 0، والوصول المبكر، والمعلومات المتعلقة بالمنتج.",
    submit: "طلب الوصول المبكر",
    disclaimer:
      "Agent 0 هو مبادرة مفهومية وبحثية. وهو غير متاح للعامة بعد.",

    profiles: [
      "مالك منزل",
      "والد / عائلة",
      "مدير عقار",
      "مهتم بـ Smart Home",
      "شركة أمنية",
      "مستثمر / شريك",
      "آخر",
    ],
    interestLevels: [
      "وصول مبكر",
      "مختبر تجريبي",
      "شراكة",
      "استثمار / استفسار تجاري",
      "متابعة التحديثات فقط",
    ],
    protectTargets: [
      "منزل",
      "شقة",
      "مكتب",
      "مستودع",
      "منزل عطلات",
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
