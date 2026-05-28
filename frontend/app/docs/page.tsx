"use client";

import Link from "next/link";
import { getSavedLocale } from "../../lib/i18n";



const docsTranslations = {
  en: {
    badge: "Runexa Docs",
    title: "AI Agent API Documentation",
    subtitle:
      "Build AI-powered workflows using Runexa asynchronous APIs for legal, finance, business intelligence, and study automation.",
    developerPlatform: "Developer Platform",
    developerSubtitle: "Async AI infrastructure for enterprise workflows",
    contents: "Contents",
    introduction: "Introduction",
    authentication: "Authentication",
    asyncJobs: "Async jobs",
    financeAi: "Finance AI",
    legalAi: "Legal AI",
    businessAi: "Business AI",
    studyAi: "Study AI",
    jobsApi: "Jobs API",
    errors: "Errors",
    rateLimits: "Rate limits",
    security: "Security",
    infrastructure: "Runexa AI infrastructure",
    introText:
      "Runexa API allows developers and enterprises to integrate advanced AI analysis workflows directly into products, dashboards, internal tools, and enterprise systems.",
    legalAnalysis: "Legal AI analysis",
    financeAnalysis: "Finance AI analysis",
    businessAnalysis: "Business AI analysis",
    studyAnalysis: "Study AI analysis",
    authText: "All API requests require a bearer API key.",
    asyncArchitecture: "Async Architecture",
    asyncText:
      "Runexa APIs use asynchronous AI processing powered by queue-based workers.",
    uploadFile: "Upload file",
    createJob: "Create AI job",
    workerProcessing: "Worker processing",
    retrieveResults: "Retrieve results",
    bankStatements: "Bank statements",
    subscriptions: "Subscriptions",
    savingsOpportunities: "Savings opportunities",
    contractAnalysis: "Contract analysis",
    riskDetection: "Risk detection",
    clauseExtraction: "Clause extraction",
    kpiDashboards: "KPI dashboards",
    forecasting: "Forecasting",
    executiveReporting: "Executive reporting",
    studyDocuments: "Study documents",
    summaries: "Summaries",
    quizzesFlashcards: "Quizzes and flashcards",
    missingApiKey: "Missing or invalid API key.",
    insufficientCredits: "Insufficient credits or API access disabled.",
    fileTooLarge: "Uploaded file exceeds allowed limits.",
    rateLimitExceeded: "Rate limit exceeded.",
    unexpectedError: "Unexpected AI processing error.",
    custom: "Custom",
    neverExpose: "Never expose API keys publicly",
    storeServerSide: "Store API keys server-side",
    rotateKeys: "Rotate compromised keys immediately",
    useHttps: "Use HTTPS only",
    baseUrl: "Base URL",
    production: "Production",
    local: "Local",
    jobsApiText: "Retrieve asynchronous AI analysis results.",
    errorResponses: "Error Responses",
    plan: "Plan",
    requests: "Requests",
    securityEnterpriseSupport: "Security & Enterprise Support",
    enterpriseSupport: "Enterprise Support",
    exploreApiPlatform: "Explore API Platform",
  },
  fr: {
    badge: "Documentation Runexa",
    title: "Documentation API des agents IA",
    subtitle:
      "Construisez des workflows IA avec les API asynchrones Runexa pour le juridique, la finance, la business intelligence et l’apprentissage.",
    developerPlatform: "Plateforme développeur",
    developerSubtitle: "Infrastructure IA asynchrone pour workflows entreprise",
    contents: "Sommaire",
    introduction: "Introduction",
    authentication: "Authentification",
    asyncJobs: "Jobs asynchrones",
    financeAi: "IA finance",
    legalAi: "IA juridique",
    businessAi: "IA business",
    studyAi: "IA étude",
    jobsApi: "API Jobs",
    errors: "Erreurs",
    rateLimits: "Limites de débit",
    security: "Sécurité",
    infrastructure: "Infrastructure IA Runexa",
    introText:
      "L’API Runexa permet aux développeurs et entreprises d’intégrer des workflows avancés d’analyse IA directement dans leurs produits, dashboards, outils internes et systèmes entreprise.",
    legalAnalysis: "Analyse IA juridique",
    financeAnalysis: "Analyse IA finance",
    businessAnalysis: "Analyse IA business",
    studyAnalysis: "Analyse IA étude",
    authText: "Toutes les requêtes API nécessitent une clé API Bearer.",
    asyncArchitecture: "Architecture asynchrone",
    asyncText:
      "Les API Runexa utilisent un traitement IA asynchrone alimenté par des workers et une file de jobs.",
    uploadFile: "Téléverser le fichier",
    createJob: "Créer le job IA",
    workerProcessing: "Traitement par worker",
    retrieveResults: "Récupérer les résultats",
    bankStatements: "Relevés bancaires",
    subscriptions: "Abonnements",
    savingsOpportunities: "Opportunités d’économies",
    contractAnalysis: "Analyse de contrat",
    riskDetection: "Détection des risques",
    clauseExtraction: "Extraction des clauses",
    kpiDashboards: "Dashboards KPI",
    forecasting: "Prévisions",
    executiveReporting: "Reporting exécutif",
    studyDocuments: "Documents d’étude",
    summaries: "Résumés",
    quizzesFlashcards: "Quiz et flashcards",
    missingApiKey: "Clé API manquante ou invalide.",
    insufficientCredits: "Crédits insuffisants ou accès API désactivé.",
    fileTooLarge: "Le fichier dépasse les limites autorisées.",
    rateLimitExceeded: "Limite de débit dépassée.",
    unexpectedError: "Erreur inattendue du traitement IA.",
    custom: "Personnalisé",
    neverExpose: "Ne jamais exposer les clés API publiquement",
    storeServerSide: "Stocker les clés API côté serveur",
    rotateKeys: "Remplacer immédiatement les clés compromises",
    useHttps: "Utiliser HTTPS uniquement",
    baseUrl: "URL de base",
    production: "Production",
    local: "Local",
    jobsApiText: "Récupérez les résultats des analyses IA asynchrones.",
    errorResponses: "Réponses d’erreur",
    plan: "Plan",
    requests: "Requêtes",
    securityEnterpriseSupport: "Sécurité et support entreprise",
    enterpriseSupport: "Support entreprise",
    exploreApiPlatform: "Explorer la plateforme API",
  },
  ar: {
    badge: "توثيق Runexa",
    title: "توثيق API لوكلاء الذكاء الاصطناعي",
    subtitle:
      "أنشئ تدفقات عمل مدعومة بالذكاء الاصطناعي باستخدام واجهات Runexa غير المتزامنة للقانون والمالية وذكاء الأعمال والدراسة.",
    developerPlatform: "منصة المطورين",
    developerSubtitle: "بنية ذكاء اصطناعي غير متزامنة لسير عمل المؤسسات",
    contents: "المحتويات",
    introduction: "المقدمة",
    authentication: "المصادقة",
    asyncJobs: "المهام غير المتزامنة",
    financeAi: "الذكاء المالي",
    legalAi: "الذكاء القانوني",
    businessAi: "ذكاء الأعمال",
    studyAi: "ذكاء الدراسة",
    jobsApi: "API المهام",
    errors: "الأخطاء",
    rateLimits: "حدود المعدل",
    security: "الأمان",
    infrastructure: "بنية Runexa للذكاء الاصطناعي",
    introText:
      "تتيح API Runexa للمطورين والمؤسسات دمج تدفقات تحليل ذكاء اصطناعي متقدمة مباشرة داخل المنتجات ولوحات التحكم والأدوات الداخلية وأنظمة المؤسسات.",
    legalAnalysis: "تحليل قانوني بالذكاء الاصطناعي",
    financeAnalysis: "تحليل مالي بالذكاء الاصطناعي",
    businessAnalysis: "تحليل أعمال بالذكاء الاصطناعي",
    studyAnalysis: "تحليل دراسي بالذكاء الاصطناعي",
    authText: "تتطلب جميع طلبات API مفتاح Bearer.",
    asyncArchitecture: "البنية غير المتزامنة",
    asyncText:
      "تستخدم واجهات Runexa معالجة ذكاء اصطناعي غير متزامنة تعتمد على قائمة مهام وعمّال معالجة.",
    uploadFile: "رفع الملف",
    createJob: "إنشاء مهمة الذكاء الاصطناعي",
    workerProcessing: "المعالجة عبر العامل",
    retrieveResults: "استرجاع النتائج",
    bankStatements: "الكشوف البنكية",
    subscriptions: "الاشتراكات",
    savingsOpportunities: "فرص الادخار",
    contractAnalysis: "تحليل العقود",
    riskDetection: "كشف المخاطر",
    clauseExtraction: "استخراج البنود",
    kpiDashboards: "لوحات مؤشرات الأداء",
    forecasting: "التوقعات",
    executiveReporting: "تقارير تنفيذية",
    studyDocuments: "مستندات الدراسة",
    summaries: "الملخصات",
    quizzesFlashcards: "اختبارات وبطاقات تعليمية",
    missingApiKey: "مفتاح API مفقود أو غير صالح.",
    insufficientCredits: "الرصيد غير كافٍ أو الوصول إلى API معطل.",
    fileTooLarge: "الملف المرفوع يتجاوز الحدود المسموح بها.",
    rateLimitExceeded: "تم تجاوز حد المعدل.",
    unexpectedError: "خطأ غير متوقع أثناء معالجة الذكاء الاصطناعي.",
    custom: "مخصص",
    neverExpose: "لا تعرض مفاتيح API علنًا",
    storeServerSide: "خزّن مفاتيح API على الخادم",
    rotateKeys: "استبدل المفاتيح المخترقة فورًا",
    useHttps: "استخدم HTTPS فقط",
    baseUrl: "رابط الأساس",
    production: "الإنتاج",
    local: "محلي",
    jobsApiText: "استرجع نتائج تحليلات الذكاء الاصطناعي غير المتزامنة.",
    errorResponses: "استجابات الأخطاء",
    plan: "الخطة",
    requests: "الطلبات",
    securityEnterpriseSupport: "الأمان ودعم المؤسسات",
    enterpriseSupport: "دعم المؤسسات",
    exploreApiPlatform: "استكشاف منصة API",
  },
};

