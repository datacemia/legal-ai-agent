"use client";

// RUNEXA_FINANCE_FRONTEND_VERSION v20b-limited-scope-truthful-ui-fixed

import { useEffect, useState } from "react";
import jsPDF from "jspdf";
import ReactMarkdown from "react-markdown";
import { analyzeFinanceStatement } from "../../lib/api";
import { startStripeCheckout } from "../../lib/stripeCheckout";
import { getSavedLocale, setSavedLocale } from "../../lib/i18n";
type Locale = "en" | "fr" | "ar";

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
    savings_investments: "Savings & investments",
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
    savings_investments: "Épargne et investissements",
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
    savings_investments: "الادخار والاستثمارات",
    transfers: "التحويلات",
    business_services: "الخدمات المهنية",
    cash: "السحب النقدي",
    other: "أخرى",
  },
};

const savingsOpportunityLabels: any = {
  "High spending detected": {
    en: "High spending detected",
    fr: "Dépenses élevées détectées",
    ar: "تم اكتشاف إنفاق مرتفع",
  },
  "Consider reducing discretionary spending to align expenses with income.": {
    en: "Consider reducing discretionary spending to align expenses with income.",
    fr: "Réduisez les dépenses non essentielles pour aligner vos dépenses avec vos revenus.",
    ar: "فكّر في تقليل المصاريف غير الأساسية لمواءمة الإنفاق مع الدخل.",
  },
};

const severityLabels: any = {
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
};



const groundedStrategyLabels: any = {
  en: {
    reviewObservedCategory:
      "Review {category} first; it is the largest specific observed spending category in this statement.",
    reviewObservedSpending:
      "Review the largest specific observed spending categories before making category-specific changes.",
  },
  fr: {
    reviewObservedCategory:
      "Examinez d’abord la catégorie {category} : c’est la plus importante catégorie de dépenses spécifique observée sur ce relevé.",
    reviewObservedSpending:
      "Examinez les principales catégories de dépenses spécifiques observées avant toute modification ciblée.",
  },
  ar: {
    reviewObservedCategory:
      "راجع أولًا فئة {category}، فهي أكبر فئة إنفاق محددة مرصودة في هذا الكشف.",
    reviewObservedSpending:
      "راجع أكبر فئات الإنفاق المحددة المرصودة قبل إجراء أي تعديل يستهدف فئة بعينها.",
  },
};


const groundedWasteLabels: any = {
  en: {
    neutral:
      "A potential savings signal was detected, but no specific merchant or spending category is sufficiently grounded to label as avoidable. Review the underlying transactions before acting.",
    observedMerchantEvidence:
      "Observed merchant references: {details}.",
  },
  fr: {
    neutral:
      "Un signal d’économie potentiel a été détecté, mais aucun marchand ni aucune catégorie de dépense n’est suffisamment étayé pour être qualifié d’évitable. Vérifiez les transactions concernées avant d’agir.",
    observedMerchantEvidence:
      "Références marchands observées : {details}.",
  },
  ar: {
    neutral:
      "تم رصد إشارة محتملة للتوفير، لكن لا يوجد تاجر أو فئة إنفاق محددة مدعومة بما يكفي لوصفها بأنها قابلة للتجنب. راجع المعاملات المعنية قبل اتخاذ أي إجراء.",
    observedMerchantEvidence:
      "مراجع التجار المرصودة: {details}.",
  },
};

const evidenceLabels: any = {
  en: {
    basedOnObservedActivity: "Based on observed activity",
    observedExpensesVsIncome:
      "Observed expenses {expenses} vs observed income {income}.",
    observedExpenseRatio:
      "Observed expenses represent approximately {ratio} of observed income.",
    observedNetCashflowEvidence: "Observed net cashflow: {cashflow}.",
    expensesExceedIncomeBy: "Observed expenses exceed observed income by {amount}.",
    savingsOpportunityEvidence: "Estimated savings opportunity: {amount}.",
    categoryEvidence:
      "{category}: {amount} across {count} observed transactions ({share} of observed expenses).",
    categoryEvidenceNoCount:
      "{category}: {amount} ({share} of observed expenses).",
    categoryEvidenceNoShare:
      "{category}: {amount} across {count} observed transactions.",
  },
  fr: {
    basedOnObservedActivity: "Basé sur l’activité observée",
    observedExpensesVsIncome:
      "Dépenses observées {expenses} contre revenus observés {income}.",
    observedExpenseRatio:
      "Les dépenses observées représentent environ {ratio} des revenus observés.",
    observedNetCashflowEvidence: "Trésorerie nette observée : {cashflow}.",
    expensesExceedIncomeBy: "Les dépenses observées dépassent les revenus observés de {amount}.",
    savingsOpportunityEvidence: "Opportunité d’épargne estimée : {amount}.",
    categoryEvidence:
      "{category} : {amount} sur {count} transactions observées ({share} des dépenses observées).",
    categoryEvidenceNoCount:
      "{category} : {amount} ({share} des dépenses observées).",
    categoryEvidenceNoShare:
      "{category} : {amount} sur {count} transactions observées.",
  },
  ar: {
    basedOnObservedActivity: "استنادًا إلى النشاط المرصود",
    observedExpensesVsIncome:
      "المصاريف المرصودة {expenses} مقابل الدخل المرصود {income}.",
    observedExpenseRatio:
      "تمثل المصاريف المرصودة حوالي {ratio} من الدخل المرصود.",
    observedNetCashflowEvidence: "صافي التدفق النقدي المرصود: {cashflow}.",
    expensesExceedIncomeBy: "تتجاوز المصاريف المرصودة الدخل المرصود بمقدار {amount}.",
    savingsOpportunityEvidence: "فرصة الادخار المقدرة: {amount}.",
    categoryEvidence:
      "{category}: {amount} عبر {count} معاملة مرصودة ({share} من المصاريف المرصودة).",
    categoryEvidenceNoCount:
      "{category}: {amount} ({share} من المصاريف المرصودة).",
    categoryEvidenceNoShare:
      "{category}: {amount} عبر {count} معاملة مرصودة.",
  },
};

