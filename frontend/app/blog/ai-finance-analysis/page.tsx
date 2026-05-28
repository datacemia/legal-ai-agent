"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getSavedLocale } from "../../../lib/i18n";



const translations = {
  en: {
    back: "{t.back}",
    category: "{t.category}",
    title: "{t.title}",
    intro:
      "Managing personal finances is often difficult because financial data is fragmented, repetitive, and time-consuming to analyze. AI finance analysis can help users better understand spending patterns, subscriptions, savings opportunities, and overall financial habits.",
    whatIs: "{t.whatIs}",
    whatIsText:
      "AI finance analysis uses artificial intelligence to analyze bank statements and financial activity in order to generate insights, detect recurring expenses, identify waste, summarize spending behavior, and improve financial visibility.",
    why: "{t.why}",
    whyText:
      "Many people underestimate how much small recurring expenses, subscription charges, impulse purchases, or inconsistent spending habits affect long-term financial stability. Understanding where money goes is often the first step toward improving financial health.",
    subscriptionDetection: "Subscription detection",
    subscriptionDetectionText:
      "AI can identify recurring payments such as streaming services, software tools, hosting platforms, and online subscriptions.",
    spendingAnalysis: "Spending analysis",
    spendingAnalysisText:
      "AI can categorize transactions and reveal where most monthly spending occurs.",
    savingsOpportunities: "Savings opportunities",
    savingsOpportunitiesText:
      "AI can highlight areas where spending may be reduced or optimized.",
    cashflowVisibility: "Cashflow visibility",
    cashflowVisibilityText:
      "AI can help users understand inflows, outflows, and financial balance trends.",
    useCases: "{t.useCases}",
    useCasesText:
      "AI finance analysis can support budgeting, subscription tracking, monthly expense reviews, spending optimization, financial habit awareness, and personal cashflow monitoring.",
    runexa: "{t.runexa}",
    runexaText:
      "Runexa Finance Coach helps users upload PDF bank statements, analyze transactions, identify subscriptions, detect waste, discover savings opportunities, and ask follow-up questions through a conversational AI assistant.",
    support: "{t.support}",
    supportText:
      "AI finance tools are most useful when they improve visibility and understanding. Financial decisions should still be evaluated with personal context, professional advice when necessary, and long-term goals in mind.",
    ctaTitle: "{t.ctaTitle}",
    ctaText:
      "Use Runexa Finance Coach to analyze bank statements, subscriptions, spending habits, and savings opportunities.",
    ctaButton: "{t.ctaButton}",
    features: [
      "Subscription tracking",
      "Savings recommendations",
      "Cashflow summaries",
      "Financial habit analysis",
      "AI financial coaching",
      "Interactive financial Q&A",
    ],
  },

  fr: {
    back: "← Retour au blog",
    category: "IA finance",
    title: "Analyse financière IA : comprendre dépenses, économies et cashflow",
    intro:
      "Gérer ses finances personnelles est souvent difficile, car les données financières sont fragmentées, répétitives et longues à analyser. L’analyse financière IA aide à mieux comprendre les dépenses, abonnements, opportunités d’économies et habitudes financières.",
    whatIs: "Qu’est-ce que l’analyse financière IA ?",
    whatIsText:
      "L’analyse financière IA utilise l’intelligence artificielle pour analyser les relevés bancaires et l’activité financière afin de générer des insights, détecter les dépenses récurrentes, identifier le gaspillage et améliorer la visibilité financière.",
    why: "Pourquoi l’analyse financière est importante",
    whyText:
      "Beaucoup de personnes sous-estiment l’impact des petites dépenses récurrentes, abonnements, achats impulsifs et habitudes irrégulières sur la stabilité financière.",
    subscriptionDetection: "Détection des abonnements",
    subscriptionDetectionText:
      "L’IA peut identifier les paiements récurrents comme les services de streaming, outils logiciels, plateformes d’hébergement et abonnements en ligne.",
    spendingAnalysis: "Analyse des dépenses",
    spendingAnalysisText:
      "L’IA peut catégoriser les transactions et montrer où se concentrent les dépenses mensuelles.",
    savingsOpportunities: "Opportunités d’économies",
    savingsOpportunitiesText:
      "L’IA peut mettre en évidence les zones où les dépenses peuvent être réduites ou optimisées.",
    cashflowVisibility: "Visibilité du cashflow",
    cashflowVisibilityText:
      "L’IA peut aider à comprendre les entrées, sorties et tendances générales du solde financier.",
    useCases: "Cas d’usage courants de l’IA finance",
    useCasesText:
      "L’analyse financière IA peut aider au budget, suivi des abonnements, revue mensuelle des dépenses, optimisation financière et suivi du cashflow personnel.",
    runexa: "Comment Runexa Finance Coach aide",
    runexaText:
      "Runexa Finance Coach aide les utilisateurs à téléverser des relevés bancaires PDF, analyser les transactions, détecter les abonnements, identifier le gaspillage et découvrir des opportunités d’économies.",
    support: "L’IA doit améliorer la visibilité, pas remplacer le jugement",
    supportText:
      "Les outils IA finance sont utiles lorsqu’ils améliorent la compréhension. Les décisions financières doivent toujours tenir compte du contexte personnel, des objectifs long terme et, si nécessaire, d’un avis professionnel.",
    ctaTitle: "Comprenez vos finances avec l’IA",
    ctaText:
      "Utilisez Runexa Finance Coach pour analyser relevés bancaires, abonnements, habitudes de dépenses et opportunités d’économies.",
    ctaButton: "Téléverser un relevé bancaire",
    features: [
      "Suivi des abonnements",
      "Recommandations d’économies",
      "Résumés du cashflow",
      "Analyse des habitudes financières",
      "Coaching financier IA",
      "Questions-réponses financières interactives",
    ],
  },

  ar: {
    back: "← العودة إلى المدونة",
    category: "الذكاء المالي",
    title: "التحليل المالي بالذكاء الاصطناعي: فهم المصاريف والادخار والتدفق النقدي",
    intro:
      "إدارة المالية الشخصية قد تكون صعبة لأن البيانات المالية متفرقة ومتكررة وتحتاج وقتًا للتحليل. يساعد التحليل المالي بالذكاء الاصطناعي على فهم المصاريف والاشتراكات وفرص الادخار والعادات المالية.",
    whatIs: "ما هو التحليل المالي بالذكاء الاصطناعي؟",
    whatIsText:
      "يستخدم التحليل المالي بالذكاء الاصطناعي تقنيات الذكاء الاصطناعي لتحليل الكشوف البنكية والنشاط المالي، واكتشاف المصاريف المتكررة وتلخيص السلوك المالي وتحسين الرؤية المالية.",
    why: "لماذا التحليل المالي مهم",
    whyText:
      "يقلل كثير من الناس من تأثير المصاريف الصغيرة المتكررة والاشتراكات والمشتريات العفوية على الاستقرار المالي طويل المدى.",
    subscriptionDetection: "اكتشاف الاشتراكات",
    subscriptionDetectionText:
      "يمكن للذكاء الاصطناعي تحديد المدفوعات المتكررة مثل خدمات البث والأدوات البرمجية ومنصات الاستضافة والاشتراكات عبر الإنترنت.",
    spendingAnalysis: "تحليل المصاريف",
    spendingAnalysisText:
      "يمكن للذكاء الاصطناعي تصنيف المعاملات وإظهار أين تتركز أغلب المصاريف الشهرية.",
    savingsOpportunities: "فرص الادخار",
    savingsOpportunitiesText:
      "يمكن للذكاء الاصطناعي إبراز المجالات التي يمكن فيها تقليل المصاريف أو تحسينها.",
    cashflowVisibility: "رؤية التدفق النقدي",
    cashflowVisibilityText:
      "يمكن للذكاء الاصطناعي مساعدة المستخدمين على فهم المداخيل والمصاريف واتجاهات الرصيد المالي.",
    useCases: "حالات استخدام شائعة للذكاء المالي",
    useCasesText:
      "يمكن للتحليل المالي بالذكاء الاصطناعي دعم إعداد الميزانية وتتبع الاشتراكات ومراجعة المصاريف الشهرية وتحسين العادات المالية.",
    runexa: "كيف يساعد Runexa Finance Coach",
    runexaText:
      "يساعد Runexa Finance Coach المستخدمين على رفع كشوف بنكية PDF وتحليل المعاملات واكتشاف الاشتراكات والهدر وفرص الادخار.",
    support: "يجب أن يحسن الذكاء الاصطناعي الوعي لا أن يستبدل الحكم الشخصي",
    supportText:
      "تكون أدوات الذكاء المالي مفيدة عندما تحسن الرؤية والفهم. يجب تقييم القرارات المالية حسب السياق الشخصي والأهداف طويلة المدى، ومع استشارة مختص عند الحاجة.",
    ctaTitle: "افهم أموالك باستخدام الذكاء الاصطناعي",
    ctaText:
      "استخدم Runexa Finance Coach لتحليل الكشوف البنكية والاشتراكات وعادات الإنفاق وفرص الادخار.",
    ctaButton: "رفع كشف بنكي",
    features: [
      "تتبع الاشتراكات",
      "توصيات الادخار",
      "ملخصات التدفق النقدي",
      "تحليل العادات المالية",
      "تدريب مالي بالذكاء الاصطناعي",
      "أسئلة وأجوبة مالية تفاعلية",
    ],
  },
};

