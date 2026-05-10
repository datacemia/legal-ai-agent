"use client";

import { useEffect, useMemo, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

const AVAILABLE_AGENTS = [
  {
    slug: "legal",
    label: "Legal Agent",
  },
  {
    slug: "study",
    label: "Study Agent",
  },
  {
    slug: "finance",
    label: "Finance Agent",
  },
  {
    slug: "business",
    label: "Business Agent",
  },
];

export default function AdminEnterprisesPage() {
  const [enterprises, setEnterprises] = useState<any[]>([]);
  const [selectedEnterprise, setSelectedEnterprise] = useState<any>(null);
  const [selectedUsage, setSelectedUsage] = useState<any>(null);
  const [selectedMembers, setSelectedMembers] = useState<any[]>([]);

  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [message, setMessage] = useState("");

  const [name, setName] = useState("");
  const [slug, setSlug] = useState("");
  const [ownerEmail, setOwnerEmail] = useState("");
  const [creditsBalance, setCreditsBalance] = useState(0);
  const [planName, setPlanName] = useState("enterprise");
  const [enabledAgents, setEnabledAgents] = useState<string[]>([
    "legal",
    "study",
  ]);

  const token =
    typeof window !== "undefined" ? localStorage.getItem("token") : null;

  const totalEnterpriseCredits = useMemo(() => {
    return enterprises.reduce(
      (sum, item) => sum + Number(item.credits_balance || 0),
      0
    );
  }, [enterprises]);

  const totalEnterpriseUsage = useMemo(() => {
    return enterprises.reduce(
      (sum, item) => sum + Number(item.total_credits_used || 0),
      0
    );
  }, [enterprises]);

  async function fetchJson(url: string, options: RequestInit = {}) {
    const res = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        ...(options.headers || {}),
      },
    });

    const data = await res.json().catch(() => null);

    if (!res.ok) {
      throw new Error(data?.detail || data?.message || "Request failed");
    }

    return data;
  }

  async function loadEnterprises() {
    try {
      setLoading(true);
      setMessage("");

      const data = await fetchJson(`${API_URL}/admin/enterprises`);

      setEnterprises(Array.isArray(data) ? data : []);
    } catch (error: any) {
      setMessage(error.message || "Unable to load enterprises");
    } finally {
      setLoading(false);
    }
  }

  async function loadEnterpriseDetails(enterprise: any) {
    try {
      setSelectedEnterprise(enterprise);
      setSelectedUsage(null);
      setSelectedMembers([]);

      const [usage, members] = await Promise.all([
        fetchJson(`${API_URL}/admin/enterprises/${enterprise.id}/usage`),
        fetchJson(`${API_URL}/admin/enterprises/${enterprise.id}/members`),
      ]);

      setSelectedUsage(usage);
      setSelectedMembers(Array.isArray(members) ? members : []);
    } catch (error: any) {
      setMessage(error.message || "Unable to load enterprise details");
    }
  }

  useEffect(() => {
    if (!token) {
      window.location.href = "/login";
      return;
    }

    loadEnterprises();
  }, []);

  function toggleAgent(agentSlug: string) {
    setEnabledAgents((prev) =>
      prev.includes(agentSlug)
        ? prev.filter((item) => item !== agentSlug)
        : [...prev, agentSlug]
    );
  }

  async function handleCreateEnterprise() {
    try {
      setActionLoading(true);
      setMessage("");

      if (!name.trim() || !slug.trim() || !ownerEmail.trim()) {
        setMessage("Name, slug, and owner email are required.");
        return;
      }

      await fetchJson(`${API_URL}/admin/enterprises`, {
        method: "POST",
        body: JSON.stringify({
          name: name.trim(),
          slug: slug.trim().toLowerCase(),
          owner_email: ownerEmail.trim().toLowerCase(),
          credits_balance: Number(creditsBalance),
          plan_name: planName.trim() || "enterprise",
          enabled_agents: enabledAgents,
        }),
      });

      setName("");
      setSlug("");
      setOwnerEmail("");
      setCreditsBalance(0);
      setPlanName("enterprise");
      setEnabledAgents(["legal", "study"]);

      setMessage("Enterprise created successfully.");
      await loadEnterprises();
    } catch (error: any) {
      setMessage(error.message || "Unable to create enterprise");
    } finally {
      setActionLoading(false);
    }
  }

  async function handleUpdateCredits(enterprise: any, credits: number) {
    try {
      setActionLoading(true);
      setMessage("");

      await fetchJson(`${API_URL}/admin/enterprises/${enterprise.id}/credits`, {
        method: "PATCH",
        body: JSON.stringify({
          credits_balance: credits,
        }),
      });

      setMessage("Credits updated.");
      await loadEnterprises();
    } catch (error: any) {
      setMessage(error.message || "Unable to update credits");
    } finally {
      setActionLoading(false);
    }
  }

  async function handleToggleStatus(enterprise: any) {
    try {
      setActionLoading(true);
      setMessage("");

      const nextStatus =
        enterprise.status === "active" ? "suspended" : "active";

      await fetchJson(`${API_URL}/admin/enterprises/${enterprise.id}/status`, {
        method: "PATCH",
        body: JSON.stringify({
          status: nextStatus,
        }),
      });

      setMessage(`Enterprise ${nextStatus}.`);
      await loadEnterprises();
    } catch (error: any) {
      setMessage(error.message || "Unable to update status");
    } finally {
      setActionLoading(false);
    }
  }

  async function handleToggleEnterpriseAgent(
    enterprise: any,
    agentSlug: string
  ) {
    try {
      setActionLoading(true);
      setMessage("");

      const currentAgents = Array.isArray(enterprise.enabled_agents)
        ? enterprise.enabled_agents
        : [];

      const nextAgents = currentAgents.includes(agentSlug)
        ? currentAgents.filter((item: string) => item !== agentSlug)
        : [...currentAgents, agentSlug];

      await fetchJson(`${API_URL}/admin/enterprises/${enterprise.id}/agents`, {
        method: "PATCH",
        body: JSON.stringify({
          enabled_agents: nextAgents,
        }),
      });

      setMessage("Enterprise agents updated.");
      await loadEnterprises();
    } catch (error: any) {
      setMessage(error.message || "Unable to update agents");
    } finally {
      setActionLoading(false);
    }
  }

  if (loading) {
    return (
      <main className="min-h-screen bg-gray-50 p-6">
        <div className="mx-auto max-w-7xl">
          <p className="text-gray-600">Loading enterprise accounts...</p>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50 p-6">
      <div className="mx-auto max-w-7xl space-y-8">
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <a
              href="/admin"
              className="text-sm font-medium text-blue-700 hover:underline"
            >
              ← Back to Admin
            </a>

            <h1 className="mt-3 text-3xl font-bold text-gray-900">
              Enterprise Accounts
            </h1>

            <p className="mt-1 text-gray-500">
              Create, manage, suspend, fund, and monitor enterprise workspaces.
            </p>
          </div>

          <button
            onClick={loadEnterprises}
            className="rounded-xl border bg-white px-5 py-3 text-sm font-semibold text-gray-700 hover:bg-gray-50"
          >
            Refresh
          </button>
        </div>

        {message && (
          <div className="rounded-xl border border-blue-200 bg-blue-50 p-4 text-sm font-medium text-blue-800">
            {message}
          </div>
        )}

        <div className="grid gap-4 md:grid-cols-4">
          <div className="rounded-2xl border bg-white p-5">
            <p className="text-sm text-gray-500">Enterprises</p>
            <p className="mt-2 text-3xl font-bold">{enterprises.length}</p>
          </div>

          <div className="rounded-2xl border bg-white p-5">
            <p className="text-sm text-gray-500">Total credits</p>
            <p className="mt-2 text-3xl font-bold">{totalEnterpriseCredits}</p>
          </div>

          <div className="rounded-2xl border bg-white p-5">
            <p className="text-sm text-gray-500">Credits used</p>
            <p className="mt-2 text-3xl font-bold">{totalEnterpriseUsage}</p>
          </div>

          <div className="rounded-2xl border bg-white p-5">
            <p className="text-sm text-gray-500">Active accounts</p>
            <p className="mt-2 text-3xl font-bold">
              {
                enterprises.filter(
                  (item) => (item.status || "active") === "active"
                ).length
              }
            </p>
          </div>
        </div>

        <section className="rounded-2xl border bg-white p-6">
          <h2 className="text-xl font-bold text-gray-900">
            Create Enterprise
          </h2>

          <div className="mt-5 grid gap-4 md:grid-cols-2 lg:grid-cols-5">
            <input
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Company name"
              className="rounded-xl border px-4 py-3 text-sm outline-none focus:border-blue-500"
            />

            <input
              value={slug}
              onChange={(e) => setSlug(e.target.value)}
              placeholder="company-slug"
              className="rounded-xl border px-4 py-3 text-sm outline-none focus:border-blue-500"
            />

            <input
              value={ownerEmail}
              onChange={(e) => setOwnerEmail(e.target.value)}
              placeholder="owner@email.com"
              className="rounded-xl border px-4 py-3 text-sm outline-none focus:border-blue-500"
            />

            <input
              type="number"
              value={creditsBalance}
              onChange={(e) => setCreditsBalance(Number(e.target.value))}
              placeholder="Initial credits"
              className="rounded-xl border px-4 py-3 text-sm outline-none focus:border-blue-500"
            />

            <input
              value={planName}
              onChange={(e) => setPlanName(e.target.value)}
              placeholder="enterprise"
              className="rounded-xl border px-4 py-3 text-sm outline-none focus:border-blue-500"
            />
          </div>

          <div className="mt-5">
            <p className="mb-3 text-sm font-semibold text-gray-700">
              Enabled agents
            </p>

            <div className="flex flex-wrap gap-3">
              {AVAILABLE_AGENTS.map((agent) => (
                <button
                  key={agent.slug}
                  onClick={() => toggleAgent(agent.slug)}
                  className={`rounded-full border px-4 py-2 text-sm font-semibold ${
                    enabledAgents.includes(agent.slug)
                      ? "border-emerald-600 bg-emerald-50 text-emerald-700"
                      : "border-gray-200 bg-white text-gray-500"
                  }`}
                >
                  {agent.label}
                </button>
              ))}
            </div>
          </div>

          <button
            onClick={handleCreateEnterprise}
            disabled={actionLoading}
            className="mt-6 rounded-xl bg-slate-900 px-6 py-3 text-sm font-semibold text-white hover:bg-slate-800 disabled:opacity-60"
          >
            {actionLoading ? "Saving..." : "Create Enterprise"}
          </button>
        </section>

        <section className="overflow-hidden rounded-2xl border bg-white">
          <div className="border-b bg-gray-50 p-5">
            <h2 className="text-xl font-bold text-gray-900">
              Enterprise Accounts
            </h2>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full min-w-[1100px] text-sm">
              <thead className="bg-gray-100 text-gray-600">
                <tr>
                  <th className="p-4 text-left">Company</th>
                  <th className="p-4 text-left">Owner</th>
                  <th className="p-4 text-left">Status</th>
                  <th className="p-4 text-left">Credits</th>
                  <th className="p-4 text-left">Usage</th>
                  <th className="p-4 text-left">Members</th>
                  <th className="p-4 text-left">Agents</th>
                  <th className="p-4 text-right">Actions</th>
                </tr>
              </thead>

              <tbody>
                {enterprises.map((enterprise) => (
                  <tr key={enterprise.id} className="border-t align-top">
                    <td className="p-4">
                      <p className="font-semibold text-gray-900">
                        {enterprise.name}
                      </p>
                      <p className="text-xs text-gray-500">
                        {enterprise.slug} · {enterprise.plan_name}
                      </p>
                    </td>

                    <td className="p-4">
                      {enterprise.owner_email || "—"}
                    </td>

                    <td className="p-4">
                      <span
                        className={`rounded-full px-3 py-1 text-xs font-semibold ${
                          (enterprise.status || "active") === "active"
                            ? "bg-emerald-50 text-emerald-700"
                            : "bg-red-50 text-red-700"
                        }`}
                      >
                        {enterprise.status || "active"}
                      </span>
                    </td>

                    <td className="p-4">
                      <input
                        type="number"
                        defaultValue={enterprise.credits_balance}
                        onBlur={(e) =>
                          handleUpdateCredits(
                            enterprise,
                            Number(e.target.value)
                          )
                        }
                        className="w-24 rounded-lg border px-3 py-2"
                      />
                    </td>

                    <td className="p-4">
                      <p>{enterprise.total_requests || 0} requests</p>
                      <p className="text-xs text-gray-500">
                        {enterprise.total_credits_used || 0} credits used
                      </p>
                    </td>

                    <td className="p-4">
                      <p>{enterprise.members_count || 0} members</p>
                      <p className="text-xs text-gray-500">
                        {enterprise.active_members_count || 0} active
                      </p>
                    </td>

                    <td className="p-4">
                      <div className="flex max-w-xs flex-wrap gap-2">
                        {AVAILABLE_AGENTS.map((agent) => {
                          const isEnabled = enterprise.enabled_agents?.includes(
                            agent.slug
                          );

                          return (
                            <button
                              key={agent.slug}
                              onClick={() =>
                                handleToggleEnterpriseAgent(
                                  enterprise,
                                  agent.slug
                                )
                              }
                              className={`rounded-full border px-3 py-1 text-xs font-semibold ${
                                isEnabled
                                  ? "border-emerald-600 bg-emerald-50 text-emerald-700"
                                  : "border-gray-200 bg-gray-50 text-gray-500"
                              }`}
                            >
                              {agent.slug}
                            </button>
                          );
                        })}
                      </div>
                    </td>

                    <td className="p-4 text-right">
                      <div className="flex justify-end gap-3">
                        <button
                          onClick={() => loadEnterpriseDetails(enterprise)}
                          className="font-medium text-blue-700"
                        >
                          Details
                        </button>

                        <button
                          onClick={() => handleToggleStatus(enterprise)}
                          className={`font-medium ${
                            (enterprise.status || "active") === "active"
                              ? "text-red-700"
                              : "text-emerald-700"
                          }`}
                        >
                          {(enterprise.status || "active") === "active"
                            ? "Suspend"
                            : "Activate"}
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}

                {enterprises.length === 0 && (
                  <tr>
                    <td
                      colSpan={8}
                      className="p-8 text-center text-gray-500"
                    >
                      No enterprise accounts yet.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </section>

        {selectedEnterprise && (
          <section className="rounded-2xl border bg-white p-6">
            <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
              <div>
                <h2 className="text-xl font-bold text-gray-900">
                  {selectedEnterprise.name} details
                </h2>
                <p className="text-sm text-gray-500">
                  Members and usage for this enterprise account.
                </p>
              </div>

              <button
                onClick={() => {
                  setSelectedEnterprise(null);
                  setSelectedUsage(null);
                  setSelectedMembers([]);
                }}
                className="rounded-xl border px-4 py-2 text-sm font-semibold"
              >
                Close
              </button>
            </div>

            <div className="mt-6 grid gap-6 lg:grid-cols-2">
              <div>
                <h3 className="mb-3 font-semibold text-gray-900">Members</h3>

                <div className="space-y-2">
                  {selectedMembers.map((member) => (
                    <div
                      key={member.id}
                      className="rounded-xl border p-4 text-sm"
                    >
                      <p className="font-semibold">{member.email}</p>
                      <p className="text-gray-500">
                        {member.role} · {member.status}
                      </p>
                    </div>
                  ))}

                  {selectedMembers.length === 0 && (
                    <p className="text-sm text-gray-500">No members found.</p>
                  )}
                </div>
              </div>

              <div>
                <h3 className="mb-3 font-semibold text-gray-900">
                  Usage analytics
                </h3>

                <div className="rounded-xl border p-4 text-sm">
                  <p>
                    Total requests:{" "}
                    <strong>{selectedUsage?.total_requests || 0}</strong>
                  </p>

                  <p>
                    Credits used:{" "}
                    <strong>{selectedUsage?.total_credits_used || 0}</strong>
                  </p>
                </div>

                <div className="mt-3 space-y-2">
                  {selectedUsage?.usage_by_agent?.map((item: any) => (
                    <div
                      key={item.agent_slug}
                      className="flex justify-between rounded-xl border p-3 text-sm"
                    >
                      <span className="font-medium capitalize">
                        {item.agent_slug}
                      </span>

                      <span className="text-gray-500">
                        {item.requests} requests · {item.credits_used} credits
                      </span>
                    </div>
                  ))}

                  {!selectedUsage?.usage_by_agent?.length && (
                    <p className="text-sm text-gray-500">No usage yet.</p>
                  )}
                </div>
              </div>
            </div>
          </section>
        )}
      </div>
    </main>
  );
}
