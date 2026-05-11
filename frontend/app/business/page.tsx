"use client";

import { useEffect, useState } from "react";
import { analyzeBusinessFile } from "../../lib/api";
import { getSavedLocale, setSavedLocale } from "../../lib/i18n";

const safeGetLocalStorage = (key: string, fallback = "") => {
  if (typeof window === "undefined") return fallback;

  return localStorage.getItem(key) || fallback;
};

const safeSetLocalStorage = (key: string, value: string) => {
  if (typeof window === "undefined") return;

  localStorage.setItem(key, value);
};

export default function BusinessPage() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [language, setLanguage] = useState("en");
  const [plan, setPlan] = useState("");
  const [role, setRole] = useState("");
  const [creditsBalance, setCreditsBalance] = useState(0);

  useEffect(() => {
    setLanguage(getSavedLocale());

    const syncBillingState = () => {
      const savedPlan = safeGetLocalStorage("plan");
      const savedRole = safeGetLocalStorage("role");

      setPlan(savedPlan.toLowerCase().trim());
      setRole(savedRole.toLowerCase().trim());
      setCreditsBalance(Number(safeGetLocalStorage("credits_balance", "0")));
    };

    syncBillingState();

    window.addEventListener("storage", syncBillingState);

    const handleLocaleChange = () => {
      setLanguage(getSavedLocale());
    };

    window.addEventListener("locale-change", handleLocaleChange);

    refreshUserBilling();

    return () => {
      window.removeEventListener("storage", syncBillingState);
      window.removeEventListener("locale-change", handleLocaleChange);
    };
  }, []);

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

    const nextPlan = String(data.plan || "trial")
      .toLowerCase()
      .trim();

    const nextRole = String(data.role || "user")
      .toLowerCase()
      .trim();

    const nextCreditsBalance = Number(data.credits_balance || 0);

    safeSetLocalStorage(
      "credits_balance",
      String(nextCreditsBalance)
    );

    safeSetLocalStorage("plan", nextPlan);
    safeSetLocalStorage("role", nextRole);

    setPlan(nextPlan);
    setRole(nextRole);
    setCreditsBalance(nextCreditsBalance);

    window.dispatchEvent(new Event("storage"));
  };

  const handleAnalyze = async () => {
    if (!file) return;

    setLoading(true);
    setResult(null);
    setMessage("");

    try {
      let data;

      try {
        data = await analyzeBusinessFile(file, language);
      } catch (error: any) {
        const status = error?.response?.status;
        const detail =
          error?.response?.data?.detail ||
          error?.message ||
          "Failed to analyze business file.";

        if (status === 402) {
          setMessage(
            "Your enterprise quota for this AI agent has been exceeded. Please contact your organization administrator."
          );
          return;
        }

        if (status === 403) {
          setMessage(detail || "Access denied");
          return;
        }

        if (status === 429) {
          setMessage("Too many requests. Please try again later.");
          return;
        }

        throw error;
      }

      setResult(data);

      await refreshUserBilling();
    } catch (error: any) {
      const errorMessage = error?.message || "Failed to analyze business file.";

      if (errorMessage.includes("Trial already used")) {
        setMessage(t.trialUsed);
      } else if (errorMessage.includes("$1 trial payment required")) {
        setMessage(t.paymentRequired);
      } else {
        setMessage(errorMessage);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleBuyCredits = () => {
    setMessage(t.paymentMessage);
  };

  const score = Number(result?.business_health_score || 0);

  const labels: any = {
    en: {
      title: "Business Decision Agent",
      subtitle:
        "Upload business CSV data to detect trends, risks, opportunities, and get a clear action plan.",
      howTitle: "How this agent works:",
      how1:
        "Upload a CSV file with your business data such as revenue, expenses, dates, and categories.",
      how2:
        "The agent analyzes your numbers, estimates profit and margin, detects risks, identifies opportunities, and gives practical next steps.",
      disclaimer:
        "Results are for business decision support only. Always verify important decisions with a qualified professional.",
      analyze: "Analyze business data",
      loading: "Analyzing business data...",
      buyCredits: "Buy credits 💳",
      paymentMessage:
        "Stripe is not connected yet. $1 trial activation, credits, and Pro plan will be available soon.",
      proMessage:
        "Pro plan is not configured yet. Stripe will be activated soon.",
      trialInfo: "$1 trial per agent. You can also skip the trial and continue with global credits or a Pro plan.",
      startTrial: "Start $1 trial",
      upgradePro: "Upgrade to Pro",
      trialUsed: "Trial already used for business",
      paymentRequired: "$1 Business trial activation required",
      results: "Results",
      summary: "Summary",
      score: "Business health score",
      excellent: "Excellent",
      excellentDesc:
        "Your business is highly efficient with strong financial control.",
      good: "Good",
      goodDesc: "Your business is healthy but can still be optimized.",
      moderate: "Moderate",
      moderateDesc: "There are inefficiencies or risks that need attention.",
      risky: "Risky",
      riskyDesc:
        "Your business has significant risks and needs urgent improvement.",
      revenue: "Revenue estimate",
      expenses: "Expenses estimate",
      profit: "Profit estimate",
      margin: "Profit margin",
      insights: "Key insights",
      risks: "Risks",
      opportunities: "Opportunities",
      actions: "Action plan",
      noFile: "No file selected",
      chooseFile: "Choose file",
    },
    fr: {
      title: "Agent décision business",
      subtitle:
        "Téléchargez des données business CSV pour détecter les tendances, les risques, les opportunités et obtenir un plan d’action clair.",
      howTitle: "Comment fonctionne cet agent :",
      how1:
        "Téléchargez un fichier CSV avec vos données business comme les revenus, les dépenses, les dates et les catégories.",
      how2:
        "L’agent analyse vos chiffres, estime le profit et la marge, détecte les risques, identifie les opportunités et propose des prochaines étapes pratiques.",
      disclaimer:
        "Les résultats servent uniquement d’aide à la décision business. Vérifiez toujours les décisions importantes avec un professionnel qualifié.",
      analyze: "Analyser les données",
      loading: "Analyse en cours...",
      buyCredits: "Acheter des crédits 💳",
      paymentMessage:
        "Stripe n’est pas encore connecté. L’activation de l’essai à 1$, les crédits et le plan Pro seront bientôt disponibles.",
      proMessage:
        "Le plan Pro n’est pas encore configuré. Stripe sera bientôt activé.",
      trialInfo: "Essai à 1$ par agent. Vous pouvez aussi passer directement aux crédits globaux ou au plan Pro.",
      startTrial: "Activer l’essai à 1$",
      upgradePro: "Passer au plan Pro",
      trialUsed: "Essai Business déjà utilisé",
      paymentRequired: "Activation de l’essai Business à 1$ requise",
      results: "Résultats",
      summary: "Résumé",
      score: "Score de santé business",
      excellent: "Excellent",
      excellentDesc:
        "Votre business est très efficace avec un bon contrôle financier.",
      good: "Bon",
      goodDesc: "Votre business est sain mais peut encore être optimisé.",
      moderate: "Modéré",
      moderateDesc:
        "Il existe des inefficacités ou des risques qui nécessitent votre attention.",
      risky: "Risqué",
      riskyDesc:
        "Votre business présente des risques importants et nécessite une amélioration urgente.",
      revenue: "Revenus estimés",
      expenses: "Dépenses estimées",
      profit: "Profit estimé",
      margin: "Marge bénéficiaire",
      insights: "Points clés",
      risks: "Risques",
      opportunities: "Opportunités",
      actions: "Plan d’action",
      noFile: "Aucun fichier sélectionné",
      chooseFile: "Choisir un fichier",
    },
    ar: {
      title: "وكيل قرارات الأعمال",
      subtitle:
        "ارفع بيانات الأعمال بصيغة CSV لاكتشاف الاتجاهات والمخاطر والفرص والحصول على خطة عمل واضحة.",
      howTitle: "كيف يعمل هذا الوكيل:",
      how1:
        "ارفع ملف CSV يحتوي على بيانات عملك مثل الإيرادات والمصاريف والتواريخ والفئات.",
      how2:
        "يقوم الوكيل بتحليل الأرقام، وتقدير الربح والهامش، واكتشاف المخاطر، وتحديد الفرص، وتقديم خطوات عملية تالية.",
      disclaimer:
        "النتائج مخصصة لدعم قرارات الأعمال فقط. تحقق دائماً من القرارات المهمة مع مختص مؤهل.",
      analyze: "تحليل البيانات",
      loading: "جاري التحليل...",
      buyCredits: "شراء رصيد 💳",
      paymentMessage:
        "Stripe غير متصل حالياً. تفعيل تجربة 1 دولار، الأرصدة وخطة Pro ستكون متاحة قريباً.",
      proMessage:
        "خطة Pro غير مفعلة حالياً. سيتم تفعيل Stripe قريباً.",
      trialInfo: "تجربة بقيمة 1 دولار لكل وكيل. يمكنك أيضاً المتابعة مباشرة بالأرصدة العامة أو خطة Pro.",
      startTrial: "تفعيل تجربة 1 دولار",
      upgradePro: "الترقية إلى Pro",
      trialUsed: "تم استخدام تجربة وكيل الأعمال",
      paymentRequired: "يلزم تفعيل تجربة الأعمال بقيمة 1 دولار",
      results: "النتائج",
      summary: "الملخص",
      score: "مستوى صحة الأعمال",
      excellent: "ممتاز",
      excellentDesc: "عملك فعال جداً ولديه تحكم مالي قوي.",
      good: "جيد",
      goodDesc: "عملك في وضع جيد لكن يمكن تحسينه أكثر.",
      moderate: "متوسط",
      moderateDesc: "هناك أوجه قصور أو مخاطر تحتاج إلى الانتباه.",
      risky: "خطير",
      riskyDesc: "عملك لديه مخاطر كبيرة ويحتاج إلى تحسين عاجل.",
      revenue: "الإيرادات المتوقعة",
      expenses: "المصاريف المتوقعة",
      profit: "الربح المتوقع",
      margin: "هامش الربح",
      insights: "النقاط الرئيسية",
      risks: "المخاطر",
      opportunities: "الفرص",
      actions: "خطة العمل",
      noFile: "لم يتم اختيار ملف",
      chooseFile: "اختيار ملف",
    },
  };

  const t = labels[language] || labels.en;

  const hasActiveAccess =
    role === "admin" ||
    role === "enterprise_admin" ||
    role === "enterprise_member" ||
    ["paid", "pro", "premium"].includes(plan) ||
    creditsBalance > 0;

  const primaryCtaLabel = hasActiveAccess
    ? t.analyze
    : t.startTrial;

  const getScoreMeta = (score: number) => {
    if (score >= 90) {
      return {
        label: t.excellent,
        color: "bg-green-600",
        text: "text-green-700",
        desc: t.excellentDesc,
      };
    }

    if (score >= 70) {
      return {
        label: t.good,
        color: "bg-green-500",
        text: "text-green-600",
        desc: t.goodDesc,
      };
    }

    if (score >= 50) {
      return {
        label: t.moderate,
        color: "bg-yellow-500",
        text: "text-yellow-600",
        desc: t.moderateDesc,
      };
    }

    return {
      label: t.risky,
      color: "bg-red-500",
      text: "text-red-600",
      desc: t.riskyDesc,
    };
  };

  const scoreMeta = getScoreMeta(score);

  return (
    <main
      dir={language === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-4 py-10"
    >
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold">{t.title}</h1>
          <p className="text-slate-500 mt-2">{t.subtitle}</p>
        </div>

        <div className="bg-white p-6 rounded-2xl border space-y-4">
          <div className="rounded-xl bg-slate-50 border border-slate-200 p-4 text-sm text-slate-600 space-y-2">
            <p>
              <strong>{t.howTitle}</strong> {t.how1}
            </p>
            <p>{t.how2}</p>
            <p className="text-xs text-slate-500">{t.disclaimer}</p>
          </div>

          <select
            value={language}
            onChange={(e) => {
              setLanguage(e.target.value);
              setSavedLocale(e.target.value);
              setResult(null);
              setMessage("");
            }}
            className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
          >
            <option value="en">English</option>
            <option value="fr">Français</option>
            <option value="ar">العربية</option>
          </select>

          {/* UPDATED FILE INPUT */}
          <div className="space-y-2">
            <input
              id="file-upload"
              type="file"
              accept=".csv,.xlsx"
              onChange={(e) => {
                setFile(e.target.files?.[0] || null);
                setResult(null);
                setMessage("");
              }}
              className="hidden"
            />

            <label
              htmlFor="file-upload"
              className="flex items-center justify-between cursor-pointer rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm hover:bg-slate-50"
            >
              <span className="text-slate-600">
                {file ? file.name : t.noFile}
              </span>

              <span className="text-blue-600 font-medium">
                {t.chooseFile}
              </span>
            </label>
          </div>

          {!hasActiveAccess && (
            <div className="rounded-xl border border-blue-100 bg-blue-50 p-3 text-sm text-blue-700">
              {t.trialInfo}
            </div>
          )}

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <button
              onClick={handleAnalyze}
              disabled={!file || loading}
              className="w-full bg-slate-900 text-white py-3 rounded-xl disabled:bg-slate-400"
            >
              {loading ? t.loading : primaryCtaLabel}
            </button>

            <button
              onClick={handleBuyCredits}
              className="w-full bg-green-600 text-white py-3 rounded-xl hover:bg-green-700 transition"
            >
              {t.buyCredits}
            </button>

            <button
              onClick={() =>
                setMessage(t.proMessage)
              }
              className="w-full bg-blue-600 text-white py-3 rounded-xl hover:bg-blue-700 transition"
            >
              {t.upgradePro}
            </button>
          </div>

          {message && (
            <p className="text-sm text-red-700 bg-red-50 border border-red-200 rounded-xl px-4 py-3">
              {message}
            </p>
          )}
        </div>

        {result && (
          <div className="bg-white p-6 rounded-2xl border space-y-6">
            <h2 className="text-xl font-semibold">{t.results}</h2>

            {result.error ? (
              <p className="text-red-600">{result.error}</p>
            ) : (
              <>
                <div>
                  <strong>{t.summary}:</strong>
                  <p className="text-slate-600 mt-1">{result.summary}</p>
                </div>

                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <strong>{t.score}:</strong>
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-semibold text-white ${scoreMeta.color}`}
                    >
                      {scoreMeta.label}
                    </span>
                  </div>

                  <div className="text-sm text-slate-600">
                    {score}/100 — {scoreMeta.desc}
                  </div>

                  <div className="h-3 bg-slate-200 rounded-full">
                    <div
                      className={`h-3 rounded-full ${scoreMeta.color}`}
                      style={{
                        width: `${Math.min(Math.max(score, 0), 100)}%`,
                      }}
                    />
                  </div>
                </div>

                <div className="grid gap-4 sm:grid-cols-2">
                  <div className="rounded-xl border bg-slate-50 p-4">
                    <p className="text-sm text-slate-500">{t.revenue}</p>
                    <p className="text-xl font-bold">
                      {result.metrics?.revenue_estimate}
                    </p>
                  </div>

                  <div className="rounded-xl border bg-slate-50 p-4">
                    <p className="text-sm text-slate-500">{t.expenses}</p>
                    <p className="text-xl font-bold">
                      {result.metrics?.expenses_estimate}
                    </p>
                  </div>

                  <div className="rounded-xl border bg-slate-50 p-4">
                    <p className="text-sm text-slate-500">{t.profit}</p>
                    <p className="text-xl font-bold">
                      {result.metrics?.profit_estimate}
                    </p>
                  </div>

                  <div className="rounded-xl border bg-slate-50 p-4">
                    <p className="text-sm text-slate-500">{t.margin}</p>
                    <p className="text-xl font-bold">
                      {result.metrics?.profit_margin_percent}%
                    </p>
                  </div>
                </div>

                <div>
                  <strong>{t.insights}:</strong>
                  <ul className="list-disc ml-6 text-slate-700 mt-2">
                    {(result.key_insights || []).map(
                      (item: string, i: number) => (
                        <li key={i}>{item}</li>
                      )
                    )}
                  </ul>
                </div>

                <div>
                  <strong>{t.risks}:</strong>
                  <ul className="list-disc ml-6 text-red-600 mt-2">
                    {(result.risks || []).map((item: string, i: number) => (
                      <li key={i}>{item}</li>
                    ))}
                  </ul>
                </div>

                <div>
                  <strong>{t.opportunities}:</strong>
                  <ul className="list-disc ml-6 text-green-600 mt-2">
                    {(result.opportunities || []).map(
                      (item: string, i: number) => (
                        <li key={i}>{item}</li>
                      )
                    )}
                  </ul>
                </div>

                <div>
                  <strong>{t.actions}:</strong>
                  <ol className="list-decimal ml-6 text-blue-700 mt-2">
                    {(result.action_plan || []).map(
                      (item: string, i: number) => (
                        <li key={i}>{item}</li>
                      )
                    )}
                  </ol>
                </div>

                {result.disclaimer && (
                  <p className="text-xs text-slate-500 border-t pt-4">
                    {result.disclaimer}
                  </p>
                )}
              </>
            )}
          </div>
        )}
      </div>
    </main>
  );
}