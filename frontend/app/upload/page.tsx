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
      setResult({ authRequired: true });
      return;
    }

    try {
      setLoading(true);
      setResult(null);
      setOpenIndex(null);

      const doc = await uploadDocument(file);
      const analysis = await runAnalysis(doc.id, language);

      // ✅ FIX PAYMENT (IMPORTANT)
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

        {/* ✅ PAYMENT MESSAGE */}
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

        {result?.authRequired && (
          <div className="bg-black text-white rounded-2xl p-6 text-center space-y-3">
            <p className="font-medium">{t.loginRequired}</p>
            <div className="flex justify-center gap-3">
              <a href="/login" className="underline">Login</a>
              <a href="/register" className="underline">Register</a>
            </div>
          </div>
        )}

        {!result && (
          <div className="bg-white border rounded-2xl p-8 text-center text-gray-500">
            {t.empty}
          </div>
        )}

        {/* ✅ SAFE RENDER */}
        {result && !result.authRequired && !result.paymentRequired && (
          <>
            {/* TON UI EXISTANT ICI (inchangé) */}
          </>
        )}
      </div>
    </main>
  );
}