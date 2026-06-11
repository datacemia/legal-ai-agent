"use client";

import { useEffect, useState } from "react";

import { getSavedLocale } from "../../../lib/i18n";

type Locale = "en" | "fr" | "ar";

type WeeklyReport = {
  error?: string;
  title?: string;
  generated_at?: string;
  business_model?: string;
  source_file_name?: string;
  executive_brief?: string;
  weekly_summary?: string;
  business_health_score?: number;
  currency?: {
    code?: string;
    symbol?: string;
    position?: string;
    multi_currency_detected?: boolean;
  };
  kpi_snapshot?: {
    revenue?: number;
    expenses?: number;
    profit?: number;
    profit_margin_percent?: number;
    growth_rate_percent?: number;
    cashflow_status?: string;
  };
  forecast_snapshot?: {
    available?: boolean;
    next_month_revenue?: number;
    next_quarter_revenue?: number;
    trend?: string;
    cashflow_risk?: string;
    volatility?: string;
  };
  memory_summary?: string;
  top_risks?: Array<any>;
  top_opportunities?: Array<any>;
  priority_actions?: Array<any>;
  ceo_decision?: {
    decision?: string;
    why?: string;
    timeframe?: string;
  };
  data_limitations?: string[];
  disclaimer?: string;
};

const safeGetLocalStorage = (key: string, fallback = "") => {
  if (typeof window === "undefined") {
    return fallback;
  }

  return localStorage.getItem(key) || fallback;
};

const getLocale = (language: string): Locale => {
  if (language === "fr") return "fr";
  if (language === "ar") return "ar";
  return "en";
};

const formatNumber = (
  value: unknown,
  language: Locale = "en"
) => {
  if (typeof value === "number") {
    const locale =
      language === "fr"
        ? "fr-FR"
        : language === "ar"
          ? "ar-MA"
          : "en-US";

    return new Intl.NumberFormat(locale, {
      maximumFractionDigits: 2,
    }).format(value);
  }

  if (value === null || value === undefined || value === "") {
    return "-";
  }

  return String(value);
};

const formatPercent = (
  value: unknown,
  language: Locale = "en"
) => {
  if (typeof value !== "number" || Number.isNaN(value)) {
    return "-";
  }

  const formatted = formatNumber(value, language);

  if (language === "fr") {
    return `${formatted} %`;
  }

  return `${formatted}%`;
};

