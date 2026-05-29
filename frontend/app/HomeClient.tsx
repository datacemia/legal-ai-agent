"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import {
  Sparkles,
  ShieldCheck,
  Scale,
  GraduationCap,
  BarChart3,
  BriefcaseBusiness,
  Users,
  Lock,
  Zap,
  Globe,
} from "lucide-react";

const labels: any = {
  en: {
    platform: "Runexa AI Platform",
    title:
      "Specialized AI agents for legal, finance, learning, and business decision-making.",
    desc:
      "Runexa helps individuals and professionals analyze documents, understand financial data, learn more effectively, and make better decisions.",
    explore: "Explore AI Agents",
    pricing: "Plans & Pricing",
    blog: "Insights",
    trustLine:
      "$1 trial per agent · Unified credits · Secure AI platform",
    choose: "Choose Your AI Agent",
    chooseDesc:
      "One Runexa account gives you access to specialized AI agents. Analyze legal documents, optimize your finances, learn more effectively, and make smarter business decisions.",
    available: "Available",
    open: "Open Agent",
    howTitle: "How Runexa Works",
    howSteps: [
      "Upload your documents or data",
      "Runexa AI automatically analyzes the content",
      "Receive actionable insights, recommendations, and reports",
    ],
    trustCards: [
    ["Secure & Reliable", "Your data stays protected"],
    ["Unified Credits", "Use them across all agents"],
    ["Instant Access", "Get started in minutes"],
    ["Built for Real Work", "For individuals and professionals"],
  ],
    enterpriseBadge: "Custom AI Solutions",
    enterpriseTitle: "Runexa for Enterprises",
    enterpriseSubtitle:
      "Custom AI systems for teams, companies, and organizations.",
    enterpriseDesc:
      "Runexa helps organizations automate document analysis, unlock insights from financial data, optimize learning workflows, and support strategic decision-making.",
    enterprisePrimary: "Request a Demo",
    enterpriseSecondary: "Explore Enterprise Solutions",
    enterpriseCards: [
      "Team Workspaces",
      "Enterprise Dashboard",
      "Multi-User Access",
      "Custom Credits & Plans",
      "Priority Support",
    ],
    enterpriseSystem: "Custom AI Solutions",
    enterpriseWorkflow: "Intelligent Workflows",
    enterpriseFooter:
      "Connected processes • Unified insights • Faster decisions",
    enterpriseTag: "Enterprise Solutions",
    enterpriseHeader: "Runexa Business AI",
    ctaTitle:
      "One Platform. Multiple AI Agents. Real Results.",
    ctaDesc:
      "Runexa is a unified AI platform for document analysis, financial intelligence, learning, and business decision support.",
    ctaButton:
      "Create Account",
    disclaimer:
      "AI-generated insights may contain errors. Always verify information before making important decisions.",
    seoTitle:
      "AI Platform for Individuals and Enterprises",
    seoHeading:
      "Specialized AI Agents for Document Analysis, Finance, Learning, and Business Intelligence",
    seoDesc:
      "Runexa provides specialized AI agents for document analysis, contract review, financial analysis, learning assistance, business intelligence, and enterprise workflow optimization.",
    seoItems: [
      "AI Document Analysis",
      "Contract Review & Risk Detection",
      "Financial Analysis & Insights",
      "AI Learning Assistant",
      "Business Intelligence & Decision Support",
      "Enterprise Workflow Optimization",
    ],
    faqTitle: "FAQ",
    faqHeading: "Frequently Asked Questions",
    faqItems: [
      [
        "What is an AI agent?",
        "An AI agent is a specialized AI system designed to help you complete specific tasks, such as contract review, financial analysis, learning support, or business decision-making.",
      ],
      [
        "How does Runexa work?",
        "Upload a document or dataset, choose the AI agent that matches your needs, and receive structured analyses, summaries, insights, recommendations, and reports.",
      ],
      [
        "Is Runexa secure?",
        "Yes. Runexa is designed as a secure AI platform for document analysis, data processing, and professional workflows, with a strong focus on privacy and security.",
      ],
      [
        "Can businesses use Runexa?",
        "Yes. Runexa supports enterprises with team workspaces, enterprise dashboards, multi-user access, custom plans, and business intelligence solutions.",
      ],
      [
        "What can Runexa analyze?",
        "Runexa can analyze legal documents, bank statements, learning materials, and business data, depending on the AI agent you choose.",
      ],
      [
        "Does Runexa replace professionals?",
        "No. Runexa provides insights and decision-support tools, but important decisions should always be reviewed and validated by qualified professionals.",
      ],
    ],
    agents: [
    [
      "Runexa Legal Agent",
      "Identify risky clauses and understand legal risks before signing contracts.",
      "/legal-ai",
      "legal",
    ],
    [
      "Runexa Finance Coach",
      "Analyze spending, uncover savings opportunities, and improve financial decisions.",
      "/finance-ai",
      "finance",
    ],
    [
      "Runexa Study Agent",
      "Learn more effectively with AI-generated summaries, quizzes, and study plans.",
      "/study-ai",
      "study",
    ],
    [
      "Runexa Business Decision Agent",
      "Gain actionable insights to make faster and better-informed business decisions.",
      "/business-ai",
      "business",
    ],
  ],
  },

  fr: {
    platform: "Plateforme IA Runexa",
    title:
      "Des agents IA spécialisés pour le juridique, la finance, l’apprentissage et les décisions business.",
    desc:
      "Runexa aide les particuliers et les professionnels à analyser des documents, comprendre leurs données financières, apprendre plus efficacement et prendre de meilleures décisions.",
    explore: "Découvrir les agents IA",
    pricing: "Plans et tarifs",
    blog: "Ressources & Insights",
    trustLine:
      "Essai à 1 $ par agent · Crédits unifiés · Plateforme IA sécurisée",
    tryLegal: "Runexa Legal Agent",
    tryFinance: "Runexa Finance Coach",
    tryStudy: "Runexa Study Agent",
    tryBusiness: "Runexa Business Decision Agent",
    choose: "Choisissez votre agent IA",
    chooseDesc:
      "Un seul compte Runexa pour accéder à des agents IA spécialisés. Analysez vos documents juridiques, optimisez vos finances, apprenez plus efficacement et prenez de meilleures décisions.",
    available: "Disponible",
    open: "Ouvrir l’agent",
    howTitle: "Comment fonctionne Runexa",
    howSteps: [
      "Importez vos documents ou vos données",
      "L’IA Runexa analyse automatiquement le contenu",
      "Recevez des recommandations et des insights exploitables",
    ],
    trustCards: [
      ["Sécurisé et fiable", "Vos données sont protégées"],
      ["Crédits unifiés", "Valables sur tous les agents"],
      ["Accès immédiat", "Commencez instantanément"],
      ["Conçu pour un usage réel", "Particuliers et professionnels"],
    ],
    enterpriseBadge: "Solutions IA personnalisées",
    enterpriseTitle: "Runexa pour les entreprises",
    enterpriseSubtitle:
      "Des systèmes d’IA personnalisés pour les équipes, les entreprises et les organisations.",
    enterpriseDesc:
      "Runexa aide les organisations à automatiser l’analyse documentaire, exploiter les données financières, optimiser les workflows d’apprentissage et soutenir la prise de décision stratégique.",
    enterprisePrimary: "Demander une démonstration",
    enterpriseSecondary: "Découvrir les solutions entreprises",
    enterpriseCards: [
      "Espaces de travail collaboratifs",
      "Tableau de bord entreprise",
      "Accès multi-utilisateurs",
      "Crédits et plans personnalisés",
      "Support prioritaire",
    ],
    enterpriseSystem: "Solutions IA personnalisées",
    enterpriseWorkflow: "Workflows intelligents",
    enterpriseFooter:
      "Processus connectés • Vision unifiée • Décisions plus rapides",
    enterpriseTag: "Solutions entreprises",
    enterpriseHeader: "Runexa Business AI",
    ctaTitle:
      "Une plateforme. Plusieurs agents IA. Des résultats concrets.",
    ctaDesc:
      "Runexa est une plateforme IA unifiée pour l’analyse documentaire, la finance, l’apprentissage et les décisions business.",
    ctaButton:
      "Créer un compte",
    disclaimer:
      "Les analyses générées par l’IA peuvent contenir des erreurs. Vérifiez toujours les informations avant de prendre une décision.",
    seoTitle:
      "Plateforme IA pour les particuliers et les entreprises",
    seoHeading:
      "Agents IA spécialisés pour l’analyse documentaire, la finance, l’apprentissage et la business intelligence",
    seoDesc:
      "Runexa propose des agents IA spécialisés pour l’analyse documentaire, la revue de contrats, l’analyse financière, l’assistance à l’apprentissage, la business intelligence et l’optimisation des workflows en entreprise.",
    seoItems: [
      "Analyse documentaire par IA",
      "Revue de contrats et détection des risques",
      "Analyse financière et insights",
      "Assistant intelligent pour l’apprentissage",
      "Business intelligence et aide à la décision",
      "Optimisation des workflows en entreprise",
    ],
    faqTitle: "FAQ",
    faqHeading: "Questions fréquentes sur Runexa",
    faqItems: [
      [
        "Qu’est-ce qu’un agent IA ?",
        "Un agent IA est un système spécialisé conçu pour vous aider à accomplir des tâches précises, comme la revue de contrats, l’analyse financière, l’apprentissage ou l’aide à la décision.",
      ],
      [
        "Comment fonctionne Runexa ?",
        "Importez un document ou un jeu de données, choisissez l’agent adapté à votre besoin, puis recevez des analyses structurées, des résumés, des insights, des recommandations et des rapports.",
      ],
      [
        "Runexa est-il sécurisé ?",
        "Oui. Runexa est conçu comme une plateforme IA sécurisée pour l’analyse de documents, de données et de workflows professionnels, avec un fort accent sur la confidentialité.",
      ],
      [
        "Les entreprises peuvent-elles utiliser Runexa ?",
        "Oui. Runexa propose des espaces de travail collaboratifs, des tableaux de bord entreprise, un accès multi-utilisateurs, des crédits personnalisés et des solutions de business intelligence.",
      ],
      [
        "Que peut analyser Runexa ?",
        "Runexa peut analyser des documents juridiques, des relevés bancaires, des supports d’apprentissage et des données métier, selon l’agent IA sélectionné.",
      ],
      [
        "Runexa remplace-t-il les professionnels ?",
        "Non. Runexa fournit des analyses et des informations destinées à faciliter la prise de décision. Les décisions importantes doivent toujours être validées par des professionnels qualifiés.",
      ],
    ],
    agents: [
    [
      "Runexa Legal Agent",
      "Identifiez les clauses à risque et comprenez les implications juridiques avant de signer un contrat.",
      "/legal-ai",
      "legal",
    ],
    [
      "Runexa Finance Coach",
      "Analysez vos dépenses, repérez les opportunités d’économies et améliorez vos décisions financières.",
      "/finance-ai",
      "finance",
    ],
    [
      "Runexa Study Agent",
      "Apprenez plus efficacement grâce aux résumés, quiz et plans d’étude générés par l’IA.",
      "/study-ai",
      "study",
    ],
    [
      "Runexa Business Decision Agent",
      "Obtenez des analyses et des insights pour prendre des décisions plus rapides et mieux informées.",
      "/business-ai",
      "business",
    ],
  ],
  },

  ar: {
    platform: "مساحة Runexa للذكاء الاصطناعي",
    title: "وكلاء ذكاء اصطناعي متخصصون للأعمال القانونية والمالية والتعليمية والتجارية.",
    desc: "تساعد Runexa الأفراد والمحترفين على تحليل المستندات واستخلاص الرؤى من البيانات المالية وتسريع التعلّم واتخاذ قرارات أكثر ذكاءً وفعالية.",
    explore: "استكشف حلول الذكاء الاصطناعي",
    pricing: "الخطط والأسعار",
    blog: "المدونة",
    trustLine: "تجربة مقابل دولار واحد لكل وكيل · أرصدة موحدة · منصة ذكاء اصطناعي آمنة",
    tryLegal: "Runexa Legal Agent",
    tryFinance: "Runexa Finance Coach",
    tryStudy: "Runexa Study Agent",
    tryBusiness: "Runexa Business Decision Agent",
    choose: "اختر وكيلك الذكي",
    chooseDesc:
       "حساب Runexa واحد للوصول إلى وكلاء ذكاء اصطناعي متخصصين. حلّل المستندات القانونية، وافهم بياناتك المالية، وسرّع تعلّمك، واتخذ قرارات أعمال أكثر ذكاءً.",
    available: "متاح",
    open: "فتح الوكيل",
    howTitle: "كيف تعمل Runexa",
    howSteps: [
      "ارفع مستنداتك أو بياناتك",
      "يقوم ذكاء Runexa بتحليل المحتوى تلقائيًا",
      "احصل على رؤى وتوصيات قابلة للتنفيذ",
    ],
    trustCards: [
      ["آمن وموثوق", "بياناتك محمية"],
      ["أرصدة موحدة", "لجميع الوكلاء"],
      ["وصول فوري", "ابدأ فورًا"],
      ["مصمم للعمل الحقيقي", "للأفراد والمحترفين"],
    ],
    enterpriseBadge: "حلول ذكاء اصطناعي للمؤسسات",

    enterpriseTitle: "Runexa للمؤسسات",

    enterpriseSubtitle:
      "أنظمة ذكاء اصطناعي مخصصة للفرق والشركات والمؤسسات.",
    enterpriseDesc:
      "تساعد Runexa المؤسسات على أتمتة تحليل المستندات واستخلاص الرؤى من البيانات المالية وتحسين عمليات التعلّم ودعم اتخاذ القرارات الاستراتيجية.",

    enterprisePrimary: "طلب عرض توضيحي",

    enterpriseSecondary: "استكشف حلول المؤسسات",

    enterpriseCards: [
      "مساحات عمل للفرق",
      "لوحة تحكم للمؤسسات",
      "وصول متعدد المستخدمين",
      "أرصدة وخطط مخصصة",
      "دعم أولوية",
    ],
    enterpriseSystem: "حلول ذكاء اصطناعي مخصصة",
    enterpriseWorkflow: "تدفقات عمل ذكية",
    enterpriseFooter:
      "عمليات مترابطة • رؤية موحدة • قرارات أسرع",
    enterpriseTag: "حلول المؤسسات",
    ctaTitle:
      "منصة واحدة. وكلاء ذكاء اصطناعي متخصصة. نتائج ملموسة.",
    ctaDesc:
      "Runexa هي منصة ذكاء اصطناعي موحدة لتحليل المستندات وفهم البيانات المالية وتسريع التعلّم ودعم قرارات الأعمال.",

    ctaButton: "إنشاء حساب مجاني",

    disclaimer:
      "التحليلات مدعومة بالذكاء الاصطناعي وقد تحتوي على أخطاء. يُرجى التحقق من النتائج قبل اتخاذ أي قرار.",

    seoTitle:
      "منصة ذكاء اصطناعي موحدة للأفراد والمؤسسات",

    seoHeading:
      "وكلاء ذكاء اصطناعي متخصصة لتحليل المستندات والبيانات المالية والتعلّم وذكاء الأعمال",
    seoDesc:
      "توفّر Runexa منصة موحدة تضم وكلاء ذكاء اصطناعي متخصصين لتحليل المستندات ومراجعة العقود والتحليل المالي ودعم التعلّم وذكاء الأعمال وتحسين سير العمل للمؤسسات والفرق المهنية.",

    seoItems: [
      "تحليل المستندات واستخراج المعلومات",
      "مراجعة العقود واكتشاف المخاطر",
      "التحليل المالي واستخلاص الرؤى",
      "مساعد ذكي للتعلّم والدراسة",
      "ذكاء الأعمال ودعم اتخاذ القرار",
      "تحسين سير العمل والإنتاجية",
    ],
    faqTitle: "الأسئلة الشائعة",
    faqHeading: "إجابات عن أكثر الأسئلة شيوعًا حول Runexa",
    faqItems: [
      [
        "ما هو وكيل الذكاء الاصطناعي؟",
        "وكيل الذكاء الاصطناعي هو نظام متخصص مصمم لمساعدتك في تنفيذ مهام محددة، مثل مراجعة العقود وتحليل البيانات المالية وتنظيم الدراسة ودعم قرارات الأعمال.",
      ],
      [
        "كيف تعمل Runexa؟",
        "ارفع مستندًا أو ملف بيانات، واختر الوكيل المناسب، ثم احصل على تحليلات منظمة وملخصات ورؤى وتوصيات وتقارير قابلة للتنفيذ.",
      ],
      [
        "هل Runexa آمنة؟",
        "نعم. تم تصميم Runexa كمنصة ذكاء اصطناعي آمنة تساعد على تحليل المستندات والبيانات وسير العمل المهني مع التركيز على الخصوصية والأمان.",
      ],
      [
        "هل يمكن للشركات استخدام Runexa؟",
        "نعم. تدعم Runexa المؤسسات من خلال مساحات عمل للفرق ولوحات تحكم إدارية ووصول متعدد المستخدمين وأرصدة مخصصة وحلول لذكاء الأعمال.",
      ],
      [
        "ما الذي يمكن لـ Runexa تحليله؟",
        "يمكن لـ Runexa تحليل المستندات القانونية وكشوفات الحساب البنكية والمواد التعليمية وبيانات الأعمال، وفقًا للوكيل الذكي الذي تختاره.",
      ],
      [
        "هل تحل Runexa محل الخبراء؟",
        "لا. توفّر Runexa تحليلات ومعلومات تساعد على اتخاذ القرار، لكنها لا تُغني عن استشارة المختصين المؤهلين عند اتخاذ القرارات المهمة.",
      ],
    ],
    agents: [
        [
          "Runexa Legal Agent",
          "اكتشف البنود الخطرة وافهم المخاطر القانونية قبل توقيع العقود.",
          "/legal-ai",
          "legal",
        ],

        [
          "Runexa Finance Coach",
          "افهم نفقاتك وحدد فرص التوفير وحسّن قراراتك المالية.",
          "/finance-ai",
          "finance",
        ],

        [
          "Runexa Study Agent",
          "تعلّم بفعالية أكبر من خلال الملخصات والاختبارات وخطط الدراسة المدعومة بالذكاء الاصطناعي.",
          "/study-ai",
          "study",
        ],

        [
          "Runexa Business Decision Agent",
          "احصل على رؤى ذكية وتحليلات تدعم اتخاذ قرارات أعمال أكثر ثقة وفعالية.",
          "/business-ai",
          "business",
        ],
      ],
  },
};

