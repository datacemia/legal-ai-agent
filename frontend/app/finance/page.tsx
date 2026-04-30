"use client";

import { useEffect, useState } from "react";
import { analyzeFinanceStatement } from "../../lib/api";
import { getSavedLocale, setSavedLocale } from "../../lib/i18n";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const labels: any = {
  en: {
    title: "Personal Finance Coach",
    subtitle:
      "Upload your bank statement PDF to analyze spending, detect waste, and get saving strategies.",
    howTitle: "How this agent works:",
    how1:
      "Upload a bank statement PDF and the Personal Finance Coach will extract visible transactions, estimate income, spending, transfers, and categorize expenses.",
    how2:
      "The agent then detects possible waste, highlights financial risks, suggests saving strategies, and generates a financial score from 0 to 100.",
    disclaimer:
      "Results are informational only and do not replace professional financial advice.",
    analyze: "Analyze statement",
    analyzing: "Analyzing statement...",
    buyCredits: "Buy credits 💳",
    paymentMessage:
      "Stripe is not connected yet. Credit purchase will be available soon.",
    apiError: "Failed to connect to the finance analysis API.",
    results: "Results",
    summary: "Summary",
    currency: "Currency",
    unknown: "unknown",
    financialScore: "Financial score",
    totalSpending: "Total spending estimate",
    mainCategories: "Main categories",
    wasteDetected: "Waste detected",
    savingStrategies: "Saving strategies",
    riskNotes: "Risk notes",
  },
  fr: {
    title: "Coach financier personnel",
    subtitle:
      "Téléchargez votre relevé bancaire PDF pour analyser vos dépenses, détecter le gaspillage et obtenir des stratégies d’épargne.",
    howTitle: "Comment fonctionne cet agent :",
    how1:
      "Téléchargez un relevé bancaire PDF. Le coach financier extrait les transactions visibles, estime les revenus, les dépenses, les transferts et classe les dépenses par catégorie.",
    how2:
      "L’agent détecte ensuite les dépenses évitables, met en évidence les risques financiers, propose des stratégies d’épargne et génère un score financier de 0 à 100.",
    disclaimer:
      "Les résultats sont fournis à titre informatif uniquement et ne remplacent pas un conseil financier professionnel.",
    analyze: "Analyser le relevé",
    analyzing: "Analyse du relevé en cours...",
    buyCredits: "Acheter des crédits 💳",
    paymentMessage:
      "Stripe n’est pas encore connecté. L’achat de crédits sera bientôt disponible.",
    apiError: "Impossible de se connecter à l’API d’analyse financière.",
    results: "Résultats",
    summary: "Résumé",
    currency: "Devise",
    unknown: "inconnue",
    financialScore: "Score financier",
    totalSpending: "Estimation des dépenses totales",
    mainCategories: "Catégories principales",
    wasteDetected: "Dépenses évitables détectées",
    savingStrategies: "Stratégies d’épargne",
    riskNotes: "Notes de risque",
  },
  ar: {
    title: "وكيل الإدارة المالية الشخصية",
    subtitle:
      "ارفع كشف حسابك البنكي بصيغة PDF لتحليل المصاريف، كشف الهدر، والحصول على استراتيجيات ادخار.",
    howTitle: "كيف يعمل هذا الوكيل:",
    how1:
      "ارفع كشف حساب بنكي PDF وسيقوم وكيل الإدارة المالية باستخراج المعاملات الظاهرة، وتقدير الدخل، المصاريف، التحويلات، وتصنيف النفقات.",
    how2:
      "بعد ذلك يكتشف الوكيل النفقات التي يمكن تجنبها، يوضح المخاطر المالية، يقترح استراتيجيات ادخار، وينشئ نتيجة مالية من 0 إلى 100.",
    disclaimer:
      "النتائج معلوماتية فقط ولا تُعد بديلاً عن الاستشارة المالية المهنية.",
    analyze: "تحليل الكشف",
    analyzing: "جاري تحليل الكشف...",
    buyCredits: "شراء رصيد 💳",
    paymentMessage:
      "Stripe غير متصل حالياً. شراء الرصيد سيكون متاحاً قريباً.",
    apiError: "تعذر الاتصال بواجهة تحليل المالية.",
    results: "النتائج",
    summary: "الملخص",
    currency: "العملة",
    unknown: "غير معروفة",
    financialScore: "النتيجة المالية",
    totalSpending: "تقدير إجمالي المصاريف",
    mainCategories: "الفئات الرئيسية",
    wasteDetected: "الهدر المكتشف",
    savingStrategies: "استراتيجيات الادخار",
    riskNotes: "ملاحظات المخاطر",
  },
};

