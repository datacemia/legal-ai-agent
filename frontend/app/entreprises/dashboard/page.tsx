"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getSavedLocale } from "../../../lib/i18n";
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
  Scale,
  GraduationCap,
  Wallet,
  Briefcase,
} from "lucide-react";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "https://api.runexa.ai";

const AGENT_CATALOG: Record<
  string,
  {
    href: string;
    icon: typeof Scale;
    name: Record<string, string>;
    description: Record<string, string>;
  }
> = {
  legal: {
    href: "/upload",
    icon: Scale,
    name: {
      en: "Legal Agent",
      fr: "Agent juridique",
      ar: "الوكيل القانوني",
    },
    description: {
      en: "Analyze contracts, clauses, obligations, and legal risks.",
      fr: "Analyse les contrats, clauses, obligations et risques juridiques.",
      ar: "تحليل العقود والبنود والالتزامات والمخاطر القانونية.",
    },
  },

  study: {
    href: "/study",
    icon: GraduationCap,
    name: {
      en: "Study Agent",
      fr: "Agent étude",
      ar: "وكيل الدراسة",
    },
    description: {
      en: "Summaries, quizzes, flashcards, and study plans.",
      fr: "Résumés, quiz, flashcards et plans de révision.",
      ar: "ملخصات واختبارات وبطاقات تعليمية وخطط دراسة.",
    },
  },

  finance: {
    href: "/finance",
    icon: Wallet,
    name: {
      en: "Finance Coach Agent",
      fr: "Agent coach financier",
      ar: "وكيل المدرب المالي",
    },
    description: {
      en: "Analyze spending, bank statements, waste, and savings.",
      fr: "Analyse les dépenses, relevés bancaires, gaspillage et économies.",
      ar: "تحليل المصاريف والكشوف البنكية والهدر والادخار.",
    },
  },

  business: {
    href: "/business",
    icon: Briefcase,
    name: {
      en: "Business Decision Agent",
      fr: "Agent décision business",
      ar: "وكيل قرارات الأعمال",
    },
    description: {
      en: "Business risks, opportunities, decisions, and action plans.",
      fr: "Risques, opportunités, décisions et plans d’action business.",
      ar: "مخاطر وفرص الأعمال وخطط العمل واتخاذ القرار.",
    },
  },
};


