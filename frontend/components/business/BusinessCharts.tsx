
"use client";

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

type Locale = "en" | "fr" | "ar";
type ChartValue = string | number | null | undefined;
type BusinessChartRow = Record<string, ChartValue>;

type BusinessChart = {
  type: "line" | "bar" | string;
  title: string;
  x_key: string;
  y_key: string;
  data: BusinessChartRow[];
};

type BusinessChartsProps = {
  charts?: BusinessChart[];
  language?: Locale;
  currency?: any;
};

type TooltipPayloadItem = {
  name?: string | number;
  value?: ChartValue;
};

type CustomTooltipProps = {
  active?: boolean;
  label?: string | number;
  payload?: TooltipPayloadItem[];
  language: Locale;
};

const chartLabels: Record<Locale, Record<string, string>> = {
  en: {
    businessCharts: "Business Charts",
    subtitle: "Visual overview of revenue, expenses, profit, cashflow, and categories.",
    trend: "Business trend",
    category: "Category distribution",
    value: "Value",
    revenue: "Revenue Trend",
    expense: "Expense Trend",
    profit: "Profit Evolution",
    cashflow: "Cashflow Trend",
    expensesByCategory: "Expenses by Category",
  },
  fr: {
    businessCharts: "Graphiques business",
    subtitle: "Vue visuelle des revenus, dépenses, profit, cashflow et catégories.",
    trend: "Tendance business",
    category: "Répartition par catégorie",
    value: "Valeur",
    revenue: "Évolution des revenus",
    expense: "Évolution des dépenses",
    profit: "Évolution du profit",
    cashflow: "Évolution du cashflow",
    expensesByCategory: "Dépenses par catégorie",
  },
  ar: {
    businessCharts: "مخططات الأعمال",
    subtitle: "عرض بصري للإيرادات والمصاريف والأرباح والتدفق النقدي والفئات.",
    trend: "اتجاه الأعمال",
    category: "توزيع الفئات",
    value: "القيمة",
    revenue: "تطور الإيرادات",
    expense: "تطور المصاريف",
    profit: "تطور الأرباح",
    cashflow: "تطور التدفق النقدي",
    expensesByCategory: "المصاريف حسب الفئة",
  },
};

const normalizeTitle = (title: string, language: Locale) => {
  const t = chartLabels[language];
  const map: Record<string, string> = {
    "Revenue Trend": t.revenue,
    "Expense Trend": t.expense,
    "Profit Evolution": t.profit,
    "Cashflow Trend": t.cashflow,
    "Expenses by Category": t.expensesByCategory,
    "Évolution des revenus": t.revenue,
    "Évolution des dépenses": t.expense,
    "Évolution du profit": t.profit,
    "Évolution du cashflow": t.cashflow,
    "Dépenses par catégorie": t.expensesByCategory,
    "تطور الإيرادات": t.revenue,
    "تطور المصاريف": t.expense,
    "تطور الأرباح": t.profit,
    "تطور التدفق النقدي": t.cashflow,
    "المصاريف حسب الفئة": t.expensesByCategory,
  };

  return map[String(title || "").trim()] || title;
};

const translateCategory = (value: ChartValue, language: Locale) => {
  const raw = String(value ?? "");
  const map: Record<string, Record<Locale, string>> = {
    Payroll: { en: "Payroll", fr: "Masse salariale", ar: "الرواتب" },
    Marketing: { en: "Marketing", fr: "Marketing", ar: "التسويق" },
    Software: { en: "Software", fr: "Logiciels", ar: "البرمجيات" },
  };

  return map[raw]?.[language] || raw;
};

const formatNumber = (value: ChartValue, language: Locale) => {
  if (typeof value !== "number") {
    return value ?? "-";
  }

  const locale = language === "fr" ? "fr-FR" : language === "ar" ? "ar-MA" : "en-US";

  return new Intl.NumberFormat(locale, {
    maximumFractionDigits: 2,
  }).format(value);
};

const formatMoney = (value: ChartValue, currency: any, language: Locale) => {
  if (typeof value !== "number") return value ?? "-";
  const number = formatNumber(value, language);
  const displayCurrency = currency?.symbol || currency?.code || "";
  if (!displayCurrency) return number;
  if (language === "ar" || currency?.position === "suffix") return `${number} ${displayCurrency}`.trim();
  return `${displayCurrency}${number}`;
};

