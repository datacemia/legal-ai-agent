"use client";

import { useState } from "react";
import { uploadDocument, runAnalysis } from "../../lib/api";
import RiskBadge from "../../components/RiskBadge";
import RiskScore from "../../components/RiskScore";
import UploadBox from "../../components/UploadBox";

const labels: any = { /* 🔥 garde ton labels EXACT (inchangé) */ };

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
  } catch {
    clauses = [];
  }

  // 🔥 LOADING UX IMPROVED
  if (loading) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="bg-white p-8 rounded-2xl shadow border text-center space-y-4">
          <div className="w-10 h-10 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p className="font-medium">{t.loading}</p>
          {fileName && <p className="text-sm text-gray-500">{fileName}</p>}
        </div>
      </main>
    );
  }

  return (
    <main
      dir={language === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-4 py-8"
    >
      <div className="max-w-4xl mx-auto space-y-8">

        {/* 🔥 HEADER */}
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-bold">{t.pageTitle}</h1>
          <p className="text-gray-500">{t.signupCta}</p>
        </div>

        {/* 🔥 BENEFITS */}
        <div className="grid gap-4 md:grid-cols-3">
          {[t.summaryCard, t.privateCard, t.multiCard].map((title, i) => (
            <div key={i} className="bg-white p-4 rounded-xl border text-center">
              <p className="font-semibold">{title}</p>
            </div>
          ))}
        </div>

        {/* 🔥 UPLOAD CARD */}
        <div className="bg-white p-6 rounded-2xl border shadow-sm space-y-5">
          <UploadBox
            file={file}
            onFileChange={(f) => {
              setFile(f);
              setFileName(f?.name || "");
              setResult(null);
              setOpenIndex(null);
            }}
          />

          <div className="flex flex-wrap gap-4 justify-between items-center">
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="border px-3 py-2 rounded-lg"
            >
              <option value="en">English</option>
              <option value="fr">Français</option>
              <option value="ar">العربية</option>
            </select>

            <button
              onClick={handleUpload}
              disabled={!file}
              className="px-6 py-2 rounded-lg bg-blue-600 text-white font-semibold hover:bg-blue-700 disabled:opacity-40"
            >
              {t.analyzeButton}
            </button>
          </div>
        </div>

        {/* 🔥 AUTH BLOCK */}
        {result?.authRequired && (
          <div className="bg-black text-white p-6 rounded-2xl text-center space-y-3">
            <p>{t.loginRequired}</p>
            <div className="flex justify-center gap-4">
              <a href="/login" className="underline">Login</a>
              <a href="/register" className="underline">Register</a>
            </div>
          </div>
        )}

        {/* 🔥 EMPTY STATE */}
        {!result && (
          <div className="bg-white border rounded-2xl p-8 text-center text-gray-500">
            {t.empty}
          </div>
        )}

        {/* 🔥 RESULTS */}
        {result && !result.authRequired && (
          <div className="space-y-6">

            {/* SUMMARY */}
            <div className="bg-white p-6 rounded-2xl border shadow-sm">
              <div className="flex justify-between items-center">
                <h2 className="font-semibold">{t.summary}</h2>
                <RiskBadge risk={result.risk_level} language={language} />
              </div>
              <p className="mt-3 whitespace-pre-line">{result.summary}</p>
            </div>

            <RiskScore score={result.risk_score} language={language} />

            {/* SIMPLIFIED */}
            <div className="bg-blue-50 p-6 rounded-2xl border">
              <h2 className="font-semibold">{t.simplified}</h2>
              <p className="mt-3 whitespace-pre-line">
                {result.simplified_version}
              </p>
            </div>

            {/* CLAUSES */}
            <div className="bg-white p-6 rounded-2xl border shadow-sm">
              <h2 className="font-semibold mb-4">{t.clauses}</h2>

              {clauses.map((clause, i) => (
                <div
                  key={i}
                  onClick={() =>
                    setOpenIndex(openIndex === i ? null : i)
                  }
                  className="border rounded-xl p-4 mb-3 cursor-pointer hover:bg-gray-50"
                >
                  <div className="flex justify-between">
                    <span>{t.clause} {i + 1}</span>
                    <RiskBadge risk={clause.risk_level} language={language} />
                  </div>

                  {openIndex === i && (
                    <div className="mt-3 text-sm space-y-2">
                      <p>{clause.original_text}</p>
                      <p className="text-gray-500">
                        {t.recommendation}: {clause.recommendation}
                      </p>
                    </div>
                  )}
                </div>
              ))}
            </div>

          </div>
        )}
      </div>
    </main>
  );
}