const translations = {
  en: {
    workspace: "Enterprise workspace",
    workspaceDesc:
      "Centralized workspace for your organization, team access, credits, usage, and enterprise governance.",
    refresh: "Refresh",
    inviting: "Inviting...",
    inviteMember: "Invite member",
    plan: "Plan",
    credits: "Credits",
    sharedBalance: "Shared organization balance",
    members: "Members",
    activeTeam: "Active team access",
    usage: "Usage",
    creditsUsed: "credits used",
    connectedAgents: "Connected AI Agents",
    connectedAgentsDesc:
      "Test all connected Runexa agents using shared enterprise organization credits.",
    connected: "Connected",
    openAgent: "Open agent",
    noAgents:
      "No agents are enabled for this enterprise workspace yet.",
    teamMembers: "Team members",
    manageAccess:
      "Manage organization access and enterprise roles.",
    membershipAccess:
      "Your organization membership and workspace access.",
    suspend: "Suspend",
    activate: "Activate",
    remove: "Remove",
    enabled: "Enabled",
    save: "Save",
    currentUser: "Current user",
    platformRole: "Platform role",
    organizationRole: "Organization role",
    fullListAdmins:
      "Full member list is available to organization owners/admins.",
    loadingWorkspace: "Loading enterprise workspace...",
    accessUnavailable: "Enterprise access unavailable",
    retry: "Retry",
    member: "member",
    admin: "admin",
    used: "Used",
    accessQuotas: "Agent access & quotas",
    agentsConnected: "agents connected",
    enterpriseControls: "Enterprise controls",
    usageAnalytics: "Usage analytics",
    requests: "requests",
    userId: "User ID",
    memberId: "Member ID",
    saveShort: "Save",
    membersLabel: "members",
    owner: "owner",
    active: "active",
    suspended: "suspended",
    organizationCredits: "Organization-level credits",
    teamAccess: "Team member access",
    workspaceAccess: "Enterprise workspace access",
    usageReady: "Ready for usage analytics",
    inviteReady: "Ready for invite flow",
  },

  fr: {
    workspace: "Espace entreprise",
    workspaceDesc:
      "Espace centralisé pour votre organisation, les accès équipe, les crédits, l’utilisation et la gouvernance entreprise.",
    refresh: "Actualiser",
    inviting: "Invitation...",
    inviteMember: "Inviter un membre",
    plan: "Plan",
    credits: "Crédits",
    sharedBalance: "Solde partagé de l’organisation",
    members: "Membres",
    activeTeam: "Accès équipe actif",
    usage: "Utilisation",
    creditsUsed: "crédits utilisés",
    connectedAgents: "Agents IA connectés",
    connectedAgentsDesc:
      "Testez tous les agents Runexa connectés avec les crédits partagés de l’entreprise.",
    connected: "Connecté",
    openAgent: "Ouvrir l’agent",
    noAgents:
      "Aucun agent activé pour cet espace entreprise.",
    teamMembers: "Membres de l’équipe",
    manageAccess:
      "Gérer les accès et rôles entreprise.",
    membershipAccess:
      "Votre accès et appartenance à l’organisation.",
    suspend: "Suspendre",
    activate: "Activer",
    remove: "Supprimer",
    enabled: "Activé",
    save: "Enregistrer",
    currentUser: "Utilisateur actuel",
    platformRole: "Rôle plateforme",
    organizationRole: "Rôle organisation",
    fullListAdmins:
      "La liste complète est réservée aux admins/propriétaires.",
    loadingWorkspace: "Chargement de l’espace entreprise...",
    accessUnavailable: "Accès entreprise indisponible",
    retry: "Réessayer",
    member: "membre",
    admin: "admin",
    used: "Utilisé",
    accessQuotas: "Accès agents et quotas",
    agentsConnected: "agents connectés",
    enterpriseControls: "Contrôles entreprise",
    usageAnalytics: "Analyse d’utilisation",
    requests: "requêtes",
    userId: "ID utilisateur",
    memberId: "ID membre",
    saveShort: "Sauver",
    membersLabel: "membres",
    owner: "propriétaire",
    active: "actif",
    suspended: "suspendu",
    organizationCredits: "Crédits organisation",
    teamAccess: "Accès équipe",
    workspaceAccess: "Accès espace entreprise",
    usageReady: "Prêt pour les analyses d’utilisation",
    inviteReady: "Prêt pour les invitations",
  },

  ar: {
    workspace: "مساحة المؤسسة",
    workspaceDesc:
      "مساحة مركزية للمؤسسة وإدارة الفريق والأرصدة والاستخدام والصلاحيات.",
    refresh: "تحديث",
    inviting: "جارٍ إرسال الدعوة...",
    inviteMember: "دعوة عضو",
    plan: "الخطة",
    credits: "الرصيد",
    sharedBalance: "الرصيد المشترك للمؤسسة",
    members: "الأعضاء",
    activeTeam: "وصول الفريق النشط",
    usage: "الاستخدام",
    creditsUsed: "رصيد مستخدم",
    connectedAgents: "وكلاء الذكاء الاصطناعي المتصلون",
    connectedAgentsDesc:
      "اختبر جميع وكلاء Runexa باستخدام رصيد المؤسسة المشترك.",
    connected: "متصل",
    openAgent: "فتح الوكيل",
    noAgents:
      "لا توجد وكلاء مفعلة لهذه المؤسسة.",
    teamMembers: "أعضاء الفريق",
    manageAccess:
      "إدارة الوصول والأدوار داخل المؤسسة.",
    membershipAccess:
      "وصولك وعضويتك داخل المؤسسة.",
    suspend: "تعليق",
    activate: "تفعيل",
    remove: "إزالة",
    enabled: "مفعل",
    save: "حفظ",
    currentUser: "المستخدم الحالي",
    platformRole: "دور المنصة",
    organizationRole: "دور المؤسسة",
    fullListAdmins:
      "القائمة الكاملة متاحة فقط للمسؤولين.",
    loadingWorkspace: "جارٍ تحميل مساحة المؤسسة...",
    accessUnavailable: "الوصول للمؤسسة غير متاح",
    retry: "إعادة المحاولة",
    member: "عضو",
    admin: "مسؤول",
    used: "المستخدم",
    accessQuotas: "صلاحيات الوكلاء والحصص",
    agentsConnected: "وكلاء متصلون",
    enterpriseControls: "إعدادات المؤسسة",
    usageAnalytics: "تحليلات الاستخدام",
    requests: "طلبات",
    userId: "معرف المستخدم",
    memberId: "معرف العضو",
    saveShort: "حفظ",
    membersLabel: "أعضاء",
    owner: "مالك",
    active: "نشط",
    suspended: "معلق",
    organizationCredits: "رصيد المؤسسة",
    teamAccess: "وصول أعضاء الفريق",
    workspaceAccess: "الوصول إلى مساحة المؤسسة",
    usageReady: "جاهز لتحليلات الاستخدام",
    inviteReady: "جاهز لنظام الدعوات",
  },
};