const labels: any = {
  en: {
    title: "Financial Intelligence from Your Bank Statement",
    subtitle:
      "Turn a bank statement into a structured, evidence-based view of your finances.",
    heroSupport:
      "Runexa analyzes observed transactions to surface income, spending, cashflow, recurring activity, financial risks and savings opportunities — with reconciliation and quality controls built into the analysis.",
    heroStatement: "Understand your finances with evidence, not assumptions.",
    uploadBadges: ["Bank statement analysis", "Transaction reconciliation", "Private & multilingual"],
    whoTitle: "Who is this for?",
    whoItems: [
      "Individuals",
      "Freelancers",
      "Consultants",
      "Small business owners",
      "Startups",
    ],
    privacyTitle: "Your statements remain private",
    privacyItems: [
      "Secure processing",
      "No financial advice",
      "Encrypted storage",
      "User-controlled deletion",
    ],
    sampleIncomeLabel: "Monthly income",
    sampleDetectedLabel: "Detected",
    sampleAnnualSavingsLabel: "Potential annual savings",
    sampleSubscriptions: [
      ["Netflix", "$15.99"],
      ["Spotify", "$10.99"],
      ["Hostinger", "$19.99"],
    ],
    sampleAnnualSavings: "$564",
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
    trialInfo: "$1 trial per account. You can also skip the trial and continue with global credits or a Pro plan.",
    startTrial: "Start $1 trial",
    upgradePro: "Upgrade to Pro",
    trialUsed: "Your $1 trial has already been used on this account. You can continue with credits or a Pro plan.",
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
    cashRiskNow: "Cashflow risk detected now",
    noImmediateCashRisk: "No immediate cashflow risk detected",
    recommendedBudget: "Recommended Budget",
    savingsTarget: "Savings Target",
    needs: "Needs",
    wants: "Wants",
    emergencyFund: "Emergency Fund",
    safeSpending: "Safe Spending",
    estimatedRecurringCharge: "Estimated Recurring Charge",
    noRecurringSubscriptions: "No recurring subscriptions detected.",
    subscriptionCategoryNotRecurring:
      "Some spending may be categorized as subscriptions without enough recurrence evidence to confirm an active recurring subscription.",
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
    financeAnalysisLongerThanExpected: "Finance analysis is still processing. Please keep this page open or retry later.",
    aiNarrativeSummary: "AI Narrative Summary",
    aiGeneratedScore: "AI-generated overall finance score.",
    deterministicScore: "Deterministic score based on observed transactions.",
    limitedScopeTitle: "Limited analysis scope",
    limitedScopeScoreUnavailable: "Not enough data to calculate a reliable financial habits score.",
    limitedScopeBudgetUnavailable: "Not enough observed activity to generate a reliable recommended budget.",
    limitedScopeSubscriptionsUnavailable: "Not enough transaction history to assess recurring subscriptions reliably.",
    limitedScopeSavingsUnavailable: "Not enough observed activity to estimate savings opportunities reliably.",
    limitedScopeNotAssessed: "Not assessed",
    limitedScopeNotEnoughData: "Not enough data",
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
    confidenceLabel: "Confidence",
    noAiInsights: "{t.noAiInsights}",
    aiThinking: "{t.aiThinking}",
    assistantName: "Runexa AI",
    ocrRequiredTitle: "OCR required",
    ocrRequiredMessage: "This PDF is scanned or has no usable text layer. Please upload an exported PDF or process it with OCR before analysis.",
    verificationVerifiedTitle: "Analysis verified",
    verificationVerifiedMessage:
      "The extracted transactions are reconciled with the accounting evidence available in the statement.",
    verificationLedgerOnlyTitle: "Transactions reconciled",
    verificationLedgerOnlyMessage:
      "The extracted transaction ledger is reconciled, but statement-source consistency is not available. The analysis is not presented as fully verified.",
    confirmedRecurringSubscriptions: "Confirmed recurring subscriptions",
    categorizedSubscriptionSpend: "Spending categorized as subscriptions",
    verificationSourceConflictTitle:
      "Transactions reconciled — statement inconsistency detected",
    verificationSourceConflictMessage:
      "The extracted transaction ledger reconciles, but the statement's printed summary contains an internal accounting inconsistency. The statement is not presented as fully verified.",
    verificationUnverifiedTitle: "Analysis not verified",
    verificationUnverifiedMessage:
      "The extracted transactions could not be fully reconciled with the available accounting evidence in the statement.",
    verificationTransactions: "Transactions analyzed",
    verificationCurrency: "Currency",
    verificationConfidence: "Extraction confidence",
    verificationLedger: "Transaction ledger",
    verificationSource: "Statement source",
    verificationReconciled: "Reconciled",
    verificationInternallySupported: "Internally supported",
    verificationConsistent: "Consistent",
    verificationInconsistent: "Inconsistency detected",
    verificationUnavailable: "Not available",
    verificationAdvancedResultsWithheld:
      "Advanced financial indicators are not shown because the statement source contains an accounting inconsistency.",
    verificationRetryHint:
      "Review the extracted transactions and upload the original exported PDF if you need a fully verified analysis.",
    verificationSourceInconsistencyHint:
      "The statement was recognized, but its accounting evidence is internally inconsistent. Review the original statement or contact the issuing institution if needed.",
    verificationUnverifiedAnalysisAvailable:
      "Financial analysis is shown from the extracted transactions, but it is not fully verified.",
    verificationSourceInconsistentObservedAnalysis:
      "Analysis based on extracted transactions only — source statement contains an accounting inconsistency.",
    verificationSourceAlsoInconsistent:
      "The statement source also contains an internal accounting inconsistency.",
    qualityControls: "Quality controls",
    hideQualityControls: "Hide controls",
    checkStatementRecognized: "Statement recognized",
    checkTransactionsExtracted: "Transactions extracted",
    checkCurrencyDetected: "Currency detected",
    checkLedgerReconciled: "Transaction ledger status",
    checkSourceConsistent: "Statement source consistent",
    checkPassed: "Passed",
    checkWarning: "Warning",
    checkUnavailable: "Not available",
    viewTransactions: "View transactions",
    evidenceIncomeTitle: "Transactions behind observed income",
    evidenceExpensesTitle: "Transactions behind observed expenses",
    evidenceCashflowTitle: "Transactions used for observed net cashflow",
    evidenceDescription: "These are the statement transactions used by Runexa for this figure.",
    evidenceDate: "Date",
    evidenceTransaction: "Transaction",
    evidenceAmount: "Amount",
    evidenceTotal: "Observed total",
    close: "Close",
    categoryShare: "of observed expenses",
    coachEvidenceTitle: "Analysis context",
    coachEvidenceBasedOn: "This coach uses the current statement analysis",
    coachVerificationVerified: "Verified",
    coachVerificationWarning: "Source inconsistency flagged",
    coachVerificationLedgerOnly: "Transactions reconciled · Source unavailable",
    coachVerificationUnverified: "Not verified",
    coachTransactionsAnalyzed: "transactions analyzed",
    unsupportedDocumentTitle: "Statement format not supported yet",
    unsupportedDocumentMessage:
      "This statement format is not yet supported by the Finance Agent. No automatic analysis was generated to avoid inaccurate results. Support for this structure will be added in a future update.",
  },
  fr: {
    title: "L’intelligence financière à partir de votre relevé bancaire",
    subtitle:
      "Transformez un relevé bancaire en une vision structurée et fondée sur les données de votre situation financière.",
    heroSupport:
      "Runexa analyse les transactions observées pour identifier revenus, dépenses, trésorerie, opérations récurrentes, risques financiers et opportunités d’épargne, avec réconciliation et contrôles de qualité intégrés.",
    heroStatement: "Comprenez vos finances à partir des faits, pas des suppositions.",
    uploadBadges: ["Analyse de relevé bancaire", "Réconciliation des transactions", "Privé & multilingue"],
    whoTitle: "Pour qui ?",
    whoItems: [
      "Particuliers",
      "Freelances",
      "Consultants",
      "Petits entrepreneurs",
      "Startups",
    ],
    privacyTitle: "Vos relevés restent privés",
    privacyItems: [
      "Traitement sécurisé",
      "Aucun conseil financier",
      "Stockage chiffré",
      "Suppression contrôlée par l’utilisateur",
    ],
    sampleIncomeLabel: "Revenu mensuel",
    sampleDetectedLabel: "Détecté",
    sampleAnnualSavingsLabel: "Économies annuelles potentielles",
    sampleSubscriptions: [
      ["Netflix", "15,99 $"],
      ["Spotify", "10,99 $"],
      ["Hostinger", "19,99 $"],
    ],
    sampleAnnualSavings: "564 $",
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
    trialInfo: "Essai à 1$ par compte. Vous pouvez aussi passer directement aux crédits globaux ou au plan Pro.",
    startTrial: "Activer l’essai à 1$",
    upgradePro: "Passer au plan Pro",
    trialUsed: "Votre essai à 1 $ a déjà été utilisé pour ce compte. Vous pouvez continuer avec des crédits ou un abonnement Pro.",
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
    cashRiskNow: "Risque de trésorerie détecté maintenant",
    noImmediateCashRisk: "Aucun risque immédiat de trésorerie détecté",
    recommendedBudget: "Budget recommandé",
    savingsTarget: "Objectif d’épargne",
    needs: "Besoins",
    wants: "Envies",
    emergencyFund: "Fonds d’urgence",
    safeSpending: "Dépenses sûres",
    estimatedRecurringCharge: "Charge récurrente estimée",
    noRecurringSubscriptions: "Aucun abonnement récurrent détecté.",
    subscriptionCategoryNotRecurring:
      "Certaines dépenses peuvent être classées dans la catégorie « Abonnements » sans présenter suffisamment de récurrence pour confirmer un abonnement actif.",
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
    financeAnalysisLongerThanExpected: "L’analyse financière est toujours en cours. Gardez cette page ouverte ou réessayez plus tard.",
    aiNarrativeSummary: "Résumé narratif IA",
    aiGeneratedScore: "Score financier global généré par l’IA.",
    deterministicScore: "Score déterministe basé sur les transactions observées.",
    limitedScopeTitle: "Portée d’analyse limitée",
    limitedScopeScoreUnavailable: "Les données sont insuffisantes pour calculer un score fiable des habitudes financières.",
    limitedScopeBudgetUnavailable: "L’activité observée est insuffisante pour générer un budget recommandé fiable.",
    limitedScopeSubscriptionsUnavailable: "L’historique des transactions est insuffisant pour évaluer de façon fiable les abonnements récurrents.",
    limitedScopeSavingsUnavailable: "L’activité observée est insuffisante pour estimer de façon fiable les opportunités d’épargne.",
    limitedScopeNotAssessed: "Non évalué",
    limitedScopeNotEnoughData: "Données insuffisantes",
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
    confidenceLabel: "Confiance",
    noAiInsights: "Aucun insight IA disponible pour le moment.",
    aiThinking: "Runexa AI analyse votre question...",
    assistantName: "Runexa AI",
    ocrRequiredTitle: "OCR requis",
    ocrRequiredMessage: "Ce PDF est scanné ou ne contient pas de couche texte exploitable. Importez un PDF exporté ou traitez-le par OCR avant l’analyse.",
    verificationVerifiedTitle: "Analyse vérifiée",
    verificationVerifiedMessage:
      "Les transactions extraites sont réconciliées avec les éléments comptables disponibles dans le relevé.",
    verificationLedgerOnlyTitle: "Transactions réconciliées",
    verificationLedgerOnlyMessage:
      "Le ledger des transactions extraites est réconcilié, mais la cohérence du relevé source n’est pas disponible. L’analyse n’est pas présentée comme entièrement vérifiée.",
    confirmedRecurringSubscriptions: "Abonnements récurrents confirmés",
    categorizedSubscriptionSpend: "Dépenses classées comme abonnements",
    verificationSourceConflictTitle:
      "Transactions réconciliées — incohérence détectée dans le relevé",
    verificationSourceConflictMessage:
      "Le ledger des transactions extraites est réconcilié, mais le résumé imprimé du relevé contient une incohérence comptable interne. Le relevé n’est pas présenté comme entièrement vérifié.",
    verificationUnverifiedTitle: "Analyse non vérifiée",
    verificationUnverifiedMessage:
      "Les transactions extraites n’ont pas pu être entièrement réconciliées avec les éléments comptables disponibles dans le relevé.",
    verificationTransactions: "Transactions analysées",
    verificationCurrency: "Devise",
    verificationConfidence: "Confiance d’extraction",
    verificationLedger: "Ledger des transactions",
    verificationSource: "Relevé source",
    verificationReconciled: "Réconcilié",
    verificationInternallySupported: "Supporté en interne",
    verificationConsistent: "Cohérent",
    verificationInconsistent: "Incohérence détectée",
    verificationUnavailable: "Non disponible",
    verificationAdvancedResultsWithheld:
      "Les indicateurs financiers avancés ne sont pas affichés car le relevé source contient une incohérence comptable.",
    verificationRetryHint:
      "Vérifiez les transactions extraites et importez le PDF original exporté si vous avez besoin d’une analyse entièrement vérifiée.",
    verificationSourceInconsistencyHint:
      "Le relevé a été reconnu, mais ses éléments comptables présentent une incohérence interne. Vérifiez le relevé original ou contactez l’établissement émetteur si nécessaire.",
    verificationUnverifiedAnalysisAvailable:
      "L’analyse financière est affichée à partir des transactions extraites, mais elle n’est pas entièrement vérifiée.",
    verificationSourceInconsistentObservedAnalysis:
      "Analyse basée uniquement sur les transactions extraites — le relevé source contient une incohérence comptable.",
    verificationSourceAlsoInconsistent:
      "Le relevé source contient également une incohérence comptable interne.",
    qualityControls: "Contrôles de qualité",
    hideQualityControls: "Masquer les contrôles",
    checkStatementRecognized: "Relevé reconnu",
    checkTransactionsExtracted: "Transactions extraites",
    checkCurrencyDetected: "Devise détectée",
    checkLedgerReconciled: "Statut du ledger des transactions",
    checkSourceConsistent: "Cohérence du relevé source",
    checkPassed: "Validé",
    checkWarning: "Avertissement",
    checkUnavailable: "Non disponible",
    viewTransactions: "Voir les transactions",
    evidenceIncomeTitle: "Transactions à l’origine des revenus observés",
    evidenceExpensesTitle: "Transactions à l’origine des dépenses observées",
    evidenceCashflowTitle: "Transactions utilisées pour la trésorerie nette observée",
    evidenceDescription: "Voici les transactions du relevé utilisées par Runexa pour calculer ce montant.",
    evidenceDate: "Date",
    evidenceTransaction: "Transaction",
    evidenceAmount: "Montant",
    evidenceTotal: "Total observé",
    close: "Fermer",
    categoryShare: "des dépenses observées",
    coachEvidenceTitle: "Contexte de l’analyse",
    coachEvidenceBasedOn: "Ce coach utilise l’analyse en cours du relevé",
    coachVerificationVerified: "Vérifiée",
    coachVerificationWarning: "Incohérence source signalée",
    coachVerificationLedgerOnly: "Transactions réconciliées · Source non disponible",
    coachVerificationUnverified: "Non vérifié",
    coachTransactionsAnalyzed: "transactions analysées",
    unsupportedDocumentTitle: "Format de relevé non encore pris en charge",
    unsupportedDocumentMessage:
      "Ce format de relevé n’est pas encore pris en charge par l’agent Finance. Aucune analyse automatique n’a été générée afin d’éviter des résultats inexacts. Cette structure sera prise en charge dans une prochaine mise à jour.",
  },
  ar: {
    title: "ذكاء مالي مستند إلى كشف حسابك البنكي",
    subtitle:
      "حوّل كشف حسابك البنكي إلى رؤية مالية منظمة تستند إلى البيانات الفعلية.",
    heroSupport:
      "تحلل Runexa المعاملات المرصودة لاستخراج الدخل والمصاريف والتدفق النقدي والعمليات المتكررة والمخاطر المالية وفرص الادخار، مع مطابقة المعاملات وضوابط الجودة ضمن التحليل.",
    heroStatement: "افهم وضعك المالي استنادًا إلى الأدلة، لا الافتراضات.",
    uploadBadges: ["تحليل كشف الحساب", "مطابقة المعاملات", "خاص ومتعدد اللغات"],
    whoTitle: "لمن هذا الوكيل؟",
    whoItems: [
      "الأفراد",
      "العاملون المستقلون",
      "المستشارون",
      "أصحاب الأعمال الصغيرة",
      "الشركات الناشئة",
    ],
    privacyTitle: "تبقى كشوفاتك خاصة",
    privacyItems: [
      "معالجة آمنة",
      "ليست نصيحة مالية",
      "تخزين مشفّر",
      "حذف يتحكم به المستخدم",
    ],
    sampleIncomeLabel: "الدخل الشهري",
    sampleDetectedLabel: "تم اكتشاف",
    sampleAnnualSavingsLabel: "وفورات سنوية محتملة",
    sampleSubscriptions: [
      ["Netflix", "15.99 $"],
      ["Spotify", "10.99 $"],
      ["Hostinger", "19.99 $"],
    ],
    sampleAnnualSavings: "564 $",
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
    trialInfo: "تجربة واحدة بقيمة 1 دولار لكل حساب. يمكنك أيضاً المتابعة مباشرة بالأرصدة العامة أو خطة Pro.",
    startTrial: "تفعيل تجربة 1 دولار",
    upgradePro: "الترقية إلى Pro",
    trialUsed: "لقد تم استخدام تجربة 1 دولار الخاصة بهذا الحساب بالفعل. يمكنك المتابعة باستخدام الأرصدة أو الاشتراك في خطة Pro.",
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
    cashRiskNow: "تم اكتشاف خطر على التدفق النقدي الآن",
    noImmediateCashRisk: "لم يتم اكتشاف خطر فوري على التدفق النقدي",
    recommendedBudget: "الميزانية المقترحة",
    savingsTarget: "هدف الادخار",
    needs: "الاحتياجات",
    wants: "الرغبات",
    emergencyFund: "صندوق الطوارئ",
    safeSpending: "الإنفاق الآمن",
    estimatedRecurringCharge: "التكلفة المتكررة المقدرة",
    noRecurringSubscriptions: "لم يتم اكتشاف اشتراكات متكررة.",
    subscriptionCategoryNotRecurring:
      "قد تُصنَّف بعض المصاريف ضمن فئة الاشتراكات دون وجود تكرار كافٍ لتأكيد اشتراك نشط ومتكرر.",
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
    financeAnalysisLongerThanExpected: "لا يزال التحليل المالي قيد المعالجة. اترك هذه الصفحة مفتوحة أو أعد المحاولة لاحقاً.",
    aiNarrativeSummary: "ملخص سردي بالذكاء الاصطناعي",
    aiGeneratedScore: "نتيجة مالية عامة تم إنشاؤها بالذكاء الاصطناعي.",
    deterministicScore: "نتيجة حتمية مبنية على المعاملات المرصودة.",
    limitedScopeTitle: "نطاق تحليل محدود",
    limitedScopeScoreUnavailable: "لا توجد بيانات كافية لحساب درجة موثوقة للعادات المالية.",
    limitedScopeBudgetUnavailable: "النشاط المرصود غير كافٍ لإنشاء ميزانية مقترحة موثوقة.",
    limitedScopeSubscriptionsUnavailable: "سجل المعاملات غير كافٍ لتقييم الاشتراكات المتكررة بصورة موثوقة.",
    limitedScopeSavingsUnavailable: "النشاط المرصود غير كافٍ لتقدير فرص الادخار بصورة موثوقة.",
    limitedScopeNotAssessed: "لم يتم التقييم",
    limitedScopeNotEnoughData: "بيانات غير كافية",
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
    confidenceLabel: "مستوى الثقة",
    noAiInsights: "لا توجد رؤى ذكية متاحة حالياً.",
    aiThinking: "يقوم Runexa AI بتحليل سؤالك...",
    assistantName: "Runexa AI",
    ocrRequiredTitle: "يلزم التعرف الضوئي على الحروف",
    ocrRequiredMessage: "ملف PDF ممسوح ضوئياً أو لا يحتوي على طبقة نص قابلة للاستخدام. يرجى رفع ملف PDF مُصدّر أو معالجته بتقنية OCR قبل التحليل.",
    verificationVerifiedTitle: "تم التحقق من التحليل",
    verificationVerifiedMessage:
      "تمت مطابقة المعاملات المستخرجة مع الأدلة المحاسبية المتاحة في كشف الحساب.",
    verificationLedgerOnlyTitle: "تمت مطابقة المعاملات",
    verificationLedgerOnlyMessage:
      "تمت مطابقة سجل المعاملات المستخرجة، لكن التحقق من اتساق كشف الحساب المصدر غير متاح. لذلك لا يتم عرض التحليل على أنه متحقق منه بالكامل.",
    confirmedRecurringSubscriptions: "الاشتراكات المتكررة المؤكدة",
    categorizedSubscriptionSpend: "المصاريف المصنفة كاشتراكات",
    verificationSourceConflictTitle:
      "تمت مطابقة المعاملات — تم اكتشاف تناقض في كشف الحساب",
    verificationSourceConflictMessage:
      "تمت مطابقة سجل المعاملات المستخرجة، لكن الملخص المطبوع في كشف الحساب يحتوي على تناقض محاسبي داخلي. لذلك لا يتم عرض كشف الحساب على أنه متحقق منه بالكامل.",
    verificationUnverifiedTitle: "لم يتم التحقق من التحليل",
    verificationUnverifiedMessage:
      "تعذر مطابقة المعاملات المستخرجة بالكامل مع الأدلة المحاسبية المتاحة في كشف الحساب.",
    verificationTransactions: "المعاملات التي تم تحليلها",
    verificationCurrency: "العملة",
    verificationConfidence: "ثقة الاستخراج",
    verificationLedger: "سجل المعاملات",
    verificationSource: "كشف الحساب المصدر",
    verificationReconciled: "تمت المطابقة",
    verificationInternallySupported: "مدعوم داخليًا",
    verificationConsistent: "متسق",
    verificationInconsistent: "تم اكتشاف تناقض",
    verificationUnavailable: "غير متاح",
    verificationAdvancedResultsWithheld:
      "لا يتم عرض المؤشرات المالية المتقدمة لأن المعاملات المستخرجة لم تتم مطابقتها بالكامل.",
    verificationRetryHint:
      "راجع المعاملات المستخرجة وارفع ملف PDF الأصلي المُصدَّر إذا كنت تحتاج إلى تحليل متحقق منه بالكامل.",
    verificationSourceInconsistencyHint:
      "تم التعرف على كشف الحساب، لكن الأدلة المحاسبية فيه تتضمن تناقضًا داخليًا. راجع الكشف الأصلي أو تواصل مع الجهة المصدرة عند الحاجة.",
    verificationUnverifiedAnalysisAvailable:
      "يتم عرض التحليل المالي استنادًا إلى المعاملات المستخرجة، لكنه غير متحقق منه بالكامل.",
    verificationSourceInconsistentObservedAnalysis:
      "يعتمد التحليل فقط على المعاملات المستخرجة — يحتوي كشف الحساب المصدر على عدم اتساق محاسبي.",
    verificationSourceAlsoInconsistent:
      "يحتوي كشف الحساب المصدر أيضًا على تناقض محاسبي داخلي.",
    qualityControls: "ضوابط الجودة",
    hideQualityControls: "إخفاء الضوابط",
    checkStatementRecognized: "تم التعرف على كشف الحساب",
    checkTransactionsExtracted: "تم استخراج المعاملات",
    checkCurrencyDetected: "تم اكتشاف العملة",
    checkLedgerReconciled: "حالة سجل المعاملات",
    checkSourceConsistent: "اتساق كشف الحساب المصدر",
    checkPassed: "تم التحقق",
    checkWarning: "تنبيه",
    checkUnavailable: "غير متاح",
    viewTransactions: "عرض المعاملات",
    evidenceIncomeTitle: "المعاملات التي تكوّن الدخل المرصود",
    evidenceExpensesTitle: "المعاملات التي تكوّن المصاريف المرصودة",
    evidenceCashflowTitle: "المعاملات المستخدمة لصافي التدفق النقدي المرصود",
    evidenceDescription: "هذه هي معاملات كشف الحساب التي استخدمتها Runexa لحساب هذا المبلغ.",
    evidenceDate: "التاريخ",
    evidenceTransaction: "المعاملة",
    evidenceAmount: "المبلغ",
    evidenceTotal: "الإجمالي المرصود",
    close: "إغلاق",
    categoryShare: "من المصاريف المرصودة",
    coachEvidenceTitle: "سياق التحليل",
    coachEvidenceBasedOn: "يستخدم هذا المدرب التحليل الحالي لكشف الحساب",
    coachVerificationVerified: "تم التحقق",
    coachVerificationWarning: "تم التنبيه إلى تناقض في المصدر",
    coachVerificationLedgerOnly: "تمت مطابقة المعاملات · المصدر غير متاح",
    coachVerificationUnverified: "غير متحقق منه",
    coachTransactionsAnalyzed: "معاملة تم تحليلها",
    unsupportedDocumentTitle: "تنسيق كشف الحساب غير مدعوم حالياً",
    unsupportedDocumentMessage:
      "تنسيق كشف الحساب هذا غير مدعوم حالياً من قبل وكيل التحليل المالي. لم يتم إنشاء أي تحليل تلقائي لتجنب تقديم نتائج غير دقيقة. سيتم دعم هذه البنية في تحديث قادم.",
  },
};

