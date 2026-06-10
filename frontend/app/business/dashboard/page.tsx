"use client";

import { useEffect, useMemo, useState } from "react";

import BusinessCharts from "../../../components/business/BusinessCharts";
import { getBusinessHistory } from "../../../lib/api";
import { getSavedLocale } from "../../../lib/i18n";

type Locale = "en" | "fr" | "ar";

type BusinessHistoryItem = {
  id: number;
  file_name: string;
  result: any;
  created_at: string;
};

type AnyObject = Record<string, any>;

const safeGetLocalStorage = (
  key: string,
  fallback = ""
) => {
  if (typeof window === "undefined") {
    return fallback;
  }

  return localStorage.getItem(key) || fallback;
};

const safeParseResult = (value: any) => {
  try {
    return typeof value === "string" ? JSON.parse(value) : value || {};
  } catch {
    return {};
  }
};

const asArray = (value: any): any[] => {
  return Array.isArray(value) ? value : [];
};

const getLocale = (language: string): Locale => {
  if (language === "fr") return "fr";
  if (language === "ar") return "ar";
  return "en";
};

const readableText = (value: any) => {
  if (typeof value === "string") {
    return value;
  }

  if (!value || typeof value !== "object") {
    return "";
  }

  return (
    value.title ||
    value.description ||
    value.risk ||
    value.opportunity ||
    value.recommendation ||
    value.decision ||
    value.what_happened ||
    value.summary ||
    ""
  );
};

const readableDescription = (value: any) => {
  if (!value || typeof value !== "object") {
    return "";
  }

  return (
    value.explanation ||
    value.why ||
    value.why_it_matters ||
    value.reason ||
    value.recommended_action ||
    value.expected_impact ||
    value.description ||
    ""
  );
};

const formatNumber = (
  value: any,
  language: Locale = "en"
) => {
  if (typeof value !== "number" || Number.isNaN(value)) {
    return value ?? "-";
  }

  const locale =
    language === "fr"
      ? "fr-FR"
      : language === "ar"
        ? "ar-MA"
        : "en-US";

  return new Intl.NumberFormat(locale, {
    maximumFractionDigits: 2,
  }).format(value);
};

const formatPercent = (
  value: any,
  language: Locale = "en"
) => {
  if (typeof value !== "number" || Number.isNaN(value)) {
    return value ?? "-";
  }

  return `${formatNumber(value, language)}%`;
};

const formatMoney = (
  value: any,
  currency: any,
  language: Locale = "en"
) => {
  if (typeof value !== "number" || Number.isNaN(value)) {
    return value ?? "-";
  }

  const number = formatNumber(value, language);
  const symbol = currency?.symbol || "";
  const code = currency?.code || "";
  const displayCurrency = symbol || code;

  if (!displayCurrency) {
    return number;
  }

  if (language === "ar") {
    return `${number} ${displayCurrency}`.trim();
  }

  if (currency?.position === "suffix") {
    return `${number} ${displayCurrency}`.trim();
  }

  return `${displayCurrency}${number}`;
};

const getCurrencyDisplay = (
  currency: any,
  language: Locale = "en"
) => {
  const code = currency?.code || "";
  const symbol = currency?.symbol || "";

  if (!code && !symbol) {
    return "N/A";
  }

  if (!symbol) {
    return code;
  }

  if (!code) {
    return symbol;
  }

  if (language === "ar") {
    return `${code} ${symbol}`;
  }

  return `${symbol} ${code}`;
};

const isMetricAvailable = (
  source: AnyObject | null | undefined,
  keys: string[],
  fallback = true
) => {
  for (const key of keys) {
    if (typeof source?.[key] === "boolean") {
      return Boolean(source[key]);
    }
  }

  return fallback;
};

const unavailableMetricLabel = (locale: Locale = "en") => {
  if (locale === "ar") return "غير متاح";
  if (locale === "fr") return "Indisponible";
  return "N/A";
};


const downloadBlob = async (
  response: Response,
  fallbackName: string
) => {
  const blob = await response.blob();
  const disposition = response.headers.get("Content-Disposition") || "";
  const match = disposition.match(/filename="?([^";]+)"?/i);
  const fileName = match?.[1] || fallbackName;
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement("a");

  link.href = url;
  link.download = fileName;
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
};


