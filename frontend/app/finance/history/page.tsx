"use client";

import { useEffect, useState } from "react";
import { getFinanceHistory } from "../../../lib/api";

export default function FinanceHistoryPage() {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const getCurrencySymbol = (currency: string) => {
    switch (currency) {
      case "USD":
        return "$";
      case "EUR":
        return "€";
      case "MAD":
        return "MAD";
      case "GBP":
        return "£";
      case "CAD":
        return "CA$";
      default:
        return "";
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 70) return "text-green-600";
    if (score >= 50) return "text-yellow-600";
    return "text-red-600";
  };

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await getFinanceHistory();

        setData(Array.isArray(res) ? res : []);
      } catch (error) {
        console.error("Finance history load failed:", error);
        setData([]);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-10">
      <div className="max-w-5xl mx-auto space-y-6">
        <div className="rounded-3xl bg-gradient-to-br from-slate-900 to-slate-800 text-white p-8 shadow-xl">
          <div className="flex flex-wrap gap-2 mb-4">
            <span className="px-3 py-1 rounded-full bg-white/10 text-xs">
              AI Financial Intelligence
            </span>

            <span className="px-3 py-1 rounded-full bg-white/10 text-xs">
              Personal & Enterprise
            </span>

            <span className="px-3 py-1 rounded-full bg-white/10 text-xs">
              Finance OS
            </span>
          </div>

          <h1 className="text-4xl font-bold leading-tight">
            AI Financial Operating System
          </h1>

          <p className="text-slate-300 mt-4 max-w-3xl">
            Analyze bank statements, detect subscriptions,
            forecast cashflow, monitor spending habits,
            and generate intelligent financial insights
            for both individuals and businesses.
          </p>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8">
            <div className="rounded-2xl bg-white/5 p-4">
              <p className="text-2xl font-bold">AI</p>
              <p className="text-sm text-slate-300">
                Smart analysis
              </p>
            </div>

            <div className="rounded-2xl bg-white/5 p-4">
              <p className="text-2xl font-bold">PDF</p>
              <p className="text-sm text-slate-300">
                Statement parsing
              </p>
            </div>

            <div className="rounded-2xl bg-white/5 p-4">
              <p className="text-2xl font-bold">B2C</p>
              <p className="text-sm text-slate-300">
                Personal finance
              </p>
            </div>

            <div className="rounded-2xl bg-white/5 p-4">
              <p className="text-2xl font-bold">B2B</p>
              <p className="text-sm text-slate-300">
                Enterprise ready
              </p>
            </div>
          </div>
        </div>

        <h1 className="text-3xl font-bold text-center">
          Finance Analysis History
        </h1>

        {loading ? (
          <p className="text-center text-slate-500">Loading...</p>
        ) : data.length === 0 ? (
          <p className="text-center text-slate-500">No analyses yet</p>
        ) : (
          <div className="grid gap-4">
            {data.map((item) => {
              const result =
                typeof item.result === "string"
                  ? JSON.parse(item.result)
                  : item.result || {};

              const score = result.financial_score ?? 0;
              const currencySymbol = getCurrencySymbol(
                result.currency_detected
              );

              return (
                <div
                  key={item.id}
                  className="bg-white border rounded-xl p-5 shadow-sm"
                >
                  <div className="flex justify-between items-center mb-2 gap-4">
                    <h2 className="font-semibold">{item.file_name}</h2>

                    <span className="text-sm text-slate-500 whitespace-nowrap">
                      {new Date(item.created_at).toLocaleDateString()}
                    </span>
                  </div>

                  <p className="text-sm text-slate-600 mb-3">
                    {result.summary}
                  </p>

                  <div className="flex justify-between items-center">
                    <div>
                      <span className="text-sm text-slate-500">Score:</span>{" "}
                      <strong className={getScoreColor(score)}>
                        {result.financial_score ?? "-"}
                      </strong>
                    </div>

                    <div>
                      <span className="text-sm text-slate-500">Spending:</span>{" "}
                      <strong>
                        {currencySymbol}{" "}
                        {result.total_spending_estimate ?? "-"}
                      </strong>
                    </div>
                  </div>

                  <button className="mt-4 text-sm text-blue-600 hover:underline">
                    View details
                  </button>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </main>
  );
}
