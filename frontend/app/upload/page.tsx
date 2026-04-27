"use client";

import { useState } from "react";
import { uploadDocument, runAnalysis } from "../../lib/api";
import { trackEvent } from "../../lib/track";
import RiskBadge from "../../components/RiskBadge";
import RiskScore from "../../components/RiskScore";
import UploadBox from "../../components/UploadBox";

const labels: any = {
  en: {
    pageTitle: "Analyze your contract",
    loading: "Analyzing your contract...",
    file: "File",
    summaryCard: "60-second summary",
    summaryCardText: "Understand key points fast.",
    privateCard: "Private by design",
    privateCardText: "Your documents stay protected.",
    multiCard: "EN / FR / AR",
    multiCardText: "Multilingual contract analysis.",
    signupCta: "Free analysis available after signup",
    loginRequired: "Create an account to analyze your contract",
    author: "Created by Dr. Rachid Ejjami",
    analyzeButton: "Analyze Contract",
    empty:
      "Upload a contract to see the summary, risk score, simplified version, and clause analysis.",
    summary: "Summary",
    simplified: "Simplified Version",
    clauses: "Clauses Analysis",
    clause: "Clause",
    trigger: "Trigger",
    none: "None",
    recommendation: "Recommendation",
  },
  fr: {
    pageTitle: "Analyser votre contrat",
    loading: "Analyse de votre contrat...",
    file: "Fichier",
    summaryCard: "Résumé en 60 secondes",
    summaryCardText: "Comprenez rapidement les points clés.",
    privateCard: "Confidentialité intégrée",
    privateCardText: "Vos documents restent protégés.",
    multiCard: "EN / FR / AR",
    multiCardText: "Analyse multilingue des contrats.",
    signupCta: "Analyse gratuite disponible après inscription",
    loginRequired: "Créez un compte pour analyser votre contrat",
    author: "Créé par Dr. Rachid Ejjami",
    analyzeButton: "Analyser le contrat",
    empty:
      "Téléversez un contrat pour voir le résumé, le score de risque, la version simplifiée et l’analyse des clauses.",
    summary: "Résumé",
    simplified: "Version simplifiée",
    clauses: "Analyse des clauses",
    clause: "Clause",
    trigger: "Déclencheur",
    none: "Aucun",
    recommendation: "Recommandation",
  },
  ar: {
    pageTitle: "تحليل العقد",
    loading: "جاري تحليل العقد...",
    file: "الملف",
    summaryCard: "ملخص خلال 60 ثانية",
    summaryCardText: "افهم النقاط الأساسية بسرعة.",
    privateCard: "خصوصية مدمجة",
    privateCardText: "تبقى مستنداتك محمية.",
    multiCard: "EN / FR / AR",
    multiCardText: "تحليل عقود متعدد اللغات.",
    signupCta: "التحليل المجاني متاح بعد التسجيل",
    loginRequired: "أنشئ حسابًا لتحليل عقدك",
    author: "تم تطويره بواسطة د. رشيد الجامعي",
    analyzeButton: "تحليل العقد",
    empty:
      "قم برفع عقد لعرض الملخص ودرجة المخاطر والنسخة المبسطة وتحليل البنود.",
    summary: "ملخص",
    simplified: "نسخة مبسطة",
    clauses: "تحليل البنود",
    clause: "البند",
    trigger: "المؤشر",
    none: "لا يوجد",
    recommendation: "التوصية",
  },
};

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [fileName, setFileName] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [language, setLanguage] = useState("en");
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  const t = labels[language] || labels.en;

  const handleUpload = async () => {
    if (!file) return;

    const token = localStorage.getItem("token");

    if (!token) {
      setResult({ authRequired: true });
      return;
    }

    trackEvent("upload_document");

    try {
      setLoading(true);
      setResult(null);
      setOpenIndex(null);

      const doc = await uploadDocument(file);
      const analysis = await runAnalysis(doc.id, language);

      if (analysis.detail?.includes("Payment required")) {
        alert("You used your free analysis. Please buy one analysis credit.");
        window.location.href = "/dashboard";
        return;
      }

      setResult(analysis);
    } finally {
      setLoading(false);
    }
  };

  let clauses: any[] = [];

  try {
    if (result?.clauses && !result?.authRequired) {
      clauses = Array.isArray(result.clauses)
        ? result.clauses
        : JSON.parse(result.clauses);
    }
  } catch (e) {
    console.error("Clause parsing error:", e);
    clauses = [];
  }

  const isLimitedPreview =
    result &&
    !result.authRequired &&
    clauses.length <= 2;

  if (loading) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-slate-50 px-4">
        <div className="bg-white p-8 rounded-2xl shadow-sm border text-center space-y-4 w-full max-w-sm">
          <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="font-medium text-slate-900">{t.loading}</p>
          {fileName && (
            <p className="text-sm text-slate-500">
              {t.file}: {fileName}
            </p>
          )}
        </div>
      </main>
    );
  }

  const featureCards = [
    { number: "01", title: t.summaryCard, text: t.summaryCardText },
    { number: "02", title: t.privateCard, text: t.privateCardText },
    { number: "03", title: t.multiCard, text: t.multiCardText },
  ];

  return (
    <main
      dir={language === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-4 py-8 sm:px-6"
    >
      <div className="max-w-5xl mx-auto space-y-8">
        <div className="text-center space-y-3">
          <p className="text-sm font-semibold text-blue-600">{t.signupCta}</p>
          <h1 className="text-3xl sm:text-4xl font-bold text-slate-950">
            {t.pageTitle}
          </h1>
          <p className="text-sm text-slate-500">{t.author}</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {featureCards.map((card) => (
            <div key={card.number} className="bg-white border rounded-2xl p-5">
              <p className="font-semibold">{card.title}</p>
              <p className="text-sm text-slate-500 mt-2">{card.text}</p>
            </div>
          ))}
        </div>

        <UploadBox file={file} onFileChange={setFile} />

        {result && isLimitedPreview && (
          <div className="bg-yellow-50 p-4 rounded-xl text-sm text-yellow-800">
            Limited preview: free users see summary, risk score, full simplified
            version, and only 2 clauses with recommendations.
          </div>
        )}

        {result && (
          <>
            <RiskBadge risk={result.risk_level} />
            <RiskScore score={result.risk_score} />

            <div>{result.summary}</div>

            {result.simplified_version && (
              <div>{result.simplified_version}</div>
            )}

            {clauses.map((c, i) => (
              <div key={i}>
                <div>{c.explanation_simple}</div>
                {c.recommendation && <div>{c.recommendation}</div>}
              </div>
            ))}
          </>
        )}
      </div>
    </main>
  );
}