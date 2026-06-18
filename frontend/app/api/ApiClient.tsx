"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getSavedLocale } from "../../lib/i18n";

const translations = {
  en: {
    badge: "Runexa API",

    title:
        "AI APIs for production workflows",

    subtitle:
        "Integrate legal intelligence, financial analysis, learning automation, and business decision support into your applications, dashboards, and internal tools.",

    viewDocs:
        "View Documentation",

    developers:
        "Developers",

    legalApi:
        "Legal Intelligence API",

    legalDesc:
        "Submit legal documents and receive structured risk analysis, clause extraction, obligations, and recommendations.",

    financeApi:
        "Financial Analysis API",

    financeDesc:
        "Process financial statements and receive spending insights, subscriptions, savings opportunities, and financial health indicators.",

    studyApi:
        "Learning Intelligence API",

    studyDesc:
        "Generate summaries, quizzes, flashcards, and personalized learning workflows from educational content.",

    businessApi:
        "Business Intelligence API",

    businessDesc:
        "Analyze business data and receive performance metrics, risk assessments, opportunities, and executive recommendations.",

    architecture:
        "API Architecture",

    asyncTitle:
        "Built for asynchronous processing",

    asyncDesc:
        "Analysis workloads may require additional processing time depending on document size and workflow complexity. Runexa APIs use a job-based architecture: submit a request, receive a job identifier, track progress, and retrieve structured results when processing is complete.",

    uploadFile:
        "Upload Document",

    createJob:
        "Create Job",

    pollStatus:
        "Check Status",

    receiveJson:
        "Retrieve Results",

    exampleResponse:
        "Example Response",

    ctaTitle:
        "Build with Runexa",

    ctaDesc:
        "Use Runexa APIs to power document intelligence, financial analysis, learning automation, and business decision support within your products and workflows.",

    readDocs:
        "Read Documentation",
    },
  fr: {
    badge:
        "API Runexa",

    title:
        "API d’IA pour les workflows en production",

    subtitle:
        "Intégrez l’intelligence juridique, l’analyse financière, l’automatisation de l’apprentissage et l’aide à la décision business dans vos applications, tableaux de bord et outils internes.",

    viewDocs:
        "Voir la documentation",

    developers:
        "Développeurs",

    legalApi:
        "API d’intelligence juridique",

    legalDesc:
        "Envoyez des documents juridiques et recevez des analyses de risques structurées, l’extraction de clauses, les obligations et des recommandations.",

    financeApi:
        "API d’analyse financière",

    financeDesc:
        "Traitez des relevés financiers et obtenez des insights sur les dépenses, les abonnements, les opportunités d’économies et les indicateurs de santé financière.",

    studyApi:
        "API d’intelligence pédagogique",

    studyDesc:
        "Générez des résumés, quiz, flashcards et parcours d’apprentissage personnalisés à partir de contenus éducatifs.",

    businessApi:
        "API d’intelligence business",

    businessDesc:
        "Analysez des données business et obtenez des indicateurs de performance, des évaluations de risques, des opportunités et des recommandations stratégiques.",

    architecture:
        "Architecture API",

    asyncTitle:
        "Conçue pour le traitement asynchrone",

    asyncDesc:
        "Les analyses peuvent nécessiter un temps de traitement supplémentaire selon la taille des documents et la complexité des workflows. Les API Runexa utilisent une architecture basée sur des traitements : envoyez une requête, recevez un identifiant, suivez la progression et récupérez les résultats structurés une fois le traitement terminé.",

    uploadFile:
        "Téléverser un document",

    createJob:
        "Créer un traitement",

    pollStatus:
        "Vérifier l’état",

    receiveJson:
        "Récupérer les résultats",

    exampleResponse:
        "Exemple de réponse",

    ctaTitle:
        "Développez avec Runexa",

    ctaDesc:
        "Utilisez les API Runexa pour alimenter l’intelligence documentaire, l’analyse financière, l’automatisation de l’apprentissage et l’aide à la décision business au sein de vos produits et workflows.",

    readDocs:
        "Lire la documentation",
    },
  ar: {
    badge:
        "واجهة Runexa API",

    title:
        "واجهات ذكاء اصطناعي لتدفقات العمل في بيئات الإنتاج",

    subtitle:
        "دمج الذكاء القانوني والتحليل المالي وأتمتة التعلّم ودعم قرارات الأعمال داخل تطبيقاتك ولوحات التحكم والأدوات الداخلية.",

    viewDocs:
        "عرض التوثيق",

    developers:
        "المطورون",

    legalApi:
        "واجهة الذكاء القانوني",

    legalDesc:
        "أرسل المستندات القانونية واحصل على تحليلات مخاطر منظمة واستخراج البنود والالتزامات والتوصيات.",

    financeApi:
        "واجهة التحليل المالي",

    financeDesc:
        "عالج البيانات المالية واحصل على رؤى حول الإنفاق والاشتراكات وفرص الادخار ومؤشرات الصحة المالية.",

    studyApi:
        "واجهة ذكاء التعلّم",

    studyDesc:
        "أنشئ ملخصات واختبارات وبطاقات تعليمية ومسارات تعلّم مخصصة من المحتوى التعليمي.",

    businessApi:
        "واجهة ذكاء الأعمال",

    businessDesc:
        "حلّل بيانات الأعمال واحصل على مؤشرات الأداء وتقييمات المخاطر والفرص والتوصيات التنفيذية.",

    architecture:
        "بنية API",

    asyncTitle:
        "مصممة للمعالجة غير المتزامنة",

    asyncDesc:
        "قد تتطلب عمليات التحليل وقتاً إضافياً حسب حجم المستندات وتعقيد سير العمل. تعتمد واجهات Runexa على بنية قائمة على المهام: أرسل طلباً، واحصل على معرف معالجة، وتابع التقدم، ثم استرجع النتائج المنظمة عند اكتمال المعالجة.",

    uploadFile:
        "رفع مستند",

    createJob:
        "إنشاء مهمة",

    pollStatus:
        "التحقق من الحالة",

    receiveJson:
        "استرجاع النتائج",

    exampleResponse:
        "مثال على الاستجابة",

    ctaTitle:
        "ابدأ البناء مع Runexa",

    ctaDesc:
        "استخدم واجهات Runexa لتشغيل ذكاء المستندات والتحليل المالي وأتمتة التعلّم ودعم قرارات الأعمال داخل منتجاتك وتدفقات العمل الخاصة بك.",

    readDocs:
        "قراءة التوثيق",
    },
};

