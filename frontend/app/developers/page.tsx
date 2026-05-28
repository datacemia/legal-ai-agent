"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getSavedLocale } from "../../lib/i18n";

const translations = {
  en: {
    badge: "Runexa Developers",
    title: "Build AI workflows with specialized Runexa agents",
    subtitle:
      "Runexa is evolving into an AI workspace and API platform for legal analysis, finance intelligence, study automation, and business decision support.",
    exploreApi: "Explore API",
    viewDocs: "View Docs",
    legalAi: "Legal AI",
    legalDesc:
      "Analyze contracts, risky clauses, obligations, and recommendations.",
    financeAi: "Finance AI",
    financeDesc:
      "Analyze statements, subscriptions, spending, and savings opportunities.",
    studyAi: "Study AI",
    studyDesc:
      "Generate summaries, quizzes, flashcards, and study plans.",
    businessAi: "Business AI",
    businessDesc:
      "Analyze KPIs, risks, opportunities, and strategic decisions.",
    workflow: "Developer workflow",
    workflowTitle: "Async AI jobs designed for real workloads",
    step1: "Send a file or structured data to a Runexa agent endpoint.",
    step2: "Receive a job ID while Runexa processes the AI workflow.",
    step3: "Poll the job status and retrieve structured analysis results.",
    authentication: "Authentication",
    authText:
      "Runexa API requests use bearer token authentication. Include your API key in the Authorization header for every request.",
    exampleFlow: "Example API flow",
    ctaTitle: "Start with Runexa AI agents",
    ctaText:
      "Explore Runexa APIs, review endpoint examples, and prepare AI workflows for legal, finance, study, and business use cases.",
    readDocs: "Read Developer Docs",
  },
  fr: {
    badge: "Développeurs Runexa",
    title: "Construisez des workflows IA avec les agents spécialisés Runexa",
    subtitle:
      "Runexa évolue vers un espace de travail IA et une plateforme API pour l’analyse juridique, l’intelligence financière, l’automatisation de l’apprentissage et l’aide à la décision business.",
    exploreApi: "Explorer l’API",
    viewDocs: "Voir la documentation",
    legalAi: "IA juridique",
    legalDesc:
      "Analysez les contrats, clauses à risque, obligations et recommandations.",
    financeAi: "IA finance",
    financeDesc:
      "Analysez les relevés, abonnements, dépenses et opportunités d’économies.",
    studyAi: "IA étude",
    studyDesc:
      "Générez des résumés, quiz, flashcards et plans de révision.",
    businessAi: "IA business",
    businessDesc:
      "Analysez les KPI, risques, opportunités et décisions stratégiques.",
    workflow: "Workflow développeur",
    workflowTitle: "Jobs IA asynchrones conçus pour des usages réels",
    step1: "Envoyez un fichier ou des données structurées vers un endpoint agent Runexa.",
    step2: "Recevez un ID de job pendant que Runexa traite le workflow IA.",
    step3: "Consultez le statut du job et récupérez des résultats structurés.",
    authentication: "Authentification",
    authText:
      "Les requêtes API Runexa utilisent une authentification par token Bearer. Incluez votre clé API dans l’en-tête Authorization pour chaque requête.",
    exampleFlow: "Exemple de flow API",
    ctaTitle: "Commencez avec les agents IA Runexa",
    ctaText:
      "Explorez les API Runexa, consultez les exemples d’endpoints et préparez des workflows IA pour les usages juridiques, finance, étude et business.",
    readDocs: "Lire la documentation développeur",
  },
  ar: {
    badge: "مطورو Runexa",
    title: "أنشئ تدفقات عمل ذكاء اصطناعي باستخدام وكلاء Runexa المتخصصين",
    subtitle:
      "تتطور Runexa إلى مساحة عمل ومنصة API للذكاء الاصطناعي للتحليل القانوني والذكاء المالي وأتمتة الدراسة ودعم قرارات الأعمال.",
    exploreApi: "استكشاف API",
    viewDocs: "عرض التوثيق",
    legalAi: "الذكاء القانوني",
    legalDesc:
      "حلّل العقود والبنود الخطرة والالتزامات والتوصيات.",
    financeAi: "الذكاء المالي",
    financeDesc:
      "حلّل الكشوف والاشتراكات والمصاريف وفرص الادخار.",
    studyAi: "ذكاء الدراسة",
    studyDesc:
      "أنشئ ملخصات واختبارات وبطاقات تعليمية وخطط دراسة.",
    businessAi: "ذكاء الأعمال",
    businessDesc:
      "حلّل مؤشرات الأداء والمخاطر والفرص والقرارات الاستراتيجية.",
    workflow: "سير عمل المطور",
    workflowTitle: "مهام ذكاء اصطناعي غير متزامنة مصممة للاستخدامات الواقعية",
    step1: "أرسل ملفًا أو بيانات منظمة إلى endpoint خاص بوكيل Runexa.",
    step2: "استلم معرف المهمة بينما تعالج Runexa سير عمل الذكاء الاصطناعي.",
    step3: "تابع حالة المهمة واسترجع نتائج تحليل منظمة.",
    authentication: "المصادقة",
    authText:
      "تستخدم طلبات API في Runexa مصادقة Bearer token. أضف مفتاح API داخل ترويسة Authorization في كل طلب.",
    exampleFlow: "مثال على تدفق API",
    ctaTitle: "ابدأ مع وكلاء Runexa للذكاء الاصطناعي",
    ctaText:
      "استكشف واجهات Runexa، وراجع أمثلة الـ endpoints، وجهّز تدفقات عمل للمهام القانونية والمالية والدراسة والأعمال.",
    readDocs: "قراءة توثيق المطورين",
  },
};