const normalizeBackendText = (
  value: any,
  language: Locale = "en"
) => {
  if (value === null || value === undefined || value === "") {
    return "-";
  }

  let text = String(value);

  const dictionaries: Record<Locale, Record<string, string>> = {
    en: {},
    fr: {
      "up": "en hausse",
      "down": "en baisse",
      "stable": "stable",
      "low": "faible",
      "medium": "moyen",
      "high": "élevé",
      "critical": "critique",
      "healthy": "sain",
      "positive": "positif",
      "negative": "négatif",
      "normal": "normal",
      "general": "général",
      "saas": "SaaS / abonnement",

      "Healthy profit margin.": "Marge bénéficiaire saine.",
      "Healthy growth.": "Croissance saine.",
      "Positive cashflow.": "Flux de trésorerie positif.",
      "Healthy ROAS.": "ROAS sain.",
      "Healthy CAC efficiency.": "Efficacité CAC saine.",
      "Critical churn level.": "Taux de churn critique.",

      "Payroll": "Masse salariale",
      "Marketing": "Marketing",
      "Software": "Logiciels",
      "Customers": "Clients",
      "New customers": "Nouveaux clients",
      "Churned customers": "Clients perdus",
      "Revenue/customer": "Revenu par client",
      "Orders": "Commandes",
      "Ad spend": "Dépenses publicitaires",

      "Profit Margin": "Marge bénéficiaire",
      "Growth": "Croissance",
      "Cashflow": "Flux de trésorerie",
      "Churn": "Churn",
      "Roas": "ROAS",
      "Cac Efficiency": "Efficacité CAC",
      "Data Quality": "Qualité des données",
      "Revenue": "Chiffre d’affaires",
      "Expenses": "Dépenses",
      "Profit": "Bénéfice",
      "Profit Margin Percent": "Taux de marge bénéficiaire",
      "Growth Rate Percent": "Taux de croissance"
    },
    ar: {
    "up": "في ارتفاع",
    "down": "في انخفاض",
    "stable": "مستقر",

    "low": "منخفض",
    "medium": "متوسط",
    "high": "مرتفع",
    "critical": "حرج",

    "healthy": "سليم",
    "positive": "إيجابي",
    "negative": "سلبي",
    "normal": "طبيعي",

    "general": "عام",
    "saas": "البرمجيات كخدمة (SaaS)",

    "Healthy profit margin.": "هامش الربح في مستوى صحي.",
    "Healthy growth.": "النمو في مستوى صحي.",
    "Positive cashflow.": "التدفق النقدي إيجابي.",
    "Healthy ROAS.": "عائد الإنفاق الإعلاني في مستوى صحي.",
    "Healthy CAC efficiency.": "كفاءة تكلفة اكتساب العملاء في مستوى صحي.",
    "Critical churn level.": "معدل فقدان العملاء في مستوى حرج.",

    "Payroll": "الرواتب",
    "Marketing": "التسويق",
    "Software": "البرمجيات",

    "Customers": "العملاء",
    "New customers": "العملاء الجدد",
    "Churned customers": "العملاء المفقودون",

    "Revenue/customer": "الإيراد لكل عميل",

    "Orders": "الطلبات",
    "Ad spend": "الإنفاق الإعلاني",

    "Profit Margin": "هامش الربح",
    "Growth": "النمو",
    "Cashflow": "التدفق النقدي",
    "Churn": "معدل فقدان العملاء",

    "Roas": "عائد الإنفاق الإعلاني",
    "Cac Efficiency": "كفاءة تكلفة اكتساب العملاء",

    "Data Quality": "جودة البيانات",

    "Revenue": "الإيرادات",
    "Expenses": "المصروفات",
    "Profit": "صافي الربح",

    "Profit Margin Percent": "نسبة هامش الربح",
    "Growth Rate Percent": "معدل النمو"
  },
  };

  const dictionary = dictionaries[language] || {};

  Object.entries(dictionary).forEach(([source, target]) => {
    const escaped = source.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    text = text.replace(
      new RegExp(`(^|[^A-Za-z])${escaped}(?=$|[^A-Za-z])`, "gi"),
      (_match, prefix) => `${prefix}${target}`
    );
  });

  if (language === "fr") {
    text = text
      .replaceAll("cashffaible", "cashflow")
      .replaceAll("cashflow est Positif", "cashflow est positif")
      .replaceAll("score de santé backend est de 73/100 (Sain)", "score de santé backend est de 73/100 (sain)")
      .replaceAll("situation actuelle comme Critique", "situation actuelle comme critique")
      .replaceAll("Volatilité moyen", "Volatilité moyenne")
      .replaceAll("Risque cashflow faible", "Risque de cashflow faible");
  }

  if (language === "ar" && text === "N/A") {
    return "غير متاح";
  }

  if (language === "fr" && text === "N/A") {
    return "Indisponible";
  }

  return text;
};

