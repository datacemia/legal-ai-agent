"use client";

import { useEffect, useState } from "react";

import { getBusinessHistory } from "../../../lib/api";
import { getSavedLocale } from "../../../lib/i18n";

type Locale = "en" | "fr" | "ar";



const normalizeBackendText = (
  value: any,
  language: Locale = "en"
) => {
  if (value === null || value === undefined || value === "") {
    return "-";
  }

  let text = String(value);

  const dictionaries: Record<Locale, Record<string, string>> = {
    en: {},
    fr: {
      "up": "hausse",
      "down": "baisse",
      "stable": "stable",
      "low": "faible",
      "medium": "moyen",
      "high": "élevé",
      "critical": "critique",
      "healthy": "sain",
      "positive": "positif",
      "negative": "négatif",
      "normal": "normal",
      "general": "général",
      "saas": "SaaS / abonnement",
      "Healthy profit margin.": "Marge bénéficiaire saine.",
      "Healthy growth.": "Croissance saine.",
      "Positive cashflow.": "Cashflow positif.",
      "Healthy ROAS.": "ROAS sain.",
      "Healthy CAC efficiency.": "Efficacité CAC saine.",
      "Critical churn level.": "Niveau de churn critique.",
      "Payroll": "Masse salariale",
      "Marketing": "Marketing",
      "Software": "Logiciels",
      "Customers": "Clients",
      "New customers": "Nouveaux clients",
      "Churned customers": "Clients perdus",
      "Revenue/customer": "Revenu/client",
      "Orders": "Commandes",
      "Ad spend": "Dépenses publicitaires",
      "Profit Margin": "Marge bénéficiaire",
      "Growth": "Croissance",
      "Cashflow": "Cashflow",
      "Churn": "Churn",
      "Roas": "ROAS",
      "Cac Efficiency": "Efficacité CAC",
      "Data Quality": "Qualité des données",
      "Revenue": "Revenus",
      "Expenses": "Dépenses",
      "Profit": "Profit",
      "Profit Margin Percent": "Marge bénéficiaire",
      "Growth Rate Percent": "Taux de croissance"
    },
    ar: {
      "up": "صاعد",
      "down": "هابط",
      "stable": "مستقر",
      "low": "منخفض",
      "medium": "متوسط",
      "high": "مرتفع",
      "critical": "حرج",
      "healthy": "صحي",
      "positive": "إيجابي",
      "negative": "سلبي",
      "normal": "طبيعي",
      "general": "عام",
      "saas": "SaaS / اشتراك",
      "Healthy profit margin.": "هامش ربح صحي.",
      "Healthy growth.": "نمو صحي.",
      "Positive cashflow.": "تدفق نقدي إيجابي.",
      "Healthy ROAS.": "عائد إنفاق إعلاني صحي.",
      "Healthy CAC efficiency.": "كفاءة صحية لتكلفة اكتساب العميل.",
      "Critical churn level.": "مستوى فقدان العملاء حرج.",
      "Payroll": "الرواتب",
      "Marketing": "التسويق",
      "Software": "البرمجيات",
      "Customers": "العملاء",
      "New customers": "العملاء الجدد",
      "Churned customers": "العملاء المفقودون",
      "Revenue/customer": "الإيراد لكل عميل",
      "Orders": "الطلبات",
      "Ad spend": "الإنفاق الإعلاني",
      "Profit Margin": "هامش الربح",
      "Growth": "النمو",
      "Cashflow": "التدفق النقدي",
      "Churn": "فقدان العملاء",
      "Roas": "عائد الإنفاق الإعلاني",
      "Cac Efficiency": "كفاءة تكلفة الاكتساب",
      "Data Quality": "جودة البيانات",
      "Revenue": "الإيرادات",
      "Expenses": "المصاريف",
      "Profit": "الأرباح",
      "Profit Margin Percent": "هامش الربح",
      "Growth Rate Percent": "معدل النمو"
    },
  };

  const dictionary = dictionaries[language] || {};

  Object.entries(dictionary).forEach(([source, target]) => {
    const escaped = source.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    text = text.replace(
      new RegExp(`(^|[^A-Za-z])${escaped}(?=$|[^A-Za-z])`, "gi"),
      (_match, prefix) => `${prefix}${target}`
    );
  });

  if (language === "fr") {
    text = text
      .replaceAll("cashffaible", "cashflow")
      .replaceAll("cashflow est Positif", "cashflow est positif")
      .replaceAll("score de santé backend est de 73/100 (Sain)", "score de santé backend est de 73/100 (sain)")
      .replaceAll("situation actuelle comme Critique", "situation actuelle comme critique")
      .replaceAll("Volatilité moyen", "Volatilité moyenne")
      .replaceAll("Risque cashflow faible", "Risque de cashflow faible");
  }

  return text;
};

