"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getDocuments, createCheckoutSession } from "../../lib/api";
import { getToken } from "../../lib/auth";
import RiskBadge from "../../components/RiskBadge";
import Navbar from "../../components/Navbar";

export default function DashboardPage() {
  const [documents, setDocuments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

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

    alert(data.detail || "Payment is not configured yet.");
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
      <main className="min-h-screen flex items-center justify-center bg-gray-50">
        <p className="text-gray-600">Loading dashboard...</p>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto space-y-8">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
            <p className="text-gray-500 mt-1">
              Manage your contract analyses.
            </p>
          </div>

          <div className="flex gap-3">
            <button
              onClick={handleBuyCredit}
              className="px-5 py-2 bg-green-600 text-white rounded-lg"
            >
              Buy credit
            </button>

            <Link
              href="/upload"
              className="px-5 py-2 bg-black text-white rounded-lg"
            >
              New Analysis
            </Link>
          </div>
        </div>

        {documents.length === 0 ? (
          <div className="bg-white border rounded-2xl p-10 text-center">
            <h2 className="text-xl font-semibold">No documents yet</h2>
            <p className="text-gray-500 mt-2">
              Upload your first contract to start.
            </p>

            <Link
              href="/upload"
              className="inline-block mt-5 px-5 py-2 bg-black text-white rounded-lg"
            >
              Upload Contract
            </Link>
          </div>
        ) : (
          <div className="bg-white border rounded-2xl overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-gray-100 text-gray-600">
                <tr>
                  <th className="text-left p-4">Document</th>
                  <th className="text-left p-4">Type</th>
                  <th className="text-left p-4">Language</th>
                  <th className="text-left p-4">Status</th>
                  <th className="text-left p-4">Date</th>
                  <th className="text-right p-4">Action</th>
                </tr>
              </thead>

              <tbody>
                {documents.map((doc) => (
                  <tr key={doc.id} className="border-t">
                    <td className="p-4 font-medium">{doc.file_name}</td>
                    <td className="p-4">{doc.file_type?.toUpperCase()}</td>
                    <td className="p-4">{doc.language || "—"}</td>
                    <td className="p-4">
                      <RiskBadge
                        risk={doc.status === "completed" ? "low" : "medium"}
                      />
                    </td>
                    <td className="p-4">
                      {new Date(doc.created_at).toLocaleDateString()}
                    </td>
                    <td className="p-4 text-right">
                      <Link
                        href={`/document/${doc.id}`}
                        className="text-blue-700 font-medium"
                      >
                        View
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </main>
  );
}