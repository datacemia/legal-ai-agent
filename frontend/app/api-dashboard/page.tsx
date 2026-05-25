"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

type ApiKey = {
  id: number;
  name: string;
  key_prefix: string;
  is_active: boolean;
  last_used_at: string | null;
  created_at: string;
  revoked_at: string | null;
};

type ApiUsage = {
  id: number;
  api_key_id: number | null;
  endpoint: string;
  agent: string;
  credits_used: number;
  status: string;
  created_at: string;
};

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "https://api.runexa.ai";

export default function ApiDashboardPage() {
  const [keys, setKeys] = useState<ApiKey[]>([]);
  const [usage, setUsage] = useState<ApiUsage[]>([]);
  const [newKeyName, setNewKeyName] = useState("Production API Key");
  const [createdKey, setCreatedKey] = useState("");
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  const token =
    typeof window !== "undefined" ? localStorage.getItem("token") : null;

  async function loadData() {
    if (!token) {
      window.location.href = "/login";
      return;
    }

    const apiEnabled =
      localStorage.getItem("api_enabled") === "true";

    if (!apiEnabled) {
      window.location.href = "/pricing";
      return;
    }

    setLoading(true);

    try {
      const [keysRes, usageRes] = await Promise.all([
        fetch(`${API_URL}/api-keys`, {
          headers: { Authorization: `Bearer ${token}` },
        }),
        fetch(`${API_URL}/api-keys/usage`, {
          headers: { Authorization: `Bearer ${token}` },
        }),
      ]);

      if (!keysRes.ok || !usageRes.ok) {
        setMessage("Could not load API dashboard data.");
        return;
      }

      setKeys(await keysRes.json());
      setUsage(await usageRes.json());
    } catch {
      setMessage("Could not connect to the API server.");
    } finally {
      setLoading(false);
    }
  }

  async function createKey() {
    if (!token) return;

    const res = await fetch(`${API_URL}/api-keys`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ name: newKeyName }),
    });

    const data = await res.json();

    if (!res.ok) {
      setMessage(data.detail || "Could not create API key.");
      return;
    }

    setCreatedKey(data.api_key);
    setMessage("API key created. Copy it now. It will only be shown once.");
    await loadData();
  }

  async function revokeKey(id: number) {
    if (!token) return;

    const res = await fetch(`${API_URL}/api-keys/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!res.ok) {
      setMessage("Could not revoke API key.");
      return;
    }

    setMessage("API key revoked.");
    await loadData();
  }

  useEffect(() => {
    loadData();
  }, []);


  const totalRequests = usage.length;
  const creditsUsed = usage.reduce((sum, row) => sum + row.credits_used, 0);
  const activeKeys = keys.filter((key) => key.is_active).length;
  const successRate =
    usage.length === 0
      ? "100%"
      : `${Math.round(
          (usage.filter((row) => row.status !== "failed").length /
            usage.length) *
            100
        )}%`;

  return (
    <main className="min-h-screen bg-slate-50 px-6 py-20 text-slate-900">
      <section className="mx-auto max-w-6xl">
        <p className="font-semibold text-blue-600">Runexa API Dashboard</p>

        <div className="mt-4 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div>
            <h1 className="text-5xl font-bold tracking-tight">
              Manage your API access
            </h1>
            <p className="mt-4 max-w-3xl text-lg leading-8 text-slate-600">
              Monitor API keys, usage, and Runexa AI agent activity.
            </p>
          </div>

          <div className="flex gap-3">
            <Link href="/docs" className="rounded-xl border bg-white px-5 py-3 text-sm font-bold">
              Docs
            </Link>
            <Link href="/pricing" className="rounded-xl bg-blue-600 px-5 py-3 text-sm font-bold text-white">
              Upgrade API
            </Link>
          </div>
        </div>
      </section>

      {message && (
        <div className="mx-auto mt-8 max-w-6xl rounded-2xl border border-blue-200 bg-blue-50 p-4 text-sm font-semibold text-blue-800">
          {message}
        </div>
      )}

      {createdKey && (
        <div className="mx-auto mt-6 max-w-6xl rounded-2xl border border-amber-200 bg-amber-50 p-5">
          <p className="font-bold text-amber-900">Copy your API key now</p>
          <code className="mt-3 block break-all rounded-xl bg-white p-4 text-sm text-slate-900">
            {createdKey}
          </code>
        </div>
      )}

      <section className="mx-auto mt-12 grid max-w-6xl gap-6 md:grid-cols-4">
        {[
          ["Active Keys", activeKeys],
          ["Total Requests", totalRequests],
          ["Credits Used", creditsUsed],
          ["Success Rate", successRate],
        ].map(([label, value]) => (
          <div key={label} className="rounded-3xl border bg-white p-6 shadow-sm">
            <p className="text-sm font-semibold text-slate-500">{label}</p>
            <p className="mt-3 text-3xl font-bold">{value}</p>
          </div>
        ))}
      </section>

      <section className="mx-auto mt-10 grid max-w-6xl gap-6 lg:grid-cols-[1.2fr_0.8fr]">
        <div className="rounded-3xl border bg-white p-6 shadow-sm">
          <h2 className="text-2xl font-bold">API Keys</h2>

          <div className="mt-5 flex gap-3">
            <input
              value={newKeyName}
              onChange={(e) => setNewKeyName(e.target.value)}
              className="flex-1 rounded-xl border border-slate-200 px-4 py-3 text-sm"
              placeholder="API key name"
            />
            <button
              onClick={createKey}
              className="rounded-xl bg-slate-950 px-5 py-3 text-sm font-bold text-white"
            >
              Create key
            </button>
          </div>

          <div className="mt-6 overflow-hidden rounded-2xl border">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-50 text-slate-500">
                <tr>
                  <th className="px-4 py-3">Name</th>
                  <th className="px-4 py-3">Prefix</th>
                  <th className="px-4 py-3">Status</th>
                  <th className="px-4 py-3">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {keys.map((key) => (
                  <tr key={key.id}>
                    <td className="px-4 py-4 font-semibold">{key.name}</td>
                    <td className="px-4 py-4 font-mono">{key.key_prefix}</td>
                    <td className="px-4 py-4">
                      {key.is_active ? "Active" : "Revoked"}
                    </td>
                    <td className="px-4 py-4">
                      {key.is_active && (
                        <button
                          onClick={() => revokeKey(key.id)}
                          className="text-sm font-bold text-red-600"
                        >
                          Revoke
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="rounded-3xl border bg-slate-950 p-6 text-white shadow-sm">
          <h2 className="text-2xl font-bold">Quickstart</h2>
          <pre className="mt-5 overflow-x-auto rounded-2xl border border-white/10 bg-white/5 p-4 text-xs">
{`curl -X POST "https://api.runexa.ai/v1/finance/analyze" \\
  -H "Authorization: Bearer rk_live_xxx" \\
  -F "file=@statement.pdf" \\
  -F "output_language=en"`}
          </pre>
        </div>
      </section>

      <section className="mx-auto mt-10 max-w-6xl rounded-3xl border bg-white p-6 shadow-sm">
        <h2 className="text-2xl font-bold">Recent usage</h2>

        <div className="mt-6 overflow-hidden rounded-2xl border">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-50 text-slate-500">
              <tr>
                <th className="px-4 py-3">Endpoint</th>
                <th className="px-4 py-3">Agent</th>
                <th className="px-4 py-3">Credits</th>
                <th className="px-4 py-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {usage.map((row) => (
                <tr key={row.id}>
                  <td className="px-4 py-4 font-mono">{row.endpoint}</td>
                  <td className="px-4 py-4">{row.agent}</td>
                  <td className="px-4 py-4">{row.credits_used}</td>
                  <td className="px-4 py-4">{row.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  );
}