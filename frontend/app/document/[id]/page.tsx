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
      <main className="min-h-screen flex items-center justify-center bg-gray-50">
        <p className="text-gray-600">Loading analysis...</p>
      </main>
    );
  }

  if (!analysis?.id) {
    return (
      <main className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-4xl mx-auto bg-white border rounded-2xl p-8">
          <h1 className="text-xl font-bold">Analysis not found</h1>
          <Link href="/dashboard" className="text-blue-700 mt-4 inline-block">
            Back to dashboard
          </Link>
        </div>
      </main>
    );
  }

  const clauses = analysis?.clauses ? JSON.parse(analysis.clauses) : [];

  return (
    <main className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-5xl mx-auto space-y-8">
        <Link href="/dashboard" className="text-blue-700">
          ← Back to dashboard
        </Link>

        <div className="bg-white p-6 rounded-2xl shadow-sm border">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold">Contract Analysis</h1>
            <RiskBadge risk={analysis.risk_level} />
          </div>

          <p className="mt-4 text-gray-700 whitespace-pre-line">
            {analysis.summary}
          </p>
        </div>

        <RiskScore score={analysis.risk_score} />

        <div className="bg-blue-50 p-6 rounded-2xl border border-blue-200">
          <h2 className="text-xl font-semibold text-blue-800">
            Simplified Version
          </h2>

          <p className="mt-4 text-blue-900 whitespace-pre-line">
            {analysis.simplified_version}
          </p>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow-sm border">
          <h2 className="text-xl font-semibold mb-4">Clauses Analysis</h2>

          <div className="space-y-4">
            {clauses.map((clause: any, index: number) => (
              <div
                key={index}
                className={`border rounded-xl p-4 cursor-pointer transition ${
                  clause.risk_level === "high"
                    ? "border-red-300 bg-red-50"
                    : clause.risk_level === "medium"
                    ? "border-yellow-300 bg-yellow-50"
                    : "border-gray-200 bg-white hover:bg-gray-50"
                }`}
                onClick={() => setOpenIndex(openIndex === index ? null : index)}
              >
                <div className="flex justify-between items-center">
                  <span className="font-semibold">Clause {index + 1}</span>
                  <RiskBadge risk={clause.risk_level} />
                </div>

                <p className="text-blue-700 text-sm mt-2">
                  {clause.explanation_simple}
                </p>

                {openIndex === index && (
                  <div className="mt-3 space-y-2">
                    <p className="text-sm text-gray-500">
                      Trigger: {clause.trigger || "None"}
                    </p>
                    <p className="text-gray-800">{clause.original_text}</p>
                    <p className="text-gray-600 text-sm">
                      Recommendation: {clause.recommendation}
                    </p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}