export default function DevelopersPage() {
  const [locale, setLocale] = useState<"en" | "fr" | "ar">("en");

  useEffect(() => {
    const savedLocale = getSavedLocale();

    if (savedLocale === "fr" || savedLocale === "ar") {
      setLocale(savedLocale);
    } else {
      setLocale("en");
    }
  }, []);

  const t = translations[locale];

  return (
    <main
      dir={locale === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-6 py-20 text-slate-900"
    >
      <section className="mx-auto max-w-6xl text-center">
        <p className="font-semibold text-blue-600">{t.badge}</p>

        <h1 className="mt-4 text-5xl font-bold tracking-tight">
          {t.title}
        </h1>

        <p className="mx-auto mt-6 max-w-3xl text-lg leading-8 text-slate-600">
          {t.subtitle}
        </p>

        <div className="mt-8 flex flex-wrap justify-center gap-3">
          <Link
            href="/api"
            className="rounded-xl bg-blue-600 px-6 py-3 text-sm font-semibold text-white hover:bg-blue-700"
          >
            {t.exploreApi}
          </Link>

          <Link
            href="/docs"
            className="rounded-xl border border-slate-200 bg-white px-6 py-3 text-sm font-semibold text-slate-900 hover:bg-slate-50"
          >
            {t.viewDocs}
          </Link>
        </div>
      </section>

      <section className="mx-auto mt-16 grid max-w-6xl gap-6 md:grid-cols-4">
        {[
          [t.legalAi, t.legalDesc],
          [t.financeAi, t.financeDesc],
          [t.studyAi, t.studyDesc],
          [t.businessAi, t.businessDesc],
        ].map(([title, desc]) => (
          <div
            key={title}
            className="rounded-2xl border bg-white p-6 shadow-sm"
          >
            <h2 className="font-bold">{title}</h2>
            <p className="mt-3 text-sm leading-6 text-slate-600">
              {desc}
            </p>
          </div>
        ))}
      </section>

      <section className="mx-auto mt-16 max-w-6xl rounded-3xl border bg-slate-950 p-8 text-white shadow-sm md:p-12">
        <p className="text-sm font-semibold text-blue-300">
          {t.workflow}
        </p>

        <h2 className="mt-3 text-3xl font-bold">
          {t.workflowTitle}
        </h2>

        <div className="mt-8 grid gap-4 md:grid-cols-3">
          {[
            ["1", t.step1],
            ["2", t.step2],
            ["3", t.step3],
          ].map(([num, text]) => (
            <div
              key={num}
              className="rounded-2xl border border-white/10 bg-white/5 p-5"
            >
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-600 text-sm font-bold">
                {num}
              </div>
              <p className="mt-4 text-sm leading-6 text-slate-200">
                {text}
              </p>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto mt-16 max-w-6xl rounded-3xl border bg-white p-8 shadow-sm md:p-12">
        <h2 className="text-3xl font-bold">{t.authentication}</h2>

        <p className="mt-4 max-w-3xl leading-8 text-slate-600">
          {t.authText}
        </p>

        <pre className="mt-6 overflow-x-auto rounded-2xl bg-slate-950 p-5 text-sm text-slate-100">
{`Authorization: Bearer rk_live_xxx`}
        </pre>
      </section>

      <section className="mx-auto mt-16 max-w-6xl rounded-3xl border bg-white p-8 shadow-sm md:p-12">
        <h2 className="text-3xl font-bold">{t.exampleFlow}</h2>

        <pre className="mt-6 overflow-x-auto rounded-2xl bg-slate-950 p-5 text-sm text-slate-100">
{`POST /v1/legal/analyze
Authorization: Bearer RUNEXA_API_KEY

Response:
{
  "job_id": 123,
  "status": "pending"
}

GET /v1/jobs/123

Response:
{
  "status": "completed",
  "result": {
    "risk_score": 82,
    "summary": "...",
    "recommendations": []
  }
}`}
        </pre>
      </section>

      <section className="mx-auto mt-16 max-w-6xl rounded-3xl bg-blue-600 p-8 text-center text-white md:p-12">
        <h2 className="text-3xl font-bold">{t.ctaTitle}</h2>
        <p className="mx-auto mt-4 max-w-2xl text-blue-100">
          {t.ctaText}
        </p>

        <Link
          href="/docs"
          className="mt-6 inline-block rounded-xl bg-white px-6 py-3 text-sm font-semibold text-blue-600"
        >
          {t.readDocs}
        </Link>
      </section>
    </main>
  );
}