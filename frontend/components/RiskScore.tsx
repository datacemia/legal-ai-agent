export default function RiskScore({
  score,
  language = "en",
}: {
  score: number;
  language?: string;
}) {
  const safeScore = Math.min(Math.max(score || 0, 0), 100);

  // 🔥 labels multilingues
  const labels = {
    en: {
      title: "Risk Score",
      subtitle: "Overall contract risk assessment",
      high: "High Risk",
      medium: "Medium Risk",
      low: "Low Risk",
      lowShort: "Low",
      mediumShort: "Medium",
      highShort: "High",
    },
    fr: {
      title: "Score de risque",
      subtitle: "Évaluation globale du risque du contrat",
      high: "Risque élevé",
      medium: "Risque moyen",
      low: "Risque faible",
      lowShort: "Faible",
      mediumShort: "Moyen",
      highShort: "Élevé",
    },
    ar: {
      title: "درجة المخاطر",
      subtitle: "تقييم المخاطر العام للعقد",
      high: "مخاطر عالية",
      medium: "مخاطر متوسطة",
      low: "مخاطر منخفضة",
      lowShort: "منخفض",
      mediumShort: "متوسط",
      highShort: "مرتفع",
    },
  };

  const t = labels[language as keyof typeof labels] || labels.en;

  const label =
    safeScore >= 70
      ? t.high
      : safeScore >= 40
      ? t.medium
      : t.low;

  const barColor =
    safeScore >= 70
      ? "bg-red-500"
      : safeScore >= 40
      ? "bg-yellow-500"
      : "bg-green-500";

  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border">
      <div className="flex items-center justify-between mb-3">
        <div>
          <h2 className="text-xl font-semibold text-gray-900">
            {t.title}
          </h2>
          <p className="text-sm text-gray-500">
            {t.subtitle}
          </p>
        </div>

        <div className="text-right">
          <div className="text-3xl font-bold text-gray-900">
            {safeScore}/100
          </div>
          <div className="text-sm text-gray-500">{label}</div>
        </div>
      </div>

      <div className="w-full h-4 bg-gray-100 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-700 ${barColor}`}
          style={{ width: `${safeScore}%` }}
        />
      </div>

      <div className="flex justify-between text-xs text-gray-400 mt-2">
        <span>{t.lowShort}</span>
        <span>{t.mediumShort}</span>
        <span>{t.highShort}</span>
      </div>
    </div>
  );
}