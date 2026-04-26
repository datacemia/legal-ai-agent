"use client";

import Link from "next/link";
import { useState } from "react";

const labels: any = {
  en: {
    platform: "Runexa AI Agents Platform",
    title: "AI agents that help you get work done faster.",
    desc: "Runexa brings specialized AI agents for legal, finance, HR, business, and more — all in one simple platform.",
    explore: "Explore agents",
    tryLegal: "Try Legal Agent",
    choose: "Choose your AI agent",
    chooseDesc: "Start with Legal Agent today. More specialized agents are coming soon.",
    available: "Available",
    coming: "Coming soon",
    open: "Open agent",
    ctaTitle: "One platform. Multiple AI agents. Real business outcomes.",
    ctaDesc: "Start with contract analysis today, then expand into finance, HR, operations, and business automation as your needs grow.",
    ctaButton: "Start with Legal Agent",
    footerDesc: "Specialized AI agents for legal, finance, HR, and business productivity.",
    developedBy: "Developed by Dr. Rachid Ejjami",
    products: "Products",
    platformFooter: "Platform",
    about: "About",
    copyright: "© 2025 Runexa AI. All rights reserved.",
    agents: [
      ["Legal Agent", "Analyze contracts, detect risky clauses, and get clear recommendations before you sign."],
      ["Finance Agent", "Review invoices, budgets, expenses, and financial documents faster."],
      ["HR Agent", "Analyze CVs, job descriptions, HR policies, and employee documents."],
      ["Business Agent", "Generate summaries, reports, strategies, and business insights."],
    ],
  },
  fr: {
    platform: "Plateforme d’agents IA Runexa",
    title: "Des agents IA pour travailler plus vite.",
    desc: "Runexa réunit des agents IA spécialisés pour le juridique, la finance, les RH, le business et plus encore.",
    explore: "Explorer les agents",
    tryLegal: "Tester l’agent juridique",
    choose: "Choisissez votre agent IA",
    chooseDesc: "Commencez avec l’agent juridique. D’autres agents spécialisés arrivent bientôt.",
    available: "Disponible",
    coming: "Bientôt",
    open: "Ouvrir l’agent",
    ctaTitle: "Une plateforme. Plusieurs agents IA. Des résultats concrets.",
    ctaDesc: "Commencez avec l’analyse de contrats, puis développez vers la finance, les RH et l’automatisation business.",
    ctaButton: "Commencer avec l’agent juridique",
    footerDesc: "Agents IA spécialisés pour le juridique, la finance, les RH et la productivité business.",
    developedBy: "Développé par Dr. Rachid Ejjami",
    products: "Produits",
    platformFooter: "Plateforme",
    about: "À propos",
    copyright: "© 2025 Runexa AI. Tous droits réservés.",
    agents: [
      ["Agent juridique", "Analysez vos contrats, détectez les clauses à risque et obtenez des recommandations claires."],
      ["Agent finance", "Analysez factures, budgets, dépenses et documents financiers plus rapidement."],
      ["Agent RH", "Analysez CV, fiches de poste, politiques RH et documents employés."],
      ["Agent business", "Générez des résumés, rapports, stratégies et insights business."],
    ],
  },
  ar: {
    platform: "منصة Runexa للوكلاء الذكيين",
    title: "وكلاء ذكاء اصطناعي يساعدونك على إنجاز العمل بسرعة.",
    desc: "تجمع Runexa وكلاء متخصصين في القانون والمالية والموارد البشرية والأعمال في منصة واحدة.",
    explore: "استكشاف الوكلاء",
    tryLegal: "تجربة الوكيل القانوني",
    choose: "اختر وكيلك الذكي",
    chooseDesc: "ابدأ بالوكيل القانوني اليوم. المزيد من الوكلاء المتخصصين قريباً.",
    available: "متاح",
    coming: "قريباً",
    open: "فتح الوكيل",
    ctaTitle: "منصة واحدة. عدة وكلاء ذكاء اصطناعي. نتائج عملية.",
    ctaDesc: "ابدأ بتحليل العقود، ثم توسع إلى المالية والموارد البشرية وأتمتة الأعمال.",
    ctaButton: "ابدأ بالوكيل القانوني",
    footerDesc: "وكلاء ذكاء اصطناعي متخصصون للقانون والمالية والموارد البشرية والأعمال.",
    developedBy: "تم التطوير بواسطة Dr. Rachid Ejjami",
    products: "المنتجات",
    platformFooter: "المنصة",
    about: "حول",
    copyright: "© 2025 Runexa AI. جميع الحقوق محفوظة.",
    agents: [
      ["الوكيل القانوني", "حلل العقود، واكتشف البنود الخطرة، واحصل على توصيات واضحة."],
      ["وكيل المالية", "راجع الفواتير والميزانيات والمصاريف والوثائق المالية بسرعة."],
      ["وكيل الموارد البشرية", "حلل السير الذاتية والوصف الوظيفي وسياسات الموارد البشرية."],
      ["وكيل الأعمال", "أنشئ ملخصات وتقارير واستراتيجيات ورؤى عملية."],
    ],
  },
};

const agentLinks = ["/upload", "#", "#", "#"];

export default function HomePage() {
  const [language, setLanguage] = useState("en");
  const t = labels[language] || labels.en;

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
              onChange={(e) => setLanguage(e.target.value)}
              className="border rounded-lg px-3 py-2 bg-white"
            >
              <option value="en">English</option>
              <option value="fr">Français</option>
              <option value="ar">العربية</option>
            </select>
          </div>

          <p className="text-blue-600 font-semibold">{t.platform}</p>

          <h1 className="text-5xl font-bold leading-tight">{t.title}</h1>

          <p className="text-lg text-slate-600 max-w-3xl mx-auto">{t.desc}</p>

          <div className="flex justify-center gap-4">
            <a
              href="#agents"
              className="px-6 py-3 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition"
            >
              {t.explore}
            </a>

            <Link
              href="/upload"
              className="px-6 py-3 bg-white border border-slate-200 rounded-xl font-semibold hover:bg-slate-100 transition"
            >
              {t.tryLegal}
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
              const isAvailable = index === 0;

              return (
                <div
                  key={agent[0]}
                  className="bg-white p-6 rounded-2xl border shadow-sm flex flex-col justify-between"
                >
                  <div>
                    <div className="flex items-center justify-between gap-3">
                      <h3 className="text-xl font-bold">{agent[0]}</h3>
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
                      className="mt-6 px-4 py-2 bg-slate-100 text-slate-400 rounded-xl font-semibold cursor-not-allowed"
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

          <Link
            href="/upload"
            className="inline-block mt-6 px-6 py-3 bg-white text-blue-600 rounded-xl font-semibold"
          >
            {t.ctaButton}
          </Link>
        </div>
      </section>

      
    </main>
  );
}