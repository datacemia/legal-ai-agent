"use client";

import { useEffect, useState } from "react";
import { getStudyHistory } from "../../../lib/api";

export default function StudyHistoryPage() {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      const res = await getStudyHistory();
      setData(Array.isArray(res) ? res : []);
      setLoading(false);
    }

    fetchData();
  }, []);

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-10">
      <div className="max-w-5xl mx-auto space-y-6">
        <h1 className="text-3xl font-bold text-center">
          Study Analysis History
        </h1>

        {loading ? (
          <p className="text-center text-slate-500">Loading...</p>
        ) : data.length === 0 ? (
          <p className="text-center text-slate-500">No study analyses yet</p>
        ) : (
          <div className="grid gap-4">
            {data.map((item) => (
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
                  {item.result?.summary}
                </p>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-sm">
                  <div className="rounded-xl bg-slate-50 border px-3 py-2">
                    <span className="text-slate-500">Key points:</span>{" "}
                    <strong>{item.result?.key_points?.length ?? 0}</strong>
                  </div>

                  <div className="rounded-xl bg-slate-50 border px-3 py-2">
                    <span className="text-slate-500">Quiz questions:</span>{" "}
                    <strong>
                      {(item.result?.quiz?.theory_questions?.length ?? 0) +
                        (item.result?.quiz?.practice_questions?.length ?? 0)}
                    </strong>
                  </div>

                  <div className="rounded-xl bg-slate-50 border px-3 py-2">
                    <span className="text-slate-500">Flashcards:</span>{" "}
                    <strong>{item.result?.flashcards?.length ?? 0}</strong>
                  </div>
                </div>

                <a
                  href="/study"
                  className="inline-block mt-4 text-sm text-blue-600 hover:underline"
                >
                  Analyze another PDF
                </a>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}