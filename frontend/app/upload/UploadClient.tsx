"use client";

import { useEffect, useState } from "react";
import { uploadDocument, runAnalysis } from "../../lib/api";
import { startStripeCheckout } from "../../lib/stripeCheckout";
import { trackEvent } from "../../lib/track";
import { getSavedLocale, setSavedLocale } from "../../lib/i18n";
import RiskBadge from "../../components/RiskBadge";
import RiskScore from "../../components/RiskScore";
import UploadBox from "../../components/UploadBox";
import ExecutiveDashboard from "../../components/ExecutiveDashboard";


const safeGetLocalStorage = (key: string, fallback = "") => {
  if (typeof window === "undefined") return fallback;

  return localStorage.getItem(key) || fallback;
};

const safeSetLocalStorage = (key: string, value: string) => {
  if (typeof window === "undefined") return;

  localStorage.setItem(key, value);
};

const safeRemoveLocalStorage = (key: string) => {
  if (typeof window === "undefined") return;

  localStorage.removeItem(key);
};

const LEGAL_LAST_RESULT_KEY = "legal_last_result";
const LEGAL_LAST_LANGUAGE_KEY = "legal_last_language";

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
    signupCta: "$1 trial activation required per account",
    loginRequired: "Create an account to analyze your contract",
    analyzeButton: "Analyze Contract",
    buyCredit: "Buy credits",
    proMessage:
      "Payments are temporarily unavailable during platform rollout. Pro access will be available soon.",
    trialInfo: "$1 trial per account. You can also skip the trial and continue with global credits or a Pro plan.",
    upgradePro: "Upgrade to Pro",
    trialUsed: "Your $1 trial has already been used on this account. You can continue with credits or a Pro plan.",
    paymentRequired: "$1 Legal trial activation required",
    heroTitle: "AI Legal Intelligence Platform",
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
    heroStats:
      "OCR-ready • Enterprise-grade • Structured legal analysis",
    sampleOutputTitle: "Sample AI analysis",
    sampleOutputSubtitle:
      "Preview the kind of structured legal intelligence Runexa generates.",
    sampleRiskScore: "Risk score preview",
    sampleRiskLevel: "Medium risk",
    sampleClauseTitle: "Sensitive clause detected",
    sampleClauseText:
      "Broad termination rights may create operational uncertainty if notice periods are unclear.",
    sampleAdviceTitle: "Negotiation advice",
    sampleAdviceText:
      "Request clearer notice periods, mutual termination rights, and written cure opportunities.",
    sampleSummaryTitle: "Executive summary",
    sampleSummaryText:
      "Runexa highlights risk exposure, practical obligations, and negotiation priorities before signing.",
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
    signupCta: "Activation de l’essai à 1$ requise par compte",
    loginRequired: "Créez un compte pour analyser votre contrat",
    analyzeButton: "Analyser le contrat",
    buyCredit: "Acheter des crédits",
    proMessage:
      "Les paiements sont temporairement indisponibles pendant le déploiement de la plateforme. L’accès Pro sera bientôt disponible.",
    trialInfo: "Essai à 1$ par compte. Vous pouvez aussi passer directement aux crédits globaux ou au plan Pro.",
    upgradePro: "Passer au plan Pro",
    trialUsed: "Votre essai à 1 $ a déjà été utilisé pour ce compte. Vous pouvez continuer avec des crédits ou un abonnement Pro.",
    paymentRequired: "Activation de l’essai Legal à 1$ requise",
    heroTitle: "Plateforme d’intelligence juridique IA",
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
    heroStats:
      "OCR-ready • Niveau entreprise • Analyse juridique structurée",
    sampleOutputTitle: "Exemple d’analyse IA",
    sampleOutputSubtitle:
      "Aperçu du type d’intelligence juridique structurée générée par Runexa.",
    sampleRiskScore: "Aperçu du score de risque",
    sampleRiskLevel: "Risque moyen",
    sampleClauseTitle: "Clause sensible détectée",
    sampleClauseText:
      "Des droits de résiliation trop larges peuvent créer une incertitude opérationnelle si les délais de préavis sont flous.",
    sampleAdviceTitle: "Conseil de négociation",
    sampleAdviceText:
      "Demandez des délais de préavis plus clairs, des droits réciproques et des possibilités de correction écrites.",
    sampleSummaryTitle: "Résumé exécutif",
    sampleSummaryText:
      "Runexa met en évidence l’exposition au risque, les obligations pratiques et les priorités de négociation avant signature.",
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
    signupCta: "يلزم تفعيل تجربة واحدة بقيمة 1 دولار لكل حساب",
    loginRequired: "أنشئ حساباً لتحليل عقدك",
    analyzeButton: "تحليل العقد",
    buyCredit: "شراء أرصدة",
    proMessage:
      "المدفوعات غير متاحة مؤقتاً أثناء إطلاق المنصة. سيتوفر وصول Pro قريباً.",
    trialInfo: "تجربة واحدة بقيمة 1 دولار لكل حساب. يمكنك أيضاً المتابعة مباشرة بالأرصدة العامة أو خطة Pro.",
    upgradePro: "الترقية إلى Pro",
    trialUsed: "لقد تم استخدام تجربة 1 دولار الخاصة بهذا الحساب بالفعل. يمكنك المتابعة باستخدام الأرصدة أو الاشتراك في خطة Pro.",
    paymentRequired: "يلزم تفعيل تجربة القانون بقيمة 1 دولار",
    heroTitle: "منصة ذكاء قانوني مدعومة بالذكاء الاصطناعي",
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
    heroStats:
      "جاهز للتعرف الضوئي OCR • بمستوى المؤسسات • تحليل قانوني منظم",
    sampleOutputTitle: "مثال على تحليل الذكاء الاصطناعي",
    sampleOutputSubtitle:
      "معاينة لنوع الذكاء القانوني المنظم الذي تولده Runexa.",
    sampleRiskScore: "معاينة درجة المخاطر",
    sampleRiskLevel: "مخاطر متوسطة",
    sampleClauseTitle: "تم اكتشاف بند حساس",
    sampleClauseText:
      "قد تؤدي حقوق الإنهاء الواسعة إلى عدم وضوح تشغيلي إذا كانت فترات الإشعار غير محددة.",
    sampleAdviceTitle: "نصيحة تفاوض",
    sampleAdviceText:
      "اطلب فترات إشعار أوضح، وحقوق إنهاء متبادلة، وفرص تصحيح مكتوبة.",
    sampleSummaryTitle: "ملخص تنفيذي",
    sampleSummaryText:
      "تُبرز Runexa التعرض للمخاطر والالتزامات العملية وأولويات التفاوض قبل التوقيع.",
    viewDetails: "عرض التفاصيل",
    hideDetails: "إخفاء التفاصيل",
  },
};

