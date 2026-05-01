"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

const labels: any = {
  en: {
    platform: "Runexa AI Agents Platform",
    title: "AI agents that help you get work done faster.",
    desc: "Runexa provides AI agents that help you analyze documents, make smarter decisions, and move faster.",
    explore: "Explore agents",
    tryLegal: "Try Legal Agent",
    tryStudy: "Try Study Agent",
    tryFinance: "Try Finance Coach",
    choose: "Choose your AI agent",

    // ✅ UPDATED
    chooseDesc:
      "One account to access all Runexa AI agents (Legal, Study, Finance, Business).",

    available: "Available",
    coming: "Coming soon",
    open: "Open agent",
    pricing: "See pricing",
    ctaTitle: "One platform. Multiple AI agents. Real business outcomes.",
    ctaDesc:
      "Runexa Systems is an AI agents platform that helps you analyze documents, learn faster, manage personal finances, and make smarter business decisions.",
    ctaButton: "Start with Runexa Systems",
    agents: [
      [
        "Legal Agent",
        "Analyze contracts, detect risky clauses, and get clear recommendations before you sign.",
      ],
      [
        "Study Agent",
        "Analyze study materials, generate summaries, quizzes, and smart revision plans.",
      ],
      [
        "Personal Finance Coach Agent",
        "Analyze your expenses, detect waste, and provide actionable saving strategies.",
      ],
      [
        "Business Decision Agent",
        "Analyze business data, detect trends, and support smarter strategic decisions.",
      ],
    ],
  },

  fr: {
    platform: "Plateforme d’agents IA Runexa",
    title: "Des agents IA pour travailler plus vite.",
    desc: "Runexa propose des agents IA qui vous aident à analyser vos documents, prendre de meilleures décisions et avancer plus vite.",
    explore: "Explorer les agents",
    tryLegal: "Tester l’agent juridique",
    tryStudy: "Tester l’agent étude",
    tryFinance: "Tester le coach financier",
    choose: "Choisissez votre agent IA",

    // ✅ UPDATED
    chooseDesc:
      "Un seul compte pour accéder à tous les agents IA Runexa (juridique, étude, finance, business).",

    available: "Disponible",
    coming: "Bientôt",
    open: "Ouvrir l’agent",
    pricing: "Voir les tarifs",
    ctaTitle: "Une plateforme. Plusieurs agents IA. Des résultats concrets.",
    ctaDesc:
      "Runexa Systems est une plateforme d’agents IA qui vous permet d’analyser vos documents, apprendre plus vite, gérer vos finances personnelles et prendre des décisions business plus intelligentes.",
    ctaButton: "Commencer avec Runexa Systems",
    agents: [
      [
        "Agent juridique",
        "Analysez vos contrats, détectez les clauses à risque et obtenez des recommandations claires.",
      ],
      [
        "Agent étude",
        "Analysez vos cours, générez des résumés, quiz et plans de révision intelligents.",
      ],
      [
        "Agent coach financier personnel",
        "Analysez vos dépenses, détectez le gaspillage et recevez des stratégies d’épargne concrètes.",
      ],
      [
        "Agent décision business",
        "Analysez vos données business, identifiez les tendances et prenez de meilleures décisions stratégiques.",
      ],
    ],
  },

  ar: {
    platform: "منصة Runexa للوكلاء الذكيين",
    title: "وكلاء ذكاء اصطناعي يساعدونك على إنجاز العمل بسرعة.",
    desc: "توفر Runexa وكلاء ذكاء اصطناعي يساعدونك على تحليل المستندات واتخاذ قرارات أفضل والعمل بشكل أسرع.",
    explore: "استكشاف الوكلاء",
    tryLegal: "تجربة الوكيل القانوني",
    tryStudy: "تجربة وكيل الدراسة",
    tryFinance: "تجربة وكيل الإدارة المالية",
    choose: "اختر وكيلك الذكي",

    // ✅ UPDATED
    chooseDesc:
      "حساب واحد للوصول إلى جميع وكلاء Runexa للذكاء الاصطناعي (القانوني، الدراسة، المالية، الأعمال).",

    available: "متاح",
    coming: "قريباً",
    open: "فتح الوكيل",
    pricing: "عرض الأسعار",
    ctaTitle: "منصة واحدة. عدة وكلاء ذكاء اصطناعي. نتائج عملية.",
    ctaDesc:
      "Runexa Systems هي منصة وكلاء ذكاء اصطناعي تساعدك على تحليل المستندات، التعلم بشكل أسرع، إدارة أموالك الشخصية، واتخاذ قرارات أعمال أكثر ذكاءً.",
    ctaButton: "ابدأ مع Runexa Systems",
    agents: [
      [
        "الوكيل القانوني",
        "حلل العقود، واكتشف البنود الخطرة، واحصل على توصيات واضحة.",
      ],
      [
        "وكيل الدراسة",
        "حلل المواد الدراسية، وأنشئ ملخصات واختبارات وخطط مراجعة ذكية.",
      ],
      [
        "وكيل الإدارة المالية الشخصية",
        "حلل مصاريفك، واكتشف الهدر، واحصل على استراتيجيات ادخار فعالة.",
      ],
      [
        "وكيل قرارات الأعمال",
        "حلل بيانات الأعمال، واكتشف الاتجاهات، واتخذ قرارات استراتيجية أفضل.",
      ],
    ],
  },
};

