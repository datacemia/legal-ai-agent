"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getSavedLocale } from "../../../lib/i18n";

const translations = {
  en: {
    back: "← Back to Blog",

    category: "Enterprise AI",

    title:
      "Enterprise AI Workflows: How Organizations Build AI-Powered Operations",

    intro:
      "Enterprise AI is moving beyond chatbots and basic automation. Modern organizations are building AI-powered workflows that help teams analyze documents, improve decision-making, reduce repetitive work, and scale operational intelligence across departments.",

    whatIs:
      "What are enterprise AI workflows?",

    whatIsText:
      "Enterprise AI workflows combine artificial intelligence, structured processes, business data, and operational systems to automate analysis and support professional decision-making at scale.",

    why:
      "Why organizations are adopting AI workflows",

    whyText:
      "Teams spend significant time reviewing documents, summarizing reports, extracting information, preparing decisions, and managing repetitive processes. AI workflows can reduce operational friction, improve visibility, and accelerate analysis across departments.",

    operationalEfficiency:
      "Operational efficiency",

    operationalEfficiencyText:
      "AI workflows reduce repetitive manual work and accelerate analysis processes.",

    decisionSupport:
      "Decision support",

    decisionSupportText:
      "AI systems help teams understand risks, opportunities, and business signals faster.",

    documentIntelligence:
      "Document intelligence",

    documentIntelligenceText:
      "Organizations can analyze contracts, reports, statements, and structured files more efficiently.",

    scalableWorkflows:
      "Scalable workflows",

    scalableWorkflowsText:
      "AI allows teams to scale operations without proportionally increasing manual review workloads.",

    examples:
      "Common enterprise AI workflow examples",

    examplesText:
      "Enterprise AI workflows can support legal operations, financial analysis, internal learning systems, customer support, compliance review, procurement workflows, reporting pipelines, and strategic business intelligence.",

    structured:
      "Enterprise AI requires structured systems",

    structuredText:
      "Effective AI workflows are not only about large language models. Organizations also need structured pipelines, document management, secure infrastructure, permission systems, workflow orchestration, and human validation processes.",

    runexa:
      "How Runexa approaches enterprise AI",

    runexaText:
      "Runexa is designed as an enterprise AI workspace with specialized AI agents for legal analysis, financial workflows, learning systems, business intelligence, and operational decision support. The goal is to create practical AI workflows that improve clarity, productivity, and strategic execution.",

    support:
      "AI should augment teams, not replace them",

    supportText:
      "The strongest enterprise AI systems are designed to support human expertise. AI can accelerate analysis and surface insights, but critical decisions still require human judgment, organizational context, and professional oversight.",

    ctaTitle:
      "Build enterprise AI workflows with Runexa",

    ctaText:
      "Explore AI systems for legal analysis, financial workflows, business intelligence, learning operations, and organizational decision support.",

    ctaButton:
      "Explore Enterprise AI",

    features: [
      "AI document analysis",
      "Business intelligence workflows",
      "Financial reporting systems",
      "Learning and knowledge workflows",
      "Decision-support infrastructure",
      "Secure AI workspaces",
    ],

    jsonDescription:
      "Learn how enterprise AI workflows help organizations automate analysis, improve decision-making, and scale operational intelligence.",
  },

  fr: {
  back: "← Retour au blog",

  category: "IA d’entreprise",

  title:
  "Workflows IA d’entreprise : comment les organisations construisent des opérations augmentées par l’IA",

  intro:
  "L’IA d’entreprise dépasse aujourd’hui le cadre des chatbots et de l’automatisation basique. Les organisations modernes mettent en place des workflows alimentés par l’IA afin d’analyser les documents, améliorer la prise de décision, réduire les tâches répétitives et développer l’intelligence opérationnelle à grande échelle.",

  whatIs:
  "Que sont les workflows IA d’entreprise ?",

  whatIsText:
  "Les workflows IA d’entreprise combinent intelligence artificielle, processus structurés, données métier et systèmes opérationnels afin d’automatiser l’analyse et de soutenir la prise de décision professionnelle à grande échelle.",

  why:
  "Pourquoi les organisations adoptent les workflows IA",

  whyText:
  "Les équipes consacrent une part importante de leur temps à examiner des documents, synthétiser des rapports, extraire des informations, préparer des décisions et gérer des processus répétitifs. Les workflows IA permettent de réduire les frictions opérationnelles, d’améliorer la visibilité et d’accélérer l’analyse dans l’ensemble de l’organisation.",

  operationalEfficiency:
  "Efficacité opérationnelle",

  operationalEfficiencyText:
  "Les workflows IA réduisent les tâches manuelles répétitives et accélèrent les processus d’analyse.",

  decisionSupport:
  "Aide à la décision",

  decisionSupportText:
  "Les systèmes IA permettent aux équipes d’identifier plus rapidement les risques, les opportunités et les signaux stratégiques.",

  documentIntelligence:
  "Intelligence documentaire",

  documentIntelligenceText:
  "Les organisations peuvent analyser plus efficacement les contrats, rapports, relevés et documents structurés.",

  scalableWorkflows:
  "Workflows évolutifs",

  scalableWorkflowsText:
  "L’IA permet de développer les opérations sans augmenter proportionnellement la charge de travail liée aux revues manuelles.",

  examples:
  "Exemples courants de workflows IA d’entreprise",

  examplesText:
  "Les workflows IA d’entreprise peuvent soutenir les opérations juridiques, l’analyse financière, les systèmes de formation interne, le support client, les processus de conformité, les achats, le reporting et la business intelligence stratégique.",

  structured:
  "L’IA d’entreprise nécessite des systèmes structurés",

  structuredText:
  "Les workflows IA performants ne reposent pas uniquement sur les grands modèles de langage. Les organisations ont également besoin de pipelines structurés, de systèmes de gestion documentaire, d’infrastructures sécurisées, de mécanismes de permissions, d’orchestration des workflows et de processus de validation humaine.",

  runexa:
  "Comment Runexa aborde l’IA d’entreprise",

  runexaText:
  "Runexa est conçu comme un espace de travail IA d’entreprise intégrant des agents spécialisés pour l’analyse juridique, les workflows financiers, les systèmes d’apprentissage, la business intelligence et l’aide à la décision opérationnelle. L’objectif est de créer des workflows IA concrets qui améliorent la clarté, la productivité et l’exécution stratégique.",

  support:
  "L’IA doit renforcer les équipes, pas les remplacer",

  supportText:
  "Les systèmes IA d’entreprise les plus performants sont conçus pour compléter l’expertise humaine. L’IA peut accélérer l’analyse et faire émerger des insights, mais les décisions critiques nécessitent toujours un jugement humain, une compréhension du contexte organisationnel et une supervision professionnelle.",

  ctaTitle:
  "Construisez vos workflows IA d’entreprise avec Runexa",

  ctaText:
  "Explorez des systèmes IA dédiés à l’analyse juridique, aux workflows financiers, à la business intelligence, aux opérations d’apprentissage et à l’aide à la décision organisationnelle.",

  ctaButton:
  "Explorer l’IA d’entreprise",

  features: [
  "Analyse documentaire par IA",
  "Workflows de business intelligence",
  "Systèmes de reporting financier",
  "Workflows d’apprentissage et de gestion des connaissances",
  "Infrastructure d’aide à la décision",
  "Espaces de travail IA sécurisés",
  ],

  jsonDescription:
  "Découvrez comment les workflows IA d’entreprise aident les organisations à automatiser l’analyse, améliorer la prise de décision et développer leur intelligence opérationnelle.",
  },

  ar: {
  back: "← العودة إلى المدونة",

  category: "الذكاء الاصطناعي للمؤسسات",

  title:
  "تدفقات عمل الذكاء الاصطناعي للمؤسسات: كيف تبني المؤسسات عمليات مدعومة بالذكاء الاصطناعي",

  intro:
  "لم يعد الذكاء الاصطناعي للمؤسسات يقتصر على روبوتات المحادثة أو الأتمتة الأساسية. فالمؤسسات الحديثة تبني تدفقات عمل مدعومة بالذكاء الاصطناعي تساعد الفرق على تحليل المستندات وتحسين اتخاذ القرار وتقليل المهام المتكررة وتطوير الذكاء التشغيلي على نطاق واسع.",

  whatIs:
  "ما هي تدفقات عمل الذكاء الاصطناعي للمؤسسات؟",

  whatIsText:
  "تجمع تدفقات عمل الذكاء الاصطناعي للمؤسسات بين الذكاء الاصطناعي والعمليات المنظمة وبيانات الأعمال والأنظمة التشغيلية بهدف أتمتة التحليل ودعم اتخاذ القرار المهني على نطاق واسع.",

  why:
  "لماذا تعتمد المؤسسات تدفقات العمل المدعومة بالذكاء الاصطناعي؟",

  whyText:
  "تقضي الفرق وقتاً كبيراً في مراجعة المستندات وتلخيص التقارير واستخراج المعلومات وإعداد القرارات وإدارة العمليات المتكررة. تساعد تدفقات العمل المدعومة بالذكاء الاصطناعي على تقليل الاحتكاك التشغيلي وتحسين الرؤية وتسريع التحليل عبر مختلف الأقسام.",

  operationalEfficiency:
  "الكفاءة التشغيلية",

  operationalEfficiencyText:
  "تساعد تدفقات العمل الذكية على تقليل الأعمال اليدوية المتكررة وتسريع عمليات التحليل.",

  decisionSupport:
  "دعم اتخاذ القرار",

  decisionSupportText:
  "تمكّن أنظمة الذكاء الاصطناعي الفرق من فهم المخاطر والفرص والمؤشرات التجارية بشكل أسرع.",

  documentIntelligence:
  "ذكاء المستندات",

  documentIntelligenceText:
  "يمكن للمؤسسات تحليل العقود والتقارير والكشوف والملفات المنظمة بكفاءة أعلى.",

  scalableWorkflows:
  "تدفقات عمل قابلة للتوسع",

  scalableWorkflowsText:
  "يتيح الذكاء الاصطناعي للمؤسسات توسيع عملياتها دون زيادة متناسبة في أعباء المراجعة اليدوية.",

  examples:
  "أمثلة شائعة على تدفقات عمل الذكاء الاصطناعي للمؤسسات",

  examplesText:
  "يمكن لتدفقات العمل المدعومة بالذكاء الاصطناعي دعم العمليات القانونية والتحليل المالي وأنظمة التعلم الداخلية ودعم العملاء وعمليات الامتثال والمشتريات وخطوط إعداد التقارير وذكاء الأعمال الاستراتيجي.",

  structured:
  "يتطلب الذكاء الاصطناعي للمؤسسات أنظمة منظمة",

  structuredText:
  "لا تعتمد تدفقات العمل الفعالة على نماذج اللغة الكبيرة فقط. بل تحتاج المؤسسات أيضاً إلى مسارات عمل منظمة وأنظمة لإدارة المستندات وبنية تحتية آمنة وآليات للتحكم في الصلاحيات وأدوات لتنسيق سير العمل وعمليات تحقق بشرية.",

  runexa:
  "كيف تتعامل Runexa مع الذكاء الاصطناعي للمؤسسات",

  runexaText:
  "تم تصميم Runexa كمساحة عمل للذكاء الاصطناعي المؤسسي تضم وكلاء متخصصين للتحليل القانوني والعمليات المالية وأنظمة التعلم وذكاء الأعمال ودعم القرارات التشغيلية. ويتمثل الهدف في إنشاء تدفقات عمل عملية تعزز الوضوح والإنتاجية والتنفيذ الاستراتيجي.",

  support:
  "يجب أن يعزز الذكاء الاصطناعي قدرات الفرق لا أن يستبدلها",

  supportText:
  "تم تصميم أقوى أنظمة الذكاء الاصطناعي للمؤسسات لدعم الخبرة البشرية وتعزيزها. يمكن للذكاء الاصطناعي تسريع التحليل وإبراز الرؤى المهمة، لكن القرارات الجوهرية لا تزال تتطلب حكماً بشرياً وفهماً للسياق المؤسسي وإشرافاً مهنياً.",

  ctaTitle:
  "ابنِ تدفقات عمل مؤسسية مدعومة بالذكاء الاصطناعي مع Runexa",

  ctaText:
  "استكشف أنظمة الذكاء الاصطناعي المخصصة للتحليل القانوني والعمليات المالية وذكاء الأعمال وعمليات التعلم ودعم اتخاذ القرار المؤسسي.",

  ctaButton:
  "استكشاف الذكاء الاصطناعي للمؤسسات",

  features: [
  "تحليل المستندات بالذكاء الاصطناعي",
  "تدفقات عمل ذكاء الأعمال",
  "أنظمة التقارير المالية",
  "تدفقات التعلم وإدارة المعرفة",
  "بنية تحتية لدعم اتخاذ القرار",
  "مساحات عمل آمنة للذكاء الاصطناعي",
  ],

  jsonDescription:
  "تعرّف على كيفية مساعدة تدفقات عمل الذكاء الاصطناعي للمؤسسات في أتمتة التحليل وتحسين اتخاذ القرار وتطوير الذكاء التشغيلي على نطاق واسع.",
  },

};

export default function EnterpriseAIWorkflowsArticle() {
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
              [t.operationalEfficiency, t.operationalEfficiencyText],
              [t.decisionSupport, t.decisionSupportText],
              [t.documentIntelligence, t.documentIntelligenceText],
              [t.scalableWorkflows, t.scalableWorkflowsText],
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
              {t.examples}
            </h2>

            <p className="mt-4 leading-8 text-slate-600">
              {t.examplesText}
            </p>
          </div>

          <div className="rounded-3xl border bg-white p-8 shadow-sm">
            <h2 className="text-2xl font-bold">
              {t.structured}
            </h2>

            <p className="mt-4 leading-8 text-slate-600">
              {t.structuredText}
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
              {t.runexa}
            </h2>

            <p className="mt-4 leading-8 text-slate-600">
              {t.runexaText}
            </p>
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
            href="/enterprise-ai"
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
              mainEntityOfPage: {
                "@type": "WebPage",
                "@id":
                  "https://runexa.ai/blog/enterprise-ai-workflows",
              },
              headline: t.title,
              description:
                t.jsonDescription,
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
