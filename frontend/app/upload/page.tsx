"use client";

import { useEffect, useState } from "react";
import { uploadDocument, runAnalysis } from "../../lib/api";
import { trackEvent } from "../../lib/track";
import { getSavedLocale, setSavedLocale } from "../../lib/i18n";
import RiskBadge from "../../components/RiskBadge";
import RiskScore from "../../components/RiskScore";
import UploadBox from "../../components/UploadBox";


const safeGetLocalStorage = (key: string, fallback = "") => {
  if (typeof window === "undefined") return fallback;

  return localStorage.getItem(key) || fallback;
};

const safeSetLocalStorage = (key: string, value: string) => {
  if (typeof window === "undefined") return;

  localStorage.setItem(key, value);
};

const labels: any = {
  en: {
    pageTitle: "Analyze your contract",
    loading: "Analyzing your contract...",
    loadingSteps: {
      extracting: "Extracting contract text...",
      summary: "Generating summary...",
      clauses: "Analyzing clauses...",
      finalizing: "Finalizing report...",
    },
    elapsed: "Elapsed",
    file: "File",
    signupCta: "$1 trial activation required per agent",
    loginRequired: "Create an account to analyze your contract",
    analyzeButton: "Analyze Contract",
    buyCredit: "Buy credits",
    proMessage:
      "Pro plan is not configured yet. Stripe will be activated soon.",
    trialInfo: "$1 trial per agent. You can also skip the trial and continue with global credits or a Pro plan.",
    upgradePro: "Upgrade to Pro",
    trialUsed: "Trial already used for legal",
    paymentRequired: "$1 Legal trial activation required",
    heroTitle: "AI-powered contract review",
    heroDesc:
      "Get a clear view of contract risks, sensitive clauses, obligations, and practical recommendations before signing.",
    whatYouGet: "Contract intelligence at a glance",
    whatYouGetItems: [
      "Sensitive clause analysis",
      "Obligation and risk assessment",
      "Clear executive summary",
      "Practical recommendations before signing",
    ],
    whatYouGetDescriptions: [
      "Identify clauses that may impact liability, ownership, payment obligations, or termination rights.",
      "Evaluate legal and operational exposure before signing the agreement.",
      "Receive a structured executive summary with practical implications.",
      "Get actionable recommendations and negotiation guidance.",
    ],
    whatYouGetBadges: [
      "Clauses",
      "Risk",
      "Summary",
      "Negotiation",
    ],
    howItWorks: "How it works",
    howItWorksItems: [
      "Upload the contract",
      "Choose the report language",
      "Receive a structured analysis",
    ],
    workflowDescriptions: [
      "Secure PDF, DOCX & scanned document upload",
      "AI-powered contract intelligence",
      "Structured legal analysis in seconds",
    ],
    quality: "Analysis quality",
    qualityScore: "Analysis quality score",
    qualityValid: "Analysis output validated",
    qualityIssues: "Analysis quality issues",
    summary: "Summary",
    simplified: "Simplified Version",
    clauses: "Clauses Analysis",
    clause: "Clause",
    recommendation: "Recommendation",
    negotiationAdvice: "Negotiation Advice",
    saferAlternative: "Safer Alternative",
    negotiationPriority: "Negotiation Priority",
    favours: "Favours",
    legalInsight: "Legal Insight",
    marketComparison: "Market Comparison",
    redFlag: "Red Flag",
    limitedNotice:
      "Trial analysis may be limited. Continue with credits or Pro to unlock full usage.",
    viewDetails: "View details",
    hideDetails: "Hide details",
  },
  fr: {
    pageTitle: "Analyser votre contrat",
    loading: "Analyse de votre contrat en cours...",
    loadingSteps: {
      extracting: "Extraction du texte du contrat...",
      summary: "Génération du résumé...",
      clauses: "Analyse des clauses...",
      finalizing: "Finalisation du rapport...",
    },
    elapsed: "Temps écoulé",
    file: "Fichier",
    signupCta: "Activation de l’essai à 1$ requise par agent",
    loginRequired: "Créez un compte pour analyser votre contrat",
    analyzeButton: "Analyser le contrat",
    buyCredit: "Acheter des crédits",
    proMessage:
      "Le plan Pro n’est pas encore configuré. Stripe sera bientôt activé.",
    trialInfo: "Essai à 1$ par agent. Vous pouvez aussi passer directement aux crédits globaux ou au plan Pro.",
    upgradePro: "Passer au plan Pro",
    trialUsed: "Essai Legal déjà utilisé",
    paymentRequired: "Activation de l’essai Legal à 1$ requise",
    heroTitle: "Analyse contractuelle assistée par IA",
    heroDesc:
      "Obtenez une lecture claire des risques, des clauses sensibles, des obligations et des recommandations pratiques avant signature.",
    whatYouGet: "Informations contractuelles clés",
    whatYouGetItems: [
      "Analyse des clauses sensibles",
      "Évaluation des obligations et des risques",
      "Synthèse exécutive claire",
      "Recommandations pratiques avant signature",
    ],
    whatYouGetDescriptions: [
      "Identifier les clauses pouvant impacter la responsabilité, la propriété, les paiements ou la résiliation.",
      "Évaluer les risques juridiques et opérationnels avant signature.",
      "Recevoir une synthèse structurée avec les implications pratiques.",
      "Obtenir des recommandations concrètes et des conseils de négociation.",
    ],
    whatYouGetBadges: [
      "Clauses",
      "Risques",
      "Résumé",
      "Négociation",
    ],
    howItWorks: "Fonctionnement",
    howItWorksItems: [
      "Importez le contrat",
      "Choisissez la langue du rapport",
      "Recevez une analyse structurée",
    ],
    workflowDescriptions: [
      "Import sécurisé de PDF, DOCX et documents scannés",
      "Analyse intelligente du contrat",
      "Rapport structuré en quelques secondes",
    ],
    quality: "Qualité de l’analyse",
    qualityScore: "Score qualité de l’analyse",
    qualityValid: "Résultat d’analyse validé",
    qualityIssues: "Points qualité détectés",
    summary: "Résumé",
    simplified: "Version simplifiée",
    clauses: "Analyse des clauses",
    clause: "Clause",
    recommendation: "Recommandation",
    negotiationAdvice: "Conseil de négociation",
    saferAlternative: "Alternative plus sûre",
    negotiationPriority: "Priorité de négociation",
    favours: "Favorise",
    legalInsight: "Analyse juridique",
    marketComparison: "Comparaison avec le marché",
    redFlag: "Alerte",
    limitedNotice:
      "L’analyse d’essai peut être limitée. Continuez avec des crédits ou Pro pour débloquer l’usage complet.",
    viewDetails: "Voir les détails",
    hideDetails: "Masquer les détails",
  },
  ar: {
    pageTitle: "تحليل العقد",
    loading: "جاري تحليل العقد...",
    loadingSteps: {
      extracting: "استخراج نص العقد...",
      summary: "إنشاء الملخص...",
      clauses: "تحليل البنود...",
      finalizing: "إنهاء التقرير...",
    },
    elapsed: "الوقت المنقضي",
    file: "الملف",
    signupCta: "يلزم تفعيل تجربة 1 دولار لكل وكيل",
    loginRequired: "أنشئ حساباً لتحليل عقدك",
    analyzeButton: "تحليل العقد",
    buyCredit: "شراء أرصدة",
    proMessage:
      "خطة Pro غير مفعلة حالياً. سيتم تفعيل Stripe قريباً.",
    trialInfo: "تجربة بقيمة 1 دولار لكل وكيل. يمكنك أيضاً المتابعة مباشرة بالأرصدة العامة أو خطة Pro.",
    upgradePro: "الترقية إلى Pro",
    trialUsed: "تم استخدام تجربة الوكيل القانوني",
    paymentRequired: "يلزم تفعيل تجربة القانون بقيمة 1 دولار",
    heroTitle: "تحليل تعاقدي مدعوم بالذكاء الاصطناعي",
    heroDesc:
      "احصل على تقييم واضح للمخاطر والبنود الحساسة والالتزامات والتوصيات العملية قبل التوقيع.",
    whatYouGet: "رؤى تعاقدية فورية",
    whatYouGetItems: [
      "تحليل البنود الحساسة",
      "تقييم الالتزامات والمخاطر",
      "ملخص تنفيذي واضح",
      "توصيات عملية قبل التوقيع",
    ],
    whatYouGetDescriptions: [
      "تحديد البنود التي قد تؤثر على المسؤولية، الملكية، الدفع أو إنهاء العقد.",
      "تقييم المخاطر القانونية والتشغيلية قبل التوقيع.",
      "الحصول على ملخص منظم مع الآثار العملية المهمة.",
      "اقتراح توصيات عملية ونقاط تفاوض واضحة.",
    ],
    whatYouGetBadges: [
      "البنود",
      "المخاطر",
      "الملخص",
      "التفاوض",
    ],
    howItWorks: "آلية العمل",
    howItWorksItems: [
      "ارفع العقد",
      "اختر لغة التقرير",
      "احصل على تحليل منظم",
    ],
    workflowDescriptions: [
      "رفع آمن لملفات PDF و DOCX والمستندات الممسوحة ضوئياً",
      "تحليل ذكي لمحتوى العقد",
      "تقرير منظم خلال ثوانٍ",
    ],
    quality: "جودة التحليل",
    qualityScore: "درجة جودة التحليل",
    qualityValid: "تم التحقق من نتيجة التحليل",
    qualityIssues: "ملاحظات جودة التحليل",
    summary: "الملخص",
    simplified: "نسخة مبسطة",
    clauses: "تحليل البنود",
    clause: "بند",
    recommendation: "توصية",
    negotiationAdvice: "نصيحة تفاوض",
    saferAlternative: "صياغة أكثر أماناً",
    negotiationPriority: "أولوية التفاوض",
    favours: "يميل لصالح",
    legalInsight: "تحليل قانوني",
    marketComparison: "مقارنة بالسوق",
    redFlag: "تنبيه مهم",
    limitedNotice:
      "قد يكون تحليل التجربة محدوداً. تابع باستخدام الأرصدة أو Pro لفتح الاستخدام الكامل.",
    viewDetails: "عرض التفاصيل",
    hideDetails: "إخفاء التفاصيل",
  },
};

