export default function RiskScore({ score }: { score: number }) {
  const safeScore = Math.min(Math.max(score || 0, 0), 100);

  const label =
    safeScore >= 70 ? "High Risk" : safeScore >= 40 ? "Medium Risk" : "Low Risk";

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
          <h2 className="text-xl font-semibold text-gray-900">Risk Score</h2>
          <p className="text-sm text-gray-500">
            Overall contract risk assessment
          </p>
        </div>

        <div className="text-right">
          <div className="text-3xl font-bold text-gray-900">{safeScore}/100</div>
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
        <span>Low</span>
        <span>Medium</span>
        <span>High</span>
      </div>
    </div>
  );
}