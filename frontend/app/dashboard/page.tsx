"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getDocuments, createCheckoutSession } from "../../lib/api";
import { getToken } from "../../lib/auth";
import RiskBadge from "../../components/RiskBadge";

export default function DashboardPage() {
  const [documents, setDocuments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  async function loadDocuments() {
    try {
      const data = await getDocuments();
      setDocuments(data);
    } finally {
      setLoading(false);
    }
  }

  const handleBuyCredit = async () => {
    const data = await createCheckoutSession();

    if (data.checkout_url) {
      window.location.href = data.checkout_url;
      return;
    }

    setMessage(data.detail || "Payment is not configured yet.");
  };

  useEffect(() => {
    const token = getToken();

    if (!token) {
      window.location.href = "/login";
      return;
    }

    loadDocuments();
  }, []);

  if (loading) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-slate-50">
        <p className="text-slate-600">Loading dashboard...</p>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-8 sm:px-6">
      <div className="max-w-6xl mx-auto space-y-8">

        {/* HEADER */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold text-slate-900">Dashboard</h1>
            <p className="text-slate-500 mt-1">
              Manage your contract analyses.
            </p>
          </div>

          <div className="flex flex-wrap gap-3">
            <button
              onClick={handleBuyCredit}
              className="px-5 py-2 rounded-xl bg-green-600 text-white font-medium hover:bg-green-700 transition"
            >
              Buy credit
            </button>

            <Link
              href="/upload"
              className="px-5 py-2 rounded-xl bg-slate-900 text-white font-medium hover:bg-slate-800 transition"
            >
              New Analysis
            </Link>
          </div>
        </div>

        {/* MESSAGE */}
        {message && (
          <div className="bg-red-50 text-red-700 border border-red-200 text-sm p-3 rounded-xl text-center">
            {message}
          </div>
        )}

        {/* STATS CARDS (UI ONLY — no logic change) */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="bg-white border rounded-2xl p-5">
            <p className="text-sm text-slate-500">Total documents</p>
            <p className="text-2xl font-bold text-slate-900 mt-1">
              {documents.length}
            </p>
          </div>

          <div className="bg-white border rounded-2xl p-5">
            <p className="text-sm text-slate-500">Completed</p>
            <p className="text-2xl font-bold text-slate-900 mt-1">
              {documents.filter((d) => d.status === "completed").length}
            </p>
          </div>

          <div className="bg-white border rounded-2xl p-5">
            <p className="text-sm text-slate-500">In progress</p>
            <p className="text-2xl font-bold text-slate-900 mt-1">
              {documents.filter((d) => d.status !== "completed").length}
            </p>
          </div>
        </div>

        {/* EMPTY STATE */}
        {documents.length === 0 ? (
          <div className="bg-white border rounded-2xl p-12 text-center">
            <h2 className="text-xl font-semibold text-slate-900">
              No documents yet
            </h2>

            <p className="text-slate-500 mt-2">
              Upload your first contract to start analyzing.
            </p>

            <Link
              href="/upload"
              className="inline-block mt-6 px-6 py-3 bg-slate-900 text-white rounded-xl font-medium hover:bg-slate-800 transition"
            >
              Upload Contract
            </Link>
          </div>
        ) : (
          /* TABLE */
          <div className="bg-white border rounded-2xl overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-slate-100 text-slate-600">
                  <tr>
                    <th className="text-left p-4 font-medium">Document</th>
                    <th className="text-left p-4 font-medium">Type</th>
                    <th className="text-left p-4 font-medium">Language</th>
                    <th className="text-left p-4 font-medium">Status</th>
                    <th className="text-left p-4 font-medium">Date</th>
                    <th className="text-right p-4 font-medium">Action</th>
                  </tr>
                </thead>

                <tbody>
                  {documents.map((doc) => (
                    <tr
                      key={doc.id}
                      className="border-t hover:bg-slate-50 transition"
                    >
                      <td className="p-4 font-medium text-slate-900">
                        {doc.file_name}
                      </td>

                      <td className="p-4 text-slate-600">
                        {doc.file_type?.toUpperCase()}
                      </td>

                      <td className="p-4 text-slate-600">
                        {doc.language || "—"}
                      </td>

                      <td className="p-4">
                        <RiskBadge
                          risk={doc.status === "completed" ? "low" : "medium"}
                        />
                      </td>

                      <td className="p-4 text-slate-600">
                        {new Date(doc.created_at).toLocaleDateString()}
                      </td>

                      <td className="p-4 text-right">
                        <Link
                          href={`/document/${doc.id}`}
                          className="text-blue-600 font-medium hover:underline"
                        >
                          View
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}