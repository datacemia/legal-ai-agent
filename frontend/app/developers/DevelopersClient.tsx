"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getSavedLocale } from "../../lib/i18n";

const translations = {
  en: {
    badge: "Runexa Developers",

    title:
        "Build AI-powered workflows with Runexa",

    subtitle:
        "Integrate specialized AI capabilities for legal analysis, financial intelligence, learning automation, and business decision support into your applications and workflows.",

    exploreApi:
        "Explore API",

    viewDocs:
        "View Documentation",

    legalAi:
        "Legal Intelligence",

    legalDesc:
        "Analyze contracts, obligations, risks, and legal documents through structured AI workflows.",

    financeAi:
        "Financial Intelligence",

    financeDesc:
        "Process financial statements, spending activity, subscriptions, and savings opportunities.",

    studyAi:
        "Learning Intelligence",

    studyDesc:
        "Generate summaries, quizzes, flashcards, and personalized learning workflows.",

    businessAi:
        "Business Intelligence",

    businessDesc:
        "Analyze performance metrics, risks, opportunities, and strategic decisions.",

    workflow:
        "Developer Workflow",

    workflowTitle:
        "Asynchronous AI processing built for production",

    step1:
        "Send a document or structured data to a Runexa API endpoint.",

    step2:
        "Receive a job identifier while Runexa processes the workflow.",

    step3:
        "Retrieve structured results, insights, and recommendations when processing is complete.",

    authentication:
        "Authentication",

    authText:
        "Runexa APIs use bearer token authentication. Include your API key in the Authorization header for every request.",

    exampleFlow:
        "Example API Workflow",

    ctaTitle:
        "Start building with Runexa",

    ctaText:
        "Explore APIs, review integration examples, and build AI-powered workflows for legal, finance, learning, and business use cases.",

    readDocs:
        "Read Documentation",
    },
  fr: {
    badge: "Développeurs Runexa",

    title:
        "Créez des workflows IA avec Runexa",

    subtitle:
        "Intégrez des capacités d’IA spécialisées pour l’analyse juridique, l’intelligence financière, l’automatisation de l’apprentissage et l’aide à la décision business dans vos applications et workflows.",

    exploreApi:
        "Explorer l’API",

    viewDocs:
        "Voir la documentation",

    legalAi:
        "Intelligence juridique",

    legalDesc:
        "Analysez les contrats, obligations, risques et documents juridiques grâce à des workflows IA structurés.",

    financeAi:
        "Intelligence financière",

    financeDesc:
        "Traitez les relevés financiers, les dépenses, les abonnements et les opportunités d’optimisation.",

    studyAi:
        "Intelligence pédagogique",

    studyDesc:
        "Générez des résumés, quiz, flashcards et parcours d’apprentissage personnalisés.",

    businessAi:
        "Intelligence business",

    businessDesc:
        "Analysez les indicateurs de performance, les risques, les opportunités et les décisions stratégiques.",

    workflow:
        "Workflow développeur",

    workflowTitle:
        "Traitement IA asynchrone conçu pour la production",

    step1:
        "Envoyez un document ou des données structurées vers une API Runexa.",

    step2:
        "Recevez un identifiant de traitement pendant que Runexa exécute le workflow.",

    step3:
        "Récupérez des résultats structurés, des insights et des recommandations une fois le traitement terminé.",

    authentication:
        "Authentification",

    authText:
        "Les API Runexa utilisent une authentification par jeton Bearer. Incluez votre clé API dans l’en-tête Authorization pour chaque requête.",

    exampleFlow:
        "Exemple de workflow API",

    ctaTitle:
        "Commencez à développer avec Runexa",

    ctaText:
        "Explorez les API, consultez les exemples d’intégration et créez des workflows alimentés par l’IA pour les usages juridiques, financiers, pédagogiques et business.",

    readDocs:
        "Lire la documentation",
    },
  ar: {
    badge:
        "مطورو Runexa",

    title:
        "أنشئ تدفقات عمل مدعومة بالذكاء الاصطناعي مع Runexa",

    subtitle:
        "دمج قدرات ذكاء اصطناعي متخصصة للتحليل القانوني والذكاء المالي وأتمتة التعلّم ودعم قرارات الأعمال داخل تطبيقاتك وتدفقات العمل الخاصة بك.",

    exploreApi:
        "استكشاف API",

    viewDocs:
        "عرض التوثيق",

    legalAi:
        "الذكاء القانوني",

    legalDesc:
        "حلّل العقود والالتزامات والمخاطر والمستندات القانونية من خلال تدفقات عمل ذكاء اصطناعي منظمة.",

    financeAi:
        "الذكاء المالي",

    financeDesc:
        "عالج الكشوف المالية والمصروفات والاشتراكات وفرص تحسين الإنفاق.",

    studyAi:
        "ذكاء التعلّم",

    studyDesc:
        "أنشئ ملخصات واختبارات وبطاقات تعليمية ومسارات تعلّم مخصصة.",

    businessAi:
        "ذكاء الأعمال",

    businessDesc:
        "حلّل مؤشرات الأداء والمخاطر والفرص والقرارات الاستراتيجية.",

    workflow:
        "سير عمل المطور",

    workflowTitle:
        "معالجة غير متزامنة للذكاء الاصطناعي مصممة لبيئات الإنتاج",

    step1:
        "أرسل مستنداً أو بيانات منظمة إلى إحدى واجهات Runexa.",

    step2:
        "استلم معرف معالجة بينما يقوم Runexa بتنفيذ سير العمل.",

    step3:
        "استرجع النتائج المنظمة والرؤى والتوصيات بعد اكتمال المعالجة.",

    authentication:
        "المصادقة",

    authText:
        "تستخدم واجهات Runexa مصادقة Bearer Token. أضف مفتاح API الخاص بك داخل ترويسة Authorization في كل طلب.",

    exampleFlow:
        "مثال على سير عمل API",

    ctaTitle:
        "ابدأ البناء مع Runexa",

    ctaText:
        "استكشف واجهات API، وراجع أمثلة التكامل، وأنشئ تدفقات عمل مدعومة بالذكاء الاصطناعي للاستخدامات القانونية والمالية والتعليمية والتجارية.",

    readDocs:
        "قراءة التوثيق",
    },
};

type Locale = "en" | "fr" | "ar";

export default function DevelopersClient({
  initialLocale = "en",
  lockInitialLocale = false,
}: {
  initialLocale?: Locale;
  lockInitialLocale?: boolean;
}) {
  const [locale, setLocale] = useState<Locale>(initialLocale);

  useEffect(() => {
    if (lockInitialLocale) {
      setLocale(initialLocale);
      return;
    }

    const savedLocale = getSavedLocale();

    if (savedLocale === "fr" || savedLocale === "ar" || savedLocale === "en") {
      setLocale(savedLocale);
    } else {
      setLocale(initialLocale);
    }
  }, [initialLocale, lockInitialLocale]);

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