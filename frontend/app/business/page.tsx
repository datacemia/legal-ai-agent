"use client";

import { useEffect, useState } from "react";
import { analyzeBusinessFile } from "../../lib/api";
import { getSavedLocale, setSavedLocale } from "../../lib/i18n";

export default function BusinessPage() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [language, setLanguage] = useState("en");

  useEffect(() => {
    setLanguage(getSavedLocale());

    const handleLocaleChange = () => {
      setLanguage(getSavedLocale());
    };

    window.addEventListener("locale-change", handleLocaleChange);

    return () => {
      window.removeEventListener("locale-change", handleLocaleChange);
    };
  }, []);

  const handleAnalyze = async () => {
    if (!file) return;

    setLoading(true);
    setResult(null);
    setMessage("");

    try {
      const data = await analyzeBusinessFile(file, language);
      setResult(data);
    } catch (error: any) {
      setMessage(error?.message || "Failed to analyze business file.");
    } finally {
      setLoading(false);
    }
  };

  const score = Number(result?.business_health_score || 0);

  const getScoreMeta = (score: number) => {
    if (score >= 90) {
      return {
        label: "Excellent",
        color: "bg-green-600",
        text: "text-green-700",
        desc: "Your business is highly efficient with strong financial control.",
      };
    }

    if (score >= 70) {
      return {
        label: "Good",
        color: "bg-green-500",
        text: "text-green-600",
        desc: "Your business is healthy but can still be optimized.",
      };
    }

    if (score >= 50) {
      return {
        label: "Moderate",
        color: "bg-yellow-500",
        text: "text-yellow-600",
        desc: "There are inefficiencies or risks that need attention.",
      };
    }

    return {
      label: "Risky",
      color: "bg-red-500",
      text: "text-red-600",
      desc: "Your business has significant risks and needs urgent improvement.",
    };
  };

  const scoreMeta = getScoreMeta(score);

  const labels: any = {
    en: {
      title: "Business Decision Agent",
      analyze: "Analyze business data",
      loading: "Analyzing business data...",
    },
    fr: {
      title: "Agent décision business",
      analyze: "Analyser les données",
      loading: "Analyse en cours...",
    },
    ar: {
      title: "وكيل قرارات الأعمال",
      analyze: "تحليل البيانات",
      loading: "جاري التحليل...",
    },
  };

  const t = labels[language] || labels.en;

  return (
    <main
      dir={language === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-4 py-10"
    >
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold">{t.title}</h1>
          <p className="text-slate-500 mt-2">
            Upload business CSV data to detect trends, risks, opportunities, and
            get a clear action plan.
          </p>
        </div>

        <div className="bg-white p-6 rounded-2xl border space-y-4">
          <div className="rounded-xl bg-slate-50 border border-slate-200 p-4 text-sm text-slate-600 space-y-2">
            <p>
              <strong>How this agent works:</strong> Upload a CSV file with your
              business data such as revenue, expenses, dates, and categories.
            </p>
            <p>
              The agent analyzes your numbers, estimates profit and margin,
              detects risks, identifies opportunities, and gives practical next
              steps.
            </p>
            <p className="text-xs text-slate-500">
              Results are for business decision support only. Always verify
              important decisions with a qualified professional.
            </p>
          </div>

          <select
            value={language}
            onChange={(e) => {
              setLanguage(e.target.value);
              setSavedLocale(e.target.value);
              setResult(null);
              setMessage("");
            }}
            className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
          >
            <option value="en">English</option>
            <option value="fr">Français</option>
            <option value="ar">العربية</option>
          </select>

          <input
            type="file"
            accept=".csv,.xlsx"
            onChange={(e) => {
              setFile(e.target.files?.[0] || null);
              setResult(null);
              setMessage("");
            }}
            className="w-full rounded-xl border border-slate-300 px-4 py-3 text-sm"
          />

          <button
            onClick={handleAnalyze}
            disabled={!file || loading}
            className="w-full bg-slate-900 text-white py-3 rounded-xl disabled:bg-slate-400"
          >
            {loading ? t.loading : t.analyze}
          </button>

          {message && (
            <p className="text-sm text-red-700 bg-red-50 border border-red-200 rounded-xl px-4 py-3">
              {message}
            </p>
          )}
        </div>

        {result && (
          <div className="bg-white p-6 rounded-2xl border space-y-6">
            <h2 className="text-xl font-semibold">Results</h2>

            {result.error ? (
              <p className="text-red-600">{result.error}</p>
            ) : (
              <>
                <div>
                  <strong>Summary:</strong>
                  <p className="text-slate-600 mt-1">{result.summary}</p>
                </div>

                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <strong>Business health score:</strong>
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-semibold text-white ${scoreMeta.color}`}
                    >
                      {scoreMeta.label}
                    </span>
                  </div>

                  <div className="text-sm text-slate-600">
                    {score}/100 — {scoreMeta.desc}
                  </div>

                  <div className="h-3 bg-slate-200 rounded-full">
                    <div
                      className={`h-3 rounded-full ${scoreMeta.color}`}
                      style={{
                        width: `${Math.min(Math.max(score, 0), 100)}%`,
                      }}
                    />
                  </div>
                </div>

                <div className="grid gap-4 sm:grid-cols-2">
                  <div className="rounded-xl border bg-slate-50 p-4">
                    <p className="text-sm text-slate-500">Revenue estimate</p>
                    <p className="text-xl font-bold">
                      {result.metrics?.revenue_estimate}
                    </p>
                  </div>

                  <div className="rounded-xl border bg-slate-50 p-4">
                    <p className="text-sm text-slate-500">Expenses estimate</p>
                    <p className="text-xl font-bold">
                      {result.metrics?.expenses_estimate}
                    </p>
                  </div>

                  <div className="rounded-xl border bg-slate-50 p-4">
                    <p className="text-sm text-slate-500">Profit estimate</p>
                    <p className="text-xl font-bold">
                      {result.metrics?.profit_estimate}
                    </p>
                  </div>

                  <div className="rounded-xl border bg-slate-50 p-4">
                    <p className="text-sm text-slate-500">Profit margin</p>
                    <p className="text-xl font-bold">
                      {result.metrics?.profit_margin_percent}%
                    </p>
                  </div>
                </div>

                <div>
                  <strong>Key insights:</strong>
                  <ul className="list-disc ml-6 text-slate-700 mt-2">
                    {(result.key_insights || []).map(
                      (item: string, i: number) => (
                        <li key={i}>{item}</li>
                      )
                    )}
                  </ul>
                </div>

                <div>
                  <strong>Risks:</strong>
                  <ul className="list-disc ml-6 text-red-600 mt-2">
                    {(result.risks || []).map((item: string, i: number) => (
                      <li key={i}>{item}</li>
                    ))}
                  </ul>
                </div>

                <div>
                  <strong>Opportunities:</strong>
                  <ul className="list-disc ml-6 text-green-600 mt-2">
                    {(result.opportunities || []).map(
                      (item: string, i: number) => (
                        <li key={i}>{item}</li>
                      )
                    )}
                  </ul>
                </div>

                <div>
                  <strong>Action plan:</strong>
                  <ol className="list-decimal ml-6 text-blue-700 mt-2">
                    {(result.action_plan || []).map(
                      (item: string, i: number) => (
                        <li key={i}>{item}</li>
                      )
                    )}
                  </ol>
                </div>

                {result.disclaimer && (
                  <p className="text-xs text-slate-500 border-t pt-4">
                    {result.disclaimer}
                  </p>
                )}
              </>
            )}
          </div>
        )}
      </div>
    </main>
  );
}