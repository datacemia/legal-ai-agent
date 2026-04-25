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
  fr: {
    pageTitle: "Analyser votre contrat",
    loading: "Analyse de votre contrat...",
    file: "Fichier",
    summaryCard: "⚡ Résumé en 60 secondes",
    summaryCardText: "Comprenez rapidement les points clés.",
    privateCard: "🔒 Confidentialité intégrée",
    privateCardText: "Vos documents restent protégés.",
    multiCard: "🌍 EN / FR / AR",
    multiCardText: "Analyse multilingue des contrats.",
    signupCta: "Analyse gratuite disponible après inscription",
    loginRequired: "Créez un compte pour analyser votre contrat",
    author: "Créé par Dr. Rachid Ejjami",
    analyzeButton: "Analyser le contrat",
    empty: "Téléversez un contrat pour voir le résumé, le score de risque, la version simplifiée et l’analyse des clauses.",
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
    summaryCard: "⚡ ملخص خلال 60 ثانية",
    summaryCardText: "افهم النقاط الأساسية بسرعة.",
    privateCard: "🔒 خصوصية مدمجة",
    privateCardText: "تبقى مستنداتك محمية.",
    multiCard: "🌍 EN / FR / AR",
    multiCardText: "تحليل عقود متعدد اللغات.",
    signupCta: "التحليل المجاني متاح بعد التسجيل",
    loginRequired: "أنشئ حسابًا لتحليل عقدك",
    author: "تم تطويره بواسطة د. رشيد الجامعي",
    analyzeButton: "تحليل العقد",
    empty: "قم برفع عقد لعرض الملخص ودرجة المخاطر والنسخة المبسطة وتحليل البنود.",
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

  const clauses =
    result?.clauses && !result?.authRequired ? JSON.parse(result.clauses) : [];

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

        {result && !result.authRequired && (
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