const normalizeLocale = (
  value: string,
  fallback: Locale = "en"
): Locale => {
  if (value === "fr" || value === "ar" || value === "en") {
    return value;
  }

  return fallback;
};

const getClientLocale = (
  fallback: Locale = "en"
): Locale => {
  return normalizeLocale(getSavedLocale(), fallback);
};

export default function FinanceClient({
  initialLocale = "en",
  lockInitialLocale = false,
}: {
  initialLocale?: Locale;
  lockInitialLocale?: boolean;
}) {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [paymentMessage, setPaymentMessage] = useState("");
  const [language, setLanguage] = useState<Locale>(initialLocale);
  const [plan, setPlan] = useState("");
  const [role, setRole] = useState("");
  const [creditsBalance, setCreditsBalance] = useState(0);
  const [financeTrialPaid, setFinanceTrialPaid] = useState(false);
  const [financeTrialUsed, setFinanceTrialUsed] = useState(false);
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
  const [showVerificationDetails, setShowVerificationDetails] = useState(false);
  const [evidenceView, setEvidenceView] = useState<"income" | "expense" | "cashflow" | null>(null);

  useEffect(() => {
    if (lockInitialLocale) {
      setLanguage(initialLocale);
    } else {
      setLanguage(getClientLocale(initialLocale));
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
    refreshFinanceTrial();

    window.addEventListener("storage", syncBillingState);

    return () => {
      window.removeEventListener("storage", syncBillingState);
    };
  }, [initialLocale, lockInitialLocale]);

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

  const verificationStatus = String(
    result?.verification?.status || ""
  )
    .trim()
    .toLowerCase();

  const hasVerificationContract =
    Boolean(result?.verification) &&
    ["verified", "verified_with_source_inconsistency", "unverified"].includes(
      verificationStatus
    );

  const isVerificationVerified =
    verificationStatus === "verified" &&
    result?.verification?.accounting_reconciled === true &&
    result?.verification?.source_consistent === true &&
    result?.verification?.source_inconsistency_detected !== true;

  const isVerificationUnverified =
    hasVerificationContract &&
    verificationStatus === "unverified";

  const isVerificationSourceConflict =
    verificationStatus === "verified_with_source_inconsistency" &&
    result?.verification?.accounting_reconciled === true &&
    result?.verification?.source_inconsistency_detected === true;

  const isVerificationLedgerOnly =
    verificationStatus === "verified" &&
    result?.verification?.accounting_reconciled === true &&
    result?.verification?.source_consistent !== true &&
    result?.verification?.source_inconsistency_detected !== true;

  const shouldWithholdFinancialAnalysis =
    hasVerificationContract &&
    result?.verification?.analysis_withheld === true;

  // Frontend v20: suppressed analytics are not numeric zeroes.
  // Activate only on explicit backend limited-scope status.
  const isLimitedAnalysisScope =
    String(result?.recommended_budget?.status || "")
      .trim()
      .toLowerCase() === "limited_scope" ||
    String(result?.analysis_scope || "")
      .trim()
      .toLowerCase() === "limited_scope" ||
    result?.limited_analysis_scope === true;

  const coachVerificationStatusLabel = isVerificationSourceConflict
    ? t.coachVerificationWarning
    : isVerificationLedgerOnly
      ? t.coachVerificationLedgerOnly
      : isVerificationVerified
        ? t.coachVerificationVerified
        : t.coachVerificationUnverified;

  const verificationPresentation = isVerificationUnverified
    ? {
        tone: "neutral",
        title: t.verificationUnverifiedTitle,
        message: t.verificationUnverifiedMessage,
      }
    : isVerificationSourceConflict
    ? {
        tone: "warning",
        title: t.verificationSourceConflictTitle,
        message: t.verificationSourceConflictMessage,
      }
    : isVerificationLedgerOnly
    ? {
        tone: "neutral",
        title: t.verificationLedgerOnlyTitle,
        message: t.verificationLedgerOnlyMessage,
      }
    : isVerificationVerified
    ? {
        tone: "success",
        title: t.verificationVerifiedTitle,
        message: t.verificationVerifiedMessage,
      }
    : {
        tone: "neutral",
        title: t.verificationUnverifiedTitle,
        message: t.verificationUnverifiedMessage,
      };


  const isInsufficientData =
    result?.status === "insufficient_data" ||
    result?.analysis_status === "insufficient_data";

  const isOcrRequired =
    result?.status === "ocr_required" ||
    result?.analysis_status === "ocr_required" ||
    result?.reason === "scanned_pdf_requires_ocr";

  const isUnsupportedDocument =
    result?.status === "unsupported_document" ||
    result?.reason === "unsupported_statement_format" ||
    result?.reason === "no_transactions_extracted";

  const isRecognizedButUnreconciled =
    !hasVerificationContract &&
    (
      result?.status === "recognized_but_unreconciled" ||
      result?.analysis_status === "recognized_but_unreconciled" ||
      result?.reason === "source_statement_section_inconsistency" ||
      (
        result?.recognized === true &&
        result?.financial_authority === false
      )
    );


  const renderSafeText = (
    value: any,
    fallback = ""
  ): string => {
    if (value === null || value === undefined) return fallback;

    if (
      typeof value === "string" ||
      typeof value === "number" ||
      typeof value === "boolean"
    ) {
      return String(value);
    }

    // Never pass raw objects/arrays to React as children.
    return fallback;
  };


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

  const translateSavingsText = (value: any) => {
    if (typeof value !== "string") return value;

    return savingsOpportunityLabels[value]?.[language] || value;
  };


  const normalizeStrategySearchText = (value: unknown): string =>
    String(value || "")
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/[’']/g, "'");

  const canonicalStrategyCategory = (value: unknown): string => {
    const normalized = normalizeEvidenceCategory(value);

    const aliases: Record<string, string> = {
      cash_withdrawals: "cash",
      cash_withdrawal: "cash",
      atm: "cash",
      food_dining: "food",
      restaurants: "food",
      restaurant: "food",
      grocery: "groceries",
      debt_loans: "debt",
      loans: "debt",
      business_expenses: "business_operations",
      business_operations: "business_operations",
      government_taxes: "government_taxes",
      taxes: "government_taxes",
      savings_investments: "savings_investments",
    };

    return aliases[normalized] || normalized;
  };

  const strategyCategoryAliases: Record<string, string[]> = {
    shopping: [
      "shopping",
      "shop",
      "achats",
      "achat",
      "shopping et",
      "التسوق",
      "المشتريات",
    ],
    entertainment: [
      "entertainment",
      "leisure",
      "recreation",
      "divertissement",
      "divertissements",
      "loisirs",
      "الترفيه",
      "ترفيه",
    ],
    food: [
      "food",
      "dining",
      "restaurant",
      "restaurants",
      "nourriture",
      "repas",
      "restaurants et cafes",
      "المطاعم",
      "الطعام",
      "الأطعمة",
    ],
    groceries: [
      "groceries",
      "grocery",
      "courses",
      "supermarche",
      "البقالة",
    ],
    cash: [
      "cash withdrawal",
      "cash withdrawals",
      "atm",
      "retrait d'especes",
      "retraits d'especes",
      "السحب النقدي",
      "الصراف",
    ],
    housing: ["housing", "rent", "logement", "loyer", "السكن", "الإيجار"],
    utilities: [
      "utilities",
      "bills",
      "utility bills",
      "factures",
      "services et factures",
      "المرافق",
      "الفواتير",
    ],
    transport: ["transport", "transportation", "النقل"],
    travel: ["travel", "voyage", "السفر"],
    subscriptions: ["subscription", "subscriptions", "abonnement", "abonnements", "الاشتراكات"],
    fees: ["fees", "frais", "الرسوم"],
    debt: ["debt", "loan", "loans", "dette", "dettes", "pret", "prets", "الديون", "القروض"],
    business_operations: [
      "business expenses",
      "business expense",
      "depenses professionnelles",
      "مصاريف الاعمال",
      "مصاريف الأعمال",
    ],
    government_taxes: [
      "tax",
      "taxes",
      "impot",
      "impots",
      "taxe",
      "taxes",
      "الضرائب",
    ],
    healthcare: ["healthcare", "health", "sante", "الصحة"],
    insurance: ["insurance", "assurance", "التأمين"],
    education: ["education", "التعليم"],
  };

  const getStrategyMentionedCategories = (value: unknown): string[] => {
    const normalizedText = normalizeStrategySearchText(value);

    return Object.entries(strategyCategoryAliases)
      .filter(([, aliases]) =>
        aliases.some((alias) =>
          normalizedText.includes(normalizeStrategySearchText(alias))
        )
      )
      .map(([category]) => category);
  };

  const translateSeverity = (value: any) => {
    if (typeof value !== "string") return value;

    return severityLabels[value]?.[language] || value;
  };

  const hasPaidFinanceTrial = financeTrialPaid && !financeTrialUsed;

  const hasAccountAccess =
    role === "admin" ||
    role === "enterprise_admin" ||
    role === "enterprise_member" ||
    ["paid", "pro", "premium"].includes(plan) ||
    creditsBalance > 0;

  const hasActiveAccess = hasAccountAccess || hasPaidFinanceTrial;

  const trialActivatedMessage =
    language === "fr"
      ? "Essai Finance activé. Importez votre relevé et cliquez sur Analyser le relevé."
      : language === "ar"
      ? "تم تفعيل تجربة المالية. ارفع كشف الحساب ثم اضغط على تحليل الكشف."
      : "Finance trial activated. Upload your statement and click Analyze statement.";

  const getCheckoutErrorMessage = () => {
    if (language === "fr") {
      return "Impossible d’ouvrir la page de paiement Stripe. Veuillez réessayer.";
    }

    if (language === "ar") {
      return "تعذر فتح صفحة الدفع عبر Stripe. يرجى المحاولة مرة أخرى.";
    }

    return "Unable to start Stripe checkout. Please try again.";
  };

  const getFriendlyPaymentMessage = (error: any) => {
    const rawMessage = String(error?.message || "");

    if (
      rawMessage.includes("already been activated") ||
      rawMessage.includes("already activated") ||
      rawMessage.includes("already used") ||
      rawMessage.includes("$1 trial") ||
      rawMessage.includes("409")
    ) {
      return t.trialUsed;
    }

    if (rawMessage.includes("Unable to start checkout")) {
      return getCheckoutErrorMessage();
    }

    return rawMessage || getCheckoutErrorMessage();
  };

  const primaryCtaLabel = hasActiveAccess
    ? t.analyze
    : financeTrialUsed
    ? t.trialUsed
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

  const resolvedCurrency = String(
    result?.currency_detected || ""
  ).toUpperCase();

  const formatMoney = (value: any) => {
    const parsed = Number(value);
    const amount = Number.isFinite(parsed) ? parsed : 0;
    const locale = language === "ar" ? "ar" : language === "fr" ? "fr-FR" : "en-US";

    if (/^[A-Z]{3}$/.test(resolvedCurrency) && resolvedCurrency !== "UNKNOWN") {
      try {
        return new Intl.NumberFormat(locale, {
          style: "currency",
          currency: resolvedCurrency,
          currencyDisplay:
            resolvedCurrency === "GBP" && language === "fr"
              ? "narrowSymbol"
              : "symbol",
          minimumFractionDigits: 2,
          maximumFractionDigits: 2,
        }).format(amount);
      } catch {
        return `${amount.toLocaleString(locale, { minimumFractionDigits: 2, maximumFractionDigits: 2 })} ${resolvedCurrency}`;
      }
    }

    return amount.toLocaleString(locale, {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    });
  };


  const fillEvidenceTemplate = (
    template: string,
    values: Record<string, string | number>
  ) =>
    Object.entries(values).reduce(
      (output, [key, value]) =>
        output.replaceAll(`{${key}}`, String(value)),
      template
    );

  const normalizeEvidenceCategory = (value: any) =>
    String(value || "")
      .toLowerCase()
      .trim()
      .replace(/[\s&/]+/g, "_");

  const getObservedExpenseTotal = () => {
    const value = Number(result?.cashflow_forecast?.observed_expenses);
    return Number.isFinite(value) ? value : null;
  };

  const getObservedIncomeTotal = () => {
    const value = Number(result?.cashflow_forecast?.observed_income);
    return Number.isFinite(value) ? value : null;
  };

  const sourceEvidenceIsLimited =
    isVerificationSourceConflict || isVerificationLedgerOnly;

  const evidenceSensitiveCopy = {
    estimateBadge:
      language === "fr"
        ? "Estimation indicative"
        : language === "ar"
          ? "تقدير إرشادي"
          : "Indicative estimate",
    estimateNoteConflict:
      language === "fr"
        ? "À interpréter avec prudence : une incohérence a été détectée dans le relevé source."
        : language === "ar"
          ? "يُرجى تفسير هذا التقدير بحذر: تم اكتشاف عدم اتساق في كشف الحساب المصدر."
          : "Interpret with caution: an inconsistency was detected in the source statement.",
    estimateNoteUnavailable:
      language === "fr"
        ? "À interpréter avec prudence : la cohérence du relevé source n’est pas disponible."
        : language === "ar"
          ? "يُرجى تفسير هذا التقدير بحذر: التحقق من اتساق كشف الحساب المصدر غير متاح."
          : "Interpret with caution: statement-source consistency is unavailable.",
    budgetHeading:
      language === "fr"
        ? "Budget indicatif"
        : language === "ar"
          ? "ميزانية إرشادية"
          : "Indicative budget",
    savingsHeading:
      language === "fr"
        ? "Opportunités d’épargne indicatives"
        : language === "ar"
          ? "فرص ادخار إرشادية"
          : "Indicative savings opportunities",
  };

  const evidenceSensitiveNote = isVerificationSourceConflict
    ? evidenceSensitiveCopy.estimateNoteConflict
    : evidenceSensitiveCopy.estimateNoteUnavailable;

  const formatEvidenceShare = (value: number): string => {
    const locale =
      language === "fr" ? "fr-FR" : language === "ar" ? "ar" : "en-US";

    return new Intl.NumberFormat(locale, {
      style: "percent",
      minimumFractionDigits: 1,
      maximumFractionDigits: 1,
    }).format(value / 100);
  };

  const getCategoryEvidence = (category: any) => {
    if (!category) return null;

    const normalizedTarget = normalizeEvidenceCategory(category);
    const breakdown = Array.isArray(result?.charts?.category_breakdown)
      ? result.charts.category_breakdown
      : [];

    const match = breakdown.find(
      (entry: any) =>
        normalizeEvidenceCategory(entry?.category) === normalizedTarget
    );

    if (!match) return null;

    const amount = Number(match?.amount);
    if (!Number.isFinite(amount)) return null;

    const expenseTotal = getObservedExpenseTotal();
    const share =
      expenseTotal !== null && expenseTotal > 0
        ? Number(((Math.abs(amount) / expenseTotal) * 100).toFixed(1))
        : null;

    const transactions = Array.isArray(result?.transactions)
      ? result.transactions.filter(
          (transaction: any) =>
            transaction &&
            transaction.excluded_from_financial_kpis !== true &&
            transaction.exclude_from_cashflow !== true
        )
      : [];

    const count = transactions.filter(
      (transaction: any) =>
        normalizeEvidenceCategory(transaction?.category) === normalizedTarget
    ).length;

    const categoryLabel = translateCategory(match?.category || category);
    const localized = evidenceLabels[language] || evidenceLabels.en;

    if (count > 0 && share !== null) {
      return fillEvidenceTemplate(localized.categoryEvidence, {
        category: categoryLabel,
        amount: formatMoney(Math.abs(amount)),
        count,
        share: formatEvidenceShare(share),
      });
    }

    if (share !== null) {
      return fillEvidenceTemplate(localized.categoryEvidenceNoCount, {
        category: categoryLabel,
        amount: formatMoney(Math.abs(amount)),
        share: formatEvidenceShare(share),
      });
    }

    if (count > 0) {
      return fillEvidenceTemplate(localized.categoryEvidenceNoShare, {
        category: categoryLabel,
        amount: formatMoney(Math.abs(amount)),
        count,
      });
    }

    return null;
  };


  const confirmedRecurringSubscriptionCount = Array.isArray(
    result?.subscriptions_detected
  )
    ? result.subscriptions_detected.length
    : 0;

  const nonActionableStrategyCategories = new Set([
    "income",
    "other",
    "transfers",
    "savings",
    "savings_investments",
  ]);

  const observedActionableStrategyCategories = (
    Array.isArray(result?.charts?.category_breakdown)
      ? result.charts.category_breakdown
      : []
  )
    .map((entry: any) => {
      const amount = Number(entry?.amount);
      const canonical = canonicalStrategyCategory(entry?.category);

      return {
        rawCategory: entry?.category,
        canonical,
        amount: Number.isFinite(amount) ? Math.abs(amount) : 0,
      };
    })
    .filter(
      (entry: any) =>
        entry.amount > 0 &&
        entry.canonical &&
        !nonActionableStrategyCategories.has(entry.canonical) &&
        !(
          entry.canonical === "subscriptions" &&
          confirmedRecurringSubscriptionCount === 0
        )
    )
    .sort((a: any, b: any) => b.amount - a.amount);

  const observedActionableStrategySet = new Set(
    observedActionableStrategyCategories.map((entry: any) => entry.canonical)
  );

  const getTransactionSearchText = (transaction: any): string =>
    normalizeStrategySearchText(
      [
        transaction?.description,
        transaction?.merchant,
        transaction?.merchant_name,
        transaction?.name,
        transaction?.label,
        transaction?.raw_description,
      ]
        .filter(Boolean)
        .join(" ")
    );

  const observedTransactionSearchTexts = Array.isArray(result?.transactions)
    ? result.transactions
        .filter(
          (transaction: any) =>
            transaction &&
            transaction.excluded_from_financial_kpis !== true &&
            transaction.exclude_from_cashflow !== true
        )
        .map((transaction: any) => getTransactionSearchText(transaction))
    : [];

  const extractWasteMerchantExamples = (value: unknown): string[] => {
    const raw = String(value || "").trim();
    if (!raw) return [];

    const match = raw.match(
      /(?:\blike\b|\bsuch as\b|\bcomme\b|\btels?\s+que\b|مثل)\s+(.+?)(?:[.!؟]|$)/i
    );
    if (!match?.[1]) return [];

    return match[1]
      .split(/\s*(?:,|;)\s*|\s+(?:and|et|و)\s+/i)
      .map((item) => item.trim())
      .filter((item) => item.length >= 2 && item.length <= 80)
      .slice(0, 6);
  };

  const getObservedMerchantMatchCount = (merchant: string): number => {
    const normalizedMerchant = normalizeStrategySearchText(merchant);
    if (!normalizedMerchant) return 0;

    return observedTransactionSearchTexts.filter((textValue) =>
      textValue.includes(normalizedMerchant)
    ).length;
  };

  const normalizeNarrativeMoney = (value: unknown): string => {
    if (
      value === null ||
      value === undefined ||
      (typeof value !== "string" &&
        typeof value !== "number" &&
        typeof value !== "boolean")
    ) {
      return "";
    }

    const textValue = String(value);
    if (!textValue.trim()) return textValue;

    const locale =
      language === "fr" ? "fr-FR" : language === "ar" ? "ar" : "en-US";

    return textValue.replace(
      /(-?\d+(?:[.,]\d+)?)\s+(EUR|GBP|AUD|USD)\b/g,
      (match, rawAmount, currencyCode) => {
        const amount = Number(String(rawAmount).replace(",", "."));
        if (!Number.isFinite(amount)) return match;

        try {
          return new Intl.NumberFormat(locale, {
            style: "currency",
            currency: currencyCode,
            currencyDisplay:
              currencyCode === "GBP" && language === "fr"
                ? "narrowSymbol"
                : "symbol",
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
          }).format(amount);
        } catch {
          return match;
        }
      }
    );
  };


  const getGroundedWasteItem = (value: unknown) => {
    const translated = normalizeNarrativeMoney(
      translateBackendMessage(String(value || ""))
    );

    const merchants = extractWasteMerchantExamples(translated);
    if (merchants.length === 0) {
      return {
        text: translated,
        evidence: null as string | null,
        replaced: false,
      };
    }

    const merchantEvidence = merchants.map((merchant) => ({
      merchant,
      count: getObservedMerchantMatchCount(merchant),
    }));

    const allSupported = merchantEvidence.every((item) => item.count > 0);
    const localized = groundedWasteLabels[language] || groundedWasteLabels.en;

    if (!allSupported) {
      return {
        text: localized.neutral,
        evidence: null as string | null,
        replaced: true,
      };
    }

    const details = merchantEvidence
      .map((item) => `${item.merchant} (${item.count})`)
      .join(language === "ar" ? "، " : ", ");

    return {
      text: translated,
      evidence: fillEvidenceTemplate(
        localized.observedMerchantEvidence,
        { details }
      ),
      replaced: false,
    };
  };

  const getGroundedSavingStrategy = (value: unknown) => {
    const translated = normalizeNarrativeMoney(
      translateBackendMessage(String(value || ""))
    );

    const mentionedCategories = getStrategyMentionedCategories(translated);
    const unsupportedCategories = mentionedCategories.filter(
      (category) => !observedActionableStrategySet.has(category)
    );

    const firstSupportedMention = mentionedCategories.find((category) =>
      observedActionableStrategySet.has(category)
    );

    const supportedObservedEntry = firstSupportedMention
      ? observedActionableStrategyCategories.find(
          (entry: any) => entry.canonical === firstSupportedMention
        )
      : null;

    // If a strategy names an absent/non-actionable category, never display
    // that unsupported claim. Replace it with a neutral strategy grounded in
    // the largest specific observed category.
    if (unsupportedCategories.length > 0) {
      const topObserved = observedActionableStrategyCategories[0] || null;
      const localized =
        groundedStrategyLabels[language] || groundedStrategyLabels.en;

      if (!topObserved) {
        return {
          text: localized.reviewObservedSpending,
          evidence: null as string | null,
          replaced: true,
        };
      }

      return {
        text: fillEvidenceTemplate(localized.reviewObservedCategory, {
          category: translateCategory(topObserved.rawCategory),
        }),
        evidence: getCategoryEvidence(topObserved.rawCategory),
        replaced: true,
      };
    }

    // If the backend strategy names a category that really exists, keep the
    // original strategy and attach factual evidence for that category.
    if (supportedObservedEntry) {
      return {
        text: translated,
        evidence: getCategoryEvidence(supportedObservedEntry.rawCategory),
        replaced: false,
      };
    }

    // General strategies that do not assert a category remain unchanged.
    return {
      text: translated,
      evidence: null as string | null,
      replaced: false,
    };
  };

  const totalSavingsOpportunity = Number(
    (result?.savings_opportunities || [])
      .reduce(
        (sum: number, item: any) =>
          sum + Number(item?.estimated_savings_opportunity || 0),
        0
      )
      .toFixed(2)
  );


  const groundedWasteItems = (() => {
    const backendItems = Array.isArray(result?.waste_detected)
      ? result.waste_detected
      : [];

    if (backendItems.length > 0) {
      return backendItems.map((item: unknown) => getGroundedWasteItem(item));
    }

    // Preserve the section only when there is a real positive savings signal.
    // Do not invent a waste merchant/category when the backend provides none.
    if (totalSavingsOpportunity > 0) {
      const localized =
        groundedWasteLabels[language] || groundedWasteLabels.en;

      return [
        {
          text: localized.neutral,
          evidence: null as string | null,
          replaced: true,
        },
      ];
    }

    return [];
  })();

  const groundedSavingStrategies = (() => {
    const backendItems = Array.isArray(result?.saving_strategies)
      ? result.saving_strategies
      : [];

    if (backendItems.length > 0) {
      return backendItems.map((item: unknown) =>
        getGroundedSavingStrategy(item)
      );
    }

    // If a savings opportunity exists but no backend strategy survived,
    // provide one neutral strategy grounded in the largest specific observed
    // actionable category. Never use Other/Transfers/Income/Savings.
    if (totalSavingsOpportunity > 0) {
      const localized =
        groundedStrategyLabels[language] || groundedStrategyLabels.en;
      const topObserved = observedActionableStrategyCategories[0] || null;

      if (!topObserved) {
        return [
          {
            text: localized.reviewObservedSpending,
            evidence: null as string | null,
            replaced: true,
          },
        ];
      }

      return [
        {
          text: fillEvidenceTemplate(localized.reviewObservedCategory, {
            category: translateCategory(topObserved.rawCategory),
          }),
          evidence: getCategoryEvidence(topObserved.rawCategory),
          replaced: true,
        },
      ];
    }

    return [];
  })();

  const getCashflowEvidence = () => {
    const expenses = getObservedExpenseTotal();
    const income = getObservedIncomeTotal();

    if (expenses === null || income === null) return null;

    return fillEvidenceTemplate(
      (evidenceLabels[language] || evidenceLabels.en)
        .observedExpensesVsIncome,
      {
        expenses: formatMoney(expenses),
        income: formatMoney(income),
      }
    );
  };


  const getExpenseShortfallEvidence = () => {
    const expenses = getObservedExpenseTotal();
    const income = getObservedIncomeTotal();

    if (expenses === null || income === null || expenses <= income) {
      return null;
    }

    return fillEvidenceTemplate(
      (evidenceLabels[language] || evidenceLabels.en).expensesExceedIncomeBy,
      {
        amount: formatMoney(expenses - income),
      }
    );
  };

  const getExpenseRatioEvidence = () => {
    const expenses = getObservedExpenseTotal();
    const income = getObservedIncomeTotal();

    if (
      expenses === null ||
      income === null ||
      !Number.isFinite(income) ||
      income <= 0
    ) {
      return null;
    }

    const ratio = Number(((expenses / income) * 100).toFixed(1));

    return fillEvidenceTemplate(
      (evidenceLabels[language] || evidenceLabels.en).observedExpenseRatio,
      {
        ratio: formatEvidenceShare(ratio),
        expenses: formatMoney(expenses),
        income: formatMoney(income),
      }
    );
  };

  const getSavingsEvidence = (item: any) => {
    // Use an explicit backend category when available.
    // Do not infer a category or merchant from recommendation wording.
    const categoryEvidence = getCategoryEvidence(
      item?.category || item?.expense_category
    );

    if (categoryEvidence) return categoryEvidence;

    // High-spending recommendations can still be explained using the
    // already-calculated observed expense and income totals.
    if (
      String(item?.issue || "").toLowerCase() ===
        "high spending detected" ||
      String(item?.severity || "").toLowerCase() === "high"
    ) {
      return getCashflowEvidence();
    }

    return null;
  };

  type FinanceInsightConcept =
    | "cashflow"
    | "savings_opportunity"
    | "expense_ratio"
    | "savings_capacity"
    | "subscriptions"
    | "financial_habits"
    | "other";

  const getInsightConcept = (
    titleValue: unknown,
    messageValue: unknown = ""
  ): FinanceInsightConcept => {
    const searchable = normalizeStrategySearchText(
      `${String(titleValue || "")} ${String(messageValue || "")}`
    );

    const hasAny = (terms: string[]) =>
      terms.some((term) =>
        searchable.includes(normalizeStrategySearchText(term))
      );

    if (
      hasAny([
        "cashflow",
        "cash flow",
        "negative cashflow",
        "trésorerie",
        "flux de trésorerie",
        "تدفق نقدي",
        "التدفق النقدي",
      ])
    ) {
      return "cashflow";
    }

    if (
      hasAny([
        "savings opportunities",
        "saving opportunities",
        "savings opportunity",
        "opportunités d’économies",
        "opportunités d'economies",
        "opportunités d’épargne",
        "opportunités d'epargne",
        "فرص للتوفير",
        "فرص الادخار",
        "فرص توفير",
      ])
    ) {
      return "savings_opportunity";
    }

    if (
      hasAny([
        "expense ratio",
        "expenses consume",
        "spending level",
        "moderate spending",
        "ratio de dépenses",
        "niveau de dépenses",
        "dépenses consomment",
        "نسبة المصاريف",
        "نسبة مصاريف",
        "مستوى الإنفاق",
        "المصاريف تستهلك",
      ])
    ) {
      return "expense_ratio";
    }

    if (
      hasAny([
        "savings capacity",
        "limited savings capacity",
        "excellent savings capacity",
        "capacité d’épargne",
        "capacité d'epargne",
        "قدرة محدودة على الادخار",
        "قدرة الادخار",
      ])
    ) {
      return "savings_capacity";
    }

    if (
      hasAny([
        "subscription",
        "subscriptions",
        "abonnement",
        "abonnements",
        "اشتراك",
        "الاشتراكات",
      ])
    ) {
      return "subscriptions";
    }

    if (
      hasAny([
        "financial habits",
        "habits need improvement",
        "habitudes financières",
        "habitudes financieres",
        "العادات المالية",
      ])
    ) {
      return "financial_habits";
    }

    return "other";
  };

  const shouldHideInsightAsDuplicate = (insight: any): boolean => {
    const concept = getInsightConcept(insight?.title, insight?.message);

    // Dedicated Cashflow Forecast card already states the status/risk.
    if (concept === "cashflow" && result?.cashflow_forecast) {
      return true;
    }

    // Dedicated AI Savings Opportunities card already states the amount.
    if (
      concept === "savings_opportunity" &&
      Array.isArray(result?.savings_opportunities)
    ) {
      return true;
    }

    // Dedicated subscription card already owns subscription-control messaging.
    if (concept === "subscriptions" && result?.subscriptions) {
      return true;
    }

    return false;
  };

  const visibleFinancialInsights = Array.isArray(result?.financial_insights)
    ? result.financial_insights.filter(
        (insight: any) => !shouldHideInsightAsDuplicate(insight)
      )
    : [];

  const visibleInsightConcepts = new Set<FinanceInsightConcept>(
    visibleFinancialInsights.map((insight: any) =>
      getInsightConcept(insight?.title, insight?.message)
    )
  );

  const shouldHideRiskNoteAsDuplicate = (note: unknown): boolean => {
    const concept = getInsightConcept(note);

    // Cashflow status is already explicit in the dedicated forecast card.
    if (concept === "cashflow" && result?.cashflow_forecast) {
      return true;
    }

    // Savings opportunities have their own card.
    if (
      concept === "savings_opportunity" &&
      Array.isArray(result?.savings_opportunities)
    ) {
      return true;
    }

    // Financial Habits Score already communicates overall habit quality.
    if (concept === "financial_habits" && result?.financial_habit_scores) {
      return true;
    }

    // If the same concept is already explained by a visible Smart Money
    // Coach insight, avoid repeating it again as a risk note.
    if (
      concept !== "other" &&
      visibleInsightConcepts.has(concept)
    ) {
      return true;
    }

    return false;
  };

  const visibleRiskNotes = Array.isArray(result?.risk_notes)
    ? result.risk_notes.filter(
        (note: unknown) => !shouldHideRiskNoteAsDuplicate(note)
      )
    : [];

  const getInsightEvidence = (insight: any) => {
    const categoryEvidence = getCategoryEvidence(
      insight?.category || insight?.expense_category
    );
    if (categoryEvidence) return categoryEvidence;

    const title = String(insight?.title || "").toLowerCase();
    const message = String(insight?.message || "").toLowerCase();
    const searchable = `${title} ${message}`;
    const localized = evidenceLabels[language] || evidenceLabels.en;

    const includesAny = (terms: string[]) =>
      terms.some((term) => searchable.includes(term));

    const isExpenseRatioInsight = includesAny([
      "expense ratio",
      "expenses consume",
      "moderate spending",
      "spending level",
      "spending is moderate",
      "ratio de dépenses",
      "dépenses consomment",
      "niveau de dépenses",
      "dépenses sont modérées",
      "نسبة مصاريف",
      "نسبة المصاريف",
      "المصاريف تستهلك",
      "مستوى الإنفاق",
      "الإنفاق معتدل",
    ]);

    if (isExpenseRatioInsight) {
      return getExpenseRatioEvidence();
    }

    const isSavingsOpportunityInsight = includesAny([
      "savings opportunities",
      "saving opportunities",
      "opportunités d’économies",
      "opportunités d'économies",
      "opportunités d’épargne",
      "opportunités d'épargne",
      "فرص للتوفير",
      "فرص الادخار",
      "فرص توفير",
    ]);

    if (isSavingsOpportunityInsight) {
      if (
        Number.isFinite(totalSavingsOpportunity) &&
        totalSavingsOpportunity > 0
      ) {
        return fillEvidenceTemplate(localized.savingsOpportunityEvidence, {
          amount: formatMoney(totalSavingsOpportunity),
        });
      }
      return null;
    }

    const isCashflowInsight = includesAny([
      "cashflow",
      "cash flow",
      "trésorerie",
      "flux de trésorerie",
      "تدفق نقدي",
      "التدفق النقدي",
    ]);

    if (isCashflowInsight) {
      const net = Number(result?.cashflow_forecast?.observed_net_cashflow);
      if (Number.isFinite(net)) {
        return fillEvidenceTemplate(localized.observedNetCashflowEvidence, {
          cashflow: formatMoney(net),
        });
      }
      return getCashflowEvidence();
    }

    const isLimitedSavingsCapacityInsight = includesAny([
      "limited savings capacity",
      "limited room for savings",
      "savings capacity",
      "capacité d’épargne limitée",
      "capacité d'epargne limitée",
      "marge limitée pour l’épargne",
      "marge limitée pour l'epargne",
      "قدرة محدودة على الادخار",
      "مجالًا محدودًا للادخار",
      "مجالا محدودا للادخار",
    ]);

    if (isLimitedSavingsCapacityInsight) {
      return getExpenseShortfallEvidence() || getCashflowEvidence();
    }

    return null;
  };

  const chartData =
    result?.charts?.category_breakdown?.map((item: any) => {
      const canonical = canonicalStrategyCategory(item?.category);
      const isUnconfirmedSubscriptionCategory =
        canonical === "subscriptions" &&
        confirmedRecurringSubscriptionCount === 0;

      return {
        name: isUnconfirmedSubscriptionCategory
          ? t.categorizedSubscriptionSpend
          : translateCategory(item.category),
        value: Number(item.amount),
      };
    }) || [];


  const usableTransactions = Array.isArray(result?.transactions)
    ? result.transactions.filter(
        (tx: any) =>
          tx &&
          tx.excluded_from_financial_kpis !== true &&
          tx.exclude_from_cashflow !== true
      )
    : [];

  const incomeEvidenceTransactions = usableTransactions.filter(
    (tx: any) => String(tx?.type || "").toLowerCase() === "income"
  );

  const expenseEvidenceTransactions = usableTransactions.filter(
    (tx: any) => String(tx?.type || "").toLowerCase() === "expense"
  );

  const cashflowEvidenceTransactions = usableTransactions.filter((tx: any) =>
    ["income", "expense"].includes(String(tx?.type || "").toLowerCase())
  );

  const getEvidenceTransactions = () => {
    if (evidenceView === "income") return incomeEvidenceTransactions;
    if (evidenceView === "expense") return expenseEvidenceTransactions;
    if (evidenceView === "cashflow") return cashflowEvidenceTransactions;
    return [];
  };

  const getEvidenceTitle = () => {
    if (evidenceView === "income") return t.evidenceIncomeTitle;
    if (evidenceView === "expense") return t.evidenceExpensesTitle;
    return t.evidenceCashflowTitle;
  };

  const getEvidenceTotal = () => {
    const rows = getEvidenceTransactions();

    return rows.reduce((sum: number, tx: any) => {
      const signedCandidate = Number(tx?.signed_amount);
      const amountCandidate = Number(tx?.amount);
      const value = Number.isFinite(signedCandidate)
        ? signedCandidate
        : Number.isFinite(amountCandidate)
        ? amountCandidate
        : 0;

      const txType = String(tx?.type || "").toLowerCase();

      if (evidenceView === "income") {
        return sum + Math.abs(value);
      }

      if (evidenceView === "expense") {
        return sum + Math.abs(value);
      }

      if (evidenceView === "cashflow") {
        if (txType === "expense") return sum - Math.abs(value);
        if (txType === "income") return sum + Math.abs(value);
      }

      return sum + value;
    }, 0);
  };

  const formatEvidenceDate = (value: any) => {
    if (!value) return "-";
    const parsed = new Date(String(value));
    if (Number.isNaN(parsed.getTime())) return String(value);
    const locale =
      language === "ar" ? "ar" : language === "fr" ? "fr-FR" : "en-US";
    return new Intl.DateTimeFormat(locale, {
      day: "2-digit",
      month: "short",
      year: "numeric",
    }).format(parsed);
  };

  const formatChartDate = (value: any) => {
    if (!value) return "";
    const parsed = new Date(String(value));
    if (Number.isNaN(parsed.getTime())) return String(value);

    const locale =
      language === "ar" ? "ar" : language === "fr" ? "fr-FR" : "en-US";

    return new Intl.DateTimeFormat(locale, {
      day: "2-digit",
      month: "short",
    }).format(parsed);
  };

  const makeDedupedChartDateFormatter = () => {
    let previousLabel = "";

    return (value: any) => {
      const label = formatChartDate(value);
      if (label === previousLabel) return "";
      previousLabel = label;
      return label;
    };
  };

  const buildSparseDateTicks = (rows: any[], maxTicks = 7) => {
    if (!Array.isArray(rows) || rows.length === 0) return undefined;

    const uniqueDates = Array.from(
      new Set(
        rows
          .map((row: any) => row?.date)
          .filter((value: any) => Boolean(value))
      )
    );

    if (uniqueDates.length <= maxTicks) return uniqueDates;

    const lastIndex = uniqueDates.length - 1;
    const selected: any[] = [];

    for (let i = 0; i < maxTicks; i += 1) {
      const index = Math.round((i * lastIndex) / (maxTicks - 1));
      const value = uniqueDates[index];
      if (!selected.includes(value)) selected.push(value);
    }

    return selected;
  };

  const formatChartTooltipDate = (value: any) => {
    if (!value) return "";
    const parsed = new Date(String(value));
    if (Number.isNaN(parsed.getTime())) return String(value);

    const locale =
      language === "ar" ? "ar" : language === "fr" ? "fr-FR" : "en-US";

    return new Intl.DateTimeFormat(locale, {
      day: "2-digit",
      month: "short",
      year: "numeric",
    }).format(parsed);
  };

  const formatChartAxisAmount = (value: any) => {
    const amount = Number(value);
    if (!Number.isFinite(amount)) return String(value ?? "");

    const locale =
      language === "ar" ? "ar" : language === "fr" ? "fr-FR" : "en-US";

    return new Intl.NumberFormat(locale, {
      notation: "compact",
      maximumFractionDigits: 1,
    }).format(amount);
  };

  const cashflowTrend = String(
    result?.cashflow_forecast?.trend || ""
  ).toLowerCase();

  const cashRiskDays = Number(
    result?.cashflow_forecast?.days_until_cash_risk
  );

  const showCashRiskCountdown =
    ["negative", "risky"].includes(cashflowTrend) &&
    Number.isFinite(cashRiskDays) &&
    cashRiskDays > 0;

  const showImmediateCashRisk =
    ["negative", "risky"].includes(cashflowTrend) &&
    Number.isFinite(cashRiskDays) &&
    cashRiskDays <= 0;

  const showNoImmediateCashRisk =
    !["negative", "risky"].includes(cashflowTrend);

  const totalCategorySpend = chartData.reduce(
    (sum: number, item: any) =>
      sum + (Number.isFinite(Number(item.value)) ? Number(item.value) : 0),
    0
  );


  const subscriptionCategorySpend = Array.isArray(
    result?.charts?.category_breakdown
  )
    ? result.charts.category_breakdown.reduce((sum: number, item: any) => {
        const category = String(item?.category || "").toLowerCase().trim();
        const amount = Number(item?.amount);

        if (
          ["subscriptions", "subscription"].includes(category) &&
          Number.isFinite(amount)
        ) {
          return sum + Math.abs(amount);
        }

        return sum;
      }, 0)
    : 0;

  const hasSubscriptionCategoryWithoutConfirmedRecurring =
    subscriptionCategorySpend > 0 &&
    confirmedRecurringSubscriptionCount === 0;


  const translatedCashflowTrend =
    trendLabels[language]?.[result?.cashflow_forecast?.trend] ??
    result?.cashflow_forecast?.trend ??
    "unknown";

  const translatedBudgetStatus =
    budgetLabels[language]?.[result?.recommended_budget?.status] ??
    result?.recommended_budget?.status ??
    "unknown";

  const quickQuestions = isLimitedAnalysisScope
    ? [t.chatBiggestExpenses, t.chatSaveMoreMoney]
    : [
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

  const refreshFinanceTrial = async () => {
    const token = safeGetLocalStorage("token");

    if (!token) return;

    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/payments/trial-status/finance`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!res.ok) return;

      const data = await res.json();

      setFinanceTrialPaid(Boolean(data.trial_paid));
      setFinanceTrialUsed(Boolean(data.trial_used));
    } catch (error) {
      console.error("Could not refresh finance trial status:", error);
    }
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

        // Finance jobs are processed asynchronously by the worker.
        // Large scanned statements can legitimately require more than 6 minutes.
        const maxPollingAttempts = 900;
        const pollingIntervalMs = 2000;

        while (attempts < maxPollingAttempts && !completed) {
          await new Promise((resolve) =>
            setTimeout(resolve, pollingIntervalMs)
          );

          const statusResponse = await fetch(
            `${API_URL}/jobs/${currentJobId}?timestamp=${Date.now()}`,
            {
              method: "GET",
              cache: "no-store",
              headers: {
                Accept: "application/json",
                ...(token
                  ? {
                      Authorization: `Bearer ${token}`,
                    }
                  : {}),
                "Cache-Control": "no-cache, no-store, must-revalidate",
                Pragma: "no-cache",
              },
            }
          );

          const responseText = await statusResponse.text();

          let statusData: any = null;

          try {
            statusData = responseText ? JSON.parse(responseText) : null;
          } catch {
            throw new Error(
              `Invalid finance job response (${statusResponse.status})`
            );
          }

          if (!statusResponse.ok) {
            throw new Error(
              statusData?.detail ||
                statusData?.error ||
                t.couldNotCheckFinanceStatus
            );
          }

          const normalizedStatus = String(statusData?.status || "")
            .trim()
            .toLowerCase();

          console.log("FINANCE_JOB_STATUS", {
            requestedJobId: currentJobId,
            response: statusData,
          });

          setJobId(statusData?.id || currentJobId);
          setJobStatus(normalizedStatus);

          if (typeof statusData?.progress === "number") {
            setLoadingProgress(statusData.progress);
          }

          if (statusData?.status_message) {
            setLoadingStep(
              typeof statusData.status_message === "string"
                ? statusData.status_message
                : t.queued
            );
          }

          if (normalizedStatus === "completed") {
            if (!statusData?.result) {
              throw new Error(
                `Job ${currentJobId} completed without a result.`
              );
            }

            data = statusData.result;
            completed = true;
            break;
          }

          if (normalizedStatus === "failed") {
            throw new Error(
              statusData?.error ||
                statusData?.detail ||
                t.financeAnalysisFailed
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
      await refreshFinanceTrial();
    } catch (error) {
      console.error("Finance analysis failed", {
        error,
        jobId,
        jobStatus,
        apiUrl: process.env.NEXT_PUBLIC_API_URL,
      });

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

  const handlePrimaryCta = async () => {
    setPaymentMessage("");

    if (hasActiveAccess) {
      await handleAnalyze();
      return;
    }

    if (financeTrialUsed) {
      setPaymentMessage(t.trialUsed);
      return;
    }

    try {
      await startStripeCheckout("trial", {
        agent_slug: "finance",
      });
    } catch (error: any) {
      await refreshFinanceTrial();
      setPaymentMessage(getFriendlyPaymentMessage(error));
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
    doc.text(
      isLimitedAnalysisScope
        ? `${t.financialHabitsScore}: ${t.limitedScopeNotAssessed}`
        : `${t.financialHabitsScore}: ${result.financial_habit_scores?.overall_financial_habits_score ?? "-"}/100`,
      14,
      y
    );

    addLine(12);
    doc.setFontSize(13);
    doc.text(t.aiSavingsOpportunities, 14, y);

    addLine(8);
    doc.setFontSize(10);

    (result.savings_opportunities || []).forEach((item: any) => {
      doc.text(
        `${normalizeNarrativeMoney(translateSavingsText(item.issue))}: ${t.estimatedSavingsOpportunity} ${formatMoney(item.estimated_savings_opportunity)}`,
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
        <section className="rounded-3xl border border-slate-200 bg-white px-6 py-10 text-center shadow-sm sm:px-10 sm:py-12">
          <h1 className="mx-auto max-w-3xl text-4xl font-bold tracking-tight text-slate-950 sm:text-5xl">
            {t.title}
          </h1>

          <p className="mx-auto mt-5 max-w-2xl text-lg leading-8 text-slate-600">
            {t.subtitle}
          </p>

          <p className="mx-auto mt-4 max-w-3xl text-sm leading-6 text-slate-500">
            {t.heroSupport}
          </p>

          <p className="mx-auto mt-6 max-w-2xl text-sm font-semibold text-slate-900">
            {t.heroStatement}
          </p>

          <div className="mt-7 flex flex-wrap justify-center gap-2">
            {t.uploadBadges.map((badge: string) => (
              <span
                key={badge}
                className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1.5 text-xs font-medium text-slate-600"
              >
                {badge}
              </span>
            ))}
          </div>
        </section>

        <div className="bg-gradient-to-b from-white to-slate-50/80 p-6 rounded-2xl border space-y-4 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-md">
          <div className="rounded-xl bg-slate-50 border border-slate-200 p-4 text-sm text-slate-600 space-y-2 transition-all duration-300 hover:border-blue-200 hover:bg-white hover:shadow-md">
            <p>
              <strong>{t.howTitle}</strong> {t.how1}
            </p>
            <p>{t.how2}</p>
            <p className="text-xs text-slate-500">{t.disclaimer}</p>
          </div>

          <select
            value={language}
            onChange={(e) => {
              if (lockInitialLocale) {
                return;
              }

              const nextLocale = normalizeLocale(e.target.value, initialLocale);

              setLanguage(nextLocale);
              setSavedLocale(nextLocale);
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

          {hasPaidFinanceTrial && !hasAccountAccess && (
            <div className="rounded-xl border border-green-100 bg-green-50 p-3 text-sm text-green-700">
              {trialActivatedMessage}
            </div>
          )}

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <button
              onClick={handlePrimaryCta}
              disabled={
                hasActiveAccess
                  ? !file || loading
                  : loading || financeTrialUsed
              }
              className="w-full rounded-xl bg-slate-900 py-3 text-white transition-all duration-300 hover:bg-slate-800 hover:shadow-xl disabled:bg-slate-400 disabled:hover:shadow-none"
            >
              {loading ? t.analyzing : primaryCtaLabel}
            </button>

            <button
              onClick={async () => {
                try {
                  await startStripeCheckout("credits_pack", {
                    pack: "starter",
                  });
                } catch (error: any) {
                  setPaymentMessage(getFriendlyPaymentMessage(error));
                }
              }}
              className="w-full rounded-xl border border-slate-300 bg-white py-3 text-slate-800 transition-all duration-300 hover:border-blue-200 hover:bg-slate-50 hover:shadow-md"
            >
              <span className="flex items-center justify-center gap-2">
                {t.buyCredits}
              </span>
            </button>

            <button
              onClick={async () => {
                try {
                  await startStripeCheckout("subscription");
                } catch (error: any) {
                  setPaymentMessage(getFriendlyPaymentMessage(error));
                }
              }}
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

            {!isUnsupportedDocument &&
              !isOcrRequired &&
              !isRecognizedButUnreconciled &&
              !result.detail && (
              <button
                onClick={exportFinanceReportPdf}
                className="rounded-xl bg-slate-900 px-4 py-2 text-sm font-medium text-white transition-all duration-300 hover:bg-slate-800 hover:shadow-md"
              >
                {t.exportPdf}
              </button>
            )}

            {result.detail ? (
              <p className="text-red-600">
                {typeof result.detail === "string"
                  ? result.detail
                  : JSON.stringify(result.detail)}
              </p>
            ) : isRecognizedButUnreconciled ? (
              <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5">
                <p className="text-sm font-semibold text-amber-900">
                  {language === "fr"
                    ? "Analyse non disponible pour ce relevé"
                    : language === "ar"
                    ? "التحليل غير متاح لهذا الكشف"
                    : "Analysis unavailable for this statement"}
                </p>

                <p className="mt-2 text-sm leading-7 text-amber-800">
                  {language === "fr"
                    ? "Les données extraites ne permettent pas de produire une analyse financière suffisamment fiable. Aucun résultat automatique n’a été généré afin d’éviter de présenter des informations inexactes."
                    : language === "ar"
                    ? "لا تسمح البيانات المستخرجة بإنتاج تحليل مالي بدرجة كافية من الموثوقية. لم يتم إنشاء نتائج تلقائية لتجنب عرض معلومات غير دقيقة."
                    : "The extracted data is not reliable enough to produce a financial analysis. No automatic results were generated to avoid presenting inaccurate information."}
                </p>

                <p className="mt-3 text-xs text-amber-700">
                  {language === "fr"
                    ? "Vous pouvez réessayer avec le PDF original exporté depuis votre espace bancaire."
                    : language === "ar"
                    ? "يمكنك إعادة المحاولة باستخدام ملف PDF الأصلي المُصدَّر من حسابك البنكي."
                    : "You can retry with the original PDF exported from your banking portal."}
                </p>
              </div>
            ) : isOcrRequired ? (
              <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5">
                <p className="text-sm font-semibold text-amber-900">
                  {t.ocrRequiredTitle}
                </p>
                <p className="mt-2 text-sm leading-7 text-amber-800">
                  {renderSafeText(result.message, t.ocrRequiredMessage)}
                </p>
              </div>
            ) : isUnsupportedDocument ? (
              <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5">
                <p className="text-sm font-semibold text-amber-900">
                  {t.unsupportedDocumentTitle}
                </p>

                <p className="mt-2 text-sm leading-7 text-amber-800">
                  {t.unsupportedDocumentMessage}
                </p>
              </div>
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
                      {typeof result.message === "string"
                        ? result.message
                        : language === "fr"
                        ? "Les données extraites ne permettent pas de produire une analyse suffisamment fiable."
                        : language === "ar"
                        ? "البيانات المستخرجة غير كافية لإنتاج تحليل موثوق."
                        : "The extracted data is insufficient to produce a reliable analysis."}
                    </p>

                    <p className="mt-3 text-xs text-amber-700">
                      {t.confidenceLabel}: {result.confidence ?? result.analysis_quality?.confidence ?? 25}%
                    </p>
                  </div>
                ) : (
                  <>
                    {hasVerificationContract && (
                      <div
                        className={`rounded-2xl border p-5 ${
                          verificationPresentation.tone === "success"
                            ? "border-emerald-200 bg-emerald-50"
                            : verificationPresentation.tone === "warning"
                            ? "border-amber-200 bg-amber-50"
                            : "border-slate-200 bg-slate-50"
                        }`}
                        dir={language === "ar" ? "rtl" : "ltr"}
                      >
                        <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                          <div>
                            <div className="flex items-center gap-2">
                              <span
                                className={`inline-flex h-7 w-7 items-center justify-center rounded-full text-sm font-bold ${
                                  verificationPresentation.tone === "success"
                                    ? "bg-emerald-100 text-emerald-700"
                                    : verificationPresentation.tone === "warning"
                                    ? "bg-amber-100 text-amber-700"
                                    : "bg-slate-200 text-slate-700"
                                }`}
                                aria-hidden="true"
                              >
                                {verificationPresentation.tone === "success"
                                  ? "✓"
                                  : verificationPresentation.tone === "warning"
                                  ? "!"
                                  : "i"}
                              </span>

                              <p
                                className={`text-sm font-semibold ${
                                  verificationPresentation.tone === "success"
                                    ? "text-emerald-900"
                                    : verificationPresentation.tone === "warning"
                                    ? "text-amber-900"
                                    : "text-slate-900"
                                }`}
                              >
                                {verificationPresentation.title}
                              </p>
                            </div>

                            <p
                              className={`mt-2 text-sm leading-7 ${
                                verificationPresentation.tone === "success"
                                  ? "text-emerald-800"
                                  : verificationPresentation.tone === "warning"
                                  ? "text-amber-800"
                                  : "text-slate-700"
                              }`}
                            >
                              {verificationPresentation.message}
                            </p>
                          </div>

                          {typeof result?.verification?.confidence === "number" &&
                            !(
                              shouldWithholdFinancialAnalysis &&
                              Number(result.verification.confidence) <= 0
                            ) && (
                            <span
                              className={`shrink-0 rounded-full px-3 py-1 text-xs font-medium ${
                                verificationPresentation.tone === "success"
                                  ? "bg-emerald-100 text-emerald-800"
                                  : verificationPresentation.tone === "warning"
                                  ? "bg-amber-100 text-amber-800"
                                  : "bg-slate-200 text-slate-700"
                              }`}
                            >
                              {t.verificationConfidence}:{" "}
                              {result.verification.confidence}%
                            </span>
                          )}
                        </div>

                        <div className="mt-4 grid grid-cols-2 gap-3 lg:grid-cols-4">
                          <div className="rounded-xl bg-white/70 p-3">
                            <p className="text-xs text-slate-500">
                              {shouldWithholdFinancialAnalysis
                                ? t.checkTransactionsExtracted
                                : t.verificationTransactions}
                            </p>
                            <p className="mt-1 text-sm font-semibold text-slate-900">
                              {shouldWithholdFinancialAnalysis
                                ? (
                                    result?.verification?.extracted_transaction_count ??
                                    result?.verification?.transaction_count ??
                                    "-"
                                  )
                                : (result?.verification?.transaction_count ?? "-")}
                            </p>
                          </div>

                          <div className="rounded-xl bg-white/70 p-3">
                            <p className="text-xs text-slate-500">
                              {t.verificationCurrency}
                            </p>
                            <p className="mt-1 text-sm font-semibold text-slate-900">
                              {(() => {
                                const verificationCurrency = String(
                                  result?.verification?.currency || ""
                                ).trim();
                                const detectedCurrency = String(
                                  result?.currency_detected || ""
                                ).trim();

                                if (
                                  verificationCurrency &&
                                  verificationCurrency.toUpperCase() !== "UNKNOWN"
                                ) {
                                  return verificationCurrency;
                                }

                                if (
                                  detectedCurrency &&
                                  detectedCurrency.toUpperCase() !== "UNKNOWN"
                                ) {
                                  return detectedCurrency;
                                }

                                return t.verificationUnavailable;
                              })()}
                            </p>
                          </div>

                          <div className="rounded-xl bg-white/70 p-3">
                            <p className="text-xs text-slate-500">
                              {t.verificationLedger}
                            </p>
                            <p className="mt-1 text-sm font-semibold text-slate-900">
                              {result?.verification?.ledger_status === "reconciled" ||
                              result?.verification?.accounting_reconciled === true
                                ? t.verificationReconciled
                                : result?.verification?.ledger_status ===
                                  "internally_supported"
                                ? t.verificationInternallySupported
                                : t.verificationUnavailable}
                            </p>
                          </div>

                          <div className="rounded-xl bg-white/70 p-3">
                            <p className="text-xs text-slate-500">
                              {t.verificationSource}
                            </p>
                            <p className="mt-1 text-sm font-semibold text-slate-900">
                              {result?.verification?.source_inconsistency_detected === true
                                ? t.verificationInconsistent
                                : result?.verification?.source_consistent === true
                                ? t.verificationConsistent
                                : t.verificationUnavailable}
                            </p>
                          </div>
                        </div>

                        <div className="mt-4 border-t border-black/5 pt-4">
                          <button
                            type="button"
                            onClick={() =>
                              setShowVerificationDetails((current) => !current)
                            }
                            className="text-xs font-semibold text-slate-700 underline decoration-slate-300 underline-offset-4 transition hover:text-slate-950"
                          >
                            {showVerificationDetails
                              ? t.hideQualityControls
                              : t.qualityControls}
                          </button>

                          {showVerificationDetails && (
                            <div className="mt-3 grid gap-2 text-sm sm:grid-cols-2">
                              {[
                                {
                                  label: t.checkStatementRecognized,
                                  value:
                                    result?.verification?.checks
                                      ?.statement_recognized === true,
                                },
                                {
                                  label: t.checkTransactionsExtracted,
                                  value:
                                    result?.verification?.checks
                                      ?.transactions_extracted === true,
                                },
                                {
                                  label: t.checkCurrencyDetected,
                                  value:
                                    result?.verification?.checks
                                      ?.currency_detected === true,
                                },
                                {
                                  label: t.checkLedgerReconciled,
                                  value:
                                    result?.verification?.checks
                                      ?.ledger_reconciled === true ||
                                    result?.verification?.checks
                                      ?.accounting_reconciled === true,
                                  warning:
                                    result?.verification?.ledger_status ===
                                    "internally_supported",
                                  warningLabel: t.verificationInternallySupported,
                                },
                              ].map((check) => (
                                <div
                                  key={check.label}
                                  className="flex items-center justify-between gap-3 rounded-xl bg-white/70 px-3 py-2"
                                >
                                  <span className="text-slate-600">
                                    {check.label}
                                  </span>
                                  <span
                                    className={`font-semibold ${
                                      check.value
                                        ? "text-emerald-700"
                                        : check.warning
                                        ? "text-amber-700"
                                        : "text-slate-600"
                                    }`}
                                  >
                                    {check.value
                                      ? `✓ ${t.checkPassed}`
                                      : check.warning
                                      ? `! ${check.warningLabel}`
                                      : t.checkUnavailable}
                                  </span>
                                </div>
                              ))}

                              <div className="flex items-center justify-between gap-3 rounded-xl bg-white/70 px-3 py-2 sm:col-span-2">
                                <span className="text-slate-600">
                                  {t.checkSourceConsistent}
                                </span>
                                <span
                                  className={`font-semibold ${
                                    result?.verification
                                      ?.source_inconsistency_detected === true
                                      ? "text-amber-700"
                                      : result?.verification?.source_consistent ===
                                        true
                                      ? "text-emerald-700"
                                      : "text-slate-600"
                                  }`}
                                >
                                  {result?.verification
                                    ?.source_inconsistency_detected === true
                                    ? `! ${t.checkWarning}`
                                    : result?.verification?.source_consistent ===
                                      true
                                    ? `✓ ${t.checkPassed}`
                                    : t.checkUnavailable}
                                </span>
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    )}

                    {shouldWithholdFinancialAnalysis ? (
                      <div
                        className="rounded-2xl border border-slate-200 bg-slate-50 p-5"
                        dir={language === "ar" ? "rtl" : "ltr"}
                      >
                        <p className="text-sm font-semibold text-slate-900">
                          {t.verificationUnverifiedTitle}
                        </p>
                        <p className="mt-2 text-sm leading-7 text-slate-700">
                          {t.verificationAdvancedResultsWithheld}
                        </p>
                        <p className="mt-2 text-sm leading-7 text-amber-700">
                          {t.verificationSourceAlsoInconsistent}
                        </p>
                        <p className="mt-3 text-xs leading-6 text-slate-500">
                          {t.verificationSourceInconsistencyHint}
                        </p>
                      </div>
                    ) : (
                      <>
                        {isVerificationUnverified &&
                          result?.verification?.analysis_available_unverified === true && (
                            <div
                              className="mb-4 rounded-2xl border border-amber-200 bg-amber-50 p-4"
                              dir={language === "ar" ? "rtl" : "ltr"}
                            >
                              <p className="text-sm font-semibold text-amber-900">
                                {t.verificationUnverifiedTitle}
                              </p>
                              <p className="mt-1 text-sm leading-6 text-amber-800">
                                {result?.verification?.source_inconsistent_observed_analysis === true
                                  ? t.verificationSourceInconsistentObservedAnalysis
                                  : t.verificationUnverifiedAnalysisAvailable}
                              </p>
                              {result?.verification?.source_inconsistent_observed_analysis === true && (
                                <p className="mt-2 text-xs font-medium leading-5 text-amber-900">
                                  {t.verificationSourceAlsoInconsistent}
                                </p>
                              )}
                              {typeof result?.verification?.max_direction_gap_ratio === "number" && (
                                <p className="mt-2 text-xs leading-5 text-amber-700">
                                  {language === "fr"
                                    ? `Écart comptable observé : ${(result.verification.max_direction_gap_ratio * 100).toFixed(3)} % du flux officiel concerné.`
                                    : language === "ar"
                                    ? `الفارق المحاسبي المرصود: ${(result.verification.max_direction_gap_ratio * 100).toFixed(3)}٪ من التدفق الرسمي المعني.`
                                    : `Observed accounting gap: ${(result.verification.max_direction_gap_ratio * 100).toFixed(3)}% of the affected official flow.`}
                                </p>
                              )}
                            </div>
                          )}

                        <div className="rounded-2xl border bg-blue-50 p-5">
                  <p className="text-sm text-blue-700">
                    {t.aiNarrativeSummary}
                  </p>
                  <p className="mt-2 text-sm leading-7 text-slate-700">
                    {normalizeNarrativeMoney(renderSafeText(result.summary, "-"))}
                  </p>
                </div>

                <p>
                  <strong>{t.currency}:</strong>{" "}
                  {renderSafeText(result.currency_detected, t.unknown)}
                </p>

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
                    {incomeEvidenceTransactions.length > 0 && (
                      <button
                        type="button"
                        onClick={() => setEvidenceView("income")}
                        className="mt-3 text-xs font-semibold text-blue-700 underline decoration-blue-200 underline-offset-4 hover:text-blue-900"
                      >
                        {t.viewTransactions} ({incomeEvidenceTransactions.length})
                      </button>
                    )}
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
                    {expenseEvidenceTransactions.length > 0 && (
                      <button
                        type="button"
                        onClick={() => setEvidenceView("expense")}
                        className="mt-3 text-xs font-semibold text-blue-700 underline decoration-blue-200 underline-offset-4 hover:text-blue-900"
                      >
                        {t.viewTransactions} ({expenseEvidenceTransactions.length})
                      </button>
                    )}
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
                    {cashflowEvidenceTransactions.length > 0 && (
                      <button
                        type="button"
                        onClick={() => setEvidenceView("cashflow")}
                        className="mt-3 text-xs font-semibold text-blue-700 underline decoration-blue-200 underline-offset-4 hover:text-blue-900"
                      >
                        {t.viewTransactions} ({cashflowEvidenceTransactions.length})
                      </button>
                    )}
                  </div>
                </div>

                <div className="rounded-2xl border bg-slate-50 p-5 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-md">
                  <p className="text-sm text-slate-500">
                    {t.financialHabitsScore}
                  </p>

                  {isLimitedAnalysisScope ? (
                    <div className="mt-3">
                      <h3 className="text-2xl font-bold text-slate-700">
                        {t.limitedScopeNotEnoughData}
                      </h3>
                      <p className="mt-2 text-sm leading-6 text-slate-500">
                        {t.limitedScopeScoreUnavailable}
                      </p>
                    </div>
                  ) : (
                    <>
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
                    </>
                  )}
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

                    <div
                      className={language === "ar" ? "text-left" : "text-right"}
                    >
                      {showCashRiskCountdown ? (
                        <>
                          <p className="text-sm text-slate-500">
                            {t.daysUntilRisk}
                          </p>
                          <p className="text-xl font-semibold text-amber-700">
                            {cashRiskDays}
                          </p>
                        </>
                      ) : showImmediateCashRisk ? (
                        <p className="max-w-[220px] text-sm font-semibold text-red-700">
                          {t.cashRiskNow}
                        </p>
                      ) : showNoImmediateCashRisk ? (
                        <p className="max-w-[240px] text-sm font-semibold text-emerald-700">
                          {t.noImmediateCashRisk}
                        </p>
                      ) : null}
                    </div>
                  </div>

                  <p className="text-sm text-slate-600 mt-4">
                    {translateBackendMessage(result.cashflow_forecast?.message)}
                  </p>
                </div>

                <div className="rounded-2xl border bg-slate-50 p-5 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-md">
                  <div>
                    <p className="text-sm text-slate-500">
                      {sourceEvidenceIsLimited
                        ? evidenceSensitiveCopy.budgetHeading
                        : t.recommendedBudget}
                    </p>

                    {isLimitedAnalysisScope ? (
                      <div className="mt-3">
                        <h3 className="text-2xl font-bold text-slate-700">
                          {t.limitedScopeNotAssessed}
                        </h3>
                        <p className="mt-2 text-sm leading-6 text-slate-500">
                          {t.limitedScopeBudgetUnavailable}
                        </p>
                      </div>
                    ) : (
                      <>
                        <h3 className="text-2xl font-bold text-slate-800 mt-1">
                          {translatedBudgetStatus}
                        </h3>

                        {sourceEvidenceIsLimited && (
                          <div className="mt-2 max-w-xl rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-xs text-amber-900">
                            <div className="font-semibold">
                              {evidenceSensitiveCopy.estimateBadge}
                            </div>
                            <div>{evidenceSensitiveNote}</div>
                          </div>
                        )}

                        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mt-5">
                          <div>
                            <p className="text-xs text-slate-500">{t.savingsTarget}</p>
                            <p className="font-semibold">{formatMoney(result.recommended_budget?.savings_target)}</p>
                          </div>
                          <div>
                            <p className="text-xs text-slate-500">{t.needs}</p>
                            <p className="font-semibold">{formatMoney(result.recommended_budget?.needs)}</p>
                          </div>
                          <div>
                            <p className="text-xs text-slate-500">{t.wants}</p>
                            <p className="font-semibold">{formatMoney(result.recommended_budget?.wants)}</p>
                          </div>
                          <div>
                            <p className="text-xs text-slate-500">{t.emergencyFund}</p>
                            <p className="font-semibold">{formatMoney(result.recommended_budget?.emergency_fund_target)}</p>
                          </div>
                          <div>
                            <p className="text-xs text-slate-500">{t.safeSpending}</p>
                            <p className="font-semibold">{formatMoney(result.recommended_budget?.max_safe_spending)}</p>
                          </div>
                        </div>

                        <p className="text-sm text-slate-600 mt-4">
                          {translateBackendMessage(result.recommended_budget?.message)}
                        </p>
                      </>
                    )}
                  </div>
                </div>

                <div className="rounded-2xl border bg-slate-50 p-5 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-md">
                  <div className="mb-4">
                    <p className="text-sm font-medium text-slate-700">
                      {t.detectedSubscriptions}
                    </p>

                    {isLimitedAnalysisScope ? (
                      <div className="mt-3 rounded-xl border border-slate-200 bg-white px-4 py-3">
                        <p className="text-sm font-semibold text-slate-700">
                          {t.limitedScopeNotAssessed}
                        </p>
                        <p className="mt-1 text-sm leading-6 text-slate-500">
                          {t.limitedScopeSubscriptionsUnavailable}
                        </p>
                      </div>
                    ) : (
                    <div className="mt-3 grid gap-3 sm:grid-cols-3">
                      <div className="rounded-xl border border-slate-200 bg-white px-3 py-3">
                        <p className="text-xs text-slate-500">
                          {t.confirmedRecurringSubscriptions}
                        </p>
                        <p className="mt-1 text-xl font-bold text-slate-800">
                          {result.subscriptions_detected?.length ?? 0}
                        </p>
                      </div>

                      <div className="rounded-xl border border-slate-200 bg-white px-3 py-3">
                        <p className="text-xs text-slate-500">
                          {t.categorizedSubscriptionSpend}
                        </p>
                        <p className="mt-1 text-xl font-semibold text-slate-800">
                          {formatMoney(subscriptionCategorySpend)}
                        </p>
                      </div>

                      <div className="rounded-xl border border-slate-200 bg-white px-3 py-3">
                        <p className="text-xs text-slate-500">
                          {t.estimatedRecurringCharge}
                        </p>
                        <p className="mt-1 text-xl font-semibold text-red-600">
                          {formatMoney(
                            result.financial_habit_scores?.metrics?.subscription_total
                          )}
                        </p>
                      </div>
                    </div>
                    )}
                  </div>

                  {!isLimitedAnalysisScope && (
                    result.subscriptions_detected?.length > 0 ? (
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
                    <div className="space-y-2">
                      <p className="text-sm text-slate-500">
                        {t.noRecurringSubscriptions}
                      </p>

                      {hasSubscriptionCategoryWithoutConfirmedRecurring && (
                        <div className="rounded-xl border border-amber-100 bg-amber-50 px-3 py-2 text-xs leading-6 text-amber-800">
                          {t.subscriptionCategoryNotRecurring}
                        </div>
                      )}
                    </div>
                    )
                  )}
                </div>

                <div className="rounded-2xl border bg-slate-50 p-5 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-md">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <p className="text-sm text-slate-500">
                        {sourceEvidenceIsLimited
                          ? evidenceSensitiveCopy.savingsHeading
                          : t.aiSavingsOpportunities}
                      </p>

                      <h3 className="text-2xl font-bold text-green-600 mt-1">
                        {isLimitedAnalysisScope
                          ? t.limitedScopeNotAssessed
                          : formatMoney(totalSavingsOpportunity)}
                      </h3>
                      {sourceEvidenceIsLimited && (
                        <div className="mt-2 max-w-xl rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-xs text-amber-900">
                          <div className="font-semibold">
                            {evidenceSensitiveCopy.estimateBadge}
                          </div>
                          <div>{evidenceSensitiveNote}</div>
                        </div>
                      )}

                      <p className="text-xs text-slate-500 mt-1">
                        {isLimitedAnalysisScope
                          ? t.limitedScopeSavingsUnavailable
                          : t.estimatedSavingsOpportunity}
                      </p>
                    </div>

                    {totalSavingsOpportunity > 0 && (
                      <span className="rounded-full bg-green-100 px-3 py-1 text-xs font-medium text-green-700">
                        {t.aiDetected}
                      </span>
                    )}
                  </div>

                  {isLimitedAnalysisScope ? (
                    <p className="text-sm text-slate-500">
                      {t.limitedScopeSavingsUnavailable}
                    </p>
                  ) : result.savings_opportunities?.length > 0 ? (
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
                                  {translateSavingsText(item.issue)}
                                </p>

                                <p className="text-sm text-slate-500 mt-1">
                                  {normalizeNarrativeMoney(
                                    translateSavingsText(item.recommendation)
                                  )}
                                </p>
                              </div>

                              <div className="text-right shrink-0">
                                <p className="font-semibold text-green-600">
                                  {formatMoney(
                                    item.estimated_savings_opportunity
                                  )}
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
                              {translateSeverity(item.severity)}
                            </span>

                            {getSavingsEvidence(item) && (
                              <div
                                className="mt-3 rounded-lg border border-slate-200 bg-slate-50 px-3 py-2"
                                dir={language === "ar" ? "rtl" : "ltr"}
                              >
                                <p className="text-xs font-semibold text-slate-700">
                                  {
                                    (evidenceLabels[language] ||
                                      evidenceLabels.en)
                                      .basedOnObservedActivity
                                  }
                                </p>
                                <p className="mt-1 text-xs leading-5 text-slate-600">
                                  {getSavingsEvidence(item)}
                                </p>
                              </div>
                            )}
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

                  {visibleFinancialInsights.length > 0 ? (
                    <div className="space-y-3">
                      {visibleFinancialInsights.map(
                        (insight: any, index: number) => {
                          const insightEvidence = getInsightEvidence(insight);

                          return (
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
                                  {normalizeNarrativeMoney(translateInsightText(insight.message))}
                                </p>

                                {insightEvidence && (
                                  <div
                                    className="mt-3 rounded-lg border border-slate-200/80 bg-white/70 px-3 py-2"
                                    dir={language === "ar" ? "rtl" : "ltr"}
                                  >
                                    <p className="text-xs font-semibold text-slate-700">
                                      {
                                        (evidenceLabels[language] ||
                                          evidenceLabels.en)
                                          .basedOnObservedActivity
                                      }
                                    </p>
                                    <p className="mt-1 text-xs leading-5 text-slate-600">
                                      {insightEvidence}
                                    </p>
                                  </div>
                                )}
                              </div>
                            </div>
                          </div>
                        );
                        }
                      )}
                    </div>
                  ) : (
                    <p className="text-sm text-slate-500">
                      No AI insights available yet.
                    </p>
                  )}
                </div>

                {groundedWasteItems.length > 0 && (
                  <section className="rounded-2xl border bg-slate-50 p-5 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-md">
                    <h3 className="text-xl font-semibold mb-3">
                      {t.wasteDetected}
                    </h3>

                    <div className="space-y-3">
                      {groundedWasteItems.map(
                        (groundedWaste: any, i: number) => {
                          return (
                            <div
                              key={i}
                              className="rounded-xl border border-slate-200 bg-white px-4 py-3"
                              dir={language === "ar" ? "rtl" : "ltr"}
                            >
                              <p className="text-sm text-slate-700">
                                {groundedWaste.text}
                              </p>

                              {groundedWaste.evidence && (
                                <div className="mt-2 border-t border-slate-100 pt-2">
                                  <p className="text-[11px] font-medium uppercase tracking-wide text-slate-500">
                                    {
                                      (evidenceLabels[language] ||
                                        evidenceLabels.en)
                                        .basedOnObservedActivity
                                    }
                                  </p>
                                  <p className="mt-1 text-xs leading-5 text-slate-500">
                                    {groundedWaste.evidence}
                                  </p>
                                </div>
                              )}
                            </div>
                          );
                        }
                      )}
                    </div>
                  </section>
                )}

                {groundedSavingStrategies.length > 0 && (
                  <section className="rounded-2xl border bg-slate-50 p-5 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-md">
                    <h3 className="text-xl font-semibold mb-3">
                      {t.savingStrategies}
                    </h3>

                    <div className="space-y-3">
                      {groundedSavingStrategies.map(
                        (groundedStrategy: any, i: number) => {
                          return (
                            <div
                              key={i}
                              className="rounded-xl border border-slate-200 bg-white px-4 py-3"
                              dir={language === "ar" ? "rtl" : "ltr"}
                            >
                              <p className="text-sm text-slate-700">
                                {groundedStrategy.text}
                              </p>

                              {groundedStrategy.evidence && (
                                <div className="mt-2 border-t border-slate-100 pt-2">
                                  <p className="text-[11px] font-medium uppercase tracking-wide text-slate-500">
                                    {
                                      (evidenceLabels[language] ||
                                        evidenceLabels.en)
                                        .basedOnObservedActivity
                                    }
                                  </p>
                                  <p className="mt-1 text-xs leading-5 text-slate-500">
                                    {groundedStrategy.evidence}
                                  </p>
                                </div>
                              )}
                            </div>
                          );
                        }
                      )}
                    </div>
                  </section>
                )}

                {visibleRiskNotes.length > 0 && (
                  <section className="rounded-2xl border bg-slate-50 p-5 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-md">
                    <h3 className="text-xl font-semibold mb-3">
                      {t.riskNotes}
                    </h3>

                    <div className="space-y-2">
                      {visibleRiskNotes.map(
                        (item: string, i: number) => (
                          <p key={i} className="text-sm text-slate-700">
                            {normalizeNarrativeMoney(
                              translateBackendMessage(item)
                            )}
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

                        <XAxis
                          dataKey="date"
                          tickFormatter={formatChartDate}
                          minTickGap={52}
                          tickMargin={8}
                          tick={{ fontSize: 11 }}
                          interval="preserveStartEnd"
                        />

                        <YAxis
                          tickFormatter={formatChartAxisAmount}
                          width={54}
                          tick={{ fontSize: 11 }}
                        />

                        <Tooltip
                          labelFormatter={formatChartTooltipDate}
                          formatter={(value) => formatMoney(value)}
                        />

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

                        <XAxis
                          dataKey="date"
                          tickFormatter={formatChartDate}
                          minTickGap={52}
                          tickMargin={8}
                          tick={{ fontSize: 11 }}
                          interval="preserveStartEnd"
                        />
                        <YAxis
                          tickFormatter={formatChartAxisAmount}
                          width={54}
                          tick={{ fontSize: 11 }}
                        />
                        <Tooltip
                          labelFormatter={formatChartTooltipDate}
                          formatter={(value) => formatMoney(value)}
                        />

                        <Line
                          type="monotone"
                          dataKey="amount"
                          stroke="#16a34a"
                          strokeWidth={3}
                          dot={false}
                          activeDot={{ r: 4 }}
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

                  {confirmedRecurringSubscriptionCount > 0 &&
                  result.charts?.subscription_growth?.length > 0 ? (
                    <div className="h-80">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={result.charts.subscription_growth}>
                          <CartesianGrid
                            strokeDasharray="3 3"
                            vertical={false}
                          />

                          <XAxis
                          dataKey="date"
                          tickFormatter={formatChartDate}
                          minTickGap={52}
                          tickMargin={8}
                          tick={{ fontSize: 11 }}
                          interval="preserveStartEnd"
                        />
                          <YAxis
                          tickFormatter={formatChartAxisAmount}
                          width={54}
                          tick={{ fontSize: 11 }}
                        />
                          <Tooltip
                          labelFormatter={formatChartTooltipDate}
                          formatter={(value) => formatMoney(value)}
                        />

                          <Bar
                            dataKey="amount"
                            fill="#f97316"
                            radius={[8, 8, 0, 0]}
                          />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  ) : (
                    <div className="flex min-h-24 items-center justify-center rounded-xl border border-dashed bg-slate-50 px-6 py-6 text-center text-sm text-slate-500">
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

                        <XAxis
                          dataKey="date"
                          ticks={buildSparseDateTicks(
                            result.charts?.savings_evolution || [],
                            7
                          )}
                          tickFormatter={makeDedupedChartDateFormatter()}
                          minTickGap={64}
                          tickMargin={8}
                          tick={{ fontSize: 11 }}
                          interval="preserveStartEnd"
                        />
                        <YAxis
                          tickFormatter={formatChartAxisAmount}
                          width={54}
                          tick={{ fontSize: 11 }}
                        />
                        <Tooltip
                          labelFormatter={formatChartTooltipDate}
                          formatter={(value) => formatMoney(value)}
                        />

                        <Line
                          type="monotone"
                          dataKey="amount"
                          stroke="#7c3aed"
                          strokeWidth={3}
                          dot={false}
                          activeDot={{ r: 4 }}
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
                                <td className="px-3 py-2 text-right whitespace-nowrap">
                                  <div className="font-semibold">
                                    {formatMoney(item.value)}
                                  </div>
                                  {totalCategorySpend > 0 && (
                                    <div className="mt-0.5 text-xs font-normal text-slate-500">
                                      {formatEvidenceShare(
                                        (Number(item.value) /
                                          totalCategorySpend) *
                                          100
                                      )}{" "}
                                      {t.categoryShare}
                                    </div>
                                  )}
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </>
                  )}
                </div>

                <div className="rounded-2xl border bg-white p-6 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-md">
                  <div className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                    <div>
                      <p className="text-sm text-slate-500">
                        {t.aiFinancialCoach}
                      </p>

                      <h3 className="text-2xl font-bold text-slate-800">
                        {t.askFinanceAssistant}
                      </h3>
                      {hasVerificationContract && (
                        <div
                          className="mt-3 rounded-xl border border-blue-100 bg-blue-50 px-3 py-2 text-xs text-slate-600"
                          dir={language === "ar" ? "rtl" : "ltr"}
                        >
                          <span className="font-semibold text-slate-800">
                            {t.coachEvidenceTitle}:
                          </span>{" "}
                          {t.coachEvidenceBasedOn} ·{" "}
                          {shouldWithholdFinancialAnalysis
                            ? (
                                result?.verification?.extracted_transaction_count ??
                                result?.verification?.transaction_count ??
                                0
                              )
                            : (result?.verification?.transaction_count ?? 0)}{" "}
                          {shouldWithholdFinancialAnalysis
                            ? t.checkTransactionsExtracted
                            : t.coachTransactionsAnalyzed} ·{" "}
                          {(() => {
                            const verificationCurrency = String(
                              result?.verification?.currency || ""
                            ).trim();
                            const detectedCurrency = String(
                              result?.currency_detected || ""
                            ).trim();

                            if (
                              verificationCurrency &&
                              verificationCurrency.toUpperCase() !== "UNKNOWN"
                            ) {
                              return verificationCurrency;
                            }

                            if (
                              detectedCurrency &&
                              detectedCurrency.toUpperCase() !== "UNKNOWN"
                            ) {
                              return detectedCurrency;
                            }

                            return t.verificationUnavailable;
                          })()}{" "}
                          ·{" "}
                          {coachVerificationStatusLabel}
                        </div>
                      )}

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
                              ? t.you
                              : t.assistantName}
                          </p>

                          <div className="prose prose-sm max-w-none text-slate-700">
                            <ReactMarkdown>
                              {renderSafeText(message.content)}
                            </ReactMarkdown>
                          </div>
                        </div>
                      )
                    )}

                    {chatLoading && (
                      <div className="rounded-2xl bg-blue-50 border border-blue-100 p-4">
                        <p className="text-sm text-slate-500">
                          {t.aiThinking}
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
                    {renderSafeText(
                      translateBackendMessage(result.disclaimer),
                      t.disclaimer
                    )}
                  </p>
                )}
                      </>
                    )}
                  </>
                )}
              </>
            )}
          </div>
        )}
      </div>

        {evidenceView && (
          <div
            className="fixed inset-0 z-50 flex items-end justify-center bg-slate-950/40 p-0 sm:items-center sm:p-6"
            role="dialog"
            aria-modal="true"
            aria-label={getEvidenceTitle()}
            onClick={() => setEvidenceView(null)}
          >
            <div
              className="max-h-[88vh] w-full max-w-4xl overflow-hidden rounded-t-3xl bg-white shadow-2xl sm:rounded-3xl"
              dir={language === "ar" ? "rtl" : "ltr"}
              onClick={(event) => event.stopPropagation()}
            >
              <div className="flex items-start justify-between gap-4 border-b px-5 py-4 sm:px-6">
                <div>
                  <p className="text-sm font-semibold text-slate-900">
                    {getEvidenceTitle()}
                  </p>
                  <p className="mt-1 text-xs leading-5 text-slate-500">
                    {t.evidenceDescription}
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() => setEvidenceView(null)}
                  className="rounded-full border px-3 py-1.5 text-xs font-semibold text-slate-600 hover:bg-slate-50"
                >
                  {t.close}
                </button>
              </div>

              <div className="max-h-[62vh] overflow-auto">
                <table className="w-full text-sm">
                  <thead className="sticky top-0 bg-slate-50 text-xs text-slate-500">
                    <tr>
                      <th className="px-4 py-3 text-start font-medium">
                        {t.evidenceDate}
                      </th>
                      <th className="px-4 py-3 text-start font-medium">
                        {t.evidenceTransaction}
                      </th>
                      <th className="px-4 py-3 text-end font-medium">
                        {t.evidenceAmount}
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {getEvidenceTransactions().map((tx: any, index: number) => {
                      const signedCandidate = Number(tx?.signed_amount);
                      const amountCandidate = Number(tx?.amount);
                      const rawAmount = Number.isFinite(signedCandidate)
                        ? signedCandidate
                        : Number.isFinite(amountCandidate)
                        ? amountCandidate
                        : 0;

                      const txType = String(tx?.type || "").toLowerCase();

                      const displayAmount =
                        evidenceView === "expense"
                          ? Math.abs(rawAmount)
                          : evidenceView === "income"
                          ? Math.abs(rawAmount)
                          : txType === "expense"
                          ? -Math.abs(rawAmount)
                          : txType === "income"
                          ? Math.abs(rawAmount)
                          : rawAmount;

                      return (
                        <tr
                          key={`${tx?.date || "date"}-${tx?.description || "tx"}-${index}`}
                          className="border-t"
                        >
                          <td className="whitespace-nowrap px-4 py-3 text-slate-500">
                            {formatEvidenceDate(tx?.date)}
                          </td>
                          <td className="px-4 py-3 text-slate-800">
                            {renderSafeText(
                              tx?.description || tx?.label || tx?.merchant,
                              "-"
                            )}
                          </td>
                          <td
                            className={`whitespace-nowrap px-4 py-3 text-end font-semibold ${
                              displayAmount < 0
                                ? "text-red-600"
                                : "text-emerald-700"
                            }`}
                          >
                            {formatMoney(displayAmount)}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>

              <div className="flex items-center justify-between gap-4 border-t bg-slate-50 px-5 py-4 sm:px-6">
                <span className="text-sm text-slate-600">
                  {t.evidenceTotal}
                </span>
                <span className="text-lg font-bold text-slate-900">
                  {formatMoney(getEvidenceTotal())}
                </span>
              </div>
            </div>
          </div>
        )}

    </main>
  );
}