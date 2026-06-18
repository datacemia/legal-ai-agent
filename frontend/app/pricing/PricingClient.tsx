"use client";

import { useEffect, useState } from "react";

type Language = "en" | "fr" | "ar";

type Agent = {
  slug: string;
  name: string;
  description: string;
  trialOutcome: string;
  credits: number;
  gradient: string;
};

type CreditPack = {
  name: string;
  credits: number;
  price: string;
  description: string;
  highlighted?: boolean;
};

type WhyCard = {
  title: string;
  desc: string;
};

type PricingMessages = {
  trial: (agentName: string) => string;
  credits: string;
  pro: string;
};

type PricingLabels = {
  apiSectionBadge: string;
  apiSectionTitle: string;
  apiSectionDesc: string;

  apiPlans: {
    name: string;
    price: string;
    credits: string;
    rate: string;
    desc: string;
    highlighted?: boolean;
    features: string[];
  }[];

  apiStartPlan: string;
  apiContactSales: string;
  badge: string;
  title: string;
  desc: string;
  socialProof: string;
  workflowLine: string;
  powerUserBadge: string;
  activateTrialCta: string;
  viewPlans: string;
  audience: string;
  trustedWorkflow: string;
  whyTitle: string;
  whyCards: WhyCard[];
  mostPopular: string;
  microTrust: string[];
  section1: string;
  section2: string;
  section3: string;
  section4: string;
  trialsTitle: string;
  trialsDesc: string;
  trialsBadge: string;
  oneTimeTrial: string;
  trialAnalysis: string;
  trialReassurance: string;
  startTrial: string;
  creditsTitle: string;
  mostFlexible: string;
  creditsDesc: string;
  bestValue: string;
  oneTime: string;
  globalCredits: string;
  buyCredits: string;
  plansTitle: string;
  plansDesc: string;
  globalPro: string;
  bestForProfessionals: string;
  proValueNote: string;
  proDesc: string;
  month: string;
  proFeatures: string[];
  proUsage: string;
  proCreditsPolicy: string;
  proPurchasedCredits: string;
  upgradePro: string;
  enterprise: string;
  premiumDesc: string;
  custom: string;
  tailoredPricing: string;
  premiumFeatures: string[];
  contactSales: string;
  creditCostsTitle: string;
  creditCostsDesc: string;
  creditComplexityNote: string;
  creditsPerAnalysis: string;
  infoCards: WhyCard[];
  disclaimer: string;
  messages: PricingMessages;
  agents: Agent[];
  creditPacks: CreditPack[];
};

