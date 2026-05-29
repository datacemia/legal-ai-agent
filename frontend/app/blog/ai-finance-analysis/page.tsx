"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getSavedLocale } from "../../../lib/i18n";



const translations = {
  en: {
    back: "← Back to Blog",

    category: "Financial Intelligence",

    title:
      "AI Finance Analysis: Understanding Spending, Subscriptions, and Savings",

    intro:
      "Managing personal finances can be difficult when financial data is fragmented across statements, transactions, subscriptions, and recurring expenses. AI finance analysis helps users understand spending patterns, identify subscriptions, detect waste, and improve financial visibility.",

    whatIs:
      "What is AI finance analysis?",

    whatIsText:
      "AI finance analysis uses artificial intelligence to review bank statements and financial activity, generate insights, detect recurring expenses, identify waste, summarize spending behavior, and improve visibility into personal finances.",

    why:
      "Why financial visibility matters",

    whyText:
      "Small recurring expenses, subscription charges, impulse purchases, and inconsistent spending habits can have a significant impact over time. Understanding where money goes is often the first step toward improving financial health.",

    subscriptionDetection:
      "Subscription detection",

    subscriptionDetectionText:
      "AI can identify recurring payments such as streaming services, software tools, hosting platforms, memberships, and online subscriptions.",

    spendingAnalysis:
      "Spending analysis",

    spendingAnalysisText:
      "AI can categorize transactions and show where most monthly spending occurs.",

    savingsOpportunities:
      "Savings opportunities",

    savingsOpportunitiesText:
      "AI can highlight areas where spending may be reduced, optimized, or reviewed more carefully.",

    cashflowVisibility:
      "Cashflow visibility",

    cashflowVisibilityText:
      "AI can help users understand inflows, outflows, recurring expenses, and financial balance trends.",

    useCases:
      "Common use cases for AI finance analysis",

    useCasesText:
      "AI finance analysis can support budgeting, subscription tracking, monthly expense reviews, spending optimization, financial habit awareness, and personal cashflow monitoring.",

    runexa:
      "How Runexa Finance Coach helps",

    runexaText:
      "Runexa Finance Coach helps users upload bank statements, analyze transactions, identify subscriptions, detect waste, discover savings opportunities, and ask follow-up questions through a conversational AI assistant.",

    support:
      "AI should support financial awareness, not replace financial judgment",

    supportText:
      "AI finance tools are most useful when they improve visibility and understanding. Financial decisions should still be evaluated with personal context, qualified advice when needed, and long-term goals in mind.",

    ctaTitle:
      "Understand your finances with AI",

    ctaText:
      "Use Runexa Finance Coach to analyze bank statements, subscriptions, spending habits, and savings opportunities.",

    ctaButton:
      "Analyze Financial Data",

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

    category: "Intelligence financière",

    title:
      "Analyse financière par IA : comprendre les dépenses, les abonnements et les opportunités d’économies",

    intro:
      "Gérer ses finances personnelles peut être complexe lorsque les données financières sont dispersées entre relevés bancaires, transactions, abonnements et dépenses récurrentes. L’analyse financière par IA aide à mieux comprendre les habitudes de dépenses, identifier les abonnements, détecter les gaspillages et améliorer la visibilité financière.",

    whatIs:
      "Qu’est-ce que l’analyse financière par IA ?",

    whatIsText:
      "L’analyse financière par IA utilise l’intelligence artificielle pour examiner les relevés bancaires et l’activité financière, générer des insights, détecter les dépenses récurrentes, identifier les sources de gaspillage, résumer les comportements de dépenses et améliorer la visibilité sur les finances personnelles.",

    why:
      "Pourquoi la visibilité financière est importante",

    whyText:
      "Les petites dépenses récurrentes, les abonnements, les achats impulsifs et les habitudes de consommation irrégulières peuvent avoir un impact significatif à long terme. Comprendre où va son argent constitue souvent la première étape vers une meilleure santé financière.",

    subscriptionDetection:
      "Détection des abonnements",

    subscriptionDetectionText:
      "L’IA peut identifier les paiements récurrents tels que les services de streaming, les logiciels, les plateformes d’hébergement, les adhésions et les abonnements en ligne.",

    spendingAnalysis:
      "Analyse des dépenses",

    spendingAnalysisText:
      "L’IA peut catégoriser les transactions et mettre en évidence les principaux postes de dépenses mensuelles.",

    savingsOpportunities:
      "Opportunités d’économies",

    savingsOpportunitiesText:
      "L’IA peut identifier les domaines où les dépenses peuvent être réduites, optimisées ou examinées plus attentivement.",

    cashflowVisibility:
      "Visibilité des flux financiers",

    cashflowVisibilityText:
      "L’IA peut aider à comprendre les entrées, les sorties, les dépenses récurrentes et les tendances générales de l’équilibre financier.",

    useCases:
      "Cas d’usage courants de l’analyse financière par IA",

    useCasesText:
      "L’analyse financière par IA peut accompagner la gestion du budget, le suivi des abonnements, la revue des dépenses mensuelles, l’optimisation des dépenses, la compréhension des habitudes financières et le suivi des flux financiers personnels.",

    runexa:
      "Comment Runexa Finance Coach aide",

    runexaText:
      "Runexa Finance Coach permet aux utilisateurs de téléverser des relevés bancaires, d’analyser les transactions, d’identifier les abonnements, de détecter les gaspillages, de découvrir des opportunités d’économies et de poser des questions complémentaires via un assistant conversationnel alimenté par l’IA.",

    support:
      "L’IA doit améliorer la compréhension financière, pas remplacer le jugement financier",

    supportText:
      "Les outils d’analyse financière par IA sont particulièrement utiles lorsqu’ils améliorent la visibilité et la compréhension. Les décisions financières doivent toujours être prises en tenant compte du contexte personnel, d’un avis professionnel lorsque nécessaire et des objectifs à long terme.",

    ctaTitle:
      "Comprenez mieux vos finances grâce à l’IA",

    ctaText:
      "Utilisez Runexa Finance Coach pour analyser vos relevés bancaires, abonnements, habitudes de dépenses et opportunités d’économies.",

    ctaButton:
      "Analyser un relevé bancaire",

    features: [
      "Suivi des abonnements",
      "Recommandations d’économies",
      "Synthèses des flux financiers",
      "Analyse des habitudes financières",
      "Coaching financier par IA",
      "Questions-réponses financières interactives",
    ],
  },
  ar: {
    back: "← العودة إلى المدونة",

    category: "الذكاء المالي",

    title:
      "التحليل المالي بالذكاء الاصطناعي: فهم الإنفاق والاشتراكات وفرص الادخار",

    intro:
      "قد تكون إدارة الشؤون المالية الشخصية معقدة عندما تكون البيانات موزعة بين الكشوف البنكية والمعاملات والاشتراكات والمصروفات المتكررة. يساعد التحليل المالي بالذكاء الاصطناعي المستخدمين على فهم أنماط الإنفاق وتحديد الاشتراكات واكتشاف الهدر وتحسين الرؤية المالية.",

    whatIs:
      "ما هو التحليل المالي بالذكاء الاصطناعي؟",

    whatIsText:
      "يستخدم التحليل المالي بالذكاء الاصطناعي تقنيات الذكاء الاصطناعي لمراجعة الكشوف البنكية والنشاط المالي، وإنشاء رؤى تحليلية، واكتشاف المصروفات المتكررة، وتحديد مصادر الهدر، وتلخيص أنماط الإنفاق، وتحسين فهم الوضع المالي الشخصي.",

    why:
      "لماذا تعد الرؤية المالية مهمة؟",

    whyText:
      "قد يكون للمصروفات الصغيرة المتكررة والاشتراكات والمشتريات الاندفاعية والعادات المالية غير المنتظمة تأثير كبير على المدى الطويل. وغالباً ما يكون فهم كيفية إنفاق الأموال هو الخطوة الأولى نحو تحسين الصحة المالية.",

    subscriptionDetection:
      "اكتشاف الاشتراكات",

    subscriptionDetectionText:
      "يمكن للذكاء الاصطناعي تحديد المدفوعات المتكررة مثل خدمات البث الرقمي والأدوات البرمجية ومنصات الاستضافة والعضويات والاشتراكات عبر الإنترنت.",

    spendingAnalysis:
      "تحليل الإنفاق",

    spendingAnalysisText:
      "يمكن للذكاء الاصطناعي تصنيف المعاملات وإبراز الفئات التي تستحوذ على الجزء الأكبر من الإنفاق الشهري.",

    savingsOpportunities:
      "فرص الادخار",

    savingsOpportunitiesText:
      "يمكن للذكاء الاصطناعي تحديد المجالات التي يمكن فيها تقليل الإنفاق أو تحسينه أو مراجعته بشكل أكثر فعالية.",

    cashflowVisibility:
      "وضوح التدفقات النقدية",

    cashflowVisibilityText:
      "يمكن للذكاء الاصطناعي مساعدة المستخدمين على فهم التدفقات الداخلة والخارجة والمصروفات المتكررة والاتجاهات العامة للتوازن المالي.",

    useCases:
      "حالات الاستخدام الشائعة للتحليل المالي بالذكاء الاصطناعي",

    useCasesText:
      "يمكن للتحليل المالي بالذكاء الاصطناعي دعم إعداد الميزانيات وتتبع الاشتراكات ومراجعة المصروفات الشهرية وتحسين الإنفاق وفهم العادات المالية ومراقبة التدفقات النقدية الشخصية.",

    runexa:
      "كيف يساعد Runexa Finance Coach",

    runexaText:
      "يُمكّن Runexa Finance Coach المستخدمين من رفع الكشوف البنكية وتحليل المعاملات وتحديد الاشتراكات واكتشاف الهدر والعثور على فرص الادخار وطرح أسئلة متابعة عبر مساعد محادثة مدعوم بالذكاء الاصطناعي.",

    support:
      "يجب أن يعزز الذكاء الاصطناعي الوعي المالي لا أن يحل محل الحكم المالي",

    supportText:
      "تكون أدوات التحليل المالي بالذكاء الاصطناعي أكثر فائدة عندما تساعد على تحسين الرؤية والفهم. ويجب دائماً اتخاذ القرارات المالية مع مراعاة الظروف الشخصية والأهداف طويلة المدى والاستعانة بمشورة متخصصة عند الحاجة.",

    ctaTitle:
      "افهم أموالك بشكل أفضل باستخدام الذكاء الاصطناعي",

    ctaText:
      "استخدم Runexa Finance Coach لتحليل الكشوف البنكية والاشتراكات وعادات الإنفاق وفرص الادخار.",

    ctaButton:
      "تحليل كشف بنكي",

    features: [
      "تتبع الاشتراكات",
      "توصيات للادخار",
      "ملخصات التدفقات النقدية",
      "تحليل العادات المالية",
      "إرشاد مالي بالذكاء الاصطناعي",
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