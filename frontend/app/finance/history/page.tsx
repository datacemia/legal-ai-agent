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
      const res = await getFinanceHistory();
      setData(res);
      setLoading(false);
    }

    fetchData();
  }, []);

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-10">
      <div className="max-w-5xl mx-auto space-y-6">
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
              const score = item.result.financial_score ?? 0;
              const currencySymbol = getCurrencySymbol(
                item.result.currency_detected
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
                    {item.result.summary}
                  </p>

                  <div className="flex justify-between items-center">
                    <div>
                      <span className="text-sm text-slate-500">Score:</span>{" "}
                      <strong className={getScoreColor(score)}>
                        {item.result.financial_score ?? "-"}
                      </strong>
                    </div>

                    <div>
                      <span className="text-sm text-slate-500">Spending:</span>{" "}
                      <strong>
                        {currencySymbol}{" "}
                        {item.result.total_spending_estimate ?? "-"}
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