const labels: Record<Language, PricingLabels> = {
  en: {
    apiSectionBadge: "Runexa API",
    apiSectionTitle: "API Plans for Developers",
    apiSectionDesc:
      "Runexa API is a dedicated paid product for teams that want to embed AI agents into applications, dashboards, internal tools, and enterprise workflows.",
    apiStartPlan: "Start API Plan",
    apiContactSales: "Contact Sales",
    apiPlans: [
        {
    name: "API Starter",
    price: "$29",
    credits: "100 API Credits",
    rate: "10 Requests / Minute",

    desc:
      "Designed for developers exploring Runexa AI APIs and building early-stage integrations.",

    features: [
      "Legal AI API",
      "Finance AI API",
      "Study AI API",
      "Business AI API",
      "Asynchronous Processing",
      "API Key Management",
      "Usage Analytics Dashboard",
      "Developer Documentation",
    ],
  },
      {
        name: "API Pro",
        price: "$99",
        credits: "500 API Credits",
        rate: "Higher API Limits",
        desc:
          "Built for production applications, growing teams, and higher API usage.",
        highlighted: true,
        features: [
          "Everything in API Starter",
          "Higher API Limits",
          "Priority Processing",
          "Usage Analytics Dashboard",
          "Credits & Usage Tracking",
          "Production-Ready Integrations",
        ],
      },
      {
        name: "Enterprise API",

        price: "Custom",

        credits: "Custom API Credits",

        rate: "Custom Limits",

        desc:
          "Built for enterprises requiring custom AI solutions, advanced integrations, and dedicated support.",

        features: [
          "Everything in API Pro",
          "Custom AI Workflows",
          "Team API Access",
          "Private Infrastructure Options",
          "Dedicated Support",
          "Enterprise Onboarding",
        ],
      },
    ],

    badge: "Unified Access to Every Runexa AI Agent",
    title: "One Account. Every AI Agent. Simple Pricing.",
    desc:
      "Access every Runexa AI agent with a single account. Start with a $1 trial, use unified credits, or upgrade to Pro for unlimited access.",
    socialProof:
      "Trusted for legal analysis, financial insights, learning support, and business decision-making.",
    workflowLine:
      "Built for real-world analysis, learning, and decision workflows.",
    powerUserBadge:
      "Most Popular for Professionals",
    activateTrialCta:
      "Start Your One-Time $1 Trial",
    viewPlans:
      "Compare Plans",
    audience:
      "For Individuals, Professionals, and Enterprises",
    trustedWorkflow:
      "Upload → Analyze → Act",
    whyTitle:
      "Why People Choose Runexa",
    whyCards: [
    {
      title: "Identify Contract Risks",
      desc: "Review contracts, obligations, and potential risks before signing.",
    },

    {
      title: "Improve Financial Decisions",
      desc: "Discover spending patterns, subscriptions, and opportunities to save.",
    },

    {
      title: "Learn More Effectively",
      desc: "Transform study materials into summaries, quizzes, and study plans.",
    },

    {
      title: "Make Better Business Decisions",
      desc: "Analyze opportunities, risks, and strategic options with AI-powered insights.",
    },
  ],
    mostPopular: "Most Popular",

    microTrust: [
      "🔒 Secure AI Platform",
      "🌍 Global Access",
      "⚡ Fast AI Insights",
    ],

    section1: "Start with a $1 Trial",

    section2: "Unified Credits",

    section3: "Pro & Enterprise Plans",

    section4: "Credit Usage by Agent",

    trialsTitle: "$1 Trials",

    trialsDesc:
      "Each account includes one one-time $1 trial. Choose one Runexa AI agent and explore it before using credits or upgrading to a plan.",

    trialsBadge: "Choose Your AI Agent",

    oneTimeTrial: "One-Time Trial per Account",

    trialAnalysis: "One AI-Powered Analysis",

    trialReassurance:
      "One $1 trial per account. Instant access after activation.",

    startTrial: "Start Trial",

    creditsTitle: "Unified Credits",

    mostFlexible: "Most Flexible",

    creditsDesc:
      "Purchase credits once and use them across every Runexa AI agent. Ideal for occasional users who do not need a subscription.",

    bestValue: "Best Value",

    oneTime: "One-Time Purchase",

    globalCredits: "Credits",

    buyCredits: "Buy Credits",

    plansTitle: "Pro & Enterprise Plans",

    plansDesc:
      "One subscription gives you access to all Runexa AI agents. No separate subscriptions required.",

    globalPro: "Runexa Pro",

    bestForProfessionals: "Best for Professionals",

    proValueNote:
      "Designed for regular users who rely on multiple AI agents.",

    proDesc:
      "For individuals and professionals who need ongoing access across multiple AI agents.",

    month: "/month",

    proFeatures: [
      "500 Credits per Month",
      "Usable Across All Agents",
      "Priority Processing",
      "Access to Legal, Finance, Study, and Business AI",
      "Future AI Agents Included",
    ],

    proUsage:
      "Includes up to 100 Study Sessions, 71 Financial Analyses, 41 Legal Reviews, or 16 Business Decision Analyses per month.",

    proCreditsPolicy:
      "Subscription credits renew every month and do not carry over to the next billing cycle.",

    proPurchasedCredits:
      "Purchased credit packs never expire.",

    upgradePro: "Upgrade to Pro",

    enterprise: "Enterprise",

    premiumDesc:
      "For teams, organizations, educational institutions, and businesses.",

    custom: "Custom",

    tailoredPricing: "Custom Pricing",

    premiumFeatures: [
      "Secure Workspaces",
      "Team Collaboration",
      "Private AI Workflows",
      "Organization Management",
      "Priority Support",
    ],
    contactSales: "Contact Sales",

    creditCostsTitle: "Credit Usage by Agent",

    creditCostsDesc:
      "A single credit balance works across all Runexa AI agents.",

    creditComplexityNote:
      "Credit consumption depends on the complexity of the analysis.",

    creditsPerAnalysis: "Credits per Analysis",
    infoCards: [
    {
      title: "Start Your Way",
      desc: "Try one AI agent for $1 per account, or go directly to credits or a subscription plan.",
    },

    {
      title: "One Credit Balance",
      desc: "Use the same credits across Legal, Finance, Study, and Business AI agents.",
    },

    {
      title: "One Plan for All Agents",
      desc: "A single Pro subscription gives you access across the entire Runexa platform.",
    },
  ],
    disclaimer:
      "⚠️ Runexa AI agents provide informational and decision-support insights. Always verify important legal, financial, academic, and business decisions with qualified professionals or official sources.",

    messages: {
      trial: (agentName: string) =>
        `Continue to checkout to activate ${agentName}.`,

      credits:
        "Continue to checkout to purchase credits.",

      pro:
        "Continue to checkout to activate your subscription.",
    },
    agents: [
    {
      slug: "legal",
      name: "Runexa Legal Agent",
      description:
        "Identify contract risks, obligations, and critical clauses before signing.",
      trialOutcome: "One AI-powered contract analysis",
      credits: 12,
      gradient: "from-slate-950 to-blue-700",
    },

    {
      slug: "finance",
      name: "Runexa Finance Coach",
      description:
        "Understand spending patterns, reduce waste, and improve financial decisions.",
      trialOutcome: "One AI-powered financial analysis",
      credits: 7,
      gradient: "from-emerald-700 to-teal-500",
    },

    {
      slug: "study",
      name: "Runexa Study Agent",
      description:
        "Transform study materials into summaries, quizzes, and learning plans.",
      trialOutcome: "One AI-powered learning session",
      credits: 5,
      gradient: "from-indigo-700 to-violet-500",
    },

    {
      slug: "business",
      name: "Runexa Business Decision Agent",
      description:
        "Evaluate opportunities, risks, and strategic business decisions.",
      trialOutcome: "One AI-powered business analysis",
      credits: 30,
      gradient: "from-amber-700 to-orange-500",
    },
  ],
    creditPacks: [
    {
      name: "Starter",
      credits: 50,
      price: "$9",
      description:
        "Ideal for exploring multiple Runexa AI agents and occasional use.",
    },

    {
      name: "Growth",
      credits: 150,
      price: "$24",
      description:
        "Best value for regular users working across multiple AI agents.",
      highlighted: true,
    },

    {
      name: "Scale",
      credits: 500,
      price: "$75",
      description:
        "Designed for professionals, teams, and higher-volume AI workloads.",
    },
  ],
  },

  fr: {
    apiSectionBadge: "API Runexa",

    apiSectionTitle: "Offres API pour les développeurs",

    apiSectionDesc:
      "L’API Runexa est un produit dédié aux développeurs et aux entreprises qui souhaitent intégrer des agents IA dans leurs applications, tableaux de bord, outils internes et workflows métier.",

    apiStartPlan: "Commencer avec l’API",

    apiContactSales: "Contacter l’équipe commerciale",

    apiPlans: [
      {
        name: "API Starter",

        price: "$29",

        credits: "100 crédits API",

        rate: "10 requêtes / minute",

        desc:
          "Conçu pour les développeurs qui découvrent les API IA Runexa et créent leurs premières intégrations.",

        features: [
          "API IA juridique",
          "API IA finance",
          "API IA étude",
          "API IA business",
          "Traitement asynchrone",
          "Gestion des clés API",
          "Tableau de bord d’utilisation",
          "Documentation développeur",
        ],
      },

      {
        name: "API Pro",

        price: "$99",

        credits: "500 crédits API",

        rate: "Limites API étendues",

        desc:
          "Conçu pour les applications en production, les équipes en croissance et une utilisation avancée de l’API.",

        highlighted: true,

        features: [
          "Tout ce qui est inclus dans API Starter",
          "Limites API étendues",
          "Traitement prioritaire",
          "Tableau de bord d’utilisation",
          "Suivi des crédits et de l’utilisation",
          "Intégrations prêtes pour la production",
        ],
      },
      {
        name: "API Entreprise",

        price: "Sur mesure",

        credits: "Crédits API personnalisés",

        rate: "Limites personnalisées",

        desc:
          "Conçu pour les entreprises ayant besoin de solutions IA personnalisées, d’intégrations avancées et d’un accompagnement dédié.",

        features: [
          "Tout ce qui est inclus dans API Pro",
          "Workflows IA personnalisés",
          "Accès API pour les équipes",
          "Options d’infrastructure privée",
          "Support dédié",
          "Onboarding entreprise",
        ],
      },
    ],

    badge: "Accès unifié à tous les agents IA Runexa",
    title: "Un compte. Tous les agents IA. Une tarification simple.",
    desc:
      "Accédez à tous les agents IA Runexa avec un seul compte. Commencez avec un essai à 1 $, utilisez des crédits unifiés ou passez à Runexa Pro.",
    socialProof:
      "Utilisé pour l’analyse juridique, les finances personnelles, l’apprentissage et la prise de décision business.",
    workflowLine:
      "Conçu pour l’analyse, l’apprentissage et la prise de décision dans le monde réel.",
    powerUserBadge:
      "Le choix privilégié des professionnels",
    activateTrialCta:
      "Commencer votre essai unique à 1 $",
    viewPlans:
      "Comparer les offres",
    audience:
      "Pour les particuliers, les professionnels et les entreprises",
    trustedWorkflow:
      "Importer → Analyser → Agir",
    whyTitle:
      "Pourquoi choisir Runexa",
    whyCards: [
    {
      title: "Identifier les risques contractuels",
      desc:
        "Analysez les contrats, obligations et risques potentiels avant de signer.",
    },

    {
      title: "Améliorer vos décisions financières",
      desc:
        "Identifiez les habitudes de dépenses, les abonnements et les opportunités d’économies.",
    },

    {
      title: "Apprendre plus efficacement",
      desc:
        "Transformez vos supports d’étude en résumés, quiz et plans d’apprentissage.",
    },

    {
      title: "Prendre de meilleures décisions business",
      desc:
        "Analysez les opportunités, les risques et les options stratégiques grâce à des insights alimentés par l’IA.",
    },
  ],
    mostPopular: "Le plus populaire",
    microTrust: [
      "🔒 Plateforme IA sécurisée",
      "🌍 Accès mondial",
      "⚡ Insights IA rapides",
    ],
    section1: "Commencer avec un essai à 1 $",
    section2: "Crédits unifiés",
    section3: "Offres Pro & Entreprise",
    section4: "Utilisation des crédits par agent",
    trialsTitle: "Essais à 1 $",
    trialsDesc:
      "Chaque compte bénéficie d’un seul essai à 1 $. Choisissez un agent IA Runexa et découvrez-le avant d’utiliser des crédits ou de passer à une offre.",
    trialsBadge: "Choisissez votre agent IA",
    oneTimeTrial: "Essai unique par compte",
    trialAnalysis: "Une analyse alimentée par l’IA",
    trialReassurance:
      "Un seul essai à 1 $ par compte. Accès instantané après activation.",
    startTrial: "Commencer l’essai",
    creditsTitle: "Crédits unifiés",
    mostFlexible: "Le plus flexible",
    creditsDesc:
      "Achetez des crédits une seule fois et utilisez-les sur tous les agents IA Runexa. Idéal pour les utilisateurs occasionnels qui n’ont pas besoin d’un abonnement.",
    bestValue: "Meilleur rapport qualité-prix",
    oneTime: "Paiement unique",
    globalCredits: "Crédits",
    buyCredits: "Acheter des crédits",
    plansTitle: "Offres Pro & Entreprise",
    plansDesc:
      "Un seul abonnement vous donne accès à tous les agents IA Runexa. Aucun abonnement séparé n’est nécessaire.",
    globalPro: "Runexa Pro",
    bestForProfessionals: "Idéal pour les professionnels",
    proValueNote:
      "Conçu pour les utilisateurs réguliers qui s’appuient sur plusieurs agents IA.",
    proDesc:
      "Pour les particuliers et les professionnels qui ont besoin d’un accès continu à plusieurs agents IA.",
    month: "/mois",
    proFeatures: [
      "500 crédits par mois",
      "Utilisables sur tous les agents",
      "Traitement prioritaire",
      "Accès aux agents IA Juridique, Finance, Étude et Business",
      "Nouveaux agents IA inclus",
    ],

    proUsage:
      "Comprend jusqu'à 100 sessions d'apprentissage, 71 analyses financières, 41 revues juridiques ou 16 analyses de décision d'entreprise par mois.",

    proCreditsPolicy:
      "Les crédits d'abonnement sont renouvelés chaque mois et ne sont pas reportés au cycle de facturation suivant.",

    proPurchasedCredits:
      "Les packs de crédits achetés n'expirent jamais.",

    upgradePro: "Passer à Runexa Pro",
    enterprise: "Entreprise",
    premiumDesc:
      "Pour les équipes, les organisations, les établissements d’enseignement et les entreprises.",
    custom: "Sur mesure",
    tailoredPricing: "Tarification personnalisée",
    premiumFeatures: [
      "Espaces de travail sécurisés",
      "Collaboration d’équipe",
      "Workflows IA privés",
      "Gestion de l’organisation",
      "Support prioritaire",
    ],
    contactSales: "Contacter l’équipe commerciale",
    creditCostsTitle: "Utilisation des crédits par agent",
    creditCostsDesc:
      "Un seul solde de crédits fonctionne sur tous les agents IA Runexa.",
    creditComplexityNote:
      "La consommation de crédits dépend de la complexité de l’analyse.",
    creditsPerAnalysis: "Crédits par analyse",
    infoCards: [
      {
        title: "Accès flexible",
        desc:
          "Commencez avec un seul essai à 1 $ par compte, achetez des crédits ou choisissez une offre par abonnement.",
      },
      {
        title: "Un solde de crédits unique",
        desc:
          "Le même solde de crédits fonctionne sur tous les agents IA Runexa.",
      },
      {
        title: "Une seule offre pour tous les agents",
        desc:
          "Un abonnement Runexa Pro vous donne accès à l’ensemble de la plateforme Runexa.",
      },
    ],
    disclaimer:
      "⚠️ Les agents IA Runexa fournissent des analyses informatives et des insights d’aide à la décision. Vérifiez toujours les décisions juridiques, financières, académiques ou commerciales importantes auprès de professionnels qualifiés ou de sources officielles.",

    messages: {
      trial: (agentName: string) =>
        `Poursuivez vers le paiement pour activer ${agentName}.`,

      credits:
        "Poursuivez vers le paiement pour acheter des crédits.",

      pro:
        "Poursuivez vers le paiement pour activer votre abonnement.",
    },
    agents: [
    {
      slug: "legal",
      name: "Runexa Legal Agent",
      description:
        "Identifiez les risques contractuels, les obligations et les clauses critiques avant de signer.",
      trialOutcome: "Une analyse de contrat alimentée par l’IA",
      credits: 12,
      gradient: "from-slate-950 to-blue-700",
    },

    {
      slug: "finance",
      name: "Runexa Finance Coach",
      description:
        "Comprenez vos habitudes de dépenses, réduisez le gaspillage et améliorez vos décisions financières.",
      trialOutcome: "Une analyse financière alimentée par l’IA",
      credits: 7,
      gradient: "from-emerald-700 to-teal-500",
    },

    {
      slug: "study",
      name: "Runexa Study Agent",
      description:
        "Transformez vos supports d’étude en résumés, quiz et plans d’apprentissage.",
      trialOutcome: "Une session d’apprentissage alimentée par l’IA",
      credits: 5,
      gradient: "from-indigo-700 to-violet-500",
    },

    {
      slug: "business",
      name: "Runexa Business Decision Agent",
      description:
        "Évaluez les opportunités, les risques et les décisions stratégiques.",
      trialOutcome: "Une analyse business alimentée par l’IA",
      credits: 30,
      gradient: "from-amber-700 to-orange-500",
    },
  ],
    creditPacks: [
    {
      name: "Starter",
      credits: 50,
      price: "$9",
      description:
        "Idéal pour découvrir plusieurs agents IA Runexa et pour une utilisation occasionnelle.",
    },
    {
      name: "Growth",
      credits: 150,
      price: "$24",
      description:
        "Le meilleur rapport qualité-prix pour les utilisateurs réguliers qui utilisent plusieurs agents IA.",
      highlighted: true,
    },
    {
      name: "Scale",
      credits: 500,
      price: "$75",
      description:
        "Conçu pour les professionnels, les équipes et les volumes d’utilisation plus importants.",
    },
  ],
  },

  ar: {
    apiSectionBadge: "واجهة Runexa API",
    apiSectionTitle: "خطط API للمطورين",
    apiSectionDesc:
      "واجهة Runexa API هي منتج مخصص للمطورين والشركات الذين يرغبون في دمج وكلاء الذكاء الاصطناعي داخل تطبيقاتهم ولوحات التحكم والأدوات الداخلية وسير العمل المؤسسي.",
    apiStartPlan: "ابدأ مع API",
    apiContactSales: "تواصل مع فريق المبيعات",
    apiPlans: [
      {
        name: "API Starter",
        price: "$29",
        credits: "100 رصيد API",
        rate: "10 طلبات / دقيقة",
        desc:
          "مصممة للمطورين الذين يستكشفون واجهات Runexa AI API ويبنون تكاملاتهم الأولى.",
        features: [
          "API الذكاء القانوني",
          "API الذكاء المالي",
          "API الدراسة الذكية",
          "API ذكاء الأعمال",
          "المعالجة غير المتزامنة",
          "إدارة مفاتيح API",
          "لوحة تحليلات الاستخدام",
          "توثيق المطورين",
        ],
      },

      {
  name: "API Pro",

  price: "$99",

  credits: "500 رصيد API",

  rate: "حدود API أعلى",

  desc:
    "مصممة للتطبيقات العاملة في بيئات الإنتاج، والفرق المتنامية، والاستخدام المتقدم لواجهة API.",

  highlighted: true,

  features: [
    "كل ما يتضمنه API Starter",
    "حدود API أعلى",
    "معالجة ذات أولوية",
    "لوحة تحليلات الاستخدام",
    "تتبع الأرصدة والاستخدام",
    "تكاملات جاهزة للإنتاج",
  ],
},

{
  name: "API Enterprise",

  price: "مخصص",

  credits: "أرصدة API مخصصة",

  rate: "حدود مخصصة",

  desc:
    "مصممة للمؤسسات التي تحتاج إلى حلول ذكاء اصطناعي مخصصة، وتكاملات متقدمة، ودعم مخصص.",

  features: [
        "كل ما يتضمنه API Pro",
        "سير عمل ذكاء اصطناعي مخصص",
        "وصول API للفرق",
        "خيارات بنية تحتية خاصة",
        "دعم مخصص",
        "تهيئة المؤسسات",
      ],
    },
    ],

    badge: "وصول موحّد إلى جميع وكلاء Runexa الذكية",
    title: "حساب واحد. جميع الوكلاء الذكيين. تسعير بسيط.",
    desc:
      "استفد من جميع وكلاء Runexa الذكية من خلال حساب واحد. ابدأ بتجربة مقابل 1 دولار، أو استخدم الأرصدة الموحّدة، أو قم بالترقية إلى Runexa Pro.",
    socialProof:
      "يُستخدم للتحليل القانوني، والرؤى المالية، ودعم التعلّم، واتخاذ قرارات الأعمال.",
    workflowLine:
      "مصمم للتحليل والتعلّم واتخاذ القرارات في بيئات العمل الواقعية.",
    powerUserBadge:
      "الخيار المفضل للمحترفين",
    activateTrialCta:
      "ابدأ تجربتك الوحيدة مقابل 1 دولار",
    viewPlans:
      "مقارنة الخطط",
    audience:
      "للأفراد والمحترفين والمؤسسات",
    trustedWorkflow:
      "رفع → تحليل → تنفيذ",
    whyTitle:
      "لماذا يختار المستخدمون Runexa",
    whyCards: [
    {
      title: "تحديد المخاطر التعاقدية",
      desc:
        "راجع العقود والالتزامات والمخاطر المحتملة قبل التوقيع.",
    },
    {
      title: "تحسين قراراتك المالية",
      desc:
        "اكتشف أنماط الإنفاق والاشتراكات وفرص التوفير.",
    },
    {
      title: "التعلّم بفعالية أكبر",
      desc:
        "حوّل موادك الدراسية إلى ملخصات واختبارات وخطط تعلّم.",
    },
    {
      title: "اتخاذ قرارات أعمال أفضل",
      desc:
        "حلّل الفرص والمخاطر والخيارات الاستراتيجية باستخدام رؤى مدعومة بالذكاء الاصطناعي.",
    },
  ],
    mostPopular: "الأكثر شيوعاً",
    microTrust: [
      "🔒 منصة ذكاء اصطناعي آمنة",
      "🌍 وصول عالمي",
      "⚡ رؤى سريعة بالذكاء الاصطناعي",
    ],
    section1: "ابدأ بتجربة مقابل 1 دولار",
    section2: "الأرصدة الموحّدة",
    section3: "خطط Pro والمؤسسات",
    section4: "استخدام الأرصدة حسب الوكيل",
    trialsTitle: "تجارب بقيمة 1 دولار",
    trialsDesc:
      "يمنح كل حساب تجربة واحدة فقط مقابل 1 دولار. اختر وكيلاً واحداً من Runexa واستكشفه قبل استخدام الأرصدة أو الترقية إلى إحدى الخطط.",
    trialsBadge: "اختر وكيل الذكاء الاصطناعي",
    oneTimeTrial: "تجربة واحدة لكل حساب",
    trialAnalysis: "تحليل مدعوم بالذكاء الاصطناعي",
    trialReassurance:
      "تجربة واحدة فقط بقيمة 1 دولار لكل حساب. وصول فوري بعد التفعيل.",
    startTrial: "ابدأ التجربة",
    creditsTitle: "الأرصدة الموحّدة",
    mostFlexible: "الأكثر مرونة",
    creditsDesc:
      "اشترِ الأرصدة مرة واحدة واستخدمها عبر جميع وكلاء Runexa الذكية. مثالية للمستخدمين الذين لا يحتاجون إلى اشتراك شهري.",
    bestValue: "أفضل قيمة",
    oneTime: "دفعة واحدة",
    globalCredits: "الأرصدة",
    buyCredits: "شراء الأرصدة",
    plansTitle: "خطط Pro والمؤسسات",
    plansDesc:
      "اشتراك واحد يمنحك الوصول إلى جميع وكلاء Runexa الذكية. لا حاجة لاشتراكات منفصلة.",
    globalPro: "Runexa Pro",
    bestForProfessionals: "الأفضل للمحترفين",
    proValueNote:
      "مصممة للمستخدمين المنتظمين الذين يعتمدون على عدة وكلاء ذكاء اصطناعي.",
    proDesc:
      "للأفراد والمحترفين الذين يحتاجون إلى وصول مستمر إلى عدة وكلاء ذكاء اصطناعي.",
    month: "/شهر",
    proFeatures: [
      "500 رصيد شهرياً",
      "صالحة للاستخدام على جميع الوكلاء",
      "معالجة ذات أولوية",
      "الوصول إلى وكلاء القانون والمالية والدراسة والأعمال",
      "الوكلاء الجدد مشمولون",
    ],

    proUsage:
      "يتضمن ما يصل إلى 100 جلسة تعلم، أو 71 تحليلاً مالياً، أو 41 مراجعة قانونية، أو 16 تحليلاً لاتخاذ القرارات التجارية شهرياً.",

    proCreditsPolicy:
      "يتم تجديد أرصدة الاشتراك شهرياً ولا يتم ترحيلها إلى دورة الفوترة التالية.",

    proPurchasedCredits:
      "حزم الأرصدة المشتراة لا تنتهي صلاحيتها.",

    upgradePro: "الترقية إلى Runexa Pro",
    enterprise: "المؤسسات",
    premiumDesc:
      "للفرق والمؤسسات التعليمية والشركات والمنظمات.",
    custom: "مخصص",
    tailoredPricing: "تسعير مخصص",
    premiumFeatures: [
      "مساحات عمل آمنة",
      "تعاون الفرق",
      "سير عمل ذكاء اصطناعي خاصة",
      "إدارة المؤسسات",
      "دعم ذو أولوية",
    ],
    contactSales: "تواصل مع فريق المبيعات",
    creditCostsTitle: "استخدام الأرصدة حسب الوكيل",
    creditCostsDesc:
      "رصيد واحد يعمل عبر جميع وكلاء Runexa الذكية.",
    creditComplexityNote:
      "يعتمد استهلاك الأرصدة على تعقيد التحليل.",
    creditsPerAnalysis: "أرصدة لكل تحليل",
    infoCards: [
    {
      title: "وصول مرن",
      desc:
        "ابدأ بتجربة واحدة فقط مقابل 1 دولار لكل حساب، أو اشترِ أرصدة، أو اختر إحدى الخطط المناسبة لك.",
    },

    {
      title: "رصيد موحّد",
      desc:
        "يعمل نفس الرصيد عبر جميع وكلاء Runexa الذكية.",
    },

    {
      title: "خطة واحدة لجميع الوكلاء",
      desc:
        "يمنحك اشتراك Runexa Pro الوصول إلى كامل منصة Runexa ووكلائها الذكية.",
    },
  ],
    disclaimer:
      "⚠️ يقدم وكلاء Runexa للذكاء الاصطناعي تحليلات ورؤى داعمة لاتخاذ القرار. يجب دائماً التحقق من القرارات القانونية أو المالية أو الأكاديمية أو التجارية المهمة بالاستعانة بمختصين مؤهلين أو مصادر رسمية.",

    messages: {
      trial: (agentName: string) =>
        `تابع إلى صفحة الدفع لتفعيل ${agentName}.`,

      credits:
        "تابع إلى صفحة الدفع لشراء الأرصدة.",

      pro:
        "تابع إلى صفحة الدفع لتفعيل اشتراكك.",
    },
   agents: [
    {
      slug: "legal",
      name: "Runexa Legal Agent",
      description:
        "حدد المخاطر التعاقدية والالتزامات والبنود المهمة قبل التوقيع.",
      trialOutcome: "تحليل عقد مدعوم بالذكاء الاصطناعي",
      credits: 12,
      gradient: "from-slate-950 to-blue-700",
    },
    {
      slug: "finance",
      name: "Runexa Finance Coach",
      description:
        "افهم أنماط الإنفاق، وقلّل الهدر، وحسّن قراراتك المالية.",
      trialOutcome: "تحليل مالي مدعوم بالذكاء الاصطناعي",
      credits: 7,
      gradient: "from-emerald-700 to-teal-500",
    },
    {
      slug: "study",
      name: "Runexa Study Agent",
      description:
        "حوّل موادك الدراسية إلى ملخصات واختبارات وخطط تعلّم.",
      trialOutcome: "جلسة تعلّم مدعومة بالذكاء الاصطناعي",
      credits: 5,
      gradient: "from-indigo-700 to-violet-500",
    },
    {
      slug: "business",
      name: "Runexa Business Decision Agent",
      description:
        "قيّم الفرص والمخاطر والقرارات الاستراتيجية للأعمال.",
      trialOutcome: "تحليل أعمال مدعوم بالذكاء الاصطناعي",
      credits: 30,
      gradient: "from-amber-700 to-orange-500",
    },
  ],
  creditPacks: [
    {
      name: "Starter",
      credits: 50,
      price: "$9",
      description:
        "مثالي لاستكشاف عدة وكلاء ذكاء اصطناعي من Runexa والاستخدام العرضي.",
    },
    {
      name: "Growth",
      credits: 150,
      price: "$24",
      description:
        "أفضل قيمة للمستخدمين المنتظمين الذين يستخدمون عدة وكلاء ذكاء اصطناعي.",
      highlighted: true,
    },
    {
      name: "Scale",
      credits: 500,
      price: "$75",
      description:
        "مصمم للمحترفين والفرق وأحجام الاستخدام الأكبر.",
    },
  ],
  },
};

