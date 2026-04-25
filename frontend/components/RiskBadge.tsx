type Props = {
  risk: "low" | "medium" | "high" | string;
};

export default function RiskBadge({ risk }: Props) {
  const colors: Record<string, string> = {
    low: "bg-green-100 text-green-700",
    medium: "bg-yellow-100 text-yellow-800",
    high: "bg-red-100 text-red-700",
  };

  const style = colors[risk] || "bg-gray-100 text-gray-700";

  return (
    <span className={`px-3 py-1 rounded-full text-sm font-semibold ${style}`}>
      {risk?.toUpperCase()}
    </span>
  );
}