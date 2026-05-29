"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getSavedLocale } from "../../lib/i18n";



const docsTranslations = {
  en: {
    badge: "Runexa Documentation",

    title:
        "Runexa API Documentation",

    subtitle:
        "Build AI-powered applications and workflows using Runexa APIs for legal intelligence, financial analysis, learning automation, and business decision support.",

    developerPlatform:
        "Developer Platform",

    developerSubtitle:
        "Asynchronous AI infrastructure built for production",

    contents:
        "Contents",

    introduction:
        "Introduction",

    authentication:
        "Authentication",

    asyncJobs:
        "Asynchronous Processing",

    financeAi:
        "Financial Intelligence",

    legalAi:
        "Legal Intelligence",

    businessAi:
        "Business Intelligence",

    studyAi:
        "Learning Intelligence",

    jobsApi:
        "Jobs API",

    errors:
        "Errors",

    rateLimits:
        "Rate Limits",

    security:
        "Security",

    infrastructure:
        "Runexa AI Infrastructure",

    introText:
        "Runexa APIs enable developers and organizations to integrate advanced AI analysis workflows into applications, dashboards, internal tools, and enterprise systems.",

    legalAnalysis:
        "Legal Document Analysis",

    financeAnalysis:
        "Financial Analysis",

    businessAnalysis:
        "Business Intelligence",

    studyAnalysis:
        "Learning Analysis",

    authText:
        "All API requests require a valid bearer API key.",

    asyncArchitecture:
        "Asynchronous Architecture",

    asyncText:
        "Runexa APIs use asynchronous processing powered by distributed workers and job queues.",

    uploadFile:
        "Upload Document",

    createJob:
        "Create Job",

    workerProcessing:
        "Processing",

    retrieveResults:
        "Retrieve Results",

    bankStatements:
        "Bank Statements",

    subscriptions:
        "Subscriptions",

    savingsOpportunities:
        "Savings Opportunities",

    contractAnalysis:
        "Contract Analysis",

    riskDetection:
        "Risk Detection",

    clauseExtraction:
        "Clause Extraction",

    kpiDashboards:
        "Performance Metrics",

    forecasting:
        "Forecasting",

    executiveReporting:
        "Executive Reporting",

    studyDocuments:
        "Learning Materials",

    summaries:
        "Summaries",

    quizzesFlashcards:
        "Quizzes & Flashcards",

    missingApiKey:
        "Missing or invalid API key.",

    insufficientCredits:
        "Insufficient credits or API access unavailable.",

    fileTooLarge:
        "Uploaded file exceeds allowed limits.",

    rateLimitExceeded:
        "Rate limit exceeded.",

    unexpectedError:
        "Unexpected processing error.",

    custom:
        "Custom",

    neverExpose:
        "Never expose API keys in client-side applications",

    storeServerSide:
        "Store API keys securely on the server",

    rotateKeys:
        "Rotate compromised keys immediately",

    useHttps:
        "Use HTTPS for all API requests",

    baseUrl:
        "Base URL",

    production:
        "Production",

    local:
        "Local",

    jobsApiText:
        "Retrieve the status and results of asynchronous AI jobs.",

    errorResponses:
        "Error Responses",

    plan:
        "Plan",

    requests:
        "Requests",

    securityEnterpriseSupport:
        "Security & Enterprise Support",

    enterpriseSupport:
        "Enterprise Support",

    exploreApiPlatform:
        "Explore the API Platform",
    },
  fr: {
    badge:
        "Documentation Runexa",

    title:
        "Documentation de l’API Runexa",

    subtitle:
        "Créez des applications et des workflows alimentés par l’IA grâce aux API Runexa pour l’intelligence juridique, l’analyse financière, l’automatisation de l’apprentissage et l’aide à la décision business.",

    developerPlatform:
        "Plateforme développeur",

    developerSubtitle:
        "Infrastructure IA asynchrone conçue pour la production",

    contents:
        "Sommaire",

    introduction:
        "Introduction",

    authentication:
        "Authentification",

    asyncJobs:
        "Traitement asynchrone",

    financeAi:
        "Intelligence financière",

    legalAi:
        "Intelligence juridique",

    businessAi:
        "Intelligence business",

    studyAi:
        "Intelligence pédagogique",

    jobsApi:
        "API Jobs",

    errors:
        "Erreurs",

    rateLimits:
        "Limites de débit",

    security:
        "Sécurité",

    infrastructure:
        "Infrastructure IA Runexa",

    introText:
        "Les API Runexa permettent aux développeurs et aux organisations d’intégrer des workflows avancés d’analyse IA dans leurs applications, tableaux de bord, outils internes et systèmes d’entreprise.",

    legalAnalysis:
        "Analyse de documents juridiques",

    financeAnalysis:
        "Analyse financière",

    businessAnalysis:
        "Intelligence business",

    studyAnalysis:
        "Analyse pédagogique",

    authText:
        "Toutes les requêtes API nécessitent une clé API Bearer valide.",

    asyncArchitecture:
        "Architecture asynchrone",

    asyncText:
        "Les API Runexa utilisent un traitement asynchrone alimenté par des workers distribués et des files de traitement.",

    uploadFile:
        "Téléverser un document",

    createJob:
        "Créer un traitement",

    workerProcessing:
        "Traitement",

    retrieveResults:
        "Récupérer les résultats",

    bankStatements:
        "Relevés bancaires",

    subscriptions:
        "Abonnements",

    savingsOpportunities:
        "Opportunités d’économies",

    contractAnalysis:
        "Analyse de contrats",

    riskDetection:
        "Détection des risques",

    clauseExtraction:
        "Extraction de clauses",

    kpiDashboards:
        "Indicateurs de performance",

    forecasting:
        "Prévisions",

    executiveReporting:
        "Reporting exécutif",

    studyDocuments:
        "Supports d’apprentissage",

    summaries:
        "Résumés",

    quizzesFlashcards:
        "Quiz et flashcards",

    missingApiKey:
        "Clé API manquante ou invalide.",

    insufficientCredits:
        "Crédits insuffisants ou accès API indisponible.",

    fileTooLarge:
        "Le fichier dépasse les limites autorisées.",

    rateLimitExceeded:
        "Limite de débit dépassée.",

    unexpectedError:
        "Erreur inattendue lors du traitement.",

    custom:
        "Personnalisé",

    neverExpose:
        "Ne jamais exposer les clés API dans des applications côté client",

    storeServerSide:
        "Stocker les clés API de manière sécurisée côté serveur",

    rotateKeys:
        "Remplacer immédiatement les clés compromises",

    useHttps:
        "Utiliser HTTPS pour toutes les requêtes API",

    baseUrl:
        "URL de base",

    production:
        "Production",

    local:
        "Local",

    jobsApiText:
        "Récupérez l’état et les résultats des traitements IA asynchrones.",

    errorResponses:
        "Réponses d’erreur",

    plan:
        "Plan",

    requests:
        "Requêtes",

    securityEnterpriseSupport:
        "Sécurité et support entreprise",

    enterpriseSupport:
        "Support entreprise",

    exploreApiPlatform:
        "Explorer la plateforme API",
    },
  ar: {
    badge:
        "توثيق Runexa",

    title:
        "توثيق واجهات Runexa API",

    subtitle:
        "أنشئ تطبيقات وتدفقات عمل مدعومة بالذكاء الاصطناعي باستخدام واجهات Runexa للتحليل القانوني والذكاء المالي وأتمتة التعلّم ودعم قرارات الأعمال.",

    developerPlatform:
        "منصة المطورين",

    developerSubtitle:
        "بنية تحتية غير متزامنة للذكاء الاصطناعي مصممة لبيئات الإنتاج",

    contents:
        "المحتويات",

    introduction:
        "المقدمة",

    authentication:
        "المصادقة",

    asyncJobs:
        "المعالجة غير المتزامنة",

    financeAi:
        "الذكاء المالي",

    legalAi:
        "الذكاء القانوني",

    businessAi:
        "ذكاء الأعمال",

    studyAi:
        "ذكاء التعلّم",

    jobsApi:
        "واجهة Jobs API",

    errors:
        "الأخطاء",

    rateLimits:
        "حدود المعدل",

    security:
        "الأمان",

    infrastructure:
        "بنية Runexa للذكاء الاصطناعي",

    introText:
        "تمكّن واجهات Runexa المطورين والمؤسسات من دمج تدفقات متقدمة لتحليل الذكاء الاصطناعي داخل التطبيقات ولوحات التحكم والأدوات الداخلية وأنظمة المؤسسات.",

    legalAnalysis:
        "تحليل المستندات القانونية",

    financeAnalysis:
        "التحليل المالي",

    businessAnalysis:
        "ذكاء الأعمال",

    studyAnalysis:
        "تحليل التعلّم",

    authText:
        "تتطلب جميع طلبات API مفتاح Bearer صالحاً.",

    asyncArchitecture:
        "البنية غير المتزامنة",

    asyncText:
        "تستخدم واجهات Runexa معالجة غير متزامنة تعتمد على عمّال معالجة موزعين وقوائم انتظار للمهام.",

    uploadFile:
        "رفع مستند",

    createJob:
        "إنشاء مهمة",

    workerProcessing:
        "المعالجة",

    retrieveResults:
        "استرجاع النتائج",

    bankStatements:
        "الكشوف البنكية",

    subscriptions:
        "الاشتراكات",

    savingsOpportunities:
        "فرص الادخار",

    contractAnalysis:
        "تحليل العقود",

    riskDetection:
        "كشف المخاطر",

    clauseExtraction:
        "استخراج البنود",

    kpiDashboards:
        "مؤشرات الأداء",

    forecasting:
        "التوقعات",

    executiveReporting:
        "التقارير التنفيذية",

    studyDocuments:
        "مواد التعلّم",

    summaries:
        "الملخصات",

    quizzesFlashcards:
        "الاختبارات والبطاقات التعليمية",

    missingApiKey:
        "مفتاح API مفقود أو غير صالح.",

    insufficientCredits:
        "الرصيد غير كافٍ أو الوصول إلى API غير متاح.",

    fileTooLarge:
        "الملف المرفوع يتجاوز الحدود المسموح بها.",

    rateLimitExceeded:
        "تم تجاوز حد المعدل.",

    unexpectedError:
        "حدث خطأ غير متوقع أثناء المعالجة.",

    custom:
        "مخصص",

    neverExpose:
        "لا تعرض مفاتيح API داخل تطبيقات العميل",

    storeServerSide:
        "خزّن مفاتيح API بشكل آمن على الخادم",

    rotateKeys:
        "استبدل المفاتيح المخترقة فوراً",

    useHttps:
        "استخدم HTTPS لجميع طلبات API",

    baseUrl:
        "الرابط الأساسي",

    production:
        "الإنتاج",

    local:
        "محلي",

    jobsApiText:
        "استرجع حالة ونتائج مهام الذكاء الاصطناعي غير المتزامنة.",

    errorResponses:
        "استجابات الأخطاء",

    plan:
        "الخطة",

    requests:
        "الطلبات",

    securityEnterpriseSupport:
        "الأمان ودعم المؤسسات",

    enterpriseSupport:
        "دعم المؤسسات",

    exploreApiPlatform:
        "استكشاف منصة API",
    },
};

export default function DocsClient() {
  const [locale, setLocale] =
    useState<"en" | "fr" | "ar">("en");

  useEffect(() => {
    const saved = getSavedLocale();

    if (saved === "fr" || saved === "ar") {
      setLocale(saved);
    } else {
      setLocale("en");
    }
  }, []);

  const t = docsTranslations[locale];

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
    </main>
  );
}