type Locale = "en" | "fr" | "ar";

export default function ApiClient({
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
            href="/docs"
            className="rounded-xl bg-blue-600 px-6 py-3 text-sm font-semibold text-white hover:bg-blue-700"
          >
            {t.viewDocs}
          </Link>

          <Link
            href="/developers"
            className="rounded-xl border border-slate-200 bg-white px-6 py-3 text-sm font-semibold text-slate-900 hover:bg-slate-50"
          >
            {t.developers}
          </Link>
        </div>
      </section>

      <section className="mx-auto mt-16 grid max-w-6xl gap-6 md:grid-cols-2">
        {[
          [t.legalApi, t.legalDesc, "POST /v1/legal/analyze"],
          [t.financeApi, t.financeDesc, "POST /v1/finance/analyze"],
          [t.studyApi, t.studyDesc, "POST /v1/study/analyze"],
          [t.businessApi, t.businessDesc, "POST /v1/business/analyze"],
        ].map(([title, desc, endpoint]) => (
          <div key={title} className="rounded-3xl border bg-white p-8 shadow-sm">
            <h2 className="text-2xl font-bold">{title}</h2>
            <p className="mt-4 leading-7 text-slate-600">{desc}</p>

            <div className="mt-6 rounded-2xl bg-slate-950 px-4 py-3 font-mono text-sm text-slate-100">
              {endpoint}
            </div>
          </div>
        ))}
      </section>

      <section className="mx-auto mt-16 max-w-6xl rounded-3xl border bg-white p-8 shadow-sm md:p-12">
        <p className="text-sm font-semibold text-blue-600">
          {t.architecture}
        </p>

        <h2 className="mt-3 text-3xl font-bold">{t.asyncTitle}</h2>

        <p className="mt-4 max-w-4xl leading-7 text-slate-600">
          {t.asyncDesc}
        </p>

        <div className="mt-8 grid gap-4 md:grid-cols-4">
          {[
            t.uploadFile,
            t.createJob,
            t.pollStatus,
            t.receiveJson,
          ].map((item, index) => (
            <div key={item} className="rounded-2xl bg-slate-50 p-5">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-600 text-sm font-bold text-white">
                {index + 1}
              </div>
              <p className="mt-4 font-semibold">{item}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto mt-16 max-w-6xl rounded-3xl border bg-slate-950 p-8 text-white shadow-sm md:p-12">
        <h2 className="text-3xl font-bold">{t.exampleResponse}</h2>

        <pre className="mt-6 overflow-x-auto rounded-2xl border border-white/10 bg-white/5 p-5 text-sm text-slate-100">
{`{
  "job_id": "job_123",
  "status": "completed",
  "result": {
    "agent": "legal",
    "risk_score": 82,
    "summary": "The contract contains several medium-risk clauses.",
    "recommendations": [
      "Clarify termination notice periods.",
      "Review liability limitation language."
    ]
  }
}`}
        </pre>
      </section>

      <section className="mx-auto mt-16 max-w-6xl rounded-3xl bg-blue-600 p-8 text-center text-white md:p-12">
        <h2 className="text-3xl font-bold">{t.ctaTitle}</h2>

        <p className="mx-auto mt-4 max-w-2xl text-blue-100">
          {t.ctaDesc}
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