const localizedKeyLabel = (
  key: string,
  language: Locale = "en"
) => {
  const normalized = String(key || "")
    .replaceAll("_", " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());

  return normalizeBackendText(normalized, language);
};

const safeGetLocalStorage = (
  key: string,
  fallback = ""
) => {
  if (typeof window === "undefined") {
    return fallback;
  }

  return localStorage.getItem(key) || fallback;
};

const downloadBlob = async (
  response: Response,
  fallbackName: string
) => {
  const blob = await response.blob();
  const disposition = response.headers.get("Content-Disposition") || "";
  const match = disposition.match(/filename="?([^";]+)"?/i);
  const fileName = match?.[1] || fallbackName;
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement("a");

  link.href = url;
  link.download = fileName;
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
};

export default function BusinessHistoryPage() {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [exporting, setExporting] = useState<string | null>(null);
  const [exportMessage, setExportMessage] = useState("");
  const [language, setLanguage] = useState("en");

  useEffect(() => {
    setLanguage(getSavedLocale());

    async function fetchData() {
      try {
        const res = await getBusinessHistory();

        setData(Array.isArray(res) ? res : []);
      } catch (error) {
        console.error("Business history load failed:", error);
        setData([]);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  const parseResult = (value: any) => {
    try {
      return typeof value === "string"
        ? JSON.parse(value)
        : value || {};
    } catch {
      return {};
    }
  };

  const getLocale = (language: string): Locale => {
    if (language === "fr") return "fr";
    if (language === "ar") return "ar";
    return "en";
  };

  const locale = getLocale(language);

  const handleExport = async (
    analysisId: number,
    kind: "pdf" | "pptx"
  ) => {
    const exportKey = `${analysisId}-${kind}`;

    setExporting(exportKey);
    setExportMessage("");

    try {
      const token = safeGetLocalStorage("token");

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/business/export/${kind}/${analysisId}`,
        {
          method: "POST",
          headers: {
            ...(token
              ? {
                  Authorization: `Bearer ${token}`,
                }
              : {}),
          },
        }
      );

      if (!response.ok) {
        let detail = "Failed to export report.";

        try {
          const errorData = await response.json();
          detail = errorData?.detail || errorData?.error || detail;
        } catch {
          // Export endpoints may return file responses.
        }

        setExportMessage(detail);
        return;
      }

      await downloadBlob(
        response,
        `business_analysis_${analysisId}.${kind}`
      );

      setExportMessage("Report exported successfully.");
    } catch (error: any) {
      setExportMessage(error?.message || "Failed to export report.");
    } finally {
      setExporting(null);
    }
  };

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-10">
      <div className="max-w-6xl mx-auto space-y-6">
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-bold">
            Business Analysis History
          </h1>

          <p className="text-slate-500">
            Your previous AI CFO business analyses
          </p>
        </div>

        {exportMessage && (
          <div
            className={`rounded-xl border px-4 py-3 text-center text-sm font-semibold ${
              exportMessage.includes("success")
                ? "border-emerald-200 bg-emerald-50 text-emerald-700"
                : "border-red-200 bg-red-50 text-red-700"
            }`}
          >
            {exportMessage}
          </div>
        )}

        {loading ? (
          <p className="text-center text-slate-500">
            Loading...
          </p>
        ) : data.length === 0 ? (
          <p className="text-center text-slate-500">
            No business analyses yet
          </p>
        ) : (
          <div className="grid gap-5">
            {data.map((item) => {
              const result = parseResult(item.result);

              return (
                <div
                  key={item.id}
                  className="bg-white border rounded-2xl p-6 shadow-sm"
                >
                  {/* Header */}
                  <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-4">
                    <div>
                      <h2 className="text-lg font-semibold">
                        {item.file_name}
                      </h2>

                      <p className="text-sm text-slate-500">
                        {new Date(
                          item.created_at
                        ).toLocaleDateString()}
                      </p>
                    </div>

                    <div className="flex items-center gap-3 flex-wrap">
                      <div className="px-3 py-1 rounded-full bg-slate-100 text-sm">
                        Model:{" "}
                        <strong>
                          {normalizeBackendText(result.business_model || "general", locale)}
                        </strong>
                      </div>

                      <div className="px-3 py-1 rounded-full bg-blue-50 text-blue-700 text-sm">
                        Score:{" "}
                        <strong>
                          {result.business_health_score ?? 0}/100
                        </strong>
                      </div>
                    </div>
                  </div>

                  {/* Executive Summary */}
                  <div className="mb-5">
                    <h3 className="font-medium mb-2">
                      Executive Summary
                    </h3>

                    <p className="text-sm text-slate-600 leading-relaxed">
                      {normalizeBackendText(result.executive_summary ||
                        "No executive summary available.", locale)}
                    </p>
                  </div>

                  {/* KPI Cards */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-5">
                    <div className="rounded-xl border bg-slate-50 px-4 py-3">
                      <p className="text-xs text-slate-500 mb-1">
                        Revenue
                      </p>

                      <p className="font-semibold">
                        {result.kpis?.revenue ?? "-"}
                      </p>
                    </div>

                    <div className="rounded-xl border bg-slate-50 px-4 py-3">
                      <p className="text-xs text-slate-500 mb-1">
                        Expenses
                      </p>

                      <p className="font-semibold">
                        {result.kpis?.expenses ?? "-"}
                      </p>
                    </div>

                    <div className="rounded-xl border bg-slate-50 px-4 py-3">
                      <p className="text-xs text-slate-500 mb-1">
                        Profit
                      </p>

                      <p className="font-semibold">
                        {result.kpis?.profit ?? "-"}
                      </p>
                    </div>

                    <div className="rounded-xl border bg-slate-50 px-4 py-3">
                      <p className="text-xs text-slate-500 mb-1">
                        Margin
                      </p>

                      <p className="font-semibold">
                        {result.kpis?.profit_margin_percent ?? 0}%
                      </p>
                    </div>
                  </div>

                  {/* Most Important Decision */}
                  {result.smart_insights?.most_important_decision && (
                    <div className="rounded-2xl border bg-amber-50 border-amber-200 p-4 mb-5">
                      <div className="flex items-start justify-between gap-4">
                        <div className="space-y-2">
                          <p className="text-xs uppercase tracking-wide text-amber-700 font-semibold">
                            Most Important Decision
                          </p>

                          <h3 className="font-semibold text-lg">
                            {
                              result.smart_insights
                                .most_important_decision.title
                            }
                          </h3>

                          <p className="text-sm text-slate-700">
                            {
                              result.smart_insights
                                .most_important_decision.decision
                            }
                          </p>

                          <p className="text-xs text-slate-500">
                            {
                              result.smart_insights
                                .most_important_decision.why
                            }
                          </p>
                        </div>

                        <div className="text-right text-sm">
                          <p className="text-slate-500">
                            Impact
                          </p>

                          <strong>
                            {
                              result.smart_insights
                                .most_important_decision.impact
                            }
                          </strong>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Key Insights */}
                  {Array.isArray(
                    result.smart_insights?.key_insights
                  ) &&
                    result.smart_insights.key_insights.length > 0 && (
                      <div className="mb-5">
                        <h3 className="font-medium mb-3">
                          Key Insights
                        </h3>

                        <ul className="space-y-2">
                          {result.smart_insights.key_insights.map(
                            (insight: string, index: number) => (
                              <li
                                key={index}
                                className="text-sm text-slate-600 flex gap-2"
                              >
                                <span>•</span>
                                <span>{normalizeBackendText(insight, locale)}</span>
                              </li>
                            )
                          )}
                        </ul>
                      </div>
                    )}

                  {/* Footer */}
                  <div className="pt-4 border-t flex justify-between items-center">
                    <div className="text-xs text-slate-400">
                      Confidence:{" "}
                      {normalizeBackendText(result.confidence_level || "low", locale)}
                    </div>

                    <div className="flex flex-wrap items-center gap-2">
                      <button
                        type="button"
                        onClick={() => handleExport(item.id, "pdf")}
                        disabled={exporting !== null}
                        className="rounded-full bg-slate-950 px-3 py-2 text-xs font-bold text-white transition hover:bg-slate-800 disabled:bg-slate-400"
                      >
                        {exporting === `${item.id}-pdf`
                          ? "Generating PDF..."
                          : "Export PDF"}
                      </button>

                      <button
                        type="button"
                        onClick={() => handleExport(item.id, "pptx")}
                        disabled={exporting !== null}
                        className="rounded-full border border-slate-200 bg-white px-3 py-2 text-xs font-bold text-slate-800 transition hover:bg-slate-50 disabled:text-slate-400"
                      >
                        {exporting === `${item.id}-pptx`
                          ? "Generating PPTX..."
                          : "Export PPTX"}
                      </button>

                      <a
                        href="/business"
                        className="text-sm text-blue-600 hover:underline"
                      >
                        Analyze another file
                      </a>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </main>
  );
}
