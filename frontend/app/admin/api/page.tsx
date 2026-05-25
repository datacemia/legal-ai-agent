"use client";

import { useEffect, useState } from "react";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "https://api.runexa.ai";

type ApiOverview = {
  api_users: number;
  active_keys: number;
  total_usage: number;
  total_api_credits: number;
};

type ApiUser = {
  id: number;
  email: string;
  role: string;
  plan: string;
  api_enabled: boolean;
  api_plan: string;
  api_credits_balance: number;
  created_at: string;
};

type ApiKey = {
  id: number;
  user_id: number;
  email: string;
  name: string;
  key_prefix: string;
  is_active: boolean;
  last_used_at: string | null;
  created_at: string;
  revoked_at: string | null;
};

type ApiUsage = {
  id: number;
  user_id: number;
  email: string;
  api_key_id: number | null;
  endpoint: string;
  agent: string | null;
  credits_used: number;
  status: string;
  created_at: string;
};

export default function AdminApiPage() {
  const [overview, setOverview] = useState<ApiOverview | null>(null);
  const [users, setUsers] = useState<ApiUser[]>([]);
  const [keys, setKeys] = useState<ApiKey[]>([]);
  const [usage, setUsage] = useState<ApiUsage[]>([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  const token =
    typeof window !== "undefined"
      ? localStorage.getItem("token")
      : null;

  async function apiFetch(path: string, options: RequestInit = {}) {
    if (!token) {
      window.location.href = "/login";
      return null;
    }

    const res = await fetch(`${API_URL}${path}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        ...(options.headers || {}),
      },
    });

    if (res.status === 401 || res.status === 403) {
      window.location.href = "/dashboard";
      return null;
    }

    return res;
  }

  async function loadData() {
    setLoading(true);
    setMessage("");

    try {
      const [overviewRes, usersRes, keysRes, usageRes] =
        await Promise.all([
          apiFetch("/admin/api/overview"),
          apiFetch("/admin/api/users"),
          apiFetch("/admin/api/keys"),
          apiFetch("/admin/api/usage"),
        ]);

      if (!overviewRes || !usersRes || !keysRes || !usageRes) {
        return;
      }

      if (
        !overviewRes.ok ||
        !usersRes.ok ||
        !keysRes.ok ||
        !usageRes.ok
      ) {
        setMessage("Could not load admin API data.");
        return;
      }

      setOverview(await overviewRes.json());
      setUsers(await usersRes.json());
      setKeys(await keysRes.json());
      setUsage(await usageRes.json());
    } finally {
      setLoading(false);
    }
  }

  function updateLocalUser(
    userId: number,
    field: keyof ApiUser,
    value: string | boolean | number
  ) {
    setUsers((current) =>
      current.map((user) =>
        user.id === userId ? { ...user, [field]: value } : user
      )
    );
  }

  async function saveUser(user: ApiUser) {
    const res = await apiFetch(`/admin/api/users/${user.id}`, {
      method: "PATCH",
      body: JSON.stringify({
        api_enabled: user.api_enabled,
        api_plan: user.api_plan,
        api_credits_balance: Number(user.api_credits_balance),
      }),
    });

    if (!res) return;

    if (!res.ok) {
      const data = await res.json();
      setMessage(data.detail || "Could not update API user.");
      return;
    }

    setMessage("API user updated.");
    await loadData();
  }

  async function revokeKey(keyId: number) {
    const confirmed = window.confirm(
      "Revoke this API key? This action cannot be undone."
    );

    if (!confirmed) return;

    const res = await apiFetch(`/admin/api/keys/${keyId}`, {
      method: "DELETE",
    });

    if (!res) return;

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

  if (loading) {
    return (
      <main className="min-h-screen bg-slate-50 p-6">
        <div className="mx-auto max-w-6xl">
          <p className="text-slate-600">Loading API admin...</p>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-50 p-6 text-slate-900">
      <div className="mx-auto max-w-7xl space-y-8">
        <section>
          <p className="font-semibold text-blue-600">
            Admin API Management
          </p>

          <h1 className="mt-3 text-4xl font-bold">
            Manage Runexa API access
          </h1>

          <p className="mt-3 max-w-3xl text-slate-600">
            Enable API access, update API plans, adjust API credits,
            review keys, and monitor usage across users.
          </p>
        </section>

        {message && (
          <div className="rounded-2xl border border-blue-200 bg-blue-50 p-4 text-sm font-semibold text-blue-800">
            {message}
          </div>
        )}

        <section className="grid gap-4 md:grid-cols-4">
          {[
            ["API Users", overview?.api_users ?? 0],
            ["Active Keys", overview?.active_keys ?? 0],
            ["Usage Events", overview?.total_usage ?? 0],
            ["API Credits", overview?.total_api_credits ?? 0],
          ].map(([label, value]) => (
            <div
              key={label}
              className="rounded-2xl border bg-white p-5 shadow-sm"
            >
              <p className="text-sm text-slate-500">{label}</p>
              <p className="mt-2 text-3xl font-bold">{value}</p>
            </div>
          ))}
        </section>

        <section className="rounded-3xl border bg-white p-6 shadow-sm">
          <h2 className="text-2xl font-bold">API Users</h2>

          <div className="mt-6 overflow-x-auto rounded-2xl border">
            <table className="w-full min-w-[900px] text-left text-sm">
              <thead className="bg-slate-100 text-slate-600">
                <tr>
                  <th className="p-4">ID</th>
                  <th className="p-4">Email</th>
                  <th className="p-4">Enabled</th>
                  <th className="p-4">API Plan</th>
                  <th className="p-4">API Credits</th>
                  <th className="p-4 text-right">Action</th>
                </tr>
              </thead>

              <tbody className="divide-y">
                {users.map((user) => (
                  <tr key={user.id}>
                    <td className="p-4">{user.id}</td>
                    <td className="p-4 font-medium">{user.email}</td>

                    <td className="p-4">
                      <input
                        type="checkbox"
                        checked={user.api_enabled}
                        onChange={(event) =>
                          updateLocalUser(
                            user.id,
                            "api_enabled",
                            event.target.checked
                          )
                        }
                      />
                    </td>

                    <td className="p-4">
                      <select
                        value={user.api_plan}
                        onChange={(event) =>
                          updateLocalUser(
                            user.id,
                            "api_plan",
                            event.target.value
                          )
                        }
                        className="rounded-lg border px-3 py-2"
                      >
                        <option value="none">none</option>
                        <option value="api_starter">api_starter</option>
                        <option value="api_pro">api_pro</option>
                        <option value="api_enterprise">
                          api_enterprise
                        </option>
                      </select>
                    </td>

                    <td className="p-4">
                      <input
                        type="number"
                        min={0}
                        value={user.api_credits_balance}
                        onChange={(event) =>
                          updateLocalUser(
                            user.id,
                            "api_credits_balance",
                            Number(event.target.value)
                          )
                        }
                        className="w-28 rounded-lg border px-3 py-2"
                      />
                    </td>

                    <td className="p-4 text-right">
                      <button
                        onClick={() => saveUser(user)}
                        className="rounded-xl bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700"
                      >
                        Save
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="grid gap-6 lg:grid-cols-2">
          <div className="rounded-3xl border bg-white p-6 shadow-sm">
            <h2 className="text-2xl font-bold">API Keys</h2>

            <div className="mt-6 overflow-x-auto rounded-2xl border">
              <table className="w-full min-w-[760px] text-left text-sm">
                <thead className="bg-slate-100 text-slate-600">
                  <tr>
                    <th className="p-4">User</th>
                    <th className="p-4">Name</th>
                    <th className="p-4">Prefix</th>
                    <th className="p-4">Status</th>
                    <th className="p-4 text-right">Action</th>
                  </tr>
                </thead>

                <tbody className="divide-y">
                  {keys.map((key) => (
                    <tr key={key.id}>
                      <td className="p-4">{key.email}</td>
                      <td className="p-4 font-medium">{key.name}</td>
                      <td className="p-4 font-mono">{key.key_prefix}</td>
                      <td className="p-4">
                        {key.is_active ? "Active" : "Revoked"}
                      </td>
                      <td className="p-4 text-right">
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

          <div className="rounded-3xl border bg-white p-6 shadow-sm">
            <h2 className="text-2xl font-bold">Recent API Usage</h2>

            <div className="mt-6 overflow-x-auto rounded-2xl border">
              <table className="w-full min-w-[760px] text-left text-sm">
                <thead className="bg-slate-100 text-slate-600">
                  <tr>
                    <th className="p-4">User</th>
                    <th className="p-4">Endpoint</th>
                    <th className="p-4">Agent</th>
                    <th className="p-4">Credits</th>
                    <th className="p-4">Status</th>
                  </tr>
                </thead>

                <tbody className="divide-y">
                  {usage.map((row) => (
                    <tr key={row.id}>
                      <td className="p-4">{row.email}</td>
                      <td className="p-4 font-mono">{row.endpoint}</td>
                      <td className="p-4">{row.agent || "—"}</td>
                      <td className="p-4">{row.credits_used}</td>
                      <td className="p-4">{row.status}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
