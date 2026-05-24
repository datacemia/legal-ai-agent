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

const labels: Record<Language, any> = {
  en: {
    badge: "Global pricing for every Runexa AI agent",
    title: "One account. All agents. Simple global billing.",
    desc: "Access every Runexa AI agent with one account. Start with a $1 trial, global credits, or a Pro subscription.",
    socialProof: "Used for legal analysis, personal finance, learning, and business decisions.",
    workflowLine: "Built for real-world AI workflows.",
    powerUserBadge: "Recommended for power users",
    activateTrialCta: "Activate any agent with a one-time $1 trial",
    viewPlans: "View Pro & Premium",
    audience: "For individuals, professionals, and organizations",
    trustedWorkflow: "Upload → AI analysis → actionable insights",
    whyTitle: "Why people use Runexa",
    whyCards: [
      {
        title: "Detect risky contract clauses",
        desc: "Review contracts and obligations before signing.",
      },
      {
        title: "Understand spending habits",
        desc: "Find waste, subscriptions, and financial patterns.",
      },
      {
        title: "Learn faster",
        desc: "Turn study material into summaries and revision systems.",
      },
      {
        title: "Make smarter business decisions",
        desc: "Analyze opportunities, risks, and strategic choices.",
      },
    ],
    mostPopular: "Most popular",
    microTrust: [
      "🔒 Secure AI workspace",
      "🌍 Global access",
      "⚡ Fast AI analysis",
    ],
    section1: "Start with a $1 AI trial",
    section2: "Global AI credits",
    section3: "Professional plans",
    section4: "Credit usage by AI agent",
    trialsTitle: "$1 Trials by Agent",
    trialsDesc:
      "Each agent has its own one-time $1 activation. Try exactly the agent you need before using global credits or a plan.",
    trialsBadge: "Choose the agent you need",
    oneTimeTrial: "one-time trial",
    trialAnalysis: "One focused AI analysis",
    trialReassurance: "Instant activation when payments are available.",
    startTrial: "Start trial",
    creditsTitle: "Global Credits",
    mostFlexible: "Most flexible",
    creditsDesc:
      "Buy credits once and use them on all Runexa agents. Credits are the flexible option for users who do not need a monthly plan.",
    bestValue: "Best value",
    oneTime: "one-time",
    globalCredits: "global credits",
    buyCredits: "Buy credits",
    plansTitle: "Pro / Premium Plans",
    plansDesc:
      "One global subscription covers all agents. No separate Pro plan per agent.",
    globalPro: "Global Pro",
    bestForProfessionals: "Best for professionals",
    proValueNote: "For regular users of multiple AI agents.",
    proDesc:
      "For individuals and professionals who use multiple agents regularly.",
    month: "/month",
    proFeatures: [
      "200 credits/month",
      "Usable on all agents",
      "Priority processing",
      "Access to Legal, Study, Finance, and Business agents",
      "Future agents included when available",
    ],
    upgradePro: "Upgrade to Pro",
    enterprise: "Enterprise",
    premiumDesc: "For teams, companies, schools, and multi-user organizations.",
    custom: "Custom",
    tailoredPricing: "tailored pricing",
    premiumFeatures: [
      "Secure workspaces",
      "Team collaboration",
      "Private AI workflows",
      "Organization management",
      "Priority support",
    ],
    contactSales: "Contact sales",
    creditCostsTitle: "Agent credit costs",
    creditCostsDesc:
      "Credits are global. The same balance works across every agent.",
    creditComplexityNote: "The cost depends on the complexity of the AI analysis.",
    creditsPerAnalysis: "credits / analysis",
    infoCards: [
      {
        title: "Trials are optional",
        desc: "You can activate a $1 trial for one agent or skip directly to credits or Pro.",
      },
      {
        title: "Credits are global",
        desc: "Buy once and use the same balance for Legal, Study, Finance, or Business.",
      },
      {
        title: "Pro is global",
        desc: "One monthly Pro plan includes credits usable across all agents.",
      },
    ],
    disclaimer:
      "⚠️ Runexa AI agents provide informational and decision-support output. Always verify important legal, financial, academic, or business decisions with qualified professionals or official sources.",
    messages: {
      trial: (agentName: string) =>
        `$1 trial payment for ${agentName} is not configured yet. Payments are temporarily unavailable during platform rollout.`,
      credits:
        "Payments are temporarily unavailable during platform rollout. Global credits will be available soon.",
      pro: "Pro subscription is not configured yet. Payments are temporarily unavailable during platform rollout.",
    },
    agents: [
      {
        slug: "legal",
        name: "Runexa Legal Agent",
        description:
          "Detect risky clauses before signing contracts.",
        trialOutcome: "Analyze one contract",
        credits: 12,
        gradient: "from-slate-950 to-blue-700",
      },
      {
        slug: "finance",
        name: "Runexa Finance Coach",
        description: "Understand spending, reduce waste, and improve financial habits.",
        trialOutcome: "Analyze one bank statement",
        credits: 7,
        gradient: "from-emerald-700 to-teal-500",
      },
      {
        slug: "study",
        name: "Runexa Study Agent",
        description: "Learn faster with AI summaries and revision systems.",
        trialOutcome: "Generate one AI study session",
        credits: 5,
        gradient: "from-indigo-700 to-violet-500",
      },
      {
        slug: "business",
        name: "Runexa Business Decision Agent",
        description: "Analyze opportunities, risks, and strategic decisions.",
        trialOutcome: "Run one business analysis",
        credits: 30,
        gradient: "from-amber-700 to-orange-500",
      },
    ] as Agent[],
    creditPacks: [
      {
        name: "Starter",
        credits: 50,
        price: "$9",
        description: "Perfect for testing multiple Runexa agents.",
      },
      {
        name: "Growth",
        credits: 150,
        price: "$24",
        description: "Best value for regular multi-agent usage.",
        highlighted: true,
      },
      {
        name: "Scale",
        credits: 500,
        price: "$89",
        description: "Built for professionals and advanced workloads.",
      },
    ] as CreditPack[],
  },

  fr: {
    badge: "Tarification globale pour tous les agents IA Runexa",
    title: "Un compte. Tous les agents. Une facturation simple et globale.",
    desc: "Accédez à tous les agents IA Runexa avec un seul compte. Commencez avec un essai à 1 $, des crédits globaux ou un abonnement Pro.",
    socialProof: "Utilisé pour l’analyse juridique, la finance personnelle, l’apprentissage et les décisions business.",
    workflowLine: "Conçu pour les workflows IA du monde réel.",
    powerUserBadge: "Recommandé pour les utilisateurs avancés",
    activateTrialCta: "Activer un agent avec un essai unique à 1 $",
    viewPlans: "Voir Pro & Premium",
    audience: "Pour les particuliers, les professionnels et les organisations",
    trustedWorkflow: "Téléversement → Analyse IA → Insights actionnables",
    whyTitle: "Pourquoi utiliser Runexa",
    whyCards: [
      {
        title: "Détecter les clauses risquées",
        desc: "Analysez les contrats et obligations avant signature.",
      },
      {
        title: "Comprendre les dépenses",
        desc: "Identifiez le gaspillage, les abonnements et les habitudes financières.",
      },
      {
        title: "Apprendre plus vite",
        desc: "Transformez vos contenus en résumés et systèmes de révision.",
      },
      {
        title: "Décider plus intelligemment",
        desc: "Analysez les opportunités, les risques et les choix stratégiques.",
      },
    ],
    mostPopular: "Le plus populaire",
    microTrust: [
      "🔒 Espace IA sécurisé",
      "🌍 Accès global",
      "⚡ Analyse IA rapide",
    ],
    section1: "Commencez avec un essai IA à 1 $",
    section2: "Crédits IA globaux",
    section3: "Plans professionnels",
    section4: "Utilisation des crédits par agent IA",
    trialsTitle: "Essais à 1 $ par agent",
    trialsDesc:
      "Chaque agent dispose de sa propre activation unique à 1 $. Essayez exactement l’agent dont vous avez besoin avant d’utiliser des crédits globaux ou un abonnement.",
    trialsBadge: "Choisissez l’agent dont vous avez besoin",
    oneTimeTrial: "essai unique",
    trialAnalysis: "Une analyse IA ciblée",
    trialReassurance: "Activation instantanée dès disponibilité des paiements.",
    startTrial: "Démarrer l’essai",
    creditsTitle: "Crédits globaux",
    mostFlexible: "Le plus flexible",
    creditsDesc:
      "Achetez des crédits une seule fois et utilisez-les sur tous les agents Runexa. Les crédits sont l’option flexible pour les utilisateurs qui n’ont pas besoin d’un abonnement mensuel.",
    bestValue: "Meilleur choix",
    oneTime: "paiement unique",
    globalCredits: "crédits globaux",
    buyCredits: "Acheter des crédits",
    plansTitle: "Plans Pro / Premium",
    plansDesc:
      "Un seul abonnement global couvre tous les agents. Aucun plan Pro séparé par agent.",
    globalPro: "Global Pro",
    bestForProfessionals: "Idéal pour les professionnels",
    proValueNote: "Pour les utilisateurs réguliers de plusieurs agents IA.",
    proDesc:
      "Pour les particuliers et professionnels qui utilisent régulièrement plusieurs agents.",
    month: "/mois",
    proFeatures: [
      "200 crédits/mois",
      "Utilisables sur tous les agents",
      "Traitement prioritaire",
      "Accès aux agents Legal, Study, Finance et Business",
      "Futurs agents inclus dès leur disponibilité",
    ],
    upgradePro: "Passer à Pro",
    enterprise: "Entreprise",
    premiumDesc:
      "Pour les équipes, entreprises, écoles et organisations multi-utilisateurs.",
    custom: "Sur mesure",
    tailoredPricing: "tarification personnalisée",
    premiumFeatures: [
      "Workspaces sécurisés",
      "Collaboration équipe",
      "Workflows IA privés",
      "Gestion organisationnelle",
      "Support prioritaire",
    ],
    contactSales: "Contacter l’équipe commerciale",
    creditCostsTitle: "Coût en crédits par agent",
    creditCostsDesc:
      "Les crédits sont globaux. Le même solde fonctionne sur chaque agent.",
    creditComplexityNote: "Le coût dépend de la complexité de l’analyse IA.",
    creditsPerAnalysis: "crédits / analyse",
    infoCards: [
      {
        title: "Les essais sont optionnels",
        desc: "Vous pouvez activer un essai à 1 $ pour un agent ou passer directement aux crédits ou au plan Pro.",
      },
      {
        title: "Les crédits sont globaux",
        desc: "Achetez une fois et utilisez le même solde pour Legal, Study, Finance ou Business.",
      },
      {
        title: "Pro est global",
        desc: "Un seul plan Pro mensuel inclut des crédits utilisables sur tous les agents.",
      },
    ],
    disclaimer:
      "⚠️ Les agents IA Runexa fournissent des analyses informatives et d’aide à la décision. Vérifiez toujours les décisions juridiques, financières, académiques ou commerciales importantes auprès de professionnels qualifiés ou de sources officielles.",
    messages: {
      trial: (agentName: string) =>
        `Le paiement d’essai à 1 $ pour ${agentName} n’est pas encore configuré. Les paiements sont temporairement indisponibles pendant le déploiement de la plateforme.`,
      credits:
        "Les paiements sont temporairement indisponibles pendant le déploiement de la plateforme. Les crédits globaux seront bientôt disponibles.",
      pro: "L’abonnement Pro n’est pas encore configuré. Les paiements sont temporairement indisponibles pendant le déploiement de la plateforme.",
    },
    agents: [
      {
        slug: "legal",
        name: "Runexa Legal Agent",
        description:
          "Détectez les clauses risquées avant de signer des contrats.",
        trialOutcome: "Analyser un contrat",
        credits: 12,
        gradient: "from-slate-950 to-blue-700",
      },
      {
        slug: "finance",
        name: "Runexa Finance Coach",
        description:
          "Comprenez vos dépenses, réduisez le gaspillage et améliorez vos habitudes financières.",
        trialOutcome: "Analyser un relevé bancaire",
        credits: 7,
        gradient: "from-emerald-700 to-teal-500",
      },
      {
        slug: "study",
        name: "Runexa Study Agent",
        description: "Apprenez plus vite avec des résumés IA et des systèmes de révision.",
        trialOutcome: "Générer une session d’étude IA",
        credits: 5,
        gradient: "from-indigo-700 to-violet-500",
      },
      {
        slug: "business",
        name: "Runexa Business Decision Agent",
        description:
          "Analysez les opportunités, les risques et les décisions stratégiques.",
        trialOutcome: "Lancer une analyse business",
        credits: 30,
        gradient: "from-amber-700 to-orange-500",
      },
    ] as Agent[],
    creditPacks: [
      {
        name: "Starter",
        credits: 50,
        price: "$9",
        description: "Parfait pour tester plusieurs agents Runexa.",
      },
      {
        name: "Growth",
        credits: 150,
        price: "$24",
        description:
          "Le meilleur choix pour une utilisation régulière multi-agents.",
        highlighted: true,
      },
      {
        name: "Scale",
        credits: 500,
        price: "$89",
        description: "Conçu pour les professionnels et les charges avancées.",
      },
    ] as CreditPack[],
  },

  ar: {
    badge: "منصة موحّدة لجميع وكلاء Runexa الذكية",
    title: "حساب واحد. جميع الوكلاء. تجربة موحّدة.",
    desc: "من حساب واحد، يمكنك الوصول إلى جميع وكلاء Runexa الذكية. ابدأ بتجربة 1 دولار أو استخدم الأرصدة الموحّدة أو خطة Pro.",
    socialProof: "يُستخدم للتحليل القانوني، والمالية الشخصية، والتعلّم، وقرارات الأعمال.",
    workflowLine: "مصمم لسير العمل الحقيقي بالذكاء الاصطناعي.",
    powerUserBadge: "موصى به للمستخدمين المتقدمين",
    activateTrialCta: "تفعيل أي وكيل بتجربة واحدة بقيمة 1 دولار",
    viewPlans: "عرض Pro وPremium",
    audience: "للأفراد والمحترفين والمؤسسات",
    trustedWorkflow: "رفع الملفات → تحليل بالذكاء الاصطناعي → رؤى قابلة للتنفيذ",
    whyTitle: "لماذا يختار المستخدمون Runexa",
    whyCards: [
      {
        title: "اكتشاف البنود الخطرة",
        desc: "راجع العقود والالتزامات قبل التوقيع.",
      },
      {
        title: "فهم عادات الإنفاق",
        desc: "اكتشف الهدر والاشتراكات والأنماط المالية.",
      },
      {
        title: "التعلّم بشكل أسرع",
        desc: "حوّل المحتوى الدراسي إلى ملخصات وأنظمة مراجعة.",
      },
      {
        title: "قرارات أعمال أذكى",
        desc: "حلّل الفرص والمخاطر والخيارات الاستراتيجية.",
      },
    ],
    mostPopular: "الأكثر شعبية",
    microTrust: [
      "🔒 مساحة ذكاء اصطناعي آمنة",
      "🌍 وصول عالمي",
      "⚡ تحليل سريع بالذكاء الاصطناعي",
    ],
    section1: "ابدأ بتجربة ذكاء اصطناعي مقابل 1 دولار",
    section2: "أرصدة ذكاء اصطناعي موحّدة",
    section3: "خطط احترافية",
    section4: "استخدام الأرصدة حسب وكيل الذكاء الاصطناعي",
    trialsTitle: "تجارب بقيمة 1 دولار حسب الوكيل",
    trialsDesc:
      "لكل وكيل تفعيل تجريبي خاص بقيمة 1 دولار لمرة واحدة. جرّب الوكيل الذي تحتاجه قبل استخدام الأرصدة الموحّدة أو الاشتراك.",
    trialsBadge: "اختر الوكيل الذي تحتاجه",
    oneTimeTrial: "تجربة لمرة واحدة",
    trialAnalysis: "تحليل ذكاء اصطناعي مركّز",
    trialReassurance: "تفعيل فوري عند توفر المدفوعات.",
    startTrial: "بدء التجربة",
    creditsTitle: "الأرصدة الموحّدة",
    mostFlexible: "الأكثر مرونة",
    creditsDesc:
      "اشترِ الأرصدة مرة واحدة واستخدمها على جميع وكلاء Runexa. الأرصدة هي الخيار المرن للمستخدمين الذين لا يحتاجون إلى اشتراك شهري.",
    bestValue: "أفضل قيمة",
    oneTime: "دفعة واحدة",
    globalCredits: "أرصدة موحّدة",
    buyCredits: "شراء الأرصدة",
    plansTitle: "خطط Pro / Premium",
    plansDesc:
      "اشتراك عالمي واحد يغطي جميع الوكلاء. لا توجد خطة Pro منفصلة لكل وكيل.",
    globalPro: "Global Pro",
    bestForProfessionals: "الأفضل للمحترفين",
    proValueNote: "للمستخدمين المنتظمين لعدة وكلاء ذكاء اصطناعي.",
    proDesc: "للأفراد والمحترفين الذين يستخدمون عدة وكلاء بانتظام.",
    month: "/شهر",
    proFeatures: [
      "200 رصيد/شهر",
      "صالحة للاستخدام على جميع الوكلاء",
      "معالجة ذات أولوية",
      "الوصول إلى وكلاء Legal وStudy وFinance وBusiness",
      "تشمل الوكلاء المستقبليين عند توفرهم",
    ],
    upgradePro: "الترقية إلى Pro",
    enterprise: "المؤسسات",
    premiumDesc: "للفرق والشركات والمدارس والمؤسسات متعددة المستخدمين.",
    custom: "مخصص",
    tailoredPricing: "تسعير مخصص",
    premiumFeatures: [
      "مساحات عمل آمنة",
      "تعاون الفرق",
      "سير عمل ذكاء اصطناعي خاص",
      "إدارة المؤسسات",
      "دعم ذو أولوية",
    ],
    contactSales: "التواصل مع فريق المبيعات",
    creditCostsTitle: "تكلفة الأرصدة حسب الوكيل",
    creditCostsDesc: "الأرصدة موحّدة. نفس الرصيد يعمل على كل وكيل.",
    creditComplexityNote: "تعتمد التكلفة على تعقيد تحليل الذكاء الاصطناعي.",
    creditsPerAnalysis: "رصيد / تحليل",
    infoCards: [
      {
        title: "التجارب اختيارية",
        desc: "يمكنك تفعيل تجربة بقيمة 1 دولار لوكيل واحد أو الانتقال مباشرة إلى الأرصدة أو خطة Pro.",
      },
      {
        title: "الأرصدة موحّدة",
        desc: "اشترِ مرة واحدة واستخدم نفس الرصيد مع Legal أو Study أو Finance أو Business.",
      },
      {
        title: "خطة Pro موحّدة",
        desc: "خطة Pro شهرية واحدة تتضمن أرصدة قابلة للاستخدام على جميع الوكلاء.",
      },
    ],
    disclaimer:
      "⚠️ يقدم وكلاء Runexa للذكاء الاصطناعي مخرجات معلوماتية وداعمة لاتخاذ القرار. تحقق دائماً من القرارات القانونية أو المالية أو الأكاديمية أو التجارية المهمة مع مختصين مؤهلين أو مصادر رسمية.",
    messages: {
      trial: (agentName: string) =>
        `دفع تجربة 1 دولار لـ ${agentName} غير مفعّل بعد. المدفوعات غير متاحة مؤقتاً أثناء إطلاق المنصة.`,
      credits: "المدفوعات غير متاحة مؤقتاً أثناء إطلاق المنصة. ستصبح الأرصدة الموحّدة متاحة قريباً.",
      pro: "اشتراك Pro غير مفعّل بعد. المدفوعات غير متاحة مؤقتاً أثناء إطلاق المنصة.",
    },
    agents: [
      {
        slug: "legal",
        name: "Runexa Legal Agent",
        description: "اكتشف البنود الخطرة قبل توقيع العقود.",
        trialOutcome: "تحليل عقد واحد",
        credits: 12,
        gradient: "from-slate-950 to-blue-700",
      },
      {
        slug: "finance",
        name: "Runexa Finance Coach",
        description:
          "افهم الإنفاق، قلّل الهدر، وحسّن العادات المالية.",
        trialOutcome: "تحليل كشف بنكي واحد",
        credits: 7,
        gradient: "from-emerald-700 to-teal-500",
      },
      {
        slug: "study",
        name: "Runexa Study Agent",
        description: "تعلّم أسرع مع ملخصات الذكاء الاصطناعي وأنظمة المراجعة.",
        trialOutcome: "إنشاء جلسة دراسة ذكية",
        credits: 5,
        gradient: "from-indigo-700 to-violet-500",
      },
      {
        slug: "business",
        name: "Runexa Business Decision Agent",
        description: "حلّل الفرص والمخاطر والقرارات الاستراتيجية.",
        trialOutcome: "إجراء تحليل أعمال واحد",
        credits: 30,
        gradient: "from-amber-700 to-orange-500",
      },
    ] as Agent[],
    creditPacks: [
      {
        name: "Starter",
        credits: 50,
        price: "$9",
        description: "مثالي لاختبار عدة وكلاء من Runexa.",
      },
      {
        name: "Growth",
        credits: 150,
        price: "$24",
        description: "أفضل قيمة للاستخدام المنتظم لعدة وكلاء.",
        highlighted: true,
      },
      {
        name: "Scale",
        credits: 500,
        price: "$89",
        description: "مصمم للمحترفين والمهام المتقدمة.",
      },
    ] as CreditPack[],
  },
};

