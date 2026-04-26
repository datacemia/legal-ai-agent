"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { getAnalysis } from "../../../lib/api";
import RiskBadge from "../../../components/RiskBadge";
import RiskScore from "../../../components/RiskScore";

export default function DocumentPage() {
  const params = useParams();
  const documentId = Number(params.id);

  const [analysis, setAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  useEffect(() => {
    async function loadAnalysis() {
      try {
        const data = await getAnalysis(documentId);
        setAnalysis(data);
      } finally {
        setLoading(false);
      }
    }

    loadAnalysis();
  }, [documentId]);

  if (loading) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-slate-50">
        <p className="text-slate-600">Loading analysis...</p>
      </main>
    );
  }

  if (!analysis?.id) {
    return (
      <main className="min-h-screen bg-slate-50 px-4 py-8">
        <div className="max-w-4xl mx-auto bg-white border border-slate-200 rounded-3xl p-8 shadow-sm">
          <h1 className="text-xl font-bold text-slate-950">
            Analysis not found
          </h1>

          <Link
            href="/dashboard"
            className="text-blue-600 mt-4 inline-block font-medium"
          >
            ← Back to dashboard
          </Link>
        </div>
      </main>
    );
  }

  const isArabic = analysis.language === "ar";
  const textDirection = isArabic ? "rtl" : "ltr";
  const clauses = analysis?.clauses ? JSON.parse(analysis.clauses) : [];

  return (
    <main
      dir={textDirection}
      className="min-h-screen bg-slate-50 px-4 py-8 sm:px-6"
    >
      <div className="max-w-5xl mx-auto space-y-8">
        <Link
          href="/dashboard"
          className="inline-flex text-sm font-medium text-blue-600 hover:text-blue-700"
        >
          ← Back to dashboard
        </Link>

        <section className="bg-white p-6 rounded-3xl shadow-sm border border-slate-200">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-sm font-semibold text-blue-600">
                Document analysis
              </p>
              <h1 className="mt-1 text-2xl sm:text-3xl font-bold text-slate-950">
                Contract Analysis
              </h1>
            </div>

            <RiskBadge risk={analysis.risk_level} />
          </div>

          <p
            dir={textDirection}
            className="mt-6 text-slate-700 whitespace-pre-line leading-7 text-start"
          >
            {analysis.summary}
          </p>
        </section>

        <RiskScore score={analysis.risk_score} />

        <section className="bg-blue-50 p-6 rounded-3xl border border-blue-200">
          <h2 className="text-xl font-semibold text-blue-800">
            Simplified Version
          </h2>

          <p
            dir={textDirection}
            className="mt-4 text-blue-900 whitespace-pre-line leading-7 text-start"
          >
            {analysis.simplified_version}
          </p>
        </section>

        <section className="bg-white p-6 rounded-3xl shadow-sm border border-slate-200">
          <div className="flex items-center justify-between gap-4 mb-5">
            <div>
              <p className="text-sm text-slate-500">Detailed review</p>
              <h2 className="text-xl font-semibold text-slate-950">
                Clauses Analysis
              </h2>
            </div>

            <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600">
              {clauses.length} clauses
            </span>
          </div>

          <div className="space-y-4">
            {clauses.map((clause: any, index: number) => (
              <div
                key={index}
                className={`border rounded-2xl p-4 cursor-pointer transition ${
                  clause.risk_level === "high"
                    ? "border-red-300 bg-red-50"
                    : clause.risk_level === "medium"
                    ? "border-yellow-300 bg-yellow-50"
                    : "border-slate-200 bg-white hover:bg-slate-50"
                }`}
                onClick={() => setOpenIndex(openIndex === index ? null : index)}
              >
                <div className="flex items-center justify-between gap-4">
                  <div className="flex items-center gap-3">
                    <span className="flex h-8 w-8 items-center justify-center rounded-xl bg-white text-sm font-semibold text-slate-700 border">
                      {index + 1}
                    </span>

                    <span className="font-semibold text-slate-900">
                      Clause {index + 1}
                    </span>

                    <span className="text-xs text-slate-400">
                      {openIndex === index ? "▲" : "▼"}
                    </span>
                  </div>

                  <RiskBadge risk={clause.risk_level} />
                </div>

                <p
                  dir={textDirection}
                  className="text-blue-700 text-sm mt-3 text-start"
                >
                  {clause.explanation_simple}
                </p>

                {openIndex === index && (
                  <div className="mt-4 space-y-3">
                    <p
                      dir={textDirection}
                      className="text-sm text-slate-500 text-start"
                    >
                      Trigger: {clause.trigger || "None"}
                    </p>

                    <p
                      dir={textDirection}
                      className="text-slate-800 leading-7 text-start"
                    >
                      {clause.original_text}
                    </p>

                    <p
                      dir={textDirection}
                      className="text-slate-600 text-sm text-start"
                    >
                      Recommendation: {clause.recommendation}
                    </p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}