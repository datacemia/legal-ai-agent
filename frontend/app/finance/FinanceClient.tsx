"use client";

import { useEffect, useState } from "react";
import jsPDF from "jspdf";
import ReactMarkdown from "react-markdown";
import { analyzeFinanceStatement } from "../../lib/api";
import { getSavedLocale, setSavedLocale } from "../../lib/i18n";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  AreaChart,
  Area,
  BarChart,
  Bar,
} from "recharts";

const safeGetLocalStorage = (key: string, fallback = "") => {
  if (typeof window === "undefined") return fallback;

  return localStorage.getItem(key) || fallback;
};

const safeSetLocalStorage = (key: string, value: string) => {
  if (typeof window === "undefined") return;

  localStorage.setItem(key, value);
};


const trendLabels: any = {
  en: {
    negative: "Negative",
    risky: "Risky",
    stable: "Stable",
    improving: "Improving",
  },
  fr: {
    negative: "Négatif",
    risky: "À risque",
    stable: "Stable",
    improving: "En amélioration",
  },
  ar: {
    negative: "سلبي",
    risky: "معرّض للخطر",
    stable: "مستقر",
    improving: "في تحسن",
  },
};

const budgetLabels: any = {
  en: {
    over_budget: "Over budget",
    healthy: "Healthy",
    balanced: "Balanced",
    under_budget: "Under budget",
  },
  fr: {
    over_budget: "Dépassement du budget",
    healthy: "Sain",
    balanced: "Équilibré",
    under_budget: "Sous le budget",
  },
  ar: {
    over_budget: "تجاوز الميزانية",
    healthy: "صحي",
    balanced: "متوازن",
    under_budget: "أقل من الميزانية",
  },
};


const categoryLabels: any = {
  en: {
    income: "Income",
    housing: "Housing",
    utilities: "Utilities",
    government: "Government",
    insurance: "Insurance",
    healthcare: "Healthcare",
    groceries: "Groceries",
    food: "Food & restaurants",
    transport: "Transport",
    travel: "Travel",
    shopping: "Shopping",
    subscriptions: "Subscriptions",
    education: "Education",
    childcare: "Childcare",
    pets: "Pets",
    charity: "Charity",
    fees: "Fees",
    debt: "Debt",
    debt_loans: "Debt & Loans",
    government_taxes: "Government & Taxes",
    business_operations: "Business Expenses",
    food_dining: "Food & Dining",
    savings: "Savings",
    transfers: "Transfers",
    business_services: "Business services",
    cash: "Cash withdrawals",
    other: "Other",
  },
  fr: {
    income: "Revenus",
    housing: "Logement",
    utilities: "Services et factures",
    government: "Impôts et administration",
    insurance: "Assurance",
    healthcare: "Santé",
    groceries: "Courses",
    food: "Restaurants et cafés",
    transport: "Transport",
    travel: "Voyage",
    shopping: "Achats",
    subscriptions: "Abonnements",
    education: "Éducation",
    childcare: "Garde d’enfants",
    pets: "Animaux",
    charity: "Dons",
    fees: "Frais",
    debt: "Dettes et crédits",
    debt_loans: "Dettes & prêts",
    government_taxes: "Gouvernement & taxes",
    business_operations: "Dépenses professionnelles",
    food_dining: "Restaurants & cafés",
    savings: "Épargne",
    transfers: "Transferts",
    business_services: "Services professionnels",
    cash: "Retraits d’espèces",
    other: "Autre",
  },
  ar: {
    income: "الدخل",
    housing: "السكن",
    utilities: "المرافق والفواتير",
    government: "الضرائب والإدارة",
    insurance: "التأمين",
    healthcare: "الصحة",
    groceries: "البقالة",
    food: "المطاعم والمقاهي",
    transport: "النقل",
    travel: "السفر",
    shopping: "التسوق",
    subscriptions: "الاشتراكات",
    education: "التعليم",
    childcare: "رعاية الأطفال",
    pets: "الحيوانات الأليفة",
    charity: "التبرعات",
    fees: "الرسوم",
    debt: "الديون والقروض",
    debt_loans: "القروض والديون",
    government_taxes: "الجهات الحكومية والضرائب",
    business_operations: "مصاريف الأعمال",
    food_dining: "المطاعم والمقاهي",
    savings: "الادخار",
    transfers: "التحويلات",
    business_services: "الخدمات المهنية",
    cash: "السحب النقدي",
    other: "أخرى",
  },
};

