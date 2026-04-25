type Props = {
  risk: "low" | "medium" | "high" | string;
  language?: string;
};

export default function RiskBadge({ risk, language = "en" }: Props) {
  const colors: Record<string, string> = {
    low: "bg-green-100 text-green-700",
    medium: "bg-yellow-100 text-yellow-800",
    high: "bg-red-100 text-red-700",
  };

  const style = colors[risk] || "bg-gray-100 text-gray-700";

  // 🔥 traduction des labels
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

  const t = labels[language] || labels.en;

  const display = t[risk] || risk?.toUpperCase();

  return (
    <span className={`px-3 py-1 rounded-full text-sm font-semibold ${style}`}>
      {display}
    </span>
  );
}