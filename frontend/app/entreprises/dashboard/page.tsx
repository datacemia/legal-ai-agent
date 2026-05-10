"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import {
  Building2,
  Users,
  CreditCard,
  Activity,
  ShieldCheck,
  MailPlus,
  Crown,
  RefreshCw,
  Bot,
  ArrowRight,
} from "lucide-react";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

const connectedAgents = [
  {
    slug: "legal",
    name: "Legal Agent",
    href: "/upload",
    credits: 8,
    description: "Analyze contracts, clauses, obligations, and legal risks.",
  },
  {
    slug: "study",
    name: "Study Agent",
    href: "/study",
    credits: 3,
    description: "Summaries, quizzes, flashcards, and study plans.",
  },
  
  {
    slug: "business",
    name: "Business Decision Agent",
    href: "/business",
    credits: 20,
    description: "Business risks, opportunities, decisions, and action plans.",
  },
];

export default function EntreprisesDashboardPage() {
  const [enterprise, setEnterprise] = useState<any>(null);
  const [members, setMembers] = useState<any[]>([]);
  const [usageSummary, setUsageSummary] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchEnterpriseData = async () => {
    setLoading(true);
    setError("");

    try {
      const token = localStorage.getItem("token");

      if (!token) {
        window.location.href = "/login";
        return;
      }

      const [meRes, membersRes, usageRes] = await Promise.all([
        fetch(`${API_URL}/enterprise/me`, {
          headers: { Authorization: `Bearer ${token}` },
        }),

        fetch(`${API_URL}/enterprise/members`, {
          headers: { Authorization: `Bearer ${token}` },
        }),

        fetch(`${API_URL}/enterprise/usage/summary`, {
          headers: { Authorization: `Bearer ${token}` },
        }),
      ]);

      if (meRes.status === 401) {
        localStorage.removeItem("token");
        window.location.href = "/login";
        return;
      }

      if (meRes.status === 403) {
        window.location.href = "/dashboard";
        return;
      }

      if (!meRes.ok) {
        throw new Error("Enterprise access denied or organization not found.");
      }

      const meData = await meRes.json();

      if (meData?.user?.role !== "enterprise_admin") {
        window.location.href = "/dashboard";
        return;
      }

      const membersData = membersRes.ok ? await membersRes.json() : [];
      const usageData = usageRes.ok ? await usageRes.json() : null;

      setEnterprise(meData);
      setMembers(Array.isArray(membersData) ? membersData : []);
      setUsageSummary(usageData);
    } catch (err: any) {
      setError(err.message || "Unable to load enterprise dashboard.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEnterpriseData();
  }, []);

  if (loading) {
    return (
      <main className="min-h-screen bg-slate-950 p-8 text-white">
        <div className="mx-auto max-w-7xl">
          <div className="rounded-3xl border border-white/10 bg-white/5 p-10">
            Loading enterprise workspace...
          </div>
        </div>
      </main>
    );
  }

  if (error) {
    return (
      <main className="min-h-screen bg-slate-950 p-8 text-white">
        <div className="mx-auto max-w-3xl rounded-3xl border border-red-500/20 bg-red-500/10 p-8">
          <h1 className="text-2xl font-bold">Enterprise access unavailable</h1>
          <p className="mt-3 text-red-100">{error}</p>
          <button
            onClick={fetchEnterpriseData}
            className="mt-6 rounded-xl bg-white px-5 py-3 font-semibold text-slate-950"
          >
            Retry
          </button>
        </div>
      </main>
    );
  }

  const org = enterprise?.organization;
  const user = enterprise?.user;
  const membership = enterprise?.membership;

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <section className="border-b border-white/10 bg-gradient-to-br from-slate-950 via-blue-950 to-slate-900">
        <div className="mx-auto max-w-7xl px-6 py-10">
          <div className="flex flex-col justify-between gap-6 lg:flex-row lg:items-center">
            <div>
              <div className="inline-flex items-center gap-2 rounded-full border border-blue-400/20 bg-blue-400/10 px-4 py-2 text-sm font-semibold text-blue-100">
                <ShieldCheck className="h-4 w-4" />
                Enterprise workspace
              </div>

              <h1 className="mt-5 text-4xl font-bold tracking-tight md:text-5xl">
                {org?.name}
              </h1>

              <p className="mt-3 max-w-2xl text-slate-300">
                Centralized workspace for your organization, team access,
                credits, usage, and enterprise governance.
              </p>
            </div>

            <div className="flex gap-3">
              <button
                onClick={fetchEnterpriseData}
                className="inline-flex items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-5 py-3 text-sm font-semibold text-white hover:bg-white/10"
              >
                <RefreshCw className="h-4 w-4" />
                Refresh
              </button>

              <button className="inline-flex items-center gap-2 rounded-xl bg-white px-5 py-3 text-sm font-bold text-slate-950 hover:bg-blue-50">
                <MailPlus className="h-4 w-4" />
                Invite member
              </button>
            </div>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-6 py-8">
        <div className="grid gap-5 md:grid-cols-4">
          <MetricCard icon={<Building2 className="h-5 w-5" />} label="Plan" value={org?.plan_name || "enterprise"} subtext={`Workspace slug: ${org?.slug}`} />
          <MetricCard icon={<CreditCard className="h-5 w-5" />} label="Credits" value={org?.credits_balance ?? 0} subtext="Shared organization balance" />
          <MetricCard icon={<Users className="h-5 w-5" />} label="Members" value={members.length} subtext="Active team access" />
          <MetricCard
            icon={<Activity className="h-5 w-5" />}
            label="Usage"
            value={usageSummary?.total_requests ?? 0}
            subtext={`${usageSummary?.total_credits_used ?? 0} credits used`}
          />
        </div>

        <div className="mt-8 rounded-3xl border border-white/10 bg-white/[0.03] p-6 shadow-2xl">
          <div className="flex flex-col justify-between gap-4 border-b border-white/10 pb-5 md:flex-row md:items-center">
            <div>
              <h2 className="text-2xl font-bold">Connected AI Agents</h2>
              <p className="mt-1 text-sm text-slate-400">
                Test all connected Runexa agents using shared enterprise organization credits.
              </p>
            </div>

            <span className="rounded-full bg-emerald-500/10 px-3 py-1 text-xs font-semibold text-emerald-300">
              {connectedAgents.length} agents connected
            </span>
          </div>

          <div className="mt-6 grid gap-5 md:grid-cols-2 xl:grid-cols-4">
            {connectedAgents.map((agent) => (
              <Link
                key={agent.slug}
                href={agent.href}
                className="group rounded-2xl border border-white/10 bg-white/[0.04] p-5 transition hover:-translate-y-1 hover:border-blue-400/30 hover:bg-white/[0.07]"
              >
                <div className="flex items-center justify-between">
                  <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-blue-500/10 text-blue-200">
                    <Bot className="h-5 w-5" />
                  </div>

                  <span className="rounded-full bg-emerald-500/10 px-3 py-1 text-xs font-semibold text-emerald-300">
                    Connected
                  </span>
                </div>

                <h3 className="mt-5 text-lg font-bold text-white">
                  {agent.name}
                </h3>

                <p className="mt-2 min-h-[72px] text-sm leading-6 text-slate-400">
                  {agent.description}
                </p>

                <p className="mt-4 text-sm font-semibold text-blue-100">
                  {agent.credits} credits / analysis
                </p>

                <div className="mt-5 inline-flex items-center gap-2 text-sm font-bold text-blue-300 transition group-hover:text-blue-200">
                  Open agent
                  <ArrowRight className="h-4 w-4" />
                </div>
              </Link>
            ))}
          </div>
        </div>

        <div className="mt-8 grid gap-6 lg:grid-cols-[1.4fr_0.8fr]">
          <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-6 shadow-2xl">
            <div className="flex items-center justify-between border-b border-white/10 pb-5">
              <div>
                <h2 className="text-2xl font-bold">Team members</h2>
                <p className="mt-1 text-sm text-slate-400">
                  Manage organization access and enterprise roles.
                </p>
              </div>

              <span className="rounded-full bg-blue-500/10 px-3 py-1 text-xs font-semibold text-blue-200">
                {members.length} member{members.length > 1 ? "s" : ""}
              </span>
            </div>

            <div className="mt-5 space-y-3">
              {members.map((member) => (
                <div
                  key={member.id}
                  className="flex flex-col gap-4 rounded-2xl border border-white/10 bg-white/[0.04] p-4 md:flex-row md:items-center md:justify-between"
                >
                  <div>
                    <div className="flex items-center gap-2">
                      <p className="font-semibold">{member.email}</p>
                      {member.role === "owner" && (
                        <Crown className="h-4 w-4 text-amber-300" />
                      )}
                    </div>
                    <p className="mt-1 text-sm text-slate-400">
                      User ID #{member.user_id} · Member ID #{member.id}
                    </p>
                  </div>

                  <div className="flex flex-wrap gap-2">
                    <span className="rounded-full bg-white/10 px-3 py-1 text-xs font-semibold text-slate-200">
                      {member.role}
                    </span>
                    <span className="rounded-full bg-emerald-500/10 px-3 py-1 text-xs font-semibold text-emerald-300">
                      {member.status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <aside className="space-y-6">
            <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-6">
              <h2 className="text-xl font-bold">Current admin</h2>
              <div className="mt-5 rounded-2xl border border-white/10 bg-white/[0.04] p-4">
                <p className="font-semibold">{user?.email}</p>
                <p className="mt-1 text-sm text-slate-400">
                  Platform role: {user?.role}
                </p>
                <p className="mt-1 text-sm text-slate-400">
                  Organization role: {membership?.role}
                </p>
              </div>
            </div>

            <div className="rounded-3xl border border-blue-400/20 bg-blue-500/10 p-6">
              <h2 className="text-xl font-bold text-blue-50">
                Enterprise controls
              </h2>
              <div className="mt-4 space-y-3 text-sm text-blue-100">
                <p>✔ Organization-level credits</p>
                <p>✔ Team member access</p>
                <p>✔ Enterprise admin gate</p>
                <p>✔ Ready for invite flow</p>
                <p>✔ Ready for usage analytics</p>
              </div>
            </div>
          </aside>

          <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-6">
            <h2 className="text-2xl font-bold">Usage analytics</h2>

            <div className="mt-6 space-y-4">
              {usageSummary?.usage_by_agent?.length ? (
                usageSummary.usage_by_agent.map((agent: any) => (
                  <div
                    key={agent.agent_slug}
                    className="rounded-2xl border border-white/10 bg-white/[0.04] p-4"
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="font-semibold capitalize">
                          {agent.agent_slug}
                        </p>

                        <p className="mt-1 text-sm text-slate-400">
                          {agent.requests} requests
                        </p>
                      </div>

                      <div className="text-right">
                        <p className="text-xl font-bold">
                          {agent.credits_used}
                        </p>

                        <p className="text-sm text-slate-400">
                          credits used
                        </p>
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="rounded-2xl border border-dashed border-white/10 p-6 text-sm text-slate-400">
                  No enterprise usage yet.
                </div>
              )}
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}

function MetricCard({
  icon,
  label,
  value,
  subtext,
}: {
  icon: React.ReactNode;
  label: string;
  value: any;
  subtext: string;
}) {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/[0.04] p-6 shadow-xl">
      <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-blue-500/10 text-blue-200">
        {icon}
      </div>
      <p className="mt-5 text-sm font-semibold uppercase tracking-[0.2em] text-slate-400">
        {label}
      </p>
      <h2 className="mt-2 text-3xl font-bold capitalize">{value}</h2>
      <p className="mt-2 text-sm text-slate-400">{subtext}</p>
    </div>
  );
}