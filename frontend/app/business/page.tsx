"use client";

import { useEffect, useMemo, useState } from "react";

import {
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { analyzeBusinessFile } from "../../lib/api";
import {
  getSavedLocale,
  setSavedLocale,
} from "../../lib/i18n";

type Locale = "en" | "fr" | "ar";

type ChartPoint = Record<string, any>;

type BusinessChart = {
  type?: "line" | "bar" | string;
  title?: string;
  x_key?: string;
  y_key?: string;
  data?: ChartPoint[];
};

const safeGetLocalStorage = (
  key: string,
  fallback = ""
) => {
  if (typeof window === "undefined") {
    return fallback;
  }

  return localStorage.getItem(key) || fallback;
};

const safeSetLocalStorage = (
  key: string,
  value: string
) => {
  if (typeof window === "undefined") {
    return;
  }

  localStorage.setItem(key, value);
};

const BUSINESS_LAST_RESULT_KEY = "runexa_business_last_analysis_result";
const BUSINESS_LAST_FILE_NAME_KEY = "runexa_business_last_analysis_file_name";

const safeRemoveLocalStorage = (key: string) => {
  if (typeof window === "undefined") {
    return;
  }

  localStorage.removeItem(key);
};

const safeParseJson = (value: string) => {
  try {
    return value ? JSON.parse(value) : null;
  } catch {
    return null;
  }
};

const saveLastBusinessAnalysis = (
  data: any,
  fileName?: string
) => {
  if (typeof window === "undefined" || !data) {
    return;
  }

  try {
    localStorage.setItem(
      BUSINESS_LAST_RESULT_KEY,
      JSON.stringify({
        ...data,
        __saved_at: new Date().toISOString(),
        __file_name: fileName || data?.file_metadata?.file_name || "",
      })
    );

    if (fileName) {
      localStorage.setItem(
        BUSINESS_LAST_FILE_NAME_KEY,
        fileName
      );
    }
  } catch {
    // Ignore storage quota/private-mode errors.
  }
};

const getLastBusinessAnalysis = () => {
  if (typeof window === "undefined") {
    return null;
  }

  return safeParseJson(
    localStorage.getItem(BUSINESS_LAST_RESULT_KEY) || ""
  );
};

const clearLastBusinessAnalysis = () => {
  safeRemoveLocalStorage(BUSINESS_LAST_RESULT_KEY);
  safeRemoveLocalStorage(BUSINESS_LAST_FILE_NAME_KEY);
};


const asArray = (value: any): any[] => {
  return Array.isArray(value) ? value : [];
};

const getLocale = (language: string): Locale => {
  if (language === "fr") return "fr";
  if (language === "ar") return "ar";
  return "en";
};

const formatNumber = (
  value: any,
  language = "en"
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
  language = "en"
) => {
  if (typeof value !== "number" || Number.isNaN(value)) {
    return value ?? "-";
  }

  return `${formatNumber(value, language)}%`;
};

const formatMoney = (
  value: any,
  currency: any,
  language = "en"
) => {
  if (typeof value !== "number" || Number.isNaN(value)) {
    return value ?? "-";
  }

  const number = formatNumber(value, language);
  const symbol = currency?.symbol || "";
  const code = currency?.code || "";

  if (!symbol && !code) {
    return number;
  }

  const displayCurrency = symbol || code;

  if (language === "ar") {
    return `${number} ${displayCurrency}`.trim();
  }

  const position = currency?.position || "prefix";

  if (position === "suffix") {
    return `${number} ${displayCurrency}`.trim();
  }

  return `${displayCurrency}${number}`;
};

const getCurrencyDisplay = (
  currency: any,
  language = "en"
) => {
  const code = currency?.code || "USD";
  const symbol = currency?.symbol || "";

  if (!symbol) {
    return code;
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
      "up": "hausse",
      "down": "baisse",
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
      "Positive cashflow.": "Cashflow positif.",
      "Healthy ROAS.": "ROAS sain.",
      "Healthy CAC efficiency.": "Efficacité CAC saine.",
      "Critical churn level.": "Niveau de churn critique.",
      "Payroll": "Masse salariale",
      "Marketing": "Marketing",
      "Software": "Logiciels",
      "Customers": "Clients",
      "New customers": "Nouveaux clients",
      "Churned customers": "Clients perdus",
      "Revenue/customer": "Revenu/client",
      "Orders": "Commandes",
      "Ad spend": "Dépenses publicitaires",
      "Profit Margin": "Marge bénéficiaire",
      "Growth": "Croissance",
      "Cashflow": "Cashflow",
      "Churn": "Churn",
      "Roas": "ROAS",
      "Cac Efficiency": "Efficacité CAC",
      "Data Quality": "Qualité des données",
      "Revenue": "Revenus",
      "Expenses": "Dépenses",
      "Profit": "Profit",
      "Profit Margin Percent": "Marge bénéficiaire",
      "Growth Rate Percent": "Taux de croissance"
    },
    ar: {
      "up": "صاعد",
      "down": "هابط",
      "stable": "مستقر",
      "low": "منخفض",
      "medium": "متوسط",
      "high": "مرتفع",
      "critical": "حرج",
      "healthy": "صحي",
      "positive": "إيجابي",
      "negative": "سلبي",
      "normal": "طبيعي",
      "general": "عام",
      "saas": "SaaS / اشتراك",
      "Healthy profit margin.": "هامش ربح صحي.",
      "Healthy growth.": "نمو صحي.",
      "Positive cashflow.": "تدفق نقدي إيجابي.",
      "Healthy ROAS.": "عائد إنفاق إعلاني صحي.",
      "Healthy CAC efficiency.": "كفاءة صحية لتكلفة اكتساب العميل.",
      "Critical churn level.": "مستوى فقدان العملاء حرج.",
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
      "Churn": "فقدان العملاء",
      "Roas": "عائد الإنفاق الإعلاني",
      "Cac Efficiency": "كفاءة تكلفة الاكتساب",
      "Data Quality": "جودة البيانات",
      "Revenue": "الإيرادات",
      "Expenses": "المصاريف",
      "Profit": "الأرباح",
      "Profit Margin Percent": "هامش الربح",
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


const getLatestSavedBusinessAnalysisId = async (
  token: string,
  fileName?: string
) => {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/business/history`,
    {
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
    return null;
  }

  const history = await response.json();

  if (!Array.isArray(history) || history.length === 0) {
    return null;
  }

  const matchingItem = fileName
    ? history.find((item: any) => item?.file_name === fileName)
    : null;

  return matchingItem?.id || history[0]?.id || null;
};

const translateCategoryLabel = (
  value: any,
  language: Locale
) => {
  const raw = String(value ?? "");

  const categoryMap: Record<string, Record<Locale, string>> = {
    Payroll: {
      en: "Payroll",
      fr: "Masse salariale",
      ar: "الرواتب",
    },
    Marketing: {
      en: "Marketing",
      fr: "Marketing",
      ar: "التسويق",
    },
    Software: {
      en: "Software",
      fr: "Logiciels",
      ar: "البرمجيات",
    },
  };

  return categoryMap[raw]?.[language] || raw;
};

const formatChartValue = (
  value: any,
  chart: BusinessChart,
  language: Locale,
  currency: any
) => {
  if (typeof value !== "number" || Number.isNaN(value)) {
    return "-";
  }

  const yKey = String(chart.y_key || "").toLowerCase();

  if (
    yKey.includes("revenue") ||
    yKey.includes("expense") ||
    yKey.includes("profit") ||
    yKey.includes("cashflow") ||
    yKey.includes("cost") ||
    yKey.includes("spend")
  ) {
    return formatMoney(value, currency, language);
  }

  return formatNumber(value, language);
};

const getItemTitle = (item: any) => {
  if (typeof item === "string") {
    return item;
  }

  if (!item || typeof item !== "object") {
    return "Item";
  }

  return (
    item.title ||
    item.risk ||
    item.opportunity ||
    item.recommendation ||
    item.decision ||
    item.description ||
    item.what_happened ||
    "Item"
  );
};

const getItemDescription = (item: any) => {
  if (!item || typeof item !== "object") {
    return "";
  }

  return (
    item.description ||
    item.explanation ||
    item.why_it_matters ||
    item.expected_impact ||
    item.recommended_action ||
    item.owner_focus ||
    item.why ||
    item.summary ||
    ""
  );
};

const getItemBadge = (item: any) => {
  if (!item || typeof item !== "object") {
    return "";
  }

  return (
    item.severity ||
    item.priority ||
    item.impact ||
    item.category ||
    ""
  );
};

const badgeClass = (value: string) => {
  const normalized = String(value || "").toLowerCase();

  if (
    normalized.includes("critical") ||
    normalized.includes("high") ||
    normalized.includes("critique") ||
    normalized.includes("élevé") ||
    normalized.includes("حرج") ||
    normalized.includes("مرتفع")
  ) {
    return "bg-red-100 text-red-700 border-red-200";
  }

  if (
    normalized.includes("medium") ||
    normalized.includes("moyen") ||
    normalized.includes("متوسط")
  ) {
    return "bg-amber-100 text-amber-700 border-amber-200";
  }

  if (
    normalized.includes("low") ||
    normalized.includes("faible") ||
    normalized.includes("منخفض")
  ) {
    return "bg-slate-100 text-slate-700 border-slate-200";
  }

  return "bg-white text-slate-700 border-slate-200";
};

const chartLabels: Record<Locale, Record<string, string>> = {
  en: {
    visualIntelligence: "Visual intelligence",
    businessCharts: "Business Charts",
    chartsSubtitle:
      "Backend-calculated trends for revenue, expenses, profit, cashflow, and categories.",
    chartsCount: "charts",
    latest: "Latest",
    businessTrend: "Business trend",
    categoryDistribution: "Category distribution",
    noChartData: "No chart data available.",
    revenueTrend: "Revenue Trend",
    expenseTrend: "Expense Trend",
    profitEvolution: "Profit Evolution",
    cashflowTrend: "Cashflow Trend",
    expensesByCategory: "Expenses by Category",
  },
  fr: {
    visualIntelligence: "Intelligence visuelle",
    businessCharts: "Graphiques business",
    chartsSubtitle:
      "Tendances calculées par le backend pour les revenus, dépenses, profit, cashflow et catégories.",
    chartsCount: "graphiques",
    latest: "Dernier",
    businessTrend: "Tendance business",
    categoryDistribution: "Répartition par catégorie",
    noChartData: "Aucune donnée graphique disponible.",
    revenueTrend: "Évolution des revenus",
    expenseTrend: "Évolution des dépenses",
    profitEvolution: "Évolution du profit",
    cashflowTrend: "Évolution du cashflow",
    expensesByCategory: "Dépenses par catégorie",
  },
  ar: {
    visualIntelligence: "الذكاء البصري",
    businessCharts: "مخططات الأعمال",
    chartsSubtitle:
      "اتجاهات محسوبة من النظام الخلفي للإيرادات والمصاريف والربح والتدفق النقدي والفئات.",
    chartsCount: "مخططات",
    latest: "الأحدث",
    businessTrend: "اتجاه النشاط",
    categoryDistribution: "توزيع الفئات",
    noChartData: "لا توجد بيانات رسومية متاحة.",
    revenueTrend: "تطور الإيرادات",
    expenseTrend: "تطور المصاريف",
    profitEvolution: "تطور الأرباح",
    cashflowTrend: "تطور التدفق النقدي",
    expensesByCategory: "المصاريف حسب الفئة",
  },
};

const normalizeChartTitle = (
  title: string | undefined,
  language: Locale
) => {
  const t = chartLabels[language];
  const normalized = String(title || "").trim();

  const titleMap: Record<string, string> = {
    "Revenue Trend": t.revenueTrend,
    "Expense Trend": t.expenseTrend,
    "Profit Evolution": t.profitEvolution,
    "Cashflow Trend": t.cashflowTrend,
    "Expenses by Category": t.expensesByCategory,

    "Évolution des revenus": t.revenueTrend,
    "Évolution des dépenses": t.expenseTrend,
    "Évolution du profit": t.profitEvolution,
    "Évolution du cashflow": t.cashflowTrend,
    "Dépenses par catégorie": t.expensesByCategory,

    "تطور الإيرادات": t.revenueTrend,
    "تطور المصاريف": t.expenseTrend,
    "تطور الأرباح": t.profitEvolution,
    "تطور التدفق النقدي": t.cashflowTrend,
    "المصاريف حسب الفئة": t.expensesByCategory,
  };

  return titleMap[normalized] || normalized || t.businessTrend;
};

const getChartSubtitle = (
  chart: BusinessChart,
  language: Locale
) => {
  const t = chartLabels[language];

  if (chart.type === "bar") {
    return t.categoryDistribution;
  }

  return t.businessTrend;
};

const getChartLatestValue = (chart: BusinessChart) => {
  const data = asArray(chart.data);
  const yKey = chart.y_key;

  if (!yKey || data.length === 0) {
    return null;
  }

  const latest = data[data.length - 1];

  if (!latest || typeof latest !== "object") {
    return null;
  }

  const value = latest[yKey];

  return typeof value === "number" ? value : null;
};

const getChartChange = (chart: BusinessChart) => {
  const data = asArray(chart.data);
  const yKey = chart.y_key;

  if (!yKey || data.length < 2) {
    return null;
  }

  const first = Number(data[0]?.[yKey]);
  const last = Number(data[data.length - 1]?.[yKey]);

  if (!Number.isFinite(first) || !Number.isFinite(last) || first === 0) {
    return null;
  }

  return ((last - first) / Math.abs(first)) * 100;
};

function MiniLineChart({
  chart,
  language,
  currency,
}: {
  chart: BusinessChart;
  language: Locale;
  currency: any;
}) {
  const data = asArray(chart.data);
  const xKey = chart.x_key || "period";
  const yKey = chart.y_key || "value";

  const values = data
    .map((item) => Number(item?.[yKey]))
    .filter((value) => Number.isFinite(value));

  if (data.length === 0 || values.length === 0) {
    return null;
  }

  return (
    <div className="h-72 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={data}
          margin={{
            top: 12,
            right: 18,
            left: 4,
            bottom: 12,
          }}
        >
          <CartesianGrid
            strokeDasharray="3 3"
            vertical={false}
            stroke="#e2e8f0"
          />

          <XAxis
            dataKey={xKey}
            tick={{
              fontSize: 12,
              fill: "#64748b",
            }}
            axisLine={false}
            tickLine={false}
            tickFormatter={(value) => String(value)}
          />

          <YAxis
            tick={{
              fontSize: 12,
              fill: "#64748b",
            }}
            axisLine={false}
            tickLine={false}
            width={72}
            tickFormatter={(value) =>
              formatChartValue(Number(value), chart, language, currency)
            }
          />

          <Tooltip
            cursor={{
              stroke: "#94a3b8",
              strokeDasharray: "3 3",
            }}
            formatter={(value: any) => [
              formatChartValue(Number(value), chart, language, currency),
              normalizeChartTitle(chart.title, language),
            ]}
            labelFormatter={(label) => String(label)}
            contentStyle={{
              borderRadius: "16px",
              border: "1px solid #e2e8f0",
              boxShadow: "0 18px 45px rgba(15, 23, 42, 0.12)",
              fontSize: "12px",
            }}
          />

          <Line
            type="monotone"
            dataKey={yKey}
            stroke="#0f172a"
            strokeWidth={3}
            dot={{
              r: 4,
              strokeWidth: 2,
              fill: "#ffffff",
              stroke: "#0f172a",
            }}
            activeDot={{
              r: 6,
              strokeWidth: 2,
              fill: "#0f172a",
              stroke: "#ffffff",
            }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

function MiniBarChart({
  chart,
  language,
  currency,
}: {
  chart: BusinessChart;
  language: Locale;
  currency: any;
}) {
  const data = asArray(chart.data);
  const xKey = chart.x_key || "category";
  const yKey = chart.y_key || "value";

  const chartData = data.map((item) => ({
    ...item,
    __translatedLabel: translateCategoryLabel(item?.[xKey], language),
  }));

  const values = chartData
    .map((item) => Number(item?.[yKey]))
    .filter((value) => Number.isFinite(value));

  if (chartData.length === 0 || values.length === 0) {
    return null;
  }

  return (
    <div className="h-72 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={chartData}
          margin={{
            top: 12,
            right: 18,
            left: 4,
            bottom: 12,
          }}
        >
          <CartesianGrid
            strokeDasharray="3 3"
            vertical={false}
            stroke="#e2e8f0"
          />

          <XAxis
            dataKey="__translatedLabel"
            tick={{
              fontSize: 12,
              fill: "#64748b",
            }}
            axisLine={false}
            tickLine={false}
          />

          <YAxis
            tick={{
              fontSize: 12,
              fill: "#64748b",
            }}
            axisLine={false}
            tickLine={false}
            width={72}
            tickFormatter={(value) =>
              formatChartValue(Number(value), chart, language, currency)
            }
          />

          <Tooltip
            cursor={{
              fill: "rgba(15, 23, 42, 0.06)",
            }}
            formatter={(value: any) => [
              formatChartValue(Number(value), chart, language, currency),
              normalizeChartTitle(chart.title, language),
            ]}
            labelFormatter={(label) => String(label)}
            contentStyle={{
              borderRadius: "16px",
              border: "1px solid #e2e8f0",
              boxShadow: "0 18px 45px rgba(15, 23, 42, 0.12)",
              fontSize: "12px",
            }}
          />

          <Bar
            dataKey={yKey}
            fill="#0f172a"
            radius={[10, 10, 0, 0]}
            maxBarSize={72}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

function LocalizedBusinessCharts({
  charts,
  language,
  currency,
}: {
  charts?: BusinessChart[];
  language: Locale;
  currency: any;
}) {
  const safeCharts = asArray(charts) as BusinessChart[];
  const t = chartLabels[language];

  if (safeCharts.length === 0) {
    return null;
  }

  return (
    <section className="rounded-[2rem] border border-slate-200 bg-gradient-to-b from-white to-slate-50 p-6 shadow-sm md:p-8">
      <div className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-xs uppercase tracking-wide text-slate-500">
            {t.visualIntelligence}
          </p>

          <h3 className="mt-1 text-xl font-bold text-slate-900">
            {t.businessCharts}
          </h3>

          <p className="mt-1 text-sm text-slate-500">
            {t.chartsSubtitle}
          </p>
        </div>

        <span className="w-fit rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-semibold text-slate-700">
          {safeCharts.length} {t.chartsCount}
        </span>
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        {safeCharts.map((chart, index) => {
          const latest = getChartLatestValue(chart);
          const change = getChartChange(chart);

          return (
            <article
              key={`${chart.title || "chart"}-${index}`}
              className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md"
            >
              <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                <div>
                  <h4 className="font-bold text-slate-900">
                    {normalizeChartTitle(chart.title, language)}
                  </h4>

                  <p className="text-sm text-slate-500">
                    {getChartSubtitle(chart, language)}
                  </p>
                </div>

                <div className="text-left sm:text-right">
                  <p className="text-xs text-slate-500">
                    {t.latest}
                  </p>

                  <p className="font-bold text-slate-900">
                    {latest === null
                      ? "-"
                      : formatChartValue(latest, chart, language, currency)}
                  </p>

                  {change !== null && (
                    <p
                      className={`text-xs font-semibold ${
                        change >= 0
                          ? "text-emerald-600"
                          : "text-red-600"
                      }`}
                    >
                      {change >= 0 ? "+" : ""}
                      {formatPercent(change, language)}
                    </p>
                  )}
                </div>
              </div>

              {chart.type === "bar" ? (
                <MiniBarChart
                  chart={chart}
                  language={language}
                  currency={currency}
                />
              ) : (
                <MiniLineChart
                  chart={chart}
                  language={language}
                  currency={currency}
                />
              )}

              {(!Array.isArray(chart.data) ||
                chart.data.length === 0) && (
                <p className="text-sm text-slate-500">
                  {t.noChartData}
                </p>
              )}
            </article>
          );
        })}
      </div>
    </section>
  );
}

function ResultList({
  items,
  variant = "default",
  language = "en",
}: {
  items?: any[];
  variant?: "default" | "risk" | "opportunity" | "recommendation";
  language?: Locale;
}) {
  const safeItems = asArray(items);

  if (safeItems.length === 0) {
    return (
      <p className="text-sm text-slate-500">
        -
      </p>
    );
  }

  const variantClasses = {
    default: "border-slate-200 bg-slate-50",
    risk: "border-red-200 bg-red-50",
    opportunity: "border-green-200 bg-green-50",
    recommendation: "border-blue-200 bg-blue-50",
  };

  return (
    <div className="space-y-3">
      {safeItems.map((item, index) => {
        const title = normalizeBackendText(getItemTitle(item), language);
        const description = normalizeBackendText(getItemDescription(item), language);
        const badge = normalizeBackendText(getItemBadge(item), language);

        return (
          <div
            key={index}
            className={`rounded-3xl border p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md ${variantClasses[variant]}`}
          >
            <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
              <div className="space-y-1">
                <p className="font-semibold text-slate-900">
                  {title}
                </p>

                {description && (
                  <p className="text-sm leading-relaxed text-slate-700">
                    {description}
                  </p>
                )}

                {Array.isArray(item?.business_impact) &&
                  item.business_impact.length > 0 && (
                    <div className="flex flex-wrap gap-2 pt-2">
                      {item.business_impact.map(
                        (impact: string, impactIndex: number) => (
                          <span
                            key={impactIndex}
                            className="rounded-full border border-slate-200 bg-white px-2 py-1 text-xs text-slate-600"
                          >
                            {normalizeBackendText(impact, language)}
                          </span>
                        )
                      )}
                    </div>
                  )}
              </div>

              {badge && (
                <span
                  className={`w-fit rounded-full border px-3 py-1 text-xs font-semibold ${badgeClass(
                    badge
                  )}`}
                >
                  {badge}
                </span>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}

function InfoCard({
  title,
  description,
  badge,
  index,
}: {
  title: string;
  description: string;
  badge?: string;
  index: number;
}) {
  return (
    <div className="rounded-3xl border border-slate-200 bg-gradient-to-b from-white to-slate-50 p-5 shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:shadow-md">
      <div className="mb-4 flex items-center justify-between gap-3">
        <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-slate-950 text-sm font-black text-white">
          {index + 1}
        </div>

        {badge && (
          <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-bold text-slate-700">
            {badge}
          </span>
        )}
      </div>

      <h3 className="text-base font-black text-slate-950">
        {title}
      </h3>

      <p className="mt-2 text-[13px] leading-6 text-slate-600">
        {description}
      </p>
    </div>
  );
}

function LoadingPanel({
  language,
  progress,
  step,
  elapsedSeconds,
}: {
  language: Locale;
  progress: number;
  step: string;
  elapsedSeconds: number;
}) {
  const text = {
    en: {
      elapsed: "Elapsed",
      quality: "Data quality",
      kpis: "KPI extraction",
      decision: "Decision layer",
      final: "Final report",
      seconds: "s",
    },
    fr: {
      elapsed: "Temps écoulé",
      quality: "Qualité des données",
      kpis: "Extraction KPI",
      decision: "Couche décisionnelle",
      final: "Rapport final",
      seconds: "s",
    },
    ar: {
      elapsed: "الوقت المنقضي",
      quality: "جودة البيانات",
      kpis: "استخراج المؤشرات",
      decision: "طبقة القرار",
      final: "التقرير النهائي",
      seconds: "ث",
    },
  }[language];

  const steps = [
    { label: text.quality, threshold: 20 },
    { label: text.kpis, threshold: 45 },
    { label: text.decision, threshold: 75 },
    { label: text.final, threshold: 95 },
  ];

  return (
    <div className="rounded-3xl border border-blue-100 bg-blue-50 p-5">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="font-bold text-blue-950">
            {step}
          </p>

          <p className="text-sm text-blue-700">
            {text.elapsed}: {elapsedSeconds}{text.seconds}
          </p>
        </div>

        <span className="rounded-full bg-white px-3 py-1 text-sm font-black text-blue-700">
          {progress}%
        </span>
      </div>

      <div className="mt-4 h-2 overflow-hidden rounded-full bg-white">
        <div
          className="h-full rounded-full bg-blue-600 transition-all duration-700"
          style={{ width: `${progress}%` }}
        />
      </div>

      <div className="mt-5 grid gap-3 md:grid-cols-4">
        {steps.map((item, index) => {
          const done = progress >= item.threshold;
          const active =
            !done &&
            progress >= (steps[index - 1]?.threshold || 0);

          return (
            <div
              key={item.label}
              className={`rounded-2xl border p-3 text-xs font-semibold ${
                done
                  ? "border-green-200 bg-green-50 text-green-800"
                  : active
                    ? "border-blue-200 bg-white text-blue-800"
                    : "border-slate-200 bg-white/70 text-slate-500"
              }`}
            >
              {done ? "✓" : active ? "⏳" : "○"} {item.label}
            </div>
          );
        })}
      </div>

      <div className="mt-5 grid gap-3 sm:grid-cols-3">
        {[0, 1, 2].map((item) => (
          <div
            key={item}
            className="animate-pulse rounded-2xl border border-blue-100 bg-white p-4"
          >
            <div className="h-3 w-1/3 rounded-full bg-slate-200" />
            <div className="mt-3 h-3 w-full rounded-full bg-slate-100" />
            <div className="mt-2 h-3 w-2/3 rounded-full bg-slate-100" />
          </div>
        ))}
      </div>
    </div>
  );
}


function SectionShell({
  children,
  className = "",
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <section
      className={`rounded-[2rem] border border-slate-200 bg-white/95 p-6 shadow-sm ring-1 ring-slate-950/[0.02] backdrop-blur md:p-8 ${className}`}
    >
      {children}
    </section>
  );
}

function KpiCard({
  label,
  value,
  helper,
  tone = "slate",
}: {
  label: string;
  value: React.ReactNode;
  helper?: React.ReactNode;
  tone?: "slate" | "green" | "amber" | "blue";
}) {
  const toneClass = {
    slate: "from-white to-slate-50",
    green: "from-white to-emerald-50/70",
    amber: "from-white to-amber-50/70",
    blue: "from-white to-blue-50/70",
  }[tone];

  return (
    <div
      className={`group rounded-3xl border border-slate-200 bg-gradient-to-b ${toneClass} p-5 shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:shadow-md`}
    >
      <p className="text-[13px] font-semibold text-slate-500">
        {label}
      </p>

      <p className="mt-3 break-words text-2xl font-black tracking-tight text-slate-950 md:text-3xl">
        {value}
      </p>

      {helper && (
        <div className="mt-2 text-xs font-semibold text-slate-500">
          {helper}
        </div>
      )}
    </div>
  );
}


export default function BusinessPage() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [language, setLanguage] = useState("en");
  const [plan, setPlan] = useState("");
  const [role, setRole] = useState("");
  const [creditsBalance, setCreditsBalance] = useState(0);
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [loadingStep, setLoadingStep] = useState("");
  const [startedAt, setStartedAt] = useState<number | null>(null);
  const [elapsedSeconds, setElapsedSeconds] = useState(0);
  const [exporting, setExporting] = useState<"pdf" | "pptx" | null>(null);
  const [exportMessage, setExportMessage] = useState("");

  useEffect(() => {
    setLanguage(getSavedLocale());

    const syncBillingState = () => {
      const savedPlan = safeGetLocalStorage("plan");
      const savedRole = safeGetLocalStorage("role");

      setPlan(savedPlan.toLowerCase().trim());
      setRole(savedRole.toLowerCase().trim());

      setCreditsBalance(
        Number(
          safeGetLocalStorage(
            "credits_balance",
            "0"
          )
        )
      );
    };

    syncBillingState();

    const cachedAnalysis = getLastBusinessAnalysis();

    if (cachedAnalysis) {
      setResult(cachedAnalysis);
    }

    window.addEventListener(
      "storage",
      syncBillingState
    );

    const handleLocaleChange = () => {
      setLanguage(getSavedLocale());
    };

    window.addEventListener(
      "locale-change",
      handleLocaleChange
    );

    refreshUserBilling();

    return () => {
      window.removeEventListener(
        "storage",
        syncBillingState
      );

      window.removeEventListener(
        "locale-change",
        handleLocaleChange
      );
    };
  }, []);

  useEffect(() => {
    if (!loading || !startedAt) {
      return;
    }

    const interval = window.setInterval(() => {
      setElapsedSeconds(
        Math.max(0, Math.floor((Date.now() - startedAt) / 1000))
      );
    }, 1000);

    return () => window.clearInterval(interval);
  }, [loading, startedAt]);

  useEffect(() => {
    if (!loading) {
      return;
    }

    const interval = window.setInterval(() => {
      setLoadingProgress((current) => {
        if (current < 20) return current + 4;
        if (current < 45) return current + 3;
        if (current < 75) return current + 2;
        if (current < 92) return current + 1;
        return current;
      });
    }, 700);

    return () => window.clearInterval(interval);
  }, [loading]);

  useEffect(() => {
    const locale = getLocale(language);
    const t = labels[locale] || labels.en;

    if (loadingProgress < 20) {
      setLoadingStep(t.loadingSteps.quality);
    } else if (loadingProgress < 45) {
      setLoadingStep(t.loadingSteps.kpis);
    } else if (loadingProgress < 75) {
      setLoadingStep(t.loadingSteps.forecast);
    } else if (loadingProgress < 95) {
      setLoadingStep(t.loadingSteps.decision);
    } else {
      setLoadingStep(t.loadingSteps.finalizing);
    }
  }, [loadingProgress, language]);

  const refreshUserBilling = async () => {
    const token = safeGetLocalStorage("token");

    if (!token) return;

    const res = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/users/me`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!res.ok) return;

    const data = await res.json();

    const nextPlan = String(
      data.plan || "trial"
    )
      .toLowerCase()
      .trim();

    const nextRole = String(
      data.role || "user"
    )
      .toLowerCase()
      .trim();

    const nextCreditsBalance = Number(
      data.credits_balance || 0
    );

    safeSetLocalStorage(
      "credits_balance",
      String(nextCreditsBalance)
    );

    safeSetLocalStorage(
      "plan",
      nextPlan
    );

    safeSetLocalStorage(
      "role",
      nextRole
    );

    setPlan(nextPlan);
    setRole(nextRole);
    setCreditsBalance(nextCreditsBalance);

    window.dispatchEvent(
      new Event("storage")
    );
  };

  const handleAnalyze = async () => {
    if (!file) {
      setMessage(t.noFile);
      return;
    }

    setLoading(true);
    setResult(null);
    setMessage("");
    setLoadingProgress(0);
    setLoadingStep("");
    setStartedAt(Date.now());
    setElapsedSeconds(0);

    try {
      let data;

      try {
        data = await analyzeBusinessFile(
          file,
          language
        );
      } catch (error: any) {
        const status = error?.response?.status;

        const detail =
          error?.response?.data?.detail ||
          error?.message ||
          "Failed to analyze business file.";

        if (status === 402) {
          setMessage(
            "Your enterprise quota for this AI agent has been exceeded."
          );

          return;
        }

        if (status === 403) {
          setMessage(
            detail || "Access denied"
          );

          return;
        }

        if (status === 429) {
          setMessage(
            "Too many requests. Please try again later."
          );

          return;
        }

        throw error;
      }

      setLoadingProgress(100);

      const token = safeGetLocalStorage("token");
      const savedAnalysisId =
        data?.analysis_id ||
        data?.business_analysis_id ||
        data?.id ||
        (await getLatestSavedBusinessAnalysisId(token, file.name));

      const nextResult = {
        ...data,
        analysis_id: savedAnalysisId || data?.analysis_id,
      };

      setResult(nextResult);

      saveLastBusinessAnalysis(
        nextResult,
        file.name
      );

      await refreshUserBilling();
    } catch (error: any) {
      setMessage(
        error?.message ||
          "Failed to analyze business file."
      );
    } finally {
      setLoading(false);
      setStartedAt(null);
    }
  };

  const handleExport = async (kind: "pdf" | "pptx") => {
    setExporting(kind);
    setExportMessage("");

    try {
      const token = safeGetLocalStorage("token");

      let analysisId =
        result?.analysis_id ||
        result?.business_analysis_id ||
        result?.id;

      if (!analysisId) {
        analysisId = await getLatestSavedBusinessAnalysisId(
          token,
          file?.name || result?.file_metadata?.file_name
        );
      }

      if (!analysisId) {
        setExportMessage(t.exportNeedsHistory);
        return;
      }

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/business/export/${kind}/${analysisId}`,
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
          // File endpoints may not always return JSON errors.
        }

        setExportMessage(detail);
        return;
      }

      await downloadBlob(
        response,
        `business_analysis_${analysisId}.${kind}`
      );

      setExportMessage(t.exportSuccess);
    } catch (error: any) {
      setExportMessage(error?.message || t.exportError);
    } finally {
      setExporting(null);
    }
  };

  const score = Number(
    result?.business_health_score || 0
  );

  const labels: Record<Locale, Record<string, any>> = {
    en: {
      title: "Business Decision Intelligence",
      subtitle:
        "Upload business data to receive a data-verified executive analysis with KPIs, risks, opportunities, forecasts, and priority decisions.",
      eyebrow: "Universal AI business agent",
      chooseFile: "Choose file",
      noFile: "No file selected",
      analyze: "Analyze Business",
      loading: "Analyzing business data...",
      results: "AI Executive Business Analysis",
      summary: "Executive Summary",
      score: "Business Health Score",
      businessModel: "Business Model",
      insights: "Key Insights",
      risks: "Risks",
      opportunities: "Opportunities",
      recommendations: "Recommendations",
      decision: "Priority Decision",
      forecast: "Forecast",
      revenue: "Revenue",
      expenses: "Expenses",
      profit: "Profit",
      margin: "Margin",
      growth: "Growth",
      cashflow: "Cashflow",
      currency: "Currency",
      multiCurrencyWarning: "Multiple currencies detected",
      confidence: "Confidence",
      source: "Source",
      verifiedAnalysis: "Data-verified analysis",
      exportPdf: "Export PDF",
      exportPptx: "Export PowerPoint",
      exportingPdf: "Generating PDF...",
      exportingPptx: "Generating PowerPoint...",
      exportSuccess: "Report exported successfully.",
      exportError: "Failed to export report.",
      exportNeedsHistory: "Open the dashboard to export the saved analysis.",
      dashboard: "Open dashboard",
      whatItIs: "What this agent does",
      howItWorks: "How it works",
      dataTypes: "Supported business data",
      enterpriseReady: "Public & enterprise-ready",
      trustedData: "Numbers stay backend-calculated. AI explains, the backend verifies.",
      whatYouGetItems: [
        "Executive business summary",
        "Financial KPI calculation",
        "Risk and anomaly detection",
        "Strategic recommendations",
      ],
      whatYouGetDescriptions: [
        "Understand revenue, profit, margin, growth, cashflow, and operational signals in one clear view.",
        "The backend calculates core metrics and advanced KPIs before any narrative is generated.",
        "Detect churn pressure, profitability risks, cashflow issues, and unusual business signals.",
        "Receive practical decisions, opportunities, and next actions for public users or enterprise teams.",
      ],
      whatYouGetBadges: [
        "Summary",
        "KPIs",
        "Risks",
        "Decisions",
      ],
      howItWorksItems: [
        "Upload a CSV or Excel file",
        "Choose the output language",
        "Receive a structured executive dashboard",
      ],
      workflowDescriptions: [
        "Works with business data from SaaS, commerce, services, agencies, restaurants, marketplaces, and general operations.",
        "The input file can be in Arabic, French, or English. The output can be Arabic, French, or English.",
        "The system returns KPIs, charts, forecast, data quality, risks, opportunities, and recommendations.",
      ],
      dataTypeItems: [
        "Financial columns",
        "Customer and retention data",
        "Marketing and sales data",
        "Operations and categories",
      ],
      dataTypeDescriptions: [
        "Revenue, expenses, profit, cashflow, monthly periods, cost categories, and margins.",
        "Customers, new customers, churned customers, retention, MRR, ARR, and revenue per customer.",
        "Orders, ad spend, ROAS, CAC, channels, conversion-related data, and sales performance.",
        "Business categories, departments, stores, products, services, regions, or custom operating fields.",
      ],
      loadingSteps: {
        quality: "Checking data quality...",
        kpis: "Calculating KPIs...",
        forecast: "Building forecast and charts...",
        decision: "Detecting risks and priority decisions...",
        finalizing: "Finalizing executive report...",
      },
    },

    fr: {
      title: "Intelligence décisionnelle business",
      subtitle:
        "Importez vos données business pour recevoir une analyse exécutive vérifiée par les données avec KPIs, risques, opportunités, prévisions et décisions prioritaires.",
      eyebrow: "Agent business IA universel",
      chooseFile: "Choisir un fichier",
      noFile: "Aucun fichier sélectionné",
      analyze: "Analyser le business",
      loading: "Analyse des données business...",
      results: "Analyse exécutive business IA",
      summary: "Résumé exécutif",
      score: "Score de santé business",
      businessModel: "Modèle business",
      insights: "Points clés",
      risks: "Risques",
      opportunities: "Opportunités",
      recommendations: "Recommandations",
      decision: "Décision prioritaire",
      forecast: "Prévisions",
      revenue: "Revenus",
      expenses: "Dépenses",
      profit: "Profit",
      margin: "Marge",
      growth: "Croissance",
      cashflow: "Cashflow",
      currency: "Devise",
      multiCurrencyWarning: "Plusieurs devises détectées",
      confidence: "Confiance",
      source: "Source",
      verifiedAnalysis: "Analyse vérifiée par les données",
      exportPdf: "Exporter PDF",
      exportPptx: "Exporter PowerPoint",
      exportingPdf: "Génération du PDF...",
      exportingPptx: "Génération du PowerPoint...",
      exportSuccess: "Rapport exporté avec succès.",
      exportError: "Échec de l’export du rapport.",
      exportNeedsHistory: "Ouvrez le dashboard pour exporter l’analyse sauvegardée.",
      dashboard: "Ouvrir le dashboard",
      whatItIs: "Ce que fait cet agent",
      howItWorks: "Fonctionnement",
      dataTypes: "Données business prises en charge",
      enterpriseReady: "Prêt public & entreprise",
      trustedData: "Les chiffres restent calculés par le backend. L’IA explique, le backend vérifie.",
      whatYouGetItems: [
        "Résumé exécutif business",
        "Calcul des KPIs financiers",
        "Détection des risques et anomalies",
        "Recommandations stratégiques",
      ],
      whatYouGetDescriptions: [
        "Comprendre revenus, profit, marge, croissance, cashflow et signaux opérationnels dans une vue claire.",
        "Le backend calcule les métriques clés et les KPIs avancés avant toute génération narrative.",
        "Détecter churn, risques de rentabilité, pression cashflow et signaux business inhabituels.",
        "Recevoir des décisions pratiques, opportunités et prochaines actions pour utilisateurs publics ou équipes entreprise.",
      ],
      whatYouGetBadges: [
        "Résumé",
        "KPIs",
        "Risques",
        "Décisions",
      ],
      howItWorksItems: [
        "Importez un fichier CSV ou Excel",
        "Choisissez la langue de sortie",
        "Recevez un dashboard exécutif structuré",
      ],
      workflowDescriptions: [
        "Fonctionne avec SaaS, commerce, services, agences, restaurants, marketplaces et opérations générales.",
        "Le fichier source peut être en arabe, français ou anglais. La sortie peut être en arabe, français ou anglais.",
        "Le système retourne KPIs, graphiques, prévisions, qualité des données, risques, opportunités et recommandations.",
      ],
      dataTypeItems: [
        "Colonnes financières",
        "Données clients et rétention",
        "Marketing et ventes",
        "Opérations et catégories",
      ],
      dataTypeDescriptions: [
        "Revenus, dépenses, profit, cashflow, périodes mensuelles, catégories de coûts et marges.",
        "Clients, nouveaux clients, clients perdus, rétention, MRR, ARR et revenus par client.",
        "Commandes, dépenses publicitaires, ROAS, CAC, canaux, conversion et performance commerciale.",
        "Catégories business, départements, magasins, produits, services, régions ou champs opérationnels personnalisés.",
      ],
      loadingSteps: {
        quality: "Vérification de la qualité des données...",
        kpis: "Calcul des KPIs...",
        forecast: "Construction des prévisions et graphiques...",
        decision: "Détection des risques et décisions prioritaires...",
        finalizing: "Finalisation du rapport exécutif...",
      },
    },

    ar: {
      title: "ذكاء قرارات الأعمال",
      subtitle:
        "ارفع بيانات الأعمال للحصول على تحليل تنفيذي موثوق بالبيانات يتضمن المؤشرات والمخاطر والفرص والتوقعات والقرارات ذات الأولوية.",
      eyebrow: "وكيل أعمال ذكي عالمي",
      chooseFile: "اختيار ملف",
      noFile: "لم يتم اختيار ملف",
      analyze: "تحليل الأعمال",
      loading: "جاري تحليل بيانات الأعمال...",
      results: "نتائج التحليل التنفيذي للأعمال",
      summary: "الملخص التنفيذي",
      score: "مستوى صحة الأعمال",
      businessModel: "نوع النشاط",
      insights: "النقاط الرئيسية",
      risks: "المخاطر",
      opportunities: "الفرص",
      recommendations: "التوصيات",
      decision: "القرار الأولوي",
      forecast: "التوقعات",
      revenue: "الإيرادات",
      expenses: "المصاريف",
      profit: "الأرباح",
      margin: "الهامش",
      growth: "النمو",
      cashflow: "التدفق النقدي",
      currency: "العملة",
      multiCurrencyWarning: "تم اكتشاف عدة عملات",
      confidence: "الثقة",
      source: "المصدر",
      verifiedAnalysis: "تحليل موثوق بالبيانات",
      exportPdf: "تصدير PDF",
      exportPptx: "تصدير PowerPoint",
      exportingPdf: "جاري إنشاء PDF...",
      exportingPptx: "جاري إنشاء PowerPoint...",
      exportSuccess: "تم تصدير التقرير بنجاح.",
      exportError: "فشل تصدير التقرير.",
      exportNeedsHistory: "افتح لوحة التحكم لتصدير التحليل المحفوظ.",
      dashboard: "فتح لوحة التحكم",
      whatItIs: "ماذا يفعل هذا الوكيل",
      howItWorks: "آلية العمل",
      dataTypes: "أنواع بيانات الأعمال المدعومة",
      enterpriseReady: "جاهز للاستخدام العام والمؤسسات",
      trustedData: "الأرقام تُحسب في النظام الخلفي. الذكاء الاصطناعي يشرح، والنظام الخلفي يتحقق.",
      whatYouGetItems: [
        "ملخص تنفيذي للأعمال",
        "حساب مؤشرات الأداء المالية",
        "كشف المخاطر والشذوذ",
        "توصيات استراتيجية",
      ],
      whatYouGetDescriptions: [
        "فهم الإيرادات والربح والهامش والنمو والتدفق النقدي والإشارات التشغيلية في واجهة واضحة.",
        "النظام الخلفي يحسب المؤشرات الأساسية والمتقدمة قبل إنشاء أي سرد أو تفسير.",
        "كشف ضغط فقدان العملاء ومخاطر الربحية ومشاكل التدفق النقدي والإشارات غير المعتادة.",
        "الحصول على قرارات عملية وفرص وخطوات تالية للمستخدمين العامين أو فرق المؤسسات.",
      ],
      whatYouGetBadges: [
        "ملخص",
        "مؤشرات",
        "مخاطر",
        "قرارات",
      ],
      howItWorksItems: [
        "ارفع ملف CSV أو Excel",
        "اختر لغة التقرير",
        "احصل على لوحة تنفيذية منظمة",
      ],
      workflowDescriptions: [
        "يعمل مع SaaS والتجارة والخدمات والوكالات والمطاعم والأسواق الرقمية والعمليات العامة.",
        "يمكن أن يكون ملف الإدخال بالعربية أو الفرنسية أو الإنجليزية. ويمكن أن تكون المخرجات بالعربية أو الفرنسية أو الإنجليزية.",
        "يعرض النظام المؤشرات والرسوم والتوقعات وجودة البيانات والمخاطر والفرص والتوصيات.",
      ],
      dataTypeItems: [
        "الأعمدة المالية",
        "بيانات العملاء والاحتفاظ",
        "التسويق والمبيعات",
        "العمليات والفئات",
      ],
      dataTypeDescriptions: [
        "الإيرادات، المصاريف، الربح، التدفق النقدي، الفترات الشهرية، فئات التكاليف والهامش.",
        "العملاء، العملاء الجدد، العملاء المفقودون، الاحتفاظ، MRR، ARR والإيراد لكل عميل.",
        "الطلبات، الإنفاق الإعلاني، ROAS، CAC، القنوات، التحويل وأداء المبيعات.",
        "فئات الأعمال، الأقسام، المتاجر، المنتجات، الخدمات، المناطق أو الحقول التشغيلية المخصصة.",
      ],
      loadingSteps: {
        quality: "فحص جودة البيانات...",
        kpis: "حساب المؤشرات...",
        forecast: "إنشاء التوقعات والرسوم...",
        decision: "كشف المخاطر والقرارات ذات الأولوية...",
        finalizing: "إنهاء التقرير التنفيذي...",
      },
    },
  };

  const locale = getLocale(language);
  const t = labels[locale] || labels.en;

  const getScoreColor = (
    score: number
  ) => {
    if (score >= 80) {
      return "bg-green-500";
    }

    if (score >= 60) {
      return "bg-yellow-500";
    }

    return "bg-red-500";
  };

  const decision =
    result?.smart_insights?.most_important_decision;
  const keyInsights = asArray(
    result?.smart_insights?.key_insights
  );
  const risks = asArray(result?.risks);
  const opportunities = asArray(
    result?.opportunities
  );
  const recommendations = asArray(
    result?.recommendations
  );

  const charts = useMemo(
    () => asArray(result?.charts) as BusinessChart[],
    [result]
  );

  const currency = result?.currency || null;
  const hasCurrency = Boolean(currency?.code || currency?.symbol);

  return (
    <main
      dir={
        locale === "ar"
          ? "rtl"
          : "ltr"
      }
      className={`min-h-screen bg-[radial-gradient(circle_at_top,_#f8fafc_0,_#eef2ff_32%,_#f8fafc_70%)] px-4 py-10 ${
        locale === "ar" ? "tracking-normal" : ""
      }`}
    >
      <div className="mx-auto max-w-7xl space-y-10">
        {/* Hero */}
        <section className="overflow-hidden rounded-[2.25rem] border border-slate-200 bg-white/95 shadow-sm ring-1 ring-slate-950/[0.02] backdrop-blur">
          <div className="grid gap-8 p-6 md:p-8 lg:grid-cols-[1.35fr_0.85fr] lg:p-10">
            <div>
              <div className="flex flex-wrap gap-2">
                <span className="rounded-full border border-blue-200 bg-blue-50 px-3 py-1 text-xs font-bold text-blue-700">
                  {t.eyebrow}
                </span>

                <span className="rounded-full border border-green-200 bg-green-50 px-3 py-1 text-xs font-bold text-green-700">
                  {t.enterpriseReady}
                </span>
              </div>

              <h1 className={`mt-6 max-w-4xl text-4xl font-black tracking-tight text-slate-950 md:text-6xl ${
                locale === "ar" ? "leading-[1.35]" : "leading-[1.03]"
              }`}>
                {t.title}
              </h1>

              <p className={`mt-5 max-w-3xl text-[15px] text-slate-600 md:text-base ${
                locale === "ar" ? "leading-8" : "leading-7"
              }`}>
                {t.subtitle}
              </p>

              <p className={`mt-5 max-w-3xl rounded-3xl border border-slate-200 bg-gradient-to-b from-white to-slate-50 p-5 text-sm font-semibold text-slate-700 shadow-sm ${
                locale === "ar" ? "leading-8" : "leading-6"
              }`}>
                {t.trustedData}
              </p>
            </div>

            <div className="rounded-[2rem] border border-slate-800 bg-slate-950 p-6 text-white shadow-xl shadow-slate-950/10">
              <p className="text-sm font-semibold text-slate-300">
                {t.dataTypes}
              </p>

              <div className="mt-5 grid gap-3">
                {t.dataTypeItems.map((item: string, index: number) => (
                  <div
                    key={item}
                    className="rounded-2xl bg-white/10 p-3"
                  >
                    <p className="font-bold">
                      {item}
                    </p>

                    <p className="mt-1 text-xs leading-5 text-slate-300">
                      {t.dataTypeDescriptions[index]}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* Explanation */}
        <section className="grid grid-cols-1 gap-5 lg:grid-cols-2">
          <SectionShell>
            <h2 className="text-2xl font-black text-slate-950">
              {t.whatItIs}
            </h2>

            <div className="mt-5 grid gap-4 sm:grid-cols-2">
              {t.whatYouGetItems.map((item: string, index: number) => (
                <InfoCard
                  key={item}
                  title={item}
                  description={t.whatYouGetDescriptions[index]}
                  badge={t.whatYouGetBadges[index]}
                  index={index}
                />
              ))}
            </div>
          </SectionShell>

          <SectionShell>
            <h2 className="text-2xl font-black text-slate-950">
              {t.howItWorks}
            </h2>

            <div className="mt-5 space-y-4">
              {t.howItWorksItems.map((item: string, index: number) => (
                <InfoCard
                  key={item}
                  title={item}
                  description={t.workflowDescriptions[index]}
                  index={index}
                />
              ))}
            </div>
          </SectionShell>
        </section>

        {/* Upload Card */}
        <SectionShell className="space-y-6">
          <select
            value={language}
            onChange={(e) => {
              setLanguage(e.target.value);
              setSavedLocale(e.target.value);
            }}
            className="w-full rounded-2xl border border-slate-300 bg-white px-4 py-4 text-sm font-semibold outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
          >
            <option value="en">
              English
            </option>

            <option value="fr">
              Français
            </option>

            <option value="ar">
              العربية
            </option>
          </select>

          <div className="space-y-2">
            <input
              id="file-upload"
              type="file"
              accept=".csv,.xlsx,.xls"
              className="hidden"
              onChange={(e) => {
                const selectedFile = e.target.files?.[0] || null;
                setFile(selectedFile);
                setMessage("");
                setExportMessage("");
              }}
            />

            <label
              htmlFor="file-upload"
              className="flex cursor-pointer items-center justify-between rounded-3xl border border-slate-200 bg-gradient-to-b from-white to-slate-50 px-5 py-5 shadow-sm transition hover:border-blue-200 hover:bg-blue-50/40 hover:shadow-md"
            >
              <span className="truncate text-sm font-medium text-slate-700">
                {file
                  ? file.name
                  : t.noFile}
              </span>

              <span className="rounded-full bg-slate-950 px-4 py-2 text-sm font-bold text-white">
                {t.chooseFile}
              </span>
            </label>
          </div>

          <button
            onClick={handleAnalyze}
            disabled={!file || loading}
            className="w-full rounded-3xl bg-slate-950 px-6 py-4 text-sm font-black text-white shadow-sm transition hover:-translate-y-0.5 hover:bg-slate-800 hover:shadow-md disabled:translate-y-0 disabled:bg-slate-400 disabled:shadow-none"
          >
            {loading
              ? t.loading
              : t.analyze}
          </button>

          {message && (
            <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-center text-sm text-red-700">
              {message}
            </div>
          )}

          {loading && (
            <LoadingPanel
              language={locale}
              progress={loadingProgress}
              step={loadingStep || t.loading}
              elapsedSeconds={elapsedSeconds}
            />
          )}
        </SectionShell>

        {/* Results */}
        {result && (
          <SectionShell className="space-y-8">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <h2 className="text-2xl font-black text-slate-950">
                {t.results}
              </h2>

              <div className="flex flex-wrap items-center gap-2">
                {result.backend_truth?.source && (
                  <span
                    title={result.backend_truth.source}
                    className="w-fit rounded-full border border-green-200 bg-green-50 px-3 py-1 text-xs font-bold text-green-700"
                  >
                    {t.verifiedAnalysis}
                  </span>
                )}

                <button
                  type="button"
                  onClick={() => handleExport("pdf")}
                  disabled={exporting !== null}
                  className="rounded-full bg-slate-950 px-4 py-2 text-xs font-bold text-white transition hover:bg-slate-800 disabled:bg-slate-400"
                >
                  {exporting === "pdf" ? t.exportingPdf : t.exportPdf}
                </button>

                <button
                  type="button"
                  onClick={() => handleExport("pptx")}
                  disabled={exporting !== null}
                  className="rounded-full border border-slate-200 bg-white px-4 py-2 text-xs font-bold text-slate-800 transition hover:bg-slate-50 disabled:text-slate-400"
                >
                  {exporting === "pptx" ? t.exportingPptx : t.exportPptx}
                </button>

                <a
                  href="/business/dashboard"
                  className="rounded-full border border-blue-200 bg-blue-50 px-4 py-2 text-xs font-bold text-blue-700"
                >
                  {t.dashboard}
                </a>
              </div>
            </div>

            {exportMessage && (
              <div className={`rounded-2xl border px-4 py-3 text-sm font-semibold ${
                exportMessage === t.exportSuccess
                  ? "border-emerald-200 bg-emerald-50 text-emerald-700"
                  : exportMessage === t.exportNeedsHistory
                    ? "border-blue-200 bg-blue-50 text-blue-700"
                    : "border-red-200 bg-red-50 text-red-700"
              }`}>
                {exportMessage}
              </div>
            )}

            {/* Summary */}
            <div>
              <h3 className="mb-2 text-lg font-black text-slate-950">
                {t.summary}
              </h3>

              <p className={`text-[15px] text-slate-600 ${
                locale === "ar" ? "leading-8" : "leading-7"
              }`}>
                {normalizeBackendText(result.executive_summary || "-", locale)}
              </p>

              {result.currency_warning && (
                <div className="mt-4 rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm font-semibold text-amber-800">
                  {t.multiCurrencyWarning}
                </div>
              )}
            </div>

            {/* Score */}
            <div className="space-y-4 rounded-3xl border border-slate-200 bg-gradient-to-b from-white to-slate-50 p-6 shadow-sm">
              <div className="flex justify-between">
                <span className="font-bold text-slate-700">
                  {t.score}
                </span>

                <span className="font-black text-slate-950">
                  {score}/100
                </span>
              </div>

              <div className="h-3 bg-slate-200 rounded-full">
                <div
                  className={`h-3 rounded-full ${getScoreColor(
                    score
                  )}`}
                  style={{
                    width: `${Math.min(
                      Math.max(score, 0),
                      100
                    )}%`,
                  }}
                />
              </div>
            </div>

            {/* Business Model */}
            <div className="rounded-3xl border border-slate-200 bg-gradient-to-b from-white to-slate-50 p-5 shadow-sm">
              <p className="text-sm text-slate-500 mb-1">
                {t.businessModel}
              </p>

              <p className="font-semibold capitalize">
                {result.business_model || "general"}
              </p>
            </div>

            {/* KPI Grid */}
            <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 xl:grid-cols-6">
              <KpiCard
                label={t.revenue}
                value={formatMoney(result.kpis?.revenue, currency, locale)}
                tone="green"
              />

              <KpiCard
                label={t.expenses}
                value={formatMoney(result.kpis?.expenses, currency, locale)}
                tone="amber"
              />

              <KpiCard
                label={t.profit}
                value={formatMoney(result.kpis?.profit, currency, locale)}
                tone="green"
              />

              <KpiCard
                label={t.margin}
                value={formatPercent(result.kpis?.profit_margin_percent, locale)}
              />

              <KpiCard
                label={t.growth}
                value={formatPercent(result.kpis?.growth_rate_percent, locale)}
                tone="blue"
              />

              <KpiCard
                label={t.currency}
                value={hasCurrency ? getCurrencyDisplay(currency, locale) : "-"}
                helper={
                  currency?.multi_currency_detected
                    ? t.multiCurrencyWarning
                    : undefined
                }
              />
            </div>

            {/* Charts */}
            {charts.length > 0 && (
              <LocalizedBusinessCharts
                charts={charts}
                language={locale}
                currency={currency}
              />
            )}

            {/* Decision */}
            {decision && (
              <div className="rounded-[2rem] border border-amber-200 bg-gradient-to-b from-amber-50 to-white p-6 shadow-sm">
                <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                  <div>
                    <p className="text-xs uppercase text-amber-700 font-bold mb-2">
                      {t.decision}
                    </p>

                    <h3 className="text-lg font-black mb-2 text-slate-950">
                      {normalizeBackendText(decision.title || "-", locale)}
                    </h3>

                    <p className="text-slate-700">
                      {normalizeBackendText(decision.decision || "-", locale)}
                    </p>

                    {decision.why && (
                      <p className="mt-2 text-sm leading-relaxed text-slate-600">
                        {normalizeBackendText(decision.why, locale)}
                      </p>
                    )}
                  </div>

                  {decision.impact && (
                    <span
                      className={`w-fit rounded-full border px-3 py-1 text-xs font-bold ${badgeClass(
                        decision.impact
                      )}`}
                    >
                      {normalizeBackendText(decision.impact, locale)}
                    </span>
                  )}
                </div>
              </div>
            )}

            {/* Insights */}
            {keyInsights.length > 0 && (
              <div>
                <h3 className="mb-3 text-lg font-black text-slate-950">
                  {t.insights}
                </h3>

                <ul className="space-y-2">
                  {keyInsights.map(
                    (
                      item: string,
                      index: number
                    ) => (
                      <li
                        key={index}
                        className="flex gap-2 text-slate-700"
                      >
                        <span>•</span>
                        <span>{item}</span>
                      </li>
                    )
                  )}
                </ul>
              </div>
            )}

            {/* Risks / Opportunities */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {risks.length > 0 && (
                <div>
                  <h3 className="font-bold mb-3 text-red-600">
                    {t.risks}
                  </h3>

                  <ResultList
                    items={risks}
                    variant="risk"
                    language={locale}
                  />
                </div>
              )}

              {opportunities.length > 0 && (
                <div>
                  <h3 className="font-bold mb-3 text-green-600">
                    {t.opportunities}
                  </h3>

                  <ResultList
                    items={opportunities}
                    variant="opportunity"
                    language={locale}
                  />
                </div>
              )}
            </div>

            {/* Recommendations */}
            {recommendations.length > 0 && (
              <div>
                <h3 className="mb-3 text-lg font-black text-slate-950">
                  {t.recommendations}
                </h3>

                <ResultList
                  items={recommendations}
                  variant="recommendation"
                  language={locale}
                />
              </div>
            )}

            {/* Disclaimer */}
            {result.disclaimer && (
              <p className="text-xs text-slate-500 border-t pt-4">
                {result.disclaimer}
              </p>
            )}
          </SectionShell>
        )}
      </div>
    </main>
  );
}