export default function Pricing() {
  const [language, setLanguage] = useState<Language>("en");
  const [message, setMessage] = useState("");

  const t = labels[language] || labels.en;
  const agents = t.agents as Agent[];
  const creditPacks = t.creditPacks as CreditPack[];

  useEffect(() => {
    const saved = localStorage.getItem("locale") as Language | null;

    if (saved && labels[saved]) {
      setLanguage(saved);
    }

    const handleLocaleChange = () => {
      const updated = localStorage.getItem("locale") as Language | null;

      if (updated && labels[updated]) {
        setLanguage(updated);
      }
    };

    window.addEventListener("locale-change", handleLocaleChange);

    return () => {
      window.removeEventListener("locale-change", handleLocaleChange);
    };
  }, []);

  const requireAuth = () => {
    const token = localStorage.getItem("token");

    if (!token) {
      window.location.href = "/register";
      return false;
    }

    return true;
  };

  const handleStartTrial = (agentName: string) => {
    if (!requireAuth()) return;

    setMessage(t.messages.trial(agentName));
  };

  const handleBuyCredits = () => {
    if (!requireAuth()) return;

    setMessage(t.messages.credits);
  };

  const handleUpgradePro = () => {
    if (!requireAuth()) return;

    setMessage(t.messages.pro);
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
                    onClick={() => handleStartTrial(agent.name)}
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
                  onClick={handleBuyCredits}
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
              Runexa API
            </p>
            <h2 className="mt-2 text-3xl font-bold tracking-tight">
              API Plans for Developers
            </h2>
            <p className="mt-3 max-w-2xl text-slate-600">
              Runexa API is a separate paid product for developers and companies who want
              to integrate AI agents into their own apps, dashboards, and workflows.
            </p>
          </div>

          <div className="mt-8 grid gap-6 lg:grid-cols-3">
            {[
              {
                name: "API Starter",
                price: "$29",
                credits: "100 API credits",
                rate: "10 requests/minute",
                desc: "For developers testing Runexa API integrations.",
                features: [
                  "Legal AI API",
                  "Finance AI API",
                  "Study AI API",
                  "Business AI API",
                  "Async job processing",
                ],
              },
              {
                name: "API Pro",
                price: "$99",
                credits: "500 API credits",
                rate: "60 requests/minute",
                desc: "For production workflows and regular API usage.",
                highlighted: true,
                features: [
                  "Everything in API Starter",
                  "Higher API limits",
                  "Production-ready workflows",
                  "Priority processing",
                  "Usage tracking",
                ],
              },
              {
                name: "Enterprise API",
                price: "Custom",
                credits: "Custom API credits",
                rate: "Custom rate limits",
                desc: "For organizations with private workflows and scale needs.",
                features: [
                  "Custom AI workflows",
                  "Team API access",
                  "Private infrastructure options",
                  "Priority support",
                  "Enterprise onboarding",
                ],
              },
            ].map((plan) => (
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
                    Contact Sales
                  </a>
                ) : (
                  <button
                    onClick={handleBuyCredits}
                    className={`mt-8 w-full rounded-xl px-5 py-3 text-sm font-bold transition ${
                      plan.highlighted
                        ? "bg-blue-600 text-white hover:bg-blue-700"
                        : "bg-slate-950 text-white hover:bg-slate-800"
                    }`}
                  >
                    Start API Plan
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
