"use client";

import { useEffect, useState } from "react";
import { uploadDocument, runAnalysis, createCheckoutSession } from "../../lib/api";
import { trackEvent } from "../../lib/track";
import { getSavedLocale, setSavedLocale } from "../../lib/i18n";
import RiskBadge from "../../components/RiskBadge";
import RiskScore from "../../components/RiskScore";
import UploadBox from "../../components/UploadBox";


const labels: any = {
  en: {
    pageTitle: "Analyze your contract",
    loading: "Analyzing your contract...",
    file: "File",
    signupCta: "Free analysis available after signup",
    loginRequired: "Create an account to analyze your contract",
    analyzeButton: "Analyze Contract",
    buyCredit: "Buy credit",
    heroTitle: "Analyze your contracts in seconds",
    heroDesc:
      "Upload your document to detect risky clauses, identify key obligations, and get clear, actionable recommendations before you sign.",
    whatYouGet: "What you get",
    whatYouGetItems: [
      "Risky clauses detection",
      "Key obligations summary",
      "Potential legal issues explained",
      "Clear recommendations",
    ],
    howItWorks: "How it works",
    howItWorksItems: [
      "Upload your contract",
      "AI analyzes the content",
      "Get a structured report instantly",
    ],
    summary: "Summary",
    simplified: "Simplified Version",
    clauses: "Clauses Analysis",
    clause: "Clause",
    recommendation: "Recommendation",
    limitedNotice:
      "Only 2 clauses are displayed in the free version. Upgrade to unlock full clause analysis.",
  },
  fr: {
    pageTitle: "Analyser votre contrat",
    loading: "Analyse de votre contrat en cours...",
    file: "Fichier",
    signupCta: "Analyse gratuite disponible après inscription",
    loginRequired: "Créez un compte pour analyser votre contrat",
    analyzeButton: "Analyser le contrat",
    buyCredit: "Acheter un crédit",
    heroTitle: "Analysez vos contrats en quelques secondes",
    heroDesc:
      "Téléchargez votre document pour détecter les clauses risquées, identifier les obligations clés et obtenir des recommandations claires avant de signer.",
    whatYouGet: "Ce que vous obtenez",
    whatYouGetItems: [
      "Détection des clauses à risque",
      "Résumé des obligations clés",
      "Explication des risques juridiques potentiels",
      "Recommandations claires",
    ],
    howItWorks: "Comment ça marche",
    howItWorksItems: [
      "Téléchargez votre contrat",
      "L’IA analyse le contenu",
      "Recevez instantanément un rapport structuré",
    ],
    summary: "Résumé",
    simplified: "Version simplifiée",
    clauses: "Analyse des clauses",
    clause: "Clause",
    recommendation: "Recommandation",
    limitedNotice:
      "Seules 2 clauses sont affichées dans la version gratuite. Passez à la version complète pour débloquer toute l’analyse.",
  },
  ar: {
    pageTitle: "تحليل العقد",
    loading: "جاري تحليل العقد...",
    file: "الملف",
    signupCta: "تحليل مجاني متاح بعد إنشاء الحساب",
    loginRequired: "أنشئ حساباً لتحليل عقدك",
    analyzeButton: "تحليل العقد",
    buyCredit: "شراء رصيد",
    heroTitle: "حلل عقودك في ثوانٍ",
    heroDesc:
      "ارفع مستندك لاكتشاف البنود الخطرة، وتحديد الالتزامات الأساسية، والحصول على توصيات واضحة قبل التوقيع.",
    whatYouGet: "ماذا ستحصل عليه",
    whatYouGetItems: [
      "اكتشاف البنود الخطرة",
      "ملخص الالتزامات الأساسية",
      "شرح المخاطر القانونية المحتملة",
      "توصيات واضحة",
    ],
    howItWorks: "كيف يعمل",
    howItWorksItems: [
      "ارفع العقد",
      "يقوم الذكاء الاصطناعي بتحليل المحتوى",
      "احصل على تقرير منظم فوراً",
    ],
    summary: "الملخص",
    simplified: "نسخة مبسطة",
    clauses: "تحليل البنود",
    clause: "بند",
    recommendation: "توصية",
    limitedNotice:
      "يتم عرض بندين فقط في النسخة المجانية. قم بالترقية لفتح التحليل الكامل للبنود.",
  },
};

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [fileName, setFileName] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [language, setLanguage] = useState("en");
  const [openIndex, setOpenIndex] = useState<number | null>(null);
  const [message, setMessage] = useState("");

  useEffect(() => {
    setLanguage(getSavedLocale());
  }, []);

  const t = labels[language] || labels.en;

  const handleBuyCredit = async () => {
    const token = localStorage.getItem("token");

    if (!token) {
      window.location.href = "/register";
      return;
    }

    const data = await createCheckoutSession();

    if (data.checkout_url) {
      window.location.href = data.checkout_url;
      return;
    }

    setMessage(data.detail || "Payment is not configured yet.");
  };

  const handleUpload = async () => {
    if (!file) return;

    const token = localStorage.getItem("token");

    if (!token) {
      window.location.href = "/register";
      return;
    }

    trackEvent("upload_document");

    try {
      setLoading(true);
      setResult(null);
      setMessage("");
      setOpenIndex(null);

      const doc = await uploadDocument(file);

      if (!doc || !doc.id) {
        throw new Error("Upload failed");
      }

      const analysis = await runAnalysis(doc.id, language);

      if (analysis.detail?.includes("Payment required")) {
        setMessage("You used your free analysis. Please buy one analysis credit.");
        window.location.href = "/pricing";
        return;
      }

      setResult(analysis);
    } catch (err: any) {
      setMessage(
        err?.response?.data?.detail ||
          "Invalid file. Only PDF or DOCX allowed."
      );
      return;
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
    <main
      dir={language === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-4 py-8 sm:px-6"
    >
      <div className="max-w-5xl mx-auto space-y-8">

        <div className="max-w-3xl mx-auto text-center">
          <h1 className="text-3xl font-semibold tracking-tight text-slate-900 sm:text-4xl">
            {t.heroTitle}
          </h1>

          <p className="mt-4 text-base leading-7 text-slate-600">
            {t.heroDesc}
          </p>
        </div>

        <div className="bg-white p-6 rounded-3xl shadow-sm border space-y-5">
          <UploadBox
            file={file}
            onFileChange={(selected) => {
              setFile(selected);
              setFileName(selected?.name || "");
              setResult(null);
              setMessage("");
              setOpenIndex(null);
            }}
          />

          <select
            value={language}
            onChange={(e) => {
              setLanguage(e.target.value);
              setSavedLocale(e.target.value);
              setResult(null);
            }}
            className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
          >
            <option value="en">English</option>
            <option value="fr">Français</option>
            <option value="ar">العربية</option>
          </select>

          <button
            onClick={handleUpload}
            disabled={!file}
            className="w-full rounded-xl bg-slate-900 px-6 py-3 text-sm font-semibold text-white hover:bg-slate-800 disabled:bg-slate-400"
          >
            {t.analyzeButton}
          </button>

          <button
            onClick={handleBuyCredit}
            className="w-full rounded-xl bg-green-600 px-6 py-3 text-sm font-semibold text-white hover:bg-green-700"
          >
            {t.buyCredit}
          </button>

          {message && (
            <div className="bg-red-50 text-red-700 border border-red-200 text-sm p-3 rounded-xl text-center">
              {message}
            </div>
          )}
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          <div className="bg-white p-6 rounded-3xl shadow-sm border">
            <h2 className="text-lg font-semibold text-slate-900">
              {t.whatYouGet}
            </h2>

            <ul className="mt-4 space-y-3 text-sm text-slate-600">
              {t.whatYouGetItems.map((item: string, index: number) => (
                <li key={index}>• {item}</li>
              ))}
            </ul>
          </div>

          <div className="bg-white p-6 rounded-3xl shadow-sm border">
            <h2 className="text-lg font-semibold text-slate-900">
              {t.howItWorks}
            </h2>

            <ol className="mt-4 space-y-3 text-sm text-slate-600">
              {t.howItWorksItems.map((item: string, index: number) => (
                <li key={index}>
                  {index + 1}. {item}
                </li>
              ))}
            </ol>
          </div>
        </div>

        {result && !result.authRequired && (
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-3xl border">
              <h2 className="text-xl font-semibold">{t.summary}</h2>
              <p className="mt-4">{result.summary}</p>
            </div>

            <RiskScore score={result.risk_score} language={language} />

            <div className="bg-blue-50 p-6 rounded-3xl border">
              <h2 className="text-xl font-semibold">{t.simplified}</h2>
              <p className="mt-4">{result.simplified_version}</p>
            </div>

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
                    className="border rounded-2xl p-4 cursor-pointer"
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
                      <div className="mt-3 text-sm text-slate-600">
                        <p>
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