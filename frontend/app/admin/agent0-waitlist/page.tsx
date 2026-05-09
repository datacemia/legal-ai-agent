"use client";

import { useEffect, useState } from "react";
import { getToken } from "../../../lib/auth";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export default function Agent0WaitlistAdminPage() {
  const [items, setItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  useEffect(() => {
    const role = localStorage.getItem("role");

    if (role !== "admin") {
      window.location.href = "/";
      return;
    }

    loadWaitlist();
  }, []);

  const loadWaitlist = async () => {
    try {
      const token = getToken();

      const res = await fetch(`${API_URL}/agent0-waitlist/`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Failed to load waitlist.");
      }

      setItems(Array.isArray(data) ? data : []);
    } catch (error: any) {
      setMessage(error.message || "Error loading Agent 0 waitlist.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-50 px-6 py-10">
      <div className="mx-auto max-w-7xl space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">
            Agent 0 Waitlist
          </h1>
          <p className="mt-2 text-slate-500">
            People interested in Runexa Agent 0 early access.
          </p>
        </div>

        {loading && (
          <div className="rounded-2xl border bg-white p-6 text-slate-600">
            Loading waitlist...
          </div>
        )}

        {message && (
          <div className="rounded-2xl border border-red-200 bg-red-50 p-4 text-red-700">
            {message}
          </div>
        )}

        {!loading && !message && (
          <div className="rounded-2xl border bg-white shadow-sm">
            <div className="border-b p-5">
              <p className="font-semibold text-slate-900">
                Total leads: {items.length}
              </p>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-slate-100 text-slate-600">
                  <tr>
                    <th className="p-4 text-left">Name</th>
                    <th className="p-4 text-left">Email</th>
                    <th className="p-4 text-left">Country</th>
                    <th className="p-4 text-left">Profile</th>
                    <th className="p-4 text-left">Interest</th>
                    <th className="p-4 text-left">Protect</th>
                    <th className="p-4 text-left">Message</th>
                    <th className="p-4 text-left">Date</th>
                  </tr>
                </thead>

                <tbody>
                  {items.map((item) => (
                    <tr key={item.id} className="border-t hover:bg-slate-50">
                      <td className="p-4 font-medium">{item.full_name}</td>
                      <td className="p-4">{item.email}</td>
                      <td className="p-4">{item.country || "—"}</td>
                      <td className="p-4">{item.profile || "—"}</td>
                      <td className="p-4">{item.interest_level || "—"}</td>
                      <td className="p-4">{item.protect_target || "—"}</td>
                      <td className="max-w-xs p-4 text-slate-600">
                        {item.message || "—"}
                      </td>
                      <td className="p-4 whitespace-nowrap">
                        {item.created_at
                          ? new Date(item.created_at).toLocaleDateString()
                          : "—"}
                      </td>
                    </tr>
                  ))}

                  {items.length === 0 && (
                    <tr>
                      <td colSpan={8} className="p-8 text-center text-slate-500">
                        No waitlist submissions yet.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}