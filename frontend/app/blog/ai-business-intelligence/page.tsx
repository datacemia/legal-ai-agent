"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getSavedLocale } from "../../../lib/i18n";

const translations = {
  en: {
    back: "← Back to Blog",

    category: "Business Intelligence",

    title:
      "AI Business Intelligence: Turning Data into Better Decisions",

    intro:
      "Business intelligence is no longer limited to dashboards and static reports. Modern AI systems can help organizations understand performance, identify risks, uncover opportunities, and generate actionable insights faster.",

    whatIs:
      "What is AI business intelligence?",

    whatIsText:
      "AI business intelligence combines structured business data with artificial intelligence to help organizations understand performance, trends, risks, and growth opportunities.",

    why:
      "Why dashboards alone are not enough",

    whyText:
      "Dashboards provide visibility, but they often require users to interpret the data themselves. AI adds context and reasoning that transform metrics into actionable business insights.",

    riskDetection:
      "Risk detection",

    riskDetectionText:
      "AI can identify early warning signals such as declining revenue, increasing costs, customer concentration, operational bottlenecks, and performance anomalies.",

    opportunityDiscovery:
      "Opportunity discovery",

    opportunityDiscoveryText:
      "AI can uncover growth opportunities, high-performing segments, underutilized channels, and areas where resources can be allocated more effectively.",

    executiveSummaries:
      "Executive summaries",

    executiveSummariesText:
      "AI can convert complex business data into concise summaries for executives, managers, and decision-makers.",

    decisionSupport:
      "Decision support",

    decisionSupportText:
      "AI can recommend next steps based on performance metrics, operational risks, and strategic objectives.",

    useCases:
      "Common use cases for AI business intelligence",

    useCasesText:
      "AI business intelligence supports a wide range of workflows, from startup planning and financial forecasting to operational reporting and executive decision-making.",

    runexa:
      "How Runexa Business Agent helps",

    runexaText:
      "Runexa Business Agent enables organizations to upload structured business data, analyze performance, identify risks, uncover opportunities, and generate AI-powered recommendations.",

    support:
      "AI should support decisions, not replace judgment",

    supportText:
      "The most effective business AI systems help teams make better decisions through clearer reasoning and faster analysis. AI-generated insights should always be reviewed alongside human expertise.",

    ctaTitle:
      "Turn business data into actionable insights",

    ctaText:
      "Use Runexa Business Agent to analyze performance, risks, opportunities, KPIs, and strategic decisions with AI.",

    ctaButton:
      "Analyze Business Data",

    features: [
      "Business performance analysis",
      "Risk and opportunity detection",
      "KPI interpretation",
      "Executive AI summaries",
      "Strategic recommendations",
      "Exportable business reports",
    ],
  },

  fr: {
    back: "← Retour au blog",

    category: "Business Intelligence",

    title:
      "Business Intelligence IA : transformer les données en meilleures décisions",

    intro:
      "La business intelligence ne se limite plus aux tableaux de bord et aux rapports statiques. Les systèmes d’IA modernes aident les organisations à comprendre leur performance, identifier les risques, détecter les opportunités et générer des insights actionnables plus rapidement.",

    whatIs:
      "Qu’est-ce que la business intelligence IA ?",

    whatIsText:
      "La business intelligence IA combine des données business structurées avec l’intelligence artificielle afin d’aider les organisations à comprendre leurs performances, leurs tendances, leurs risques et leurs opportunités de croissance.",

    why:
      "Pourquoi les tableaux de bord seuls ne suffisent pas",

    whyText:
      "Les tableaux de bord offrent de la visibilité, mais ils nécessitent souvent une interprétation humaine. L’IA ajoute une couche de contexte et de raisonnement qui transforme les métriques en insights business exploitables.",

    riskDetection:
      "Détection des risques",

    riskDetectionText:
      "L’IA peut identifier des signaux d’alerte précoces tels qu’une baisse du chiffre d’affaires, une hausse des coûts, une concentration excessive des clients, des goulets d’étranglement opérationnels ou des anomalies de performance.",

    opportunityDiscovery:
      "Découverte d’opportunités",

    opportunityDiscoveryText:
      "L’IA peut révéler des opportunités de croissance, des segments performants, des canaux sous-exploités et des domaines où les ressources peuvent être allouées plus efficacement.",

    executiveSummaries:
      "Résumés exécutifs",

    executiveSummariesText:
      "L’IA peut transformer des données complexes en synthèses claires destinées aux dirigeants, managers et décideurs.",

    decisionSupport:
      "Aide à la décision",

    decisionSupportText:
      "L’IA peut recommander des actions à entreprendre en fonction des performances, des risques opérationnels et des objectifs stratégiques.",

    useCases:
      "Cas d’usage courants de la business intelligence IA",

    useCasesText:
      "La business intelligence IA prend en charge de nombreux workflows, de la planification de startups et des prévisions financières jusqu’au reporting opérationnel et à la prise de décision stratégique.",

    runexa:
      "Comment Runexa Business Agent aide",

    runexaText:
      "Runexa Business Agent permet aux organisations de téléverser des données business structurées, d’analyser les performances, d’identifier les risques, de détecter les opportunités et de générer des recommandations alimentées par l’IA.",

    support:
      "L’IA doit soutenir les décisions, pas remplacer le jugement",

    supportText:
      "Les systèmes d’IA les plus performants aident les équipes à prendre de meilleures décisions grâce à une analyse plus rapide et un raisonnement plus clair. Les insights générés par l’IA doivent toujours être examinés avec l’expertise humaine.",

    ctaTitle:
      "Transformez vos données business en insights actionnables",

    ctaText:
      "Utilisez Runexa Business Agent pour analyser les performances, les risques, les opportunités, les KPI et les décisions stratégiques grâce à l’IA.",

    ctaButton:
      "Analyser des données business",

    features: [
      "Analyse des performances business",
      "Détection des risques et opportunités",
      "Interprétation des KPI",
      "Résumés exécutifs IA",
      "Recommandations stratégiques",
      "Rapports business exportables",
    ],
  },

  ar: {
    back: "← العودة إلى المدونة",

    category: "ذكاء الأعمال",

    title:
      "ذكاء الأعمال المدعوم بالذكاء الاصطناعي: تحويل البيانات إلى قرارات أفضل",

    intro:
      "لم يعد ذكاء الأعمال يقتصر على لوحات المعلومات والتقارير الثابتة. تساعد أنظمة الذكاء الاصطناعي الحديثة المؤسسات على فهم الأداء وتحديد المخاطر واكتشاف الفرص وتوليد رؤى قابلة للتنفيذ بسرعة أكبر.",

    whatIs:
      "ما هو ذكاء الأعمال المدعوم بالذكاء الاصطناعي؟",

    whatIsText:
      "يجمع ذكاء الأعمال المدعوم بالذكاء الاصطناعي بين البيانات المنظمة وتقنيات الذكاء الاصطناعي لمساعدة المؤسسات على فهم الأداء والاتجاهات والمخاطر وفرص النمو.",

    why:
      "لماذا لا تكفي لوحات المعلومات وحدها",

    whyText:
      "توفر لوحات المعلومات رؤية واضحة للبيانات، لكنها غالباً ما تتطلب تفسيراً بشرياً. يضيف الذكاء الاصطناعي طبقة من السياق والاستدلال تحول المقاييس إلى رؤى أعمال قابلة للتنفيذ.",

    riskDetection:
      "اكتشاف المخاطر",

    riskDetectionText:
      "يمكن للذكاء الاصطناعي تحديد إشارات إنذار مبكرة مثل انخفاض الإيرادات وارتفاع التكاليف والتركيز المفرط للعملاء والاختناقات التشغيلية والانحرافات في الأداء.",

    opportunityDiscovery:
      "اكتشاف الفرص",

    opportunityDiscoveryText:
      "يمكن للذكاء الاصطناعي الكشف عن فرص النمو والقطاعات عالية الأداء والقنوات غير المستغلة والمجالات التي يمكن فيها تخصيص الموارد بشكل أكثر كفاءة.",

    executiveSummaries:
      "الملخصات التنفيذية",

    executiveSummariesText:
      "يمكن للذكاء الاصطناعي تحويل البيانات المعقدة إلى ملخصات واضحة وموجزة للمديرين التنفيذيين وصناع القرار.",

    decisionSupport:
      "دعم اتخاذ القرار",

    decisionSupportText:
      "يمكن للذكاء الاصطناعي اقتراح الخطوات التالية استناداً إلى مؤشرات الأداء والمخاطر التشغيلية والأهداف الاستراتيجية.",

    useCases:
      "حالات الاستخدام الشائعة لذكاء الأعمال",

    useCasesText:
      "يدعم ذكاء الأعمال المدعوم بالذكاء الاصطناعي مجموعة واسعة من الاستخدامات، من تخطيط الشركات الناشئة والتوقعات المالية إلى التقارير التشغيلية واتخاذ القرارات الاستراتيجية.",

    runexa:
      "كيف يساعد Runexa Business Agent",

    runexaText:
      "يمكّن Runexa Business Agent المؤسسات من رفع بيانات أعمال منظمة وتحليل الأداء وتحديد المخاطر واكتشاف الفرص وإنشاء توصيات مدعومة بالذكاء الاصطناعي.",

    support:
      "يجب أن يدعم الذكاء الاصطناعي القرارات لا أن يحل محل الحكم البشري",

    supportText:
      "تساعد أفضل أنظمة الذكاء الاصطناعي الفرق على اتخاذ قرارات أفضل من خلال تحليل أسرع واستدلال أوضح. ويجب دائماً مراجعة الرؤى الناتجة عن الذكاء الاصطناعي إلى جانب الخبرة البشرية.",

    ctaTitle:
      "حوّل بيانات الأعمال إلى رؤى قابلة للتنفيذ",

    ctaText:
      "استخدم Runexa Business Agent لتحليل الأداء والمخاطر والفرص ومؤشرات الأداء والقرارات الاستراتيجية باستخدام الذكاء الاصطناعي.",

    ctaButton:
      "تحليل بيانات الأعمال",

    features: [
      "تحليل أداء الأعمال",
      "اكتشاف المخاطر والفرص",
      "تفسير مؤشرات الأداء",
      "ملخصات تنفيذية بالذكاء الاصطناعي",
      "توصيات استراتيجية",
      "تقارير أعمال قابلة للتصدير",
    ],
  },
};


