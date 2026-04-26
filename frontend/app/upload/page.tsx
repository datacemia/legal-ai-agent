"use client";

import { useState } from "react";
import { uploadDocument, runAnalysis } from "../../lib/api";
import RiskBadge from "../../components/RiskBadge";
import RiskScore from "../../components/RiskScore";
import UploadBox from "../../components/UploadBox";
import Navbar from "../../components/Navbar";

const labels: any = {
  en: {
    pageTitle: "Analyze your contract",
    loading: "Analyzing your contract...",
    file: "File",
    summaryCard: "⚡ 60-second summary",
    summaryCardText: "Understand key points fast.",
    privateCard: "🔒 Private by design",
    privateCardText: "Your documents stay protected.",
    multiCard: "🌍 EN / FR / AR",
    multiCardText: "Multilingual contract analysis.",
    signupCta: "Free analysis available after signup",
    loginRequired: "Create an account to analyze your contract",
    author: "Created by Dr. Rachid Ejjami",
    analyzeButton: "Analyze Contract",
    empty: "Upload a contract to see the summary, risk score, simplified version, and clause analysis.",
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
      setResult({
        authRequired: true,
      });
      return;
    }

    try {
      setLoading(true);
      setResult(null);
      setOpenIndex(null);

      const doc = await uploadDocument(file);
      const analysis = await runAnalysis(doc.id, language);

      // ✅ MODIF 1
      if (analysis.detail?.includes("Payment required")) {
        setResult({ paymentRequired: true });
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

  if (loading) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center space-y-4">
          <div className="w-12 h-12 border-4 border-black border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p className="text-gray-600">{t.loading}</p>
          {fileName && (
            <p className="text-sm text-gray-500">
              {t.file}: {fileName}
            </p>
          )}
        </div>
      </main>
    );
  }

  return (
    <main
      dir={language === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-gray-50 p-6"
    >
      <div className="max-w-5xl mx-auto space-y-8">
        <h1 className="text-3xl font-bold text-gray-900">{t.pageTitle}</h1>

        {result?.authRequired && (
          <div className="bg-black text-white rounded-2xl p-6 text-center space-y-3">
            <p className="font-medium">{t.loginRequired}</p>

            <div className="flex justify-center gap-3">
              <a href="/login" className="underline">
                Login
              </a>
              <a href="/register" className="underline">
                Register
              </a>
            </div>
          </div>
        )}

        {/* ✅ MODIF 3 */}
        {result?.paymentRequired && (
          <div className="bg-yellow-50 text-yellow-800 border border-yellow-200 rounded-2xl p-6 text-center space-y-3">
            <p className="font-medium">
              You used your free analysis. Please buy one analysis credit.
            </p>

            <a
              href="/dashboard"
              className="inline-block bg-black text-white px-4 py-2 rounded-lg"
            >
              Go to dashboard
            </a>
          </div>
        )}

        {!result && (
          <div className="bg-white border rounded-2xl p-8 text-center text-gray-500">
            {t.empty}
          </div>
        )}

        {/* ✅ MODIF 2 */}
        {result && !result.authRequired && !result.paymentRequired && (
          <>
            <div className="bg-white p-6 rounded-2xl shadow-sm border">
              <div className="flex justify-between items-center">
                <h2 className="text-xl font-semibold">{t.summary}</h2>
                <RiskBadge risk={result.risk_level} language={language} />
              </div>

              <p className="mt-4 text-gray-700 whitespace-pre-line">
                {result.summary}
              </p>
            </div>

            <RiskScore score={result.risk_score} language={language} />

            <div className="bg-blue-50 p-6 rounded-2xl border border-blue-200">
              <h2 className="text-xl font-semibold text-blue-800">
                {t.simplified}
              </h2>

              <p className="mt-4 text-blue-900 whitespace-pre-line">
                {result.simplified_version}
              </p>
            </div>

            <div className="bg-white p-6 rounded-2xl shadow-sm border">
              <h2 className="text-xl font-semibold mb-4">{t.clauses}</h2>

              <div className="space-y-4">
                {clauses.map((clause: any, index: number) => (
                  <div
                    key={index}
                    className={`border rounded-xl p-4 cursor-pointer transition ${
                      clause.risk_level === "high"
                        ? "border-red-300 bg-red-50"
                        : clause.risk_level === "medium"
                        ? "border-yellow-300 bg-yellow-50"
                        : "border-gray-200 bg-white hover:bg-gray-50"
                    }`}
                    onClick={() =>
                      setOpenIndex(openIndex === index ? null : index)
                    }
                  >
                    <div className="flex justify-between items-center">
                      <div className="flex items-center gap-2">
                        <span className="font-semibold">
                          {t.clause} {index + 1}
                        </span>
                        <span className="text-xs text-gray-400">
                          {openIndex === index ? "▲" : "▼"}
                        </span>
                      </div>

                      <RiskBadge
                        risk={clause.risk_level}
                        language={language || "en"}
                      />
                    </div>

                    <p className="text-blue-700 text-sm mt-2">
                      {clause.explanation_simple}
                    </p>

                    {openIndex === index && (
                      <div className="mt-3 space-y-2">
                        <p className="text-sm text-gray-500">
                          {t.trigger}: {clause.trigger || t.none}
                        </p>

                        <p className="text-gray-800">
                          {clause.original_text}
                        </p>

                        <p className="text-gray-600 text-sm">
                          {t.recommendation}: {clause.recommendation}
                        </p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </>
        )}
      </div>
    </main>
  );
}