const agentLinks = ["/upload", "/study", "/finance", "/business"];

export default function HomePage() {
  const [language, setLanguage] = useState("en");
  const t = labels[language] || labels.en;

  useEffect(() => {
    const saved = localStorage.getItem("locale");
    if (saved && labels[saved]) {
      setLanguage(saved);
    }
  }, []);

  const handleLanguageChange = (lang: string) => {
    setLanguage(lang);
    localStorage.setItem("locale", lang);
    window.dispatchEvent(new Event("locale-change"));
  };

  return (
    <main
      dir={language === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 text-slate-900"
    >
      <section className="px-6 py-20">
        <div className="max-w-6xl mx-auto text-center space-y-8">
          <div className="flex justify-center">
            <select
              value={language}
              onChange={(e) => handleLanguageChange(e.target.value)}
              className="border rounded-lg px-3 py-2 bg-white"
            >
              <option value="en">English</option>
              <option value="fr">Français</option>
              <option value="ar">العربية</option>
            </select>
          </div>

          <p className="text-blue-600 font-semibold">{t.platform}</p>
          <h1 className="text-5xl font-bold leading-tight">{t.title}</h1>
          <p className="text-lg text-slate-600 max-w-3xl mx-auto">
            {t.desc}
          </p>

          <div className="flex flex-wrap justify-center gap-4">
            <a
              href="#agents"
              className="px-6 py-3 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition"
            >
              {t.explore}
            </a>

            <Link href="/upload" className="px-6 py-3 bg-white border border-slate-200 rounded-xl font-semibold hover:bg-slate-100 transition">
              {t.tryLegal}
            </Link>

            <Link href="/study" className="px-6 py-3 bg-white border border-slate-200 rounded-xl font-semibold hover:bg-slate-100 transition">
              {t.tryStudy}
            </Link>

            <Link href="/finance" className="px-6 py-3 bg-green-600 text-white rounded-xl font-semibold hover:bg-green-700 transition">
              {t.tryFinance}
            </Link>

            <Link href="/pricing" className="px-6 py-3 bg-white border border-slate-200 rounded-xl font-semibold hover:bg-slate-100 transition">
              {t.pricing}
            </Link>
          </div>
        </div>
      </section>

      <section id="agents" className="px-6 py-12">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-10">
            <h2 className="text-3xl font-bold">{t.choose}</h2>
            <p className="mt-3 text-slate-600">{t.chooseDesc}</p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {t.agents.map((agent: string[], index: number) => {
              const isAvailable = index <= 3;

              return (
                <div key={agent[0]} className="bg-white p-6 rounded-2xl border shadow-sm flex flex-col justify-between">
                  <div>
                    <div className="flex items-center justify-between gap-3">
                      <h3 className="text-xl font-bold">
                        {agent[0]}
                      </h3>
                      <span className="text-xs bg-slate-100 text-slate-600 px-3 py-1 rounded-full">
                        {isAvailable ? t.available : t.coming}
                      </span>
                    </div>

                    <p className="mt-4 text-slate-600">{agent[1]}</p>
                  </div>

                  {isAvailable ? (
                    <Link
                      href={agentLinks[index]}
                      className="inline-block mt-6 text-center px-4 py-2 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition"
                    >
                      {t.open}
                    </Link>
                  ) : (
                    <button
                      disabled
                      className="mt-6 px-4 py-2 bg-slate-100 text-slate-400 rounded-xl font-semibold"
                    >
                      {t.coming}
                    </button>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </section>

      <section className="px-6 py-16">
        <div className="max-w-5xl mx-auto bg-blue-600 text-white rounded-3xl p-10 text-center">
          <h2 className="text-3xl font-bold">{t.ctaTitle}</h2>
          <p className="mt-4 text-blue-100">{t.ctaDesc}</p>

          <Link href="/upload" className="inline-block mt-6 px-6 py-3 bg-white text-blue-600 rounded-xl font-semibold">
            {t.ctaButton}
          </Link>

          <p className="mt-8 text-center text-sm text-slate-500 max-w-2xl mx-auto">
            AI-powered insights. Always verify before you act.
          </p>
        </div>
      </section>
    </main>
  );
}