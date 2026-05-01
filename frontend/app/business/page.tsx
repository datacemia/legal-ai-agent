"use client";

import { useState } from "react";
import { analyzeBusinessFile } from "../../lib/api";

export default function BusinessPage() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleAnalyze = async () => {
    if (!file) return;

    setLoading(true);
    setResult(null);
    setMessage("");

    try {
      const data = await analyzeBusinessFile(file);
      setResult(data);
    } catch (error: any) {
      setMessage(error?.message || "Failed to analyze business file.");
    } finally {
      setLoading(false);
    }
  };

  const score = Number(result?.business_health_score || 0);

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-10">
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold">Business Decision Agent</h1>
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
            {loading ? "Analyzing business data..." : "Analyze business data"}
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

                <div>
                  <strong>Business health score:</strong>{" "}
                  {result.business_health_score}/100

                  <div className="mt-3 h-3 bg-slate-200 rounded-full">
                    <div
                      className={`h-3 rounded-full ${
                        score >= 70
                          ? "bg-green-500"
                          : score >= 50
                          ? "bg-yellow-500"
                          : "bg-red-500"
                      }`}
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