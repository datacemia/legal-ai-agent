"use client";

import { useEffect, useState } from "react";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "https://api.runexa.ai";

type FreeAccessRequest = {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  country: string;
  created_at: string | null;
};

export default function FreeAccessRequestsPage() {
  const [requests, setRequests] = useState<FreeAccessRequest[]>([]);
  const [message, setMessage] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      window.location.href = "/login";
      return;
    }

    fetch(`${API_URL}/admin/free-access-requests`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => {
        if (!res.ok) throw new Error("Not allowed");
        return res.json();
      })
      .then((data: FreeAccessRequest[]) => setRequests(data))
      .catch(() =>
        setMessage("Not allowed or unable to load free access requests.")
      );
  }, []);

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-10">
      <div className="mx-auto max-w-6xl space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-slate-950">
            Free access requests
          </h1>

          <p className="mt-1 text-slate-500">
            Review requests for complimentary Runexa evaluation credits.
          </p>
        </div>

        {message && (
          <div className="rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-700">
            {message}
          </div>
        )}

        <div className="overflow-hidden rounded-2xl border bg-white">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-slate-100 text-slate-600">
                <tr>
                  <th className="p-4 text-start">First name</th>
                  <th className="p-4 text-start">Last name</th>
                  <th className="p-4 text-start">Email</th>
                  <th className="p-4 text-start">Country</th>
                  <th className="p-4 text-start">Date</th>
                </tr>
              </thead>

              <tbody>
                {requests.map((req) => (
                  <tr key={req.id} className="border-t">
                    <td className="p-4 font-medium">
                      {req.first_name}
                    </td>

                    <td className="p-4">
                      {req.last_name}
                    </td>

                    <td className="p-4">
                      {req.email}
                    </td>

                    <td className="p-4">
                      {req.country}
                    </td>

                    <td className="p-4">
                      {req.created_at
                        ? new Date(req.created_at).toLocaleDateString()
                        : "—"}
                    </td>
                  </tr>
                ))}

                {requests.length === 0 && !message && (
                  <tr>
                    <td
                      className="p-6 text-center text-slate-500"
                      colSpan={5}
                    >
                      No free access requests yet.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>
  );
}