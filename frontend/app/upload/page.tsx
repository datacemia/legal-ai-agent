"use client";

import { useState } from "react";
import { uploadDocument, runAnalysis } from "../../lib/api";
import RiskBadge from "../../components/RiskBadge";
import RiskScore from "../../components/RiskScore";
import UploadBox from "../../components/UploadBox";
import Navbar from "../../components/Navbar";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [fileName, setFileName] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [language, setLanguage] = useState("en");
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  const handleUpload = async () => {
    if (!file) return;

    try {
      setLoading(true);
      setResult(null);
      setOpenIndex(null);

      const doc = await uploadDocument(file);
      const analysis = await runAnalysis(doc.id, language);

      if (analysis.detail?.includes("Payment required")) {
        alert("You used your free analysis. Please buy one analysis credit.");
        window.location.href = "/dashboard";
        return;
      }

      setResult(analysis);
    } finally {
      setLoading(false);
    }
  };

  const clauses = result?.clauses ? JSON.parse(result.clauses) : [];

  if (loading) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center space-y-4">
          <div className="w-12 h-12 border-4 border-black border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p className="text-gray-600">Analyzing your contract...</p>
          {fileName && <p className="text-sm text-gray-500">File: {fileName}</p>}
        </div>
      </main>
    );
  }

  return (
    <main
      dir={language === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-gray-50 p-6"
    >
      <div className="max-w-5xl mx-auto space-y-8">
        <h1 className="text-3xl font-bold text-gray-900">
          Analyze your contract
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white border rounded-xl p-4">
            <p className="font-semibold">⚡ 60-second summary</p>
            <p className="text-sm text-gray-500">Understand key points fast.</p>
          </div>

          <div className="bg-white border rounded-xl p-4">
            <p className="font-semibold">🔒 Private by design</p>
            <p className="text-sm text-gray-500">Your documents stay protected.</p>
          </div>

          <div className="bg-white border rounded-xl p-4">
            <p className="font-semibold">🌍 EN / FR / AR</p>
            <p className="text-sm text-gray-500">Multilingual contract analysis.</p>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow-sm border">
          <UploadBox
            file={file}
            onFileChange={(selected) => {
              setFile(selected);
              setFileName(selected?.name || "");
              setResult(null);
              setOpenIndex(null);
            }}
          />

          <div className="flex items-center gap-4 mt-5 flex-wrap">
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="border rounded-lg px-3 py-2"
            >
              <option value="en">English</option>
              <option value="fr">Français</option>
              <option value="ar">العربية</option>
            </select>

            <button
              onClick={handleUpload}
              disabled={!file}
              className="px-5 py-2 bg-black text-white rounded-lg disabled:opacity-50"
            >
              Analyze Contract
            </button>
          </div>
        </div>

        {!result && (
          <div className="bg-white border rounded-2xl p-8 text-center text-gray-500">
            Upload a contract to see the summary, risk score, simplified version,
            and clause analysis.
          </div>
        )}

        {result && (
          <>
            <div className="bg-white p-6 rounded-2xl shadow-sm border">
              <div className="flex justify-between items-center">
                <h2 className="text-xl font-semibold">Summary</h2>
                <RiskBadge risk={result.risk_level} />
              </div>

              <p className="mt-4 text-gray-700 whitespace-pre-line">
                {result.summary}
              </p>
            </div>

            <RiskScore score={result.risk_score} />

            <div className="bg-blue-50 p-6 rounded-2xl border border-blue-200">
              <h2 className="text-xl font-semibold text-blue-800">
                Simplified Version
              </h2>

              <p className="mt-4 text-blue-900 whitespace-pre-line">
                {result.simplified_version}
              </p>
            </div>

            <div className="bg-white p-6 rounded-2xl shadow-sm border">
              <h2 className="text-xl font-semibold mb-4">
                Clauses Analysis
              </h2>

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
                    onClick={() =>
                      setOpenIndex(openIndex === index ? null : index)
                    }
                  >
                    <div className="flex justify-between items-center">
                      <div className="flex items-center gap-2">
                        <span className="font-semibold">
                          Clause {index + 1}
                        </span>
                        <span className="text-xs text-gray-400">
                          {openIndex === index ? "▲" : "▼"}
                        </span>
                      </div>

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

                        <p className="text-gray-800">
                          {clause.original_text}
                        </p>

                        <p className="text-gray-600 text-sm">
                          Recommendation: {clause.recommendation}
                        </p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </>
        )}
      </div>
    </main>
  );
}