const JOB_UI_TRANSLATIONS: any = {
  en: {
    job: "Job",
    status: "Status",
    started: "Started",
    completed: "Completed",
    pending: "Pending",
    running: "Running",
    completedStatus: "Completed",
    failed: "Failed",
    remaining: "Remaining",
    estimated: "Estimated",
  },
  fr: {
    job: "Job",
    status: "Statut",
    started: "Début",
    completed: "Fin",
    pending: "En attente",
    running: "En cours",
    completedStatus: "Terminé",
    failed: "Échec",
    remaining: "Restant",
    estimated: "Estimé",
  },
  ar: {
    job: "المهمة",
    status: "الحالة",
    started: "بدأت",
    completed: "اكتملت",
    pending: "قيد الانتظار",
    running: "قيد المعالجة",
    completedStatus: "مكتمل",
    failed: "فشل",
    remaining: "المتبقي",
    estimated: "تقديري",
  },
};

const jobText = (
  key: string,
  language: string,
) => {
  return (
    JOB_UI_TRANSLATIONS?.[language]?.[key] ||
    JOB_UI_TRANSLATIONS?.en?.[key] ||
    key
  );
};

const translateJobStatus = (
  status: string,
  language: string,
) => {
  const normalized = String(status || "").toLowerCase().trim();

  if (normalized === "completed") {
    return jobText("completedStatus", language);
  }

  return jobText(normalized, language);
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



const UI_TRANSLATIONS: any = {
  en: {
    overview: "Overview",
    clauses: "Clauses",
    graphs: "Graphs",
    topRisks: "Top Risks",
    executiveNarrative: "Executive Narrative",
    dependencyGraph: "Dependency Graph",
    legalRelationGraph: "Legal Relation Graph",
    clauseGroups: "Clause Groups",
    structuredDomains: "Structured legal domains",
    noCriticalRisks: "No critical legal risks detected",
    enterpriseGrade: "Enterprise-grade",
    all: "All",
    high: "High",
    medium: "Medium",
    low: "Low",
    documentPreamble: "Document Preamble",
  },
  fr: {
    overview: "Vue d’ensemble",
    clauses: "Clauses",
    graphs: "Graphiques",
    topRisks: "Principaux risques",
    executiveNarrative: "Résumé exécutif",
    dependencyGraph: "Graphe des dépendances",
    legalRelationGraph: "Graphe des relations juridiques",
    clauseGroups: "Groupes de clauses",
    structuredDomains: "Domaines juridiques structurés",
    noCriticalRisks: "Aucun risque juridique critique détecté",
    enterpriseGrade: "Niveau entreprise",
    all: "Tous",
    high: "Élevé",
    medium: "Moyen",
    low: "Faible",
    documentPreamble: "Préambule du contrat",
  },
  ar: {
    overview: "نظرة عامة",
    clauses: "البنود",
    graphs: "الرسوم البيانية",
    topRisks: "أهم المخاطر",
    executiveNarrative: "السرد التنفيذي",
    dependencyGraph: "مخطط التبعيات",
    legalRelationGraph: "مخطط العلاقات القانونية",
    clauseGroups: "مجموعات البنود",
    structuredDomains: "المجالات القانونية المنظمة",
    noCriticalRisks: "لم يتم اكتشاف مخاطر قانونية حرجة",
    enterpriseGrade: "بمستوى المؤسسات",
    all: "الكل",
    high: "مرتفع",
    medium: "متوسط",
    low: "منخفض",
    documentPreamble: "مقدمة العقد",
  },
};

const GROUP_TRANSLATIONS: any = {
  en: {
    other: "Other",
    performance_service_obligations: "Performance & Service Obligations",
    compensation_payment: "Compensation & Payment",
    confidentiality_data: "Confidentiality & Data",
    ip_ownership_license: "IP Ownership & Licensing",
    dispute_jurisdiction_arbitration: "Disputes & Arbitration",
    liability_indemnity_insurance: "Liability, Indemnity & Insurance",
    termination: "Termination",
    confidentiality: "Confidentiality",
  },
  fr: {
    other: "Autres",
    performance_service_obligations: "Obligations de service et de performance",
    compensation_payment: "Rémunération et paiements",
    confidentiality_data: "Confidentialité et données",
    ip_ownership_license: "Propriété intellectuelle et licences",
    dispute_jurisdiction_arbitration: "Litiges et arbitrage",
    liability_indemnity_insurance: "Responsabilité, indemnisation et assurance",
    termination: "Résiliation",
    confidentiality: "Confidentialité",
  },
  ar: {
    other: "أخرى",
    performance_service_obligations: "التزامات الأداء والخدمات",
    compensation_payment: "التعويضات والمدفوعات",
    confidentiality_data: "السرية والبيانات",
    ip_ownership_license: "الملكية الفكرية والتراخيص",
    dispute_jurisdiction_arbitration: "النزاعات والتحكيم",
    liability_indemnity_insurance: "المسؤولية والتعويض والتأمين",
    termination: "إنهاء العقد",
    confidentiality: "السرية",
  },
};

const translateGroupLabel = (
  value: string,
  language: string,
) => {
  return (
    GROUP_TRANSLATIONS?.[language]?.[value] ||
    GROUP_TRANSLATIONS?.en?.[value] ||
    value
  );
};

const uiText = (
  key: string,
  language: string,
) => {
  const fallbackMap: any = {
    enterpriseGrade: {
      en: "Enterprise-grade",
      fr: "Niveau entreprise",
      ar: "بمستوى المؤسسات",
    },
    all: {
      en: "All",
      fr: "Tous",
      ar: "الكل",
    },
    high: {
      en: "High",
      fr: "Élevé",
      ar: "مرتفع",
    },
    medium: {
      en: "Medium",
      fr: "Moyen",
      ar: "متوسط",
    },
    low: {
      en: "Low",
      fr: "Faible",
      ar: "منخفض",
    },
    documentPreamble: {
      en: "Document Preamble",
      fr: "Préambule du contrat",
      ar: "مقدمة العقد",
    },
  };

  return (
    UI_TRANSLATIONS?.[language]?.[key] ||
    fallbackMap?.[key]?.[language] ||
    UI_TRANSLATIONS?.en?.[key] ||
    fallbackMap?.[key]?.en ||
    key
  );
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

export default function UploadClient() {
  const [file, setFile] = useState<File | null>(null);
  const [fileName, setFileName] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState("");
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [language, setLanguage] = useState("en");
  const [openIndex, setOpenIndex] = useState<number | null>(null);
  const [activeTab, setActiveTab] = useState("overview");
  const [riskFilter, setRiskFilter] = useState("medium");
  const [message, setMessage] = useState("");
  const [plan, setPlan] = useState("");
  const [role, setRole] = useState("");
  const [creditsBalance, setCreditsBalance] = useState(0);
  const [legalTrialPaid, setLegalTrialPaid] = useState(false);
  const [legalTrialUsed, setLegalTrialUsed] = useState(false);
  const [analysisStartedAt, setAnalysisStartedAt] = useState<number | null>(null);
  const [elapsedSeconds, setElapsedSeconds] = useState(0);
  const [jobId, setJobId] = useState<number | null>(null);
  const [jobStatus, setJobStatus] = useState("");
  const [jobStartedAt, setJobStartedAt] = useState("");
  const [jobCompletedAt, setJobCompletedAt] = useState("");

  const hasPaidLegalTrial = legalTrialPaid && !legalTrialUsed;
  const hasUsedLegalTrial = legalTrialPaid && legalTrialUsed;

  const hasAccountAccess =
    role === "admin" ||
    role === "enterprise_admin" ||
    role === "enterprise_member" ||
    ["paid", "pro", "premium"].includes(plan) ||
    creditsBalance > 0;

  const hasActiveAccess = hasAccountAccess || hasPaidLegalTrial;

  const legalTrialActivatedMessage =
    language === "fr"
      ? "Essai Legal activé. Importez votre contrat et cliquez sur Analyser le contrat."
      : language === "ar"
      ? "تم تفعيل تجربة الوكيل القانوني. ارفع العقد ثم اضغط على تحليل العقد."
      : "Legal trial activated. Upload your contract and click Analyze Contract.";

  useEffect(() => {
    const savedLocale = getSavedLocale();

    setLanguage(savedLocale);

    const savedResult = safeGetLocalStorage(LEGAL_LAST_RESULT_KEY);
    const savedResultLanguage = safeGetLocalStorage(LEGAL_LAST_LANGUAGE_KEY);

    if (savedResult) {
      try {
        setResult(JSON.parse(savedResult));

        if (savedResultLanguage) {
          setLanguage(savedResultLanguage);
        }
      } catch {
        safeRemoveLocalStorage(LEGAL_LAST_RESULT_KEY);
        safeRemoveLocalStorage(LEGAL_LAST_LANGUAGE_KEY);
      }
    }

    const syncBillingState = () => {
      const savedPlan = safeGetLocalStorage("plan");
      const savedRole = safeGetLocalStorage("role");

      setPlan(savedPlan.toLowerCase().trim());
      setRole(savedRole.toLowerCase().trim());
      setCreditsBalance(Number(safeGetLocalStorage("credits_balance", "0")));
    };

    syncBillingState();
    refreshUserBilling();
    refreshLegalTrial();

    window.addEventListener("storage", syncBillingState);

    return () => {
      window.removeEventListener("storage", syncBillingState);
    };
  }, []);

  const t = labels[language] || labels.en;

  useEffect(() => {
    if (!loading || !analysisStartedAt) return;

    const interval = window.setInterval(() => {
      setElapsedSeconds(
        Math.max(
          0,
          Math.floor((Date.now() - analysisStartedAt) / 1000)
        )
      );
    }, 1000);

    return () => window.clearInterval(interval);
  }, [loading, analysisStartedAt]);

  const primaryButtonLabel = hasActiveAccess
    ? t.analyzeButton
    : hasUsedLegalTrial
      ? t.trialUsed
      : t.signupCta;

  const loadingTimeline = [
    {
      key: "extracting",
      label: t.loadingSteps.extracting,
      threshold: 15,
    },
    {
      key: "summary",
      label: t.loadingSteps.summary,
      threshold: 40,
    },
    {
      key: "clauses",
      label: t.loadingSteps.clauses,
      threshold: 70,
    },
    {
      key: "finalizing",
      label: t.loadingSteps.finalizing,
      threshold: 90,
    },
  ];

  const liveMetrics = [
    {
      label:
        language === "fr"
          ? "Texte sécurisé"
          : language === "ar"
          ? "النص مؤمّن"
          : "Secure text",
      value:
        loadingProgress >= 15
          ? language === "fr"
            ? "OK"
            : language === "ar"
            ? "تم"
            : "OK"
          : "—",
    },
    {
      label:
        language === "fr"
          ? "Résumé exécutif"
          : language === "ar"
          ? "الملخص التنفيذي"
          : "Executive summary",
      value:
        loadingProgress >= 40
          ? language === "fr"
            ? "En préparation"
            : language === "ar"
            ? "قيد التحضير"
            : "Preparing"
          : "—",
    },
    {
      label:
        language === "fr"
          ? "Analyse des clauses"
          : language === "ar"
          ? "تحليل البنود"
          : "Clause analysis",
      value:
        loadingProgress >= 70
          ? language === "fr"
            ? "Avancé"
            : language === "ar"
            ? "متقدم"
            : "Advanced"
          : loadingProgress >= 50
          ? language === "fr"
            ? "En cours"
            : language === "ar"
            ? "قيد المعالجة"
            : "In progress"
          : "—",
    },
  ];

  const formatElapsed = (seconds: number) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;

    return `${minutes}:${String(remainingSeconds).padStart(2, "0")}`;
  };

  const parseBackendDate = (value: string) => {
    if (!value) return null;

    const normalized = /Z$|[+-]\d{2}:\d{2}$/.test(value)
      ? value
      : `${value}Z`;

    const parsed = new Date(normalized);

    if (Number.isNaN(parsed.getTime())) {
      return null;
    }

    return parsed;
  };

  const formatJobDateTime = (value: string) => {
    const parsed = parseBackendDate(value);

    if (!parsed) return "—";

    return parsed.toLocaleTimeString();
  };

  const getRealJobElapsed = () => {
    const startedDate = parseBackendDate(jobStartedAt);

    if (!startedDate) {
      return formatElapsed(elapsedSeconds);
    }

    const completedDate = parseBackendDate(jobCompletedAt);

    const ended = completedDate
      ? completedDate.getTime()
      : Date.now();

    return formatElapsed(
      Math.max(
        0,
        Math.floor((ended - startedDate.getTime()) / 1000)
      )
    );
  };

  const getEstimatedRemaining = () => {
    const startedDate = parseBackendDate(jobStartedAt);

    if (
      !startedDate ||
      loadingProgress < 70 ||
      loadingProgress >= 100 ||
      jobStatus === "completed" ||
      jobStatus === "failed"
    ) {
      return null;
    }

    const elapsed = Math.max(
      0,
      Math.floor(
        (Date.now() - startedDate.getTime()) / 1000
      )
    );

    if (elapsed < 15) {
      return null;
    }

    const estimatedTotal = Math.floor(
      elapsed / (loadingProgress / 100)
    );

    const remaining = Math.max(
      0,
      estimatedTotal - elapsed
    );

    return formatElapsed(remaining);
  };

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

  const refreshLegalTrial = async () => {
    const token = safeGetLocalStorage("token");

    if (!token) return;

    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/payments/trial-status/legal`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!res.ok) return;

      const data = await res.json();

      setLegalTrialPaid(Boolean(data.trial_paid));
      setLegalTrialUsed(Boolean(data.trial_used));
    } catch (error) {
      console.error("Could not refresh legal trial status:", error);
    }
  };

  const handleBuyCredit = async () => {
    try {
      await startStripeCheckout("credits_pack", {
        pack: "starter",
      });
    } catch (error: any) {
      setMessage(error?.message || "Unable to start checkout.");
    }
  };

  const handleUpgradePro = async () => {
    try {
      await startStripeCheckout("subscription");
    } catch (error: any) {
      setMessage(error?.message || "Unable to start checkout.");
    }
  };

  const handlePrimaryAction = async () => {
    if (hasActiveAccess) {
      await handleUpload();
      return;
    }

    if (hasUsedLegalTrial) {
      setMessage(t.trialUsed);
      return;
    }

    try {
      await startStripeCheckout("trial", {
        agent_slug: "legal",
      });
    } catch (error: any) {
      setMessage(error?.message || "Unable to start checkout.");
    }
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
      setAnalysisStartedAt(Date.now());
      setElapsedSeconds(0);
      setLoading(true);
      setLoadingStep(t.loadingSteps.extracting);
      setLoadingProgress(0);
      setJobId(null);
      setJobStatus("");
      setJobStartedAt("");
      setJobCompletedAt("");
      setResult(null);
      setMessage("");
      setOpenIndex(null);
      setActiveTab("overview");
      setRiskFilter("all");

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

        if (analysis?.job_id) {
          const token = safeGetLocalStorage("token");
          const jobId = analysis.job_id;

          setJobId(jobId);
          setJobStatus(analysis.status || "pending");
          setLoadingStep(
            analysis.status_message || t.loadingSteps.extracting
          );
          setLoadingProgress(
            typeof analysis.progress === "number"
              ? analysis.progress
              : 0
          );

          let attempts = 0;
          let completed = false;

          while (attempts < 120 && !completed) {
            await new Promise((resolve) =>
              setTimeout(resolve, 2000)
            );

            const statusRes = await fetch(
              `${process.env.NEXT_PUBLIC_API_URL}/jobs/${jobId}`,
              {
                headers: {
                  Authorization: `Bearer ${token}`,
                },
              }
            );

            if (!statusRes.ok) {
              throw new Error(
                "Could not check legal analysis status"
              );
            }

            const statusData = await statusRes.json();

            setJobId(statusData.id || jobId);
            setJobStatus(statusData.status || "");

            if (statusData.started_at) {
              setJobStartedAt(statusData.started_at);
            }

            if (statusData.completed_at) {
              setJobCompletedAt(statusData.completed_at);
            }

            if (
              typeof statusData.progress === "number"
            ) {
              setLoadingProgress(statusData.progress);
            }

            if (statusData.status_message) {
              setLoadingStep(
                statusData.status_message
              );
            }

            if (
              statusData.status === "completed"
            ) {
              analysis = statusData.result;
              completed = true;
              break;
            }

            if (
              statusData.status === "failed"
            ) {
              throw new Error(
                statusData.error ||
                  "Legal analysis failed"
              );
            }

            attempts++;
          }

          if (!completed) {
            throw new Error(
              "Legal analysis timeout"
            );
          }
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

      safeSetLocalStorage(
        LEGAL_LAST_RESULT_KEY,
        JSON.stringify(analysis)
      );

      safeSetLocalStorage(
        LEGAL_LAST_LANGUAGE_KEY,
        language
      );

      await refreshUserBilling();
      await refreshLegalTrial();
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
      setAnalysisStartedAt(null);
    }
  };

  let clauses: any[] = [];
  let isLimited = false;

  try {
    if (result?.clauses && !result?.authRequired) {
      if (Array.isArray(result.clauses)) {
        clauses = result.clauses;
      } else if (Array.isArray(result.clauses?.results)) {
        clauses = result.clauses.results;
      } else if (Array.isArray(result.clauses?.clauses?.results)) {
        clauses = result.clauses.clauses.results;
      } else if (typeof result.clauses === "string") {
        const parsed = JSON.parse(result.clauses);

        if (Array.isArray(parsed)) {
          clauses = parsed;
        } else if (Array.isArray(parsed?.results)) {
          clauses = parsed.results;
        }
      }

      isLimited = clauses.length === 2;
    }
  } catch (e) {
    console.error("Clause parsing error:", e);
    clauses = [];
  }

  return (
    <main
      dir={language === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-4 py-12 sm:px-6 sm:py-16"
    >
      <div className="max-w-5xl mx-auto space-y-8">

        <div className="max-w-3xl mx-auto text-center">
          <h1 className="text-3xl font-semibold tracking-tight text-slate-900 sm:text-4xl">
            {t.heroTitle}
          </h1>

          <p className="mt-4 text-base leading-7 text-slate-600">
            {t.heroDesc}
          </p>

          <div className="mt-5 flex flex-wrap items-center justify-center gap-3 text-sm font-medium text-slate-500">
            {t.heroStats}
          </div>
        </div>

        <div className="bg-gradient-to-b from-white to-slate-50/80 p-6 rounded-3xl shadow-sm border space-y-5 transition-all duration-300 hover:border-blue-200 hover:shadow-xl">
          <UploadBox
            file={file}
            language={language}
            onFileChange={(selected) => {
              setFile(selected);
              setFileName(selected?.name || "");
              setResult(null);
              safeRemoveLocalStorage(LEGAL_LAST_RESULT_KEY);
              safeRemoveLocalStorage(LEGAL_LAST_LANGUAGE_KEY);
              setMessage("");
              setOpenIndex(null);
              setActiveTab("overview");
              setRiskFilter("all");
            }}
          />

          <select
            value={language}
            onChange={(e) => {
              setLanguage(e.target.value);
              setSavedLocale(e.target.value);
              setResult(null);
              safeRemoveLocalStorage(LEGAL_LAST_RESULT_KEY);
              safeRemoveLocalStorage(LEGAL_LAST_LANGUAGE_KEY);
            }}
            className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
          >
            <option value="en">English</option>
            <option value="fr">Français</option>
            <option value="ar">العربية</option>
          </select>

          {!hasActiveAccess && !hasUsedLegalTrial && (
            <div className="rounded-xl border border-blue-100 bg-blue-50 p-3 text-sm text-blue-700">
              {t.trialInfo}
            </div>
          )}

          {hasPaidLegalTrial && !hasAccountAccess && (
            <div className="rounded-xl border border-green-100 bg-green-50 p-3 text-sm text-green-700">
              {legalTrialActivatedMessage}
            </div>
          )}

          {hasUsedLegalTrial && !hasAccountAccess && (
            <div className="rounded-xl border border-amber-200 bg-amber-50 p-3 text-sm text-amber-700">
              {t.trialUsed}
            </div>
          )}

          <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
            <button
              onClick={handlePrimaryAction}
              disabled={hasActiveAccess ? !file || loading : loading || hasUsedLegalTrial}
              className="w-full rounded-xl bg-slate-900 px-6 py-3 text-sm font-semibold text-white transition-all duration-300 hover:bg-slate-800 hover:shadow-xl disabled:bg-slate-400 disabled:hover:shadow-none"
            >
              {loading ? t.loading : primaryButtonLabel}
            </button>

            <button
              onClick={handleBuyCredit}
              className="w-full rounded-xl border border-slate-300 bg-white px-6 py-3 text-sm font-semibold text-slate-800 transition-all duration-300 hover:border-blue-200 hover:bg-slate-50 hover:shadow-md"
            >
              {t.buyCredit}
            </button>

            <button
              onClick={handleUpgradePro}
              className="w-full rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-3 text-sm font-semibold text-white transition-all duration-300 hover:shadow-xl"
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
              <div className="flex items-center justify-between gap-4 text-sm">
                <span className="font-medium text-blue-900">
                  {loadingStep || t.loading}
                </span>

                <div className="flex flex-wrap items-center gap-3 text-blue-700">
                  <span>
                    {t.elapsed}: {getRealJobElapsed()}
                  </span>

                  {getEstimatedRemaining() && (
                    <span>
                      {jobText("remaining", language)}: {getEstimatedRemaining()}
                    </span>
                  )}

                  <span>
                    {loadingProgress}%
                  </span>
                </div>
              </div>

              <div className="mt-3 h-2 w-full overflow-hidden rounded-full bg-white">
                <div
                  className="h-full rounded-full bg-blue-600 transition-all duration-700"
                  style={{ width: `${loadingProgress}%` }}
                />
              </div>

              {(jobId || jobStatus || jobStartedAt || jobCompletedAt) && (
                <div className="mt-4 grid gap-3 sm:grid-cols-4">
                  <div className="rounded-xl border border-blue-100 bg-white p-3">
                    <div className="text-xs text-slate-500">
                      {jobText("job", language)}
                    </div>
                    <div className="mt-1 text-sm font-semibold text-slate-900">
                      {jobId ? `#${jobId}` : "—"}
                    </div>
                  </div>

                  <div className="rounded-xl border border-blue-100 bg-white p-3">
                    <div className="text-xs text-slate-500">
                      {jobText("status", language)}
                    </div>
                    <div className="mt-1 text-sm font-semibold text-slate-900">
                      {jobStatus
                        ? translateJobStatus(jobStatus, language)
                        : "—"}
                    </div>
                  </div>

                  <div className="rounded-xl border border-blue-100 bg-white p-3">
                    <div className="text-xs text-slate-500">
                      {jobText("started", language)}
                    </div>
                    <div className="mt-1 text-sm font-semibold text-slate-900">
                      {formatJobDateTime(jobStartedAt)}
                    </div>
                  </div>

                  <div className="rounded-xl border border-blue-100 bg-white p-3">
                    <div className="text-xs text-slate-500">
                      {jobText("completed", language)}
                    </div>
                    <div className="mt-1 text-sm font-semibold text-slate-900">
                      {formatJobDateTime(jobCompletedAt)}
                    </div>
                  </div>
                </div>
              )}

              <div className="mt-5 grid gap-3 md:grid-cols-4">
                {loadingTimeline.map((step, index) => {
                  const completed = loadingProgress >= step.threshold;
                  const active =
                    !completed &&
                    loadingProgress >=
                      (loadingTimeline[index - 1]?.threshold || 0);

                  return (
                    <div
                      key={step.key}
                      className={`rounded-xl border p-3 text-xs ${
                        completed
                          ? "border-green-200 bg-green-50 text-green-800"
                          : active
                          ? "border-blue-200 bg-white text-blue-800"
                          : "border-slate-200 bg-white/70 text-slate-500"
                      }`}
                    >
                      <div className="font-semibold">
                        {completed ? "✓" : active ? "⏳" : "○"} {step.label}
                      </div>
                    </div>
                  );
                })}
              </div>

              <div className="mt-4 grid gap-3 sm:grid-cols-3">
                {liveMetrics.map((metric) => (
                  <div
                    key={metric.label}
                    className="rounded-xl border border-blue-100 bg-white p-3 transition-all duration-300 hover:border-blue-200 hover:shadow-md"
                  >
                    <div className="text-xs text-slate-500">
                      {metric.label}
                    </div>
                    <div className="mt-1 text-sm font-semibold text-slate-900">
                      {metric.value}
                    </div>
                  </div>
                ))}
              </div>

              <div className="mt-5 space-y-3">
                {[0, 1, 2].map((item) => (
                  <div
                    key={item}
                    className="animate-pulse rounded-2xl border border-blue-100 bg-white p-4"
                  >
                    <div className="h-3 w-1/3 rounded-full bg-slate-200" />
                    <div className="mt-3 h-3 w-full rounded-full bg-slate-100" />
                    <div className="mt-2 h-3 w-2/3 rounded-full bg-slate-100" />
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-xl">
          <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <p className="text-sm font-medium text-blue-600">
                {t.sampleOutputTitle}
              </p>

              <h2 className="mt-1 text-xl font-semibold text-slate-900">
                {t.whatYouGet}
              </h2>

              <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500">
                {t.sampleOutputSubtitle}
              </p>
            </div>

            <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700">
              {uiText("enterpriseGrade", language)}
            </span>
          </div>

          <div className="mt-6 grid gap-4 lg:grid-cols-3">
            <div className="rounded-2xl border border-slate-200 bg-gradient-to-br from-slate-50 to-white p-5">
              <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
                {t.sampleRiskScore}
              </p>

              <div className="mt-4 flex items-end gap-2">
                <span className="text-4xl font-bold text-amber-600">62</span>
                <span className="mb-1 text-sm text-slate-500">/100</span>
              </div>

              <p className="mt-2 text-sm font-semibold text-amber-700">
                {t.sampleRiskLevel}
              </p>

              <div className="mt-4 rounded-xl bg-amber-50 p-3 text-xs leading-5 text-amber-800">
                {t.sampleSummaryText}
              </div>
            </div>

            <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5 lg:col-span-1">
              <p className="text-sm font-bold text-amber-900">
                {t.sampleClauseTitle}
              </p>

              <div className="mt-4 rounded-xl border-l-4 border-amber-500 bg-white p-4 text-sm leading-7 text-slate-700">
                “{t.sampleClauseText}”
              </div>

              <p className="mt-4 text-xs font-semibold uppercase tracking-wide text-amber-700">
                {language === "fr"
                  ? "Signal de risque"
                  : language === "ar"
                  ? "إشارة مخاطر"
                  : "Risk signal"}
              </p>
            </div>

            <div className="rounded-2xl border border-blue-200 bg-blue-50 p-5">
              <p className="text-sm font-bold text-blue-900">
                {t.sampleAdviceTitle}
              </p>

              <p className="mt-3 text-sm leading-6 text-blue-800">
                {t.sampleAdviceText}
              </p>

              <div className="mt-4 rounded-xl border border-green-200 bg-green-50 p-3">
                <p className="text-xs font-semibold text-green-800">
                  {language === "fr"
                    ? "Extraction des obligations"
                    : language === "ar"
                    ? "استخراج الالتزامات"
                    : "Obligation extraction"}
                </p>

                <p className="mt-1 text-xs leading-5 text-green-700">
                  {language === "fr"
                    ? "Période de préavis, droits de résiliation, possibilité de correction et exigences d’approbation écrite."
                    : language === "ar"
                    ? "فترة الإشعار، حقوق الإنهاء، إمكانية المعالجة، ومتطلبات الموافقة الكتابية."
                    : "Notice period, termination rights, cure opportunity, and written approval requirements."}
                </p>
              </div>
            </div>
          </div>
        </div>

        {result && !result.authRequired && (
          <div className="space-y-6">
            {result?.quality_check && (
              <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm mb-6">

                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold">
                    {t.quality}
                  </h3>

                  <div className="flex items-center">
                    <span
                      className={`rounded-full px-3 py-1 text-sm font-medium ${
                        result.quality_check.valid
                          ? "bg-green-100 text-green-700"
                          : "bg-yellow-100 text-yellow-700"
                      }`}
                    >
                      {result.quality_check.score}/100
                    </span>

                    {result.quality_check.score >= 90 && (
                      <span className="ml-2 rounded-full bg-green-100 px-2 py-1 text-xs text-green-700">
                        {uiText("enterpriseGrade", language)}
                      </span>
                    )}
                  </div>
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

            <RiskScore score={result.risk_score} language={language} />

            <div className="flex flex-wrap gap-2 mb-6">
              {[
                ["overview", uiText("overview", language)],
                ["clauses", `${uiText("clauses", language)} (${clauses.length})`],
                ["graphs", uiText("graphs", language)],
              ].map(([key, label]) => (
                <button
                  key={key}
                  onClick={() => setActiveTab(key)}
                  className={`rounded-full px-4 py-2 text-sm font-medium transition ${
                    activeTab === key
                      ? "bg-blue-600 text-white shadow-sm"
                      : "bg-white border text-slate-700 hover:bg-slate-50"
                  }`}
                >
                  {label}
                </button>
              ))}
            </div>
            {activeTab === "overview" && (
              <>
                <ExecutiveDashboard
                  result={result}
                  language={language}
                  showGraphs={false}
                />

                <div className="rounded-3xl border border-blue-100 bg-gradient-to-br from-blue-50 via-white to-slate-50 p-6 shadow-sm">
                  <h2 className="text-xl font-semibold text-slate-900">{t.simplified}</h2>
                  <div className="mt-4 whitespace-pre-wrap text-sm leading-8 text-slate-700">
                    {result.simplified_version}
                  </div>
                </div>

                <div className="bg-white p-6 rounded-3xl border shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-xl">
                  <h2 className="text-xl font-semibold">{t.summary}</h2>
                  <div className="mt-4 whitespace-pre-wrap text-sm leading-7 text-slate-700">
                    {result.summary}
                  </div>
                </div>
              </>
            )}

            {activeTab === "graphs" && (
              <ExecutiveDashboard
                result={result}
                language={language}
                showGraphs={true}
              />
            )}


            {activeTab === "clauses" && (
              <div className="bg-white p-6 rounded-3xl border shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-xl">
              <h2 className="text-xl font-semibold mb-4">{t.clauses}</h2>

              {isLimited && (
                <div className="mb-4 text-sm text-amber-700 bg-amber-50 border border-amber-200 rounded-xl p-3">
                  {t.limitedNotice}
                </div>
              )}

              <div className="flex gap-2 mb-5">
                {["all", "high", "medium", "low"].map((level) => (
                  <button
                    key={level}
                    onClick={() => setRiskFilter(level)}
                    className={`rounded-full px-3 py-1 text-sm ${
                      riskFilter === level
                        ? "bg-blue-600 text-white shadow-sm"
                        : "bg-slate-100"
                    }`}
                  >
                    {level === "all"
                      ? uiText("all", language)
                      : level === "high"
                      ? translateEnum("high", language)
                      : level === "medium"
                      ? translateEnum("medium", language)
                      : translateEnum("low", language)}
                  </button>
                ))}
              </div>

              <div className="space-y-4">
                {clauses
                  .filter((clause: any) => {
                    if (riskFilter === "all") return true;

                    return (
                      String(clause.risk_level).toLowerCase() === riskFilter
                    );
                  })
                  .map((clause: any, index: number) => {
                  const isOpen = openIndex === index;
                  const localizedTitle =
                    clause.title === "Document Preamble"
                      ? uiText("documentPreamble", language)
                      : clause.title;

                  return (
                  <div
                    key={index}
                    className={`rounded-3xl border p-5 transition-all duration-200 ${isOpen ? "border-blue-200 bg-blue-50/20 shadow-sm" : "border-slate-200 bg-white hover:border-blue-100 hover:shadow-sm"}` }
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <span className="font-semibold text-slate-900">
                          {localizedTitle || `${t.clause} ${index + 1}`}
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

                    <p className="mt-3 line-clamp-4 text-[13px] leading-6 text-slate-600">
                      {clause.explanation_simple}
                    </p>

                    {clause.has_details && (
                      <button
                        type="button"
                        onClick={() =>
                          setOpenIndex(openIndex === index ? null : index)
                        }
                        className="mt-4 inline-flex items-center rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 transition hover:border-blue-200 hover:bg-blue-50 hover:text-blue-700"
                      >
                        {isOpen ? t.hideDetails : t.viewDetails}
                      </button>
                    )}

                    {isOpen && clause.has_details && (
                    <div className="mt-4 space-y-4 text-sm">

                        {clause.recommendation &&
                         !clause.recommendation.includes("Confirm that the clause is consistent") && (
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

                        {clause.legal_insight &&
                         !clause.legal_insight.includes("No significant legal imbalance detected") &&
                         !clause.legal_insight.includes("This clause creates contractual obligations") && (
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

                            <div className="whitespace-pre-wrap text-green-800 mt-2 text-[13px] leading-6">
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
            )}
          </div>
        )}
      </div>
    </main>
  );
}
