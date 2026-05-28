"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getSavedLocale } from "../../lib/i18n";

const translations = {
  en: {
    badge: "Runexa Finance Coach",
    title: "AI Financial Analysis & Personal Finance Coach",
    subtitle:
      "Runexa Finance Coach helps users analyze PDF bank statements, understand spending patterns, detect subscriptions, identify savings opportunities, and improve financial habits.",
    tryFinanceCoach: "Try Finance Coach",
    viewPricing: "View Pricing",

    bankStatementAnalysis: "Bank statement analysis",
    bankStatementAnalysisText:
      "Upload PDF bank statements and receive structured financial insights.",
    subscriptionDetection: "Subscription detection",
    subscriptionDetectionText:
      "Find recurring charges and review possible subscription waste.",
    savingsOpportunities: "Savings opportunities",
    savingsOpportunitiesText:
      "Identify practical ways to reduce expenses and improve cashflow.",
    aiFinanceCoach: "AI finance coach",
    aiFinanceCoachText:
      "Ask follow-up questions and get personalized explanations from your analysis.",

    howItWorks: "How Runexa finance AI works",
    steps: [
      "Upload a PDF bank statement",
      "Runexa analyzes transactions, subscriptions, spending, and cashflow",
      "Receive insights, charts, budget recommendations, and coaching",
    ],

    faqTitle: "Finance AI FAQ",
    faq: [
      [
        "Does Runexa replace a financial advisor?",
        "No. Runexa provides informational financial analysis and decision-support output. It does not replace professional financial advice.",
      ],
      [
        "What files can the Finance Coach analyze?",
        "Runexa Finance Coach is designed for PDF bank statements.",
      ],
      [
        "Can Runexa detect subscriptions?",
        "Yes. Runexa can identify recurring charges and highlight potential subscription spending patterns.",
      ],
      [
        "Can I ask questions after the analysis?",
        "Yes. The Finance Coach includes a conversational AI assistant for follow-up questions based on your analysis.",
      ],
    ],

    jsonDescription:
      "AI finance coach for bank statement analysis, subscription detection, savings opportunities, and financial habits.",
  },

  fr: {
    badge: "Runexa Finance Coach",
    title: "Analyse financière IA et coach de finances personnelles",
    subtitle:
      "Runexa Finance Coach aide les utilisateurs à analyser des relevés bancaires PDF, comprendre leurs dépenses, détecter les abonnements, identifier les opportunités d’économies et améliorer leurs habitudes financières.",
    tryFinanceCoach: "Tester le coach financier",
    viewPricing: "Voir les tarifs",

    bankStatementAnalysis: "Analyse des relevés bancaires",
    bankStatementAnalysisText:
      "Téléversez des relevés bancaires PDF et recevez des insights financiers structurés.",
    subscriptionDetection: "Détection des abonnements",
    subscriptionDetectionText:
      "Identifiez les charges récurrentes et les dépenses d’abonnements potentiellement inutiles.",
    savingsOpportunities: "Opportunités d’économies",
    savingsOpportunitiesText:
      "Identifiez des moyens pratiques de réduire les dépenses et d’améliorer le cashflow.",
    aiFinanceCoach: "Coach financier IA",
    aiFinanceCoachText:
      "Posez des questions de suivi et obtenez des explications personnalisées à partir de votre analyse.",

    howItWorks: "Comment fonctionne l’IA finance Runexa",
    steps: [
      "Téléversez un relevé bancaire PDF",
      "Runexa analyse les transactions, abonnements, dépenses et cashflow",
      "Recevez des insights, graphiques, recommandations budgétaires et coaching",
    ],

    faqTitle: "FAQ IA finance",
    faq: [
      [
        "Runexa remplace-t-il un conseiller financier ?",
        "Non. Runexa fournit une analyse financière informative et une aide à la décision. Il ne remplace pas un conseil financier professionnel.",
      ],
      [
        "Quels fichiers le Finance Coach peut-il analyser ?",
        "Runexa Finance Coach est conçu pour les relevés bancaires PDF.",
      ],
      [
        "Runexa peut-il détecter les abonnements ?",
        "Oui. Runexa peut identifier les charges récurrentes et mettre en évidence les habitudes de dépenses liées aux abonnements.",
      ],
      [
        "Puis-je poser des questions après l’analyse ?",
        "Oui. Le Finance Coach inclut un assistant IA conversationnel pour les questions de suivi basées sur votre analyse.",
      ],
    ],

    jsonDescription:
      "Coach financier IA pour l’analyse des relevés bancaires, la détection des abonnements, les opportunités d’économies et les habitudes financières.",
  },

  ar: {
    badge: "مدرب Runexa المالي",
    title: "تحليل مالي بالذكاء الاصطناعي ومدرب للمالية الشخصية",
    subtitle:
      "يساعد Runexa Finance Coach المستخدمين على تحليل كشوف الحساب البنكية بصيغة PDF، وفهم أنماط الإنفاق، واكتشاف الاشتراكات، وتحديد فرص الادخار، وتحسين العادات المالية.",
    tryFinanceCoach: "جرّب المدرب المالي",
    viewPricing: "عرض الأسعار",

    bankStatementAnalysis: "تحليل الكشوف البنكية",
    bankStatementAnalysisText:
      "ارفع كشوفًا بنكية PDF واحصل على رؤى مالية منظمة.",
    subscriptionDetection: "اكتشاف الاشتراكات",
    subscriptionDetectionText:
      "اكتشف المدفوعات المتكررة وراجع مصاريف الاشتراكات غير الضرورية المحتملة.",
    savingsOpportunities: "فرص الادخار",
    savingsOpportunitiesText:
      "حدد طرقًا عملية لتقليل المصاريف وتحسين التدفق النقدي.",
    aiFinanceCoach: "مدرب مالي بالذكاء الاصطناعي",
    aiFinanceCoachText:
      "اطرح أسئلة متابعة واحصل على تفسيرات مخصصة بناءً على تحليلك.",

    howItWorks: "كيف يعمل الذكاء الاصطناعي المالي في Runexa",
    steps: [
      "ارفع كشف حساب بنكي PDF",
      "يحلل Runexa المعاملات والاشتراكات والإنفاق والتدفق النقدي",
      "احصل على رؤى ورسوم بيانية وتوصيات للميزانية وتوجيه مالي",
    ],

    faqTitle: "أسئلة شائعة حول الذكاء المالي",
    faq: [
      [
        "هل يستبدل Runexa المستشار المالي؟",
        "لا. يوفر Runexa تحليلًا ماليًا معلوماتيًا ومخرجات لدعم القرار، ولا يحل محل الاستشارة المالية المهنية.",
      ],
      [
        "ما الملفات التي يمكن لـ Finance Coach تحليلها؟",
        "تم تصميم Runexa Finance Coach لتحليل كشوف الحساب البنكية بصيغة PDF.",
      ],
      [
        "هل يمكن لـ Runexa اكتشاف الاشتراكات؟",
        "نعم. يمكن لـ Runexa تحديد الرسوم المتكررة وإبراز أنماط الإنفاق المرتبطة بالاشتراكات.",
      ],
      [
        "هل يمكنني طرح أسئلة بعد التحليل؟",
        "نعم. يتضمن Finance Coach مساعدًا حواريًا بالذكاء الاصطناعي لأسئلة المتابعة بناءً على تحليلك.",
      ],
    ],

    jsonDescription:
      "مدرب مالي بالذكاء الاصطناعي لتحليل الكشوف البنكية واكتشاف الاشتراكات وفرص الادخار والعادات المالية.",
  },
};

