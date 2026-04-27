"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { getAnalysis } from "../../../lib/api";
import RiskBadge from "../../../components/RiskBadge";
import RiskScore from "../../../components/RiskScore";

function normalizeLanguage(value?: string) {
  const lang = value?.toLowerCase().trim() || "";

  if (
    lang === "fr" ||
    lang.includes("french") ||
    lang.includes("français")
  ) {
    return "fr";
  }

  if (
    lang === "ar" ||
    lang.includes("arabic") ||
    lang.includes("العربية")
  ) {
    return "ar";
  }

  return "en";
}

const labels: any = {
  en: {
    loading: "Loading analysis...",
    notFound: "Analysis not found",
    back: "← Back to dashboard",
    documentAnalysis: "Document analysis",
    title: "Contract Analysis",
    simplified: "Simplified Version",
    detailed: "Detailed review",
    clauses: "Clauses Analysis",
    clause: "Clause",
    trigger: "Trigger",
    none: "None",
    recommendation: "Recommendation",
  },
  fr: {
    loading: "Chargement de l’analyse...",
    notFound: "Analyse introuvable",
    back: "← Retour au tableau de bord",
    documentAnalysis: "Analyse du document",
    title: "Analyse du contrat",
    simplified: "Version simplifiée",
    detailed: "Revue détaillée",
    clauses: "Analyse des clauses",
    clause: "Clause",
    trigger: "Déclencheur",
    none: "Aucun",
    recommendation: "Recommandation",
  },
  ar: {
    loading: "جاري تحميل التحليل...",
    notFound: "لم يتم العثور على التحليل",
    back: "← الرجوع إلى لوحة التحكم",
    documentAnalysis: "تحليل الوثيقة",
    title: "تحليل العقد",
    simplified: "النسخة المبسطة",
    detailed: "مراجعة تفصيلية",
    clauses: "تحليل البنود",
    clause: "البند",
    trigger: "المؤشر",
    none: "لا يوجد",
    recommendation: "التوصية",
  },
};

export default function DocumentPage() {
  const params = useParams();
  const documentId = Number(params.id);

  const [analysis, setAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  useEffect(() => {
    async function loadAnalysis() {
      try {
        const data = await getAnalysis(documentId);
        setAnalysis(data);
      } finally {
        setLoading(false);
      }
    }

    loadAnalysis();
  }, [documentId]);

  const language = normalizeLanguage(analysis?.language);
  const isArabic = language === "ar";
  const t = labels[language] || labels.en;

  if (loading) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-slate-50">
        <p className="text-slate-600">{t.loading}</p>
      </main>
    );
  }

  if (!analysis?.id) {
    return (
      <main className="min-h-screen bg-slate-50 px-4 py-8">
        <div className="max-w-4xl mx-auto bg-white border border-slate-200 rounded-3xl p-8 shadow-sm">
          <h1 className="text-xl font-bold text-slate-950">{t.notFound}</h1>

          <Link
            href="/dashboard"
            className="text-blue-600 mt-4 inline-block font-medium"
          >
            {t.back}
          </Link>
          <div className="rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">
         ⚠️ {language === "fr"
          ? "Cet outil ne remplace pas un avocat. Vérifiez toujours vos contrats attentivement."
          : language === "ar"
          ? "⚠️ هذه الأداة لا تغني عن محامٍ. يجب مراجعة العقود بعناية."
          : "This tool does not replace a lawyer. Always review contracts carefully."}
          </div>
        </div>
      </main>
    );
  }

  const clauses = analysis?.clauses ? JSON.parse(analysis.clauses) : [];

  return (
    <main
      dir={isArabic ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-4 py-8 sm:px-6"
    >
      <div className="max-w-5xl mx-auto space-y-8">
        <Link
          href="/dashboard"
          className="inline-flex text-sm font-medium text-blue-600 hover:text-blue-700"
        >
          {t.back}
        </Link>

        <section className="bg-white p-6 rounded-3xl shadow-sm border border-slate-200">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div className="text-start">
              <p className="text-sm font-semibold text-blue-600">
                {t.documentAnalysis}
              </p>
              <h1 className="mt-1 text-2xl sm:text-3xl font-bold text-slate-950">
                {t.title}
              </h1>
            </div>

            <RiskBadge risk={analysis.risk_level} language={language} />
          </div>

          <p className="mt-6 text-slate-700 whitespace-pre-line leading-7 text-start">
            {analysis.summary}
          </p>
        </section>

        <RiskScore score={analysis.risk_score} language={language} />

        <section className="bg-blue-50 p-6 rounded-3xl border border-blue-200">
          <h2 className="text-xl font-semibold text-blue-800 text-start">
            {t.simplified}
          </h2>

          <p className="mt-4 text-blue-900 whitespace-pre-line leading-7 text-start">
            {analysis.simplified_version}
          </p>
        </section>

        <section className="bg-white p-6 rounded-3xl shadow-sm border border-slate-200">
          <div className="flex items-center justify-between gap-4 mb-5">
            <div className="text-start">
              <p className="text-sm text-slate-500">{t.detailed}</p>
              <h2 className="text-xl font-semibold text-slate-950">
                {t.clauses}
              </h2>
            </div>

            <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600">
              {clauses.length}
            </span>
          </div>

          <div className="space-y-4">
            {clauses.map((clause: any, index: number) => (
              <div
                key={index}
                className={`border rounded-2xl p-4 cursor-pointer transition ${
                  clause.risk_level === "high"
                    ? "border-red-300 bg-red-50"
                    : clause.risk_level === "medium"
                    ? "border-yellow-300 bg-yellow-50"
                    : "border-slate-200 bg-white hover:bg-slate-50"
                }`}
                onClick={() => setOpenIndex(openIndex === index ? null : index)}
              >
                <div className="flex items-center justify-between gap-4">
                  <div className="flex items-center gap-3">
                    <span className="flex h-8 w-8 items-center justify-center rounded-xl bg-white text-sm font-semibold text-slate-700 border">
                      {index + 1}
                    </span>

                    <span className="font-semibold text-slate-900">
                      {t.clause} {index + 1}
                    </span>

                    <span className="text-xs text-slate-400">
                      {openIndex === index ? "▲" : "▼"}
                    </span>
                  </div>

                  <RiskBadge risk={clause.risk_level} language={language} />
                </div>

                <p className="text-blue-700 text-sm mt-3 text-start whitespace-pre-line">
                  {clause.explanation_simple}
                </p>

                {openIndex === index && (
                  <div className="mt-4 space-y-3 text-start">
                    <p className="text-sm text-slate-500">
                      <span className="font-medium">{t.trigger}:</span>{" "}
                      {clause.trigger || t.none}
                    </p>

                    <p className="text-slate-800 leading-7 whitespace-pre-line">
                      {clause.original_text}
                    </p>

                    <p className="text-slate-600 text-sm leading-7">
                      <span className="font-medium">{t.recommendation}:</span>{" "}
                      {clause.recommendation}
                    </p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}