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

  // ✅ SAFE VERSION
  const clauses =
    result?.clauses && !result?.authRequired
      ? Array.isArray(result.clauses)
        ? result.clauses
        : JSON.parse(result.clauses)
      : [];

  if (loading) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center space-y-4">
          <div className="w-12 h-12 border-4 border-black border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p className="text-gray-600">{t.loading}</p>
          {fileName && <p className="text-sm text-gray-500">{t.file}: {fileName}</p>}
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

        {/* ... (tout le reste inchangé) */}

        {result && !result.authRequired && (
          <>
            {/* autres blocs */}

            <div className="bg-white p-6 rounded-2xl shadow-sm border">
              <h2 className="text-xl font-semibold mb-4">{t.clauses}</h2>

              {/* ✅ message si vide */}
              {clauses.length === 0 && (
                <p className="text-sm text-gray-500">
                  No clause analysis returned for this document.
                </p>
              )}

              <div className="space-y-4">
                {clauses.map((clause: any, index: number) => (
                  <div key={index}>
                    {/* ton rendering existant */}
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