export default function AIBusinessIntelligenceArticle() {
  const [locale, setLocale] =
    useState<"en" | "fr" | "ar">("en");

  useEffect(() => {
    const saved = getSavedLocale();

    if (saved === "fr" || saved === "ar") {
      setLocale(saved);
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
      <article className="mx-auto max-w-4xl">
        <Link href="/blog" className="text-sm font-semibold text-blue-600">
          {t.back}
        </Link>

        <p className="mt-8 text-sm font-semibold uppercase tracking-wide text-blue-600">
          {t.category}
        </p>

        <h1 className="mt-4 text-5xl font-bold tracking-tight">
          {t.title}
        </h1>

        <p className="mt-6 text-lg leading-8 text-slate-600">
          {t.intro}
        </p>

        <div className="mt-10 rounded-3xl border bg-white p-8 shadow-sm">
          <h2 className="text-2xl font-bold">{t.whatIs}</h2>
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
              [t.riskDetection, t.riskDetectionText],
              [t.opportunityDiscovery, t.opportunityDiscoveryText],
              [t.executiveSummaries, t.executiveSummariesText],
              [t.decisionSupport, t.decisionSupportText],
            ].map(([title, text]) => (
              <div key={title} className="rounded-2xl border bg-white p-6 shadow-sm">
                <h3 className="font-bold">{title}</h3>
                <p className="mt-3 text-sm leading-6 text-slate-600">{text}</p>
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

        <section className="mt-12 rounded-3xl bg-blue-600 p-8 text-white">
          <h2 className="text-3xl font-bold">
            {t.ctaTitle}
          </h2>
          <p className="mt-4 text-blue-100">
            {t.ctaText}
          </p>

          <Link
            href="/business"
            className="mt-6 inline-block rounded-xl bg-white px-6 py-3 text-sm font-semibold text-blue-600"
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
              headline:
                t.title,
              description:
                "Learn how AI business intelligence helps teams analyze data, detect risks, identify opportunities, and improve strategic decision-making.",
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