const labels: any = {
  en: {
    title: "Personal Finance Coach",
    subtitle:
      "Upload your bank statement PDF to analyze spending, detect waste, and get saving strategies.",
    heroSupport:
      "AI-powered financial insights, subscription detection, savings analysis, and personalized coaching.",
    uploadBadges: ["PDF bank statements", "Private analysis", "Multi-language"],
    sampleOutputTitle: "See example AI financial analysis",
    sampleOutputSubtitle:
      "Preview the kind of insights Runexa generates from a bank statement.",
    sampleNarrativeTitle: "AI Narrative Summary",
    sampleNarrative:
      "Your financial profile shows stable income and positive cashflow, but recurring subscriptions and discretionary spending may reduce long-term savings potential.",
    sampleSavingsTitle: "AI Savings Opportunity",
    sampleSavings:
      "Review unused subscriptions first. Small recurring charges can become meaningful monthly savings.",
    sampleCoachTitle: "Smart Money Coach",
    sampleCoach:
      "Ask follow-up questions, request a savings plan, or understand your score in plain language.",
    exportPdf: "Export Executive PDF Report",
    chartInsightSpending:
      "AI interpretation: spending patterns help reveal peaks, habits, and possible budget pressure.",
    chartInsightCashflow:
      "AI interpretation: daily cashflow shows whether income timing is safely covering expenses.",
    chartInsightSubscriptions:
      "AI interpretation: recurring costs can quietly increase and reduce long-term savings.",
    chartInsightSavings:
      "AI interpretation: running balance highlights whether your financial position is improving over time.",
    coachSubtitle: "Continue your financial analysis conversation",
    coachSecure: "Analysis saved securely",
    howTitle: "How this agent works:",
    how1:
      "Upload a bank statement PDF and the Personal Finance Coach will extract visible transactions, estimate income, spending, transfers, and categorize expenses.",
    how2:
      "The agent then detects possible waste, highlights financial risks, suggests saving strategies, and generates a financial score from 0 to 100.",
    disclaimer:
      "Results are informational only and do not replace professional financial advice.",
    analyze: "Analyze statement",
    analyzing: "Analyzing statement...",
    queued: "Finance analysis queued...",
    elapsed: "Elapsed",
    seconds: "s",
    loadingStages: [
      "Extracting statement text",
      "Detecting transactions",
      "Building financial forecast",
      "Generating AI insights",
    ],
    buyCredits: "Buy credits 💳",
    paymentMessage:
      "Payments are temporarily unavailable during platform rollout. $1 trial activation, credits, and Pro plan will be available soon.",
    proMessage:
      "Payments are temporarily unavailable during platform rollout. Pro access will be available soon.",
    trialInfo: "$1 trial per agent. You can also skip the trial and continue with global credits or a Pro plan.",
    startTrial: "Start $1 trial",
    upgradePro: "Upgrade to Pro",
    trialUsed: "Trial already used for finance",
    paymentRequired: "$1 Finance trial activation required",
    apiError: "Failed to connect to the finance analysis API.",
    results: "Results",
    summary: "Summary",
    currency: "Currency",
    unknown: "unknown",
    financialScore: "Financial score",
    totalSpending: "AI spending estimate",
    observedIncome: "Observed Income",
    financialHabitsScore: "Financial Habits Score",
    cashflowForecast: "Cashflow Forecast",
    detectedSubscriptions: "Detected Subscriptions",
    observedExpenses: "Observed Expenses",
    observedNetCashflow: "Observed Net Cashflow",
    daysUntilRisk: "Days Until Risk",
    recommendedBudget: "Recommended Budget",
    savingsTarget: "Savings Target",
    needs: "Needs",
    wants: "Wants",
    emergencyFund: "Emergency Fund",
    safeSpending: "Safe Spending",
    estimatedRecurringCharge: "Estimated Recurring Charge",
    noRecurringSubscriptions: "No recurring subscriptions detected.",
    aiSavingsOpportunities: "AI Savings Opportunities",
    aiDetected: "AI detected",
    savingsOpportunity: "Savings opportunity",
    aiFinancialInsights: "AI Financial Insights",
    smartMoneyCoach: "Smart Money Coach",
    spendingOverTime: "Spending Over Time",
    expenseEvolution: "Expense Evolution",
    observedNetCashflowOverTime: "Observed Net Cashflow Over Time",
    dailyCashflowTrend: "Daily Cashflow Trend",
    subscriptionGrowth: "Subscription Growth",
    recurringSpendingTrend: "Recurring Spending Trend",
    noRecurringSubscriptionSpending: "No recurring subscription spending detected for this statement.",
    savingsEvolution: "Savings Evolution",
    runningNetBalance: "Running Net Balance",
    aiFinancialCoach: "AI Financial Coach",
    financialOverview: "Financial Overview",
    income: "Income",
    expenses: "Expenses",
    pdfTitle: "Runexa Personal Finance AI Report",
    generated: "Generated",
    executiveSummary: "Executive Summary",
    disclaimerPdf: "Disclaimer: This report is informational only and does not replace professional financial advice.",
    previewTitle: "AI Financial Intelligence Preview",
    previewBadge: "AI preview",
    previewFinancialScore: "Financial score",
    previewSpendingBreakdown: "Spending breakdown",
    previewNeeds: "Needs",
    previewBills: "Bills",
    previewSubscriptions: "Subscriptions",
    previewOther: "Other",
    previewSubscriptionsDetected: "Subscriptions detected",
    previewSavingsOpportunities: "Savings opportunities",
    previewCancelUnusedSubscriptions: "Cancel unused subscriptions",
    previewReduceDiscretionarySpending: "Reduce discretionary spending",
    previewSetMonthlySavingsTarget: "Set monthly savings target",
    chatCancelSubscriptions: "What subscriptions should I cancel first?",
    chatSaveMoreMoney: "How can I save more money?",
    chatAvoidCashflowRisk: "How can I avoid cashflow risk?",
    chatBiggestExpenses: "What are my biggest expenses?",
    chatWhyScoreLow: "Why is my financial score low?",
    chatFinanciallyHealthy: "Am I financially healthy?",
    chatExplainFinancialScore: "Explain my financial score",
    chatCreateSavingsPlan: "Create a 30-day savings plan",
    chatPlaceholder: "Ask about your finances...",
    send: "Send",
    you: "You",
    suggestedFollowUpQuestions: "Suggested follow-up questions",
    couldNotCheckFinanceStatus: "Could not check finance analysis status.",
    financeAnalysisFailed: "Finance analysis failed.",
    financeAnalysisLongerThanExpected: "Finance analysis is taking longer than expected. Please retry in a moment.",
    aiNarrativeSummary: "AI Narrative Summary",
    aiGeneratedScore: "AI-generated overall finance score.",
    deterministicScore: "Deterministic score based on observed transactions.",
    savingBehavior: "Saving behavior",
    subscriptionControl: "Subscription control",
    transactions: "transactions",
    averageCharge: "Average charge",
    totalObserved: "Total observed",
    estimatedSavingsOpportunity: "Estimated savings opportunity",
    noMajorSavingsOpportunities: "No major savings opportunities detected.",
    negativeCashflowRisk: "Negative cashflow risk",
    financialHabitsNeedImprovement: "Financial habits need improvement",
    spendingPatternsNeedMonitoring: "Your spending patterns may require closer monitoring.",
    askFinanceAssistant: "Ask your finance assistant",
    notFinancialAdvice: "This is not financial advice. It is for informational purposes only.",
    mainCategories: "Main categories",
    wasteDetected: "Waste detected",
    savingStrategies: "Saving strategies",
    riskNotes: "Risk notes",
    noFile: "No file selected",
    chooseFile: "Choose file",
  },
  fr: {
    title: "Coach financier personnel",
    subtitle:
      "Téléchargez votre relevé bancaire PDF pour analyser vos dépenses, détecter le gaspillage et obtenir des stratégies d’épargne.",
    heroSupport:
      "Analyse financière IA, détection des abonnements, stratégies d’épargne et coaching personnalisé.",
    uploadBadges: ["Relevés bancaires PDF", "Analyse privée", "Multilingue"],
    sampleOutputTitle: "Voir un exemple d’analyse financière IA",
    sampleOutputSubtitle:
      "Aperçu du type d’insights que Runexa génère à partir d’un relevé bancaire.",
    sampleNarrativeTitle: "Résumé narratif IA",
    sampleNarrative:
      "Votre profil financier montre des revenus stables et un cashflow positif, mais les abonnements récurrents et les dépenses discrétionnaires peuvent réduire votre potentiel d’épargne à long terme.",
    sampleSavingsTitle: "Opportunité d’épargne IA",
    sampleSavings:
      "Analysez d’abord les abonnements inutilisés. Les petits frais récurrents peuvent devenir des économies mensuelles importantes.",
    sampleCoachTitle: "Coach financier intelligent",
    sampleCoach:
      "Posez des questions, demandez un plan d’épargne ou comprenez votre score en langage clair.",
    exportPdf: "Exporter le rapport exécutif PDF",
    chartInsightSpending:
      "Interprétation IA : les tendances de dépenses révèlent les pics, habitudes et pressions budgétaires possibles.",
    chartInsightCashflow:
      "Interprétation IA : le cashflow quotidien montre si le timing des revenus couvre les dépenses en sécurité.",
    chartInsightSubscriptions:
      "Interprétation IA : les coûts récurrents peuvent augmenter discrètement et réduire l’épargne long terme.",
    chartInsightSavings:
      "Interprétation IA : le solde courant montre si votre position financière s’améliore dans le temps.",
    coachSubtitle: "Continuez votre conversation d’analyse financière",
    coachSecure: "Analyse sauvegardée en toute sécurité",
    howTitle: "Comment fonctionne cet agent :",
    how1:
      "Téléchargez un relevé bancaire PDF. Le coach financier extrait les transactions visibles, estime les revenus, les dépenses, les transferts et classe les dépenses par catégorie.",
    how2:
      "L’agent détecte ensuite les dépenses évitables, met en évidence les risques financiers, propose des stratégies d’épargne et génère un score financier de 0 à 100.",
    disclaimer:
      "Les résultats sont fournis à titre informatif uniquement et ne remplacent pas un conseil financier professionnel.",
    analyze: "Analyser le relevé",
    analyzing: "Analyse du relevé en cours...",
    queued: "Analyse financière en file d’attente...",
    elapsed: "Temps écoulé",
    seconds: "s",
    loadingStages: [
      "Extraction du relevé",
      "Détection des transactions",
      "Construction des prévisions",
      "Génération des insights IA",
    ],
    buyCredits: "Acheter des crédits 💳",
    paymentMessage:
      "Les paiements sont temporairement indisponibles pendant le déploiement de la plateforme. L’activation de l’essai à 1$, les crédits et le plan Pro seront bientôt disponibles.",
    proMessage:
      "Les paiements sont temporairement indisponibles pendant le déploiement de la plateforme. L’accès Pro sera bientôt disponible.",
    trialInfo: "Essai à 1$ par agent. Vous pouvez aussi passer directement aux crédits globaux ou au plan Pro.",
    startTrial: "Activer l’essai à 1$",
    upgradePro: "Passer au plan Pro",
    trialUsed: "Essai Finance déjà utilisé",
    paymentRequired: "Activation de l’essai Finance à 1$ requise",
    apiError: "Impossible de se connecter à l’API d’analyse financière.",
    results: "Résultats",
    summary: "Résumé",
    currency: "Devise",
    unknown: "inconnue",
    financialScore: "Score financier",
    totalSpending: "Estimation IA des dépenses",
    observedIncome: "Revenus observés",
    financialHabitsScore: "Score des habitudes financières",
    cashflowForecast: "Prévision de trésorerie",
    detectedSubscriptions: "Abonnements détectés",
    observedExpenses: "Dépenses observées",
    observedNetCashflow: "Trésorerie nette observée",
    daysUntilRisk: "Jours avant risque",
    recommendedBudget: "Budget recommandé",
    savingsTarget: "Objectif d’épargne",
    needs: "Besoins",
    wants: "Envies",
    emergencyFund: "Fonds d’urgence",
    safeSpending: "Dépenses sûres",
    estimatedRecurringCharge: "Charge récurrente estimée",
    noRecurringSubscriptions: "Aucun abonnement récurrent détecté.",
    aiSavingsOpportunities: "Opportunités d’épargne IA",
    aiDetected: "Détecté par IA",
    savingsOpportunity: "Opportunité d’épargne",
    aiFinancialInsights: "Insights financiers IA",
    smartMoneyCoach: "Coach financier intelligent",
    spendingOverTime: "Dépenses dans le temps",
    expenseEvolution: "Évolution des dépenses",
    observedNetCashflowOverTime: "Trésorerie nette observée dans le temps",
    dailyCashflowTrend: "Tendance quotidienne de trésorerie",
    subscriptionGrowth: "Évolution des abonnements",
    recurringSpendingTrend: "Tendance des dépenses récurrentes",
    noRecurringSubscriptionSpending: "Aucune dépense d’abonnement récurrente détectée pour ce relevé.",
    savingsEvolution: "Évolution de l’épargne",
    runningNetBalance: "Solde net courant",
    aiFinancialCoach: "Coach financier IA",
    financialOverview: "Vue d’ensemble financière",
    income: "Revenus",
    expenses: "Dépenses",
    pdfTitle: "Rapport financier personnel IA Runexa",
    generated: "Généré le",
    executiveSummary: "Résumé exécutif",
    disclaimerPdf: "Avertissement : ce rapport est fourni à titre informatif uniquement et ne remplace pas un conseil financier professionnel.",
    previewTitle: "Aperçu de l’intelligence financière IA",
    previewBadge: "Aperçu IA",
    previewFinancialScore: "Score financier",
    previewSpendingBreakdown: "Répartition des dépenses",
    previewNeeds: "Besoins",
    previewBills: "Factures",
    previewSubscriptions: "Abonnements",
    previewOther: "Autre",
    previewSubscriptionsDetected: "Abonnements détectés",
    previewSavingsOpportunities: "Opportunités d’épargne",
    previewCancelUnusedSubscriptions: "Annuler les abonnements inutilisés",
    previewReduceDiscretionarySpending: "Réduire les dépenses discrétionnaires",
    previewSetMonthlySavingsTarget: "Définir un objectif d’épargne mensuel",
    chatCancelSubscriptions: "Quels abonnements dois-je annuler en premier ?",
    chatSaveMoreMoney: "Comment puis-je économiser plus d’argent ?",
    chatAvoidCashflowRisk: "Comment éviter un risque de trésorerie ?",
    chatBiggestExpenses: "Quelles sont mes plus grosses dépenses ?",
    chatWhyScoreLow: "Pourquoi mon score financier est-il bas ?",
    chatFinanciallyHealthy: "Ma situation financière est-elle saine ?",
    chatExplainFinancialScore: "Explique mon score financier",
    chatCreateSavingsPlan: "Crée un plan d’épargne sur 30 jours",
    chatPlaceholder: "Posez une question sur vos finances...",
    send: "Envoyer",
    you: "Vous",
    suggestedFollowUpQuestions: "Questions de suivi suggérées",
    couldNotCheckFinanceStatus: "Impossible de vérifier le statut de l’analyse financière.",
    financeAnalysisFailed: "L’analyse financière a échoué.",
    financeAnalysisLongerThanExpected: "L’analyse financière prend plus de temps que prévu. Veuillez réessayer dans un moment.",
    aiNarrativeSummary: "Résumé narratif IA",
    aiGeneratedScore: "Score financier global généré par l’IA.",
    deterministicScore: "Score déterministe basé sur les transactions observées.",
    savingBehavior: "Comportement d’épargne",
    subscriptionControl: "Contrôle des abonnements",
    transactions: "transactions",
    averageCharge: "Frais moyens",
    totalObserved: "Total observé",
    estimatedSavingsOpportunity: "Opportunité d’épargne estimée",
    noMajorSavingsOpportunities: "Aucune opportunité d’épargne majeure détectée.",
    negativeCashflowRisk: "Risque de trésorerie négative",
    financialHabitsNeedImprovement: "Les habitudes financières doivent être améliorées",
    spendingPatternsNeedMonitoring: "Vos habitudes de dépense peuvent nécessiter un suivi plus attentif.",
    askFinanceAssistant: "Posez une question à votre assistant financier",
    notFinancialAdvice: "Ceci n’est pas un conseil financier. Ces informations sont fournies à titre informatif uniquement.",
    mainCategories: "Catégories principales",
    wasteDetected: "Dépenses évitables détectées",
    savingStrategies: "Stratégies d’épargne",
    riskNotes: "Notes de risque",
    noFile: "Aucun fichier sélectionné",
    chooseFile: "Choisir un fichier",
  },
  ar: {
    title: "وكيل الإدارة المالية الشخصية",
    subtitle:
      "ارفع كشف حسابك البنكي بصيغة PDF لتحليل المصاريف، كشف الهدر، والحصول على استراتيجيات ادخار.",
    heroSupport:
      "تحليل مالي بالذكاء الاصطناعي، كشف الاشتراكات، استراتيجيات الادخار، وتوجيه مالي ذكي.",
    uploadBadges: ["كشوفات بنكية PDF", "تحليل خاص", "متعدد اللغات"],
    sampleOutputTitle: "شاهد مثالاً لتحليل مالي بالذكاء الاصطناعي",
    sampleOutputSubtitle:
      "معاينة لنوع الرؤى التي تولدها Runexa من كشف الحساب البنكي.",
    sampleNarrativeTitle: "ملخص سردي ذكي",
    sampleNarrative:
      "يُظهر ملفك المالي دخلاً مستقراً وتدفقاً نقدياً إيجابياً، لكن الاشتراكات المتكررة والإنفاق الاختياري قد يقللان من القدرة على الادخار على المدى الطويل.",
    sampleSavingsTitle: "فرصة ادخار ذكية",
    sampleSavings:
      "راجع الاشتراكات غير المستخدمة أولاً. الرسوم الصغيرة المتكررة قد تتحول إلى وفورات شهرية مهمة.",
    sampleCoachTitle: "مدرب مالي ذكي",
    sampleCoach:
      "اطرح أسئلة متابعة، اطلب خطة ادخار، أو افهم نتيجتك المالية بلغة واضحة.",
    exportPdf: "تصدير تقرير PDF تنفيذي",
    chartInsightSpending:
      "تفسير الذكاء الاصطناعي: أنماط الإنفاق تكشف الذروات والعادات وضغط الميزانية المحتمل.",
    chartInsightCashflow:
      "تفسير الذكاء الاصطناعي: التدفق النقدي اليومي يوضح ما إذا كان توقيت الدخل يغطي النفقات بأمان.",
    chartInsightSubscriptions:
      "تفسير الذكاء الاصطناعي: التكاليف المتكررة قد ترتفع تدريجياً وتقلل الادخار طويل المدى.",
    chartInsightSavings:
      "تفسير الذكاء الاصطناعي: الرصيد الجاري يوضح ما إذا كان وضعك المالي يتحسن بمرور الوقت.",
    coachSubtitle: "تابع محادثة التحليل المالي",
    coachSecure: "تم حفظ التحليل بأمان",
    howTitle: "كيف يعمل هذا الوكيل:",
    how1:
      "ارفع كشف حساب بنكي PDF وسيقوم وكيل الإدارة المالية باستخراج المعاملات الظاهرة، وتقدير الدخل، المصاريف، التحويلات، وتصنيف النفقات.",
    how2:
      "بعد ذلك يكتشف الوكيل النفقات التي يمكن تجنبها، يوضح المخاطر المالية، يقترح استراتيجيات ادخار، وينشئ نتيجة مالية من 0 إلى 100.",
    disclaimer:
      "النتائج معلوماتية فقط ولا تُعد بديلاً عن الاستشارة المالية المهنية.",
    analyze: "تحليل الكشف",
    analyzing: "جاري تحليل الكشف...",
    queued: "تمت إضافة التحليل المالي إلى قائمة الانتظار...",
    elapsed: "الوقت المنقضي",
    seconds: "ث",
    loadingStages: [
      "استخراج نص الكشف",
      "كشف المعاملات",
      "إنشاء التوقعات المالية",
      "توليد الرؤى الذكية",
    ],
    buyCredits: "شراء رصيد 💳",
    paymentMessage:
      "المدفوعات غير متاحة مؤقتاً أثناء إطلاق المنصة. تفعيل تجربة 1 دولار، الأرصدة وخطة Pro ستكون متاحة قريباً.",
    proMessage:
      "المدفوعات غير متاحة مؤقتاً أثناء إطلاق المنصة. سيتوفر وصول Pro قريباً.",
    trialInfo: "تجربة بقيمة 1 دولار لكل وكيل. يمكنك أيضاً المتابعة مباشرة بالأرصدة العامة أو خطة Pro.",
    startTrial: "تفعيل تجربة 1 دولار",
    upgradePro: "الترقية إلى Pro",
    trialUsed: "تم استخدام تجربة وكيل المالية",
    paymentRequired: "يلزم تفعيل تجربة المالية بقيمة 1 دولار",
    apiError: "تعذر الاتصال بواجهة تحليل المالية.",
    results: "النتائج",
    summary: "الملخص",
    currency: "العملة",
    unknown: "غير معروفة",
    financialScore: "النتيجة المالية",
    totalSpending: "تقدير الذكاء الاصطناعي للمصاريف",
    observedIncome: "الدخل الفعلي المرصود",
    financialHabitsScore: "درجة العادات المالية",
    cashflowForecast: "توقع التدفق النقدي",
    detectedSubscriptions: "الاشتراكات المكتشفة",
    observedExpenses: "المصاريف الفعلية المرصودة",
    observedNetCashflow: "صافي التدفق النقدي المرصود",
    daysUntilRisk: "الأيام قبل الخطر",
    recommendedBudget: "الميزانية المقترحة",
    savingsTarget: "هدف الادخار",
    needs: "الاحتياجات",
    wants: "الرغبات",
    emergencyFund: "صندوق الطوارئ",
    safeSpending: "الإنفاق الآمن",
    estimatedRecurringCharge: "التكلفة المتكررة المقدرة",
    noRecurringSubscriptions: "لم يتم اكتشاف اشتراكات متكررة.",
    aiSavingsOpportunities: "فرص الادخار بالذكاء الاصطناعي",
    aiDetected: "تم اكتشافه بالذكاء الاصطناعي",
    savingsOpportunity: "فرصة ادخار",
    aiFinancialInsights: "رؤى مالية بالذكاء الاصطناعي",
    smartMoneyCoach: "مدرب مالي ذكي",
    spendingOverTime: "الإنفاق عبر الوقت",
    expenseEvolution: "تطور المصاريف",
    observedNetCashflowOverTime: "صافي التدفق النقدي المرصود عبر الوقت",
    dailyCashflowTrend: "اتجاه التدفق النقدي اليومي",
    subscriptionGrowth: "نمو الاشتراكات",
    recurringSpendingTrend: "اتجاه الإنفاق المتكرر",
    noRecurringSubscriptionSpending: "لم يتم اكتشاف إنفاق اشتراكات متكرر لهذا الكشف.",
    savingsEvolution: "تطور الادخار",
    runningNetBalance: "الرصيد الصافي الجاري",
    aiFinancialCoach: "المدرب المالي الذكي",
    financialOverview: "نظرة عامة مالية",
    income: "الدخل",
    expenses: "المصاريف",
    pdfTitle: "تقرير Runexa المالي الشخصي بالذكاء الاصطناعي",
    generated: "تم الإنشاء",
    executiveSummary: "الملخص التنفيذي",
    disclaimerPdf: "تنبيه: هذا التقرير معلوماتي فقط ولا يُعد بديلاً عن الاستشارة المالية المهنية.",
    previewTitle: "معاينة الذكاء المالي بالذكاء الاصطناعي",
    previewBadge: "معاينة بالذكاء الاصطناعي",
    previewFinancialScore: "النتيجة المالية",
    previewSpendingBreakdown: "تفصيل المصاريف",
    previewNeeds: "الاحتياجات",
    previewBills: "الفواتير",
    previewSubscriptions: "الاشتراكات",
    previewOther: "أخرى",
    previewSubscriptionsDetected: "الاشتراكات المكتشفة",
    previewSavingsOpportunities: "فرص الادخار",
    previewCancelUnusedSubscriptions: "إلغاء الاشتراكات غير المستخدمة",
    previewReduceDiscretionarySpending: "تقليل الإنفاق الاختياري",
    previewSetMonthlySavingsTarget: "تحديد هدف ادخار شهري",
    chatCancelSubscriptions: "ما الاشتراكات التي يجب أن ألغيها أولاً؟",
    chatSaveMoreMoney: "كيف يمكنني ادخار المزيد من المال؟",
    chatAvoidCashflowRisk: "كيف أتجنب خطر التدفق النقدي؟",
    chatBiggestExpenses: "ما أكبر مصاريفي؟",
    chatWhyScoreLow: "لماذا نتيجتي المالية منخفضة؟",
    chatFinanciallyHealthy: "هل وضعي المالي صحي؟",
    chatExplainFinancialScore: "اشرح نتيجتي المالية",
    chatCreateSavingsPlan: "أنشئ خطة ادخار لمدة 30 يوماً",
    chatPlaceholder: "اسأل عن أمورك المالية...",
    send: "إرسال",
    you: "أنت",
    suggestedFollowUpQuestions: "أسئلة متابعة مقترحة",
    couldNotCheckFinanceStatus: "تعذر التحقق من حالة التحليل المالي.",
    financeAnalysisFailed: "فشل التحليل المالي.",
    financeAnalysisLongerThanExpected: "يستغرق التحليل المالي وقتاً أطول من المتوقع. يرجى المحاولة بعد قليل.",
    aiNarrativeSummary: "ملخص سردي بالذكاء الاصطناعي",
    aiGeneratedScore: "نتيجة مالية عامة تم إنشاؤها بالذكاء الاصطناعي.",
    deterministicScore: "نتيجة حتمية مبنية على المعاملات المرصودة.",
    savingBehavior: "سلوك الادخار",
    subscriptionControl: "التحكم في الاشتراكات",
    transactions: "معاملات",
    averageCharge: "متوسط التكلفة",
    totalObserved: "الإجمالي المرصود",
    estimatedSavingsOpportunity: "فرصة الادخار المقدرة",
    noMajorSavingsOpportunities: "لم يتم اكتشاف فرص ادخار كبيرة.",
    negativeCashflowRisk: "خطر تدفق نقدي سلبي",
    financialHabitsNeedImprovement: "العادات المالية تحتاج إلى تحسين",
    spendingPatternsNeedMonitoring: "قد تتطلب أنماط إنفاقك مراقبة أكثر دقة.",
    askFinanceAssistant: "اسأل مساعدك المالي",
    notFinancialAdvice: "هذه ليست نصيحة مالية. المعلومات لأغراض إعلامية فقط.",
    mainCategories: "الفئات الرئيسية",
    wasteDetected: "الهدر المكتشف",
    savingStrategies: "استراتيجيات الادخار",
    riskNotes: "ملاحظات المخاطر",
    noFile: "لم يتم اختيار ملف",
    chooseFile: "اختيار ملف",
  },
};

