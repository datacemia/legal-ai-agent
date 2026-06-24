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
  UserCheck,
} from "lucide-react";

type Locale = "en" | "fr" | "ar";

const labels: any = {
  en: {
    platform: "Runexa AI Platform",
    title:
      "Analyze contracts, financial documents, study materials, and business reports in minutes.",
    desc:
      "Upload documents, detect risks, uncover insights, generate recommendations, and make faster decisions with specialized AI workflows built for real-world work.",
    explore: "Explore AI Agents",
    pricing: "Plans & Pricing",
    blog: "Insights",
    trustLine:
      "$1 trial per account · Unified credits · Privacy-first AI platform",
    privacyIntroTitle: "Built for Sensitive Documents",
    privacyIntroDesc:
      "Runexa is designed for document analysis workflows where privacy matters. Uploaded files are processed only to generate the requested analysis. Personal identifiers are anonymized before AI processing. Customer content is never used to train public AI models. Uploaded files are automatically deleted from processing storage after analysis, and customer data remains isolated between users and workspaces.",
    privacyFlow: [
      "Upload file",
      "Identifiers anonymized",
      "AI analysis",
      "Report generated",
      "File deleted",
    ],
    privacyPromises: [
      "Personal identifiers are anonymized before AI processing",
      "Customer content is never used to train public AI models",
      "Uploaded files are automatically deleted after analysis",
      "Customer data remains isolated between users and workspaces",
    ],
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
    ["Privacy-first workflow", "Upload → anonymize → analyze → delete"],
    ["No public model training", "Customer content is never used to train public AI models"],
    ["Automatic file deletion", "Uploaded files are automatically deleted after analysis"],
    ["Workspace isolation", "Customer data remains isolated between users"],
  ],
    enterpriseBadge: "Custom AI Solutions",
    enterpriseTitle: "Runexa for Enterprises",
    enterpriseSubtitle:
      "Custom AI systems for teams, companies, and organizations.",
    enterpriseDesc:
      "Runexa helps organizations analyze contracts, financial documents, learning content, and business reports through specialized AI workflows designed for faster and more informed decision-making.",
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
      "Contract Intelligence & Clause Risk Scoring",
      "Financial Intelligence & Cashflow Coaching",
      "AI Study Workspace & Adaptive Learning",
      "Data-Verified Business Decision Intelligence",
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
      "Review contracts with clause-by-clause risk scoring, red flag detection, obligation extraction, negotiation recommendations, and practical decision guidance before signing.",
      "/legal-ai",
      "legal",
    ],
    [
      "Runexa Finance Intelligence Agent",
      "Upload a bank statement and receive a complete financial intelligence report with cashflow analysis, financial health scoring, spending categorization, subscription detection, savings opportunities, budget recommendations, financial risk monitoring, multilingual explanations, and an AI financial coach.",
      "/finance-ai",
      "finance",
    ],
    [
      "Runexa Study Workspace",
      "Upload a lesson, PDF, Word document, or scanned file and automatically generate a complete personalized learning workspace with structured summaries, detailed explanations, audio lessons, visual summaries, interactive mind maps, exam-style quizzes, instant grading, learning feedback, flashcards, personalized study plans, weak-point tracking, and adaptive learning sessions. Available in English, French, and Arabic.",
      "/study-ai",
      "study",
    ],
    [
      "Runexa Business Decision Intelligence",
      "Upload CSV or Excel business data and receive a data-verified executive dashboard with deterministic KPI calculations, revenue, expenses, profit, margin, growth, cashflow, ROAS, CAC, churn, forecasts, risks, opportunities, priority decisions, charts, and export-ready PDF and PowerPoint reports.",
      "/business-ai",
      "business",
    ],
  ],
  },

  fr: {
    platform: "Plateforme IA Runexa",
    title:
      "Analysez des contrats, documents financiers, supports d’apprentissage et rapports business en quelques minutes.",
    desc:
      "Importez vos documents, détectez les risques, extrayez les insights, générez des recommandations et prenez des décisions plus rapidement avec des workflows IA spécialisés.",
    explore: "Découvrir les agents IA",
    pricing: "Plans et tarifs",
    blog: "Ressources & Insights",
    trustLine:
      "Un essai à 1 $ par compte · Crédits unifiés · Plateforme IA conçue pour la confidentialité",
    privacyIntroTitle: "Conçu pour les documents sensibles",
    privacyIntroDesc:
      "Runexa est conçu pour les workflows d’analyse documentaire où la confidentialité est essentielle. Les fichiers importés sont traités uniquement pour générer l’analyse demandée. Les identifiants personnels sont anonymisés avant le traitement par l’IA. Les contenus clients ne servent jamais à entraîner des modèles IA publics. Les fichiers importés sont automatiquement supprimés du stockage de traitement après analyse, et les données restent isolées entre utilisateurs et espaces de travail.",
    privacyFlow: [
      "Importer le fichier",
      "Identifiants anonymisés",
      "Analyse IA",
      "Rapport généré",
      "Fichier supprimé",
    ],
    privacyPromises: [
      "Les identifiants personnels sont anonymisés avant le traitement par l’IA",
      "Les contenus clients ne servent jamais à entraîner des modèles IA publics",
      "Les fichiers importés sont supprimés automatiquement après analyse",
      "Les données restent isolées entre utilisateurs et espaces de travail",
    ],
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
      ["Workflow confidentiel", "Importer → anonymiser → analyser → supprimer"],
      ["Pas d’entraînement public", "Les contenus clients ne servent jamais à entraîner des modèles IA publics"],
      ["Suppression automatique", "Les fichiers importés sont supprimés après analyse"],
      ["Isolation des espaces", "Les données restent isolées entre utilisateurs"],
    ],
    enterpriseBadge: "Solutions IA personnalisées",
    enterpriseTitle: "Runexa pour les entreprises",
    enterpriseSubtitle:
      "Des systèmes d’IA personnalisés pour les équipes, les entreprises et les organisations.",
    enterpriseDesc:
      "Runexa aide les organisations à analyser des contrats, documents financiers, contenus d’apprentissage et rapports business grâce à des workflows IA spécialisés conçus pour des décisions plus rapides et mieux informées.",
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
      "Intelligence contractuelle et scoring des risques par clause",
      "Intelligence financière et coaching cashflow",
      "Espace d’apprentissage IA et apprentissage adaptatif",
      "Business Decision Intelligence vérifiée par les données",
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
      "Analysez vos contrats avec scoring clause par clause, détection des red flags, extraction des obligations, recommandations de négociation et décision pratique avant signature.",
      "/legal-ai",
      "legal",
    ],
    [
      "Runexa Finance Intelligence Agent",
      "Importez un relevé bancaire et obtenez un rapport complet d’intelligence financière avec analyse du cashflow, score de santé financière, catégorisation automatique des dépenses, détection des abonnements, opportunités d’économies, recommandations budgétaires, surveillance des risques financiers, explications multilingues et coach financier IA.",
      "/finance-ai",
      "finance",
    ],
    [
      "Runexa Study Workspace",
      "Transformez un cours, un PDF, un document Word ou un document scanné en espace d’apprentissage personnalisé avec résumés structurés, explications détaillées, audio, cartes visuelles, mind maps interactives, quiz type examen, correction instantanée, feedback pédagogique, flashcards, plans de révision personnalisés, suivi des points faibles et sessions d’apprentissage adaptatives. Disponible en français, anglais et arabe.",
      "/study-ai",
      "study",
    ],
    [
      "Runexa Business Decision Intelligence",
      "Importez des données business CSV ou Excel et obtenez un tableau de bord exécutif vérifié avec calculs KPI déterministes, revenus, dépenses, profit, marge, croissance, cashflow, ROAS, CAC, churn, prévisions, risques, opportunités, décisions prioritaires, graphiques et rapports PDF/PowerPoint exportables.",
      "/business-ai",
      "business",
    ],
  ],
  },

  ar: {
    platform: "مساحة Runexa للذكاء الاصطناعي",
    title: "حلّل العقود والمستندات المالية ومواد الدراسة وتقارير الأعمال خلال دقائق",
    desc: "ارفع مستنداتك، واكتشف المخاطر، واستخرج الرؤى، وأنشئ توصيات قابلة للتنفيذ عبر تدفقات عمل ذكاء اصطناعي متخصصة للأعمال الواقعية",
    explore: "استكشف حلول الذكاء الاصطناعي",
    pricing: "الخطط والأسعار",
    blog: "المدونة",
    trustLine: "تجربة واحدة بقيمة 1 دولار لكل حساب · أرصدة موحدة · منصة ذكاء اصطناعي مصممة لحماية الخصوصية",
    privacyIntroTitle: "مصمم للمستندات الحساسة",
    privacyIntroDesc:
      "تم تصميم Runexa لتدفقات عمل تحليل المستندات التي تتطلب الخصوصية. تُعالج الملفات المرفوعة فقط لإنشاء التحليل المطلوب. يتم إخفاء هوية المعرّفات الشخصية قبل المعالجة بالذكاء الاصطناعي. لا تُستخدم محتويات العملاء أبداً لتدريب نماذج ذكاء اصطناعي عامة. ويتم حذف الملفات المرفوعة تلقائياً من تخزين المعالجة بعد اكتمال التحليل، وتبقى بيانات العملاء معزولة بين المستخدمين ومساحات العمل.",
    privacyFlow: [
      "رفع الملف",
      "إخفاء الهوية",
      "تحليل بالذكاء الاصطناعي",
      "إنشاء التقرير",
      "حذف الملف",
    ],
    privacyPromises: [
      "يتم إخفاء هوية المعرّفات الشخصية قبل المعالجة بالذكاء الاصطناعي",
      "لا تُستخدم محتويات العملاء أبداً لتدريب نماذج ذكاء اصطناعي عامة",
      "يتم حذف الملفات المرفوعة تلقائياً بعد اكتمال التحليل",
      "تبقى بيانات العملاء معزولة بين المستخدمين ومساحات العمل",
    ],
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
      ["Workflow يركز على الخصوصية", "رفع → إخفاء الهوية → تحليل → حذف"],
      ["بدون تدريب عام", "لا تُستخدم محتويات العملاء أبداً لتدريب نماذج عامة"],
      ["حذف تلقائي", "يتم حذف الملفات المرفوعة بعد التحليل"],
      ["عزل مساحات العمل", "تبقى بيانات العملاء معزولة بين المستخدمين"],
    ],
    enterpriseBadge: "حلول ذكاء اصطناعي للمؤسسات",

    enterpriseTitle: "Runexa للمؤسسات",

    enterpriseSubtitle:
      "أنظمة ذكاء اصطناعي مخصصة للفرق والشركات والمؤسسات.",
    enterpriseDesc:
      "تساعد Runexa المؤسسات على تحليل العقود والمستندات المالية ومحتوى التعلّم وتقارير الأعمال من خلال تدفقات عمل ذكاء اصطناعي متخصصة لاتخاذ قرارات أسرع وأكثر وضوحاً.",

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
    enterpriseHeader: "Runexa Business AI",
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
      "ذكاء العقود وتقييم المخاطر بنداً ببند",
      "الذكاء المالي وتدريب التدفقات النقدية",
      "مساحة تعلم ذكية وتعلم تكيفي",
      "ذكاء قرارات الأعمال الموثق بالبيانات",
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
          "راجع العقود مع تقييم المخاطر بنداً ببند، واكتشاف العلامات التحذيرية، واستخراج الالتزامات، وتوصيات التفاوض، وتوجيه عملي قبل التوقيع.",
          "/legal-ai",
          "legal",
        ],

        [
          "Runexa Finance Intelligence Agent",
          "ارفع كشفاً بنكياً واحصل على تقرير متكامل للذكاء المالي يتضمن تحليل التدفقات النقدية، وتقييم الصحة المالية، وتصنيف النفقات تلقائياً، واكتشاف الاشتراكات المتكررة، وفرص التوفير، والتوصيات المالية، ومراقبة المخاطر، وشرحاً باللغات العربية والإنجليزية والفرنسية، بالإضافة إلى مدرب مالي ذكي يمكنك التفاعل معه.",
          "/finance-ai",
          "finance",
        ],

        [
          "Runexa Study Workspace",
          "حوّل أي درس أو ملف PDF أو Word أو مستند ممسوح ضوئياً إلى مساحة تعلم شخصية متكاملة تتضمن ملخصات منظمة، شروحات مفصلة، دروساً صوتية، خرائط بصرية، خرائط ذهنية تفاعلية، اختبارات بأسلوب الامتحانات، تصحيحاً فورياً، تغذية راجعة تعليمية، بطاقات مراجعة، خطط دراسة شخصية، تتبع نقاط الضعف وجلسات تعلم تكيفية. متوفر بالعربية والإنجليزية والفرنسية.",
          "/study-ai",
          "study",
        ],

        [
          "Runexa Business Decision Intelligence",
          "ارفع بيانات أعمال بصيغة CSV أو Excel واحصل على لوحة تنفيذية موثقة تعتمد على حسابات KPI حتمية، وتشمل الإيرادات، النفقات، الربح، الهامش، النمو، التدفق النقدي، ROAS، CAC، معدل فقدان العملاء، التوقعات، المخاطر، الفرص، القرارات ذات الأولوية، الرسوم البيانية، وتقارير PDF وPowerPoint قابلة للتصدير.",
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

export default function HomeClient({
  initialLanguage = "en",
  lockInitialLanguage = false,
}: {
  initialLanguage?: Locale;
  lockInitialLanguage?: boolean;
}) {
  const [language, setLanguage] = useState<Locale>(initialLanguage);
  const t = labels[language] || labels.en;

  useEffect(() => {
    if (lockInitialLanguage) {
      setLanguage(initialLanguage);
      return;
    }

    const saved = localStorage.getItem("locale");

    if (
      saved === "en" ||
      saved === "fr" ||
      saved === "ar"
    ) {
      setLanguage(saved);
      return;
    }

    setLanguage(initialLanguage);
  }, [initialLanguage, lockInitialLanguage]);

  const handleLanguageChange = (lang: Locale) => {
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
              onChange={(e) => {
                const nextLanguage = e.target.value;

                if (
                  nextLanguage === "en" ||
                  nextLanguage === "fr" ||
                  nextLanguage === "ar"
                ) {
                  handleLanguageChange(nextLanguage);
                }
              }}
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

          <div className="mx-auto max-w-5xl rounded-[28px] border border-blue-100 bg-white/90 p-5 text-left shadow-sm backdrop-blur md:p-6">
            <div className="flex flex-col gap-5 md:flex-row md:items-start md:justify-between">
              <div className="max-w-3xl">
                <div className="inline-flex items-center gap-2 rounded-full border border-blue-200 bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-700">
                  <ShieldCheck className="h-4 w-4" />
                  <span>
                    {language === "fr"
                      ? "Traitement des données"
                      : language === "ar"
                      ? "معالجة البيانات"
                      : "Data handling"}
                  </span>
                </div>

                <h2 className="mt-3 text-2xl font-bold text-slate-900">
                  {t.privacyIntroTitle}
                </h2>

                <p className="mt-3 text-sm leading-6 text-slate-600 md:text-base md:leading-7">
                  {t.privacyIntroDesc}
                </p>
              </div>

              <Link
                href="/security"
                className="inline-flex shrink-0 items-center justify-center rounded-xl border border-blue-200 bg-blue-50 px-4 py-3 text-sm font-semibold text-blue-700 hover:bg-blue-100 transition"
              >
                {language === "fr"
                  ? "Voir la sécurité"
                  : language === "ar"
                  ? "عرض الأمان"
                  : "View security"}
              </Link>
            </div>

            <div className="mt-6 grid gap-3 md:grid-cols-5">
              {t.privacyFlow.map((item: string, index: number) => (
                <div
                  key={item}
                  className="rounded-2xl border border-slate-200 bg-slate-50 p-4 text-center"
                >
                  <div className="mx-auto flex h-8 w-8 items-center justify-center rounded-full bg-blue-600 text-xs font-bold text-white">
                    {index + 1}
                  </div>

                  <p className="mt-3 text-sm font-semibold text-slate-800">
                    {item}
                  </p>
                </div>
              ))}
            </div>

            <div className="mt-5 grid gap-3 md:grid-cols-2">
              {t.privacyPromises.map((item: string) => (
                <div
                  key={item}
                  className="flex items-start gap-3 rounded-2xl border border-slate-200 bg-white p-4"
                >
                  <ShieldCheck className="mt-0.5 h-5 w-5 shrink-0 text-blue-600" />
                  <p className="text-sm font-medium text-slate-700">
                    {item}
                  </p>
                </div>
              ))}
            </div>
          </div>


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
                        ? "Exemple juridique"
                        : language === "ar"
                        ? "مثال قانوني"
                        : "Legal example"}
                    </p>
                    <p className="mt-2 text-lg font-bold text-blue-600">
                      Employment Agreement.pdf
                    </p>

                    <p className="mt-2 text-sm text-slate-500">
                      {language === "fr"
                        ? "25 clauses · 1 risque élevé · 7 risques moyens"
                        : language === "ar"
                        ? "25 بنداً · خطر مرتفع واحد · 7 مخاطر متوسطة"
                        : "25 clauses · 1 high risk · 7 medium risks"}
                    </p>
                  </div>

                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-5">
                    <p className="text-sm text-slate-500">
                      {language === "fr"
                        ? "Exemple finance"
                        : language === "ar"
                        ? "مثال مالي"
                        : "Finance example"}
                    </p>

                    <p className="mt-2 text-lg font-bold text-emerald-600">
                      OMAR.pdf
                    </p>

                    <p className="mt-2 text-sm text-slate-500">
                      {language === "fr"
                        ? "85/100 · +4 911 € cashflow · 1 548 € d’économies"
                        : language === "ar"
                        ? "85/100 · تدفق نقدي +4,911€ · توفير 1,548€"
                        : "85/100 · +€4,911 cashflow · €1,548 savings"}
                    </p>
                  </div>

                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-5">
                    <p className="text-sm text-slate-500">
                      {language === "fr"
                        ? "Exemple étude"
                        : language === "ar"
                        ? "مثال دراسي"
                        : "Study example"}
                    </p>

                    <p className="mt-2 text-lg font-bold text-violet-600">
                      Arabic Geography Lesson.pdf
                    </p>

                    <p className="mt-2 text-sm text-slate-500">
                      {language === "fr"
                        ? "Résumé · audio · mind map · quiz · plan 5 jours"
                        : language === "ar"
                        ? "ملخص · صوت · خريطة ذهنية · اختبار · خطة 5 أيام"
                        : "Summary · audio · mind map · quiz · 5-day plan"}
                    </p>
                  </div>

                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-5">
                    <p className="text-sm text-slate-500">
                      {language === "fr"
                        ? "Exemple business"
                        : language === "ar"
                        ? "مثال أعمال"
                        : "Business example"}
                    </p>

                    <p className="mt-2 text-lg font-bold text-orange-600">
                      business.csv
                    </p>

                    <p className="mt-2 text-sm text-slate-500">
                      {language === "fr"
                        ? "91/100 · 52,75% croissance · dashboard exécutif"
                        : language === "ar"
                        ? "91/100 · نمو 52.75% · لوحة تنفيذية"
                        : "91/100 · 52.75% growth · executive dashboard"}
                    </p>
                  </div>
                </div>
              </div>

              <div className="rounded-3xl bg-slate-950 p-6 text-white shadow-2xl">
                <div className="flex items-center justify-between border-b border-white/10 pb-4">
                  <div>
                    <p className="text-sm text-slate-400">
                      {language === "fr"
                        ? "Plateforme IA Runexa"
                        : language === "ar"
                        ? "منصة Runexa للذكاء الاصطناعي"
                        : "Runexa AI Platform"}
                    </p>

                    <p className="text-lg font-semibold">
                      {language === "fr"
                        ? "Recommandations IA"
                        : language === "ar"
                        ? "توصيات الذكاء الاصطناعي"
                        : "AI Recommendations"}
                    </p>
                  </div>

                  <span className="rounded-full bg-green-500/10 px-3 py-1 text-xs font-medium text-green-300">
                    {language === "fr"
                      ? "Temps réel"
                      : language === "ar"
                      ? "لحظي"
                      : "Real-Time"}
                  </span>
                </div>

                <div className="mt-6 space-y-4">
                  {[
                    language === "fr"
                      ? "Analyser les clauses de résiliation, cession de droits, confidentialité et obligations"
                      : language === "ar"
                      ? "تحليل بنود الإنهاء والتنازل عن الحقوق والسرية والالتزامات"
                      : "Analyze termination, assignment of rights, confidentiality, and obligation clauses",

                    language === "fr"
                      ? "Transformer un relevé bancaire en score financier, cashflow, budget et plan d’économies"
                      : language === "ar"
                      ? "تحويل كشف بنكي إلى درجة مالية وتدفق نقدي وميزانية وخطة توفير"
                      : "Turn a bank statement into a financial score, cashflow, budget, and savings plan",

                    language === "fr"
                      ? "Transformer un cours en résumé, audio, mind map, quiz, flashcards et plan de révision"
                      : language === "ar"
                      ? "تحويل درس إلى ملخص وصوت وخريطة ذهنية واختبار وبطاقات وخطة مراجعة"
                      : "Turn a lesson into a summary, audio, mind map, quiz, flashcards, and revision plan",

                    language === "fr"
                      ? "Calculer les KPI, détecter les risques, prévoir la croissance et générer une décision prioritaire"
                      : language === "ar"
                      ? "حساب مؤشرات الأداء، اكتشاف المخاطر، توقع النمو، وإنشاء قرار ذي أولوية"
                      : "Calculate KPIs, detect risks, forecast growth, and generate a priority decision",
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

      <section className="px-6 py-12">
        <div className="max-w-6xl mx-auto">
          <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm md:p-12">
            <p className="text-sm font-semibold text-blue-600">
              {language === "fr"
                ? "Runexa Legal Agent"
                : language === "ar"
                ? "وكيل Runexa القانوني"
                : "Runexa Legal Agent"}
            </p>

            <h2 className="mt-3 text-3xl font-bold text-slate-900">
              {language === "fr"
                ? "Bien plus qu’un résumé de contrat."
                : language === "ar"
                ? "أكثر من مجرد تلخيص للعقد."
                : "More than a contract summary."}
            </h2>

            <p className="mt-4 max-w-4xl text-slate-600 leading-7">
              {language === "fr"
                ? "Le Legal Agent transforme un contrat en rapport d’intelligence juridique structuré : score de risque global, analyse clause par clause, red flags, partie favorisée, obligations, dépendances entre clauses, priorités de négociation et décision pratique."
                : language === "ar"
                ? "يحوّل الوكيل القانوني العقد إلى تقرير ذكاء قانوني منظم: درجة المخاطر العامة، تحليل بنداً ببند، علامات تحذيرية، الطرف المستفيد، الالتزامات، العلاقات بين البنود، أولويات التفاوض، وتوجيه عملي."
                : "The Legal Agent turns a contract into a structured legal intelligence report: overall risk score, clause-by-clause analysis, red flags, favored party, obligations, clause dependencies, negotiation priorities, and practical decision guidance."}
            </p>

            <div className="mt-8 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              {[
                language === "fr" ? "Score de risque global" : language === "ar" ? "درجة المخاطر العامة" : "Overall risk score",
                language === "fr" ? "Analyse clause par clause" : language === "ar" ? "تحليل بنداً ببند" : "Clause-by-clause analysis",
                language === "fr" ? "Red flags et partie favorisée" : language === "ar" ? "علامات تحذيرية والطرف المستفيد" : "Red flags and favored party",
                language === "fr" ? "Recommandations de négociation" : language === "ar" ? "توصيات التفاوض" : "Negotiation recommendations",
                language === "fr" ? "Extraction des obligations" : language === "ar" ? "استخراج الالتزامات" : "Obligation extraction",
                language === "fr" ? "Dépendances entre clauses" : language === "ar" ? "العلاقات بين البنود" : "Clause dependency mapping",
                language === "fr" ? "Qualité et complexité du contrat" : language === "ar" ? "جودة العقد وتعقيده" : "Contract quality and complexity",
                language === "fr" ? "Décision pratique avant signature" : language === "ar" ? "توجيه عملي قبل التوقيع" : "Practical decision before signing",
              ].map((item) => (
                <div
                  key={item}
                  className="rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm font-semibold text-slate-700"
                >
                  {item}
                </div>
              ))}
            </div>

            <div className="mt-8 rounded-3xl border border-blue-100 bg-blue-50 p-6">
              <p className="text-sm font-semibold text-blue-700">
                {language === "fr"
                  ? "Exemple réel de sortie"
                  : language === "ar"
                  ? "مثال واقعي للمخرجات"
                  : "Real output example"}
              </p>

              <div className="mt-4 grid gap-4 md:grid-cols-3">
                <div className="rounded-2xl bg-white p-4">
                  <p className="text-sm text-slate-500">
                    {language === "fr" ? "Contrat analysé" : language === "ar" ? "العقد المحلل" : "Analyzed contract"}
                  </p>
                  <p className="mt-2 font-bold text-slate-900">Employment Agreement.pdf</p>
                </div>

                <div className="rounded-2xl bg-white p-4">
                  <p className="text-sm text-slate-500">
                    {language === "fr" ? "Résultat détecté" : language === "ar" ? "النتيجة المكتشفة" : "Detected result"}
                  </p>
                  <p className="mt-2 font-bold text-slate-900">
                    {language === "fr" ? "25 clauses · 1 risque élevé · 7 risques moyens" : language === "ar" ? "25 بنداً · خطر مرتفع واحد · 7 مخاطر متوسطة" : "25 clauses · 1 high risk · 7 medium risks"}
                  </p>
                </div>

                <div className="rounded-2xl bg-white p-4">
                  <p className="text-sm text-slate-500">
                    {language === "fr" ? "Décision pratique" : language === "ar" ? "التوجيه العملي" : "Practical decision"}
                  </p>
                  <p className="mt-2 font-bold text-slate-900">
                    {language === "fr" ? "Négocier avant signature" : language === "ar" ? "التفاوض قبل التوقيع" : "Negotiate before signing"}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="px-6 py-12">
        <div className="max-w-6xl mx-auto">
          <div className="rounded-3xl border border-emerald-200 bg-white p-8 shadow-sm md:p-12">
            <p className="text-sm font-semibold text-emerald-600">
              {language === "fr"
                ? "Runexa Finance Intelligence Agent"
                : language === "ar"
                ? "وكيل Runexa للذكاء المالي"
                : "Runexa Finance Intelligence Agent"}
            </p>

            <h2 className="mt-3 text-3xl font-bold text-slate-900">
              {language === "fr"
                ? "Pas seulement un suivi des dépenses."
                : language === "ar"
                ? "ليس مجرد تتبع للنفقات."
                : "Not just expense tracking."}
            </h2>

            <p className="mt-4 max-w-4xl text-slate-600 leading-7">
              {language === "fr"
                ? "Le Finance Agent transforme un relevé bancaire en rapport d’intelligence financière : revenus observés, dépenses, cashflow net, score de santé financière, catégories de dépenses, détection des abonnements, opportunités d’économies, budget recommandé, notes de risque, graphiques et coach financier IA interactif."
                : language === "ar"
                ? "يحوّل وكيل التمويل كشف الحساب البنكي إلى تقرير ذكاء مالي: الدخل المرصود، النفقات، التدفق النقدي الصافي، درجة الصحة المالية، تصنيف المصاريف، اكتشاف الاشتراكات، فرص التوفير، الميزانية المقترحة، ملاحظات المخاطر، الرسوم البيانية، ومدرب مالي ذكي تفاعلي."
                : "The Finance Agent turns a bank statement into a financial intelligence report: observed income, expenses, net cashflow, financial health score, spending categories, subscription detection, savings opportunities, recommended budget, risk notes, charts, and an interactive AI financial coach."}
            </p>

            <div className="mt-8 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              {[
                language === "fr" ? "Revenus et dépenses détectés" : language === "ar" ? "اكتشاف الدخل والنفقات" : "Income and expenses detected",
                language === "fr" ? "Cashflow net et tendance" : language === "ar" ? "التدفق النقدي الصافي والاتجاه" : "Net cashflow and trend",
                language === "fr" ? "Score de santé financière" : language === "ar" ? "درجة الصحة المالية" : "Financial health score",
                language === "fr" ? "Catégorisation des dépenses" : language === "ar" ? "تصنيف النفقات" : "Spending categorization",
                language === "fr" ? "Détection des abonnements" : language === "ar" ? "اكتشاف الاشتراكات" : "Subscription detection",
                language === "fr" ? "Opportunités d’économies" : language === "ar" ? "فرص التوفير" : "Savings opportunities",
                language === "fr" ? "Budget recommandé" : language === "ar" ? "ميزانية مقترحة" : "Recommended budget",
                language === "fr" ? "Coach financier IA" : language === "ar" ? "مدرب مالي ذكي" : "AI financial coach",
              ].map((item) => (
                <div
                  key={item}
                  className="rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm font-semibold text-slate-700"
                >
                  {item}
                </div>
              ))}
            </div>

            <div className="mt-8 rounded-3xl border border-emerald-100 bg-emerald-50 p-6">
              <p className="text-sm font-semibold text-emerald-700">
                {language === "fr"
                  ? "Exemple réel de sortie"
                  : language === "ar"
                  ? "مثال واقعي للمخرجات"
                  : "Real output example"}
              </p>

              <div className="mt-4 grid gap-4 md:grid-cols-5">
                <div className="rounded-2xl bg-white p-4">
                  <p className="text-sm text-slate-500">
                    {language === "fr" ? "Relevé analysé" : language === "ar" ? "الكشف المحلل" : "Analyzed statement"}
                  </p>
                  <p className="mt-2 font-bold text-slate-900">OMAR.pdf</p>
                </div>

                <div className="rounded-2xl bg-white p-4">
                  <p className="text-sm text-slate-500">
                    {language === "fr" ? "Revenus" : language === "ar" ? "الدخل" : "Income"}
                  </p>
                  <p className="mt-2 font-bold text-slate-900">€20,393</p>
                </div>

                <div className="rounded-2xl bg-white p-4">
                  <p className="text-sm text-slate-500">
                    {language === "fr" ? "Dépenses" : language === "ar" ? "النفقات" : "Expenses"}
                  </p>
                  <p className="mt-2 font-bold text-slate-900">€15,481</p>
                </div>

                <div className="rounded-2xl bg-white p-4">
                  <p className="text-sm text-slate-500">
                    {language === "fr" ? "Cashflow net" : language === "ar" ? "التدفق الصافي" : "Net cashflow"}
                  </p>
                  <p className="mt-2 font-bold text-slate-900">+€4,911</p>
                </div>

                <div className="rounded-2xl bg-white p-4">
                  <p className="text-sm text-slate-500">
                    {language === "fr" ? "Score financier" : language === "ar" ? "الدرجة المالية" : "Finance score"}
                  </p>
                  <p className="mt-2 font-bold text-slate-900">85/100</p>
                </div>
              </div>

              <p className="mt-4 text-sm leading-6 text-emerald-900">
                {language === "fr"
                  ? "Runexa a aussi identifié une opportunité d’économies estimée à 1 548 € et un cashflow positif, avec des notes de risque et des stratégies d’épargne."
                  : language === "ar"
                  ? "حددت Runexa أيضاً فرصة توفير تقديرية بقيمة 1,548 يورو وتدفقاً نقدياً إيجابياً، مع ملاحظات حول المخاطر واستراتيجيات للادخار."
                  : "Runexa also identified an estimated €1,548 savings opportunity and positive cashflow, with risk notes and savings strategies."}
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="px-6 py-12">
        <div className="max-w-6xl mx-auto">
          <div className="rounded-3xl border border-violet-200 bg-white p-8 shadow-sm md:p-12">
            <p className="text-sm font-semibold text-violet-600">
              {language === "fr"
                ? "Runexa Study Workspace"
                : language === "ar"
                ? "مساحة Runexa التعليمية"
                : "Runexa Study Workspace"}
            </p>

            <h2 className="mt-3 text-3xl font-bold text-slate-900">
              {language === "fr"
                ? "Bien plus qu’un simple résumé de cours."
                : language === "ar"
                ? "أكثر من مجرد تلخيص للدرس."
                : "More than a study summary."}
            </h2>

            <p className="mt-4 max-w-4xl text-slate-600 leading-7">
              {language === "fr"
                ? "Le Study Workspace transforme des cours, PDF, documents Word et fichiers scannés en environnement d’apprentissage complet : résumés, explications détaillées, audio, cartes visuelles, mind maps interactives, quiz type examen, correction instantanée, feedback pédagogique, flashcards, plans de révision et apprentissage adaptatif selon le niveau de l’étudiant."
                : language === "ar"
                ? "تحوّل مساحة Runexa التعليمية الدروس وملفات PDF وWord والمستندات الممسوحة ضوئياً إلى بيئة تعلم متكاملة: ملخصات، شروحات مفصلة، دروس صوتية، خرائط بصرية، خرائط ذهنية تفاعلية، اختبارات بأسلوب الامتحانات، تصحيح فوري، تغذية راجعة تعليمية، بطاقات مراجعة، خطط مراجعة وتعلم تكيفي حسب مستوى الطالب."
                : "The Study Workspace turns lessons, PDFs, Word documents, and scanned files into a complete learning environment: summaries, detailed explanations, audio lessons, visual maps, interactive mind maps, exam-style quizzes, instant grading, learning feedback, flashcards, revision plans, and adaptive learning based on the student's level."}
            </p>

            <div className="mt-8 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              {[
                language === "fr" ? "Résumés structurés" : language === "ar" ? "ملخصات منظمة" : "Structured summaries",
                language === "fr" ? "Explications détaillées" : language === "ar" ? "شروحات مفصلة" : "Detailed explanations",
                language === "fr" ? "Lecture audio" : language === "ar" ? "دروس صوتية" : "Audio lessons",
                language === "fr" ? "Cartes visuelles" : language === "ar" ? "خرائط بصرية" : "Visual summaries",
                language === "fr" ? "Mind maps interactives" : language === "ar" ? "خرائط ذهنية تفاعلية" : "Interactive mind maps",
                language === "fr" ? "Quiz type examen" : language === "ar" ? "اختبارات بأسلوب الامتحانات" : "Exam-style quizzes",
                language === "fr" ? "Correction instantanée" : language === "ar" ? "تصحيح فوري" : "Instant grading",
                language === "fr" ? "Feedback pédagogique" : language === "ar" ? "تغذية راجعة تعليمية" : "Learning feedback",
                language === "fr" ? "Flashcards" : language === "ar" ? "بطاقات مراجعة" : "Flashcards",
                language === "fr" ? "Plan de révision personnalisé" : language === "ar" ? "خطة مراجعة شخصية" : "Personalized study plan",
                language === "fr" ? "Suivi des points faibles" : language === "ar" ? "تتبع نقاط الضعف" : "Weak-point tracking",
                language === "fr" ? "Apprentissage adaptatif" : language === "ar" ? "تعلم تكيفي" : "Adaptive learning",
              ].map((item) => (
                <div
                  key={item}
                  className="rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm font-semibold text-slate-700"
                >
                  {item}
                </div>
              ))}
            </div>

            <div className="mt-8 rounded-3xl border border-violet-100 bg-violet-50 p-6">
              <p className="text-sm font-semibold text-violet-700">
                {language === "fr"
                  ? "Exemple réel de sortie"
                  : language === "ar"
                  ? "مثال واقعي للمخرجات"
                  : "Real output example"}
              </p>

              <div className="mt-4 grid gap-4 md:grid-cols-3">
                <div className="rounded-2xl bg-white p-4">
                  <p className="text-sm text-slate-500">
                    {language === "fr" ? "Document source" : language === "ar" ? "المستند المصدر" : "Source document"}
                  </p>
                  <p className="mt-2 font-bold text-slate-900">
                    {language === "fr" ? "Cours de géographie arabe, 2 pages" : language === "ar" ? "درس جغرافيا عربي من صفحتين" : "2-page Arabic geography lesson"}
                  </p>
                </div>

                <div className="rounded-2xl bg-white p-4">
                  <p className="text-sm text-slate-500">
                    {language === "fr" ? "Temps de traitement" : language === "ar" ? "وقت المعالجة" : "Processing time"}
                  </p>
                  <p className="mt-2 font-bold text-slate-900">
                    {language === "fr" ? "Moins de 2 minutes" : language === "ar" ? "أقل من دقيقتين" : "Under 2 minutes"}
                  </p>
                </div>

                <div className="rounded-2xl bg-white p-4">
                  <p className="text-sm text-slate-500">
                    {language === "fr" ? "Score qualité" : language === "ar" ? "درجة الجودة" : "Quality score"}
                  </p>
                  <p className="mt-2 font-bold text-slate-900">97/100</p>
                </div>
              </div>

              <p className="mt-4 text-sm leading-6 text-violet-900">
                {language === "fr"
                  ? "Runexa a généré un résumé, une explication détaillée, une lecture audio, une carte visuelle, une mind map interactive, 8 questions type examen, une correction instantanée, des flashcards, un feedback pédagogique et un plan de révision sur 5 jours."
                  : language === "ar"
                  ? "أنشأت Runexa ملخصاً، وشرحاً مفصلاً، ودرساً صوتياً، وخريطة بصرية، وخريطة ذهنية تفاعلية، و8 أسئلة بأسلوب الامتحانات، وتصحيحاً فورياً، وبطاقات مراجعة، وتغذية راجعة تعليمية، وخطة مراجعة لمدة 5 أيام."
                  : "Runexa generated a summary, detailed explanation, audio lesson, visual summary, interactive mind map, 8 exam-style questions, instant grading, flashcards, learning feedback, and a personalized 5-day study plan."}
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="px-6 py-12">
        <div className="max-w-6xl mx-auto">
          <div className="rounded-3xl border border-orange-200 bg-white p-8 shadow-sm md:p-12">
            <p className="text-sm font-semibold text-orange-600">
              {language === "fr"
                ? "Runexa Business Decision Intelligence"
                : language === "ar"
                ? "ذكاء قرارات الأعمال من Runexa"
                : "Runexa Business Decision Intelligence"}
            </p>

            <h2 className="mt-3 text-3xl font-bold text-slate-900">
              {language === "fr"
                ? "Pas seulement une explication de données business."
                : language === "ar"
                ? "ليس مجرد شرح لبيانات الأعمال."
                : "Not just business data explanation."}
            </h2>

            <p className="mt-4 max-w-4xl text-slate-600 leading-7">
              {language === "fr"
                ? "L’agent Business calcule d’abord les KPI à partir des données, puis l’IA explique ce que les chiffres signifient. Importez un CSV ou Excel et recevez un dashboard exécutif vérifié avec revenus, dépenses, profit, marge, croissance, cashflow, ROAS, CAC, churn, prévisions, risques, opportunités et décisions prioritaires."
                : language === "ar"
                ? "يقوم وكيل الأعمال أولاً بحساب مؤشرات الأداء من البيانات، ثم يشرح الذكاء الاصطناعي معنى الأرقام. ارفع ملف CSV أو Excel واحصل على لوحة تنفيذية موثقة تتضمن الإيرادات، النفقات، الربح، الهامش، النمو، التدفق النقدي، ROAS، CAC، معدل فقدان العملاء، التوقعات، المخاطر، الفرص، والقرارات ذات الأولوية."
                : "The Business Agent calculates KPIs from the data first, then AI explains what the numbers mean. Upload a CSV or Excel file and receive a data-verified executive dashboard with revenue, expenses, profit, margin, growth, cashflow, ROAS, CAC, churn, forecasts, risks, opportunities, and priority decisions."}
            </p>

            <div className="mt-8 rounded-3xl border border-orange-100 bg-orange-50 p-6">
              <p className="text-sm font-semibold text-orange-700">
                {language === "fr"
                  ? "Différence clé"
                  : language === "ar"
                  ? "الفرق الأساسي"
                  : "Key difference"}
              </p>

              <p className="mt-3 text-lg font-bold text-slate-900">
                {language === "fr"
                  ? "Une IA généraliste explique vos données. Runexa calcule d’abord la performance business, puis explique les décisions à prendre."
                  : language === "ar"
                  ? "الذكاء الاصطناعي العام يشرح بياناتك. أما Runexa فيحسب أداء الأعمال أولاً، ثم يوضح القرارات التي يجب اتخاذها."
                  : "General AI explains your business data. Runexa calculates business performance first, then explains what decisions to take."}
              </p>
            </div>

            <div className="mt-8 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              {[
                language === "fr" ? "Calculs KPI déterministes" : language === "ar" ? "حسابات KPI حتمية" : "Deterministic KPI calculations",
                language === "fr" ? "Score santé business" : language === "ar" ? "درجة صحة الأعمال" : "Business Health Score",
                language === "fr" ? "Revenus, dépenses, profit" : language === "ar" ? "الإيرادات والنفقات والربح" : "Revenue, expenses, profit",
                language === "fr" ? "Marge, croissance, cashflow" : language === "ar" ? "الهامش والنمو والتدفق النقدي" : "Margin, growth, cashflow",
                language === "fr" ? "ROAS, CAC, churn" : language === "ar" ? "ROAS و CAC وفقدان العملاء" : "ROAS, CAC, churn",
                language === "fr" ? "Détection anomalies et risques" : language === "ar" ? "اكتشاف الشذوذ والمخاطر" : "Anomaly and risk detection",
                language === "fr" ? "Prévisions revenu et cashflow" : language === "ar" ? "توقعات الإيرادات والتدفق النقدي" : "Revenue and cashflow forecasts",
                language === "fr" ? "Exports PDF et PowerPoint" : language === "ar" ? "تصدير PDF وPowerPoint" : "PDF and PowerPoint exports",
              ].map((item) => (
                <div
                  key={item}
                  className="rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm font-semibold text-slate-700"
                >
                  {item}
                </div>
              ))}
            </div>

            <div className="mt-8 rounded-3xl border border-orange-100 bg-orange-50 p-6">
              <p className="text-sm font-semibold text-orange-700">
                {language === "fr"
                  ? "Exemple réel de sortie"
                  : language === "ar"
                  ? "مثال واقعي للمخرجات"
                  : "Real output example"}
              </p>

              <div className="mt-4 grid gap-4 md:grid-cols-3 lg:grid-cols-6">
                <div className="rounded-2xl bg-white p-4">
                  <p className="text-sm text-slate-500">
                    {language === "fr" ? "Fichier analysé" : language === "ar" ? "الملف المحلل" : "Analyzed file"}
                  </p>
                  <p className="mt-2 font-bold text-slate-900">business.csv</p>
                </div>

                <div className="rounded-2xl bg-white p-4">
                  <p className="text-sm text-slate-500">
                    {language === "fr" ? "Score business" : language === "ar" ? "درجة الأعمال" : "Business score"}
                  </p>
                  <p className="mt-2 font-bold text-slate-900">91/100</p>
                </div>

                <div className="rounded-2xl bg-white p-4">
                  <p className="text-sm text-slate-500">
                    {language === "fr" ? "Revenus" : language === "ar" ? "الإيرادات" : "Revenue"}
                  </p>
                  <p className="mt-2 font-bold text-slate-900">$129,510</p>
                </div>

                <div className="rounded-2xl bg-white p-4">
                  <p className="text-sm text-slate-500">
                    {language === "fr" ? "Profit" : language === "ar" ? "الربح" : "Profit"}
                  </p>
                  <p className="mt-2 font-bold text-slate-900">$25,920</p>
                </div>

                <div className="rounded-2xl bg-white p-4">
                  <p className="text-sm text-slate-500">
                    {language === "fr" ? "Croissance" : language === "ar" ? "النمو" : "Growth"}
                  </p>
                  <p className="mt-2 font-bold text-slate-900">52.75%</p>
                </div>

                <div className="rounded-2xl bg-white p-4">
                  <p className="text-sm text-slate-500">
                    {language === "fr" ? "ROAS" : language === "ar" ? "ROAS" : "ROAS"}
                  </p>
                  <p className="mt-2 font-bold text-slate-900">8.74</p>
                </div>
              </div>

              <div className="mt-6 grid gap-4 md:grid-cols-3">
                <div className="rounded-2xl bg-white p-5">
                  <p className="text-sm font-semibold text-slate-900">
                    {language === "fr" ? "Décision prioritaire" : language === "ar" ? "القرار ذو الأولوية" : "Priority decision"}
                  </p>
                  <p className="mt-2 text-sm leading-6 text-slate-600">
                    {language === "fr"
                      ? "Prioriser la rétention avant d’augmenter les dépenses d’acquisition."
                      : language === "ar"
                      ? "إعطاء الأولوية للاحتفاظ بالعملاء قبل زيادة الإنفاق على الاكتساب."
                      : "Prioritize retention before increasing acquisition spend."}
                  </p>
                </div>

                <div className="rounded-2xl bg-white p-5">
                  <p className="text-sm font-semibold text-slate-900">
                    {language === "fr" ? "Risques détectés" : language === "ar" ? "المخاطر المكتشفة" : "Detected risks"}
                  </p>
                  <p className="mt-2 text-sm leading-6 text-slate-600">
                    {language === "fr"
                      ? "Risque de rétention, pression sur la marge, risque cashflow et qualité de croissance."
                      : language === "ar"
                      ? "مخاطر الاحتفاظ بالعملاء، ضغط الهامش، مخاطر التدفق النقدي، وجودة النمو."
                      : "Retention risk, margin pressure, cashflow pressure, and growth quality risk."}
                  </p>
                </div>

                <div className="rounded-2xl bg-white p-5">
                  <p className="text-sm font-semibold text-slate-900">
                    {language === "fr" ? "Exports exécutifs" : language === "ar" ? "تصديرات تنفيذية" : "Executive exports"}
                  </p>
                  <p className="mt-2 text-sm leading-6 text-slate-600">
                    {language === "fr"
                      ? "Rapport PDF et présentation PowerPoint prêts pour revue interne ou équipe dirigeante."
                      : language === "ar"
                      ? "تقرير PDF وعرض PowerPoint جاهزان للمراجعة الداخلية أو الفريق التنفيذي."
                      : "PDF report and PowerPoint presentation ready for internal review or leadership teams."}
                  </p>
                </div>
              </div>

              <p className="mt-4 text-sm leading-6 text-orange-900">
                {language === "fr"
                  ? "Runexa a aussi calculé une marge de 20,01%, un cashflow positif, des prévisions de revenu, une volatilité élevée, 2 risques et 5 signaux positifs."
                  : language === "ar"
                  ? "حسبت Runexa أيضاً هامشاً بنسبة 20.01%، وتدفقاً نقدياً إيجابياً، وتوقعات للإيرادات، وتقلباً مرتفعاً، ومخاطرين و5 إشارات إيجابية."
                  : "Runexa also calculated a 20.01% margin, positive cashflow, revenue forecasts, high volatility, 2 risks, and 5 positive signals."}
              </p>
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
          <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm md:p-12">
            <p className="text-sm font-semibold text-blue-600">
              {language === "fr"
                ? "Pourquoi Runexa"
                : language === "ar"
                ? "لماذا Runexa"
                : "Why Runexa"}
            </p>

            <h2 className="mt-3 text-3xl font-bold text-slate-900">
              {language === "fr"
                ? "Pourquoi utiliser Runexa plutôt qu’un chatbot IA généraliste ?"
                : language === "ar"
                ? "لماذا تستخدم Runexa بدلاً من روبوت ذكاء اصطناعي عام؟"
                : "Why use Runexa instead of a general AI chatbot?"}
            </h2>

            <p className="mt-4 max-w-4xl text-slate-600 leading-7">
              {language === "fr"
                ? "Runexa n’est pas seulement une zone de chat. Chaque agent suit un workflow spécialisé pour transformer des documents réels en analyses structurées, recommandations et rapports exploitables."
                : language === "ar"
                ? "Runexa ليست مجرد مساحة دردشة. يتبع كل وكيل تدفق عمل متخصصاً لتحويل المستندات الواقعية إلى تحليلات منظمة وتوصيات وتقارير قابلة للاستخدام."
                : "Runexa is not just a chat box. Each agent follows a specialized workflow to turn real documents into structured analysis, recommendations, and usable reports."}
            </p>

            <div className="mt-8 grid gap-4 md:grid-cols-2 lg:grid-cols-5">
              {[
                language === "fr" ? "Workflows spécialisés" : language === "ar" ? "تدفقات عمل متخصصة" : "Specialized workflows",
                language === "fr" ? "Rapports structurés" : language === "ar" ? "تقارير منظمة" : "Structured reports",
                language === "fr" ? "Analyse centrée document" : language === "ar" ? "تحليل يركز على المستندات" : "Document-focused analysis",
                language === "fr" ? "Traitement orienté confidentialité" : language === "ar" ? "معالجة تركز على الخصوصية" : "Privacy-focused processing",
                language === "fr" ? "Plusieurs agents dans un espace" : language === "ar" ? "عدة وكلاء في مساحة واحدة" : "Multiple agents in one workspace",
              ].map((item) => (
                <div
                  key={item}
                  className="rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm font-semibold text-slate-700"
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

      <section className="px-6 py-12">
        <div className="max-w-6xl mx-auto">
          <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm md:p-12">
            <p className="text-sm font-semibold text-blue-600">
              {language === "fr"
                ? "Méthodologie Runexa"
                : language === "ar"
                ? "منهجية Runexa"
                : "Runexa methodology"}
            </p>

            <h2 className="mt-3 text-3xl font-bold text-slate-900">
              {language === "fr"
                ? "Comment Runexa produit ses résultats."
                : language === "ar"
                ? "كيف تنتج Runexa نتائجها."
                : "How Runexa produces results."}
            </h2>

            <p className="mt-4 max-w-4xl text-slate-600 leading-7">
              {language === "fr"
                ? "Runexa ne fonctionne pas comme une simple zone de chat. Chaque agent suit un workflow spécialisé qui extrait, structure, calcule, vérifie et transforme les documents ou données en rapports exploitables."
                : language === "ar"
                ? "لا تعمل Runexa كمجرد مساحة دردشة. يتبع كل وكيل تدفق عمل متخصصاً لاستخراج المعلومات وتنظيمها وحسابها والتحقق منها وتحويل المستندات أو البيانات إلى تقارير قابلة للاستخدام."
                : "Runexa is not just a chat box. Each agent follows a specialized workflow that extracts, structures, calculates, verifies, and transforms documents or data into usable reports."}
            </p>

            <div className="mt-8 grid gap-5 md:grid-cols-2">
              {[
                {
                  title:
                    language === "fr"
                      ? "Legal Agent"
                      : language === "ar"
                      ? "الوكيل القانوني"
                      : "Legal Agent",
                  flow:
                    language === "fr"
                      ? "Import → OCR → extraction des clauses → scoring des risques → obligations → recommandations → rapport"
                      : language === "ar"
                      ? "رفع → OCR → استخراج البنود → تقييم المخاطر → الالتزامات → التوصيات → التقرير"
                      : "Upload → OCR → clause extraction → risk scoring → obligations → recommendations → report",
                },
                {
                  title:
                    language === "fr"
                      ? "Finance Agent"
                      : language === "ar"
                      ? "وكيل التمويل"
                      : "Finance Agent",
                  flow:
                    language === "fr"
                      ? "Relevé bancaire → extraction des transactions → catégorisation → cashflow → économies → coaching"
                      : language === "ar"
                      ? "كشف بنكي → استخراج المعاملات → التصنيف → التدفق النقدي → فرص التوفير → coaching"
                      : "Bank statement → transaction extraction → categorization → cashflow → savings → coaching",
                },
                {
                  title:
                    language === "fr"
                      ? "Study Workspace"
                      : language === "ar"
                      ? "مساحة التعلم"
                      : "Study Workspace",
                  flow:
                    language === "fr"
                      ? "Cours → extraction du contenu → résumé → audio → quiz → flashcards → plan de révision"
                      : language === "ar"
                      ? "درس → استخراج المحتوى → ملخص → صوت → اختبار → بطاقات مراجعة → خطة مراجعة"
                      : "Lesson → content extraction → summary → audio → quiz → flashcards → study plan",
                },
                {
                  title:
                    language === "fr"
                      ? "Business Agent"
                      : language === "ar"
                      ? "وكيل الأعمال"
                      : "Business Agent",
                  flow:
                    language === "fr"
                      ? "CSV/Excel → calcul KPI → détection des risques → prévisions → décision prioritaire → dashboard"
                      : language === "ar"
                      ? "CSV/Excel → حساب KPI → اكتشاف المخاطر → التوقعات → قرار ذو أولوية → لوحة تنفيذية"
                      : "CSV/Excel → KPI calculation → risk detection → forecasting → priority decision → dashboard",
                },
              ].map((item) => (
                <div
                  key={item.title}
                  className="rounded-3xl border border-slate-200 bg-slate-50 p-5"
                >
                  <h3 className="font-semibold text-slate-900">
                    {item.title}
                  </h3>

                  <p className="mt-3 text-sm leading-6 text-slate-600">
                    {item.flow}
                  </p>
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
              {language === "fr"
                ? "Preuves d’usage"
                : language === "ar"
                ? "إشارات استخدام فعلية"
                : "Usage proof"}
            </p>

            <h2 className="mt-3 text-3xl font-bold text-slate-900">
              {language === "fr"
                ? "Des exemples réels avant des promesses marketing."
                : language === "ar"
                ? "أمثلة واقعية قبل الوعود التسويقية."
                : "Real examples before marketing claims."}
            </h2>

            <p className="mt-4 max-w-4xl text-slate-600 leading-7">
              {language === "fr"
                ? "Runexa affiche des exemples de sorties réelles pour chaque agent. Les métriques publiques d’usage, références clients et témoignages seront ajoutés uniquement lorsqu’ils seront vérifiés et publiables."
                : language === "ar"
                ? "تعرض Runexa أمثلة حقيقية لمخرجات كل وكيل. سيتم إضافة مقاييس الاستخدام العامة ومراجع العملاء والشهادات فقط عندما تكون موثقة وقابلة للنشر."
                : "Runexa shows real output examples for each agent. Public usage metrics, customer references, and testimonials will be added only when they are verified and publishable."}
            </p>

            <div className="mt-8 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              {[
                {
                  metric: "25",
                  label:
                    language === "fr"
                      ? "clauses détectées dans un contrat test"
                      : language === "ar"
                      ? "بنداً تم اكتشافها في عقد اختباري"
                      : "clauses detected in a test contract",
                },
                {
                  metric: "€1,548",
                  label:
                    language === "fr"
                      ? "opportunité d’économies détectée"
                      : language === "ar"
                      ? "فرصة توفير مكتشفة"
                      : "savings opportunity detected",
                },
                {
                  metric: "97/100",
                  label:
                    language === "fr"
                      ? "score qualité sur un exemple Study"
                      : language === "ar"
                      ? "درجة جودة في مثال Study"
                      : "quality score on a Study example",
                },
                {
                  metric: "91/100",
                  label:
                    language === "fr"
                      ? "score santé business sur business.csv"
                      : language === "ar"
                      ? "درجة صحة الأعمال على business.csv"
                      : "business health score on business.csv",
                },
              ].map((item) => (
                <div
                  key={item.label}
                  className="rounded-3xl border border-slate-200 bg-slate-50 p-5"
                >
                  <p className="text-3xl font-bold text-slate-900">
                    {item.metric}
                  </p>

                  <p className="mt-3 text-sm leading-6 text-slate-600">
                    {item.label}
                  </p>
                </div>
              ))}
            </div>

            <div className="mt-8 rounded-3xl border border-blue-100 bg-blue-50 p-6">
              <p className="text-sm font-semibold text-blue-700">
                {language === "fr"
                  ? "Statut actuel"
                  : language === "ar"
                  ? "الوضع الحالي"
                  : "Current status"}
              </p>

              <div className="mt-4 grid gap-3 md:grid-cols-2">
                {[
                  language === "fr"
                    ? "Exemples d’analyse disponibles pour Legal, Finance, Study et Business"
                    : language === "ar"
                    ? "أمثلة تحليل متاحة لوكلاء Legal وFinance وStudy وBusiness"
                    : "Analysis examples available for Legal, Finance, Study, and Business",
                  language === "fr"
                    ? "Démos publiques disponibles pour tester les agents"
                    : language === "ar"
                    ? "عروض عامة متاحة لاختبار الوكلاء"
                    : "Public demos available to test agents",
                  language === "fr"
                    ? "Produit dirigé par un fondateur identifiable"
                    : language === "ar"
                    ? "منتج يقوده مؤسس واضح الهوية"
                    : "Founder-led product with identifiable background",
                  language === "fr"
                    ? "Témoignages et références clients à ajouter après validation publique"
                    : language === "ar"
                    ? "سيتم إضافة الشهادات ومراجع العملاء بعد التحقق والموافقة على النشر"
                    : "Testimonials and customer references to be added after public validation",
                ].map((item) => (
                  <div
                    key={item}
                    className="rounded-2xl bg-white p-4 text-sm font-medium text-slate-700"
                  >
                    {item}
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
            <div className="grid gap-8 lg:grid-cols-[0.8fr_1.2fr] lg:items-start">
              <div className="rounded-3xl bg-slate-950 p-8 text-white">
                <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-blue-500/20 text-blue-200">
                  <UserCheck className="h-7 w-7" />
                </div>

                <p className="mt-6 text-sm font-semibold text-blue-200">
                  {language === "fr"
                    ? "Fondateur identifiable"
                    : language === "ar"
                    ? "مؤسس واضح الهوية"
                    : "Identifiable founder"}
                </p>

                <h2 className="mt-3 text-3xl font-bold">
                  {language === "fr"
                    ? "Construit par Dr. Rachid Ejjami"
                    : language === "ar"
                    ? "تم بناء Runexa بواسطة د. رشيد الجامعي"
                    : "Built by Dr. Rachid Ejjami"}
                </h2>

                <p className="mt-4 text-sm leading-6 text-slate-300">
                  {language === "fr"
                    ? "Doctor of Business Administration · École des Ponts Business School · Editor-in-Chief, JNGR 5.0"
                    : language === "ar"
                    ? "دكتوراه في إدارة الأعمال · École des Ponts Business School · رئيس تحرير JNGR 5.0"
                    : "Doctor of Business Administration · École des Ponts Business School · Editor-in-Chief, JNGR 5.0"}
                </p>
              </div>

              <div>
                <p className="text-slate-600 leading-7">
                  {language === "fr"
                    ? "Runexa est développé par Dr. Rachid Ejjami, chercheur et praticien travaillant sur les systèmes d’IA, la gouvernance de l’IA, l’intelligence décisionnelle et les applications réelles de l’IA dans les domaines juridique, financier, éducatif, santé, banque, assurance, supply chain, énergie et business."
                    : language === "ar"
                    ? "تم تطوير Runexa بواسطة د. رشيد الجامعي، باحث وممارس يعمل على أنظمة الذكاء الاصطناعي، وحوكمة الذكاء الاصطناعي، وذكاء القرار، والتطبيقات الواقعية للذكاء الاصطناعي في المجالات القانونية والمالية والتعليمية والصحية والمصرفية والتأمين وسلاسل الإمداد والطاقة وقرارات الأعمال."
                    : "Runexa is developed by Dr. Rachid Ejjami, a researcher and practitioner working on AI systems, AI governance, decision intelligence, and real-world AI applications across legal, finance, education, healthcare, banking, insurance, supply chains, energy, and business decision-making."}
                </p>

                <div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
                  {[
                    language === "fr" ? "42+ publications" : language === "ar" ? "أكثر من 42 منشوراً" : "42+ publications",
                    language === "fr" ? "5 livres IA" : language === "ar" ? "5 كتب في الذكاء الاصطناعي" : "5 AI books",
                    language === "fr" ? "629+ citations" : language === "ar" ? "أكثر من 629 استشهاداً" : "629+ citations",
                    language === "fr" ? "h-index 13" : language === "ar" ? "مؤشر h: 13" : "h-index 13",
                    language === "fr" ? "Recherche IA & gouvernance" : language === "ar" ? "بحث في الذكاء الاصطناعي والحوكمة" : "AI research & governance",
                  ].map((item) => (
                    <div
                      key={item}
                      className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm font-semibold text-slate-700"
                    >
                      {item}
                    </div>
                  ))}
                </div>



                <div className="mt-8">
                  <h3 className="text-lg font-semibold text-slate-900">
                    {language === "fr"
                      ? "Ouvrages IA sélectionnés"
                      : language === "ar"
                      ? "كتب مختارة في الذكاء الاصطناعي"
                      : "Selected AI Books"}
                  </h3>

                  <ul className="mt-4 space-y-2 text-sm leading-6 text-slate-600">
                    <li>• AI in Healthcare: A Hands-On Journey Through Two Groundbreaking Case Studies (2025)</li>
                    <li>• AI-Powered Energy Management: Forecasting Consumption and Detecting Fraud with Machine Learning (2025)</li>
                    <li>• Smart Supply Chain Solutions with AI: From Forecasting to Delivery (2025)</li>
                    <li>• Machine Learning in Banking: Building Predictive Models for Risk and Fraud (2025)</li>
                    <li>• Mastering AI Models in the Insurance Domain (2025)</li>
                  </ul>
                </div>

                <div className="mt-6 grid gap-3 sm:grid-cols-2">
                  <a
                    href="https://www.linkedin.com/in/dr-rachid-ejjami-252307129/"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center justify-center rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm font-semibold text-slate-800 hover:bg-slate-50"
                  >
                    LinkedIn
                  </a>

                  <a
                    href="https://www.researchgate.net/profile/Rachid-Ejjami"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center justify-center rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm font-semibold text-slate-800 hover:bg-slate-50"
                  >
                    ResearchGate
                  </a>
                </div>

                <p className="mt-5 text-sm leading-6 text-slate-500">
                  {language === "fr"
                    ? "Ces éléments sont présentés comme des informations de contexte sur le fondateur, sans constituer une certification de sécurité ou une garantie de performance."
                    : language === "ar"
                    ? "تُعرض هذه العناصر كمعلومات سياقية عن المؤسس، ولا تُعد شهادة أمنية أو ضماناً للأداء."
                    : "These details are provided as founder context and are not a security certification or performance guarantee."}
                </p>
              </div>
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
