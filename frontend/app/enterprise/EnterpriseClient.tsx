"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

const labels: any = {
 en: {
    badge: "Runexa for Business",

    title: "Custom AI Solutions for Modern Organizations",

    subtitle:
      "Runexa helps organizations build custom AI agents, intelligent workflows, and decision-support systems tailored to their operations, teams, and business objectives.",

    requestDemo: "Request a Demo",

    contactSales: "Contact Sales",

    customAgent: "Custom AI Solution",

    benefits: [
      "Reduce repetitive manual work",
      "Improve operational efficiency",
      "Accelerate business decision-making",
      "Scale organizational knowledge and workflows",
    ],

    buildTitle: "AI solutions designed around your business",

    buildDesc:
      "Every organization has unique processes, data structures, compliance requirements, and operational challenges. Runexa works with companies to design and deploy custom AI agents and intelligent workflow systems that integrate directly into existing business operations.",

    customTitle: "Built specifically for your workflows",

    customDesc:
      "Instead of forcing teams to adapt to generic software, Runexa develops AI systems tailored to your documents, internal processes, decision workflows, reporting requirements, and operational objectives.",

    howTitle: "How Runexa works with your organization",

    howSteps: [
      "Assess your requirements and workflows",
      "Design custom AI agents and automation systems",
      "Deploy and integrate into your existing environment",
      "Monitor, optimize, and scale across teams",
    ],

    featuresTitle: "Enterprise Capabilities",

    features: [
      "Custom AI agents",
      "Multi-user workspaces",
      "Role-based permissions",
      "Secure document processing",
      "API integrations",
      "Private deployments",
      "Custom dashboards",
      "Workflow automation",
      "Knowledge management",
      "Priority enterprise support",
    ],

    ctaTitle:
      "Ready to deploy AI across your organization?",

    ctaDesc:
      "Work with Runexa to build custom AI systems that improve productivity, automate workflows, and support better business decisions.",

    ctaButton: "Get Started",

    education: {
      eyebrow: "Runexa for Education",
      title: "AI Solutions for Education and Training",
      description:
        "Deploy secure AI workspaces for schools, universities, training centers and educational organizations with centralized administration, user management and dedicated credits.",
      primaryCardTitle: "Study Workspace Agent",
      primaryCardDesc:
        "Transforms any course document, research paper or training material into a complete learning environment: summary, audio, mind map, quiz, flashcards and personalized revision plan.",
      secondaryCardTitle: "Custom AI Solution",
      secondaryCardDesc:
        "Design education-specific AI workflows for your institution, teams, departments, programs and internal training operations.",
      useCasesTitle: "Education use cases",
      useCases: [
        "Private schools deploying AI for teachers and students",
        "Vocational training centers in any field",
        "Universities and higher education institutions",
        "Corporate training teams and onboarding programs",
        "Organizations offering professional certifications",
      ],
      whyTitle: "Why Runexa for Education",
      whyItems: [
        "Each institution has its own secure administration space",
        "User management, roles and permissions",
        "Bulk credit purchase for the entire organization",
        "Complete data isolation between workspaces",
        "No client content used to train public AI models",
        "Files deleted after analysis",
        "Available in English, French and Arabic",
      ],
    },

    categories: [
      {
        title: "Legal AI Solutions",

        description:
          "Support legal, compliance, contract, and risk-management teams with AI-powered document intelligence and workflow automation.",

        agents: [
          {
            name: "Legal AI Agent",
            desc: "Analyze legal documents, identify risks, summarize obligations, and support legal review workflows.",
          },
          {
            name: "Contract Review Agent",
            desc: "Review contracts, identify key clauses, highlight negotiation points, and generate structured legal summaries.",
          },
          {
            name: "Compliance Agent",
            desc: "Evaluate documents, policies, and procedures against compliance requirements and internal standards.",
          },
          {
            name: "Risk Detection Agent",
            desc: "Identify legal, operational, and contractual risks before they impact the organization.",
          },
        ],
      },

      {
        title: "Finance AI Solutions",

        description:
          "Automate financial analysis, reporting, forecasting, cashflow visibility, and executive decision support.",

        agents: [
          {
            name: "Finance AI Agent",
            desc: "Analyze financial documents and generate structured business insights and recommendations.",
          },
          {
            name: "Expense Optimization Agent",
            desc: "Identify unnecessary spending, recurring costs, and cost-reduction opportunities.",
          },
          {
            name: "Cashflow Forecast Agent",
            desc: "Forecast future cashflow scenarios and identify liquidity risks.",
          },
          {
            name: "Financial Reporting Agent",
            desc: "Generate executive financial reports, KPI dashboards, and performance summaries.",
          },
        ],
      },

      {
        title: "HR & Talent AI Solutions",

        description:
          "Improve recruitment, candidate screening, talent evaluation, and workforce management workflows.",

        agents: [
          {
            name: "HR AI Agent",
            desc: "Support recruitment, onboarding, employee management, and HR operations.",
          },
          {
            name: "CV Screening Agent",
            desc: "Analyze resumes and rank candidates against role requirements.",
          },
          {
            name: "Interview Assistant Agent",
            desc: "Generate interview questions and summarize candidate evaluations.",
          },
          {
            name: "Employee Performance Agent",
            desc: "Support performance reviews, development planning, and workforce insights.",
          },
        ],
      },

      {
        title: "Business Intelligence Solutions",

        description:
          "Transform business data into operational insights, KPI monitoring, risk detection, and strategic recommendations.",

        agents: [
          {
            name: "Business Decision Agent",
            desc: "Analyze business performance and support strategic planning and decision-making.",
          },
          {
            name: "Market Analysis Agent",
            desc: "Analyze competitive environments, market trends, and growth opportunities.",
          },
          {
            name: "KPI Monitoring Agent",
            desc: "Track performance metrics and identify meaningful business changes.",
          },
          {
            name: "Strategy Recommendation Agent",
            desc: "Generate actionable recommendations aligned with business objectives.",
          },
        ],
      },

      {
        title: "Document Intelligence Solutions",

        description:
          "Automate document analysis, extraction, classification, and information processing workflows.",

        agents: [
          {
            name: "Document Analysis Agent",
            desc: "Extract structured information from contracts, reports, policies, and operational documents.",
          },
          {
            name: "Invoice Processing Agent",
            desc: "Process invoices, extract financial information, detect anomalies, and support accounting operations.",
          },
        ],
      },

      {
        title: "Sales & Marketing Intelligence",

        description:
          "Help commercial teams understand customers, improve campaigns, and identify growth opportunities.",

        agents: [
          {
            name: "Sales Insights Agent",
            desc: "Analyze sales pipelines, opportunities, conversion trends, and revenue performance.",
          },
          {
            name: "Customer Behavior Agent",
            desc: "Understand customer behavior, engagement patterns, and retention opportunities.",
          },
        ],
      },
    ],
  },
  fr: {
    heroTitle: "Runexa pour les entreprises",

    heroSubtitle:
      "Des solutions d’intelligence artificielle sur mesure conçues pour votre organisation.",

    heroDesc:
      "Nous concevons des agents IA personnalisés, des workflows intelligents et des systèmes d’aide à la décision adaptés à vos processus métier, vos données et vos objectifs opérationnels — afin d’aider vos équipes à travailler plus efficacement, réduire les risques et prendre de meilleures décisions.",

    requestDemo: "Demander une démonstration",

    contactSales: "Contacter l’équipe commerciale",

    customAgent: "Solution IA sur mesure",

    benefits: [
      "Réduire les tâches manuelles répétitives",
      "Améliorer la qualité des décisions",
      "Accélérer l’efficacité opérationnelle",
      "Centraliser la connaissance et l’analyse entre les équipes",
    ],

    buildTitle: "Ce que nous construisons pour les organisations",

    buildDesc:
      "Runexa Systems conçoit des agents IA personnalisés, des workflows intelligents et des systèmes d’automatisation pour les équipes juridiques, financières, RH, business, documentaires, commerciales et marketing.",

    customTitle:
      "Des systèmes IA conçus autour de votre activité",

    customDesc:
      "Chaque organisation possède ses propres processus, données, contraintes réglementaires et objectifs métier. C’est pourquoi nous développons des solutions IA adaptées à vos documents, workflows internes, exigences opérationnelles et priorités stratégiques.",

    howTitle: "Comment nous accompagnons votre organisation",

    howSteps: [
      "Analyser vos besoins et vos workflows",
      "Concevoir votre solution IA",
      "Déployer et intégrer dans votre environnement",
      "Développer l’IA à l’échelle de l’organisation",
    ],

    featuresTitle: "Capacités Enterprise",

    features: [
      "Accès multi-utilisateurs",
      "Gestion des équipes",
      "Gestion des rôles et permissions",
      "Traitement sécurisé des données",
      "Tableaux de bord personnalisés",
      "Accès API",
      "Automatisation des workflows",
      "Déploiements privés",
      "Support prioritaire",
    ],

    ctaTitle:
      "Prêt à déployer l’IA dans votre organisation ?",

    ctaDesc:
      "Construisons ensemble une solution adaptée à vos opérations, vos équipes et vos objectifs.",

    ctaButton: "Commencer",

    education: {
      eyebrow: "Runexa pour l’Éducation",
      title: "Solutions IA pour l’Éducation et la Formation",
      description:
        "Déployez des espaces IA sécurisés pour les écoles, universités, centres de formation et organisations éducatives avec administration centralisée, gestion des utilisateurs et crédits dédiés.",
      primaryCardTitle: "Study Workspace Agent",
      primaryCardDesc:
        "Transforme tout document de cours, article de recherche ou support pédagogique en environnement d’apprentissage complet : résumé, audio, carte mentale, quiz, flashcards et plan de révision personnalisé.",
      secondaryCardTitle: "Solution IA sur mesure",
      secondaryCardDesc:
        "Concevez des workflows IA adaptés à votre établissement, vos équipes, vos départements, vos programmes et vos opérations de formation internes.",
      useCasesTitle: "Cas d’usage éducatifs",
      useCases: [
        "Écoles privées déployant l’IA pour leurs enseignants et élèves",
        "Centres de formation professionnelle dans tous les domaines",
        "Universités et établissements d’enseignement supérieur",
        "Équipes de formation en entreprise et onboarding",
        "Organisations proposant des certifications professionnelles",
      ],
      whyTitle: "Pourquoi Runexa pour l’Éducation",
      whyItems: [
        "Chaque établissement dispose de son propre espace d’administration sécurisé",
        "Gestion des utilisateurs, rôles et permissions",
        "Achat de crédits en volume pour toute l’organisation",
        "Isolation complète des données entre espaces",
        "Aucun contenu client utilisé pour entraîner des modèles IA publics",
        "Fichiers supprimés après analyse",
        "Disponible en français, anglais et arabe",
      ],
    },

    categories: [
      {
        title: "Solutions IA juridiques",

        description:
          "Accompagnez vos équipes juridiques, conformité et gestion des risques grâce à l’intelligence documentaire alimentée par l’IA.",

        agents: [
          {
            name: "Legal AI Agent",
            desc: "Analyse les contrats internes, détecte les risques et aide à garantir la conformité.",
          },
          {
            name: "Contract Review Agent",
            desc: "Examine les accords, met en évidence les clauses clés et identifie les points de négociation.",
          },
          {
            name: "Compliance Agent",
            desc: "Vérifie les documents et les processus selon vos règles internes et exigences de conformité.",
          },
          {
            name: "Risk Detection Agent",
            desc: "Détecte les risques opérationnels, juridiques et contractuels avant qu’ils ne deviennent coûteux.",
          },
        ],
      },

      {
        title: "Solutions IA financières",

        description:
          "Automatisez le reporting financier, l’analyse des dépenses, les prévisions et l’aide à la décision.",

        agents: [
          {
            name: "Finance AI Agent",
            desc: "Automatise l’analyse financière et génère des rapports internes.",
          },
          {
            name: "Expense Optimization Agent",
            desc: "Détecte les dépenses inutiles et propose des opportunités de réduction des coûts.",
          },
          {
            name: "Cashflow Forecast Agent",
            desc: "Prévoit les tendances de trésorerie et identifie les futurs risques de liquidité.",
          },
          {
            name: "Financial Reporting Agent",
            desc: "Génère des synthèses, tableaux de bord et insights financiers à partir des données business.",
          },
        ],
      },

      {
        title: "Solutions IA RH et Talents",

        description:
          "Améliorez vos processus de recrutement, de présélection, d’évaluation et de gestion des collaborateurs.",

        agents: [
          {
            name: "HR AI Agent",
            desc: "Analyse les CV et simplifie le processus de recrutement.",
          },
          {
            name: "CV Screening Agent",
            desc: "Classe les candidats selon les exigences du poste, les compétences et l’expérience.",
          },
          {
            name: "Interview Assistant Agent",
            desc: "Génère des questions d’entretien et résume les évaluations des candidats.",
          },
          {
            name: "Employee Performance Agent",
            desc: "Analyse les retours collaborateurs, les notes de performance et les plans de développement.",
          },
        ],
      },

      {
        title: "Solutions Business Intelligence",

        description:
          "Aidez les équipes dirigeantes à analyser les données, suivre les KPI et prendre de meilleures décisions stratégiques.",

        agents: [
          {
            name: "Business Decision Agent",
            desc: "Analyse les données business et soutient les décisions stratégiques.",
          },
          {
            name: "Market Analysis Agent",
            desc: "Analyse les signaux du marché, les concurrents et les opportunités.",
          },
          {
            name: "KPI Monitoring Agent",
            desc: "Suit les KPI business et met en évidence les changements de performance.",
          },
          {
            name: "Strategy Recommendation Agent",
            desc: "Génère des recommandations stratégiques à partir des données et objectifs business.",
          },
        ],
      },

      {
        title: "Solutions d’intelligence documentaire",

        description:
          "Traitez plus rapidement les documents, factures, rapports et fichiers opérationnels.",

        agents: [
          {
            name: "Document Analysis Agent",
            desc: "Extrait les informations clés des documents et résume les points importants.",
          },
          {
            name: "Invoice Processing Agent",
            desc: "Lit les factures, extrait les montants, détecte les anomalies et soutient les workflows comptables.",
          },
        ],
      },

      {
        title: "Solutions IA commerciales et marketing",

        description:
          "Aidez les équipes de croissance grâce à l’intelligence client, commerciale et marketing.",

        agents: [
          {
            name: "Sales Insights Agent",
            desc: "Analyse les données de vente, détecte les opportunités et soutient les décisions pipeline.",
          },
          {
            name: "Customer Behavior Agent",
            desc: "Comprend les comportements clients et identifie les opportunités de croissance.",
          },
        ],
      },
    ],
  },
  ar: {
   heroTitle: "Runexa للشركات",

    heroSubtitle:
      "حلول ذكاء اصطناعي مخصصة مصممة لمؤسستك.",

    heroDesc:
      "نصمم وكلاء ذكاء اصطناعي مخصصين، وسير عمل ذكي، وأنظمة دعم لاتخاذ القرار تتكيف مع عملياتك وبياناتك وأهدافك التشغيلية — لمساعدة فرقك على العمل بكفاءة أعلى، وتقليل المخاطر، واتخاذ قرارات أفضل.",

    requestDemo: "طلب عرض توضيحي",

    contactSales: "التواصل مع فريق المبيعات",

    customAgent: "حل ذكاء اصطناعي مخصص",

    benefits: [
      "تقليل المهام اليدوية المتكررة",
      "تحسين جودة القرارات",
      "تعزيز الكفاءة التشغيلية",
      "توحيد المعرفة والتحليل بين الفرق",
    ],

    buildTitle: "ما الذي نقدمه للمؤسسات",

    buildDesc:
      "تطوّر Runexa Systems حلول ذكاء اصطناعي مؤسسية مخصصة، وسير عمل ذكي، وأنظمة أتمتة تدعم العمليات الحيوية عبر مختلف الإدارات والفرق داخل المؤسسة.",

    customTitle: "حلول ذكاء اصطناعي مصممة وفق احتياجات مؤسستك",
    customDesc:
      "تختلف كل مؤسسة في عملياتها وبياناتها ومتطلباتها التنظيمية وأهدافها الاستراتيجية. لذلك نطوّر حلول ذكاء اصطناعي مخصصة تتوافق مع بيئتك التشغيلية وتتكامل مع أنظمتك الحالية لدعم النمو وتحسين الأداء.",

    howTitle: "منهجية العمل",

    howSteps: [
      "تحليل الاحتياجات والعمليات",
      "تصميم الحل وتخصيصه",
      "التنفيذ والتكامل",
      "التوسع والتحسين المستمر",
    ],

    features: [
      "وصول متعدد المستخدمين",
      "إدارة الفرق",
      "إدارة الأدوار والصلاحيات",
      "معالجة آمنة للبيانات",
      "لوحات تحكم مخصصة",
      "تكامل عبر واجهات API",
      "إدارة سير العمل بذكاء",
      "بيئات نشر خاصة",
      "دعم ذو أولوية",
    ],

    ctaTitle:
      "هل أنتم مستعدون للارتقاء بعمليات مؤسستكم باستخدام الذكاء الاصطناعي؟",

    ctaDesc:
      "دعونا نصمم معًا حلاً مخصصًا يتوافق مع احتياجاتكم التشغيلية وأهدافكم الاستراتيجية.",

    ctaButton: "ابدأوا اليوم",

    education: {
      eyebrow: "Runexa للتعليم",
      title: "حلول الذكاء الاصطناعي للتعليم والتدريب",
      description:
        "انشر مساحات ذكاء اصطناعي آمنة للمدارس والجامعات ومراكز التدريب والمؤسسات التعليمية مع إدارة مركزية، وإدارة للمستخدمين، وأرصدة مخصصة.",
      primaryCardTitle: "وكيل مساحة الدراسة",
      primaryCardDesc:
        "يحوّل أي مستند دراسي أو ورقة بحثية أو مادة تدريبية إلى بيئة تعلم متكاملة: ملخص، صوت، خريطة ذهنية، اختبار، بطاقات مراجعة وخطة مراجعة مخصصة.",
      secondaryCardTitle: "حل ذكاء اصطناعي مخصص",
      secondaryCardDesc:
        "صمّم سير عمل ذكية مخصصة لمؤسستك التعليمية وفرقك وأقسامك وبرامجك وعمليات التدريب الداخلية.",
      useCasesTitle: "حالات الاستخدام التعليمية",
      useCases: [
        "المدارس الخاصة التي تنشر الذكاء الاصطناعي للمعلمين والطلاب",
        "مراكز التكوين المهني في جميع المجالات",
        "الجامعات ومؤسسات التعليم العالي",
        "فرق التدريب في المؤسسات وبرامج الإدماج",
        "المنظمات التي تقدم شهادات مهنية",
      ],
      whyTitle: "لماذا Runexa للتعليم",
      whyItems: [
        "لكل مؤسسة فضاء إداري آمن خاص بها",
        "إدارة المستخدمين والأدوار والصلاحيات",
        "شراء الأرصدة بالجملة للمؤسسة بأكملها",
        "عزل كامل للبيانات بين الفضاءات",
        "لا يُستخدم أي محتوى للعملاء لتدريب نماذج الذكاء الاصطناعي العامة",
        "حذف الملفات بعد التحليل",
        "متاح بالإنجليزية والفرنسية والعربية",
      ],
    },

    categories: [
      {
        title: "حلول الذكاء الاصطناعي القانونية",

        description:
          "تمكين الفرق القانونية وفرق الامتثال وإدارة المخاطر من الاستفادة من تحليل الوثائق المدعوم بالذكاء الاصطناعي.",

        agents: [
          {
            name: "المستشار القانوني الذكي",
            desc: "يحلل العقود الداخلية، ويكشف المخاطر المحتملة، ويساعد على تعزيز الامتثال.",
          },
          {
            name: "مراجع العقود الذكي",
            desc: "يراجع الاتفاقيات، ويبرز البنود الرئيسية، ويحدد نقاط التفاوض المهمة.",
          },
          {
            name: "مساعد الامتثال",
            desc: "يفحص الوثائق والعمليات وفق السياسات الداخلية والمتطلبات التنظيمية.",
          },
          {
            name: "مكتشف المخاطر",
            desc: "يرصد المخاطر التشغيلية والقانونية والتعاقدية قبل أن تتحول إلى تحديات مكلفة.",
          },
        ],
      },
      {
        title: "حلول الذكاء الاصطناعي المالية",

        description:
          "تعزيز الأداء المالي من خلال التحليل الذكي للبيانات المالية، وتحسين إدارة المصروفات، ودعم اتخاذ القرار.",

        agents: [
          {
            name: "المحلل المالي الذكي",
            desc: "يحلل البيانات المالية ويُنشئ تقارير ورؤى تدعم اتخاذ القرار.",
          },
          {
            name: "مُحسِّن المصروفات",
            desc: "يرصد فرص خفض التكاليف ويكشف أوجه الإنفاق غير الضرورية.",
          },
          {
            name: "مساعد التنبؤ بالتدفقات النقدية",
            desc: "يتوقع اتجاهات التدفقات النقدية ويساعد على استباق مخاطر السيولة.",
          },
          {
            name: "مساعد التقارير المالية",
            desc: "يُعد ملخصات ولوحات معلومات ورؤى مالية انطلاقًا من بيانات المؤسسة.",
          },
        ],
      },
      {
        title: "حلول الذكاء الاصطناعي للموارد البشرية والمواهب",

        description:
          "تعزيز كفاءة التوظيف وإدارة المواهب وتطوير الموظفين من خلال حلول ذكاء اصطناعي مصممة للموارد البشرية.",

        agents: [
          {
            name: "مساعد الموارد البشرية الذكي",
            desc: "يدعم فرق الموارد البشرية في إدارة عمليات التوظيف وتقييم المرشحين.",
          },
          {
            name: "مساعد فرز السير الذاتية",
            desc: "يقيّم المرشحين وفق متطلبات الوظيفة والمهارات والخبرات المطلوبة.",
          },
          {
            name: "مساعد المقابلات",
            desc: "يقترح أسئلة المقابلات ويلخص نتائج تقييم المرشحين.",
          },
          {
            name: "مساعد أداء الموظفين",
            desc: "يحلل مؤشرات الأداء وملاحظات الموظفين ويدعم خطط التطوير المهني.",
          },
        ],
      },
      {
        title: "حلول ذكاء الأعمال ودعم القرار",

        description:
          "تمكين فرق القيادة من الاستفادة من البيانات ومؤشرات الأداء لاتخاذ قرارات أكثر دقة وفعالية.",

        agents: [
          {
            name: "مساعد اتخاذ القرار",
            desc: "يحلل بيانات المؤسسة ويوفر رؤى تدعم القرارات الاستراتيجية.",
          },
          {
            name: "مساعد تحليل السوق",
            desc: "يراقب اتجاهات السوق والمنافسين ويساعد على اكتشاف الفرص الجديدة.",
          },
          {
            name: "مساعد مؤشرات الأداء",
            desc: "يتابع مؤشرات الأداء الرئيسية ويبرز التغيرات والاتجاهات المهمة.",
          },
          {
            name: "مساعد التوصيات الاستراتيجية",
            desc: "يقدم توصيات مبنية على البيانات لدعم التخطيط وتحقيق الأهداف المؤسسية.",
          },
        ],
      },
      {
        title: "حلول الذكاء الوثائقي",

        description:
          "تسريع معالجة الوثائق والفواتير والتقارير والملفات التشغيلية واستخراج المعلومات المهمة منها بكفاءة أعلى.",

        agents: [
          {
            name: "مساعد تحليل الوثائق",
            desc: "يستخرج المعلومات الرئيسية من الوثائق ويقدم ملخصات دقيقة للنقاط المهمة.",
          },
          {
            name: "مساعد معالجة الفواتير",
            desc: "يعالج الفواتير تلقائيًا، ويستخرج البيانات الأساسية، ويدعم العمليات المالية والمحاسبية.",
          },
        ],
      },
      {
        title: "حلول الذكاء الاصطناعي للمبيعات والتسويق",

        description:
          "تمكين فرق المبيعات والتسويق من الاستفادة من البيانات ورؤى العملاء لتعزيز النمو وتحسين الأداء التجاري.",

        agents: [
          {
            name: "مساعد رؤى المبيعات",
            desc: "يحلل بيانات المبيعات ويكشف الفرص التجارية ويدعم إدارة مسار المبيعات.",
          },
          {
            name: "مساعد تحليل سلوك العملاء",
            desc: "يحلل تفضيلات العملاء وسلوكهم ويساعد على اكتشاف فرص النمو وتعزيز التفاعل.",
          },
        ],
      },
    ],
  },
};

