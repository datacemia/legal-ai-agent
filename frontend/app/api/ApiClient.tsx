"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getSavedLocale } from "../../lib/i18n";

const translations = {
  en: {
    badge: "Runexa API",
    title: "AI agent APIs for real-world workflows",
    subtitle:
      "Connect applications, dashboards, and internal tools to Runexa AI agents for contract analysis, finance intelligence, learning automation, and business decision support.",
    viewDocs: "View API Docs",
    developers: "Developers",
    legalApi: "Legal Analysis API",
    legalDesc:
      "Submit legal documents and receive risk scores, clause analysis, obligations, and recommendations.",
    financeApi: "Finance Analysis API",
    financeDesc:
      "Submit bank statements and receive spending insights, subscriptions, savings opportunities, and financial scores.",
    studyApi: "Study Agent API",
    studyDesc:
      "Submit learning material and generate summaries, quizzes, flashcards, and study plans.",
    businessApi: "Business Intelligence API",
    businessDesc:
      "Submit business files and receive KPIs, risks, opportunities, charts, and executive recommendations.",
    architecture: "API architecture",
    asyncTitle: "Built around asynchronous AI jobs",
    asyncDesc:
      "AI analysis can take time depending on file size and workflow complexity. Runexa API is designed around job-based processing: submit a request, receive a job ID, poll for progress, and retrieve structured results when complete.",
    uploadFile: "Upload file",
    createJob: "Create AI job",
    pollStatus: "Poll job status",
    receiveJson: "Receive JSON result",
    exampleResponse: "Example response",
    ctaTitle: "Build with Runexa AI infrastructure",
    ctaDesc:
      "Use Runexa APIs to power document intelligence, finance analysis, learning automation, and business decision support inside your own products.",
    readDocs: "Read API Docs",
  },
  fr: {
    badge: "API Runexa",
    title: "API d’agents IA pour workflows réels",
    subtitle:
      "Connectez vos applications, dashboards et outils internes aux agents IA Runexa pour l’analyse de contrats, l’intelligence financière, l’automatisation de l’apprentissage et l’aide à la décision business.",
    viewDocs: "Voir la documentation API",
    developers: "Développeurs",
    legalApi: "API d’analyse juridique",
    legalDesc:
      "Envoyez des documents juridiques et recevez des scores de risque, analyses de clauses, obligations et recommandations.",
    financeApi: "API d’analyse finance",
    financeDesc:
      "Envoyez des relevés bancaires et recevez des insights de dépenses, abonnements, opportunités d’économies et scores financiers.",
    studyApi: "API agent étude",
    studyDesc:
      "Envoyez du contenu pédagogique et générez des résumés, quiz, flashcards et plans de révision.",
    businessApi: "API business intelligence",
    businessDesc:
      "Envoyez des fichiers business et recevez des KPI, risques, opportunités, graphiques et recommandations exécutives.",
    architecture: "Architecture API",
    asyncTitle: "Conçue autour de jobs IA asynchrones",
    asyncDesc:
      "L’analyse IA peut prendre du temps selon la taille du fichier et la complexité du workflow. L’API Runexa repose sur un traitement par jobs : envoyez une requête, recevez un ID de job, suivez la progression et récupérez les résultats structurés une fois terminés.",
    uploadFile: "Téléverser le fichier",
    createJob: "Créer le job IA",
    pollStatus: "Suivre le statut du job",
    receiveJson: "Recevoir le résultat JSON",
    exampleResponse: "Exemple de réponse",
    ctaTitle: "Construisez avec l’infrastructure IA Runexa",
    ctaDesc:
      "Utilisez les API Runexa pour alimenter l’intelligence documentaire, l’analyse financière, l’automatisation de l’apprentissage et l’aide à la décision business dans vos propres produits.",
    readDocs: "Lire la documentation API",
  },
  ar: {
    badge: "واجهة Runexa API",
    title: "واجهات API لوكلاء ذكاء اصطناعي مخصصة لتدفقات العمل الواقعية",
    subtitle:
      "اربط التطبيقات ولوحات التحكم والأدوات الداخلية بوكلاء Runexa للتحليل القانوني والذكاء المالي وأتمتة التعلم ودعم قرارات الأعمال.",
    viewDocs: "عرض توثيق API",
    developers: "المطورون",
    legalApi: "API التحليل القانوني",
    legalDesc:
      "أرسل مستندات قانونية واحصل على درجات المخاطر وتحليل البنود والالتزامات والتوصيات.",
    financeApi: "API التحليل المالي",
    financeDesc:
      "أرسل كشوفًا بنكية واحصل على رؤى للمصاريف والاشتراكات وفرص الادخار والدرجات المالية.",
    studyApi: "API وكيل الدراسة",
    studyDesc:
      "أرسل مواد تعليمية وأنشئ ملخصات واختبارات وبطاقات تعليمية وخطط دراسة.",
    businessApi: "API ذكاء الأعمال",
    businessDesc:
      "أرسل ملفات الأعمال واحصل على مؤشرات أداء ومخاطر وفرص ورسوم بيانية وتوصيات تنفيذية.",
    architecture: "بنية API",
    asyncTitle: "مصممة حول مهام ذكاء اصطناعي غير متزامنة",
    asyncDesc:
      "قد يستغرق تحليل الذكاء الاصطناعي وقتًا حسب حجم الملف وتعقيد سير العمل. تعتمد Runexa API على معالجة مبنية على المهام: أرسل طلبًا، واحصل على معرف مهمة، وتابع التقدم، ثم استرجع النتائج المنظمة عند الاكتمال.",
    uploadFile: "رفع الملف",
    createJob: "إنشاء مهمة الذكاء الاصطناعي",
    pollStatus: "متابعة حالة المهمة",
    receiveJson: "استلام نتيجة JSON",
    exampleResponse: "مثال على الاستجابة",
    ctaTitle: "ابنِ باستخدام بنية Runexa للذكاء الاصطناعي",
    ctaDesc:
      "استخدم واجهات Runexa لتشغيل ذكاء المستندات والتحليل المالي وأتمتة التعلم ودعم قرارات الأعمال داخل منتجاتك.",
    readDocs: "قراءة توثيق API",
  },
};

export default function ApiClient() {
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
