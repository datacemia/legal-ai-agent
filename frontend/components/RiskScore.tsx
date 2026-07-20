type RiskScoreTopFactor = {
  factor?: string;
  contribution?: number;
  risk_level?: string;
};

type RiskScoreValue =
  | number
  | {
      value?: number;
      explanation?: string;
      confidence?: string;
      top_factors?: RiskScoreTopFactor[];
    }
  | null
  | undefined;

export default function RiskScore({
  score,
  language = "en",
}: {
  score: RiskScoreValue;
  language?: string;
}) {
  const rawScore = typeof score === "object" && score !== null ? score.value : score;
  const explanation = typeof score === "object" && score !== null ? score.explanation : "";
  const topFactors = typeof score === "object" && score !== null ? score.top_factors || [] : [];
  const safeScore = Math.min(Math.max(Number(rawScore || 0), 0), 100);

  const normalizedLanguage =
    language?.toLowerCase().startsWith("fr")
      ? "fr"
      : language?.toLowerCase().startsWith("ar")
      ? "ar"
      : "en";

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
      methodology: "Why this score?",
      scoreFactors: "Major Contributors",
      scoreFactorsHelp: "Clauses contributing the most to the overall score.",
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
      methodology: "Pourquoi ce score ?",
      scoreFactors: "Principaux contributeurs",
      scoreFactorsHelp: "Clauses ayant le plus contribué au score global.",
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
      methodology: "لماذا هذه الدرجة؟",
      scoreFactors: "أهم العوامل المؤثرة",
      scoreFactorsHelp: "البنود الأكثر تأثيرًا على النتيجة النهائية.",
    },
  };

  const t = labels[normalizedLanguage as keyof typeof labels];
  const label = safeScore >= 70 ? t.high : safeScore >= 40 ? t.medium : t.low;
  const barColor = safeScore >= 70 ? "bg-red-500" : safeScore >= 40 ? "bg-yellow-500" : "bg-green-500";

  return (
    <div dir={normalizedLanguage === "ar" ? "rtl" : "ltr"} className="bg-white p-6 rounded-2xl shadow-sm border">
      <div className="flex items-center justify-between mb-3">
        <div className="text-start">
          <h2 className="text-xl font-semibold text-gray-900">{t.title}</h2>
          <p className="text-sm text-gray-500">{t.subtitle}</p>
        </div>
        <div className="text-end">
          <div className="text-3xl font-bold text-gray-900">{safeScore}/100</div>
          <div className="text-sm text-gray-500">{label}</div>
        </div>
      </div>

      <div className="w-full h-4 bg-gray-100 rounded-full overflow-hidden">
        <div className={`h-full rounded-full transition-all duration-700 ${barColor}`} style={{ width: `${safeScore}%` }} />
      </div>

      <div className="flex justify-between text-xs text-gray-400 mt-2">
        <span>{t.lowShort}</span>
        <span>{t.mediumShort}</span>
        <span>{t.highShort}</span>
      </div>

      {topFactors.length > 0 && (
        <div className="mt-3 space-y-1">
          <div>
            <p className="text-xs font-semibold text-slate-500 uppercase">
              {t.scoreFactors}
            </p>
            <p className="mt-1 text-xs text-slate-500">
              {t.scoreFactorsHelp}
            </p>
          </div>

          {topFactors.map((f, i) => (
            <div
              key={i}
              className="flex items-center justify-between text-sm"
            >
              <span className="text-slate-700">
                {f.factor}
              </span>

              <span className="font-semibold text-red-600">
                +{f.contribution}
              </span>
            </div>
          ))}
        </div>
      )}

      {explanation && (
        <div className="mt-4 rounded-xl border border-slate-200 bg-slate-50 p-3 text-sm text-slate-700">
          <div className="font-semibold text-slate-900">{t.methodology}</div>
          <p className="mt-1 leading-6">{explanation}</p>
        </div>
      )}
    </div>
  );
}