const formatMoney = (
  value: unknown,
  currency: WeeklyReport["currency"],
  language: Locale = "en"
) => {
  if (typeof value !== "number" || Number.isNaN(value)) {
    return "-";
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
  currency: WeeklyReport["currency"],
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
    "Cashflow": "Cashflow",
    "Churn": "Attrition client",

    "Roas": "ROAS",
    "Cac Efficiency": "Efficacité CAC",

    "Data Quality": "Qualité des données",

    "Revenue": "Chiffre d’affaires",
    "Expenses": "Dépenses",
    "Profit": "Profit",

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

const labels: Record<Locale, Record<string, string>> = {
  en: {
    title: "Weekly Executive Business Report",

    subtitle:
      "A weekly business intelligence report based on your latest verified business analysis.",

    badge: "Business Intelligence",

    enterpriseReady: "Enterprise-ready",

    generate: "Generate Weekly Report",

    generating: "Generating Report...",

    noReport: "No report available yet.",

    source: "Source Analysis",

    healthScore: "Business Health Score",

    businessModel: "Business Model",

    currency: "Currency",

    executiveBrief: "Executive Summary",

    weeklySummary: "Weekly Summary",

    strategicDecision: "Strategic Priority",

    kpiSnapshot: "KPI Overview",

    forecast: "Forecast Overview",

    revenue: "Revenue",

    expenses: "Expenses",

    profit: "Net Profit",

    margin: "Profit Margin",

    growth: "Growth",

    cashflowStatus: "Cashflow Status",

    nextMonth: "Projected Revenue (Next Month)",

    nextQuarter: "Projected Revenue (Next Quarter)",

    trend: "Trend",

    cashflowRisk: "Cashflow Risk",

    volatility: "Volatility",

    memory: "Business Memory",

    risks: "Key Risks",

    opportunities: "Key Opportunities",

    actions: "Priority Actions",

    limitations: "Data Limitations",

    analyzeFirst: "Analyze a business file to generate a report",

    verified: "Data-verified analysis",

    multiCurrencyWarning: "Multiple currencies detected",

    exportPdf: "Export PDF",

    exportPptx: "Export PowerPoint",

    exportsSoon:
      "Exports will be available once reporting services are enabled",
  },
  fr: {
    title: "Rapport exécutif hebdomadaire",

    subtitle:
      "Synthèse hebdomadaire de business intelligence basée sur votre dernière analyse vérifiée.",

    badge: "Business Intelligence",

    enterpriseReady: "Prêt pour les entreprises",

    generate: "Générer le rapport hebdomadaire",

    generating: "Génération du rapport...",

    noReport: "Aucun rapport disponible pour le moment.",

    source: "Analyse source",

    healthScore: "Score de santé business",

    businessModel: "Modèle économique",

    currency: "Devise",

    executiveBrief: "Synthèse exécutive",

    weeklySummary: "Résumé hebdomadaire",

    strategicDecision: "Priorité stratégique",

    kpiSnapshot: "Aperçu des KPI",

    forecast: "Aperçu des prévisions",

    revenue: "Chiffre d’affaires",

    expenses: "Dépenses",

    profit: "Profit",

    margin: "Marge bénéficiaire",

    growth: "Croissance",

    cashflowStatus: "État du flux de trésorerie",

    nextMonth: "Chiffre d’affaires prévisionnel (mois prochain)",

    nextQuarter: "Chiffre d’affaires prévisionnel (prochain trimestre)",

    trend: "Tendance",

    cashflowRisk: "Risque de trésorerie",

    volatility: "Volatilité",

    memory: "Mémoire business",

    risks: "Risques principaux",

    opportunities: "Opportunités principales",

    actions: "Actions prioritaires",

    limitations: "Limites des données",

    analyzeFirst: "Analysez un fichier business pour générer un rapport",

    verified: "Analyse vérifiée par les données",

    multiCurrencyWarning: "Plusieurs devises détectées",

    exportPdf: "Exporter en PDF",

    exportPptx: "Exporter en PowerPoint",

    exportsSoon:
      "Les exports seront disponibles une fois les services de reporting activés",
  },
  ar: {
    title: "التقرير التنفيذي الأسبوعي",

    subtitle:
      "ملخص أسبوعي لذكاء الأعمال يستند إلى أحدث تحليل موثق بالبيانات.",

    badge: "ذكاء الأعمال",

    enterpriseReady: "جاهز للاستخدام المؤسسي",

    generate: "إنشاء التقرير الأسبوعي",

    generating: "جارٍ إنشاء التقرير...",

    noReport: "لا يوجد تقرير متاح حتى الآن.",

    source: "التحليل المصدر",

    healthScore: "مؤشر صحة الأعمال",

    businessModel: "نموذج الأعمال",

    currency: "العملة",

    executiveBrief: "الملخص التنفيذي",

    weeklySummary: "الملخص الأسبوعي",

    strategicDecision: "الأولوية الاستراتيجية",

    kpiSnapshot: "ملخص مؤشرات الأداء",

    forecast: "ملخص التوقعات",

    revenue: "الإيرادات",

    expenses: "المصروفات",

    profit: "صافي الربح",

    margin: "هامش الربح",

    growth: "النمو",

    cashflowStatus: "حالة التدفق النقدي",

    nextMonth: "الإيرادات المتوقعة للشهر القادم",

    nextQuarter: "الإيرادات المتوقعة للربع القادم",

    trend: "الاتجاه",

    cashflowRisk: "مخاطر التدفق النقدي",

    volatility: "التقلب",

    memory: "ذاكرة الأعمال",

    risks: "المخاطر الرئيسية",

    opportunities: "الفرص الرئيسية",

    actions: "الإجراءات ذات الأولوية",

    limitations: "قيود البيانات",

    analyzeFirst: "قم بتحليل ملف أعمال لإنشاء التقرير",

    verified: "تحليل موثق بالبيانات",

    multiCurrencyWarning: "تم اكتشاف عدة عملات",

    exportPdf: "تصدير PDF",

    exportPptx: "تصدير PowerPoint",

    exportsSoon:
      "ستتوفر عمليات التصدير عند تفعيل خدمات التقارير",
  },
};

function StatCard({
  label,
  value,
  tone = "default",
}: {
  label: string;
  value: unknown;
  tone?: "default" | "green" | "amber" | "red" | "blue";
}) {
  const styles = {
    default: "border-slate-200 bg-white",
    green: "border-emerald-200 bg-emerald-50",
    amber: "border-amber-200 bg-amber-50",
    red: "border-red-200 bg-red-50",
    blue: "border-blue-200 bg-blue-50",
  };

  return (
    <div
      className={`rounded-3xl border p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md ${styles[tone]}`}
    >
      <p className="text-sm font-medium text-slate-500">{label}</p>

      <p className="mt-2 break-words text-2xl font-black text-slate-950">
        {value === null || value === undefined || value === "" ? "-" : String(value)}
      </p>
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
    <section className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm">
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

function Badge({
  children,
  tone = "slate",
}: {
  children: React.ReactNode;
  tone?: "slate" | "green" | "red" | "amber" | "blue";
}) {
  const styles = {
    slate: "border-slate-200 bg-slate-50 text-slate-700",
    green: "border-emerald-200 bg-emerald-50 text-emerald-700",
    red: "border-red-200 bg-red-50 text-red-700",
    amber: "border-amber-200 bg-amber-50 text-amber-700",
    blue: "border-blue-200 bg-blue-50 text-blue-700",
  };

  return (
    <span
      className={`inline-flex w-fit rounded-full border px-3 py-1 text-xs font-bold ${styles[tone]}`}
    >
      {children}
    </span>
  );
}

function getItemTitle(item: any) {
  if (typeof item === "string") return item;

  return (
    item?.title ||
    item?.decision ||
    item?.risk ||
    item?.opportunity ||
    item?.recommendation ||
    item?.description ||
    item?.what_happened ||
    "Item"
  );
}

function getItemDescription(item: any) {
  if (!item || typeof item !== "object") return "";

  return (
    item?.why_it_matters ||
    item?.expected_impact ||
    item?.recommended_action ||
    item?.owner_focus ||
    item?.why ||
    item?.summary ||
    item?.description ||
    ""
  );
}

function ListCards({
  items,
  variant = "default",
  language = "en",
}: {
  items?: Array<any>;
  variant?: "default" | "risk" | "opportunity";
  language?: Locale;
}) {
  if (!Array.isArray(items) || items.length === 0) {
    return (
      <p className="text-sm text-slate-500">
        -
      </p>
    );
  }

  const styles = {
    default: "border-slate-200 bg-slate-50",
    risk: "border-red-200 bg-red-50",
    opportunity: "border-green-200 bg-green-50",
  };

  return (
    <div className="space-y-3">
      {items.map((item, index) => {
        const badge = item?.severity || item?.impact || item?.priority;
        const description = getItemDescription(item);

        return (
          <div
            key={index}
            className={`rounded-2xl border p-4 ${styles[variant]}`}
          >
            <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
              <p className="font-bold text-slate-950">
                {normalizeBackendText(getItemTitle(item), language)}
              </p>

              {badge && (
                <Badge
                  tone={
                    variant === "risk"
                      ? "red"
                      : variant === "opportunity"
                        ? "green"
                        : "blue"
                  }
                >
                  {normalizeBackendText(badge, language)}
                </Badge>
              )}
            </div>

            {description && (
              <p className="mt-2 text-sm leading-6 text-slate-700">
                {normalizeBackendText(description, language)}
              </p>
            )}
          </div>
        );
      })}
    </div>
  );
}

export default function BusinessReportsPage() {
  const [language, setLanguage] = useState("en");
  const [report, setReport] = useState<WeeklyReport | null>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    setLanguage(getSavedLocale());
  }, []);

  const locale = getLocale(language);
  const t = labels[locale] || labels.en;

  const generateReport = async () => {
    setLoading(true);
    setMessage("");

    try {
      const token = safeGetLocalStorage("token");

      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/business/weekly-report`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            ...(token
              ? {
                  Authorization: `Bearer ${token}`,
                }
              : {}),
          },
          body: JSON.stringify({
            output_language: language,
          }),
        }
      );

      const data = await res.json();

      if (!res.ok) {
        setMessage(
          data?.detail ||
            data?.error ||
            "Failed to generate weekly report."
        );
        return;
      }

      setReport(data);
    } catch (error: any) {
      setMessage(
        error?.message ||
          "Failed to generate weekly report."
      );
    } finally {
      setLoading(false);
    }
  };

  const kpis = report?.kpi_snapshot || {};
  const forecast = report?.forecast_snapshot || {};
  const currency = report?.currency || null;
  const direction = locale === "ar" ? "rtl" : "ltr";

  return (
    <main
      dir={direction}
      className="min-h-screen bg-slate-50 px-4 py-10"
    >
      <div className="mx-auto max-w-7xl space-y-8">
        {/* Hero */}
        <section className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm md:p-8">
          <div className="flex flex-col gap-5 md:flex-row md:items-end md:justify-between">
            <div>
              <div className="flex flex-wrap gap-2">
                <Badge tone="blue">{t.badge}</Badge>
                <Badge tone="green">{t.enterpriseReady}</Badge>
              </div>

              <h1 className="mt-4 text-4xl font-black tracking-tight text-slate-950 md:text-5xl">
                {t.title}
              </h1>

              <p className="mt-3 max-w-3xl text-base leading-7 text-slate-600">
                {t.subtitle}
              </p>
            </div>

            <div className="flex flex-col gap-3 sm:flex-row">
              <button
                onClick={generateReport}
                disabled={loading}
                className="rounded-2xl bg-slate-950 px-5 py-3 text-sm font-bold text-white transition hover:bg-slate-800 disabled:bg-slate-400"
              >
                {loading ? t.generating : t.generate}
              </button>

              <button
                type="button"
                disabled
                title={t.exportsSoon}
                className="rounded-2xl border border-slate-200 bg-white px-5 py-3 text-sm font-bold text-slate-400"
              >
                {t.exportPdf}
              </button>

              <button
                type="button"
                disabled
                title={t.exportsSoon}
                className="rounded-2xl border border-slate-200 bg-white px-5 py-3 text-sm font-bold text-slate-400"
              >
                {t.exportPptx}
              </button>
            </div>
          </div>
        </section>

        {message && (
          <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {message}
          </div>
        )}

        {!report ? (
          <div className="rounded-[2rem] border border-slate-200 bg-white p-8 text-center shadow-sm">
            <Badge tone="green">{t.verified}</Badge>

            <p className="mt-4 text-slate-500">{t.noReport}</p>

            <a
              href="/business"
              className="mt-5 inline-block rounded-xl border px-5 py-3 text-sm font-bold text-slate-700 hover:bg-slate-50"
            >
              {t.analyzeFirst}
            </a>
          </div>
        ) : report.error ? (
          <div className="rounded-[2rem] border border-slate-200 bg-white p-8 text-center shadow-sm">
            <p className="font-semibold text-red-600">
              {report.error}
            </p>

            <a
              href="/business"
              className="mt-5 inline-block rounded-xl bg-slate-900 px-5 py-3 text-sm font-bold text-white"
            >
              {t.analyzeFirst}
            </a>
          </div>
        ) : (
          <>
            {/* Source / Overview */}
            <div className="grid grid-cols-1 gap-4 md:grid-cols-4">
              <StatCard
                label={t.source}
                value={report.source_file_name || "-"}
              />

              <StatCard
                label={t.businessModel}
                value={report.business_model || "general"}
                tone="blue"
              />

              <StatCard
                label={t.healthScore}
                value={`${report.business_health_score ?? 0}/100`}
                tone={
                  Number(report.business_health_score || 0) >= 60
                    ? "green"
                    : "red"
                }
              />

              <StatCard
                label={t.currency}
                value={getCurrencyDisplay(currency, locale)}
              />
            </div>

            {currency?.multi_currency_detected && (
              <div className="rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm font-semibold text-amber-800">
                {t.multiCurrencyWarning}
              </div>
            )}

            {/* Executive brief */}
            <SectionCard
              title={t.executiveBrief}
              action={<Badge tone="green">{t.verified}</Badge>}
            >
              <p className="text-lg leading-relaxed text-slate-700">
                {report.executive_brief || "-"}
              </p>

              {report.generated_at && (
                <p className="mt-4 text-xs text-slate-400">
                  {new Date(report.generated_at).toLocaleString()}
                </p>
              )}
            </SectionCard>

            {/* Weekly summary */}
            <SectionCard title={t.weeklySummary}>
              <p className="leading-relaxed text-slate-700">
                {report.weekly_summary || "-"}
              </p>
            </SectionCard>

            {/* Strategic decision */}
            <SectionCard title={t.strategicDecision}>
              <div className="rounded-3xl border border-amber-200 bg-amber-50 p-5">
                <p className="text-lg font-black text-slate-950">
                  {report.ceo_decision?.decision || "-"}
                </p>

                {report.ceo_decision?.why && (
                  <p className="mt-2 text-sm leading-6 text-slate-700">
                    {report.ceo_decision.why}
                  </p>
                )}

                {report.ceo_decision?.timeframe && (
                  <Badge tone="amber">
                    {report.ceo_decision.timeframe}
                  </Badge>
                )}
              </div>
            </SectionCard>

            {/* KPI Snapshot */}
            <SectionCard title={t.kpiSnapshot}>
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-6">
                <StatCard
                  label={t.revenue}
                  value={formatMoney(kpis.revenue, currency, locale)}
                  tone="green"
                />
                <StatCard
                  label={t.expenses}
                  value={formatMoney(kpis.expenses, currency, locale)}
                  tone="amber"
                />
                <StatCard
                  label={t.profit}
                  value={formatMoney(kpis.profit, currency, locale)}
                  tone="green"
                />
                <StatCard
                  label={t.margin}
                  value={formatPercent(kpis.profit_margin_percent, locale)}
                />
                <StatCard
                  label={t.growth}
                  value={formatPercent(kpis.growth_rate_percent, locale)}
                  tone="blue"
                />
                <StatCard
                  label={t.cashflowStatus}
                  value={kpis.cashflow_status || "unknown"}
                />
              </div>
            </SectionCard>

            {/* Forecast */}
            <SectionCard title={t.forecast}>
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-5">
                <StatCard
                  label={t.nextMonth}
                  value={formatMoney(
                    forecast.next_month_revenue,
                    currency,
                    locale
                  )}
                  tone="green"
                />
                <StatCard
                  label={t.nextQuarter}
                  value={formatMoney(
                    forecast.next_quarter_revenue,
                    currency,
                    locale
                  )}
                  tone="blue"
                />
                <StatCard label={t.trend} value={forecast.trend || "-"} />
                <StatCard
                  label={t.cashflowRisk}
                  value={forecast.cashflow_risk || "-"}
                  tone="amber"
                />
                <StatCard
                  label={t.volatility}
                  value={forecast.volatility || "-"}
                />
              </div>
            </SectionCard>

            {/* Memory */}
            <SectionCard title={t.memory}>
              <p className="leading-relaxed text-slate-700">
                {report.memory_summary || "-"}
              </p>
            </SectionCard>

            {/* Risks / Opportunities */}
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
              <SectionCard title={t.risks}>
                <ListCards items={report.top_risks} variant="risk" language={locale} />
              </SectionCard>

              <SectionCard title={t.opportunities}>
                <ListCards
                  items={report.top_opportunities}
                  variant="opportunity"
                />
              </SectionCard>
            </div>

            {/* Actions */}
            <SectionCard title={t.actions}>
              <ListCards items={report.priority_actions} language={locale} />
            </SectionCard>

            {/* Limitations */}
            {Array.isArray(report.data_limitations) &&
              report.data_limitations.length > 0 && (
                <SectionCard title={t.limitations}>
                  <ul className="list-disc space-y-2 ps-5 text-sm text-slate-600">
                    {report.data_limitations.map((item, index) => (
                      <li key={index}>{item}</li>
                    ))}
                  </ul>
                </SectionCard>
              )}

            {report.disclaimer && (
              <p className="text-xs text-slate-500">
                {normalizeBackendText(report.disclaimer, locale)}
              </p>
            )}
          </>
        )}
      </div>
    </main>
  );
}
