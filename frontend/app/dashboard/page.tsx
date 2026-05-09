"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  getDocuments,
  getFinanceHistory,
  getStudyHistory,
  getBusinessHistory,
} from "../../lib/api";
import { getToken } from "../../lib/auth";
import RiskBadge from "../../components/RiskBadge";

const labels: any = {
  en: {
    title: "Dashboard",
    subtitle:
      "Manage analyses across all Runexa AI agents with global credits and subscriptions.",
    buy: "Buy credits",
    upgrade: "Upgrade to Pro",
    credits: "Global credits",
    plan: "Current plan",
    new: "New Analysis",
    loading: "Loading dashboard...",
    total: "Total documents",
    completed: "Completed",
    progress: "In progress",
    emptyTitle: "No documents yet",
    emptyDesc: "Upload your first contract to start analyzing.",
    upload: "Upload Contract",
    document: "Document",
    type: "Type",
    language: "Language",
    status: "Status",
    date: "Date",
    action: "Action",
    view: "View",
  },
};

export default function DashboardPage() {
  const [documents, setDocuments] = useState<any[]>([]);
  const [financeData, setFinanceData] = useState<any[]>([]);
  const [studyData, setStudyData] = useState<any[]>([]);
  const [businessData, setBusinessData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [locale, setLocale] = useState("en");

  const t = labels[locale] || labels.en;

  const parseFinanceResult = (value: any) => {
    try {
      return typeof value === "string" ? JSON.parse(value) : value || {};
    } catch {
      return {};
    }
  };

  useEffect(() => {
    const saved = localStorage.getItem("locale") || "en";
    setLocale(saved);

    const token = getToken();

    if (!token) {
      window.location.href = "/login";
      return;
    }

    const role = (localStorage.getItem("role") || "").toLowerCase().trim();

    const plan = (localStorage.getItem("plan") || "").toLowerCase().trim();

    if (role === "admin") {
      window.location.href = "/admin";
      return;
    }

    const allowedPlans = ["pro", "premium"];

    if (role !== "admin" && !allowedPlans.includes(plan)) {
      window.location.href = "/pricing";
      return;
    }

    loadDashboard();
  }, []);

  async function loadDashboard() {
    try {
      try {
        const docs = await getDocuments();

        setDocuments(
          Array.isArray(docs)
            ? docs
            : docs?.data || docs?.results || []
        );
      } catch (e) {
        console.error("Documents load failed:", e);
        setDocuments([]);
      }

      try {
        const finance = await getFinanceHistory();

        setFinanceData(
          Array.isArray(finance)
            ? finance
            : finance?.data || finance?.results || []
        );
      } catch (e) {
        console.error("Finance history failed:", e);
        setFinanceData([]);
      }

      try {
        const study = await getStudyHistory();

        setStudyData(
          Array.isArray(study)
            ? study
            : study?.data || study?.results || []
        );
      } catch (e) {
        console.error("Study history failed:", e);
        setStudyData([]);
      }

      try {
        const business = await getBusinessHistory();

        setBusinessData(
          Array.isArray(business)
            ? business
            : business?.data || business?.results || []
        );
      } catch (e) {
        console.error("Business history failed:", e);
        setBusinessData([]);
      }

      setMessage("");
    } finally {
      setLoading(false);
    }
  }

  const handleBuyCredit = async () => {
    setMessage(
      "Stripe is not configured yet. Credits and subscriptions will be available soon."
    );
  };

  if (loading) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-slate-50">
        <p className="text-slate-600">{t.loading}</p>
      </main>
    );
  }

  return (
    <main
      dir={locale === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-4 py-8"
    >
      <div className="max-w-6xl mx-auto space-y-8">
        <div className="flex flex-col md:flex-row md:justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold">{t.title}</h1>
            <p className="text-slate-500 mt-1">{t.subtitle}</p>
          </div>

          <div className="flex flex-wrap gap-3">
            <button
              onClick={handleBuyCredit}
              className="px-5 py-2 bg-green-600 text-white rounded-xl"
            >
              {t.buy}
            </button>

            <button
              onClick={() =>
                setMessage(
                  "Pro subscription is not configured yet. Stripe will be activated soon."
                )
              }
              className="px-5 py-2 bg-blue-600 text-white rounded-xl"
            >
              {t.upgrade}
            </button>

            <Link
              href="/upload"
              className="px-5 py-2 bg-slate-900 text-white rounded-xl"
            >
              {t.new}
            </Link>
          </div>
        </div>

        {message && (
          <div className="bg-red-50 text-red-700 border border-red-200 text-sm p-3 rounded-xl text-center">
            {message}
          </div>
        )}

        <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
          <div className="bg-white p-5 rounded-2xl border">
            <p className="text-sm text-slate-500">{t.plan}</p>
            <p className="text-2xl font-bold uppercase">
              {localStorage.getItem("plan") || "trial"}
            </p>
          </div>

          <div className="bg-white p-5 rounded-2xl border">
            <p className="text-sm text-slate-500">{t.credits}</p>
            <p className="text-2xl font-bold">
              {localStorage.getItem("credits_balance") || 0}
            </p>
          </div>

          <div className="bg-white p-5 rounded-2xl border">
            <p className="text-sm text-slate-500">{t.total}</p>
            <p className="text-2xl font-bold">{documents.length}</p>
          </div>

          <div className="bg-white p-5 rounded-2xl border">
            <p className="text-sm text-slate-500">{t.completed}</p>
            <p className="text-2xl font-bold">
              {documents.filter((d) => d.status === "completed").length}
            </p>
          </div>

          <div className="bg-white p-5 rounded-2xl border">
            <p className="text-sm text-slate-500">{t.progress}</p>
            <p className="text-2xl font-bold">
              {documents.filter((d) => d.status !== "completed").length}
            </p>
          </div>

          <div className="bg-white p-5 rounded-2xl border">
            <p className="text-sm text-slate-500">Total analyses</p>
            <p className="text-2xl font-bold">
              {documents.length +
                financeData.length +
                studyData.length +
                businessData.length}
            </p>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl border space-y-4">
          <div className="flex items-center justify-between gap-4">
            <h2 className="text-xl font-semibold">Legal Agent</h2>

            <Link href="/upload" className="text-sm text-blue-600">
              Analyze new
            </Link>
          </div>

          {documents.length === 0 ? (
            <div className="text-center py-8">
              <h3 className="text-lg font-semibold">{t.emptyTitle}</h3>
              <p className="text-slate-500 mt-2">{t.emptyDesc}</p>

              <Link
                href="/upload"
                className="inline-block mt-5 px-5 py-2 bg-slate-900 text-white rounded-lg"
              >
                {t.upload}
              </Link>
            </div>
          ) : (
            <div className="overflow-hidden rounded-2xl border">
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="bg-slate-100 text-slate-600">
                    <tr>
                      <th className="p-4 text-start">{t.document}</th>
                      <th className="p-4 text-start">{t.type}</th>
                      <th className="p-4 text-start">{t.language}</th>
                      <th className="p-4 text-start">{t.status}</th>
                      <th className="p-4 text-start">{t.date}</th>
                      <th className="p-4 text-end">{t.action}</th>
                    </tr>
                  </thead>

                  <tbody>
                    {documents.map((doc) => (
                      <tr key={doc.id} className="border-t hover:bg-slate-50">
                        <td className="p-4 font-medium">{doc.file_name}</td>
                        <td className="p-4">{doc.file_type?.toUpperCase()}</td>
                        <td className="p-4">{doc.language || "—"}</td>
                        <td className="p-4">
                          <RiskBadge
                            risk={doc.status === "completed" ? "low" : "medium"}
                          />
                        </td>
                        <td className="p-4">
                          {new Date(doc.created_at).toLocaleDateString()}
                        </td>
                        <td className="p-4 text-end">
                          <Link
                            href={`/document/${doc.id}`}
                            className="text-blue-600"
                          >
                            {t.view}
                          </Link>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>

        <div className="bg-white p-6 rounded-2xl border space-y-4">
          <div className="flex items-center justify-between gap-4">
            <h2 className="text-xl font-semibold">Study Agent</h2>

            <Link href="/study" className="text-sm text-blue-600">
              Analyze new
            </Link>
          </div>

          {studyData.length === 0 ? (
            <div className="text-center py-8">
              <h3 className="text-lg font-semibold">No study analyses yet</h3>
              <Link
                href="/study"
                className="mt-4 inline-block px-4 py-2 bg-slate-900 text-white rounded"
              >
                Upload Study PDF
              </Link>
            </div>
          ) : (
            <ul className="space-y-2">
              {studyData.slice(0, 3).map((item) => (
                <li key={item.id} className="text-sm border p-3 rounded-xl">
                  {item.file_name}
                </li>
              ))}
            </ul>
          )}

          <div className="flex gap-3 pt-2">
            <Link href="/study" className="text-sm text-blue-600">
              Analyze new
            </Link>

            <Link href="/study/history" className="text-sm text-slate-600">
              View history
            </Link>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl border space-y-4">
          <div className="flex items-center justify-between gap-4">
            <h2 className="text-xl font-semibold">Personal Finance Coach</h2>

            <Link href="/finance" className="text-sm text-blue-600">
              Analyze new
            </Link>
          </div>

          {financeData.length === 0 ? (
            <div className="text-center py-8">
              <h3 className="text-lg font-semibold">No finance analyses yet</h3>
              <p className="text-slate-500 mt-2">
                Upload your first bank statement to start analyzing.
              </p>

              <Link
                href="/finance"
                className="inline-block mt-5 px-5 py-2 bg-slate-900 text-white rounded-lg"
              >
                Upload Statement
              </Link>
            </div>
          ) : (
            <div className="overflow-hidden rounded-2xl border">
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="bg-slate-100 text-slate-600">
                    <tr>
                      <th className="p-4 text-start">Statement</th>
                      <th className="p-4 text-start">Score</th>
                      <th className="p-4 text-start">Spending</th>
                      <th className="p-4 text-start">Date</th>
                      <th className="p-4 text-end">Action</th>
                    </tr>
                  </thead>

                  <tbody>
                    {financeData.slice(0, 3).map((item) => {
                      const result = parseFinanceResult(item.result);

                      return (
                        <tr
                          key={item.id}
                          className="border-t hover:bg-slate-50"
                        >
                          <td className="p-4 font-medium">{item.file_name}</td>

                          <td className="p-4">
                            <span className="inline-flex px-3 py-1 rounded-full bg-green-50 text-green-700 text-xs font-semibold border border-green-200">
                              {result.financial_score ?? "-"}/100
                            </span>
                          </td>

                          <td className="p-4">
                            {result.total_spending_estimate ?? "-"}
                          </td>

                          <td className="p-4">
                            {new Date(item.created_at).toLocaleDateString()}
                          </td>

                          <td className="p-4 text-end">
                            <Link
                              href="/finance/history"
                              className="text-blue-600"
                            >
                              View
                            </Link>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          <div className="flex gap-3 pt-2">
            <Link href="/finance" className="text-sm text-blue-600">
              Analyze new
            </Link>

            <Link href="/finance/history" className="text-sm text-slate-600">
              View history
            </Link>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl border space-y-4">
          <div className="flex justify-between">
            <h2 className="text-xl font-semibold">Business Decision Agent</h2>

            <Link href="/business" className="text-sm text-blue-600">
              Analyze new
            </Link>
          </div>

          {businessData.length === 0 ? (
            <div className="text-center py-8">
              <h3>No business analyses yet</h3>

              <Link
                href="/business"
                className="mt-4 inline-block px-4 py-2 bg-slate-900 text-white rounded"
              >
                Upload CSV / Excel
              </Link>
            </div>
          ) : (
            <div className="space-y-2">
              {businessData.slice(0, 3).map((item) => {
                const result =
                  typeof item.result === "string"
                    ? JSON.parse(item.result)
                    : item.result;

                return (
                  <div key={item.id} className="border p-3 rounded-xl text-sm">
                    <p className="font-medium">{item.file_name}</p>

                    <p className="text-slate-500">
                      Score: {result.business_health_score ?? "-"} / 100
                    </p>
                  </div>
                );
              })}
            </div>
          )}

          <div className="flex gap-3 pt-2">
            <Link href="/business" className="text-sm text-blue-600">
              Analyze new
            </Link>

            <Link href="/business/history" className="text-sm text-slate-600">
              View history
            </Link>
          </div>
        </div>
      </div>
    </main>
  );
}