export default function EnterpriseClient() {
  const [language, setLanguage] =
    useState<"en" | "fr" | "ar">("en");
  const t = labels[language] || labels.en;
  const education = t.education || labels.en.education;

  useEffect(() => {
    const saved = localStorage.getItem("locale");

    if (saved === "fr" || saved === "ar" || saved === "en") {
      setLanguage(saved);
    }

    const handleLocaleChange = () => {
      const nextLocale = localStorage.getItem("locale");

      if (
        nextLocale === "fr" ||
        nextLocale === "ar" ||
        nextLocale === "en"
      ) {
        setLanguage(nextLocale);
      }
    };

    window.addEventListener("locale-change", handleLocaleChange);

    return () => {
      window.removeEventListener("locale-change", handleLocaleChange);
    };
  }, []);

  return (
    <main
      dir={language === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 text-slate-900 px-6 py-16"
    >
      {/* HERO */}
      <section className="max-w-5xl mx-auto text-center space-y-6">
        <h1 className="text-4xl font-bold">{t.heroTitle}</h1>

        <p className="text-lg text-slate-600">{t.heroSubtitle}</p>

        <p className="text-slate-600 max-w-2xl mx-auto">{t.heroDesc}</p>

        <div className="flex justify-center gap-4 pt-4">
          <Link
            href="/contact-entreprise/contact"
            className="px-6 py-3 bg-blue-600 text-white rounded-xl font-semibold"
          >
            {t.requestDemo}
          </Link>

          <Link
            href="/contact-entreprise/contact"
            className="px-6 py-3 border rounded-xl font-semibold"
          >
            {t.contactSales}
          </Link>
        </div>
      </section>

      {/* BENEFITS */}
      <section className="max-w-5xl mx-auto mt-20 grid md:grid-cols-2 gap-6 text-sm text-slate-600">
        {t.benefits.map((benefit: string) => (
          <div key={benefit}>✔ {benefit}</div>
        ))}
      </section>

      {/* AGENTS */}
      <section className="max-w-6xl mx-auto mt-20">
        <h2 className="text-2xl font-bold text-center mb-4">
          {t.buildTitle}
        </h2>

        <p className="text-center text-slate-600 max-w-3xl mx-auto mb-10">
          {t.buildDesc}
        </p>

        <div className="space-y-10">
          {t.categories.map((category: any) => (
            <div
              key={category.title}
              className="bg-white rounded-3xl border p-6 shadow-sm"
            >
              <div className="mb-6">
                <h3 className="text-xl font-semibold text-slate-900">
                  {category.title}
                </h3>

                <p className="text-sm text-slate-600 mt-2">
                  {category.description}
                </p>
              </div>

              <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                {category.agents.map((agent: any) => (
                  <div
                    key={agent.name}
                    className="rounded-2xl border bg-slate-50 p-5"
                  >
                    <h4 className="font-semibold text-slate-900">
                      {agent.name}
                    </h4>

                    <p className="text-sm text-slate-600 mt-3">
                      {agent.desc}
                    </p>

                    <span className="inline-block mt-4 rounded-full bg-blue-50 px-3 py-1 text-xs font-medium text-blue-700 border border-blue-100">
                      {t.customAgent}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* EDUCATION */}
      <section className="max-w-6xl mx-auto mt-20 overflow-hidden rounded-[2rem] border border-blue-100 bg-white shadow-sm">
        <div className="grid lg:grid-cols-[0.95fr_1.05fr]">
          <div className="bg-gradient-to-br from-blue-700 via-indigo-700 to-slate-950 p-8 text-white md:p-10">
            <span className="inline-flex rounded-full border border-white/20 bg-white/10 px-4 py-1.5 text-xs font-semibold uppercase tracking-[0.2em] text-blue-100">
              {education.eyebrow}
            </span>

            <h2 className="mt-6 text-3xl font-bold leading-tight md:text-4xl">
              {education.title}
            </h2>

            <p className="mt-5 text-sm leading-7 text-blue-100 md:text-base">
              {education.description}
            </p>

            <div className="mt-8 grid gap-4">
              <div className="rounded-3xl border border-white/15 bg-white/10 p-5 backdrop-blur">
                <div className="mb-3 flex h-11 w-11 items-center justify-center rounded-2xl bg-white text-xl text-blue-700 shadow-sm">
                  ◉
                </div>
                <h3 className="text-lg font-semibold">
                  {education.primaryCardTitle}
                </h3>
                <p className="mt-3 text-sm leading-6 text-blue-100">
                  {education.primaryCardDesc}
                </p>
              </div>

              <div className="rounded-3xl border border-white/15 bg-white/10 p-5 backdrop-blur">
                <div className="mb-3 flex h-11 w-11 items-center justify-center rounded-2xl bg-white text-xl text-blue-700 shadow-sm">
                  ✦
                </div>
                <h3 className="text-lg font-semibold">
                  {education.secondaryCardTitle}
                </h3>
                <p className="mt-3 text-sm leading-6 text-blue-100">
                  {education.secondaryCardDesc}
                </p>
              </div>
            </div>
          </div>

          <div className="p-8 md:p-10">
            <div className="grid gap-8 lg:grid-cols-2">
              <div>
                <h3 className="text-lg font-bold text-slate-900">
                  {education.useCasesTitle}
                </h3>
                <div className="mt-5 space-y-3">
                  {education.useCases.map((item: string) => (
                    <div
                      key={item}
                      className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm leading-6 text-slate-700"
                    >
                      <span className="font-semibold text-blue-700">✔</span> {item}
                    </div>
                  ))}
                </div>
              </div>

              <div>
                <h3 className="text-lg font-bold text-slate-900">
                  {education.whyTitle}
                </h3>
                <div className="mt-5 flex flex-wrap gap-3">
                  {education.whyItems.map((item: string) => (
                    <span
                      key={item}
                      className="rounded-full border border-blue-100 bg-blue-50 px-4 py-2 text-sm leading-6 text-blue-800"
                    >
                      ✔ {item}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CUSTOM */}
      <section className="max-w-5xl mx-auto mt-20 text-center space-y-4">
        <h2 className="text-2xl font-bold">{t.customTitle}</h2>

        <p className="text-slate-600">{t.customDesc}</p>
      </section>

      {/* HOW IT WORKS */}
      <section className="max-w-5xl mx-auto mt-20">
        <h2 className="text-2xl font-bold text-center mb-10">
          {t.howTitle}
        </h2>

        <div className="grid md:grid-cols-4 gap-6 text-sm text-slate-600 text-center">
          {t.howSteps.map((step: string) => (
            <div key={step} className="bg-white rounded-2xl border p-5">
              {step}
            </div>
          ))}
        </div>
      </section>

      {/* FEATURES */}
      <section className="max-w-5xl mx-auto mt-20">
        <h2 className="text-2xl font-bold text-center mb-10">
          {t.featuresTitle}
        </h2>

        <div className="grid md:grid-cols-2 gap-4 text-sm text-slate-600">
          {t.features.map((feature: string) => (
            <div key={feature}>✔ {feature}</div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="max-w-4xl mx-auto mt-20 bg-blue-600 text-white rounded-3xl p-10 text-center">
        <h2 className="text-2xl font-bold">{t.ctaTitle}</h2>

        <p className="mt-3 text-blue-100">{t.ctaDesc}</p>

        <Link
          href="/contact-entreprise/contact"
          className="inline-block mt-6 px-6 py-3 bg-white text-blue-600 rounded-xl font-semibold"
        >
          {t.ctaButton}
        </Link>
      </section>

    </main>
  );
}
