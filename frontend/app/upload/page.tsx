"use client";

import { useState } from "react";
import { uploadDocument, runAnalysis } from "../../lib/api";
import RiskBadge from "../../components/RiskBadge";
import RiskScore from "../../components/RiskScore";
import UploadBox from "../../components/UploadBox";
import Navbar from "../../components/Navbar";

const labels: any = {
  // ⚠️ inchangé (je ne touche pas à tes labels)
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

      // ✅ FIX PAYMENT
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

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white border rounded-xl p-4">
            <p className="font-semibold">{t.summaryCard}</p>
            <p className="text-sm text-gray-500">{t.summaryCardText}</p>
          </div>

          <div className="bg-white border rounded-xl p-4">
            <p className="font-semibold">{t.privateCard}</p>
            <p className="text-sm text-gray-500">{t.privateCardText}</p>
          </div>

          <div className="bg-white border rounded-xl p-4">
            <p className="font-semibold">{t.multiCard}</p>
            <p className="text-sm text-gray-500">{t.multiCardText}</p>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow-sm border">
          <p className="mb-4 text-sm font-medium text-gray-600">
            {t.signupCta}
          </p>

          <p className="text-xs text-gray-400 text-center">
            {t.author}
          </p>

          <UploadBox
            file={file}
            onFileChange={(selected) => {
              setFile(selected);
              setFileName(selected?.name || "");
              setResult(null);
              setOpenIndex(null);
            }}
          />

          <div className="flex items-center gap-4 mt-5 flex-wrap">
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="border rounded-lg px-3 py-2"
            >
              <option value="en">English</option>
              <option value="fr">Français</option>
              <option value="ar">العربية</option>
            </select>

            <button
              onClick={handleUpload}
              disabled={!file}
              className="px-5 py-2 bg-black text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {t.analyzeButton}
            </button>
          </div>
        </div>

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

        {!result && (
          <div className="bg-white border rounded-2xl p-8 text-center text-gray-500">
            {t.empty}
          </div>
        )}

        {/* ✅ IMPORTANT FIX */}
        {result && !result.authRequired && !result.paymentRequired && (
          <>
            {/* ⚠️ ton UI existant inchangé */}
          </>
        )}
      </div>
    </main>
  );
}