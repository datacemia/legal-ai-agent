type Props = {
  risk: "low" | "medium" | "high" | string;
  language?: string;
};

export default function RiskBadge({ risk, language = "en" }: Props) {
  const normalizedLanguage =
    language?.toLowerCase().startsWith("fr")
      ? "fr"
      : language?.toLowerCase().startsWith("ar")
      ? "ar"
      : "en";

  const normalizedRisk = risk?.toLowerCase();

  if (normalizedRisk === "informational") {
    const informationalLabels: any = {
      en: "Informational",
      fr: "Informatif",
      ar: "معلوماتي",
    };

    return (
      <span
        dir={normalizedLanguage === "ar" ? "rtl" : "ltr"}
        className="px-3 py-1 rounded-full text-sm font-semibold bg-yellow-100 text-yellow-800"
      >
        {informationalLabels[normalizedLanguage] || informationalLabels.en}
      </span>
    );
  }

  const colors: Record<string, string> = {
    low: "bg-green-100 text-green-700",
    medium: "bg-yellow-100 text-yellow-800",
    high: "bg-red-100 text-red-700",
  };

  const style = colors[normalizedRisk] || "bg-gray-100 text-gray-700";

  const labels: any = {
    en: {
      low: "LOW",
      medium: "MEDIUM",
      high: "HIGH",
    },
    fr: {
      low: "FAIBLE",
      medium: "MOYEN",
      high: "ÉLEVÉ",
    },
    ar: {
      low: "منخفض",
      medium: "متوسط",
      high: "مرتفع",
    },
  };

  const t = labels[normalizedLanguage] || labels.en;
  const display = t[normalizedRisk] || normalizedRisk?.toUpperCase();

  return (
    <span
      dir={normalizedLanguage === "ar" ? "rtl" : "ltr"}
      className={`px-3 py-1 rounded-full text-sm font-semibold ${style}`}
    >
      {display}
    </span>
  );
}