export default function FinanceClient() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [paymentMessage, setPaymentMessage] = useState("");
  const [language, setLanguage] = useState("en");
  const [plan, setPlan] = useState("");
  const [role, setRole] = useState("");
  const [creditsBalance, setCreditsBalance] = useState(0);
  const [chatMessages, setChatMessages] = useState<any[]>([]);
  const [chatInput, setChatInput] = useState("");
  const [chatLoading, setChatLoading] = useState(false);
  const [suggestedQuestions, setSuggestedQuestions] = useState<string[]>([]);
  const [jobId, setJobId] = useState<number | null>(null);
  const [jobStatus, setJobStatus] = useState("");
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [loadingStep, setLoadingStep] = useState("");
  const [startedAt, setStartedAt] = useState<number | null>(null);
  const [elapsedSeconds, setElapsedSeconds] = useState(0);

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

  useEffect(() => {
    if (!loading || !startedAt) return;

    const interval = window.setInterval(() => {
      setElapsedSeconds(
        Math.max(0, Math.floor((Date.now() - startedAt) / 1000))
      );
    }, 1000);

    return () => window.clearInterval(interval);
  }, [loading, startedAt]);

  const t = labels[language] || labels.en;

  const isInsufficientData =
    result?.status === "insufficient_data" ||
    result?.analysis_status === "insufficient_data";


  const translateInsightText = (value: any) => {
    if (typeof value !== "string") return value;

    const insightTranslations: Record<string, string> = {
      "Negative cashflow risk": t.negativeCashflowRisk,
      "Financial habits need improvement": t.financialHabitsNeedImprovement,
      "Your spending patterns may require closer monitoring.": t.spendingPatternsNeedMonitoring,
      "This is not financial advice.": t.notFinancialAdvice,
      "This is not financial advice...": t.notFinancialAdvice,
      "This is not financial advice. It is for informational purposes only.": t.notFinancialAdvice,
    };

    return insightTranslations[value] || value;
  };


  const translateBackendMessage = (value: any) => {
    if (typeof value !== "string") return value;

    const backendMessageLabels: any = {
      en: {
        "Your expenses exceed your income.": "Your expenses exceed your income.",
        "Your current spending is higher than your estimated income.": "Your current spending is higher than your estimated income.",
        "This is not financial advice. It is for informational purposes only.": t.notFinancialAdvice,
      },
      fr: {
        "Your expenses exceed your income.": "Vos dépenses dépassent vos revenus.",
        "Your current spending is higher than your estimated income.": "Vos dépenses actuelles sont supérieures à vos revenus estimés.",
        "This is not financial advice. It is for informational purposes only.": t.notFinancialAdvice,
      },
      ar: {
        "Your expenses exceed your income.": "مصاريفك تتجاوز دخلك.",
        "Your current spending is higher than your estimated income.": "إنفاقك الحالي أعلى من دخلك المقدر.",
        "This is not financial advice. It is for informational purposes only.": t.notFinancialAdvice,
      },
    };

    return backendMessageLabels[language]?.[value] || translateInsightText(value);
  };

  const translateCategory = (value: any) => {
    if (typeof value !== "string") return value;

    const normalized = value.toLowerCase().trim();

    return categoryLabels[language]?.[normalized] || value;
  };

  const hasActiveAccess =
    role === "admin" ||
    role === "enterprise_admin" ||
    role === "enterprise_member" ||
    ["paid", "pro", "premium"].includes(plan) ||
    creditsBalance > 0;

  const primaryCtaLabel = hasActiveAccess
    ? t.analyze
    : t.startTrial;

  const COLORS = [
    "#22c55e",
    "#3b82f6",
    "#f59e0b",
    "#ef4444",
    "#8b5cf6",
    "#14b8a6",
    "#ec4899",
    "#64748b",
  ];

  const currencySymbol =
    result?.currency_detected === "USD"
      ? "$"
      : result?.currency_detected === "EUR"
      ? "€"
      : result?.currency_detected === "MAD"
      ? "MAD"
      : result?.currency_detected === "GBP"
      ? "£"
      : result?.currency_detected === "CAD"
      ? "CA$"
      : "";

  const formatMoney = (value: any) => {
    const amount = Number(value || 0);
    return currencySymbol ? `${currencySymbol} ${amount}` : `${amount}`;
  };

  const chartData =
    result?.charts?.category_breakdown?.map((item: any) => ({
      name: translateCategory(item.category),
      value: Number(item.amount),
    })) || [];


  const translatedCashflowTrend =
    trendLabels[language]?.[result?.cashflow_forecast?.trend] ??
    result?.cashflow_forecast?.trend ??
    "unknown";

  const translatedBudgetStatus =
    budgetLabels[language]?.[result?.recommended_budget?.status] ??
    result?.recommended_budget?.status ??
    "unknown";

  const quickQuestions = [
    result?.subscriptions_detected?.length > 0
      ? t.chatCancelSubscriptions
      : t.chatSaveMoreMoney,
    result?.cashflow_forecast?.trend === "negative" ||
    result?.cashflow_forecast?.trend === "risky"
      ? t.chatAvoidCashflowRisk
      : t.chatBiggestExpenses,
    (result?.financial_habit_scores?.overall_financial_habits_score || 100) < 60
      ? t.chatWhyScoreLow
      : t.chatFinanciallyHealthy,
    t.chatExplainFinancialScore,
    t.chatCreateSavingsPlan,
  ];

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

  const loadFinanceChatHistory = async (analysisId: number) => {
    try {
      const token = safeGetLocalStorage("token");
      const API_URL = process.env.NEXT_PUBLIC_API_URL;

      const res = await fetch(
        `${API_URL}/finance/chat/history/${analysisId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!res.ok) return;

      const data = await res.json();

      setChatMessages(
        Array.isArray(data)
          ? data.map((item: any) => ({
              role: item.role,
              content: item.content,
            }))
          : []
      );
    } catch (error) {
      console.error("Chat history load failed:", error);
    }
  };

  const handleAnalyze = async () => {
    if (!file) return;

    setLoading(true);
    setResult(null);
    setPaymentMessage("");
    setChatMessages([]);
    setChatInput("");
    setSuggestedQuestions([]);
    setJobId(null);
    setJobStatus("");
    setLoadingProgress(0);
    setLoadingStep(t.queued);
    setStartedAt(Date.now());
    setElapsedSeconds(0);

    try {
      let data = await analyzeFinanceStatement(file, language);

      if (data?.job_id) {
        const currentJobId = data.job_id;

        setJobId(currentJobId);
        setJobStatus(data.status || "pending");
        setLoadingProgress(
          typeof data.progress === "number" ? data.progress : 0
        );
        setLoadingStep(data.status_message || t.queued);

        const token = safeGetLocalStorage("token");
        const API_URL = process.env.NEXT_PUBLIC_API_URL;

        let attempts = 0;
        let completed = false;

        while (attempts < 180 && !completed) {
          await new Promise((resolve) => setTimeout(resolve, 2000));

          const statusResponse = await fetch(
            `${API_URL}/jobs/${currentJobId}`,
            {
              headers: {
                ...(token
                  ? {
                      Authorization: `Bearer ${token}`,
                    }
                  : {}),
              },
            }
          );

          if (!statusResponse.ok) {
            throw new Error(t.couldNotCheckFinanceStatus);
          }

          const statusData = await statusResponse.json();

          setJobId(statusData.id || currentJobId);
          setJobStatus(statusData.status || "");

          if (typeof statusData.progress === "number") {
            setLoadingProgress(statusData.progress);
          }

          if (statusData.status_message) {
            setLoadingStep(statusData.status_message);
          }

          if (statusData.status === "completed") {
            data = statusData.result;
            completed = true;
            break;
          }

          if (statusData.status === "failed") {
            throw new Error(
              statusData.error || t.financeAnalysisFailed
            );
          }

          attempts++;
        }

        if (!completed) {
          throw new Error(
            t.financeAnalysisLongerThanExpected
          );
        }
      }

      setLoadingProgress(100);
      setResult(data);

      if (data?.id) {
        await loadFinanceChatHistory(data.id);
      }

      await refreshUserBilling();
    } catch (error) {
      console.error("Finance analysis failed");

      const errorMessage =
        error instanceof Error ? error.message : t.apiError;

      if (errorMessage.includes("Trial already used")) {
        setPaymentMessage(t.trialUsed);
      } else if (errorMessage.includes("$1 trial payment required")) {
        setPaymentMessage(t.paymentRequired);
      } else {
        setResult({
          detail: errorMessage,
        });
      }
    } finally {
      setLoading(false);
      setStartedAt(null);
    }
  };

  const sendFinanceQuestion = async (question?: string) => {
    const finalQuestion = question || chatInput;
    const token = safeGetLocalStorage("token");
    const analysisId = result?.id;

    if (!token || !analysisId || !finalQuestion?.trim()) return;

    setChatLoading(true);

    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL;

      const res = await fetch(`${API_URL}/finance/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          analysis_id: analysisId,
          question: finalQuestion,
          output_language: language,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || t.financeAnalysisFailed);
      }

      setChatMessages((prev) => [
        ...prev,
        {
          role: "user",
          content: finalQuestion,
        },
        {
          role: "assistant",
          content: data.answer,
        },
      ]);

      setSuggestedQuestions(
        Array.isArray(data.suggested_questions)
          ? data.suggested_questions
          : []
      );

      setChatInput("");
    } catch (error) {
      console.error("Finance chat error:", error);
    } finally {
      setChatLoading(false);
    }
  };

  const exportFinanceReportPdf = () => {
    if (!result) return;

    const doc = new jsPDF();
    let y = 18;

    const addLine = (gap = 8) => {
      y += gap;

      if (y > 280) {
        doc.addPage();
        y = 18;
      }
    };

    doc.setFontSize(20);
    doc.text(t.pdfTitle, 14, y);

    addLine(8);
    doc.setFontSize(10);
    doc.text(`${t.generated}: ${new Date().toLocaleDateString()}`, 14, y);

    addLine(12);
    doc.setFontSize(13);
    doc.text(t.executiveSummary, 14, y);

    addLine(8);
    doc.setFontSize(10);
    doc.text(doc.splitTextToSize(result.summary || "-", 180), 14, y);

    addLine(22);
    doc.setFontSize(13);
    doc.text(t.financialOverview, 14, y);

    addLine(8);
    doc.setFontSize(10);
    doc.text(`${t.income}: ${formatMoney(result.cashflow_forecast?.observed_income)}`, 14, y);
    addLine(7);
    doc.text(`${t.expenses}: ${formatMoney(result.cashflow_forecast?.observed_expenses)}`, 14, y);
    addLine(7);
    doc.text(`${t.observedNetCashflow}: ${formatMoney(result.cashflow_forecast?.observed_net_cashflow)}`, 14, y);
    addLine(7);
    doc.text(`${t.financialHabitsScore}: ${result.financial_habit_scores?.overall_financial_habits_score ?? "-"}/100`, 14, y);

    addLine(12);
    doc.setFontSize(13);
    doc.text(t.aiSavingsOpportunities, 14, y);

    addLine(8);
    doc.setFontSize(10);

    (result.savings_opportunities || []).forEach((item: any) => {
      doc.text(
        `${item.issue}: ${t.estimatedSavingsOpportunity} ${formatMoney(item.estimated_savings_opportunity)}`,
        14,
        y
      );

      addLine(6);

      doc.text(
        doc.splitTextToSize(item.recommendation || "-", 180),
        18,
        y
      );

      addLine(8);
    });

    addLine(4);
    doc.setFontSize(13);
    doc.text(t.detectedSubscriptions, 14, y);

    addLine(8);
    doc.setFontSize(10);

    (result.subscriptions_detected || []).forEach((sub: any) => {
      doc.text(
        `${sub.name}: ${t.averageCharge} ${formatMoney(sub.monthly_cost)} | ${t.totalObserved} ${formatMoney(sub.total_observed_cost)} | ${t.transactions}: ${sub.transactions_count}`,
        14,
        y
      );

      addLine(7);
    });

    addLine(6);
    doc.setFontSize(13);
    doc.text(t.recommendedBudget, 14, y);

    addLine(8);
    doc.setFontSize(10);
    doc.text(`${t.needs}: ${formatMoney(result.recommended_budget?.needs)}`, 14, y);

    addLine(7);
    doc.text(`${t.wants}: ${formatMoney(result.recommended_budget?.wants)}`, 14, y);

    addLine(7);
    doc.text(`${t.savingsTarget}: ${formatMoney(result.recommended_budget?.savings_target)}`, 14, y);

    addLine(7);
    doc.text(`${t.emergencyFund}: ${formatMoney(result.recommended_budget?.emergency_fund_target)}`, 14, y);

    addLine(7);
    doc.text(`Status: ${translatedBudgetStatus || "-"}`, 14, y);

    addLine(12);
    doc.setFontSize(9);

    doc.text(
      doc.splitTextToSize(
        t.disclaimerPdf,
        180
      ),
      14,
      y
    );

    doc.save("runexa-personal-finance-report.pdf");
  };

  return (
    <main
      dir={language === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-4 py-12 sm:py-16"
    >
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold tracking-tight text-slate-950 sm:text-5xl">
            {t.title}
          </h1>

          <p className="mx-auto mt-4 max-w-3xl text-slate-500">
            {t.subtitle}
          </p>

          <p className="mx-auto mt-4 max-w-3xl text-sm font-medium text-slate-600">
            {t.heroSupport}
          </p>
        </div>

        <div className="rounded-2xl border bg-white p-6 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-md">
          <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <p className="text-sm font-medium text-blue-600">
                {t.sampleOutputTitle}
              </p>
              <h2 className="mt-1 text-xl font-semibold text-slate-900">
                {t.previewTitle}
              </h2>
              <p className="mt-2 text-sm leading-6 text-slate-500">
                {t.sampleOutputSubtitle}
              </p>
            </div>
            <span className="rounded-full bg-green-100 px-3 py-1 text-xs font-medium text-green-700">
              {t.previewBadge}
            </span>
          </div>

          <div className="mt-6 grid gap-4 lg:grid-cols-4">
            <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4">
              <p className="text-sm font-semibold text-emerald-900">
                {t.previewFinancialScore}
              </p>

              <div className="mt-3 flex items-end gap-2">
                <span className="text-4xl font-bold text-emerald-700">78</span>
                <span className="mb-1 text-sm text-emerald-700">/100</span>
              </div>

              <div className="mt-4 h-2 overflow-hidden rounded-full bg-white">
                <div className="h-full w-[78%] rounded-full bg-emerald-600" />
              </div>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-4">
              <p className="text-sm font-semibold text-slate-900">
                {t.previewSpendingBreakdown}
              </p>

              <div className="mt-4 flex items-center justify-center">
                <div className="h-28 w-28 rounded-full bg-[conic-gradient(#22c55e_0_38%,#3b82f6_38%_62%,#f59e0b_62%_82%,#ef4444_82%_100%)]" />
              </div>

              <div className="mt-4 grid grid-cols-2 gap-2 text-xs text-slate-600">
                <span>● {t.previewNeeds}</span>
                <span>● {t.previewBills}</span>
                <span>● {t.previewSubscriptions}</span>
                <span>● {t.previewOther}</span>
              </div>
            </div>

            <div className="rounded-2xl border border-red-200 bg-red-50 p-4">
              <p className="text-sm font-semibold text-red-900">
                {t.previewSubscriptionsDetected}
              </p>

              <div className="mt-4 space-y-3">
                {[
                  ["Hostinger", "$19.99"],
                  ["Railway", "$7.39"],
                  ["Streaming", "$12.99"],
                ].map(([name, amount]) => (
                  <div
                    key={name}
                    className="flex items-center justify-between rounded-xl bg-white px-3 py-2 text-sm"
                  >
                    <span className="font-medium text-slate-700">{name}</span>
                    <span className="font-semibold text-red-600">{amount}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="rounded-2xl border border-blue-200 bg-blue-50 p-4">
              <p className="text-sm font-semibold text-blue-900">
                {t.previewSavingsOpportunities}
              </p>

              <div className="mt-4 space-y-3">
                {[
                  t.previewCancelUnusedSubscriptions,
                  t.previewReduceDiscretionarySpending,
                  t.previewSetMonthlySavingsTarget,
                ].map((item) => (
                  <div
                    key={item}
                    className="rounded-xl bg-white px-3 py-2 text-sm text-blue-800"
                  >
                    {item}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-b from-white to-slate-50/80 p-6 rounded-2xl border space-y-4 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-md">
          <div className="rounded-xl bg-slate-50 border border-slate-200 p-4 text-sm text-slate-600 space-y-2 transition-all duration-300 hover:border-blue-200 hover:bg-white hover:shadow-md">
            <p>
              <strong>{t.howTitle}</strong> {t.how1}
            </p>
            <p>{t.how2}</p>
            <p className="text-xs text-slate-500">{t.disclaimer}</p>
          </div>

          <div className="flex flex-wrap gap-2">
            {t.uploadBadges.map((badge: string) => (
              <span
                key={badge}
                className="rounded-full border border-slate-200 bg-white px-3 py-1 text-xs font-medium text-slate-600"
              >
                {badge}
              </span>
            ))}
          </div>

          <select
            value={language}
            onChange={(e) => {
              setLanguage(e.target.value);
              setSavedLocale(e.target.value);
              setResult(null);
              setPaymentMessage("");
            }}
            className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
          >
            <option value="en">English</option>
            <option value="fr">Français</option>
            <option value="ar">العربية</option>
          </select>

          <div className="space-y-2">
            <input
              id="file-upload"
              type="file"
              accept=".pdf"
              onChange={(e) => {
                setFile(e.target.files?.[0] || null);
                setResult(null);
                setPaymentMessage("");
                setChatMessages([]);
                setChatInput("");
                setSuggestedQuestions([]);
              }}
              className="hidden"
            />

            <label
              htmlFor="file-upload"
              className="flex items-center justify-between cursor-pointer rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm transition-all duration-300 hover:border-blue-200 hover:bg-slate-50 hover:shadow-md"
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
              className="w-full rounded-xl bg-slate-900 py-3 text-white transition-all duration-300 hover:bg-slate-800 hover:shadow-xl disabled:bg-slate-400 disabled:hover:shadow-none"
            >
              {loading ? t.analyzing : primaryCtaLabel}
            </button>

            <button
              onClick={() => setPaymentMessage(t.paymentMessage)}
              className="w-full rounded-xl border border-slate-300 bg-white py-3 text-slate-800 transition-all duration-300 hover:border-blue-200 hover:bg-slate-50 hover:shadow-md"
            >
              <span className="flex items-center justify-center gap-2">
                {t.buyCredits}
              </span>
            </button>

            <button
              onClick={() =>
                setPaymentMessage(t.proMessage)
              }
              className="w-full rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 py-3 text-white transition-all duration-300 hover:shadow-xl"
            >
              {t.upgradePro}
            </button>
          </div>

          {paymentMessage && (
            <p className="text-sm text-amber-600 bg-amber-50 border border-amber-200 rounded-xl px-4 py-3">
              {paymentMessage}
            </p>
          )}

          {loading && (
            <div className="rounded-2xl border border-blue-100 bg-blue-50 p-5">
              <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <p className="font-semibold text-blue-950">
                    {loadingStep || t.analyzing}
                  </p>

                  <p className="text-sm text-blue-700">
                    {t.elapsed}: {elapsedSeconds}{t.seconds}
                    {jobId ? ` · Job #${jobId}` : ""}
                    {jobStatus ? ` · ${jobStatus}` : ""}
                  </p>
                </div>

                <span className="rounded-full bg-white px-3 py-1 text-sm font-bold text-blue-700">
                  {loadingProgress}%
                </span>
              </div>

              <div className="mt-4 h-2 overflow-hidden rounded-full bg-white">
                <div
                  className="h-full animate-pulse rounded-full bg-blue-600 transition-all duration-700"
                  style={{
                    width: `${Math.min(
                      Math.max(loadingProgress || 0, 0),
                      100
                    )}%`,
                  }}
                />
              </div>

              <div className="mt-5 grid gap-3 md:grid-cols-4">
                {t.loadingStages.map((stage: string, index: number) => {
                  const thresholds = [20, 45, 70, 90];
                  const done = loadingProgress >= thresholds[index];
                  const active =
                    !done &&
                    loadingProgress >= (thresholds[index - 1] || 0);

                  return (
                    <div
                      key={stage}
                      className={`rounded-xl border p-3 text-xs font-medium ${
                        done
                          ? "border-green-200 bg-green-50 text-green-800"
                          : active
                          ? "border-blue-200 bg-white text-blue-800"
                          : "border-slate-200 bg-white/70 text-slate-500"
                      }`}
                    >
                      {done ? "✓" : active ? "⏳" : "○"} {stage}
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>

        {result && (
          <div className="bg-white p-6 rounded-2xl border space-y-4 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-md">
            <h2 className="text-xl font-semibold">{t.results}</h2>

            <button
              onClick={exportFinanceReportPdf}
              className="rounded-xl bg-slate-900 px-4 py-2 text-sm font-medium text-white transition-all duration-300 hover:bg-slate-800 hover:shadow-md"
            >
              {t.exportPdf}
            </button>

            {result.detail ? (
              <p className="text-red-600">{result.detail}</p>
            ) : (
              <>
                {isInsufficientData ? (
                  <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5">
                    <p className="text-sm font-semibold text-amber-900">
                      {language === "fr"
                        ? "Analyse terminée avec confiance limitée"
                        : language === "ar"
                        ? "تمت المعالجة بثقة محدودة"
                        : "Analysis completed with limited confidence"}
                    </p>

                    <p className="mt-2 text-sm leading-7 text-amber-800">
                      {result.message}
                    </p>

                    <p className="mt-3 text-xs text-amber-700">
                      Confidence: {result.confidence ?? result.analysis_quality?.confidence ?? 25}%
                    </p>
                  </div>
                ) : (
                  <>
                    <div className="rounded-2xl border bg-blue-50 p-5">
                  <p className="text-sm text-blue-700">
                    {t.aiNarrativeSummary}
                  </p>
                  <p className="mt-2 text-sm leading-7 text-slate-700">
                    {result.summary}
                  </p>
                </div>

                <p>
                  <strong>{t.currency}:</strong>{" "}
                  {result.currency_detected || t.unknown}
                </p>

                {result.financial_score !== undefined && (
                  <div>
                    <p>
                      <strong>{t.financialScore}:</strong>{" "}
                      {result.financial_score ?? "N/A"}/100
                    </p>

                    <p className="text-xs text-slate-500 mt-1">
                      {t.aiGeneratedScore}
                    </p>

                    <div className="mt-4">
                      <div className="h-3 bg-slate-200 rounded-full">
                        <div
                          className={`h-3 rounded-full ${
                            result.financial_score >= 70
                              ? "bg-green-500"
                              : result.financial_score >= 50
                              ? "bg-yellow-500"
                              : "bg-red-500"
                          }`}
                          style={{
                            width: `${Math.min(
                              Math.max(result.financial_score || 0, 0),
                              100
                            )}%`,
                          }}
                        />
                      </div>
                    </div>
                  </div>
                )}

                <p>
                  <strong>{t.totalSpending}:</strong>{" "}
                  {formatMoney(result.total_spending_estimate)}
                </p>

                {/* KPI CARDS */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
                  <div className="rounded-2xl border bg-slate-50 p-4 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-md">
                    <p className="text-sm text-slate-500">
                      {t.observedIncome}
                    </p>

                    <h3 className="text-2xl font-bold text-green-600 mt-1">
                      {formatMoney(
                        result.cashflow_forecast?.observed_income
                      )}
                    </h3>
                  </div>

                  <div className="rounded-2xl border bg-slate-50 p-4 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-md">
                    <p className="text-sm text-slate-500">
                      {t.observedExpenses}
                    </p>

                    <h3 className="text-2xl font-bold text-red-600 mt-1">
                      {formatMoney(
                        result.cashflow_forecast?.observed_expenses
                      )}
                    </h3>
                  </div>

                  <div className="rounded-2xl border bg-slate-50 p-4 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-md">
                    <p className="text-sm text-slate-500">
                      {t.observedNetCashflow}
                    </p>

                    <h3
                      className={`text-2xl font-bold mt-1 ${
                        (result.cashflow_forecast?.observed_net_cashflow || 0) >= 0
                          ? "text-green-600"
                          : "text-red-600"
                      }`}
                    >
                      {formatMoney(
                        result.cashflow_forecast?.observed_net_cashflow
                      )}
                    </h3>
                  </div>
                </div>

                <div className="rounded-2xl border bg-slate-50 p-5 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-md">
                  <p className="text-sm text-slate-500">
                    {t.financialHabitsScore}
                  </p>

                  <p className="text-xs text-slate-500 mt-1">
                    {t.deterministicScore}
                  </p>

                  <div className="mt-2 flex items-end gap-2">
                    <h3 className="text-4xl font-bold text-blue-600">
                      {result.financial_habit_scores?.overall_financial_habits_score ?? 0}
                    </h3>
                    <span className="text-slate-500 mb-1">/100</span>
                  </div>

                  <p className="text-sm text-slate-500 mt-2">
                    {t.savingBehavior}:{" "}
                    {result.financial_habit_scores?.saving_behavior ?? 0}/100
                  </p>

                  <p className="text-sm text-slate-500">
                    {t.subscriptionControl}:{" "}
                    {result.financial_habit_scores?.subscription_control ?? 0}/100
                  </p>
                </div>

                <div className="rounded-2xl border bg-slate-50 p-5 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-md">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-slate-500">
                        {t.cashflowForecast}
                      </p>

                      <h3
                        className={`text-2xl font-bold mt-1 ${
                          result.cashflow_forecast?.trend === "negative"
                            ? "text-red-600"
                            : result.cashflow_forecast?.trend === "risky"
                            ? "text-yellow-600"
                            : "text-green-600"
                        }`}
                      >
                        {translatedCashflowTrend}
                      </h3>
                    </div>

                    <div className="text-right">
                      <p className="text-sm text-slate-500">
                        {t.daysUntilRisk}
                      </p>

                      <p className="text-xl font-semibold">
                        {result.cashflow_forecast?.days_until_cash_risk ?? "-"}
                      </p>
                    </div>
                  </div>

                  <p className="text-sm text-slate-600 mt-4">
                    {translateBackendMessage(result.cashflow_forecast?.message)}
                  </p>
                </div>

                <div className="rounded-2xl border bg-slate-50 p-5 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-md">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-slate-500">
                        {t.recommendedBudget}
                      </p>

                      <h3 className="text-2xl font-bold text-slate-800 mt-1">
                        {translatedBudgetStatus}
                      </h3>
                    </div>

                    <div className="text-right">
                      <p className="text-sm text-slate-500">
                        {t.savingsTarget}
                      </p>

                      <p className="text-xl font-semibold text-green-600">
                        {formatMoney(
                          result.recommended_budget?.savings_target
                        )}
                      </p>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-5">
                    <div>
                      <p className="text-xs text-slate-500">
                        {t.needs}
                      </p>

                      <p className="font-semibold">
                        {formatMoney(
                          result.recommended_budget?.needs
                        )}
                      </p>
                    </div>

                    <div>
                      <p className="text-xs text-slate-500">
                        {t.wants}
                      </p>

                      <p className="font-semibold">
                        {formatMoney(
                          result.recommended_budget?.wants
                        )}
                      </p>
                    </div>

                    <div>
                      <p className="text-xs text-slate-500">
                        {t.emergencyFund}
                      </p>

                      <p className="font-semibold">
                        {formatMoney(
                          result.recommended_budget?.emergency_fund_target
                        )}
                      </p>
                    </div>

                    <div>
                      <p className="text-xs text-slate-500">
                        {t.safeSpending}
                      </p>

                      <p className="font-semibold">
                        {formatMoney(
                          result.recommended_budget?.max_safe_spending
                        )}
                      </p>
                    </div>
                  </div>

                  <p className="text-sm text-slate-600 mt-4">
                    {translateBackendMessage(result.recommended_budget?.message)}
                  </p>
                </div>

                <div className="rounded-2xl border bg-slate-50 p-5 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-md">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <p className="text-sm text-slate-500">
                        {t.detectedSubscriptions}
                      </p>

                      <h3 className="text-2xl font-bold text-slate-800 mt-1">
                        {result.subscriptions_detected?.length ?? 0}
                      </h3>
                    </div>

                    <div className="text-right">
                      <p className="text-sm text-slate-500">
                        {t.estimatedRecurringCharge}
                      </p>

                      <p className="text-xl font-semibold text-red-600">
                        {formatMoney(
                          result.financial_habit_scores?.metrics?.subscription_total
                        )}
                      </p>
                    </div>
                  </div>

                  {result.subscriptions_detected?.length > 0 ? (
                    <div className="space-y-3">
                      {result.subscriptions_detected.map(
                        (sub: any, index: number) => (
                          <div
                            key={index}
                            className="flex items-center justify-between rounded-xl border bg-white px-4 py-3 transition-all duration-300 hover:border-blue-200 hover:shadow-md"
                          >
                            <div>
                              <p className="font-medium">
                                {sub.name}
                              </p>

                              <p className="text-xs text-slate-500">
                                {sub.transactions_count} {t.transactions}
                              </p>
                            </div>

                            <div className="space-y-1 text-right">
                              <div className="font-semibold">
                                {t.averageCharge}: {formatMoney(sub.monthly_cost)}
                              </div>

                              <div className="text-sm text-slate-500">
                                {t.totalObserved}: {formatMoney(sub.total_observed_cost)}
                              </div>

                              <div className="text-sm text-slate-500">
                                {sub.transactions_count} {t.transactions}
                              </div>
                            </div>
                          </div>
                        )
                      )}
                    </div>
                  ) : (
                    <p className="text-sm text-slate-500">
                      {t.noRecurringSubscriptions}
                    </p>
                  )}
                </div>

                <div className="rounded-2xl border bg-slate-50 p-5 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-md">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <p className="text-sm text-slate-500">
                        {t.aiSavingsOpportunities}
                      </p>

                      <h3 className="text-2xl font-bold text-green-600 mt-1">
                        {formatMoney(
                          Number(
                            (result.savings_opportunities || []).reduce(
                              (sum: number, item: any) =>
                                sum + Number(item.estimated_savings_opportunity || 0),
                              0
                            ).toFixed(2)
                          )
                        )}
                      </h3>

                      <p className="text-xs text-slate-500 mt-1">
                        {t.estimatedSavingsOpportunity}
                      </p>
                    </div>

                    <span className="rounded-full bg-green-100 px-3 py-1 text-xs font-medium text-green-700">
                      {t.aiDetected}
                    </span>
                  </div>

                  {result.savings_opportunities?.length > 0 ? (
                    <div className="space-y-3">
                      {result.savings_opportunities.map(
                        (item: any, index: number) => (
                          <div
                            key={index}
                            className="rounded-xl border bg-white p-4 transition-all duration-300 hover:border-blue-200 hover:shadow-md"
                          >
                            <div className="flex items-start justify-between gap-4">
                              <div>
                                <p className="font-medium text-slate-800">
                                  {item.issue}
                                </p>

                                <p className="text-sm text-slate-500 mt-1">
                                  {item.recommendation}
                                </p>
                              </div>

                              <div className="text-right shrink-0">
                                <p className="font-semibold text-green-600">
                                  {formatMoney(item.estimated_savings_opportunity)}
                                </p>

                                <p className="text-xs text-slate-500">
                                  {t.savingsOpportunity}
                                </p>
                              </div>
                            </div>

                            <span
                              className={`mt-3 inline-flex rounded-full px-3 py-1 text-xs font-medium ${
                                item.severity === "high"
                                  ? "bg-red-100 text-red-700"
                                  : item.severity === "medium"
                                  ? "bg-yellow-100 text-yellow-700"
                                  : "bg-slate-100 text-slate-700"
                              }`}
                            >
                              {item.severity}
                            </span>
                          </div>
                        )
                      )}
                    </div>
                  ) : (
                    <p className="text-sm text-slate-500">
                      {t.noMajorSavingsOpportunities}
                    </p>
                  )}
                </div>

                <div className="rounded-2xl border bg-slate-50 p-5 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-md">
                  <div className="mb-4">
                    <p className="text-sm text-slate-500">
                      {t.aiFinancialInsights}
                    </p>

                    <h3 className="text-2xl font-bold text-slate-800 mt-1">
                      {t.smartMoneyCoach}
                    </h3>
                  </div>

                  {result.financial_insights?.length > 0 ? (
                    <div className="space-y-3">
                      {result.financial_insights.map(
                        (insight: any, index: number) => (
                          <div
                            key={index}
                            className={`rounded-xl border p-4 ${
                              insight.type === "positive"
                                ? "bg-green-50 border-green-200"
                                : insight.type === "warning"
                                ? "bg-red-50 border-red-200"
                                : "bg-blue-50 border-blue-200"
                            }`}
                          >
                            <div className="flex items-start gap-3">
                              <div className="text-xl">
                                {insight.type === "positive"
                                  ? "✅"
                                  : insight.type === "warning"
                                  ? "⚠️"
                                  : "💡"}
                              </div>

                              <div>
                                <p className="font-semibold text-slate-800">
                                  {translateInsightText(insight.title)}
                                </p>

                                <p className="text-sm text-slate-600 mt-1">
                                  {translateInsightText(insight.message)}
                                </p>
                              </div>
                            </div>
                          </div>
                        )
                      )}
                    </div>
                  ) : (
                    <p className="text-sm text-slate-500">
                      No AI insights available yet.
                    </p>
                  )}
                </div>

                {result.waste_detected?.length > 0 && (
                  <section className="rounded-2xl border bg-slate-50 p-5 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-md">
                    <h3 className="text-xl font-semibold mb-3">
                      {t.wasteDetected}
                    </h3>

                    <div className="space-y-2">
                      {result.waste_detected.map(
                        (item: string, i: number) => (
                          <p key={i} className="text-sm text-slate-700">
                            {translateBackendMessage(item)}
                          </p>
                        )
                      )}
                    </div>
                  </section>
                )}

                {result.saving_strategies?.length > 0 && (
                  <section className="rounded-2xl border bg-slate-50 p-5 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-md">
                    <h3 className="text-xl font-semibold mb-3">
                      {t.savingStrategies}
                    </h3>

                    <div className="space-y-2">
                      {result.saving_strategies.map(
                        (item: string, i: number) => (
                          <p key={i} className="text-sm text-slate-700">
                            {translateBackendMessage(item)}
                          </p>
                        )
                      )}
                    </div>
                  </section>
                )}

                {result.risk_notes?.length > 0 && (
                  <section className="rounded-2xl border bg-slate-50 p-5 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-md">
                    <h3 className="text-xl font-semibold mb-3">
                      {t.riskNotes}
                    </h3>

                    <div className="space-y-2">
                      {result.risk_notes.map(
                        (item: string, i: number) => (
                          <p key={i} className="text-sm text-slate-700">
                            {translateBackendMessage(item)}
                          </p>
                        )
                      )}
                    </div>
                  </section>
                )}

                <div className="rounded-2xl border bg-white p-5 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-md">
                  <div className="mb-4">
                    <p className="text-sm text-slate-500">
                      {t.spendingOverTime}
                    </p>

                    <h3 className="text-xl font-bold mt-1">
                      {t.expenseEvolution}
                    </h3>
                  </div>

                  <div className="h-80">
                    <ResponsiveContainer width="100%" height="100%">
                      <AreaChart
                        data={result.charts?.spending_over_time || []}
                      >
                        <defs>
                          <linearGradient
                            id="spendingGradient"
                            x1="0"
                            y1="0"
                            x2="0"
                            y2="1"
                          >
                            <stop
                              offset="5%"
                              stopColor="#2563eb"
                              stopOpacity={0.4}
                            />
                            <stop
                              offset="95%"
                              stopColor="#2563eb"
                              stopOpacity={0.05}
                            />
                          </linearGradient>
                        </defs>

                        <CartesianGrid
                          strokeDasharray="3 3"
                          vertical={false}
                        />

                        <XAxis dataKey="date" />

                        <YAxis />

                        <Tooltip />

                        <Area
                          type="monotone"
                          dataKey="amount"
                          stroke="#2563eb"
                          fillOpacity={1}
                          fill="url(#spendingGradient)"
                        />
                      </AreaChart>
                    </ResponsiveContainer>
                  </div>

                  <p className="mt-4 rounded-xl bg-slate-50 px-4 py-3 text-sm text-slate-600">
                    {t.chartInsightSpending}
                  </p>
                </div>

                <div className="rounded-2xl border bg-white p-5 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-md">
                  <div className="mb-4">
                    <p className="text-sm text-slate-500">
                      {t.observedNetCashflowOverTime}
                    </p>

                    <h3 className="text-xl font-bold mt-1">
                      {t.dailyCashflowTrend}
                    </h3>
                  </div>

                  <div className="h-80">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart
                        data={result.charts?.net_cashflow_over_time || []}
                      >
                        <CartesianGrid
                          strokeDasharray="3 3"
                          vertical={false}
                        />

                        <XAxis dataKey="date" />
                        <YAxis />
                        <Tooltip />

                        <Line
                          type="monotone"
                          dataKey="amount"
                          stroke="#16a34a"
                          strokeWidth={3}
                          dot
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>

                  <p className="mt-4 rounded-xl bg-slate-50 px-4 py-3 text-sm text-slate-600">
                    {t.chartInsightCashflow}
                  </p>
                </div>

                <div className="rounded-2xl border bg-white p-5 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-md">
                  <div className="mb-4">
                    <p className="text-sm text-slate-500">
                      {t.subscriptionGrowth}
                    </p>

                    <h3 className="text-xl font-bold mt-1">
                      {t.recurringSpendingTrend}
                    </h3>
                  </div>

                  {result.charts?.subscription_growth?.length > 0 ? (
                    <div className="h-80">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={result.charts.subscription_growth}>
                          <CartesianGrid
                            strokeDasharray="3 3"
                            vertical={false}
                          />

                          <XAxis dataKey="date" />
                          <YAxis />
                          <Tooltip />

                          <Bar
                            dataKey="amount"
                            fill="#f97316"
                            radius={[8, 8, 0, 0]}
                          />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  ) : (
                    <div className="flex h-80 items-center justify-center rounded-xl bg-slate-50 px-6 text-center text-sm text-slate-500">
                      {t.noRecurringSubscriptionSpending}
                    </div>
                  )}

                  <p className="mt-4 rounded-xl bg-slate-50 px-4 py-3 text-sm text-slate-600">
                    {t.chartInsightSubscriptions}
                  </p>
                </div>

                <div className="rounded-2xl border bg-white p-5 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-md">
                  <div className="mb-4">
                    <p className="text-sm text-slate-500">
                      {t.savingsEvolution}
                    </p>

                    <h3 className="text-xl font-bold mt-1">
                      {t.runningNetBalance}
                    </h3>
                  </div>

                  <div className="h-80">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart
                        data={result.charts?.savings_evolution || []}
                      >
                        <CartesianGrid
                          strokeDasharray="3 3"
                          vertical={false}
                        />

                        <XAxis dataKey="date" />
                        <YAxis />
                        <Tooltip />

                        <Line
                          type="monotone"
                          dataKey="amount"
                          stroke="#7c3aed"
                          strokeWidth={3}
                          dot
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>

                  <p className="mt-4 rounded-xl bg-slate-50 px-4 py-3 text-sm text-slate-600">
                    {t.chartInsightSavings}
                  </p>
                </div>

                <div>
                  <strong>{t.mainCategories}:</strong>

                  {chartData.length > 0 && (
                    <>
                      <div className="h-64 mt-4">
                        <ResponsiveContainer>
                          <PieChart>
                            <Pie
                              data={chartData}
                              dataKey="value"
                              nameKey="name"
                              outerRadius={80}
                            >
                              {chartData.map((entry, index) => (
                                <Cell
                                  key={index}
                                  fill={COLORS[index % COLORS.length]}
                                />
                              ))}
                            </Pie>
                            <Tooltip
                              formatter={(value) => formatMoney(value)}
                            />
                          </PieChart>
                        </ResponsiveContainer>
                      </div>

                      <div className="mt-4 overflow-hidden rounded-xl border">
                        <table className="w-full text-sm">
                          <tbody>
                            {chartData.map((item, index) => (
                              <tr
                                key={translateCategory(item.name)}
                                className="border-b last:border-b-0"
                              >
                                <td className="px-3 py-2">
                                  <div className="flex items-center gap-2">
                                    <span
                                      className="h-3 w-3 rounded-full shrink-0"
                                      style={{
                                        backgroundColor:
                                          COLORS[index % COLORS.length],
                                      }}
                                    />
                                    <span className="capitalize">
                                      {translateCategory(item.name)}
                                    </span>
                                  </div>
                                </td>
                                <td className="px-3 py-2 text-right font-semibold whitespace-nowrap">
                                  {formatMoney(item.value)}
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </>
                  )}
                </div>

                {result.waste_detected?.length > 0 && (
                  <div>
                    <strong>{t.wasteDetected}:</strong>
                    <ul className="list-disc ml-6 text-red-600">
                      {result.waste_detected.map(
                        (item: string, i: number) => (
                          <li key={i}>{item}</li>
                        )
                      )}
                    </ul>
                  </div>
                )}

                {result.saving_strategies?.length > 0 && (
                  <div>
                    <strong>{t.savingStrategies}:</strong>
                    <ul className="list-disc ml-6 text-green-600">
                      {result.saving_strategies.map(
                        (item: string, i: number) => (
                          <li key={i}>{item}</li>
                        )
                      )}
                    </ul>
                  </div>
                )}

                {result.risk_notes?.length > 0 && (
                  <div>
                    <strong>{t.riskNotes}:</strong>
                    <ul className="list-disc ml-6 text-amber-600">
                      {result.risk_notes.map(
                        (item: string, i: number) => (
                          <li key={i}>{item}</li>
                        )
                      )}
                    </ul>
                  </div>
                )}

                <div className="rounded-2xl border bg-white p-6 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-md">
                  <div className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                    <div>
                      <p className="text-sm text-slate-500">
                        {t.aiFinancialCoach}
                      </p>

                      <h3 className="text-2xl font-bold text-slate-800">
                        {t.askFinanceAssistant}
                      </h3>

                      <p className="mt-2 text-sm text-slate-500">
                        {t.coachSubtitle}
                      </p>
                    </div>

                    <span className="rounded-full bg-green-100 px-3 py-1 text-xs font-medium text-green-700">
                      {t.coachSecure}
                    </span>
                  </div>

                  <div className="flex flex-wrap gap-2 mb-5">
                    {quickQuestions.map((q) => (
                      <button
                        key={q}
                        onClick={() =>
                          sendFinanceQuestion(q)
                        }
                        className="rounded-full border px-3 py-2 text-sm transition-all duration-300 hover:border-blue-200 hover:bg-blue-50 hover:text-blue-700"
                      >
                        {q}
                      </button>
                    ))}
                  </div>

                  <div className="space-y-4 mb-5 max-h-[400px] overflow-y-auto">
                    {chatMessages.map(
                      (message, index) => (
                        <div
                          key={index}
                          className={`rounded-2xl p-4 ${
                            message.role === "user"
                              ? "bg-slate-100"
                              : "bg-blue-50 border border-blue-100"
                          }`}
                        >
                          <p className="text-sm font-semibold mb-1">
                            {message.role === "user"
                              ? "You"
                              : "Runexa AI"}
                          </p>

                          <div className="prose prose-sm max-w-none text-slate-700">
                            <ReactMarkdown>
                              {message.content}
                            </ReactMarkdown>
                          </div>
                        </div>
                      )
                    )}

                    {chatLoading && (
                      <div className="rounded-2xl bg-blue-50 border border-blue-100 p-4">
                        <p className="text-sm text-slate-500">
                          Runexa AI is thinking...
                        </p>
                      </div>
                    )}
                  </div>

                  {suggestedQuestions.length > 0 && (
                    <div className="mb-5">
                      <p className="text-xs uppercase tracking-wide text-slate-500 mb-2">
                        {t.suggestedFollowUpQuestions}
                      </p>

                      <div className="flex flex-wrap gap-2">
                        {suggestedQuestions.map((q, index) => (
                          <button
                            key={index}
                            onClick={() => sendFinanceQuestion(q)}
                            className="rounded-full bg-blue-50 border border-blue-200 px-3 py-2 text-sm text-blue-700 hover:bg-blue-100"
                          >
                            {q}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  <div className="flex gap-2">
                    <input
                      value={chatInput}
                      onChange={(e) =>
                        setChatInput(e.target.value)
                      }
                      onKeyDown={(e) => {
                        if (e.key === "Enter") {
                          sendFinanceQuestion();
                        }
                      }}
                      placeholder={t.chatPlaceholder}
                      className="flex-1 rounded-xl border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
                    />

                    <button
                      onClick={() =>
                        sendFinanceQuestion()
                      }
                      disabled={chatLoading}
                      className="rounded-xl bg-blue-600 px-5 py-3 text-white transition-all duration-300 hover:bg-blue-700 hover:shadow-md disabled:bg-blue-300 disabled:hover:shadow-none"
                    >
                      {t.send}
                    </button>
                  </div>
                </div>

                {result.disclaimer && (
                  <p className="text-xs text-slate-500 border-t pt-4">
                    {translateBackendMessage(result.disclaimer)}
                  </p>
                )}
                  </>
                )}
              </>
            )}
          </div>
        )}
      </div>
    </main>
  );
}