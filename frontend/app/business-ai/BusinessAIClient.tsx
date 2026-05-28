"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getSavedLocale } from "../../lib/i18n";

const translations = {
  en: {
    badge: "Runexa Business Agent",
    title: "AI Business Intelligence & Decision Support",
    subtitle:
      "Runexa Business Agent helps founders, professionals, and organizations analyze business data, identify risks, discover opportunities, and improve strategic decision-making with AI.",
    analyzeBusinessData: "Analyze Business Data",
    viewPricing: "View Pricing",

    businessIntelligence: "Business intelligence",
    businessIntelligenceText:
      "Transform business data into structured insights and recommendations.",
    riskAnalysis: "Risk analysis",
    riskAnalysisText:
      "Identify operational, strategic, and financial risk signals.",
    opportunityDetection: "Opportunity detection",
    opportunityDetectionText:
      "Discover growth opportunities and strategic improvements.",
    aiDecisionSupport: "AI decision support",
    aiDecisionSupportText:
      "Receive practical AI-assisted business recommendations.",

    howItWorks: "How Runexa business AI works",
    steps: [
      "Upload business files or reports",
      "Runexa analyzes risks, opportunities, and strategic signals",
      "Receive structured business intelligence insights",
    ],

    modernTeamsTitle:
      "AI business intelligence for modern teams",
    modernTeamsText1:
      "Runexa Business Agent is designed for business owners, founders, analysts, consultants, and teams that need faster insight from business data. Instead of manually reviewing spreadsheets, reports, KPIs, and operational signals, Runexa turns business information into structured analysis, risk detection, opportunities, forecasts, and decision recommendations.",
    modernTeamsText2:
      "The platform helps users understand revenue performance, expense trends, profitability, business health, operational risks, customer signals, and strategic priorities. It is built for practical business decision support, not generic chatbot responses.",

    useCasesTitle: "Business AI use cases",
    kpiAnalysis: "KPI analysis",
    kpiAnalysisText:
      "Analyze revenue, expenses, profit, growth, cashflow, and operational performance indicators.",
    businessRiskDetection: "Business risk detection",
    businessRiskDetectionText:
      "Identify weak margins, poor data quality, cashflow issues, declining performance, or operational warning signs.",
    aiBusinessReports: "AI business reports",
    aiBusinessReportsText:
      "Generate executive-style business summaries that explain what is happening and what actions matter most.",
    decisionSupport: "Decision support",
    decisionSupportText:
      "Turn business data into practical recommendations for pricing, cost control, growth, and strategy.",

    faqTitle: "Frequently asked questions",
    faq: [
      [
        "What is AI business intelligence?",
        "AI business intelligence uses artificial intelligence to analyze business data, detect patterns, identify risks, and generate decision-ready insights.",
      ],
      [
        "Can Runexa analyze spreadsheets?",
        "Yes. Runexa Business Agent can analyze business files and transform them into structured KPI analysis, risks, opportunities, and recommendations.",
      ],
      [
        "Who should use Runexa Business Agent?",
        "It is useful for founders, business owners, consultants, finance teams, analysts, and organizations that need faster business decision support.",
      ],
      [
        "Does Runexa replace business consultants?",
        "No. Runexa provides decision support and analysis. Important business, legal, financial, or strategic decisions should still be reviewed by qualified professionals.",
      ],
    ],
  },

  fr: {
    badge: "Runexa Business Agent",
    title: "Business Intelligence IA et aide à la décision",
    subtitle:
      "Runexa Business Agent aide les fondateurs, professionnels et organisations à analyser les données business, identifier les risques, découvrir les opportunités et améliorer la prise de décision stratégique avec l’IA.",
    analyzeBusinessData: "Analyser des données business",
    viewPricing: "Voir les tarifs",

    businessIntelligence: "Business intelligence",
    businessIntelligenceText:
      "Transformez les données business en insights structurés et recommandations.",
    riskAnalysis: "Analyse des risques",
    riskAnalysisText:
      "Identifiez les signaux de risque opérationnels, stratégiques et financiers.",
    opportunityDetection: "Détection d’opportunités",
    opportunityDetectionText:
      "Découvrez des opportunités de croissance et des améliorations stratégiques.",
    aiDecisionSupport: "Aide à la décision IA",
    aiDecisionSupportText:
      "Recevez des recommandations business pratiques assistées par l’IA.",

    howItWorks: "Comment fonctionne l’IA business Runexa",
    steps: [
      "Téléversez des fichiers ou rapports business",
      "Runexa analyse les risques, opportunités et signaux stratégiques",
      "Recevez des insights de business intelligence structurés",
    ],

    modernTeamsTitle:
      "Business intelligence IA pour les équipes modernes",
    modernTeamsText1:
      "Runexa Business Agent est conçu pour les propriétaires d’entreprise, fondateurs, analystes, consultants et équipes qui ont besoin d’insights plus rapides à partir de leurs données business. Au lieu de revoir manuellement feuilles de calcul, rapports, KPI et signaux opérationnels, Runexa transforme l’information business en analyse structurée, détection des risques, opportunités, prévisions et recommandations de décision.",
    modernTeamsText2:
      "La plateforme aide les utilisateurs à comprendre la performance du chiffre d’affaires, les tendances de dépenses, la rentabilité, la santé business, les risques opérationnels, les signaux clients et les priorités stratégiques. Elle est conçue pour une aide à la décision business pratique, pas pour des réponses génériques de chatbot.",

    useCasesTitle: "Cas d’usage de l’IA business",
    kpiAnalysis: "Analyse des KPI",
    kpiAnalysisText:
      "Analysez revenus, dépenses, profit, croissance, cashflow et indicateurs de performance opérationnelle.",
    businessRiskDetection: "Détection des risques business",
    businessRiskDetectionText:
      "Identifiez marges faibles, mauvaise qualité des données, problèmes de cashflow, baisse de performance ou signaux d’alerte opérationnels.",
    aiBusinessReports: "Rapports business IA",
    aiBusinessReportsText:
      "Générez des résumés business de type exécutif qui expliquent ce qui se passe et quelles actions comptent le plus.",
    decisionSupport: "Aide à la décision",
    decisionSupportText:
      "Transformez les données business en recommandations pratiques pour les prix, le contrôle des coûts, la croissance et la stratégie.",

    faqTitle: "Questions fréquentes",
    faq: [
      [
        "Qu’est-ce que la business intelligence IA ?",
        "La business intelligence IA utilise l’intelligence artificielle pour analyser les données business, détecter les tendances, identifier les risques et générer des insights prêts pour la décision.",
      ],
      [
        "Runexa peut-il analyser des feuilles de calcul ?",
        "Oui. Runexa Business Agent peut analyser des fichiers business et les transformer en analyse KPI structurée, risques, opportunités et recommandations.",
      ],
      [
        "Qui devrait utiliser Runexa Business Agent ?",
        "Il est utile pour les fondateurs, propriétaires d’entreprise, consultants, équipes finance, analystes et organisations qui ont besoin d’une aide à la décision business plus rapide.",
      ],
      [
        "Runexa remplace-t-il les consultants business ?",
        "Non. Runexa fournit une aide à la décision et une analyse. Les décisions business, juridiques, financières ou stratégiques importantes doivent toujours être revues par des professionnels qualifiés.",
      ],
    ],
  },

  ar: {
    badge: "وكيل Runexa للأعمال",
    title: "ذكاء الأعمال بالذكاء الاصطناعي ودعم القرار",
    subtitle:
      "يساعد Runexa Business Agent المؤسسين والمهنيين والمؤسسات على تحليل بيانات الأعمال وتحديد المخاطر واكتشاف الفرص وتحسين اتخاذ القرار الاستراتيجي باستخدام الذكاء الاصطناعي.",
    analyzeBusinessData: "تحليل بيانات الأعمال",
    viewPricing: "عرض الأسعار",

    businessIntelligence: "ذكاء الأعمال",
    businessIntelligenceText:
      "حوّل بيانات الأعمال إلى رؤى منظمة وتوصيات عملية.",
    riskAnalysis: "تحليل المخاطر",
    riskAnalysisText:
      "حدد إشارات المخاطر التشغيلية والاستراتيجية والمالية.",
    opportunityDetection: "اكتشاف الفرص",
    opportunityDetectionText:
      "اكتشف فرص النمو والتحسينات الاستراتيجية.",
    aiDecisionSupport: "دعم القرار بالذكاء الاصطناعي",
    aiDecisionSupportText:
      "احصل على توصيات أعمال عملية مدعومة بالذكاء الاصطناعي.",

    howItWorks: "كيف يعمل الذكاء الاصطناعي للأعمال في Runexa",
    steps: [
      "ارفع ملفات أو تقارير الأعمال",
      "يحلل Runexa المخاطر والفرص والإشارات الاستراتيجية",
      "احصل على رؤى منظمة لذكاء الأعمال",
    ],

    modernTeamsTitle:
      "ذكاء الأعمال بالذكاء الاصطناعي للفرق الحديثة",
    modernTeamsText1:
      "تم تصميم Runexa Business Agent لأصحاب الأعمال والمؤسسين والمحللين والاستشاريين والفرق التي تحتاج إلى رؤى أسرع من بيانات الأعمال. بدلًا من مراجعة الجداول والتقارير ومؤشرات الأداء والإشارات التشغيلية يدويًا، يحول Runexa معلومات الأعمال إلى تحليل منظم واكتشاف للمخاطر والفرص والتوقعات وتوصيات القرار.",
    modernTeamsText2:
      "تساعد المنصة المستخدمين على فهم أداء الإيرادات واتجاهات المصاريف والربحية وصحة الأعمال والمخاطر التشغيلية وإشارات العملاء والأولويات الاستراتيجية. تم بناؤها لدعم قرارات الأعمال بشكل عملي، وليس لإجابات عامة مثل روبوتات المحادثة.",

    useCasesTitle: "حالات استخدام ذكاء الأعمال",
    kpiAnalysis: "تحليل مؤشرات الأداء",
    kpiAnalysisText:
      "حلل الإيرادات والمصاريف والربح والنمو والتدفق النقدي ومؤشرات الأداء التشغيلية.",
    businessRiskDetection: "اكتشاف مخاطر الأعمال",
    businessRiskDetectionText:
      "حدد الهوامش الضعيفة أو جودة البيانات المنخفضة أو مشاكل التدفق النقدي أو انخفاض الأداء أو إشارات التحذير التشغيلية.",
    aiBusinessReports: "تقارير أعمال بالذكاء الاصطناعي",
    aiBusinessReportsText:
      "أنشئ ملخصات أعمال تنفيذية تشرح ما يحدث وما الإجراءات الأكثر أهمية.",
    decisionSupport: "دعم القرار",
    decisionSupportText:
      "حوّل بيانات الأعمال إلى توصيات عملية للتسعير والتحكم في التكاليف والنمو والاستراتيجية.",

    faqTitle: "أسئلة شائعة",
    faq: [
      [
        "ما هو ذكاء الأعمال بالذكاء الاصطناعي؟",
        "يستخدم ذكاء الأعمال بالذكاء الاصطناعي تقنيات الذكاء الاصطناعي لتحليل بيانات الأعمال واكتشاف الأنماط وتحديد المخاطر وإنشاء رؤى جاهزة لاتخاذ القرار.",
      ],
      [
        "هل يمكن لـ Runexa تحليل الجداول؟",
        "نعم. يمكن لـ Runexa Business Agent تحليل ملفات الأعمال وتحويلها إلى تحليل KPI منظم ومخاطر وفرص وتوصيات.",
      ],
      [
        "من يجب أن يستخدم Runexa Business Agent؟",
        "هو مفيد للمؤسسين وأصحاب الأعمال والاستشاريين وفرق المالية والمحللين والمؤسسات التي تحتاج إلى دعم أسرع لقرارات الأعمال.",
      ],
      [
        "هل يستبدل Runexa مستشاري الأعمال؟",
        "لا. يوفر Runexa دعمًا للقرار وتحليلًا. يجب دائمًا مراجعة القرارات التجارية أو القانونية أو المالية أو الاستراتيجية المهمة من قبل مختصين مؤهلين.",
      ],
    ],
  },
};

