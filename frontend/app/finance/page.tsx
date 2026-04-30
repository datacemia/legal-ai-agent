"use client";

import { useState } from "react";
import { analyzeFinanceStatement } from "../../lib/api";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function FinancePage() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [paymentMessage, setPaymentMessage] = useState("");

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
      const data = await analyzeFinanceStatement(file);
      setResult(data);
    } catch (error) {
      console.error("Finance analysis error:", error);
      setResult({
        detail: "Failed to connect to the finance analysis API.",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-10">
      <div className="max-w-3xl mx-auto space-y-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold">Personal Finance Coach</h1>
          <p className="text-slate-500 mt-2">
            Upload your bank statement PDF to analyze spending, detect waste,
            and get saving strategies.
          </p>
        </div>

        <div className="bg-white p-6 rounded-2xl border space-y-4">
          <div className="rounded-xl bg-slate-50 border border-slate-200 p-4 text-sm text-slate-600 space-y-2">
            <p>
              <strong>How this agent works:</strong> Upload a bank statement PDF
              and the Personal Finance Coach will extract visible transactions,
              estimate income, spending, transfers, and categorize expenses.
            </p>
            <p>
              The agent then detects possible waste, highlights financial risks,
              suggests saving strategies, and generates a financial score from 0
              to 100.
            </p>
            <p className="text-xs text-slate-500">
              Results are informational only and do not replace professional
              financial advice.
            </p>
          </div>

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
              {loading ? "Analyzing statement..." : "Analyze statement"}
            </button>

            <button
              onClick={() =>
                setPaymentMessage(
                  "Stripe is not connected yet. Credit purchase will be available soon."
                )
              }
              className="w-full bg-green-600 text-white py-3 rounded-xl hover:bg-green-700 transition"
            >
              <span className="flex items-center justify-center gap-2">
                Buy credits 💳
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
            <h2 className="text-xl font-semibold">Results</h2>

            {result.detail ? (
              <p className="text-red-600">{result.detail}</p>
            ) : (
              <>
                <p>
                  <strong>Summary:</strong> {result.summary}
                </p>

                <p>
                  <strong>Currency:</strong>{" "}
                  {result.currency_detected || "unknown"}
                </p>

                {result.financial_score !== undefined && (
                  <div>
                    <p>
                      <strong>Financial score:</strong>{" "}
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
                  <strong>Total spending estimate:</strong>{" "}
                  {formatMoney(result.total_spending_estimate)}
                </p>

                <div>
                  <strong>Main categories:</strong>

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
                  <strong>Waste detected:</strong>
                  <ul className="list-disc ml-6 text-red-600">
                    {(result.waste_detected || []).map(
                      (item: string, i: number) => (
                        <li key={i}>{item}</li>
                      )
                    )}
                  </ul>
                </div>

                <div>
                  <strong>Saving strategies:</strong>
                  <ul className="list-disc ml-6 text-green-600">
                    {(result.saving_strategies || []).map(
                      (item: string, i: number) => (
                        <li key={i}>{item}</li>
                      )
                    )}
                  </ul>
                </div>

                <div>
                  <strong>Risk notes:</strong>
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