"use client";

import { useEffect, useState } from "react";
import { getDocuments } from "../../../lib/api";

export default function LegalHistoryPage() {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await getDocuments();
        setData(Array.isArray(res) ? res : []);
      } catch (error) {
        console.error("Legal history load failed:", error);
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
        <h1 className="text-3xl font-bold text-center">
          Legal Analysis History
        </h1>

        {loading ? (
          <p className="text-center text-slate-500">Loading...</p>
        ) : data.length === 0 ? (
          <p className="text-center text-slate-500">
            No legal analyses yet
          </p>
        ) : (
          <div className="grid gap-4">
            {data.map((item) => (
              <div
                key={item.id}
                className="bg-white border rounded-xl p-5 shadow-sm"
              >
                <div className="flex justify-between items-center mb-3 gap-4">
                  <h2 className="font-semibold">
                    {item.file_name}
                  </h2>

                  <span className="text-sm text-slate-500 whitespace-nowrap">
                    {new Date(item.created_at).toLocaleDateString()}
                  </span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-sm">
                  <div className="rounded-xl bg-slate-50 border px-3 py-2">
                    <span className="text-slate-500">Type:</span>{" "}
                    <strong>
                      {item.file_type?.toUpperCase() || "PDF"}
                    </strong>
                  </div>

                  <div className="rounded-xl bg-slate-50 border px-3 py-2">
                    <span className="text-slate-500">Language:</span>{" "}
                    <strong>
                      {item.language || "—"}
                    </strong>
                  </div>

                  <div className="rounded-xl bg-slate-50 border px-3 py-2">
                    <span className="text-slate-500">Status:</span>{" "}
                    <strong>
                      {item.status || "completed"}
                    </strong>
                  </div>
                </div>

                <a
                  href="/upload"
                  className="inline-block mt-4 text-sm text-blue-600 hover:underline"
                >
                  Analyze another contract
                </a>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