export default function PricingClient({
  initialLanguage = "en",
  lockInitialLanguage = false,
}: {
  initialLanguage?: Language;
  lockInitialLanguage?: boolean;
}) {
  const [language, setLanguage] = useState<Language>(initialLanguage);
  const [message, setMessage] = useState("");

  const t = labels[language] || labels.en;
  const agents = t.agents;
  const creditPacks = t.creditPacks;

  useEffect(() => {
    if (lockInitialLanguage) {
      setLanguage(initialLanguage);
      return;
    }

    const saved = localStorage.getItem("locale") as Language | null;

    if (saved && labels[saved]) {
      setLanguage(saved);
    } else {
      setLanguage(initialLanguage);
    }

    const handleLocaleChange = () => {
      const updated = localStorage.getItem("locale") as Language | null;

      if (updated && labels[updated]) {
        setLanguage(updated);
      } else {
        setLanguage(initialLanguage);
      }
    };

    window.addEventListener("locale-change", handleLocaleChange);

    return () => {
      window.removeEventListener("locale-change", handleLocaleChange);
    };
  }, [initialLanguage, lockInitialLanguage]);

  const requireAuth = () => {
    const token = localStorage.getItem("token");

    if (!token) {
      window.location.href = "/register";
      return false;
    }

    return true;
  };

  const getTrialAlreadyUsedMessage = () => {
    if (language === "fr") {
      return "Votre essai à 1 $ a déjà été utilisé pour ce compte. Vous pouvez continuer avec des crédits ou un abonnement Pro.";
    }

    if (language === "ar") {
      return "لقد تم استخدام تجربة 1 دولار الخاصة بهذا الحساب بالفعل. يمكنك المتابعة باستخدام الأرصدة أو الاشتراك في خطة Pro.";
    }

    return "Your $1 trial has already been used on this account. You can continue with credits or a Pro plan.";
  };

  const getStripeCheckoutErrorMessage = () => {
    if (language === "fr") {
      return "Impossible d’ouvrir la page de paiement Stripe. Veuillez réessayer.";
    }

    if (language === "ar") {
      return "تعذر فتح صفحة الدفع عبر Stripe. يرجى المحاولة مرة أخرى.";
    }

    return "Unable to start Stripe checkout. Please try again.";
  };

  const handleStartTrial = async (agentSlug: string) => {
    if (!requireAuth()) return;

    try {
      const token = localStorage.getItem("token");

      const response = await fetch(
        "https://api.runexa.ai/payments/create-checkout-session",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            product_type: "trial",
            agent_slug: agentSlug,
          }),
        }
      );

      const data = await response.json();

      if (response.status === 409) {
        setMessage(getTrialAlreadyUsedMessage());
        return;
      }

      if (!response.ok) {
        throw new Error(data.detail || "Unable to create checkout session");
      }

      if (data.checkout_url) {
        window.location.href = data.checkout_url;
        return;
      }

      throw new Error("Checkout URL not returned");
    } catch (error: any) {
      console.error(error);

      const errorMessage = String(error?.message || "");

      if (
        errorMessage.includes("already been activated") ||
        errorMessage.includes("already used") ||
        errorMessage.includes("$1 trial")
      ) {
        setMessage(getTrialAlreadyUsedMessage());
        return;
      }

      setMessage(getStripeCheckoutErrorMessage());
    }
  };

  const handleBuyCredits = async (pack: "starter" | "growth" | "scale") => {
    if (!requireAuth()) return;

    try {
      const token = localStorage.getItem("token");

      const response = await fetch(
        "https://api.runexa.ai/payments/create-checkout-session",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            product_type: "credits_pack",
            pack,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Unable to create checkout session");
      }

      if (data.checkout_url) {
        window.location.href = data.checkout_url;
        return;
      }

      throw new Error("Checkout URL not returned");
    } catch (error) {
      console.error(error);
      setMessage(getStripeCheckoutErrorMessage());
    }
  };

  const handleStartApiPlan = async (apiPlan: "api_starter" | "api_pro") => {
    if (!requireAuth()) return;

    try {
      const token = localStorage.getItem("token");

      const response = await fetch(
        "https://api.runexa.ai/payments/create-checkout-session",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            product_type: "api",
            api_plan: apiPlan,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Unable to create checkout session");
      }

      if (data.checkout_url) {
        window.location.href = data.checkout_url;
        return;
      }

      throw new Error("Checkout URL not returned");
    } catch (error) {
      console.error(error);
      setMessage(
        language === "fr"
          ? "Impossible d’ouvrir le paiement API Stripe. Veuillez réessayer."
          : language === "ar"
            ? "تعذر فتح صفحة دفع API عبر Stripe. يرجى المحاولة مرة أخرى."
            : "Unable to start API Stripe checkout. Please try again."
      );
    }
  };

  const handleUpgradePro = async () => {
    if (!requireAuth()) return;

    try {
      const token = localStorage.getItem("token");

      const response = await fetch(
        "https://api.runexa.ai/payments/create-checkout-session",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            product_type: "subscription",
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Unable to create checkout session");
      }

      if (data.checkout_url) {
        window.location.href = data.checkout_url;
        return;
      }

      throw new Error("Checkout URL not returned");
    } catch (error) {
      console.error(error);

      setMessage(getStripeCheckoutErrorMessage());
    }
  };
  return (
    <main
      dir={language === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-white text-slate-950"
    >
      <section className="relative overflow-hidden border-b border-slate-200 bg-gradient-to-br from-slate-950 via-blue-950 to-slate-900">
        <div className="absolute left-1/2 top-0 h-72 w-72 -translate-x-1/2 rounded-full bg-blue-500/20 blur-3xl" />
        <div className="absolute bottom-0 right-10 h-72 w-72 rounded-full bg-cyan-400/10 blur-3xl" />

        <div className="relative mx-auto max-w-6xl px-6 py-24 text-center sm:py-32">
          <span className="inline-flex rounded-full border border-white/15 bg-white/10 px-4 py-2 text-sm font-semibold text-blue-100 backdrop-blur">
            {t.badge}
          </span>

          <h1 className="mx-auto mt-7 max-w-4xl text-4xl font-bold tracking-tight text-white sm:text-6xl">
            {t.title}
          </h1>

          <p className="mx-auto mt-6 max-w-3xl text-lg leading-8 text-blue-100">
            {t.desc}
          </p>

          <p className="mt-4 text-sm font-semibold text-blue-100/90">
            {t.audience}
          </p>

          <p className="mx-auto mt-3 max-w-2xl text-sm text-blue-100/80">
            {t.socialProof}
          </p>

          <div className="mx-auto mt-6 inline-flex rounded-full border border-white/15 bg-white/10 px-4 py-2 text-sm font-semibold text-blue-100 backdrop-blur">
            {t.trustedWorkflow}
          </div>

          <div className="mt-10 flex flex-col items-center justify-center gap-3 sm:flex-row">
            <a
              href="#trials"
              className="w-full rounded-xl bg-white px-6 py-3 text-center text-sm font-bold text-slate-950 shadow-lg shadow-blue-950/30 transition hover:bg-blue-50 sm:w-auto"
            >
              {t.activateTrialCta}
            </a>

            <a
              href="#plans"
              className="w-full rounded-xl border border-white/20 bg-white/5 px-6 py-3 text-center text-sm font-bold text-blue-100/90 backdrop-blur transition hover:bg-white/10 sm:w-auto"
            >
              {t.viewPlans}
            </a>
          </div>
        </div>
      </section>

      <div className="mx-auto max-w-6xl px-6 py-16">
        {message && (
          <div className="mb-8 rounded-2xl border border-amber-200 bg-amber-50 px-5 py-4 text-center text-sm font-medium text-amber-800">
            {message}
          </div>
        )}

        <section className="mb-16">
          <h2 className="text-2xl font-bold tracking-tight">
            {t.whyTitle}
          </h2>

          <div className="mt-6 grid gap-4 md:grid-cols-4">
            {t.whyCards.map((item: { title: string; desc: string }) => (
              <div
                key={item.title}
                className="rounded-2xl border border-slate-200 bg-slate-50 p-5 text-sm text-slate-600 transition-all duration-300 hover:border-blue-200 hover:bg-white hover:shadow-md"
              >
                <strong className="block text-slate-950">
                  ✔ {item.title}
                </strong>
                <span className="mt-2 block leading-6">
                  {item.desc}
                </span>
              </div>
            ))}
          </div>
        </section>

        <section id="trials" className="space-y-8">
          <div className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
            <div>
              <p className="text-sm font-bold uppercase tracking-[0.25em] text-blue-600">
                {t.section1}
              </p>
              <h2 className="mt-2 text-3xl font-bold tracking-tight">
                {t.trialsTitle}
              </h2>
              <p className="mt-3 max-w-2xl text-slate-600">{t.trialsDesc}</p>
            </div>

            <div className="rounded-2xl border border-blue-100 bg-blue-50 px-4 py-3 text-sm font-semibold text-blue-700">
              {t.trialsBadge}
            </div>
          </div>

          <div className="grid gap-5 md:grid-cols-4">
            {agents.map((agent) => (
              <div
                key={agent.slug}
                className="group overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm transition-all duration-300 hover:-translate-y-1 hover:border-blue-200 hover:shadow-xl"
              >
                <div className={`h-2 bg-gradient-to-r ${agent.gradient}`} />

                <div className="flex h-full flex-col p-6">
                  <div
                    className={`mb-5 flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br ${agent.gradient} text-sm font-bold text-white shadow-lg`}
                  >
                    AI
                  </div>

                  <h3 className="text-lg font-bold text-slate-950">
                    {agent.name}
                  </h3>

                  <p className="mt-2 min-h-[60px] text-sm leading-6 text-slate-600">
                    {agent.description}
                  </p>

                  <div className="mt-5">
                    <span className="text-4xl font-bold">$1</span>
                  </div>

                  <p className="mt-2 text-sm font-medium text-slate-600">
                    {agent.trialOutcome}
                  </p>

                  <button
                    onClick={() => handleStartTrial(agent.slug)}
                    className="mt-6 rounded-xl bg-slate-950 px-5 py-3 text-sm font-bold text-white transition hover:bg-slate-800"
                  >
                    {t.startTrial}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="mt-20 space-y-8">
          <div>
            <p className="text-sm font-bold uppercase tracking-[0.25em] text-blue-600">
              {t.section2}
            </p>
            <div className="mt-2 flex flex-wrap items-center gap-3">
              <h2 className="text-3xl font-bold tracking-tight">
                {t.creditsTitle}
              </h2>
              <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-bold text-emerald-700 ring-1 ring-emerald-100">
                {t.mostFlexible}
              </span>
            </div>
            <p className="mt-3 max-w-2xl text-slate-600">{t.creditsDesc}</p>
          </div>

          <div className="grid gap-6 md:grid-cols-3">
            {creditPacks.map((pack) => (
              <div
                key={pack.name}
                className={`relative rounded-3xl border bg-white p-8 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-xl ${
                  pack.highlighted
                    ? "scale-[1.02] border-blue-600 bg-gradient-to-b from-white to-blue-50/40 shadow-2xl shadow-blue-100 ring-2 ring-blue-500/20"
                    : "scale-[0.98] border-slate-200"
                }`}
              >
                {pack.highlighted && (
                  <div className="absolute -top-3 left-1/2 flex -translate-x-1/2 gap-2">
                    <span className="rounded-full bg-blue-600 px-3 py-1 text-xs font-bold text-white">
                      {t.bestValue}
                    </span>
                    <span className="rounded-full bg-slate-950 px-3 py-1 text-xs font-bold text-white">
                      {t.mostPopular}
                    </span>
                  </div>
                )}

                <h3 className="text-lg font-bold">{pack.name}</h3>
                <p className="mt-2 text-sm leading-6 text-slate-600">
                  {pack.description}
                </p>

                <div className="mt-6 flex items-end gap-2">
                  <span className="text-4xl font-bold">{pack.price}</span>
                  <span className="pb-1 text-sm text-slate-500">
                    {t.oneTime}
                  </span>
                </div>

                <p className="mt-2 text-sm font-semibold text-slate-700">
                  {pack.credits} {t.globalCredits}
                </p>

                <button
                  onClick={() =>
                    handleBuyCredits(
                      pack.name.toLowerCase() === "starter"
                        ? "starter"
                        : pack.name.toLowerCase() === "growth"
                          ? "growth"
                          : "scale"
                    )
                  }
                  className={`mt-7 w-full rounded-xl px-5 py-3 text-sm font-bold transition ${
                    pack.highlighted
                      ? "bg-blue-600 text-white hover:bg-blue-700"
                      : "bg-slate-950 text-white hover:bg-slate-800"
                  }`}
                >
                  {t.buyCredits}
                </button>
              </div>
            ))}
          </div>
        </section>

        <section id="plans" className="mt-20">
          <div>
            <p className="text-sm font-bold uppercase tracking-[0.25em] text-blue-600">
              {t.section3}
            </p>
            <h2 className="mt-2 text-3xl font-bold tracking-tight">
              {t.plansTitle}
            </h2>
            <p className="mt-3 max-w-2xl text-slate-600">{t.plansDesc}</p>
          </div>

          <div className="mt-8 grid gap-6 lg:grid-cols-2">
            <div className="relative overflow-hidden rounded-3xl border-2 border-slate-950 bg-slate-950 p-8 text-white shadow-2xl shadow-slate-200">
              <div className="absolute right-0 top-0 h-48 w-48 rounded-full bg-blue-500/20 blur-3xl" />

              <div className="relative">
                <div className="flex flex-wrap gap-2">
                  <span className="rounded-full bg-white/10 px-3 py-1 text-xs font-bold text-blue-100">
                    {t.globalPro}
                  </span>
                  <span className="rounded-full bg-blue-400/20 px-3 py-1 text-xs font-bold text-blue-100">
                    {t.bestForProfessionals}
                  </span>
                  <span className="rounded-full bg-white px-3 py-1 text-xs font-bold text-slate-950">
                    {t.mostPopular}
                  </span>
                  <span className="rounded-full bg-emerald-400/20 px-3 py-1 text-xs font-bold text-emerald-100">
                    {t.powerUserBadge}
                  </span>
                </div>

                <p className="mt-4 text-sm font-semibold text-blue-100/90">
                  {t.proValueNote}
                </p>

                <h3 className="mt-5 text-2xl font-bold">Pro</h3>
                <p className="mt-2 text-slate-300">{t.proDesc}</p>

                <div className="mt-7 flex items-end gap-2">
                  <span className="text-5xl font-bold">$49</span>
                  <span className="pb-2 text-slate-300">{t.month}</span>
                </div>

                <ul className="mt-8 space-y-4 text-sm text-slate-100">
                  {t.proFeatures.map((feature: string) => (
                    <li key={feature}>✔ {feature}</li>
                  ))}
                </ul>

                <div className="mt-6 space-y-3 border-t border-white/10 pt-6 text-sm leading-6 text-slate-300">
                  <p>{t.proUsage}</p>
                  <p>{t.proCreditsPolicy}</p>
                  <p>{t.proPurchasedCredits}</p>
                </div>

                <button
                  onClick={handleUpgradePro}
                  className="mt-8 w-full rounded-xl bg-white px-5 py-3 text-sm font-bold text-slate-950 transition hover:bg-blue-50"
                >
                  {t.upgradePro}
                </button>
              </div>
            </div>

            <div className="rounded-3xl border border-slate-300 bg-gradient-to-b from-white to-slate-50 p-8 shadow-sm">
              <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-bold text-slate-700">
                {t.enterprise}
              </span>

              <h3 className="mt-5 text-2xl font-bold">Premium</h3>
              <p className="mt-2 text-slate-600">{t.premiumDesc}</p>

              <div className="mt-7 text-5xl font-bold">{t.custom}</div>
              <p className="mt-2 text-sm text-slate-500">{t.tailoredPricing}</p>

              <ul className="mt-8 space-y-4 text-sm text-slate-700">
                {t.premiumFeatures.map((feature: string) => (
                  <li key={feature}>✔ {feature}</li>
                ))}
              </ul>

              <a
                href="/contact"
                className="mt-8 block w-full rounded-xl border border-slate-300 px-5 py-3 text-center text-sm font-bold text-slate-950 transition hover:bg-slate-50"
              >
                {t.contactSales}
              </a>
            </div>
          </div>
        </section>

        <section className="mt-20">
          <div>
            <p className="text-sm font-bold uppercase tracking-[0.25em] text-blue-600">
              {t.apiSectionBadge}
            </p>
            <h2 className="mt-2 text-3xl font-bold tracking-tight">
              {t.apiSectionTitle}
            </h2>
            <p className="mt-3 max-w-2xl text-slate-600">
              {t.apiSectionDesc}
            </p>
          </div>

          <div className="mt-8 grid gap-6 lg:grid-cols-3">
            {t.apiPlans.map((plan) => (
              <div
                key={plan.name}
                className={`rounded-3xl border p-8 shadow-sm transition-all duration-300 hover:shadow-xl ${
                  plan.highlighted
                    ? "border-blue-600 bg-blue-50 ring-2 ring-blue-500/20"
                    : "border-slate-200 bg-white"
                }`}
              >
                <h3 className="text-xl font-bold">{plan.name}</h3>
                <p className="mt-3 text-sm leading-6 text-slate-600">{plan.desc}</p>

                <div className="mt-6 text-4xl font-bold">{plan.price}</div>

                <div className="mt-5 space-y-2 text-sm font-semibold text-slate-700">
                  <p>{plan.credits}</p>
                  <p>{plan.rate}</p>
                </div>

                <ul className="mt-6 space-y-3 text-sm text-slate-600">
                  {plan.features.map((feature) => (
                    <li key={feature}>✔ {feature}</li>
                  ))}
                </ul>

                {plan.name === "Enterprise API" ? (
                  <a
                    href="/contact"
                    className="mt-8 block w-full rounded-xl border border-slate-300 px-5 py-3 text-center text-sm font-bold text-slate-950 transition hover:bg-slate-50"
                  >
                    {t.apiContactSales}
                  </a>
                ) : (
                  <button
                    onClick={() =>
                      handleStartApiPlan(
                        plan.name === "API Pro" ? "api_pro" : "api_starter"
                      )
                    }
                    className={`mt-8 w-full rounded-xl px-5 py-3 text-sm font-bold transition ${
                      plan.highlighted
                        ? "bg-blue-600 text-white hover:bg-blue-700"
                        : "bg-slate-950 text-white hover:bg-slate-800"
                    }`}
                  >
                    {t.apiStartPlan}
                  </button>
                )}
              </div>
            ))}
          </div>
        </section>

        <section className="mt-20">
          <div className="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">
            <div className="border-b border-slate-200 bg-slate-50 p-6">
              <p className="text-sm font-bold uppercase tracking-[0.25em] text-blue-600">
                {t.section4}
              </p>
              <h2 className="mt-2 text-3xl font-bold tracking-tight">
                {t.creditCostsTitle}
              </h2>
              <p className="mt-3 text-slate-600">{t.creditCostsDesc}</p>
              <p className="mt-2 text-sm text-slate-500">
                {t.creditComplexityNote}
              </p>
            </div>

            <div className="divide-y divide-slate-100">
              {agents.map((agent) => (
                <div
                  key={agent.slug}
                  className="grid gap-4 p-6 sm:grid-cols-[1fr_auto] sm:items-center"
                >
                  <div>
                    <h3 className="font-bold text-slate-950">{agent.name}</h3>
                    <p className="mt-1 text-sm text-slate-500">
                      {agent.description}
                    </p>
                  </div>

                  <div className="rounded-2xl bg-slate-950 px-5 py-3 text-center text-sm font-bold text-white">
                    {agent.credits} {t.creditsPerAnalysis}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="mt-16 grid gap-4 md:grid-cols-3">
          {t.infoCards.map((card: { title: string; desc: string }) => (
            <div
              key={card.title}
              className="rounded-2xl border border-slate-200 bg-slate-50 p-5 text-sm text-slate-600"
            >
              <strong className="block text-slate-950">{card.title}</strong>
              {card.desc}
            </div>
          ))}
        </section>

        <section className="mt-16 grid gap-4 md:grid-cols-3">
          {t.microTrust.map((item: string) => (
            <div
              key={item}
              className="rounded-2xl border border-slate-200 bg-white p-5 text-center text-sm font-medium text-slate-700 shadow-sm"
            >
              {item}
            </div>
          ))}
        </section>

        <p className="mt-10 text-center text-sm font-medium text-slate-500">
          {t.workflowLine}
        </p>

        <div className="mt-16 rounded-2xl border border-amber-200 bg-amber-50 p-5 text-center text-sm text-amber-800">
          {t.disclaimer}
        </div>
      </div>
    </main>
  );
}