const formatChartValue = (value: ChartValue, chart: BusinessChart, language: Locale, currency: any) => {
  const key = String(chart.y_key || "").toLowerCase();
  if (
    key.includes("revenue") ||
    key.includes("expense") ||
    key.includes("profit") ||
    key.includes("cashflow") ||
    key.includes("cost") ||
    key.includes("spend")
  ) {
    return formatMoney(value, currency, language);
  }

  return formatNumber(value, language);
};

const CustomTooltip = ({ active, payload, label, language }: CustomTooltipProps) => {
  if (!active || !payload || payload.length === 0) return null;

  return (
    <div className="rounded-xl border bg-white px-3 py-2 text-sm shadow-sm">
      <p className="mb-1 font-medium text-slate-900">{label ?? ""}</p>
      {payload.map((item, index) => (
        <p key={index} className="text-slate-600">
          {String(item.name ?? chartLabels[language].value)}: <span className="font-semibold text-slate-900">{formatNumber(item.value, language)}</span>
        </p>
      ))}
    </div>
  );
};

function LineChartCard({ chart, language, currency }: { chart: BusinessChart; language: Locale; currency: any }) {
  return (
    <div className="rounded-2xl border bg-white p-5 shadow-sm">
      <div className="mb-4">
        <h3 className="font-semibold text-slate-900">{normalizeTitle(chart.title, language)}</h3>
        <p className="mt-1 text-xs text-slate-500">{chartLabels[language].trend}</p>
      </div>
      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chart.data}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
            <XAxis dataKey={chart.x_key} tick={{ fontSize: 12, fill: "#64748b" }} minTickGap={20} axisLine={false} tickLine={false} />
            <YAxis tick={{ fontSize: 12, fill: "#64748b" }} width={72} axisLine={false} tickLine={false} tickFormatter={(value: ChartValue) => String(formatChartValue(value, chart, language, currency))} />
            <Tooltip content={<CustomTooltip language={language} />} />
            <Line type="monotone" dataKey={chart.y_key} stroke="#0f172a" strokeWidth={3} dot={false} activeDot={{ r: 5 }} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

function BarChartCard({ chart, language, currency }: { chart: BusinessChart; language: Locale; currency: any }) {
  const data = chart.data.map((row) => ({ ...row, __localizedLabel: translateCategory(row[chart.x_key], language) }));

  return (
    <div className="rounded-2xl border bg-white p-5 shadow-sm">
      <div className="mb-4">
        <h3 className="font-semibold text-slate-900">{normalizeTitle(chart.title, language)}</h3>
        <p className="mt-1 text-xs text-slate-500">{chartLabels[language].category}</p>
      </div>
      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
            <XAxis dataKey="__localizedLabel" tick={{ fontSize: 12, fill: "#64748b" }} minTickGap={20} axisLine={false} tickLine={false} />
            <YAxis tick={{ fontSize: 12, fill: "#64748b" }} width={72} axisLine={false} tickLine={false} tickFormatter={(value: ChartValue) => String(formatChartValue(value, chart, language, currency))} />
            <Tooltip content={<CustomTooltip language={language} />} />
            <Bar dataKey={chart.y_key} fill="#0f172a" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default function BusinessCharts({ charts = [], language = "en", currency = {} }: BusinessChartsProps) {
  const validCharts = charts.filter((chart) => chart && Array.isArray(chart.data) && chart.data.length > 0 && Boolean(chart.x_key) && Boolean(chart.y_key));

  if (validCharts.length === 0) return null;

  return (
    <section className="space-y-4" dir={language === "ar" ? "rtl" : "ltr"}>
      <div>
        <h2 className="text-xl font-bold text-slate-900">{chartLabels[language].businessCharts}</h2>
        <p className="text-sm text-slate-500">{chartLabels[language].subtitle}</p>
      </div>
      <div className="grid grid-cols-1 gap-5 xl:grid-cols-2">
        {validCharts.map((chart, index) => {
          const key = `${chart.title}-${index}`;
          return chart.type === "bar" ? (
            <BarChartCard key={key} chart={chart} language={language} currency={currency} />
          ) : (
            <LineChartCard key={key} chart={chart} language={language} currency={currency} />
          );
        })}
      </div>
    </section>
  );
}