const agentStyles: any = {
  legal: {
    icon: Scale,
    card: "border-slate-200 bg-white hover:shadow-blue-100",
    iconBox: "bg-blue-50",
    iconColor: "text-blue-700",
    arrow: "text-blue-600",
    badge: "bg-blue-50 text-blue-700",
  },
  finance: {
    icon: BarChart3,
    card: "bg-gradient-to-br from-emerald-500 to-green-600 text-white hover:shadow-emerald-200",
    iconBox: "bg-white/15 backdrop-blur",
    iconColor: "text-white",
    arrow: "text-white",
    badge: "bg-white/10 text-emerald-50",
  },
  study: {
    icon: GraduationCap,
    card: "border-slate-200 bg-white hover:shadow-violet-100",
    iconBox: "bg-violet-50",
    iconColor: "text-violet-700",
    arrow: "text-violet-600",
    badge: "bg-violet-50 text-violet-700",
  },
  business: {
    icon: BriefcaseBusiness,
    card: "border-slate-200 bg-white hover:shadow-orange-100",
    iconBox: "bg-orange-50",
    iconColor: "text-orange-700",
    arrow: "text-orange-600",
    badge: "bg-orange-50 text-orange-700",
  },
};

export default function HomeClient() {
  const [language, setLanguage] = useState("en");
  const t = labels[language] || labels.en;

  useEffect(() => {
    const saved = localStorage.getItem("locale");

    if (saved && labels[saved]) {
      setLanguage(saved);
    }
  }, []);

  const handleLanguageChange = (lang: string) => {
    setLanguage(lang);
    localStorage.setItem("locale", lang);
    window.dispatchEvent(new Event("locale-change"));
  };

  return (
    <main
      dir={language === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 text-slate-900"
    >
      <section className="px-6 py-20">
        <div className="max-w-6xl mx-auto text-center space-y-8">
          <div className="flex justify-center">
            <select
              value={language}
              onChange={(e) => handleLanguageChange(e.target.value)}
              className="border rounded-lg px-3 py-2 bg-white"
            >
              <option value="en">English</option>
              <option value="fr">Français</option>
              <option value="ar">العربية</option>
            </select>
          </div>

          <p className="text-blue-600 font-semibold">{t.platform}</p>
          <h1 className="text-5xl font-bold leading-tight">{t.title}</h1>
          <p className="text-lg text-slate-600 max-w-3xl mx-auto">
            {t.desc}
          </p>

          <div className="flex flex-col sm:flex-row justify-center gap-3">
            <a
              href="#agents"
              className="inline-flex items-center justify-center rounded-xl bg-blue-600 px-6 py-3 text-sm font-semibold text-white hover:bg-blue-700 transition"
            >
              {t.explore}
            </a>

            <Link
              href="/pricing"
              className="inline-flex items-center justify-center rounded-xl border border-slate-200 bg-white px-6 py-3 text-sm font-semibold text-slate-900 hover:bg-slate-50 transition"
            >
              {t.pricing}
            </Link>

            <Link
              href="/blog"
              className="inline-flex items-center justify-center rounded-xl border border-slate-200 bg-white px-6 py-3 text-sm font-semibold text-slate-900 hover:bg-slate-50 transition"
            >
              {t.blog}
            </Link>
          </div>

          <p className="text-sm text-slate-500">{t.trustLine}</p>

          <div className="relative mt-10">
            <div className="absolute inset-0 bg-gradient-to-r from-blue-100/40 via-transparent to-emerald-100/30 blur-3xl" />

            <div className="relative rounded-[32px] border border-slate-200/80 bg-white/80 p-6 shadow-[0_20px_80px_rgba(15,23,42,0.08)] backdrop-blur-xl md:p-10">
              <div className="mb-8 flex justify-center">
                <div className="inline-flex items-center gap-2 rounded-full border border-blue-200 bg-blue-50 px-5 py-2 text-sm font-semibold text-blue-700">
                  <span><Users className="h-4 w-4" /></span>
                  <span>
                    {language === "fr"
                      ? "Pour les particuliers, les professionnels et les entreprises"
                      : language === "ar"
                      ? "للأفراد والمهنيين والمؤسسات"
                      : "For Individuals, Professionals, and Enterprises"}
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-5">
                <a
                  href="#agents"
                  className="group relative overflow-hidden rounded-3xl bg-gradient-to-br from-blue-600 to-blue-700 p-4 xl:p-5 text-white shadow-xl transition duration-300 hover:-translate-y-1 hover:shadow-blue-200"
                >
                  <div className="absolute inset-0 bg-white/5 opacity-0 transition group-hover:opacity-100" />

                  <div className="relative flex items-start justify-between">
                    <div className="space-y-2 text-left">
                      <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-white/15 text-2xl backdrop-blur">
                        <Sparkles className="h-6 w-6" />
                      </div>

                      <div>
                        <h3 className="text-base font-bold">{t.explore}</h3>

                        <p className="mt-1 text-sm text-blue-100">
                          {language === "fr"
                            ? "Agents IA spécialisés"
                            : language === "ar"
                            ? "وكلاء ذكاء اصطناعي متخصصون"
                            : "Specialized AI Agents"}
                        </p>
                      </div>
                    </div>

                    <span className="text-2xl transition group-hover:translate-x-1">
                      →
                    </span>
                  </div>

                  <div className="mt-5 inline-flex rounded-full bg-white/10 px-3 py-1 text-xs font-medium text-blue-100">
                    {language === "fr"
                      ? "Plateforme IA"
                      : language === "ar"
                      ? "منصة ذكاء اصطناعي"
                      : "AI Platform"}
                  </div>
                </a>

                {t.agents.map((agent: string[]) => {
                  const style = agentStyles[agent[3]];
                  const Icon = style.icon;
                  const isDark = agent[3] === "finance";

                  return (
                    <Link
                      key={agent[0]}
                      href={agent[2]}
                      className={`group relative overflow-hidden rounded-3xl p-4 shadow-lg transition duration-300 hover:-translate-y-1 ${style.card}`}
                    >
                      {isDark && (
                        <div className="absolute inset-0 bg-white/5 opacity-0 transition group-hover:opacity-100" />
                      )}

                      <div className="relative flex items-start justify-between">
                        <div className="space-y-2 text-left">
                          <div className={`flex h-12 w-12 items-center justify-center rounded-2xl text-2xl ${style.iconBox}`}>
                            <Icon className={`h-6 w-6 ${style.iconColor}`} />
                          </div>

                          <div>
                            <h3 className={`text-base font-bold ${isDark ? "text-white" : "text-slate-900"}`}>
                              {agent[0]}
                            </h3>

                            <p className={`mt-1 text-sm ${isDark ? "text-emerald-100" : "text-slate-500"}`}>
                              {agent[1]}
                            </p>
                          </div>
                        </div>

                        <span className={`text-2xl transition group-hover:translate-x-1 ${style.arrow}`}>
                          →
                        </span>
                      </div>

                      <div className={`mt-5 inline-flex rounded-full px-3 py-1 text-xs font-medium ${style.badge}`}>
                        {t.available}
                      </div>
                    </Link>
                  );
                })}
              </div>

              <div className="mt-8 grid grid-cols-1 gap-4 border-t border-slate-200 pt-6 md:grid-cols-2 lg:grid-cols-4">
                {t.trustCards.map((card: string[], index: number) => {
                  const icons = [Lock, Globe, Zap, ShieldCheck];
                  const colors = [
                    "bg-violet-50 text-violet-700",
                    "bg-blue-50 text-blue-700",
                    "bg-emerald-50 text-emerald-700",
                    "bg-blue-50 text-blue-700",
                  ];
                  const Icon = icons[index];

                  return (
                    <div key={card[0]} className="flex items-center gap-3 text-left">
                      <div className={`flex h-12 w-12 items-center justify-center rounded-2xl text-xl ${colors[index]}`}>
                        <Icon className="h-6 w-6" />
                      </div>

                      <div>
                        <p className="font-semibold text-slate-900">
                          {card[0]}
                        </p>

                        <p className="text-sm text-slate-500">
                          {card[1]}
                        </p>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>

      </section>

      <section className="px-6 pb-8">
        <div className="max-w-6xl mx-auto">
          <div className="relative overflow-hidden rounded-[32px] border border-slate-200 bg-white shadow-[0_20px_80px_rgba(15,23,42,0.08)]">
            <div className="absolute inset-0 bg-gradient-to-br from-blue-50 via-white to-emerald-50" />

            <div className="relative grid gap-8 p-6 md:grid-cols-2 md:p-10">
              <div className="space-y-5">
                <div>
                  <p className="text-sm font-semibold text-blue-600">
                    {language === "fr"
                      ? "Aperçu de la plateforme IA"
                      : language === "ar"
                      ? "معاينة منصة الذكاء الاصطناعي"
                      : "AI Platform Preview"}
                  </p>

                 <h2 className="mt-3 text-3xl font-bold text-slate-900">
                    {language === "fr"
                      ? "Des analyses intelligentes pour les documents, la finance, l’apprentissage et les décisions business"
                      : language === "ar"
                      ? "تحليلات ذكية للمستندات والمالية والتعلّم وقرارات الأعمال"
                      : "Intelligent insights for documents, finance, learning, and business decisions"}
                  </h2>

                  <p className="mt-4 text-slate-600 leading-7">
                    {language === "fr"
                      ? "Runexa réunit des agents IA spécialisés dans une plateforme unique conçue pour l’analyse, l’apprentissage et la prise de décision."
                      : language === "ar"
                      ? "تجمع Runexa وكلاء ذكاء اصطناعي متخصصين ضمن منصة واحدة مصممة للتحليل والتعلّم ودعم اتخاذ القرار."
                      : "Runexa brings together specialized AI agents in a single platform built for analysis, learning, and decision-making."}
                  </p>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-5">
                    <p className="text-sm text-slate-500">
                      {language === "fr"
                        ? "Niveau de risque"
                        : language === "ar"
                        ? "مستوى المخاطر"
                        : "Risk Level"}
                    </p>
                    <p className="mt-2 text-3xl font-bold text-blue-600">
                      82/100
                    </p>

                    <p className="mt-2 text-sm text-slate-500">
                      {language === "fr"
                        ? "Agent Juridique IA"
                        : language === "ar"
                        ? "وكيل قانوني بالذكاء الاصطناعي"
                        : "Legal AI Agent"}
                    </p>
                  </div>

                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-5">
                    <p className="text-sm text-slate-500">
                      {language === "fr"
                        ? "Santé financière"
                        : language === "ar"
                        ? "الصحة المالية"
                        : "Financial Health"}
                    </p>

                    <p className="mt-2 text-3xl font-bold text-emerald-600">
                      74%
                    </p>

                    <p className="mt-2 text-sm text-slate-500">
                      {language === "fr"
                        ? "Agent Finance IA"
                        : language === "ar"
                        ? "وكيل التمويل بالذكاء الاصطناعي"
                        : "Finance AI Agent"}
                    </p>
                  </div>

                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-5">
                    <p className="text-sm text-slate-500">
                      {language === "fr"
                        ? "Progression d’apprentissage"
                        : language === "ar"
                        ? "تقدّم التعلّم"
                        : "Learning Progress"}
                    </p>

                    <p className="mt-2 text-3xl font-bold text-violet-600">
                      91%
                    </p>

                    <p className="mt-2 text-sm text-slate-500">
                      Runexa Study Agent
                    </p>
                  </div>

                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-5">
                    <p className="text-sm text-slate-500">
                      {language === "fr"
                        ? "Insights business"
                        : language === "ar"
                        ? "رؤى الأعمال"
                        : "Business Insights"}
                    </p>

                    <p className="mt-2 text-3xl font-bold text-orange-600">
                      12
                    </p>

                    <p className="mt-2 text-sm text-slate-500">
                      Runexa Business Decision Agent
                    </p>
                  </div>
                </div>
              </div>

              <div className="rounded-3xl bg-slate-950 p-6 text-white shadow-2xl">
                <div className="flex items-center justify-between border-b border-white/10 pb-4">
                  <div>
                    <p className="text-sm text-slate-400">
                      Runexa AI Workspace
                    </p>

                    <p className="text-lg font-semibold">
                      {language === "fr" ? "Recommandations IA" : language === "ar" ? "توصيات الذكاء الاصطناعي" : "AI Recommendations"}
                    </p>
                  </div>

                  <span className="rounded-full bg-green-500/10 px-3 py-1 text-xs font-medium text-green-300">
                    Live
                  </span>
                </div>

                <div className="mt-6 space-y-4">
                  {[
                    language === "fr"
                      ? "Examiner les clauses à risque du contrat fournisseur"
                      : language === "ar"
                      ? "مراجعة البنود عالية المخاطر في عقد المورد"
                      : "Review high-risk clauses in vendor contract",

                    language === "fr"
                      ? "Identifier des opportunités de réduction des dépenses récurrentes"
                      : language === "ar"
                      ? "تحديد فرص خفض النفقات المتكررة"
                      : "Identify opportunities to reduce recurring expenses",

                    language === "fr"
                      ? "Améliorer la progression d’apprentissage cette semaine"
                      : language === "ar"
                      ? "تحسين التقدم في التعلّم هذا الأسبوع"
                      : "Improve learning progress this week",

                    language === "fr"
                      ? "Surveiller les risques opérationnels et les indicateurs clés"
                      : language === "ar"
                      ? "مراقبة المخاطر التشغيلية والمؤشرات الرئيسية"
                      : "Monitor operational risks and key business metrics",
                  ].map((item) => (
                    <div
                      key={item}
                      className="flex items-start gap-3 rounded-2xl border border-white/10 bg-white/5 p-4"
                    >
                      <div className="mt-1 h-2 w-2 rounded-full bg-blue-400" />

                      <p className="text-sm text-slate-200">
                        {item}
                      </p>
                    </div>
                  ))}
                </div>

                <div className="mt-6 rounded-2xl border border-blue-400/20 bg-blue-500/10 p-4 text-sm text-blue-100">
                  {language === "fr"
                    ? "Données connectées → insights unifiés → décisions plus rapides"
                    : language === "ar"
                    ? "بيانات مترابطة → رؤى موحدة → قرارات أسرع"
                    : "Connected data → unified insights → faster decisions"}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="agents" className="px-6 py-12">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-10">
            <h2 className="text-3xl font-bold">{t.choose}</h2>
            <p className="mt-3 text-slate-600 max-w-3xl mx-auto">
              {t.chooseDesc}
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {t.agents.map((agent: string[]) => {
              const style = agentStyles[agent[3]];
              const Icon = style.icon;

              return (
                <div
                  key={agent[0]}
                  className="bg-white p-6 rounded-2xl border shadow-sm flex flex-col justify-between"
                >
                  <div>
                    <div className="flex items-center justify-between gap-3">
                      <div className={`flex h-11 w-11 items-center justify-center rounded-2xl ${style.iconBox}`}>
                        <Icon className={`h-6 w-6 ${style.iconColor}`} />
                      </div>

                      <span className="text-xs bg-slate-100 text-slate-600 px-3 py-1 rounded-full">
                        {t.available}
                      </span>
                    </div>

                    <h3 className="mt-4 text-xl font-bold">
                      {agent[0]}
                    </h3>

                    <p className="mt-4 text-slate-600">{agent[1]}</p>
                  </div>

                  <Link
                    href={agent[2]}
                    className="inline-block mt-6 text-center px-4 py-2 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition"
                  >
                    {t.open}
                  </Link>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      <section className="px-6 py-12">
        <div className="max-w-6xl mx-auto">
          <div className="relative overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">
            <div className="absolute inset-0 bg-gradient-to-br from-blue-50 via-white to-slate-50" />

            <div className="relative p-8 md:p-12">
              <div className="text-center mb-10">
                <h2 className="text-3xl font-bold text-slate-900">
                  {t.howTitle}
                </h2>
              </div>

              <div className="grid gap-4 md:grid-cols-3">
                {t.howSteps.map((step: string, index: number) => (
                  <div
                    key={step}
                    className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"
                  >
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-600 text-sm font-bold text-white">
                      {index + 1}
                    </div>

                    <p className="mt-4 font-semibold text-slate-900">
                      {step}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>


      <section className="px-6 py-12">
        <div className="max-w-6xl mx-auto">
          <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm md:p-12">
            <p className="text-sm font-semibold text-blue-600">
              {t.seoTitle}
            </p>

            <h2 className="mt-3 text-3xl font-bold text-slate-900">
              {t.seoHeading}
            </h2>

            <p className="mt-4 max-w-4xl text-slate-600 leading-7">
              {t.seoDesc}
            </p>

            <div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {t.seoItems.map((item: string) => (
                <div
                  key={item}
                  className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm font-semibold text-slate-700"
                >
                  {item}
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="px-6 py-12">
        <div className="max-w-6xl mx-auto">
          <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm md:p-12">
            <p className="text-sm font-semibold text-blue-600">
              {t.faqTitle}
            </p>

            <h2 className="mt-3 text-3xl font-bold text-slate-900">
              {t.faqHeading}
            </h2>

            <div className="mt-8 grid gap-4 md:grid-cols-2">
              {t.faqItems.map((item: string[]) => (
                <div
                  key={item[0]}
                  className="rounded-2xl border border-slate-200 bg-slate-50 p-5"
                >
                  <h3 className="font-bold text-slate-900">
                    {item[0]}
                  </h3>

                  <p className="mt-2 text-sm leading-6 text-slate-600">
                    {item[1]}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="px-6 py-16">
        <div className="max-w-6xl mx-auto">
          <div className="relative overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">
            <div className="absolute inset-0 bg-gradient-to-br from-blue-50 via-white to-slate-50" />

            <div className="relative grid gap-10 p-8 md:p-12 lg:grid-cols-2 lg:items-center">
              <div>
                <span className="inline-flex rounded-full border border-blue-100 bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-700">
                  {t.enterpriseBadge}
                </span>

                <h2 className="mt-5 text-3xl font-bold tracking-tight text-slate-900">
                  {t.enterpriseTitle}
                </h2>

                <p className="mt-3 text-lg font-medium text-slate-700">
                  {t.enterpriseSubtitle}
                </p>

                <p className="mt-4 text-slate-600 leading-7">
                  {t.enterpriseDesc}
                </p>

                <div className="mt-6 flex flex-wrap gap-3">
                  <Link
                    href="/contact-entreprise/contact"
                    className="rounded-xl bg-blue-600 px-5 py-3 text-sm font-semibold text-white hover:bg-blue-700 transition"
                  >
                    {t.enterprisePrimary}
                  </Link>

                  <Link
                    href="/enterprise"
                    className="rounded-xl border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-slate-900 hover:bg-slate-50 transition"
                  >
                    {t.enterpriseSecondary}
                  </Link>
                </div>
              </div>

              <div className="rounded-3xl border border-slate-200 bg-slate-950 p-6 text-white shadow-xl">
                <div className="flex items-center justify-between border-b border-white/10 pb-4">
                  <div>
                    <p className="text-sm text-slate-400">{t.enterpriseHeader}</p>
                    <p className="text-lg font-semibold">{t.enterpriseSystem}</p>
                  </div>

                  <span className="rounded-full bg-green-500/10 px-3 py-1 text-xs font-medium text-green-300">
                    {t.enterpriseTag}
                  </span>
                </div>

                <div className="mt-6 grid grid-cols-2 gap-3">
                  {t.enterpriseCards.map((item: string, index: number) => (
                    <div
                      key={index}
                      className="rounded-2xl border border-white/10 bg-white/5 p-4"
                    >
                      <div className="h-2 w-2 rounded-full bg-blue-400" />
                      <p className="mt-3 text-sm font-medium">{item}</p>
                      <p className="mt-2 text-xs text-slate-400">
                        {t.enterpriseWorkflow}
                      </p>
                    </div>
                  ))}
                </div>

                <div className="mt-6 rounded-2xl border border-blue-400/20 bg-blue-500/10 p-4 text-sm text-blue-100">
                  {t.enterpriseFooter}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="px-6 py-16">
        <div className="max-w-5xl mx-auto bg-blue-600 text-white rounded-3xl p-10 text-center">
          <h2 className="text-3xl font-bold">{t.ctaTitle}</h2>
          <p className="mt-4 text-blue-100">{t.ctaDesc}</p>

          <Link
            href="/register"
            className="inline-block mt-6 px-6 py-3 bg-white text-blue-600 rounded-xl font-semibold"
          >
            {t.ctaButton}
          </Link>

          <p className="mt-8 text-center text-sm text-blue-100 max-w-2xl mx-auto">
            {t.disclaimer}
          </p>
        </div>
      </section>
    </main>
  );
}
