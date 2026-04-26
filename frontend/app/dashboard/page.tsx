"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getDocuments, createCheckoutSession } from "../../lib/api";
import { getToken } from "../../lib/auth";
import RiskBadge from "../../components/RiskBadge";

const labels: any = {
  en: {
    title: "Dashboard",
    subtitle: "Manage your contract analyses.",
    buy: "Buy credit",
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
  fr: {
    title: "Tableau de bord",
    subtitle: "Gérez vos analyses de contrats.",
    buy: "Acheter crédit",
    new: "Nouvelle analyse",
    loading: "Chargement...",
    total: "Documents",
    completed: "Terminés",
    progress: "En cours",
    emptyTitle: "Aucun document",
    emptyDesc: "Téléversez votre premier contrat.",
    upload: "Téléverser",
    document: "Document",
    type: "Type",
    language: "Langue",
    status: "Statut",
    date: "Date",
    action: "Action",
    view: "Voir",
  },
  ar: {
    title: "لوحة التحكم",
    subtitle: "إدارة تحليلات العقود",
    buy: "شراء رصيد",
    new: "تحليل جديد",
    loading: "جاري التحميل...",
    total: "عدد الوثائق",
    completed: "مكتمل",
    progress: "قيد المعالجة",
    emptyTitle: "لا توجد وثائق",
    emptyDesc: "قم برفع أول عقد",
    upload: "رفع عقد",
    document: "الوثيقة",
    type: "النوع",
    language: "اللغة",
    status: "الحالة",
    date: "التاريخ",
    action: "الإجراء",
    view: "عرض",
  },
};

export default function DashboardPage() {
  const [documents, setDocuments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [locale, setLocale] = useState("en");

  const t = labels[locale] || labels.en;

  useEffect(() => {
    const saved = localStorage.getItem("locale") || "en";
    setLocale(saved);

    const token = getToken();

    if (!token) {
      window.location.href = "/login";
      return;
    }

    loadDocuments();
  }, []);

  async function loadDocuments() {
    try {
      const data = await getDocuments();
      setDocuments(data);
    } finally {
      setLoading(false);
    }
  }

  const handleBuyCredit = async () => {
    const data = await createCheckoutSession();

    if (data.checkout_url) {
      window.location.href = data.checkout_url;
      return;
    }

    setMessage(data.detail || "Payment is not configured yet.");
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

          <div className="flex gap-3">
            <button
              onClick={handleBuyCredit}
              className="px-5 py-2 bg-green-600 text-white rounded-xl"
            >
              {t.buy}
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

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
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
        </div>

        {documents.length === 0 ? (
          <div className="bg-white border rounded-2xl p-10 text-center">
            <h2 className="text-xl font-semibold">{t.emptyTitle}</h2>
            <p className="text-slate-500 mt-2">{t.emptyDesc}</p>

            <Link
              href="/upload"
              className="inline-block mt-5 px-5 py-2 bg-slate-900 text-white rounded-lg"
            >
              {t.upload}
            </Link>
          </div>
        ) : (
          <div className="bg-white border rounded-2xl overflow-hidden">
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
                      <td className="p-4 text-start font-medium">
                        {doc.file_name}
                      </td>
                      <td className="p-4 text-start">
                        {doc.file_type?.toUpperCase()}
                      </td>
                      <td className="p-4 text-start">{doc.language || "—"}</td>
                      <td className="p-4 text-start">
                        <RiskBadge
                          risk={doc.status === "completed" ? "low" : "medium"}
                        />
                      </td>
                      <td className="p-4 text-start">
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
    </main>
  );
}