export default function FinancePage() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [paymentMessage, setPaymentMessage] = useState("");
  const [language, setLanguage] = useState("en");

  useEffect(() => {
    setLanguage(getSavedLocale());
  }, []);

  const t = labels[language] || labels.en;

  const COLORS = [
    "#22c55e",
    "#3b82f6",
    "#f59e0b",
    "#ef4444",
    "#8b5cf6",
    "#14b8a6",
    "#ec4899",
    "#64748b",
  ];

  const currencySymbol =
    result?.currency_detected === "USD"
      ? "$"
      : result?.currency_detected === "EUR"
      ? "€"
      : result?.currency_detected === "MAD"
      ? "MAD"
      : result?.currency_detected === "GBP"
      ? "£"
      : result?.currency_detected === "CAD"
      ? "CA$"
      : "";

  const formatMoney = (value: any) => {
    const amount = Number(value || 0);
    return currencySymbol ? `${currencySymbol} ${amount}` : `${amount}`;
  };

  const chartData = Object.entries(result?.main_categories || {})
    .map(([name, value]) => ({
      name,
      value: Number(value),
    }))
    .filter((item) => item.value > 0);

  const handleAnalyze = async () => {
    if (!file) return;

    setLoading(true);
    setResult(null);
    setPaymentMessage("");

    try {
      const data = await analyzeFinanceStatement(file, language);
      setResult(data);
    } catch (error) {
      console.error("Finance analysis error:", error);
      setResult({
        detail: t.apiError,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <main
      dir={language === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-4 py-10"
    >
      <div className="max-w-3xl mx-auto space-y-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold">{t.title}</h1>
          <p className="text-slate-500 mt-2">{t.subtitle}</p>
        </div>

        <div className="bg-white p-6 rounded-2xl border space-y-4">
          <div className="rounded-xl bg-slate-50 border border-slate-200 p-4 text-sm text-slate-600 space-y-2">
            <p>
              <strong>{t.howTitle}</strong> {t.how1}
            </p>
            <p>{t.how2}</p>
            <p className="text-xs text-slate-500">{t.disclaimer}</p>
          </div>

          <select
            value={language}
            onChange={(e) => {
              setLanguage(e.target.value);
              setSavedLocale(e.target.value);
              setResult(null);
              setPaymentMessage("");
            }}
            className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
          >
            <option value="en">English</option>
            <option value="fr">Français</option>
            <option value="ar">العربية</option>
          </select>

          <input
            type="file"
            accept=".pdf"
            onChange={(e) => {
              setFile(e.target.files?.[0] || null);
              setResult(null);
              setPaymentMessage("");
            }}
            className="w-full rounded-xl border border-slate-300 px-4 py-3 text-sm"
          />

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <button
              onClick={handleAnalyze}
              disabled={!file || loading}
              className="w-full bg-slate-900 text-white py-3 rounded-xl disabled:bg-slate-400"
            >
              {loading ? t.analyzing : t.analyze}
            </button>

            <button
              onClick={() => setPaymentMessage(t.paymentMessage)}
              className="w-full bg-green-600 text-white py-3 rounded-xl hover:bg-green-700 transition"
            >
              <span className="flex items-center justify-center gap-2">
                {t.buyCredits}
              </span>
            </button>
          </div>

          {paymentMessage && (
            <p className="text-sm text-amber-600 bg-amber-50 border border-amber-200 rounded-xl px-4 py-3">
              {paymentMessage}
            </p>
          )}
        </div>

        {result && (
          <div className="bg-white p-6 rounded-2xl border space-y-4">
            <h2 className="text-xl font-semibold">{t.results}</h2>

            {result.detail ? (
              <p className="text-red-600">{result.detail}</p>
            ) : (
              <>
                <p>
                  <strong>{t.summary}:</strong> {result.summary}
                </p>

                <p>
                  <strong>{t.currency}:</strong>{" "}
                  {result.currency_detected || t.unknown}
                </p>

                {result.financial_score !== undefined && (
                  <div>
                    <p>
                      <strong>{t.financialScore}:</strong>{" "}
                      {result.financial_score ?? "N/A"}/100
                    </p>

                    <div className="mt-4">
                      <div className="h-3 bg-slate-200 rounded-full">
                        <div
                          className={`h-3 rounded-full ${
                            result.financial_score >= 70
                              ? "bg-green-500"
                              : result.financial_score >= 50
                              ? "bg-yellow-500"
                              : "bg-red-500"
                          }`}
                          style={{
                            width: `${Math.min(
                              Math.max(result.financial_score || 0, 0),
                              100
                            )}%`,
                          }}
                        />
                      </div>
                    </div>
                  </div>
                )}

                <p>
                  <strong>{t.totalSpending}:</strong>{" "}
                  {formatMoney(result.total_spending_estimate)}
                </p>

                <div>
                  <strong>{t.mainCategories}:</strong>

                  {chartData.length > 0 && (
                    <>
                      <div className="h-64 mt-4">
                        <ResponsiveContainer>
                          <PieChart>
                            <Pie
                              data={chartData}
                              dataKey="value"
                              nameKey="name"
                              outerRadius={80}
                            >
                              {chartData.map((entry, index) => (
                                <Cell
                                  key={index}
                                  fill={COLORS[index % COLORS.length]}
                                />
                              ))}
                            </Pie>
                            <Tooltip
                              formatter={(value) => formatMoney(value)}
                            />
                          </PieChart>
                        </ResponsiveContainer>
                      </div>

                      <div className="mt-4 overflow-hidden rounded-xl border">
                        <table className="w-full text-sm">
                          <tbody>
                            {chartData.map((item, index) => (
                              <tr
                                key={item.name}
                                className="border-b last:border-b-0"
                              >
                                <td className="px-3 py-2">
                                  <div className="flex items-center gap-2">
                                    <span
                                      className="h-3 w-3 rounded-full shrink-0"
                                      style={{
                                        backgroundColor:
                                          COLORS[index % COLORS.length],
                                      }}
                                    />
                                    <span className="capitalize">
                                      {item.name}
                                    </span>
                                  </div>
                                </td>
                                <td className="px-3 py-2 text-right font-semibold whitespace-nowrap">
                                  {formatMoney(item.value)}
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </>
                  )}
                </div>

                <div>
                  <strong>{t.wasteDetected}:</strong>
                  <ul className="list-disc ml-6 text-red-600">
                    {(result.waste_detected || []).map(
                      (item: string, i: number) => (
                        <li key={i}>{item}</li>
                      )
                    )}
                  </ul>
                </div>

                <div>
                  <strong>{t.savingStrategies}:</strong>
                  <ul className="list-disc ml-6 text-green-600">
                    {(result.saving_strategies || []).map(
                      (item: string, i: number) => (
                        <li key={i}>{item}</li>
                      )
                    )}
                  </ul>
                </div>

                <div>
                  <strong>{t.riskNotes}:</strong>
                  <ul className="list-disc ml-6 text-amber-600">
                    {(result.risk_notes || []).map(
                      (item: string, i: number) => (
                        <li key={i}>{item}</li>
                      )
                    )}
                  </ul>
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