export default function DocsPage() {
  const locale = getSavedLocale();
  const t =
    docsTranslations[locale as keyof typeof docsTranslations] ||
    docsTranslations.en;

  return (
    <main
      dir={locale === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-6 py-20 text-slate-900"
    >
      <section className="mx-auto max-w-7xl">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <p className="font-semibold text-blue-600">{t.badge}</p>

            <h1 className="mt-4 text-5xl font-bold tracking-tight">
              {t.title}
            </h1>

            <p className="mt-6 max-w-3xl text-lg leading-8 text-slate-600">
              {t.subtitle}
            </p>
          </div>

          <div className="rounded-2xl border border-blue-200 bg-blue-50 px-5 py-4">
            <p className="text-xs font-semibold uppercase tracking-[0.25em] text-blue-700">
              {t.developerPlatform}
            </p>

            <p className="mt-2 text-sm text-blue-900">
              {t.developerSubtitle}
            </p>
          </div>
        </div>
      </section>

      <section className="mx-auto mt-12 grid max-w-7xl gap-6 lg:grid-cols-[280px_1fr]">
        <aside className="sticky top-10 h-fit rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <p className="text-sm font-bold text-slate-900">{t.contents}</p>

          <nav className="mt-5 space-y-3 text-sm text-slate-600">
            {[
              [t.introduction, "#introduction"],
              [t.authentication, "#authentication"],
              [t.asyncJobs, "#jobs"],
              [t.financeAi, "#finance"],
              [t.legalAi, "#legal"],
              [t.businessAi, "#business"],
              [t.studyAi, "#study"],
              [t.jobsApi, "#jobs-api"],
              [t.errors, "#errors"],
              [t.rateLimits, "#rate-limits"],
              [t.security, "#security"],
            ].map(([label, href]) => (
              <a
                key={href}
                href={href}
                className="block transition hover:text-blue-600"
              >
                {label}
              </a>
            ))}
          </nav>
        </aside>

        <div className="space-y-8">
          <section
            id="introduction"
            className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm"
          >
            <p className="text-sm font-semibold text-blue-600">
              {t.introduction}
            </p>

            <h2 className="mt-3 text-3xl font-bold">
              {t.infrastructure}
            </h2>

            <p className="mt-5 leading-8 text-slate-600">
              {t.introText}
            </p>

            <div className="mt-8 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              {[
                t.legalAnalysis,
                t.financeAnalysis,
                t.businessAnalysis,
                t.studyAnalysis,
              ].map((item) => (
                <div
                  key={item}
                  className="rounded-2xl border border-slate-200 bg-slate-50 p-5"
                >
                  <p className="font-semibold text-slate-900">{item}</p>
                </div>
              ))}
            </div>

            <div className="mt-8 rounded-2xl bg-slate-950 p-6 text-sm text-slate-100">
              <p className="text-slate-400">{t.baseUrl}</p>

              <div className="mt-4 overflow-x-auto text-blue-300">
                <p>{t.production}:</p>
                <p>https://api.runexa.ai</p>
                <br />
                <p>{t.local}:</p>
                <p>http://127.0.0.1:8000</p>
              </div>
            </div>
          </section>

          <section
            id="authentication"
            className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm"
          >
            <h2 className="text-3xl font-bold">{t.authentication}</h2>

            <p className="mt-5 leading-8 text-slate-600">
              {t.authText}
            </p>

            <pre className="mt-6 overflow-x-auto rounded-2xl bg-slate-950 p-5 text-sm text-slate-100">
{`Authorization: Bearer rk_live_xxxxxxxxx`}
            </pre>

            <pre className="mt-6 overflow-x-auto rounded-2xl bg-slate-950 p-5 text-sm text-slate-100">
{`curl -X GET "https://api.runexa.ai/v1/test-api-key" \\
  -H "Authorization: Bearer rk_live_xxxxxxxxx"`}
            </pre>
          </section>

          <section
            id="jobs"
            className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm"
          >
            <h2 className="text-3xl font-bold">{t.asyncArchitecture}</h2>

            <p className="mt-5 leading-8 text-slate-600">
              {t.asyncText}
            </p>

            <div className="mt-8 grid gap-4 md:grid-cols-4">
              {[
                t.uploadFile,
                t.createJob,
                t.workerProcessing,
                t.retrieveResults,
              ].map((item, index) => (
                <div
                  key={item}
                  className="rounded-2xl border border-slate-200 bg-slate-50 p-5"
                >
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-600 text-sm font-bold text-white">
                    {index + 1}
                  </div>

                  <p className="mt-4 font-semibold text-slate-900">{item}</p>
                </div>
              ))}
            </div>

            <pre className="mt-8 overflow-x-auto rounded-2xl bg-slate-950 p-5 text-sm text-slate-100">
{`Frontend
→ Runexa API
→ Job Queue
→ AI Workers
→ Persistent Storage
→ Async Result Retrieval`}
            </pre>
          </section>

          <section
            id="finance"
            className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm"
          >
            <div className="flex items-center justify-between">
              <h2 className="text-3xl font-bold">{t.financeAi}</h2>

              <span className="rounded-full bg-emerald-100 px-3 py-1 text-xs font-bold text-emerald-700">
                POST /v1/finance/analyze
              </span>
            </div>

            <div className="mt-6 grid gap-4 md:grid-cols-3">
              {[
                t.bankStatements,
                t.subscriptions,
                t.savingsOpportunities,
              ].map((item) => (
                <div
                  key={item}
                  className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4"
                >
                  <p className="font-semibold text-emerald-900">{item}</p>
                </div>
              ))}
            </div>

            <pre className="mt-8 overflow-x-auto rounded-2xl bg-slate-950 p-5 text-sm text-slate-100">
{`curl -X POST "https://api.runexa.ai/v1/finance/analyze" \\
  -H "Authorization: Bearer rk_live_xxxxxxxxx" \\
  -F "file=@statement.pdf" \\
  -F "output_language=en"`}
            </pre>

            <pre className="mt-6 overflow-x-auto rounded-2xl bg-slate-950 p-5 text-sm text-slate-100">
{`{
  "job_id": 9,
  "status": "pending",
  "progress": 0,
  "status_message": "Finance API analysis queued...",
  "credits_used": 7,
  "remaining_api_credits": 88
}`}
            </pre>
          </section>

          <section
            id="legal"
            className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm"
          >
            <div className="flex items-center justify-between">
              <h2 className="text-3xl font-bold">{t.legalAi}</h2>

              <span className="rounded-full bg-amber-100 px-3 py-1 text-xs font-bold text-amber-700">
                POST /v1/legal/analyze
              </span>
            </div>

            <div className="mt-6 grid gap-4 md:grid-cols-3">
              {[
                t.contractAnalysis,
                t.riskDetection,
                t.clauseExtraction,
              ].map((item) => (
                <div
                  key={item}
                  className="rounded-2xl border border-amber-200 bg-amber-50 p-4"
                >
                  <p className="font-semibold text-amber-900">{item}</p>
                </div>
              ))}
            </div>

            <pre className="mt-8 overflow-x-auto rounded-2xl bg-slate-950 p-5 text-sm text-slate-100">
{`curl -X POST "https://api.runexa.ai/v1/legal/analyze" \\
  -H "Authorization: Bearer rk_live_xxxxxxxxx" \\
  -F "file=@contract.pdf" \\
  -F "output_language=en"`}
            </pre>

            <pre className="mt-6 overflow-x-auto rounded-2xl bg-slate-950 p-5 text-sm text-slate-100">
{`{
  "job_id": 10,
  "status": "pending",
  "credits_used": 12,
  "remaining_api_credits": 76
}`}
            </pre>
          </section>

          <section
            id="business"
            className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm"
          >
            <div className="flex items-center justify-between">
              <h2 className="text-3xl font-bold">{t.businessAi}</h2>

              <span className="rounded-full bg-blue-100 px-3 py-1 text-xs font-bold text-blue-700">
                POST /v1/business/analyze
              </span>
            </div>

            <div className="mt-6 grid gap-4 md:grid-cols-3">
              {[
                t.kpiDashboards,
                t.forecasting,
                t.executiveReporting,
              ].map((item) => (
                <div
                  key={item}
                  className="rounded-2xl border border-blue-200 bg-blue-50 p-4"
                >
                  <p className="font-semibold text-blue-900">{item}</p>
                </div>
              ))}
            </div>

            <pre className="mt-8 overflow-x-auto rounded-2xl bg-slate-950 p-5 text-sm text-slate-100">
{`curl -X POST "https://api.runexa.ai/v1/business/analyze" \\
  -H "Authorization: Bearer rk_live_xxxxxxxxx" \\
  -F "file=@business.xlsx" \\
  -F "output_language=en"`}
            </pre>

            <pre className="mt-6 overflow-x-auto rounded-2xl bg-slate-950 p-5 text-sm text-slate-100">
{`{
  "job_id": 13,
  "status": "pending",
  "credits_used": 30,
  "remaining_api_credits": 22
}`}
            </pre>
          </section>

          <section
            id="study"
            className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm"
          >
            <div className="flex items-center justify-between">
              <h2 className="text-3xl font-bold">{t.studyAi}</h2>

              <span className="rounded-full bg-violet-100 px-3 py-1 text-xs font-bold text-violet-700">
                POST /v1/study/analyze
              </span>
            </div>

            <div className="mt-6 grid gap-4 md:grid-cols-3">
              {[
                t.studyDocuments,
                t.summaries,
                t.quizzesFlashcards,
              ].map((item) => (
                <div
                  key={item}
                  className="rounded-2xl border border-violet-200 bg-violet-50 p-4"
                >
                  <p className="font-semibold text-violet-900">{item}</p>
                </div>
              ))}
            </div>

            <pre className="mt-8 overflow-x-auto rounded-2xl bg-slate-950 p-5 text-sm text-slate-100">
{`curl -X POST "https://api.runexa.ai/v1/study/analyze" \\
  -H "Authorization: Bearer rk_live_xxxxxxxxx" \\
  -F "file=@study.pdf" \\
  -F "output_language=en" \\
  -F "education_level=university"`}
            </pre>

            <pre className="mt-6 overflow-x-auto rounded-2xl bg-slate-950 p-5 text-sm text-slate-100">
{`{
  "job_id": 14,
  "status": "pending",
  "credits_used": 5,
  "remaining_api_credits": 17
}`}
            </pre>
          </section>

          <section
            id="jobs-api"
            className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm"
          >
            <h2 className="text-3xl font-bold">{t.jobsApi}</h2>

            <p className="mt-5 leading-8 text-slate-600">
              {t.jobsApiText}
            </p>

            <pre className="mt-8 overflow-x-auto rounded-2xl bg-slate-950 p-5 text-sm text-slate-100">
{`GET /v1/jobs/{job_id}

{
  "id": 15,
  "status": "completed",
  "progress": 100,
  "result": {}
}`}
            </pre>
          </section>

          <section
            id="errors"
            className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm"
          >
            <h2 className="text-3xl font-bold">{t.errors}</h2>

            <div className="mt-8 space-y-4">
              {[
                ["401", t.missingApiKey],
                ["402", t.insufficientCredits],
                ["413", t.fileTooLarge],
                ["429", t.rateLimitExceeded],
                ["500", t.unexpectedError],
              ].map(([code, desc]) => (
                <div
                  key={code}
                  className="rounded-2xl border border-slate-200 bg-slate-50 p-5"
                >
                  <p className="font-bold text-slate-900">{code}</p>

                  <p className="mt-2 text-sm text-slate-600">{desc}</p>
                </div>
              ))}
            </div>
          </section>

          <section
            id="rate-limits"
            className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm"
          >
            <h2 className="text-3xl font-bold">{t.rateLimits}</h2>

            <div className="mt-8 overflow-hidden rounded-2xl border border-slate-200">
              <table className="min-w-full divide-y divide-slate-200 text-sm">
                <thead className="bg-slate-100">
                  <tr>
                    <th className="px-5 py-4 text-left font-bold">
                      {t.plan}
                    </th>
                    <th className="px-5 py-4 text-left font-bold">
                      {t.requests}
                    </th>
                  </tr>
                </thead>

                <tbody className="divide-y divide-slate-200 bg-white">
                  {[
                    ["API Starter", "10 requests/minute"],
                    ["API Pro", "60 requests/minute"],
                    ["Enterprise API", t.custom],
                  ].map(([plan, limit]) => (
                    <tr key={plan}>
                      <td className="px-5 py-4">{plan}</td>
                      <td className="px-5 py-4">{limit}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          <section
            id="security"
            className="rounded-3xl bg-slate-950 p-8 text-white"
          >
            <h2 className="text-3xl font-bold">
              {t.securityEnterpriseSupport}
            </h2>

            <div className="mt-6 grid gap-4 md:grid-cols-2">
              {[
                t.neverExpose,
                t.storeServerSide,
                t.rotateKeys,
                t.useHttps,
              ].map((item) => (
                <div
                  key={item}
                  className="rounded-2xl bg-white/5 p-4"
                >
                  <p className="text-slate-100">{item}</p>
                </div>
              ))}
            </div>

            <div className="mt-8 rounded-2xl border border-white/10 bg-white/5 p-6">
              <p className="text-sm uppercase tracking-[0.25em] text-blue-300">
                {t.enterpriseSupport}
              </p>

              <p className="mt-3 text-lg font-semibold">
                support@runexa.ai
              </p>
            </div>

            <Link
              href="/api"
              className="mt-8 inline-flex items-center rounded-2xl bg-white px-6 py-3 text-sm font-semibold text-slate-900 transition hover:-translate-y-0.5"
            >
              {t.exploreApiPlatform}
            </Link>
          </section>
        </div>
      </section>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "TechArticle",
            headline: "Runexa {t.title}",
            description:
              "Developer documentation for Runexa AI APIs including legal AI, finance AI, business intelligence, and study automation.",
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
    </main>
  );
}