export default function EntreprisesDashboardPage() {
  const [enterprise, setEnterprise] = useState<any>(null);
  const [members, setMembers] = useState<any[]>([]);
  const [usageSummary, setUsageSummary] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [inviteEmail, setInviteEmail] = useState("");
  const [inviteRole, setInviteRole] = useState("member");
  const [inviteMessage, setInviteMessage] = useState("");
  const [inviteLoading, setInviteLoading] = useState(false);
  const [memberActionLoading, setMemberActionLoading] = useState<number | null>(null);
  const [memberAgentAccess, setMemberAgentAccess] = useState<Record<number, any[]>>({});
  const [agentAccessLoading, setAgentAccessLoading] = useState<number | null>(null);

  const locale = getSavedLocale();

  const t =
    translations[locale as keyof typeof translations] ||
    translations.en;

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

      let membersData = [];

      if (membersRes.ok) {
        membersData = await membersRes.json();
      } else if (membersRes.status === 403) {
        membersData = [];
      } else {
        membersData = [];
      }

      const usageData = usageRes.ok ? await usageRes.json() : null;

      setEnterprise(meData);
      setMembers(Array.isArray(membersData) ? membersData : []);

      if (Array.isArray(membersData)) {
        membersData.forEach((member: any) => {
          fetchMemberAgentAccess(member.id);
        });
      }
      setUsageSummary(usageData);
    } catch (err: any) {
      setError(err.message || "Unable to load enterprise dashboard.");
    } finally {
      setLoading(false);
    }
  };

  const handleInvite = async () => {
    try {
      setInviteLoading(true);
      setInviteMessage("");

      const token = localStorage.getItem("token");

      const res = await fetch(
        `${API_URL}/enterprise/invite`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            email: inviteEmail.trim(),
            role: inviteRole,
          }),
        }
      );

      const data = await res.json();

      if (!res.ok) {
        setInviteMessage(data.detail || "Invite failed");
        return;
      }

      setInviteMessage("Member invited successfully");
      setInviteEmail("");

      fetchEnterpriseData();
    } catch (err) {
      setInviteMessage("Error inviting member");
    } finally {
      setInviteLoading(false);
    }
  };

  const handleUpdateRole = async (
    memberId: number,
    role: string
  ) => {
    try {
      setMemberActionLoading(memberId);

      const token = localStorage.getItem("token");

      const res = await fetch(
        `${API_URL}/enterprise/members/${memberId}/role`,
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            role,
          }),
        }
      );

      const data = await res.json();

      if (!res.ok) {
        alert(data.detail || "Unable to update role");
        return;
      }

      fetchEnterpriseData();
    } catch (err) {
      alert("Failed to update role");
    } finally {
      setMemberActionLoading(null);
    }
  };

  const handleSuspendMember = async (
    memberId: number,
    currentStatus: string
  ) => {
    try {
      setMemberActionLoading(memberId);

      const token = localStorage.getItem("token");

      const nextStatus =
        currentStatus === "active" ? "suspended" : "active";

      const res = await fetch(
        `${API_URL}/enterprise/members/${memberId}/suspend`,
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            status: nextStatus,
          }),
        }
      );

      const data = await res.json();

      if (!res.ok) {
        alert(data.detail || "Unable to update member status");
        return;
      }

      fetchEnterpriseData();
    } catch (err) {
      alert("Failed to update member status");
    } finally {
      setMemberActionLoading(null);
    }
  };

  const handleRemoveMember = async (memberId: number) => {
    const confirmed = window.confirm(
      "Remove this member from the organization?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setMemberActionLoading(memberId);

      const token = localStorage.getItem("token");

      const res = await fetch(
        `${API_URL}/enterprise/members/${memberId}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await res.json();

      if (!res.ok) {
        alert(data.detail || "Unable to remove member");
        return;
      }

      fetchEnterpriseData();
    } catch (err) {
      alert("Failed to remove member");
    } finally {
      setMemberActionLoading(null);
    }
  };

  const fetchMemberAgentAccess = async (memberId: number) => {
    const token = localStorage.getItem("token");

    const res = await fetch(
      `${API_URL}/enterprise/member-agent-access/${memberId}`,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );

    if (!res.ok) return;

    const data = await res.json();

    setMemberAgentAccess((prev) => ({
      ...prev,
      [memberId]: data,
    }));
  };

  const handleSaveAgentAccess = async (
    memberId: number,
    agentSlug: string,
    isEnabled: boolean,
    quota: number
  ) => {
    try {
      setAgentAccessLoading(memberId);

      const token = localStorage.getItem("token");

      const res = await fetch(
        `${API_URL}/enterprise/member-agent-access/${memberId}`,
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            agent_slug: agentSlug,
            is_enabled: isEnabled,
            analysis_quota: quota,
          }),
        }
      );

      const data = await res.json();

      if (!res.ok) {
        alert(data.detail || "Unable to save agent access");
        return;
      }

      await fetchMemberAgentAccess(memberId);
    } catch (err) {
      alert("Failed to save agent access");
    } finally {
      setAgentAccessLoading(null);
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
            {t.loadingWorkspace}
          </div>
        </div>
      </main>
    );
  }

  if (error) {
    return (
      <main className="min-h-screen bg-slate-950 p-8 text-white">
        <div className="mx-auto max-w-3xl rounded-3xl border border-red-500/20 bg-red-500/10 p-8">
          <h1 className="text-2xl font-bold">{t.accessUnavailable}</h1>
          <p className="mt-3 text-red-100">{error}</p>
          <button
            onClick={fetchEnterpriseData}
            className="mt-6 rounded-xl bg-white px-5 py-3 font-semibold text-slate-950"
          >
            {t.retry}
          </button>
        </div>
      </main>
    );
  }

  const org = enterprise?.organization;
  const user = enterprise?.user;
  const membership = enterprise?.membership;

  const enabledAgentSlugs = Array.isArray(org?.enabled_agents)
    ? org.enabled_agents.filter(
        (slug: string) => slug !== "finance"
      )
    : [];

  const connectedAgents = enabledAgentSlugs
    .map((slug: string) => ({
      slug,
      ...(AGENT_CATALOG[slug] || {
        href: `/${slug}`,
        icon: Bot,
        name: {
          en: `${slug} Agent`,
          fr: `${slug} Agent`,
          ar: `${slug} Agent`,
        },
        description: {
          en: `${slug} enterprise agent`,
          fr: `${slug} enterprise agent`,
          ar: `${slug} enterprise agent`,
        },
      }),
    }))
    .filter((agent: any) => Boolean(agent.slug));

  const isOwnerOrAdmin =
    user?.role === "enterprise_admin" ||
    membership?.role === "owner" ||
    membership?.role === "admin";

  const memberCount = members.length || (membership ? 1 : 0);

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <section className="border-b border-white/10 bg-gradient-to-br from-slate-950 via-blue-950 to-slate-900">
        <div className="mx-auto max-w-7xl px-6 py-10">
          <div className="flex flex-col justify-between gap-6 lg:flex-row lg:items-center">
            <div>
              <div className="inline-flex items-center gap-2 rounded-full border border-blue-400/20 bg-blue-400/10 px-4 py-2 text-sm font-semibold text-blue-100">
                <ShieldCheck className="h-4 w-4" />
                {t.workspace}
              </div>

              <h1 className="mt-5 text-4xl font-bold tracking-tight md:text-5xl">
                {org?.name}
              </h1>

              <p className="mt-3 max-w-2xl text-slate-300">
                {t.workspaceDesc}
              </p>
            </div>

            <div className="flex gap-3">
              <button
                onClick={fetchEnterpriseData}
                className="inline-flex items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-5 py-3 text-sm font-semibold text-white hover:bg-white/10"
              >
                <RefreshCw className="h-4 w-4" />
                {t.refresh}
              </button>

              {isOwnerOrAdmin && (
                <div className="flex flex-col gap-3">
                  <div className="flex gap-2">
                    <input
                      type="email"
                      placeholder="member@email.com"
                      value={inviteEmail}
                      onChange={(e) => setInviteEmail(e.target.value)}
                      className="rounded-xl border border-white/10 bg-white/10 px-4 py-2 text-sm text-white outline-none"
                    />

                    <select
                      value={inviteRole}
                      onChange={(e) => setInviteRole(e.target.value)}
                      className="rounded-xl border border-white/10 bg-slate-900 px-3 py-2 text-sm text-white"
                    >
                      <option value="member">{t.member}</option>
                      <option value="admin">{t.admin}</option>
                    </select>

                    <button
                      onClick={handleInvite}
                      disabled={inviteLoading}
                      className="inline-flex items-center gap-2 rounded-xl bg-white px-5 py-3 text-sm font-bold text-slate-950 hover:bg-blue-50 disabled:cursor-not-allowed disabled:opacity-70"
                    >
                      <MailPlus className="h-4 w-4" />
                      {inviteLoading ? t.inviting : t.inviteMember}
                    </button>
                  </div>

                  {inviteMessage && (
                    <p className="text-sm text-blue-100">
                      {inviteMessage}
                    </p>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-6 py-8">
        <div className="grid gap-5 md:grid-cols-4">
          <MetricCard
            icon={<Building2 className="h-5 w-5" />}
            label={t.plan}
            value={org?.plan_name || "enterprise"}
            subtext={`Workspace slug: ${org?.slug}`}
          />

          <MetricCard
            icon={<CreditCard className="h-5 w-5" />}
            label={t.credits}
            value={org?.credits_balance ?? 0}
            subtext={t.sharedBalance}
          />

          <MetricCard
            icon={<Users className="h-5 w-5" />}
            label={t.members}
            value={memberCount}
            subtext={t.activeTeam}
          />

          <MetricCard
            icon={<Activity className="h-5 w-5" />}
            label={t.usage}
            value={usageSummary?.total_requests ?? 0}
            subtext={`${usageSummary?.total_credits_used ?? 0} ${t.creditsUsed}`}
          />
        </div>

        <div className="mt-8 rounded-3xl border border-white/10 bg-white/[0.03] p-6 shadow-2xl">
          <div className="flex flex-col justify-between gap-4 border-b border-white/10 pb-5 md:flex-row md:items-center">
            <div>
              <h2 className="text-2xl font-bold">{t.connectedAgents}</h2>
              <p className="mt-1 text-sm text-slate-400">
                {t.connectedAgentsDesc}
              </p>
            </div>

            <span className="rounded-full bg-emerald-500/10 px-3 py-1 text-xs font-semibold text-emerald-300">
              {connectedAgents.length} {t.agentsConnected}
            </span>
          </div>

          <div className="mt-6 grid gap-5 md:grid-cols-2 xl:grid-cols-3">
            {connectedAgents.length > 0 ? (
              connectedAgents.map((agent: any) => {
                const AgentIcon = agent.icon || Bot;

                return (
                <Link
                  key={agent.slug}
                  href={agent.href}
                  className="group rounded-2xl border border-white/10 bg-white/[0.04] p-5 transition hover:-translate-y-1 hover:border-blue-400/30 hover:bg-white/[0.07]"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-blue-500/10 text-blue-200">
                      <AgentIcon className="h-5 w-5" />
                    </div>

                    <span className="rounded-full bg-emerald-500/10 px-3 py-1 text-xs font-semibold text-emerald-300">
                      {t.connected}
                    </span>
                  </div>

                  <h3 className="mt-5 text-lg font-bold text-white">
                    {agent.name[locale] || agent.name.en}
                  </h3>

                  <p className="mt-2 min-h-[72px] text-sm leading-6 text-slate-400">
                    {agent.description[locale] || agent.description.en}
                  </p>

                  <div className="mt-5 inline-flex items-center gap-2 text-sm font-bold text-blue-300 transition group-hover:text-blue-200">
                    {t.openAgent}
                    <ArrowRight className="h-4 w-4" />
                  </div>
                </Link>
                );
              })
            ) : (
              <div className="rounded-2xl border border-dashed border-white/10 p-6 text-sm text-slate-400 md:col-span-2 xl:col-span-3">
                {t.noAgents}
              </div>
            )}
          </div>
        </div>

        <div className="mt-8 grid gap-6 lg:grid-cols-[1.4fr_0.8fr]">
          <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-6 shadow-2xl">
            <div className="flex items-center justify-between border-b border-white/10 pb-5">
              <div>
                <h2 className="text-2xl font-bold">{t.teamMembers}</h2>
                <p className="mt-1 text-sm text-slate-400">
                  {isOwnerOrAdmin
                    ? t.manageAccess
                    : t.membershipAccess}
                </p>
              </div>

              <span className="rounded-full bg-blue-500/10 px-3 py-1 text-xs font-semibold text-blue-200">
                {memberCount} {t.membersLabel}
              </span>
            </div>

            <div className="mt-5 space-y-3">
              {members.length > 0 ? (
                members.map((member) => (
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
                        {t.userId} #{member.user_id} · {t.memberId} #{member.id}
                      </p>
                    </div>

                    <div className="flex flex-wrap items-center gap-2">
                      <span className="rounded-full bg-white/10 px-3 py-1 text-xs font-semibold text-slate-200">
                        {member.role === "owner"
                          ? t.owner
                          : member.role === "admin"
                            ? t.admin
                            : t.member}
                      </span>

                      <span
                        className={`rounded-full px-3 py-1 text-xs font-semibold ${
                          member.status === "active"
                            ? "bg-emerald-500/10 text-emerald-300"
                            : "bg-red-500/10 text-red-300"
                        }`}
                      >
                        {member.status === "active" ? t.active : t.suspended}
                      </span>

                      {isOwnerOrAdmin && member.role !== "owner" && (
                        <>
                          <select
                            value={member.role}
                            disabled={memberActionLoading === member.id}
                            onChange={(e) =>
                              handleUpdateRole(member.id, e.target.value)
                            }
                            className="rounded-xl border border-white/10 bg-slate-900 px-3 py-2 text-xs text-white"
                          >
                            <option value="member">{t.member}</option>
                            <option value="admin">{t.admin}</option>
                          </select>

                          <button
                            onClick={() =>
                              handleSuspendMember(
                                member.id,
                                member.status
                              )
                            }
                            disabled={memberActionLoading === member.id}
                            className="rounded-xl border border-amber-500/20 bg-amber-500/10 px-3 py-2 text-xs font-semibold text-amber-200 hover:bg-amber-500/20"
                          >
                            {member.status === "active"
                              ? t.suspend
                              : t.activate}
                          </button>

                          <button
                            onClick={() =>
                              handleRemoveMember(member.id)
                            }
                            disabled={memberActionLoading === member.id}
                            className="rounded-xl border border-red-500/20 bg-red-500/10 px-3 py-2 text-xs font-semibold text-red-200 hover:bg-red-500/20"
                          >
                            {t.remove}
                          </button>
                        </>
                      )}
                    </div>

                    {isOwnerOrAdmin && (
                      <div className="w-full rounded-2xl border border-white/10 bg-slate-950/40 p-4">
                        <p className="mb-3 text-sm font-bold text-slate-200">
                          {t.accessQuotas}
                        </p>

                        <div className="grid gap-3 md:grid-cols-3">
                          {(memberAgentAccess[member.id] || []).map((agent: any) => (
                            <div
                              key={agent.agent_slug}
                              className="rounded-xl border border-white/10 bg-white/[0.04] p-3"
                            >
                              <p className="font-semibold capitalize">
                                {agent.agent_slug}
                              </p>

                              <p className="mt-1 text-xs text-slate-400">
                                {t.used}: {agent.analyses_used} / {agent.analysis_quota}
                              </p>

                              <label className="mt-3 flex items-center gap-2 text-xs text-slate-300">
                                <input
                                  type="checkbox"
                                  defaultChecked={agent.is_enabled}
                                  onChange={(e) => {
                                    agent.is_enabled = e.target.checked;
                                  }}
                                />
                                {t.enabled}
                              </label>

                              <input
                                type="number"
                                min={0}
                                defaultValue={agent.analysis_quota}
                                onChange={(e) => {
                                  agent.analysis_quota = Number(e.target.value);
                                }}
                                className="mt-3 w-full rounded-lg border border-white/10 bg-slate-900 px-3 py-2 text-xs text-white"
                              />

                              <button
                                onClick={() =>
                                  handleSaveAgentAccess(
                                    member.id,
                                    agent.agent_slug,
                                    agent.is_enabled,
                                    agent.analysis_quota
                                  )
                                }
                                disabled={agentAccessLoading === member.id}
                                className="mt-3 w-full rounded-lg bg-blue-600 px-3 py-2 text-xs font-bold text-white hover:bg-blue-500 disabled:opacity-60"
                              >
                                {t.saveShort}
                              </button>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ))
              ) : (
                <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-4">
                  <p className="font-semibold">{user?.email}</p>
                  <p className="mt-1 text-sm text-slate-400">
                    {t.platformRole}: {user?.role}
                  </p>
                  <p className="mt-1 text-sm text-slate-400">
                    {t.organizationRole}: {membership?.role || t.member}
                  </p>
                  {!isOwnerOrAdmin && (
                    <p className="mt-3 text-xs text-slate-500">
                      {t.fullListAdmins}
                    </p>
                  )}
                </div>
              )}
            </div>
          </div>

          <aside className="space-y-6">
            <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-6">
              <h2 className="text-xl font-bold">{t.currentUser}</h2>
              <div className="mt-5 rounded-2xl border border-white/10 bg-white/[0.04] p-4">
                <p className="font-semibold">{user?.email}</p>
                <p className="mt-1 text-sm text-slate-400">
                  {t.platformRole}: {user?.role}
                </p>
                <p className="mt-1 text-sm text-slate-400">
                  {t.organizationRole}: {membership?.role}
                </p>
              </div>
            </div>

            <div className="rounded-3xl border border-blue-400/20 bg-blue-500/10 p-6">
              <h2 className="text-xl font-bold text-blue-50">
                {t.enterpriseControls}
              </h2>
              <div className="mt-4 space-y-3 text-sm text-blue-100">
                <p>✔ {t.organizationCredits}</p>
                <p>✔ {t.teamAccess}</p>
                <p>✔ {t.workspaceAccess}</p>
                <p>✔ {t.usageReady}</p>
                {isOwnerOrAdmin && <p>✔ {t.inviteReady}</p>}
              </div>
            </div>
          </aside>

          <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-6">
            <h2 className="text-2xl font-bold">{t.usageAnalytics}</h2>

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
                          {agent.requests} {t.requests}
                        </p>
                      </div>

                      <div className="text-right">
                        <p className="text-xl font-bold">
                          {agent.credits_used}
                        </p>

                        <p className="text-sm text-slate-400">
                          {t.creditsUsed}
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