const translateEnum = (value: string, language: string) => {
  const normalized = String(value || "").toLowerCase().trim();

  const map: any = {
    en: {
      low: "Low",
      medium: "Medium",
      high: "High",
      balanced: "Balanced",
      employer: "Employer",
      employee: "Employee",
      company: "Company",
      contractor: "Contractor",
      vendor: "Vendor",
      client: "Client",
      unclear: "Unclear",
    },
    fr: {
      low: "Faible",
      medium: "Moyen",
      high: "Élevé",
      balanced: "Équilibré",
      employer: "Employeur",
      employee: "Employé",
      company: "Entreprise",
      contractor: "Contractant",
      vendor: "Fournisseur",
      client: "Client",
      unclear: "Peu clair",
    },
    ar: {
      low: "منخفض",
      medium: "متوسط",
      high: "مرتفع",
      balanced: "متوازن",
      employer: "صاحب العمل",
      employee: "الموظف",
      company: "الشركة",
      contractor: "المتعاقد",
      vendor: "المورّد",
      client: "العميل",
      unclear: "غير واضح",
    },
  };

  return map[language]?.[normalized] || value;
};

const EnterpriseIcon = ({ index }: { index: number }) => {
  const paths = [
    <path key="doc" d="M7 3.75h6.25L18 8.5v11.75H7A2.25 2.25 0 0 1 4.75 18V6A2.25 2.25 0 0 1 7 3.75Zm6 0V8.5h5" />,
    <path key="shield" d="M12 3.75 19.25 6.5v5.25c0 4.25-2.85 7.1-7.25 8.5-4.4-1.4-7.25-4.25-7.25-8.5V6.5L12 3.75Zm-3 8 2 2 4-4" />,
    <path key="chart" d="M4.75 19.25h14.5M7.25 16.25v-5.5M12 16.25v-9.5M16.75 16.25v-3.5" />,
    <path key="briefcase" d="M8.75 7.25V6A2.25 2.25 0 0 1 11 3.75h2A2.25 2.25 0 0 1 15.25 6v1.25M4.75 9.5h14.5v8.25A2.25 2.25 0 0 1 17 20H7a2.25 2.25 0 0 1-2.25-2.25V9.5Zm0 0A2.25 2.25 0 0 1 7 7.25h10a2.25 2.25 0 0 1 2.25 2.25" />,
  ];

  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
      className="h-6 w-6"
      aria-hidden="true"
    >
      {paths[index] || paths[0]}
    </svg>
  );
};

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [fileName, setFileName] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState("");
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [language, setLanguage] = useState("en");
  const [openIndex, setOpenIndex] = useState<number | null>(null);
  const [message, setMessage] = useState("");
  const [plan, setPlan] = useState("");
  const [role, setRole] = useState("");
  const [creditsBalance, setCreditsBalance] = useState(0);

  const hasActiveAccess =
    role === "admin" ||
    role === "enterprise_admin" ||
    role === "enterprise_member" ||
    ["paid", "pro", "premium"].includes(plan) ||
    creditsBalance > 0;

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
    refreshUserBilling();

    window.addEventListener("storage", syncBillingState);

    return () => {
      window.removeEventListener("storage", syncBillingState);
    };
  }, []);

  const t = labels[language] || labels.en;

  useEffect(() => {
    if (!loading) return;

    const timers = [
      setTimeout(() => {
        setLoadingStep(t.loadingSteps.extracting);
        setLoadingProgress(15);
      }, 0),
      setTimeout(() => {
        setLoadingStep(t.loadingSteps.summary);
        setLoadingProgress(40);
      }, 8000),
      setTimeout(() => {
        setLoadingStep(t.loadingSteps.clauses);
        setLoadingProgress(70);
      }, 18000),
      setTimeout(() => {
        setLoadingStep(t.loadingSteps.finalizing);
        setLoadingProgress(90);
      }, 30000),
    ];

    return () => timers.forEach(clearTimeout);
  }, [loading, language]);

  const primaryButtonLabel = hasActiveAccess
    ? t.analyzeButton
    : t.signupCta;

  const getFavoursBadgeClass = (favours: string) => {
    const normalized = String(favours || "").toLowerCase().trim();

    if (
      ["employer", "company", "client", "vendor"].includes(normalized)
    ) {
      return "bg-red-100 text-red-800";
    }

    if (
      ["employee", "contractor"].includes(normalized)
    ) {
      return "bg-blue-100 text-blue-800";
    }

    if (normalized === "balanced") {
      return "bg-green-100 text-green-800";
    }

    return "bg-gray-100 text-gray-700";
  };

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

  const handleBuyCredit = async () => {
    const token = safeGetLocalStorage("token");

    if (!token) {
      window.location.href = "/register";
      return;
    }

    setMessage(
      "Stripe is not configured yet. Credits and Pro plan will be available soon."
    );
  };

  const handleUpload = async () => {
    if (!file) return;

    const token = safeGetLocalStorage("token");

    if (!token) {
      window.location.href = "/register";
      return;
    }

    trackEvent("upload_document");

    try {
      setLoading(true);
      setLoadingStep(t.loadingSteps.extracting);
      setLoadingProgress(15);
      setResult(null);
      setMessage("");
      setOpenIndex(null);

      const doc = await uploadDocument(file);

      if (!doc || !doc.id) {
        throw new Error("Upload failed");
      }

      let analysis;

      try {
        analysis = await runAnalysis(doc.id, language);

        if (analysis?.error === "unsupported_document") {
          setMessage(analysis.message);
          setResult(null);
          setLoading(false);
          return;
        }
      } catch (err: any) {
        const status = err?.response?.status;
        const detail =
          err?.response?.data?.detail ||
          err?.message ||
          "Analysis failed";

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

        throw err;
      }

      if (analysis.detail?.includes("Payment required")) {
        setMessage("You used your free analysis. Please buy one analysis credit.");
        return;
      }

      setResult(analysis);

      await refreshUserBilling();
    } catch (err: any) {
      const detail =
        err?.response?.data?.detail ||
        (err?.message === "Failed to fetch"
          ? "The server completed the request, but the browser could not read the response. Please retry once."
          : err?.message) ||
        "Invalid file. Only PDF or DOCX allowed.";

      if (detail.includes("Trial already used")) {
        setMessage(t.trialUsed);
      } else if (detail.includes("$1 trial payment required")) {
        setMessage(t.paymentRequired);
      } else {
        setMessage(detail);
      }

      return;
    } finally {
      setLoading(false);
      setLoadingStep("");
      setLoadingProgress(0);
    }
  };

  let clauses: any[] = [];
  let isLimited = false;

  try {
    if (result?.clauses && !result?.authRequired) {
      const parsed = Array.isArray(result.clauses)
        ? result.clauses
        : JSON.parse(result.clauses);

      clauses = parsed;
      isLimited = parsed.length === 2;
    }
  } catch (e) {
    console.error("Clause parsing error:", e);
    clauses = [];
  }

  return (
    <main
      dir={language === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-4 py-8 sm:px-6"
    >
      <div className="max-w-5xl mx-auto space-y-8">

        <div className="max-w-3xl mx-auto text-center">
          <h1 className="text-3xl font-semibold tracking-tight text-slate-900 sm:text-4xl">
            {t.heroTitle}
          </h1>

          <p className="mt-4 text-base leading-7 text-slate-600">
            {t.heroDesc}
          </p>
        </div>

        <div className="bg-white p-6 rounded-3xl shadow-sm border space-y-5">
          <UploadBox
            file={file}
            language={language}
            onFileChange={(selected) => {
              setFile(selected);
              setFileName(selected?.name || "");
              setResult(null);
              setMessage("");
              setOpenIndex(null);
            }}
          />

          <select
            value={language}
            onChange={(e) => {
              setLanguage(e.target.value);
              setSavedLocale(e.target.value);
              setResult(null);
            }}
            className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
          >
            <option value="en">English</option>
            <option value="fr">Français</option>
            <option value="ar">العربية</option>
          </select>

          {!hasActiveAccess && (
            <div className="rounded-xl border border-blue-100 bg-blue-50 p-3 text-sm text-blue-700">
              {t.trialInfo}
            </div>
          )}

          <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
            <button
              onClick={handleUpload}
              disabled={!file || loading}
              className="w-full rounded-xl bg-slate-900 px-6 py-3 text-sm font-semibold text-white hover:bg-slate-800 disabled:bg-slate-400"
            >
              {loading ? t.loading : primaryButtonLabel}
            </button>

            <button
              onClick={handleBuyCredit}
              className="w-full rounded-xl bg-green-600 px-6 py-3 text-sm font-semibold text-white hover:bg-green-700"
            >
              {t.buyCredit}
            </button>

            <button
              onClick={() =>
                setMessage(t.proMessage)
              }
              className="w-full rounded-xl bg-blue-600 px-6 py-3 text-sm font-semibold text-white hover:bg-blue-700"
            >
              {t.upgradePro}
            </button>
          </div>

          {message && (
            <div className="bg-red-50 text-red-700 border border-red-200 text-sm p-3 rounded-xl text-center">
              {message}
            </div>
          )}

          {loading && (
            <div className="rounded-2xl border border-blue-100 bg-blue-50 p-4">
              <div className="flex items-center justify-between text-sm">
                <span className="font-medium text-blue-900">
                  {loadingStep || t.loading}
                </span>
                <span className="text-blue-700">
                  {loadingProgress}%
                </span>
              </div>

              <div className="mt-3 h-2 w-full overflow-hidden rounded-full bg-white">
                <div
                  className="h-full rounded-full bg-blue-600 transition-all duration-700"
                  style={{ width: `${loadingProgress}%` }}
                />
              </div>
            </div>
          )}
        </div>

        <section className="relative overflow-hidden rounded-[32px] border border-slate-200 bg-white px-6 py-14 shadow-sm">

          <div className="absolute right-0 top-0 h-72 w-72 bg-blue-100/40 blur-3xl" />
          <div className="absolute left-0 bottom-0 h-72 w-72 bg-indigo-100/30 blur-3xl" />

          <div className="relative z-10">

            <div className="mx-auto max-w-3xl text-center">
              <h2 className="text-4xl font-semibold tracking-tight text-slate-900">
                {t.whatYouGet}
              </h2>

              <p className="mt-4 text-lg leading-8 text-slate-600">
                {t.heroDesc}
              </p>
            </div>

            <div className="mt-14 grid gap-6 md:grid-cols-2 xl:grid-cols-4">

              {t.whatYouGetItems.map((item: string, index: number) => (
                <div
                  key={index}
                  className="group rounded-3xl border border-slate-200 bg-white/90 p-7 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-xl"
                >

                  <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-blue-50 text-blue-700 ring-1 ring-blue-100 transition group-hover:bg-blue-600 group-hover:text-white">
                    <EnterpriseIcon index={index} />
                  </div>

                  <h3 className="mt-6 text-lg font-semibold text-slate-900">
                    {item}
                  </h3>

                  <p className="mt-3 text-sm leading-7 text-slate-600">
                    {t.whatYouGetDescriptions[index]}
                  </p>

                  <div className="mt-6">
                    <span className="inline-flex rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700">
                      {t.whatYouGetBadges[index]}
                    </span>
                  </div>

                </div>
              ))}

            </div>

            <div className="mt-16 rounded-[28px] border border-slate-200 bg-slate-50 px-6 py-10">

              <div className="text-center">
                <h3 className="text-2xl font-semibold text-slate-900">
                  {t.howItWorks}
                </h3>
              </div>

              <div className="mt-10 grid gap-8 md:grid-cols-3">

                {t.howItWorksItems.map((item: string, index: number) => (
                  <div
                    key={index}
                    className="relative text-center"
                  >

                    <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full border border-blue-200 bg-white text-lg font-semibold text-blue-700 shadow-sm">
                      {index + 1}
                    </div>

                    <h4 className="mt-5 text-lg font-semibold text-slate-900">
                      {item}
                    </h4>

                    <div className="mt-3 text-sm text-slate-500">
                      {t.workflowDescriptions[index]}
                    </div>

                  </div>
                ))}

              </div>

            </div>

          </div>

        </section>

        {result && !result.authRequired && (
          <div className="space-y-6">
            {result?.quality_check && (
              <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm mb-6">

                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold">
                    {t.quality}
                  </h3>

                  <span
                    className={`rounded-full px-3 py-1 text-sm font-medium ${
                      result.quality_check.valid
                        ? "bg-green-100 text-green-700"
                        : "bg-yellow-100 text-yellow-700"
                    }`}
                  >
                    {result.quality_check.score}/100
                  </span>
                </div>

                <p className="mt-3 text-sm text-slate-600">
                  {result.quality_check.valid
                    ? t.qualityValid
                    : t.qualityIssues}
                </p>

                {result.quality_check.issues?.length > 0 && (
                  <ul className="mt-3 space-y-2">
                    {result.quality_check.issues.map(
                      (issue: string, index: number) => (
                        <li
                          key={index}
                          className="text-sm text-slate-500"
                        >
                          • {issue}
                        </li>
                      )
                    )}
                  </ul>
                )}
              </div>
            )}

            <div className="bg-white p-6 rounded-3xl border">
              <h2 className="text-xl font-semibold">{t.summary}</h2>
              <div className="mt-4 whitespace-pre-wrap text-sm leading-7 text-slate-700">
                {result.summary}
              </div>
            </div>

            <RiskScore score={result.risk_score} language={language} />

            <div className="rounded-3xl border border-blue-100 bg-gradient-to-br from-blue-50 via-white to-slate-50 p-6 shadow-sm">
              <h2 className="text-xl font-semibold text-slate-900">{t.simplified}</h2>
              <div className="mt-4 whitespace-pre-wrap text-sm leading-8 text-slate-700">
                {result.simplified_version}
              </div>
            </div>

            <div className="bg-white p-6 rounded-3xl border">
              <h2 className="text-xl font-semibold mb-4">{t.clauses}</h2>

              {isLimited && (
                <div className="mb-4 text-sm text-amber-700 bg-amber-50 border border-amber-200 rounded-xl p-3">
                  {t.limitedNotice}
                </div>
              )}

              <div className="space-y-4">
                {clauses.map((clause: any, index: number) => {
                  const isOpen = openIndex === index;

                  return (
                  <div
                    key={index}
                    className={`rounded-3xl border p-5 cursor-pointer transition-all duration-200 ${isOpen ? "border-blue-200 bg-blue-50/20 shadow-sm" : "border-slate-200 bg-white hover:border-blue-100 hover:shadow-sm"}` }
                    onClick={() =>
                      setOpenIndex(openIndex === index ? null : index)
                    }
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <span className="font-semibold text-slate-900">
                          {clause.title || `${t.clause} ${index + 1}`}
                        </span>

                        {clause.clause_reference && (
                          <div className="text-xs text-gray-500 mt-1">
                            {clause.clause_reference}
                          </div>
                        )}
                      </div>

                      <RiskBadge
                        risk={
                          clause.explanation_simple?.includes(
                            "organizational or administrative"
                          )
                            ? "informational"
                            : clause.risk_level
                        }
                        language={language}
                      />
                    </div>

                    {clause.favours && clause.favours !== "balanced" && (
                      <div className="mt-2 text-xs font-medium text-gray-600">
                        {t.favours}:{" "}
                        <span
                          className={`inline-flex rounded-full px-2 py-0.5 text-xs font-semibold capitalize ${getFavoursBadgeClass(
                            clause.favours
                          )}`}
                        >
                          {translateEnum(clause.favours, language)}
                        </span>
                      </div>
                    )}

                    {clause.red_flag && (
                      <div className="mt-4 rounded-xl border border-red-300 bg-red-50 p-4">
                        <div className="font-bold text-red-800">
                          🚨 {t.redFlag}
                        </div>

                        <div className="mt-1 text-sm text-red-700">
                          {clause.red_flag_reason}
                        </div>
                      </div>
                    )}

                    {clause.quoted_text && (
                      clause.detected_language === language ? (
                        <div className="mt-4 rounded-2xl border border-slate-200 bg-slate-50 p-4 italic text-sm leading-7 text-slate-700">
                          “{clause.quoted_text}”
                        </div>
                      ) : (
                        <details className="mt-4 group">
                          <summary className="cursor-pointer list-none inline-flex items-center rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-600 transition hover:border-blue-200 hover:bg-blue-50 hover:text-blue-700">
                            <span>
                              {language === "fr"
                                ? "Voir le texte original"
                                : language === "ar"
                                ? "عرض النص الأصلي"
                                : "View original text"}
                            </span>

                            <svg
                              className="ml-2 h-3.5 w-3.5 transition-transform group-open:rotate-180"
                              viewBox="0 0 20 20"
                              fill="currentColor"
                            >
                              <path
                                fillRule="evenodd"
                                d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z"
                                clipRule="evenodd"
                              />
                            </svg>
                          </summary>

                          <div className="mt-3 rounded-2xl border border-slate-200 bg-slate-50 p-4 italic text-sm leading-7 text-slate-700">
                            “{clause.quoted_text}”
                          </div>
                        </details>
                      )
                    )}

                    <p className="mt-3 text-sm leading-6 text-slate-600">
                      {clause.explanation_simple}
                    </p>

                    <button
                      type="button"
                      className="mt-4 inline-flex items-center rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 transition hover:border-blue-200 hover:bg-blue-50 hover:text-blue-700"
                    >
                      {isOpen ? t.hideDetails : t.viewDetails}
                    </button>

                    {isOpen && (
                    <div className="mt-4 space-y-4 text-sm">

                        {clause.recommendation && (
                          <div>
                            <h4 className="font-semibold text-slate-900">
                              {t.recommendation}
                            </h4>

                            <p className="text-slate-600 mt-1">
                              {clause.recommendation}
                            </p>
                          </div>
                        )}

                        {clause.negotiation_advice && (
                          <div className="bg-amber-50 border border-amber-200 rounded-xl p-3">
                            <h4 className="font-semibold text-amber-900">
                              {t.negotiationAdvice}
                            </h4>

                            <p className="text-amber-800 mt-1">
                              {clause.negotiation_advice}
                            </p>
                          </div>
                        )}

                        {clause.legal_insight && (
                          <div className="mt-4 rounded-xl border border-blue-200 bg-blue-50 p-4">
                            <div className="font-semibold text-blue-900">
                              {t.legalInsight}
                            </div>

                            <div className="mt-1 text-sm text-blue-800">
                              {clause.legal_insight}
                            </div>
                          </div>
                        )}

                        {clause.market_comparison && (
                          <div className="mt-4 rounded-xl border border-purple-200 bg-purple-50 p-4">
                            <div className="font-semibold text-purple-900">
                              {t.marketComparison}
                            </div>

                            <div className="mt-1 text-sm text-purple-800">
                              {clause.market_comparison}
                            </div>
                          </div>
                        )}

                        {clause.safer_alternative && (
                          <div className="bg-green-50 border border-green-200 rounded-xl p-3">
                            <h4 className="font-semibold text-green-900">
                              {t.saferAlternative}
                            </h4>

                            <div className="whitespace-pre-wrap text-green-800 mt-2 text-sm leading-6">
                              {clause.safer_alternative}
                            </div>
                          </div>
                        )}

                        {clause.negotiation_priority &&
                         !(
                           !clause.recommendation &&
                           !clause.negotiation_advice &&
                           !clause.legal_insight &&
                           !clause.market_comparison &&
                           !clause.safer_alternative
                         ) && (
                          <div className="text-xs">
                            <span className="font-semibold">
                              {t.negotiationPriority}:
                            </span>{" "}
                            {translateEnum(clause.negotiation_priority, language)}
                          </div>
                        )}

                      </div>
                    )}
                  </div>
                  );
                })}
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