const localizedKeyLabel = (
  key: string,
  language: Locale = "en"
) => {
  const normalized = String(key || "")
    .replaceAll("_", " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());

  return normalizeBackendText(normalized, language);
};

const labelizeKey = (key: string, language: Locale = "en") =>
  localizedKeyLabel(key, language);

const toneFromValue = (value: any): "slate" | "green" | "red" | "amber" | "blue" => {
  const normalized = String(value || "").toLowerCase();

  if (
    normalized.includes("critical") ||
    normalized.includes("high") ||
    normalized.includes("critique") ||
    normalized.includes("élevé") ||
    normalized.includes("حرج") ||
    normalized.includes("مرتفع")
  ) {
    return "red";
  }

  if (
    normalized.includes("medium") ||
    normalized.includes("moyen") ||
    normalized.includes("متوسط")
  ) {
    return "amber";
  }

  if (
    normalized.includes("healthy") ||
    normalized.includes("positive") ||
    normalized.includes("sain") ||
    normalized.includes("positif") ||
    normalized.includes("صحي") ||
    normalized.includes("إيجابي")
  ) {
    return "green";
  }

  return "slate";
};

const labels: Record<Locale, Record<string, string>> = {
  en: {
    title: "Executive Business Dashboard",

    subtitle:
      "A data-verified overview of your latest business performance, risks, opportunities, and strategic priorities.",

    latestFile: "Latest Analysis",

    healthScore: "Business Health Score",

    currency: "Currency",

    exportPdf: "Export PDF",
    exportPptx: "Export PowerPoint",

    exportingPdf: "Generating PDF...",
    exportingPptx: "Generating PowerPoint...",

    exportSuccess: "Report exported successfully.",
    exportError: "Failed to export report.",

    multiCurrencyWarning: "Multiple currencies detected",

    businessModel: "Business Model",

    revenue: "Revenue",
    expenses: "Expenses",
    profit: "Net Profit",

    margin: "Profit Margin",
    growth: "Growth",
    cashflow: "Cashflow",

    forecast: "Forecast",

    nextMonth: "Projected Revenue (Next Month)",
    nextQuarter: "Projected Revenue (Next Quarter)",

    trend: "Trend",

    cashflowRisk: "Cashflow Risk",

    volatility: "Volatility",

    memory: "Business Memory",

    decision: "Priority Decision",

    risks: "Risks",
    opportunities: "Opportunities",
    recommendations: "Recommendations",

    advancedKpis: "Advanced KPIs",

    anomalies: "Anomaly Detection",

    healthDetails: "Business Health Details",

    dataQuality: "Data Quality",

    noData: "No business analysis available yet.",

    analyzeFirst: "Analyze a business file to get started",

    verified: "Data-verified analysis",

    overview: "Overview",

    charts: "Visual Intelligence",

    strengths: "Strengths",

    warnings: "Areas of Attention",

    noAnomalies: "No significant anomalies detected.",

    noLimitations: "No significant data limitations detected.",

    noMemory: "No historical business memory available yet.",

    generatedAt: "Generated on",

    publicEnterpriseReady: "Enterprise-ready",

    priority: "Priority",

    action: "Action",
  },
  fr: {
    title: "Tableau de bord exécutif",

    subtitle:
      "Vue d’ensemble vérifiée par les données de votre performance business, des risques, des opportunités et des priorités stratégiques.",

    latestFile: "Dernière analyse",

    healthScore: "Score de santé business",

    currency: "Devise",

    exportPdf: "Exporter en PDF",
    exportPptx: "Exporter en PowerPoint",

    exportingPdf: "Génération du PDF...",
    exportingPptx: "Génération du PowerPoint...",

    exportSuccess: "Rapport exporté avec succès.",
    exportError: "Échec de l’export du rapport.",

    multiCurrencyWarning: "Plusieurs devises détectées",

    businessModel: "Modèle économique",

    revenue: "Chiffre d’affaires",
    expenses: "Dépenses",
    profit: "Profit",

    margin: "Marge bénéficiaire",
    growth: "Croissance",
    cashflow: "Flux de trésorerie",

    forecast: "Prévisions",

    nextMonth: "Chiffre d’affaires prévisionnel (mois prochain)",
    nextQuarter: "Chiffre d’affaires prévisionnel (prochain trimestre)",

    trend: "Tendance",

    cashflowRisk: "Risque de trésorerie",

    volatility: "Volatilité",

    memory: "Mémoire business",

    decision: "Décision prioritaire",

    risks: "Risques",
    opportunities: "Opportunités",
    recommendations: "Recommandations",

    advancedKpis: "Indicateurs avancés",

    anomalies: "Détection d’anomalies",

    healthDetails: "Détails du score de santé business",

    dataQuality: "Qualité des données",

    noData: "Aucune analyse business disponible pour le moment.",

    analyzeFirst: "Analysez un fichier business pour commencer",

    verified: "Analyse vérifiée par les données",

    overview: "Vue d’ensemble",

    charts: "Intelligence visuelle",

    strengths: "Points forts",

    warnings: "Points de vigilance",

    noAnomalies: "Aucune anomalie significative détectée.",

    noLimitations: "Aucune limitation significative des données détectée.",

    noMemory: "Aucune donnée historique disponible pour le moment.",

    generatedAt: "Généré le",

    publicEnterpriseReady: "Prêt pour les usages entreprise",

    priority: "Priorité",

    action: "Action",
  },
  ar: {
    title: "لوحة المعلومات التنفيذية",

    subtitle:
      "نظرة شاملة موثقة بالبيانات لأداء الأعمال والمخاطر والفرص والأولويات الاستراتيجية.",

    latestFile: "آخر تحليل",

    healthScore: "مؤشر صحة الأعمال",

    currency: "العملة",

    exportPdf: "تصدير PDF",
    exportPptx: "تصدير PowerPoint",

    exportingPdf: "جارٍ إنشاء ملف PDF...",
    exportingPptx: "جارٍ إنشاء ملف PowerPoint...",

    exportSuccess: "تم تصدير التقرير بنجاح.",
    exportError: "تعذر تصدير التقرير.",

    multiCurrencyWarning: "تم اكتشاف عدة عملات",

    businessModel: "نموذج الأعمال",

    revenue: "الإيرادات",
    expenses: "المصروفات",
    profit: "صافي الربح",

    margin: "هامش الربح",
    growth: "النمو",
    cashflow: "التدفق النقدي",

    forecast: "التوقعات",

    nextMonth: "الإيرادات المتوقعة للشهر القادم",
    nextQuarter: "الإيرادات المتوقعة للربع القادم",

    trend: "الاتجاه",

    cashflowRisk: "مخاطر التدفق النقدي",

    volatility: "التقلب",

    memory: "ذاكرة الأعمال",

    decision: "القرار ذو الأولوية",

    risks: "المخاطر",
    opportunities: "الفرص",
    recommendations: "التوصيات",

    advancedKpis: "مؤشرات الأداء المتقدمة",

    anomalies: "اكتشاف الشذوذ",

    healthDetails: "تفاصيل مؤشر صحة الأعمال",

    dataQuality: "جودة البيانات",

    noData: "لا توجد تحليلات أعمال متاحة حتى الآن.",

    analyzeFirst: "قم بتحليل ملف أعمال للبدء",

    verified: "تحليل موثق بالبيانات",

    overview: "نظرة عامة",

    charts: "الذكاء البصري",

    strengths: "نقاط القوة",

    warnings: "نقاط تستدعي الانتباه",

    noAnomalies: "لم يتم اكتشاف أي شذوذات مهمة.",

    noLimitations: "لم يتم اكتشاف أي قيود مهمة في البيانات.",

    noMemory: "لا تتوفر بيانات تاريخية للأعمال حتى الآن.",

    generatedAt: "تم الإنشاء في",

    publicEnterpriseReady: "جاهز للاستخدام المؤسسي",

    priority: "الأولوية",

    action: "الإجراء",
  },
};

function Badge({
  children,
  tone = "slate",
}: {
  children: React.ReactNode;
  tone?: "slate" | "green" | "red" | "amber" | "blue";
}) {
  const classes: Record<string, string> = {
    slate: "border-slate-200 bg-slate-50 text-slate-700",
    green: "border-emerald-200 bg-emerald-50 text-emerald-700",
    red: "border-red-200 bg-red-50 text-red-700",
    amber: "border-amber-200 bg-amber-50 text-amber-700",
    blue: "border-blue-200 bg-blue-50 text-blue-700",
  };

  return (
    <span
      className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-bold ${classes[tone]}`}
    >
      {children}
    </span>
  );
}

function StatCard({
  label,
  value,
  hint,
  tone = "slate",
}: {
  label: string;
  value: any;
  hint?: string;
  tone?: "slate" | "green" | "red" | "amber" | "blue";
}) {
  const toneClasses: Record<string, string> = {
    slate: "border-slate-200 bg-white",
    green: "border-emerald-200 bg-emerald-50/70",
    red: "border-red-200 bg-red-50/70",
    amber: "border-amber-200 bg-amber-50/70",
    blue: "border-blue-200 bg-blue-50/70",
  };

  return (
    <div
      className={`rounded-3xl border p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md ${toneClasses[tone]}`}
    >
      <p className="text-sm font-medium text-slate-500">
        {label}
      </p>

      <p className="mt-2 break-words text-2xl font-black text-slate-950">
        {value}
      </p>

      {hint && (
        <p className="mt-1 text-xs text-slate-500">
          {hint}
        </p>
      )}
    </div>
  );
}

function SectionCard({
  title,
  children,
  action,
}: {
  title: string;
  children: React.ReactNode;
  action?: React.ReactNode;
}) {
  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-5 flex items-start justify-between gap-4">
        <h2 className="text-xl font-black text-slate-950">
          {title}
        </h2>

        {action}
      </div>

      {children}
    </section>
  );
}

function HealthRing({
  score,
  rating,
  label,
}: {
  score: number | null | undefined;
  rating?: string;
  label: string;
}) {
  const scoreAvailable =
    typeof score === "number" && Number.isFinite(score);
  const safeScore = scoreAvailable
    ? Math.max(0, Math.min(100, Number(score)))
    : null;

  return (
    <div className="rounded-3xl border border-slate-200 bg-slate-950 p-6 text-white shadow-sm">
      <p className="text-sm font-semibold text-slate-300">
        {label}
      </p>

      <div className="mt-5 flex items-end gap-3">
        <p className="text-6xl font-black tracking-tight">
          {safeScore !== null ? safeScore : unavailableMetricLabel(locale)}
        </p>

        {safeScore !== null && (
          <p className="pb-2 text-lg font-bold text-slate-400">
            /100
          </p>
        )}
      </div>

      <div className="mt-5 h-3 overflow-hidden rounded-full bg-white/10">
        <div
          className="h-full rounded-full bg-white"
          style={{ width: `${safeScore ?? 0}%` }}
        />
      </div>

      {rating && rating !== "not_available" && (
        <p className="mt-4 text-sm font-semibold capitalize text-slate-200">
          {rating}
        </p>
      )}
    </div>
  );
}

function ListItemCard({
  item,
  tone,
  language = "en",
}: {
  item: any;
  tone: "red" | "green" | "amber" | "blue" | "slate";
  language?: Locale;
}) {
  const text = normalizeBackendText(readableText(item), language);
  const explanation = normalizeBackendText(readableDescription(item), language);
  const badge = normalizeBackendText(item?.severity || item?.priority || item?.impact || "", language);

  return (
    <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <p className="font-bold text-slate-950">
          {text || "Item"}
        </p>

        {badge && (
          <Badge tone={tone}>
            {badge}
          </Badge>
        )}
      </div>

      {explanation && (
        <p className="mt-2 text-sm leading-6 text-slate-600">
          {explanation}
        </p>
      )}

      {Array.isArray(item?.business_impact) &&
        item.business_impact.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-2">
            {item.business_impact.map((impact: string, index: number) => (
              <Badge key={index}>
                {normalizeBackendText(impact, language)}
              </Badge>
            ))}
          </div>
        )}
    </div>
  );
}

function LoadingSkeleton() {
  return (
    <main className="min-h-screen bg-slate-50 px-4 py-10">
      <div className="mx-auto max-w-7xl space-y-6">
        <div className="h-48 animate-pulse rounded-[2rem] bg-slate-200" />
        <div className="grid grid-cols-1 gap-5 lg:grid-cols-4">
          <div className="h-64 animate-pulse rounded-3xl bg-slate-200" />
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:col-span-3 lg:grid-cols-3">
            {Array.from({ length: 6 }).map((_, index) => (
              <div
                key={index}
                className="h-32 animate-pulse rounded-3xl bg-slate-200"
              />
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}

export default function BusinessDashboardPage() {
  const [history, setHistory] = useState<BusinessHistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [language, setLanguage] = useState("en");
  const [exporting, setExporting] = useState<"pdf" | "pptx" | null>(null);
  const [exportMessage, setExportMessage] = useState("");

  useEffect(() => {
    setLanguage(getSavedLocale());

    async function loadHistory() {
      try {
        const data = await getBusinessHistory();
        setHistory(Array.isArray(data) ? data : []);
      } catch (error) {
        console.error("Failed to load business dashboard:", error);
        setHistory([]);
      } finally {
        setLoading(false);
      }
    }

    loadHistory();
  }, []);

  const locale = getLocale(language);
  const t = labels[locale] || labels.en;
  const latest = history[0];
  const result = latest ? safeParseResult(latest.result) : null;

  const derived = useMemo(() => {
    const kpis = result?.kpis || {};
    const advanced = result?.advanced_kpis || {};
    const forecast = result?.forecast || {};
    const memory = result?.business_memory || {};
    const health = result?.business_health || {};
    const anomalies = result?.anomalies || result?.anomalies_v2 || {};
    const dataQuality = result?.data_quality || {};
    const decision = result?.smart_insights?.most_important_decision || null;
    const currency = result?.currency || null;

    return {
      kpis,
      advanced,
      forecast,
      memory,
      health,
      anomalies,
      dataQuality,
      decision,
      currency,
    };
  }, [result]);

  const handleExport = async (kind: "pdf" | "pptx") => {
    if (!latest?.id) {
      return;
    }

    setExporting(kind);
    setExportMessage("");

    try {
      const token = safeGetLocalStorage("token");
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/business/export/${kind}/${latest.id}`,
        {
          method: "POST",
          headers: {
            ...(token
              ? {
                  Authorization: `Bearer ${token}`,
                }
              : {}),
          },
        }
      );

      if (!response.ok) {
        let detail = t.exportError;

        try {
          const errorData = await response.json();
          detail = errorData?.detail || errorData?.error || detail;
        } catch {
          // The response may be a plain file/error body.
        }

        setExportMessage(detail);
        return;
      }

      await downloadBlob(
        response,
        `business_analysis_${latest.id}.${kind}`
      );

      setExportMessage(t.exportSuccess);
    } catch (error: any) {
      setExportMessage(error?.message || t.exportError);
    } finally {
      setExporting(null);
    }
  };

  if (loading) {
    return <LoadingSkeleton />;
  }

  if (!latest || !result) {
    return (
      <main
        dir={locale === "ar" ? "rtl" : "ltr"}
        className="min-h-screen bg-slate-50 px-4 py-10"
      >
        <div className="mx-auto max-w-4xl rounded-3xl border border-slate-200 bg-white p-8 text-center shadow-sm">
          <Badge tone="blue">
            {t.publicEnterpriseReady}
          </Badge>

          <h1 className="mt-4 text-3xl font-black text-slate-950">
            {t.title}
          </h1>

          <p className="mt-3 text-slate-500">
            {t.noData}
          </p>

          <a
            href="/business"
            className="mt-6 inline-block rounded-2xl bg-slate-950 px-5 py-3 text-sm font-bold text-white"
          >
            {t.analyzeFirst}
          </a>
        </div>
      </main>
    );
  }

  const {
    kpis,
    advanced,
    forecast,
    memory,
    health,
    anomalies,
    dataQuality,
    decision,
    currency,
  } = derived;

  const rawHealthScore = result.business_health_score ?? health.score;
  const healthScore =
    typeof rawHealthScore === "number" && Number.isFinite(rawHealthScore)
      ? rawHealthScore
      : null;
  const expensesAvailable = isMetricAvailable(
    kpis,
    ["expenses_available", "expense_available"]
  );
  const profitAvailable = isMetricAvailable(
    kpis,
    ["profit_available", "profitability_available"]
  );
  const profitMarginAvailable = isMetricAvailable(
    kpis,
    ["profit_margin_available", "margin_available", "profitability_available"],
    profitAvailable
  );
  const anomalyItems = asArray(anomalies.items);
  const latestDate = latest.created_at
    ? new Date(latest.created_at).toLocaleString(
        locale === "fr"
          ? "fr-FR"
          : locale === "ar"
            ? "ar-MA"
            : "en-US"
      )
    : "-";

  return (
    <main
      dir={locale === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-4 py-10"
    >
      <div className="mx-auto max-w-7xl space-y-8">
        <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex flex-col gap-5 md:flex-row md:items-end md:justify-between">
            <div>
              <div className="flex flex-wrap gap-2">
                <Badge tone="green">
                  {t.verified}
                </Badge>

                <Badge tone="blue">
                  {normalizeBackendText(result.business_model || "general", locale)}
                </Badge>

                <Badge>
                  {t.publicEnterpriseReady}
                </Badge>
              </div>

              <h1 className="mt-4 text-4xl font-black tracking-tight text-slate-950 md:text-5xl">
                {t.title}
              </h1>

              <p className="mt-2 max-w-3xl text-slate-500">
                {t.subtitle}
              </p>
            </div>

            <div className="space-y-3">
              <div className="rounded-3xl border border-slate-200 bg-slate-50 px-5 py-4 text-sm">
                <p className="text-slate-500">
                  {t.latestFile}
                </p>

                <p className="mt-1 font-bold text-slate-950">
                  {latest.file_name}
                </p>

                <p className="mt-1 text-xs text-slate-400">
                  {t.generatedAt}: {latestDate}
                </p>
              </div>

              <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
                <button
                  type="button"
                  onClick={() => handleExport("pdf")}
                  disabled={exporting !== null}
                  className="rounded-2xl bg-slate-950 px-4 py-3 text-sm font-bold text-white transition hover:bg-slate-800 disabled:bg-slate-400"
                >
                  {exporting === "pdf" ? t.exportingPdf : t.exportPdf}
                </button>

                <button
                  type="button"
                  onClick={() => handleExport("pptx")}
                  disabled={exporting !== null}
                  className="rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm font-bold text-slate-800 transition hover:bg-slate-50 disabled:text-slate-400"
                >
                  {exporting === "pptx" ? t.exportingPptx : t.exportPptx}
                </button>
              </div>
            </div>
          </div>
        </div>

        {exportMessage && (
          <div className={`rounded-2xl border px-4 py-3 text-sm font-semibold ${
            exportMessage === t.exportSuccess
              ? "border-emerald-200 bg-emerald-50 text-emerald-700"
              : "border-red-200 bg-red-50 text-red-700"
          }`}>
            {exportMessage}
          </div>
        )}

        {currency?.multi_currency_detected && (
          <div className="rounded-2xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm font-semibold text-amber-800">
            {t.multiCurrencyWarning}
          </div>
        )}

        <div className="grid grid-cols-1 gap-5 lg:grid-cols-4">
          <div className="lg:col-span-1">
            <HealthRing
              score={healthScore}
              rating={health.rating}
              label={t.healthScore}
            />
          </div>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:col-span-3 lg:grid-cols-3">
            <StatCard
              label={t.revenue}
              value={formatMoney(kpis.revenue, currency, locale)}
              tone="green"
            />

            <StatCard
              label={t.expenses}
              value={
                expensesAvailable
                  ? formatMoney(kpis.expenses, currency, locale)
                  : unavailableMetricLabel(locale)
              }
              tone="amber"
            />

            <StatCard
              label={t.profit}
              value={
                profitAvailable
                  ? formatMoney(kpis.profit, currency, locale)
                  : unavailableMetricLabel(locale)
              }
              tone={profitAvailable && Number(kpis.profit) < 0 ? "red" : "green"}
            />

            <StatCard
              label={t.margin}
              value={
                profitMarginAvailable
                  ? formatPercent(kpis.profit_margin_percent, locale)
                  : unavailableMetricLabel(locale)
              }
            />

            <StatCard
              label={t.growth}
              value={formatPercent(kpis.growth_rate_percent, locale)}
              tone={Number(kpis.growth_rate_percent) >= 0 ? "green" : "red"}
            />

            <StatCard
              label={t.cashflow}
              value={kpis.cashflow_status || "-"}
              tone={toneFromValue(kpis.cashflow_status)}
            />

            <StatCard
              label={t.currency}
              value={getCurrencyDisplay(currency, locale)}
              tone="blue"
            />
          </div>
        </div>

        {decision && (
          <SectionCard
            title={t.decision}
            action={
              decision.impact && (
                <Badge tone={toneFromValue(decision.impact)}>
                  {normalizeBackendText(decision.impact, locale)}
                </Badge>
              )
            }
          >
            <div className="rounded-3xl border border-amber-200 bg-amber-50 p-5">
              <h3 className="text-lg font-black text-slate-950">
                {normalizeBackendText(decision.title, locale)}
              </h3>

              <p className="mt-2 text-slate-800">
                {normalizeBackendText(decision.decision, locale)}
              </p>

              {decision.why && (
                <p className="mt-2 text-sm leading-6 text-slate-600">
                  {normalizeBackendText(decision.why, locale)}
                </p>
              )}

              {decision.timeframe && (
                <div className="mt-4">
                  <Badge tone="amber">
                    {normalizeBackendText(decision.timeframe, locale)}
                  </Badge>
                </div>
              )}
            </div>
          </SectionCard>
        )}

        <SectionCard title={t.advancedKpis}>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-6">
            <StatCard label="AOV" value={formatMoney(advanced.aov, currency, locale)} />
            <StatCard label="CAC" value={formatMoney(advanced.cac, currency, locale)} />
            <StatCard label="ROAS" value={formatNumber(advanced.roas, locale)} />
            <StatCard label="MRR" value={formatMoney(advanced.mrr, currency, locale)} />
            <StatCard label="ARR" value={formatMoney(advanced.arr, currency, locale)} />
            <StatCard
              label={normalizeBackendText("Churn", locale)}
              value={formatPercent(advanced.churn_rate_percent, locale)}
              tone={Number(advanced.churn_rate_percent) > 10 ? "red" : "slate"}
            />
            <StatCard label={normalizeBackendText("Customers", locale)} value={formatNumber(advanced.customers, locale)} />
            <StatCard label={normalizeBackendText("New customers", locale)} value={formatNumber(advanced.new_customers, locale)} />
            <StatCard label={normalizeBackendText("Churned customers", locale)} value={formatNumber(advanced.churned_customers, locale)} />
            <StatCard label={normalizeBackendText("Revenue/customer", locale)} value={formatMoney(advanced.revenue_per_customer, currency, locale)} />
            <StatCard label={normalizeBackendText("Orders", locale)} value={formatNumber(advanced.orders, locale)} />
            <StatCard label={normalizeBackendText("Ad spend", locale)} value={formatMoney(advanced.ad_spend, currency, locale)} />
          </div>
        </SectionCard>

        {health && health.components && (
          <SectionCard title={t.healthDetails}>
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
              {Object.entries(health.components).map(([key, component]: [string, any]) => (
                <div key={key} className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                  <p className="text-sm font-semibold text-slate-500">
                    {labelizeKey(key, locale)}
                  </p>

                  <p className="mt-2 text-2xl font-black text-slate-950">
                    {typeof component.score === "number" && Number.isFinite(component.score)
                      ? `${component.score}/100`
                      : unavailableMetricLabel(locale)}
                  </p>

                  <p className="mt-1 text-xs leading-5 text-slate-500">
                    {normalizeBackendText(component.label, locale)}
                  </p>
                </div>
              ))}
            </div>

            {(asArray(health.warnings).length > 0 || asArray(health.strengths).length > 0) && (
              <div className="mt-5 grid grid-cols-1 gap-4 md:grid-cols-2">
                {asArray(health.strengths).length > 0 && (
                  <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4">
                    <p className="font-bold text-emerald-800">
                      {t.strengths}
                    </p>

                    <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-emerald-700">
                      {health.strengths.map((item: string, index: number) => (
                        <li key={index}>{normalizeBackendText(item, locale)}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {asArray(health.warnings).length > 0 && (
                  <div className="rounded-2xl border border-red-200 bg-red-50 p-4">
                    <p className="font-bold text-red-800">
                      {t.warnings}
                    </p>

                    <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-red-700">
                      {health.warnings.map((item: string, index: number) => (
                        <li key={index}>{normalizeBackendText(item, locale)}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </SectionCard>
        )}

        {anomalies?.available && (
          <SectionCard
            title={t.anomalies}
            action={
              <Badge tone={anomalyItems.length > 0 ? "red" : "green"}>
                {normalizeBackendText(anomalies.status || "normal", locale)}
              </Badge>
            }
          >
            {anomalyItems.length === 0 ? (
              <p className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-sm font-semibold text-emerald-700">
                {t.noAnomalies}
              </p>
            ) : (
              <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
                {anomalyItems.slice(0, 6).map((item: any, index: number) => (
                  <ListItemCard
                    key={index}
                    item={item}
                    tone={toneFromValue(item.severity)}
                    language={locale}
                  />
                ))}
              </div>
            )}
          </SectionCard>
        )}

        <SectionCard title={t.forecast}>
          <div className="grid grid-cols-1 gap-4 md:grid-cols-5">
            <StatCard
              label={t.nextMonth}
              value={
                forecast?.available
                  ? formatMoney(
                      forecast.next_month_revenue,
                      currency,
                      locale
                    )
                  : unavailableMetricLabel(locale)
              }
            />

            <StatCard
              label={t.nextQuarter}
              value={
                forecast?.available
                  ? formatMoney(
                      forecast.next_quarter_revenue,
                      currency,
                      locale
                    )
                  : unavailableMetricLabel(locale)
              }
            />

            <StatCard
              label={t.trend}
              value={
                forecast?.available
                  ? normalizeBackendText(
                      forecast.trend || "-",
                      locale
                    )
                  : unavailableMetricLabel(locale)
              }
              tone={forecast?.available ? toneFromValue(forecast.trend) : "slate"}
            />

            <StatCard
              label={t.cashflowRisk}
              value={
                forecast?.available
                  ? normalizeBackendText(
                      forecast.cashflow_risk || "-",
                      locale
                    )
                  : unavailableMetricLabel(locale)
              }
              tone={forecast?.available ? toneFromValue(forecast.cashflow_risk) : "slate"}
            />

            <StatCard
              label={t.volatility}
              value={
                forecast?.available
                  ? normalizeBackendText(
                      forecast.volatility || "-",
                      locale
                    )
                  : unavailableMetricLabel(locale)
              }
              tone={forecast?.available ? toneFromValue(forecast.volatility) : "slate"}
            />
          </div>

          {forecast?.available && forecast.explanation && (
            <p className="mt-4 rounded-2xl bg-slate-50 p-4 text-sm leading-6 text-slate-600">
              {normalizeBackendText(forecast.explanation, locale)}
            </p>
          )}
        </SectionCard>

        <SectionCard
          title={t.dataQuality}
          action={
            <Badge tone={Number(dataQuality.score) >= 90 ? "green" : "amber"}>
              {typeof dataQuality.score === "number" && Number.isFinite(dataQuality.score)
                ? `${dataQuality.score}/100`
                : unavailableMetricLabel(locale)}
            </Badge>
          }
        >
          {asArray(dataQuality.limitations).length === 0 ? (
            <p className="text-sm text-slate-600">
              {t.noLimitations}
            </p>
          ) : (
            <ul className="list-disc space-y-2 pl-5 text-sm text-slate-600">
              {dataQuality.limitations.map((item: string, index: number) => (
                <li key={index}>{normalizeBackendText(item, locale)}</li>
              ))}
            </ul>
          )}
        </SectionCard>

        {memory && (
          <SectionCard title={t.memory}>
            <p className="rounded-2xl bg-slate-50 p-4 text-sm leading-6 text-slate-700">
              {normalizeBackendText(memory.summary || t.noMemory, locale)}
            </p>

            {memory.available && memory.changes && (
              <div className="mt-5 grid grid-cols-1 gap-4 md:grid-cols-3">
                {Object.entries(memory.changes).map(
                  ([key, value]: [string, any]) => (
                    <div
                      key={key}
                      className="rounded-2xl border border-slate-200 bg-white p-4"
                    >
                      <p className="text-sm text-slate-500">
                        {labelizeKey(key, locale)}
                      </p>

                      <p className="mt-2 font-black text-slate-950">
                        {formatNumber(value.current, locale)}
                      </p>

                      <p
                        className={`mt-1 text-xs font-bold ${
                          Number(value.percent_change) >= 0
                            ? "text-emerald-600"
                            : "text-red-600"
                        }`}
                      >
                        {formatPercent(value.percent_change, locale)}
                      </p>
                    </div>
                  )
                )}
              </div>
            )}
          </SectionCard>
        )}

        {Array.isArray(result.charts) && result.charts.length > 0 && (
          <SectionCard title={t.charts}>
            <BusinessCharts charts={result.charts} language={locale} currency={currency} />
          </SectionCard>
        )}

        <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
          {asArray(result.risks).length > 0 && (
            <SectionCard title={t.risks}>
              <div className="space-y-3">
                {asArray(result.risks).map((risk: any, index: number) => (
                  <ListItemCard key={index} item={risk} tone="red" language={locale} />
                ))}
              </div>
            </SectionCard>
          )}

          {asArray(result.opportunities).length > 0 && (
            <SectionCard title={t.opportunities}>
              <div className="space-y-3">
                {asArray(result.opportunities).map((opportunity: any, index: number) => (
                  <ListItemCard key={index} item={opportunity} tone="green" language={locale} />
                ))}
              </div>
            </SectionCard>
          )}
        </div>

        {asArray(result.recommendations).length > 0 && (
          <SectionCard title={t.recommendations}>
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
              {asArray(result.recommendations).map((recommendation: any, index: number) => (
                <ListItemCard key={index} item={recommendation} tone="blue" language={locale} />
              ))}
            </div>
          </SectionCard>
        )}
      </div>
    </main>
  );
}
