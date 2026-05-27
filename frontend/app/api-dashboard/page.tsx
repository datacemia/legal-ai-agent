"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getSavedLocale } from "../../lib/i18n";

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

const translations = {
  en: {
    dashboard: "Runexa API Dashboard",
    manageAccess: "Manage your API access",
    monitorUsage:
      "Monitor API keys, usage, and Runexa AI agent activity.",
    docs: "Docs",
    upgradeApi: "Upgrade API",
    copyKeyNow: "Copy your API key now",
    activeKeys: "Active Keys",
    totalRequests: "Total Requests",
    creditsUsed: "Credits Used",
    successRate: "Success Rate",
    apiKeys: "API Keys",
    apiKeyName: "API key name",
    createKey: "Create key",
    name: "Name",
    prefix: "Prefix",
    status: "Status",
    action: "Action",
    active: "Active",
    revoked: "Revoked",
    revoke: "Revoke",
    quickstart: "Quickstart",
    recentUsage: "Recent usage",
    couldNotLoad: "Could not load API dashboard data.",
    couldNotConnect: "Could not connect to the API server.",
    couldNotCreate: "Could not create API key.",
    keyCreated:
      "API key created. Copy it now. It will only be shown once.",
    couldNotRevoke: "Could not revoke API key.",
    keyRevoked: "API key revoked.",
  },

  fr: {
    dashboard: "Tableau de bord API Runexa",
    manageAccess: "Gérez votre accès API",
    monitorUsage:
      "Surveillez les clés API, l’utilisation et l’activité des agents IA Runexa.",
    docs: "Documentation",
    upgradeApi: "Mettre à niveau l’API",
    copyKeyNow: "Copiez votre clé API maintenant",
    activeKeys: "Clés actives",
    totalRequests: "Requêtes totales",
    creditsUsed: "Crédits utilisés",
    successRate: "Taux de succès",
    apiKeys: "Clés API",
    apiKeyName: "Nom de la clé API",
    createKey: "Créer une clé",
    name: "Nom",
    prefix: "Préfixe",
    status: "Statut",
    action: "Action",
    active: "Active",
    revoked: "Révoquée",
    revoke: "Révoquer",
    quickstart: "Démarrage rapide",
    recentUsage: "Utilisation récente",
    couldNotLoad:
      "Impossible de charger le tableau de bord API.",
    couldNotConnect:
      "Impossible de se connecter au serveur API.",
    couldNotCreate:
      "Impossible de créer la clé API.",
    keyCreated:
      "Clé API créée. Copiez-la maintenant. Elle ne sera affichée qu’une seule fois.",
    couldNotRevoke:
      "Impossible de révoquer la clé API.",
    keyRevoked: "Clé API révoquée.",
  },

  ar: {
    dashboard: "لوحة تحكم واجهة Runexa API",
    manageAccess: "إدارة الوصول إلى الـ API",
    monitorUsage:
      "راقب مفاتيح API والاستخدام ونشاط وكلاء Runexa.",
    docs: "التوثيق",
    upgradeApi: "ترقية API",
    copyKeyNow: "انسخ مفتاح API الآن",
    activeKeys: "المفاتيح النشطة",
    totalRequests: "إجمالي الطلبات",
    creditsUsed: "الرصيد المستخدم",
    successRate: "معدل النجاح",
    apiKeys: "مفاتيح API",
    apiKeyName: "اسم مفتاح API",
    createKey: "إنشاء مفتاح",
    name: "الاسم",
    prefix: "البادئة",
    status: "الحالة",
    action: "الإجراء",
    active: "نشط",
    revoked: "ملغى",
    revoke: "إلغاء",
    quickstart: "البدء السريع",
    recentUsage: "الاستخدام الأخير",
    couldNotLoad:
      "تعذر تحميل لوحة تحكم API.",
    couldNotConnect:
      "تعذر الاتصال بخادم API.",
    couldNotCreate:
      "تعذر إنشاء مفتاح API.",
    keyCreated:
      "تم إنشاء مفتاح API. انسخه الآن لأنه سيظهر مرة واحدة فقط.",
    couldNotRevoke:
      "تعذر إلغاء مفتاح API.",
    keyRevoked: "تم إلغاء مفتاح API.",
  },
};

