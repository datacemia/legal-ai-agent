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
      "Business intelligence is no longer only about dashboards and static reports. Modern AI systems can help teams understand business data, detect risks, identify opportunities, and generate decision-ready insights faster.",
    whatIs: "{t.whatIs}",
    whatIsText:
      "AI business intelligence combines structured business data with artificial intelligence to help organizations understand performance, risks, trends, and opportunities.",
    why: "{t.why}",
    whyText:
      "Dashboards are useful, but they often require users to interpret the data themselves. AI adds an interpretation layer that turns raw metrics into practical business context.",
    riskDetection: "Risk detection",
    riskDetectionText:
      "AI can highlight weak signals such as declining revenue, rising costs, customer concentration, or operational bottlenecks.",
    opportunityDiscovery: "Opportunity discovery",
    opportunityDiscoveryText:
      "AI can identify growth signals, high-performing segments, underused channels, or areas where resources could be reallocated.",
    executiveSummaries: "Executive summaries",
    executiveSummariesText:
      "AI can translate complex data into concise summaries for founders, managers, and teams.",
    decisionSupport: "Decision support",
    decisionSupportText:
      "AI can suggest next actions based on business performance, risks, and strategic goals.",
    useCases: "{t.useCases}",
    useCasesText:
      "AI business intelligence can support many workflows, from startup planning to enterprise reporting.",
    runexa: "{t.runexa}",
    runexaText:
      "Runexa Business Agent helps users upload structured business data, analyze performance, detect risks, identify opportunities, and generate AI-powered recommendations.",
    support: "{t.support}",
    supportText:
      "The strongest business AI systems help teams reason more clearly. AI-generated insights should be reviewed and validated with human expertise.",
    ctaTitle: "{t.ctaTitle}",
    ctaText:
      "Use Runexa Business Agent to analyze risks, opportunities, KPIs, and strategic decisions with AI.",
    ctaButton: "{t.ctaButton}",
    features: [
      "Business health analysis",
      "Risk and opportunity detection",
      "KPI interpretation",
      "Executive AI summaries",
      "Strategic recommendations",
      "Exportable business reports",
    ],
  },

  fr: {
    back: "← Retour au blog",
    category: "IA business",
    title: "Business Intelligence IA : transformer les données en meilleures décisions",
    intro: "La business intelligence ne se limite plus aux dashboards et rapports statiques. Les systèmes IA modernes aident les équipes à comprendre les données business, détecter les risques, identifier les opportunités et générer des insights actionnables plus rapidement.",
    whatIs: "Qu’est-ce que la business intelligence IA ?",
    whatIsText: "La business intelligence IA combine les données business structurées avec l’intelligence artificielle pour aider les organisations à comprendre performance, risques, tendances et opportunités.",
    why: "Pourquoi les dashboards traditionnels ne suffisent pas",
    whyText: "Les dashboards sont utiles, mais ils exigent souvent que les utilisateurs interprètent eux-mêmes les données. L’IA ajoute une couche d’interprétation qui transforme les métriques en contexte business pratique.",
    riskDetection: "Détection des risques",
    riskDetectionText: "L’IA peut détecter les signaux faibles comme la baisse du chiffre d’affaires, la hausse des coûts ou les blocages opérationnels.",
    opportunityDiscovery: "Découverte d’opportunités",
    opportunityDiscoveryText: "L’IA peut identifier les signaux de croissance, segments performants et canaux sous-utilisés.",
    executiveSummaries: "Résumés exécutifs",
    executiveSummariesText: "L’IA peut transformer des données complexes en résumés clairs pour fondateurs, managers et équipes.",
    decisionSupport: "Aide à la décision",
    decisionSupportText: "L’IA peut suggérer des prochaines actions selon la performance, les risques et les objectifs stratégiques.",
    useCases: "Cas d’usage courants de l’IA business intelligence",
    useCasesText: "L’IA business intelligence peut aider à l’analyse commerciale, segmentation client, reporting financier, analyse opérationnelle et planification stratégique.",
    runexa: "Comment Runexa Business Agent aide",
    runexaText: "Runexa Business Agent aide les utilisateurs à téléverser des données business structurées, analyser la performance, détecter les risques et générer des recommandations IA.",
    support: "L’IA doit soutenir les décisions, pas automatiser le jugement",
    supportText: "Les meilleurs systèmes IA business aident les équipes à raisonner plus clairement. Les insights IA doivent être validés avec l’expertise humaine et des données fiables.",
    ctaTitle: "Transformez vos données business en insights actionnables",
    ctaText: "Utilisez Runexa Business Agent pour analyser risques, opportunités, KPI et décisions stratégiques avec l’IA.",
    ctaButton: "Analyser des données business",
    features: [
      "Analyse de santé business",
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
    title: "ذكاء الأعمال بالذكاء الاصطناعي: تحويل البيانات إلى قرارات أفضل",
    intro: "لم تعد ذكاء الأعمال تقتصر على لوحات التحكم والتقارير الثابتة. تساعد أنظمة الذكاء الاصطناعي الحديثة الفرق على فهم بيانات الأعمال واكتشاف المخاطر وتحديد الفرص بشكل أسرع.",
    whatIs: "ما هو ذكاء الأعمال بالذكاء الاصطناعي؟",
    whatIsText: "يجمع ذكاء الأعمال بالذكاء الاصطناعي بين البيانات المنظمة وتقنيات الذكاء الاصطناعي لمساعدة المؤسسات على فهم الأداء والمخاطر والاتجاهات والفرص.",
    why: "لماذا لا تكفي لوحات التحكم التقليدية",
    whyText: "لوحات التحكم مفيدة، لكنها غالبًا تتطلب من المستخدم تفسير البيانات بنفسه. يضيف الذكاء الاصطناعي طبقة تفسير تحول الأرقام إلى سياق عملي.",
    riskDetection: "اكتشاف المخاطر",
    riskDetectionText: "يمكن للذكاء الاصطناعي اكتشاف إشارات ضعيفة مثل انخفاض الإيرادات أو ارتفاع التكاليف أو الاختناقات التشغيلية.",
    opportunityDiscovery: "اكتشاف الفرص",
    opportunityDiscoveryText: "يمكن للذكاء الاصطناعي تحديد إشارات النمو والشرائح عالية الأداء والقنوات غير المستغلة.",
    executiveSummaries: "ملخصات تنفيذية",
    executiveSummariesText: "يمكن للذكاء الاصطناعي تحويل البيانات المعقدة إلى ملخصات واضحة للمديرين والفرق.",
    decisionSupport: "دعم القرار",
    decisionSupportText: "يمكن للذكاء الاصطناعي اقتراح خطوات تالية بناءً على الأداء والمخاطر والأهداف الاستراتيجية.",
    useCases: "حالات استخدام شائعة لذكاء الأعمال",
    useCasesText: "يمكن لذكاء الأعمال بالذكاء الاصطناعي دعم تحليل المبيعات وتقسيم العملاء والتقارير المالية والتحليل التشغيلي والتخطيط الاستراتيجي.",
    runexa: "كيف يساعد Runexa Business Agent",
    runexaText: "يساعد Runexa Business Agent المستخدمين على رفع بيانات أعمال منظمة وتحليل الأداء واكتشاف المخاطر والفرص وإنشاء توصيات مدعومة بالذكاء الاصطناعي.",
    support: "يجب أن يدعم الذكاء الاصطناعي القرارات لا أن يستبدل الحكم البشري",
    supportText: "أفضل أنظمة ذكاء الأعمال تساعد الفرق على التفكير بوضوح أكبر. يجب مراجعة الرؤى الناتجة عن الذكاء الاصطناعي مع الخبرة البشرية والبيانات الموثوقة.",
    ctaTitle: "حوّل بيانات الأعمال إلى رؤى قابلة للتنفيذ",
    ctaText: "استخدم Runexa Business Agent لتحليل المخاطر والفرص ومؤشرات الأداء والقرارات الاستراتيجية بالذكاء الاصطناعي.",
    ctaButton: "تحليل بيانات الأعمال",
    features: [
      "تحليل صحة الأعمال",
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
                "{t.title}",
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