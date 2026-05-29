"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getSavedLocale } from "../../lib/i18n";

const translations = {
  en: {
    badge: "Runexa Business Agent",

    title: "AI Business Intelligence & Decision Support",

    subtitle:
        "Transform business data into actionable insights, identify risks, uncover opportunities, and make better decisions with AI-powered business intelligence.",

    analyzeBusinessData: "Analyze Business Data",
    viewPricing: "View Pricing",

    businessIntelligence: "Business Intelligence",
    businessIntelligenceText:
        "Turn business data into structured insights, forecasts, and strategic recommendations.",

    riskAnalysis: "Risk Analysis",
    riskAnalysisText:
        "Identify financial, operational, and strategic risks before they become larger problems.",

    opportunityDetection: "Opportunity Discovery",
    opportunityDetectionText:
        "Uncover growth opportunities, efficiency improvements, and untapped business potential.",

    aiDecisionSupport: "AI Decision Support",
    aiDecisionSupportText:
        "Receive practical recommendations to support faster and more informed decisions.",

    howItWorks: "How Runexa Business Agent Works",

    steps: [
        "Upload business files, reports, or structured data",
        "Runexa analyzes performance, risks, opportunities, and key business signals",
        "Receive structured insights, forecasts, and recommendations",
    ],

    modernTeamsTitle:
        "Business intelligence built for modern teams",

    modernTeamsText1:
        "Runexa Business Agent helps founders, operators, consultants, analysts, and leadership teams gain faster insights from business data. Instead of manually reviewing spreadsheets, reports, KPIs, and operational metrics, Runexa transforms information into structured analysis, risk assessments, growth opportunities, forecasts, and strategic recommendations.",

    modernTeamsText2:
        "The platform helps organizations understand revenue performance, profitability, spending trends, business health, operational risks, customer behavior, and strategic priorities. It is designed for real-world decision support, not generic chatbot conversations.",

    useCasesTitle: "Business AI Use Cases",

    kpiAnalysis: "KPI Analysis",
    kpiAnalysisText:
        "Analyze revenue, expenses, profitability, growth, cashflow, and operational performance metrics.",

    businessRiskDetection: "Business Risk Detection",
    businessRiskDetectionText:
        "Identify weak margins, declining performance, cashflow concerns, data quality issues, and operational warning signals.",

    aiBusinessReports: "Executive AI Reports",
    aiBusinessReportsText:
        "Generate executive-ready business summaries that explain performance, risks, opportunities, and recommended actions.",

    decisionSupport: "Strategic Decision Support",
    decisionSupportText:
        "Convert business data into actionable recommendations for growth, pricing, profitability, efficiency, and strategy.",

    faqTitle: "Frequently Asked Questions",

    faq: [
        [
        "What is AI business intelligence?",
        "AI business intelligence uses artificial intelligence to analyze business data, detect patterns, identify risks, uncover opportunities, and generate decision-ready insights.",
        ],
        [
        "Can Runexa analyze spreadsheets?",
        "Yes. Runexa Business Agent can analyze spreadsheets, reports, and structured business files to generate KPI analysis, risk assessments, opportunity discovery, and recommendations.",
        ],
        [
        "Who should use Runexa Business Agent?",
        "Runexa is designed for founders, executives, business owners, consultants, analysts, finance teams, and organizations that need faster business insights and decision support.",
        ],
        [
        "Does Runexa replace consultants or advisors?",
        "No. Runexa provides analysis and decision support. Important business, financial, legal, or strategic decisions should always be reviewed by qualified professionals.",
        ],
    ],
    },

 fr: {
    badge: "Runexa Business Agent",

    title: "Business Intelligence IA et aide à la décision",

    subtitle:
        "Transformez vos données d’entreprise en insights exploitables, identifiez les risques, détectez les opportunités et prenez de meilleures décisions grâce à l’intelligence artificielle.",

    analyzeBusinessData: "Analyser des données d’entreprise",
    viewPricing: "Voir les tarifs",

    businessIntelligence: "Business Intelligence",

    businessIntelligenceText:
        "Transformez vos données en analyses structurées, prévisions et recommandations stratégiques.",

    riskAnalysis: "Analyse des risques",

    riskAnalysisText:
        "Identifiez les risques financiers, opérationnels et stratégiques avant qu’ils ne deviennent des problèmes majeurs.",

    opportunityDetection: "Détection d’opportunités",

    opportunityDetectionText:
        "Repérez les leviers de croissance, les gains d’efficacité et les opportunités inexploitées.",

    aiDecisionSupport: "Aide à la décision IA",

    aiDecisionSupportText:
        "Recevez des recommandations concrètes pour prendre des décisions plus rapides et mieux informées.",

    howItWorks: "Comment fonctionne Runexa Business Agent",

    steps: [
        "Téléversez vos fichiers, rapports ou données d’entreprise",
        "Runexa analyse les performances, risques, opportunités et signaux clés",
        "Recevez des analyses structurées, prévisions et recommandations",
    ],

    modernTeamsTitle:
        "La Business Intelligence conçue pour les équipes modernes",

    modernTeamsText1:
        "Runexa Business Agent aide les dirigeants, fondateurs, consultants, analystes et équipes opérationnelles à obtenir plus rapidement des insights à partir de leurs données. Au lieu d’analyser manuellement des feuilles de calcul, rapports, KPI et indicateurs d’activité, Runexa transforme les données en analyses structurées, évaluations des risques, opportunités de croissance, prévisions et recommandations stratégiques.",

    modernTeamsText2:
        "La plateforme permet de mieux comprendre les revenus, la rentabilité, les dépenses, la santé de l’entreprise, les risques opérationnels, le comportement des clients et les priorités stratégiques. Elle est conçue pour l’aide à la décision en conditions réelles, et non pour fournir de simples réponses de chatbot.",

    useCasesTitle: "Cas d’usage de l’IA pour les entreprises",

    kpiAnalysis: "Analyse des KPI",

    kpiAnalysisText:
        "Analysez le chiffre d’affaires, les dépenses, la rentabilité, la croissance, le cash-flow et les indicateurs de performance opérationnelle.",

    businessRiskDetection: "Détection des risques",

    businessRiskDetectionText:
        "Identifiez les marges insuffisantes, les problèmes de qualité des données, les risques de trésorerie, les baisses de performance et les signaux d’alerte opérationnels.",

    aiBusinessReports: "Rapports exécutifs IA",

    aiBusinessReportsText:
        "Générez des synthèses exécutives expliquant les performances, les risques, les opportunités et les actions recommandées.",

    decisionSupport: "Aide à la décision stratégique",

    decisionSupportText:
        "Transformez vos données en recommandations concrètes pour la croissance, la rentabilité, la maîtrise des coûts et la stratégie.",

    faqTitle: "Questions fréquentes",

    faq: [
        [
        "Qu’est-ce que la Business Intelligence IA ?",
        "La Business Intelligence IA utilise l’intelligence artificielle pour analyser les données d’entreprise, détecter des tendances, identifier des risques, révéler des opportunités et produire des analyses directement exploitables."
        ],
        [
        "Runexa peut-il analyser des feuilles de calcul ?",
        "Oui. Runexa Business Agent peut analyser des feuilles de calcul, rapports et fichiers structurés afin de générer des analyses KPI, des évaluations des risques, des opportunités de croissance et des recommandations."
        ],
        [
        "À qui s’adresse Runexa Business Agent ?",
        "Runexa est conçu pour les dirigeants, fondateurs, propriétaires d’entreprise, consultants, analystes, équipes financières et organisations qui ont besoin d’analyses rapides pour soutenir leurs décisions."
        ],
        [
        "Runexa remplace-t-il les consultants ou les conseillers ?",
        "Non. Runexa fournit des analyses et une aide à la décision. Les décisions stratégiques, financières, juridiques ou opérationnelles importantes doivent toujours être validées par des professionnels qualifiés."
        ]
    ]
    },

  ar: {
    badge: "وكيل Runexa للأعمال",

    title: "ذكاء الأعمال المدعوم بالذكاء الاصطناعي ودعم اتخاذ القرار",

    subtitle:
        "حوّل بيانات الأعمال إلى رؤى قابلة للتنفيذ، وحدد المخاطر، واكتشف فرص النمو، واتخذ قرارات أكثر فاعلية بمساعدة الذكاء الاصطناعي.",

    analyzeBusinessData: "تحليل بيانات الأعمال",
    viewPricing: "عرض الأسعار",

    businessIntelligence: "ذكاء الأعمال",

    businessIntelligenceText:
        "حوّل بياناتك إلى تحليلات منظمة وتوقعات وتوصيات استراتيجية.",

    riskAnalysis: "تحليل المخاطر",

    riskAnalysisText:
        "اكتشف المخاطر المالية والتشغيلية والاستراتيجية قبل أن تتحول إلى تحديات أكبر.",

    opportunityDetection: "اكتشاف الفرص",

    opportunityDetectionText:
        "حدّد فرص النمو ومجالات تحسين الكفاءة والإمكانات غير المستغلة.",

    aiDecisionSupport: "دعم اتخاذ القرار بالذكاء الاصطناعي",

    aiDecisionSupportText:
        "احصل على توصيات عملية تساعدك على اتخاذ قرارات أسرع وأكثر دقة.",

    howItWorks: "كيف يعمل Runexa Business Agent",

    steps: [
        "ارفع ملفات الأعمال أو التقارير أو البيانات المنظمة",
        "يقوم Runexa بتحليل الأداء والمخاطر والفرص والمؤشرات الرئيسية",
        "احصل على تحليلات منظمة وتوقعات وتوصيات قابلة للتنفيذ",
    ],

    modernTeamsTitle:
        "ذكاء أعمال مصمم للفرق الحديثة",

    modernTeamsText1:
        "يساعد Runexa Business Agent المديرين والمؤسسين والاستشاريين والمحللين والفرق التشغيلية على الحصول على رؤى أسرع من بيانات الأعمال. وبدلاً من مراجعة الجداول والتقارير ومؤشرات الأداء يدويًا، يحول Runexa البيانات إلى تحليلات منظمة وتقييمات للمخاطر وفرص للنمو وتوقعات وتوصيات استراتيجية.",

    modernTeamsText2:
        "تمكّن المنصة المؤسسات من فهم الإيرادات والربحية واتجاهات الإنفاق وصحة الأعمال والمخاطر التشغيلية وسلوك العملاء والأولويات الاستراتيجية. وقد صُممت لدعم اتخاذ القرار في بيئات العمل الحقيقية، وليس لتقديم إجابات عامة شبيهة بروبوتات المحادثة.",

    useCasesTitle:
        "حالات استخدام الذكاء الاصطناعي في الأعمال",

    kpiAnalysis: "تحليل مؤشرات الأداء الرئيسية",

    kpiAnalysisText:
        "حلّل الإيرادات والمصروفات والربحية والنمو والتدفق النقدي ومؤشرات الأداء التشغيلية.",

    businessRiskDetection: "اكتشاف مخاطر الأعمال",

    businessRiskDetectionText:
        "حدّد الهوامش الضعيفة ومشكلات جودة البيانات ومخاطر التدفق النقدي وتراجع الأداء والإشارات التشغيلية التحذيرية.",

    aiBusinessReports: "تقارير تنفيذية بالذكاء الاصطناعي",

    aiBusinessReportsText:
        "أنشئ ملخصات تنفيذية تشرح الأداء والمخاطر والفرص والإجراءات الموصى بها.",

    decisionSupport: "دعم القرار الاستراتيجي",

    decisionSupportText:
        "حوّل بيانات الأعمال إلى توصيات عملية للنمو وتحسين الربحية وضبط التكاليف وتطوير الاستراتيجية.",

    faqTitle: "الأسئلة الشائعة",

    faq: [
        [
        "ما هو ذكاء الأعمال المدعوم بالذكاء الاصطناعي؟",
        "يعتمد ذكاء الأعمال المدعوم بالذكاء الاصطناعي على تحليل بيانات الأعمال لاكتشاف الأنماط وتحديد المخاطر والفرص وإنشاء رؤى تدعم اتخاذ القرار."
        ],
        [
        "هل يمكن لـ Runexa تحليل الجداول والملفات؟",
        "نعم. يستطيع Runexa Business Agent تحليل الجداول والتقارير وملفات الأعمال المنظمة لإنتاج تحليلات لمؤشرات الأداء وتقييمات للمخاطر وفرص للنمو وتوصيات عملية."
        ],
        [
        "لمن صُمم Runexa Business Agent؟",
        "صُمم Runexa للمديرين التنفيذيين والمؤسسين وأصحاب الأعمال والاستشاريين والمحللين والفرق المالية والمؤسسات التي تحتاج إلى رؤى أسرع لدعم قراراتها."
        ],
        [
        "هل يستبدل Runexa المستشارين أو الخبراء؟",
        "لا. يوفر Runexa التحليل ودعم اتخاذ القرار، لكن القرارات الاستراتيجية أو المالية أو القانونية أو التشغيلية المهمة يجب أن تُراجع دائمًا من قبل مختصين مؤهلين."
        ]
    ]
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
