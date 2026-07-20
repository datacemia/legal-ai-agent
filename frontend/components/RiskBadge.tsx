type Props = {
  risk: "low" | "medium" | "high" | "critical" | "very_high" | "moderate" | "informational" | string;
  language?: string;
};

const normalizeLanguage = (language?: string) =>
  language?.toLowerCase().startsWith("fr")
    ? "fr"
    : language?.toLowerCase().startsWith("ar")
    ? "ar"
    : "en";

const normalizeRisk = (risk?: string) => {
  const value = String(risk || "").toLowerCase().trim().replace(/\s+/g, "_");
  if (["critical", "very_high"].includes(value)) return "high";
  if (["moderate", "average"].includes(value)) return "medium";
  if (["none", "informational", "info"].includes(value)) return "informational";
  if (["low", "medium", "high"].includes(value)) return value;
  return "unknown";
};

export default function RiskBadge({ risk, language = "en" }: Props) {
  const normalizedLanguage = normalizeLanguage(language);
  const normalizedRisk = normalizeRisk(risk);

  const colors: Record<string, string> = {
    informational: "bg-slate-100 text-slate-700",
    low: "bg-green-100 text-green-700",
    medium: "bg-yellow-100 text-yellow-800",
    high: "bg-red-100 text-red-700",
    unknown: "bg-gray-100 text-gray-700",
  };

  const labels: any = {
    en: { informational: "INFO", low: "LOW", medium: "MEDIUM", high: "HIGH", unknown: "UNKNOWN" },
    fr: { informational: "INFO", low: "FAIBLE", medium: "MOYEN", high: "ÉLEVÉ", unknown: "INCONNU" },
    ar: { informational: "معلوماتي", low: "منخفض", medium: "متوسط", high: "مرتفع", unknown: "غير معروف" },
  };

  const t = labels[normalizedLanguage] || labels.en;

  return (
    <span
      dir={normalizedLanguage === "ar" ? "rtl" : "ltr"}
      className={`px-3 py-1 rounded-full text-sm font-semibold ${colors[normalizedRisk] || colors.unknown}`}
    >
      {t[normalizedRisk] || t.unknown}
    </span>
  );
}