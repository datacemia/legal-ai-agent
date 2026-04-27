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
  fr: { /* inchangé */ },
  ar: { /* inchangé */ },
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

  // ✅ FIX ICI (aligned pricing)
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

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-8">
      <div className="max-w-5xl mx-auto space-y-8">

        <UploadBox file={file} onFileChange={setFile} />

        <button
          onClick={handleUpload}
          disabled={!file}
          className="rounded-xl bg-slate-950 px-6 py-3 text-white"
        >
          {t.analyzeButton}
        </button>

        {!result && (
          <div className="text-center text-slate-500">{t.empty}</div>
        )}

        {result && !result.authRequired && (
          <div className="space-y-6">

            {/* ✅ FIX message */}
            {isLimitedPreview && (
              <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5 text-sm text-amber-800">
                Limited preview: free users see the summary, risk score, full simplified version, and up to 2 clauses with recommendations. Upgrade to unlock all clauses and recommendations.
              </div>
            )}

            <div>
              <RiskBadge risk={result.risk_level} />
              <RiskScore score={result.risk_score} />
              <p>{result.summary}</p>
            </div>

            {result.simplified_version && (
              <div>{result.simplified_version}</div>
            )}

            {clauses.map((clause, i) => (
              <div key={i}>
                <p>{clause.explanation_simple}</p>
                {clause.recommendation && (
                  <p>{clause.recommendation}</p>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}