export default function FinanceAIClient() {
  const [locale, setLocale] =
    useState<"en" | "fr" | "ar">("en");

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

  return (
    <main
      dir={locale === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-6 py-20 text-slate-900"
    >
      <section className="mx-auto max-w-6xl text-center">
        <p className="font-semibold text-emerald-600">
          {t.badge}
        </p>

        <h1 className="mt-4 text-5xl font-bold tracking-tight">
          {t.title}
        </h1>

        <p className="mx-auto mt-6 max-w-3xl text-lg text-slate-600">
          {t.subtitle}
        </p>

        <div className="mt-8 flex flex-wrap justify-center gap-3">
          <Link
            href="/finance"
            className="rounded-xl bg-emerald-600 px-6 py-3 text-sm font-semibold text-white hover:bg-emerald-700"
          >
            {t.tryFinanceCoach}
          </Link>

          <Link
            href="/pricing"
            className="rounded-xl border border-slate-200 bg-white px-6 py-3 text-sm font-semibold text-slate-900 hover:bg-slate-50"
          >
            {t.viewPricing}
          </Link>
        </div>
      </section>

      <section className="mx-auto mt-16 grid max-w-6xl gap-6 md:grid-cols-4">
        {[
          [t.bankStatementAnalysis, t.bankStatementAnalysisText],
          [t.subscriptionDetection, t.subscriptionDetectionText],
          [t.savingsOpportunities, t.savingsOpportunitiesText],
          [t.aiFinanceCoach, t.aiFinanceCoachText],
        ].map(([title, desc]) => (
          <div
            key={title}
            className="rounded-2xl border bg-white p-6 shadow-sm"
          >
            <h2 className="font-bold">
              {title}
            </h2>

            <p className="mt-3 text-sm leading-6 text-slate-600">
              {desc}
            </p>
          </div>
        ))}
      </section>

      <section className="mx-auto mt-16 max-w-6xl rounded-3xl border bg-white p-8 shadow-sm md:p-12">
        <h2 className="text-3xl font-bold">
          {t.howItWorks}
        </h2>

        <div className="mt-8 grid gap-4 md:grid-cols-3">
          {t.steps.map((step, index) => (
            <div
              key={step}
              className="rounded-2xl bg-slate-50 p-6"
            >
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-600 text-sm font-bold text-white">
                {index + 1}
              </div>

              <p className="mt-4 font-semibold">
                {step}
              </p>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto mt-16 max-w-6xl rounded-3xl border bg-white p-8 shadow-sm md:p-12">
        <h2 className="text-3xl font-bold">
          {t.faqTitle}
        </h2>

        <div className="mt-8 grid gap-4 md:grid-cols-2">
          {t.faq.map(([q, a]) => (
            <div
              key={q}
              className="rounded-2xl bg-slate-50 p-6"
            >
              <h3 className="font-bold">
                {q}
              </h3>

              <p className="mt-2 text-sm leading-6 text-slate-600">
                {a}
              </p>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