export default function ApiDashboardPage() {
  const [keys, setKeys] = useState<ApiKey[]>([]);
  const [usage, setUsage] = useState<ApiUsage[]>([]);
  const [newKeyName, setNewKeyName] = useState("Production API Key");
  const [createdKey, setCreatedKey] = useState("");
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  const locale = getSavedLocale();

  const t =
    translations[locale as keyof typeof translations] ||
    translations.en;


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
        setMessage(t.couldNotLoad);
        return;
      }

      setKeys(await keysRes.json());
      setUsage(await usageRes.json());
    } catch {
      setMessage(t.couldNotConnect);
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
      setMessage(data.detail || t.couldNotCreate);
      return;
    }

    setCreatedKey(data.api_key);
    setMessage(t.keyCreated);
    await loadData();
  }

  async function revokeKey(id: number) {
    if (!token) return;

    const res = await fetch(`${API_URL}/api-keys/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!res.ok) {
      setMessage(t.couldNotRevoke);
      return;
    }

    setMessage(t.keyRevoked);
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
        <p className="font-semibold text-blue-600">{t.dashboard}</p>

        <div className="mt-4 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div>
            <h1 className="text-5xl font-bold tracking-tight">
              {t.manageAccess}
            </h1>
            <p className="mt-4 max-w-3xl text-lg leading-8 text-slate-600">
              {t.monitorUsage}
            </p>
          </div>

          <div className="flex gap-3">
            <Link href="/docs" className="rounded-xl border bg-white px-5 py-3 text-sm font-bold">
              {t.docs}
            </Link>
            <Link href="/pricing" className="rounded-xl bg-blue-600 px-5 py-3 text-sm font-bold text-white">
              {t.upgradeApi}
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
          <p className="font-bold text-amber-900">{t.copyKeyNow}</p>
          <code className="mt-3 block break-all rounded-xl bg-white p-4 text-sm text-slate-900">
            {createdKey}
          </code>
        </div>
      )}

      <section className="mx-auto mt-12 grid max-w-6xl gap-6 md:grid-cols-4">
        {[
          [t.activeKeys, activeKeys],
          [t.totalRequests, totalRequests],
          [t.creditsUsed, creditsUsed],
          [t.successRate, successRate],
        ].map(([label, value]) => (
          <div key={label} className="rounded-3xl border bg-white p-6 shadow-sm">
            <p className="text-sm font-semibold text-slate-500">{label}</p>
            <p className="mt-3 text-3xl font-bold">{value}</p>
          </div>
        ))}
      </section>

      <section className="mx-auto mt-10 grid max-w-6xl gap-6 lg:grid-cols-[1.2fr_0.8fr]">
        <div className="rounded-3xl border bg-white p-6 shadow-sm">
          <h2 className="text-2xl font-bold">{t.apiKeys}</h2>

          <div className="mt-5 flex gap-3">
            <input
              value={newKeyName}
              onChange={(e) => setNewKeyName(e.target.value)}
              className="flex-1 rounded-xl border border-slate-200 px-4 py-3 text-sm"
              placeholder={t.apiKeyName}
            />
            <button
              onClick={createKey}
              className="rounded-xl bg-slate-950 px-5 py-3 text-sm font-bold text-white"
            >
              {t.createKey}
            </button>
          </div>

          <div className="mt-6 overflow-hidden rounded-2xl border">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-50 text-slate-500">
                <tr>
                  <th className="px-4 py-3">{t.name}</th>
                  <th className="px-4 py-3">{t.prefix}</th>
                  <th className="px-4 py-3">{t.status}</th>
                  <th className="px-4 py-3">{t.action}</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {keys.map((key) => (
                  <tr key={key.id}>
                    <td className="px-4 py-4 font-semibold">{key.name}</td>
                    <td className="px-4 py-4 font-mono">{key.key_prefix}</td>
                    <td className="px-4 py-4">
                      {key.is_active ? t.active : t.revoked}
                    </td>
                    <td className="px-4 py-4">
                      {key.is_active && (
                        <button
                          onClick={() => revokeKey(key.id)}
                          className="text-sm font-bold text-red-600"
                        >
                          {t.revoke}
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
          <h2 className="text-2xl font-bold">{t.quickstart}</h2>
          <pre className="mt-5 overflow-x-auto rounded-2xl border border-white/10 bg-white/5 p-4 text-xs">
{`curl -X POST "https://api.runexa.ai/v1/finance/analyze" \\
  -H "Authorization: Bearer rk_live_xxx" \\
  -F "file=@statement.pdf" \\
  -F "output_language=en"`}
          </pre>
        </div>
      </section>

      <section className="mx-auto mt-10 max-w-6xl rounded-3xl border bg-white p-6 shadow-sm">
        <h2 className="text-2xl font-bold">{t.recentUsage}</h2>

        <div className="mt-6 overflow-hidden rounded-2xl border">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-50 text-slate-500">
              <tr>
                <th className="px-4 py-3">Endpoint</th>
                <th className="px-4 py-3">Agent</th>
                <th className="px-4 py-3">{t.creditsUsed}</th>
                <th className="px-4 py-3">{t.status}</th>
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