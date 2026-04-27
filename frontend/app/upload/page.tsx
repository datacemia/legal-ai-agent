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
    limitedNotice:
      "Only 2 clauses are displayed in the free version. Upgrade to unlock full clause analysis.",
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
  let isLimited = false;

  try {
    if (result?.clauses && !result?.authRequired) {
      const parsed = Array.isArray(result.clauses)
        ? result.clauses
        : JSON.parse(result.clauses);

      clauses = parsed;
      isLimited = parsed.length === 2;
    }
  } catch (e) {
    console.error("Clause parsing error:", e);
    clauses = [];
  }

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
    <main className="min-h-screen bg-slate-50 px-4 py-8 sm:px-6">
      <div className="max-w-5xl mx-auto space-y-8">
        {/* Upload */}
        <div className="bg-white p-6 rounded-3xl shadow-sm border space-y-5">
          <UploadBox
            file={file}
            onFileChange={(selected) => {
              setFile(selected);
              setFileName(selected?.name || "");
              setResult(null);
              setOpenIndex(null);
            }}
          />

          <button
            onClick={handleUpload}
            disabled={!file}
            className="w-full rounded-xl bg-slate-900 px-6 py-3 text-sm font-semibold text-white hover:bg-slate-800"
          >
            {t.analyzeButton}
          </button>
        </div>

        {/* Result */}
        {result && !result.authRequired && (
          <div className="space-y-6">
            {/* Summary */}
            <div className="bg-white p-6 rounded-3xl border">
              <h2 className="text-xl font-semibold">{t.summary}</h2>
              <p className="mt-4">{result.summary}</p>
            </div>

            <RiskScore score={result.risk_score} language={language} />

            {/* Simplified */}
            <div className="bg-blue-50 p-6 rounded-3xl border">
              <h2 className="text-xl font-semibold">{t.simplified}</h2>
              <p className="mt-4">{result.simplified_version}</p>
            </div>

            {/* Clauses */}
            <div className="bg-white p-6 rounded-3xl border">
              <h2 className="text-xl font-semibold mb-4">{t.clauses}</h2>

              {isLimited && (
                <div className="mb-4 text-sm text-amber-700 bg-amber-50 border border-amber-200 rounded-xl p-3">
                  {t.limitedNotice}
                </div>
              )}

              <div className="space-y-4">
                {clauses.map((clause: any, index: number) => (
                  <div
                    key={index}
                    className="border rounded-2xl p-4"
                    onClick={() =>
                      setOpenIndex(openIndex === index ? null : index)
                    }
                  >
                    <div className="flex justify-between">
                      <span>
                        {t.clause} {index + 1}
                      </span>
                      <RiskBadge risk={clause.risk_level} language={language} />
                    </div>

                    <p className="mt-2 text-sm">
                      {clause.explanation_simple}
                    </p>

                    {openIndex === index && (
                      <div className="mt-3 text-sm">
                        <p>{clause.original_text}</p>
                        <p className="mt-2">
                          {t.recommendation}: {clause.recommendation}
                        </p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}