export default function AIFinanceAnalysisArticle() {
  const [locale, setLocale] =
    useState<"en" | "fr" | "ar">("en");

  useEffect(() => {
    const saved = getSavedLocale();

    if (saved === "fr" || saved === "ar") setLocale(saved);

    const handleLocaleChange = () => {
      const updated = getSavedLocale();

      setLocale(
        updated === "fr" || updated === "ar"
          ? updated
          : "en"
      );
    };

    window.addEventListener(
      "locale-change",
      handleLocaleChange
    );

    return () =>
      window.removeEventListener(
        "locale-change",
        handleLocaleChange
      );
  }, []);

  const t = translations[locale];
  return (
    <main
      dir={locale === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-6 py-20 text-slate-900"
    >
      <article className="mx-auto max-w-4xl">
        <Link href="/blog" className="text-sm font-semibold text-emerald-600">
          {t.back}
        </Link>

        <p className="mt-8 text-sm font-semibold uppercase tracking-wide text-emerald-600">
          {t.category}
        </p>

        <h1 className="mt-4 text-5xl font-bold tracking-tight">
          {t.title}
        </h1>

        <p className="mt-6 text-lg leading-8 text-slate-600">
          {t.intro}
        </p>

        <div className="mt-10 rounded-3xl border bg-white p-8 shadow-sm">
          <h2 className="text-2xl font-bold">
            {t.whatIs}
          </h2>

          <p className="mt-4 leading-8 text-slate-600">
            {t.whatIsText}
          </p>
        </div>

        <section className="mt-10 space-y-8">
          <div>
            <h2 className="text-3xl font-bold">
              {t.why}
            </h2>

            <p className="mt-4 leading-8 text-slate-600">
              {t.whyText}
            </p>
          </div>

          <div className="grid gap-6 md:grid-cols-2">
            {[
              [t.subscriptionDetection, t.subscriptionDetectionText],
              [t.spendingAnalysis, t.spendingAnalysisText],
              [t.savingsOpportunities, t.savingsOpportunitiesText],
              [t.cashflowVisibility, t.cashflowVisibilityText],
            ].map(([title, text]) => (
              <div
                key={title}
                className="rounded-2xl border bg-white p-6 shadow-sm"
              >
                <h3 className="font-bold">{title}</h3>

                <p className="mt-3 text-sm leading-6 text-slate-600">
                  {text}
                </p>
              </div>
            ))}
          </div>

          <div>
            <h2 className="text-3xl font-bold">
              {t.useCases}
            </h2>

            <p className="mt-4 leading-8 text-slate-600">
              {t.useCasesText}
            </p>
          </div>

          <div className="rounded-3xl border bg-white p-8 shadow-sm">
            <h2 className="text-2xl font-bold">
              {t.runexa}
            </h2>

            <p className="mt-4 leading-8 text-slate-600">
              {t.runexaText}
            </p>

            <div className="mt-6 grid gap-3 sm:grid-cols-2">
              {t.features.map((item) => (
                <div
                  key={item}
                  className="rounded-xl bg-slate-50 px-4 py-3 text-sm font-semibold text-slate-700"
                >
                  {item}
                </div>
              ))}
            </div>
          </div>

          <div>
            <h2 className="text-3xl font-bold">
              {t.support}
            </h2>

            <p className="mt-4 leading-8 text-slate-600">
              {t.supportText}
            </p>
          </div>
        </section>

        <section className="mt-12 rounded-3xl bg-emerald-600 p-8 text-white">
          <h2 className="text-3xl font-bold">
            {t.ctaTitle}
          </h2>

          <p className="mt-4 text-emerald-100">
            {t.ctaText}
          </p>

          <Link
            href="/finance"
            className="mt-6 inline-block rounded-xl bg-white px-6 py-3 text-sm font-semibold text-emerald-600"
          >
            {t.ctaButton}
          </Link>
        </section>

        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "Article",
              mainEntityOfPage: {
                "@type": "WebPage",
                "@id":
                  "https://runexa.ai/blog/ai-finance-analysis",
              },
              headline:
                "{t.title}",
              description:
                "Learn how AI finance analysis helps users understand spending patterns, subscriptions, savings opportunities, and financial habits.",
              datePublished: "2026-05-24",
              dateModified: "2026-05-24",
              author: {
                "@type": "Person",
                name: "Dr. Rachid Ejjami",
              },
              publisher: {
                "@type": "Organization",
                name: "Runexa Systems",
              },
            }),
          }}
        />
      </article>
    </main>
  );
}