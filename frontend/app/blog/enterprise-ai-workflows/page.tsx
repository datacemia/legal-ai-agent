"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getSavedLocale } from "../../../lib/i18n";

const translations = {
  en: {
    back: "← Back to Blog",
    category: "Enterprise AI",
    title: "Enterprise AI Workflows: How Organizations Use AI Systems",
    intro:
      "Enterprise AI is evolving beyond chatbots and simple automation. Modern organizations are building AI workflows that help teams analyze documents, improve decision-making, reduce repetitive work, and scale operational intelligence across departments.",
    whatIs: "What are enterprise AI workflows?",
    whatIsText:
      "Enterprise AI workflows combine artificial intelligence, structured processes, business data, and operational systems to automate analysis and support professional decision-making at scale.",
    why: "Why organizations are adopting AI workflows",
    whyText:
      "Teams spend significant time reviewing documents, summarizing reports, extracting information, preparing decisions, and managing repetitive workflows. AI systems can reduce operational friction, improve visibility, and accelerate analysis across departments.",
    operationalEfficiency: "Operational efficiency",
    operationalEfficiencyText:
      "AI workflows reduce repetitive manual work and accelerate analysis processes.",
    decisionSupport: "Decision support",
    decisionSupportText:
      "AI systems help teams understand risks, opportunities, and business signals faster.",
    documentIntelligence: "Document intelligence",
    documentIntelligenceText:
      "Organizations can analyze contracts, reports, statements, and structured files more efficiently.",
    scalableWorkflows: "Scalable workflows",
    scalableWorkflowsText:
      "AI allows teams to scale operations without proportionally increasing manual review workloads.",
    examples: "Common enterprise AI workflow examples",
    examplesText:
      "Enterprise AI workflows can support legal operations, financial analysis, internal learning systems, customer support, compliance review, procurement workflows, reporting pipelines, and strategic business intelligence.",
    structured: "Enterprise AI requires structured systems",
    structuredText:
      "Effective AI workflows are not only about large language models. Organizations also need structured pipelines, document management, secure infrastructure, permission systems, workflow orchestration, and human validation processes.",
    runexa: "How Runexa approaches enterprise AI",
    runexaText:
      "Runexa is designed as an enterprise AI workspace with specialized AI agents for legal analysis, finance workflows, study systems, business intelligence, and operational decision support. The goal is to create practical AI workflows that improve clarity, productivity, and strategic execution.",
    support: "AI should augment teams, not replace them",
    supportText:
      "The strongest enterprise AI systems are designed to support human expertise. AI can accelerate analysis and surface insights, but critical decisions still require human judgment, organizational context, and professional oversight.",
    ctaTitle: "Build enterprise AI workflows with Runexa",
    ctaText:
      "Explore AI systems for legal analysis, finance workflows, business intelligence, learning operations, and organizational decision support.",
    ctaButton: "Explore Enterprise AI",
    features: [
      "AI document analysis",
      "Business intelligence workflows",
      "Financial reporting systems",
      "Learning & knowledge workflows",
      "Decision-support infrastructure",
      "Secure AI workspaces",
    ],
    jsonDescription:
      "Learn how enterprise AI workflows help organizations automate analysis, improve decision-making, and scale operational intelligence.",
  },

  fr: {
    back: "← Retour au blog",
    category: "IA entreprise",
    title:
      "Workflows IA entreprise : comment les organisations utilisent les systèmes IA",
    intro:
      "L’IA entreprise va au-delà des chatbots et de l’automatisation simple. Les organisations modernes construisent des workflows IA pour analyser les documents, améliorer la prise de décision, réduire les tâches répétitives et développer l’intelligence opérationnelle.",
    whatIs: "Que sont les workflows IA entreprise ?",
    whatIsText:
      "Les workflows IA entreprise combinent intelligence artificielle, processus structurés, données business et systèmes opérationnels pour automatiser l’analyse et soutenir la prise de décision professionnelle à grande échelle.",
    why: "Pourquoi les organisations adoptent les workflows IA",
    whyText:
      "Les équipes passent beaucoup de temps à examiner des documents, résumer des rapports, extraire des informations et préparer des décisions. Les systèmes IA réduisent les frictions opérationnelles et accélèrent l’analyse.",
    operationalEfficiency: "Efficacité opérationnelle",
    operationalEfficiencyText:
      "Les workflows IA réduisent le travail manuel répétitif et accélèrent les processus d’analyse.",
    decisionSupport: "Aide à la décision",
    decisionSupportText:
      "Les systèmes IA aident les équipes à comprendre plus vite les risques, opportunités et signaux business.",
    documentIntelligence: "Intelligence documentaire",
    documentIntelligenceText:
      "Les organisations peuvent analyser plus efficacement contrats, rapports, relevés et fichiers structurés.",
    scalableWorkflows: "Workflows évolutifs",
    scalableWorkflowsText:
      "L’IA permet aux équipes de faire évoluer leurs opérations sans augmenter proportionnellement la charge de revue manuelle.",
    examples: "Exemples courants de workflows IA entreprise",
    examplesText:
      "Les workflows IA entreprise peuvent soutenir les opérations juridiques, l’analyse financière, les systèmes d’apprentissage interne, le support client, la conformité, les achats, le reporting et la business intelligence stratégique.",
    structured: "L’IA entreprise nécessite des systèmes structurés",
    structuredText:
      "Les workflows IA efficaces ne reposent pas seulement sur les grands modèles de langage. Les organisations ont aussi besoin de pipelines structurés, gestion documentaire, infrastructure sécurisée, permissions, orchestration et validation humaine.",
    runexa: "Comment Runexa approche l’IA entreprise",
    runexaText:
      "Runexa est conçu comme un espace de travail IA entreprise avec des agents spécialisés pour l’analyse juridique, la finance, l’étude, la business intelligence et l’aide à la décision opérationnelle.",
    support: "L’IA doit augmenter les équipes, pas les remplacer",
    supportText:
      "Les meilleurs systèmes IA entreprise soutiennent l’expertise humaine. L’IA peut accélérer l’analyse, mais les décisions critiques nécessitent toujours jugement humain, contexte organisationnel et supervision professionnelle.",
    ctaTitle: "Construisez des workflows IA entreprise avec Runexa",
    ctaText:
      "Explorez des systèmes IA pour l’analyse juridique, les workflows finance, la business intelligence, l’apprentissage et l’aide à la décision organisationnelle.",
    ctaButton: "Explorer l’IA entreprise",
    features: [
      "Analyse documentaire IA",
      "Workflows business intelligence",
      "Systèmes de reporting financier",
      "Workflows apprentissage et connaissance",
      "Infrastructure d’aide à la décision",
      "Espaces IA sécurisés",
    ],
    jsonDescription:
      "Découvrez comment les workflows IA entreprise aident les organisations à automatiser l’analyse, améliorer la prise de décision et développer l’intelligence opérationnelle.",
  },

  ar: {
    back: "← العودة إلى المدونة",
    category: "ذكاء المؤسسات",
    title:
      "تدفقات عمل الذكاء الاصطناعي للمؤسسات: كيف تستخدم المؤسسات أنظمة الذكاء الاصطناعي",
    intro:
      "يتطور الذكاء الاصطناعي للمؤسسات إلى ما هو أبعد من روبوتات المحادثة والأتمتة البسيطة. تبني المؤسسات الحديثة تدفقات عمل ذكية تساعد الفرق على تحليل المستندات وتحسين اتخاذ القرار وتقليل العمل المتكرر.",
    whatIs: "ما هي تدفقات عمل الذكاء الاصطناعي للمؤسسات؟",
    whatIsText:
      "تجمع تدفقات عمل الذكاء الاصطناعي للمؤسسات بين الذكاء الاصطناعي والعمليات المنظمة وبيانات الأعمال والأنظمة التشغيلية لأتمتة التحليل ودعم اتخاذ القرار على نطاق واسع.",
    why: "لماذا تعتمد المؤسسات تدفقات العمل الذكية",
    whyText:
      "تقضي الفرق وقتًا كبيرًا في مراجعة المستندات وتلخيص التقارير واستخراج المعلومات وتحضير القرارات. يمكن لأنظمة الذكاء الاصطناعي تقليل الاحتكاك التشغيلي وتسريع التحليل.",
    operationalEfficiency: "الكفاءة التشغيلية",
    operationalEfficiencyText:
      "تقلل تدفقات العمل الذكية العمل اليدوي المتكرر وتسرّع عمليات التحليل.",
    decisionSupport: "دعم القرار",
    decisionSupportText:
      "تساعد أنظمة الذكاء الاصطناعي الفرق على فهم المخاطر والفرص وإشارات الأعمال بشكل أسرع.",
    documentIntelligence: "ذكاء المستندات",
    documentIntelligenceText:
      "يمكن للمؤسسات تحليل العقود والتقارير والكشوف والملفات المنظمة بكفاءة أكبر.",
    scalableWorkflows: "تدفقات عمل قابلة للتوسع",
    scalableWorkflowsText:
      "يسمح الذكاء الاصطناعي للفرق بتوسيع العمليات دون زيادة متناسبة في المراجعة اليدوية.",
    examples: "أمثلة شائعة لتدفقات عمل الذكاء الاصطناعي للمؤسسات",
    examplesText:
      "يمكن لتدفقات العمل الذكية دعم العمليات القانونية والتحليل المالي وأنظمة التعلم الداخلي ودعم العملاء والامتثال والمشتريات والتقارير وذكاء الأعمال الاستراتيجي.",
    structured: "يتطلب الذكاء الاصطناعي للمؤسسات أنظمة منظمة",
    structuredText:
      "لا تعتمد تدفقات العمل الفعالة فقط على نماذج اللغة الكبيرة. تحتاج المؤسسات أيضًا إلى خطوط عمل منظمة وإدارة مستندات وبنية آمنة وأنظمة صلاحيات وتحقق بشري.",
    runexa: "كيف تتعامل Runexa مع الذكاء الاصطناعي للمؤسسات",
    runexaText:
      "تم تصميم Runexa كمساحة عمل ذكاء اصطناعي للمؤسسات مع وكلاء متخصصين للتحليل القانوني والمالية والدراسة وذكاء الأعمال ودعم القرارات التشغيلية.",
    support: "يجب أن يعزز الذكاء الاصطناعي الفرق لا أن يستبدلها",
    supportText:
      "أقوى أنظمة الذكاء الاصطناعي للمؤسسات تدعم الخبرة البشرية. يمكن للذكاء الاصطناعي تسريع التحليل، لكن القرارات المهمة لا تزال تحتاج إلى حكم بشري وسياق مؤسسي وإشراف مهني.",
    ctaTitle: "ابنِ تدفقات عمل ذكاء اصطناعي للمؤسسات مع Runexa",
    ctaText:
      "استكشف أنظمة ذكاء اصطناعي للتحليل القانوني والمالية وذكاء الأعمال والتعلم ودعم القرار المؤسسي.",
    ctaButton: "استكشاف ذكاء المؤسسات",
    features: [
      "تحليل المستندات بالذكاء الاصطناعي",
      "تدفقات ذكاء الأعمال",
      "أنظمة التقارير المالية",
      "تدفقات التعلم والمعرفة",
      "بنية دعم القرار",
      "مساحات ذكاء اصطناعي آمنة",
    ],
    jsonDescription:
      "تعرّف على كيف تساعد تدفقات عمل الذكاء الاصطناعي للمؤسسات على أتمتة التحليل وتحسين اتخاذ القرار وتوسيع الذكاء التشغيلي.",
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