export default function BusinessAIClient() {
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
        <p className="font-semibold text-amber-600">
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
            href="/business"
            className="rounded-xl bg-amber-600 px-6 py-3 text-sm font-semibold text-white hover:bg-amber-700"
          >
            {t.analyzeBusinessData}
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
          [t.businessIntelligence, t.businessIntelligenceText],
          [t.riskAnalysis, t.riskAnalysisText],
          [t.opportunityDetection, t.opportunityDetectionText],
          [t.aiDecisionSupport, t.aiDecisionSupportText],
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
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-amber-600 text-sm font-bold text-white">
                {index + 1}
              </div>

              <p className="mt-4 font-semibold">
                {step}
              </p>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto mt-16 max-w-6xl">
        <h2 className="text-3xl font-bold">
          {t.modernTeamsTitle}
        </h2>

        <p className="mt-5 max-w-4xl text-lg leading-8 text-slate-600">
          {t.modernTeamsText1}
        </p>

        <p className="mt-5 max-w-4xl text-lg leading-8 text-slate-600">
          {t.modernTeamsText2}
        </p>
      </section>

      <section className="mx-auto mt-16 max-w-6xl rounded-3xl border bg-white p-8 shadow-sm md:p-12">
        <h2 className="text-3xl font-bold">
          {t.useCasesTitle}
        </h2>

        <div className="mt-8 grid gap-6 md:grid-cols-2">
          {[
            [t.kpiAnalysis, t.kpiAnalysisText],
            [t.businessRiskDetection, t.businessRiskDetectionText],
            [t.aiBusinessReports, t.aiBusinessReportsText],
            [t.decisionSupport, t.decisionSupportText],
          ].map(([title, desc]) => (
            <div
              key={title}
              className="rounded-2xl bg-slate-50 p-6"
            >
              <h3 className="font-bold">
                {title}
              </h3>

              <p className="mt-3 text-sm leading-6 text-slate-600">
                {desc}
              </p>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto mt-16 max-w-6xl">
        <h2 className="text-3xl font-bold">
          {t.faqTitle}
        </h2>

        <div className="mt-8 space-y-4">
          {t.faq.map(([question, answer]) => (
            <div
              key={question}
              className="rounded-2xl border bg-white p-6 shadow-sm"
            >
              <h3 className="font-bold">
                {question}
              </h3>

              <p className="mt-3 text-sm leading-6 text-slate-600">
                {answer}
              </p>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
