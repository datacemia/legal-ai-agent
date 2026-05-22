"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

const labels: any = {
  en: {
    heroTitle: "Runexa for Business",
    heroSubtitle: "Custom AI agents built for your company.",
    heroDesc:
      "We design AI agents tailored to your workflows, data, and business needs — helping your teams analyze faster, reduce risks, and make better decisions.",
    requestDemo: "Request a demo",
    contactSales: "Contact sales",
    customAgent: "Custom agent",

    benefits: [
      "Reduce manual work",
      "Improve decision quality",
      "Scale operations with AI",
      "Centralize analysis across teams",
    ],

    buildTitle: "What we build for your business",
    buildDesc:
      "Runexa Systems builds custom AI agents for legal, finance, HR, business, document processing, sales, and marketing workflows.",

    customTitle: "We build AI agents tailored to your business",
    customDesc:
      "Each company is different. That’s why we create custom AI agents adapted to your data, workflows, and internal processes.",

    howTitle: "How it works",
    howSteps: [
      "Understand your needs",
      "Build your agents",
      "Deploy & integrate",
      "Scale with AI",
    ],

    featuresTitle: "Enterprise features",
    features: [
      "Multi-user access",
      "Team management",
      "Secure data processing",
      "Custom dashboards",
      "API access",
      "Priority support",
    ],

    ctaTitle: "Ready to bring AI into your business?",
    ctaDesc: "Let’s build your custom AI agents.",
    ctaButton: "Get started",

    categories: [
      {
        title: "Legal AI Agents",
        description:
          "Support legal, compliance, and risk teams with AI-powered document analysis.",
        agents: [
          {
            name: "Legal AI Agent",
            desc: "Analyze internal contracts, detect risks, and ensure compliance.",
          },
          {
            name: "Contract Review Agent",
            desc: "Review agreements, highlight key clauses, and identify negotiation points.",
          },
          {
            name: "Compliance Agent",
            desc: "Check documents and processes against internal rules and compliance requirements.",
          },
          {
            name: "Risk Detection Agent",
            desc: "Detect operational, legal, and contractual risks before they become costly.",
          },
        ],
      },
      {
        title: "Finance AI Agents",
        description:
          "Automate financial reporting, expense analysis, and decision support.",
        agents: [
          {
            name: "Finance AI Agent",
            desc: "Automate financial analysis and generate internal reports.",
          },
          {
            name: "Expense Optimization Agent",
            desc: "Detect unnecessary spending and suggest cost-saving opportunities.",
          },
          {
            name: "Cashflow Forecast Agent",
            desc: "Forecast cashflow trends and identify future liquidity risks.",
          },
          {
            name: "Financial Reporting Agent",
            desc: "Generate summaries, dashboards, and financial insights from business data.",
          },
        ],
      },
      {
        title: "HR AI Agents",
        description:
          "Improve hiring, screening, and employee management workflows.",
        agents: [
          {
            name: "HR AI Agent",
            desc: "Screen CVs and streamline recruitment.",
          },
          {
            name: "CV Screening Agent",
            desc: "Rank candidates based on role requirements, skills, and experience.",
          },
          {
            name: "Interview Assistant Agent",
            desc: "Generate interview questions and summarize candidate evaluations.",
          },
          {
            name: "Employee Performance Agent",
            desc: "Analyze employee feedback, performance notes, and development plans.",
          },
        ],
      },
      {
        title: "Business AI Agents",
        description:
          "Help leadership teams analyze data, monitor KPIs, and make better decisions.",
        agents: [
          {
            name: "Business Decision Agent",
            desc: "Analyze business data and support strategic decisions.",
          },
          {
            name: "Market Analysis Agent",
            desc: "Analyze market signals, competitors, and opportunities.",
          },
          {
            name: "KPI Monitoring Agent",
            desc: "Track business KPIs and highlight performance changes.",
          },
          {
            name: "Strategy Recommendation Agent",
            desc: "Generate strategic recommendations based on business data and goals.",
          },
        ],
      },
      {
        title: "Document AI Agents",
        description:
          "Process documents, invoices, reports, and operational files faster.",
        agents: [
          {
            name: "Document Analysis Agent",
            desc: "Extract key information from documents and summarize important points.",
          },
          {
            name: "Invoice Processing Agent",
            desc: "Read invoices, extract totals, detect anomalies, and support accounting workflows.",
          },
        ],
      },
      {
        title: "Sales & Marketing AI Agents",
        description:
          "Support growth teams with customer, sales, and campaign intelligence.",
        agents: [
          {
            name: "Sales Insights Agent",
            desc: "Analyze sales data, detect opportunities, and support pipeline decisions.",
          },
          {
            name: "Customer Behavior Agent",
            desc: "Understand customer patterns and identify growth opportunities.",
          },
        ],
      },
    ],
  },

  fr: {
    heroTitle: "Runexa for Business",
    heroSubtitle: "Des agents IA personnalisés conçus pour votre entreprise.",
    heroDesc:
      "Nous concevons des agents IA adaptés à vos flux de travail, vos données et vos besoins métiers — pour aider vos équipes à analyser plus vite, réduire les risques et prendre de meilleures décisions.",
    requestDemo: "Demander une démo",
    contactSales: "Contacter l’équipe commerciale",
    customAgent: "Agent personnalisé",

    benefits: [
      "Réduire le travail manuel",
      "Améliorer la qualité des décisions",
      "Déployer l’IA à grande échelle",
      "Centraliser l’analyse entre les équipes",
    ],

    buildTitle: "Ce que nous construisons pour votre entreprise",
    buildDesc:
      "Runexa Systems conçoit des agents IA personnalisés pour les workflows juridiques, financiers, RH, business, documentaires, commerciaux et marketing.",

    customTitle: "Nous créons des agents IA adaptés à votre entreprise",
    customDesc:
      "Chaque entreprise est différente. C’est pourquoi nous créons des agents IA personnalisés, adaptés à vos données, vos flux de travail et vos processus internes.",

    howTitle: "Comment ça fonctionne",
    howSteps: [
      "Comprendre vos besoins",
      "Construire vos agents",
      "Déployer et intégrer",
      "Passer à l’échelle avec l’IA",
    ],

    featuresTitle: "Fonctionnalités Enterprise",
    features: [
      "Accès multi-utilisateurs",
      "Gestion des équipes",
      "Traitement sécurisé des données",
      "Tableaux de bord personnalisés",
      "Accès API",
      "Support prioritaire",
    ],

    ctaTitle: "Prêt à intégrer l’IA dans votre entreprise ?",
    ctaDesc: "Construisons vos agents IA personnalisés.",
    ctaButton: "Commencer",

    categories: [
      {
        title: "Legal AI Agents",
        description:
          "Accompagnez vos équipes juridiques, conformité et risque avec l’analyse documentaire assistée par IA.",
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
        title: "Finance AI Agents",
        description:
          "Automatisez le reporting financier, l’analyse des dépenses et l’aide à la décision.",
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
            desc: "Prévoit les tendances de cashflow et identifie les futurs risques de liquidité.",
          },
          {
            name: "Financial Reporting Agent",
            desc: "Génère des synthèses, tableaux de bord et insights financiers à partir des données business.",
          },
        ],
      },
      {
        title: "HR AI Agents",
        description:
          "Améliorez vos processus de recrutement, de présélection et de gestion des collaborateurs.",
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
        title: "Business AI Agents",
        description:
          "Aidez les équipes dirigeantes à analyser les données, suivre les KPIs et prendre de meilleures décisions.",
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
            desc: "Suit les KPIs business et met en évidence les changements de performance.",
          },
          {
            name: "Strategy Recommendation Agent",
            desc: "Génère des recommandations stratégiques à partir des données et objectifs business.",
          },
        ],
      },
      {
        title: "Document AI Agents",
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
        title: "Sales & Marketing AI Agents",
        description:
          "Aidez les équipes de croissance avec l’intelligence client, commerciale et campagne.",
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
    heroTitle: "Runexa for Business",
    heroSubtitle: "وكلاء ذكاء اصطناعي مخصصون مصممون لشركتك.",
    heroDesc:
      "نصمم وكلاء ذكاء اصطناعي مخصصين حسب سير العمل والبيانات واحتياجات شركتك — لمساعدة فرقك على التحليل بسرعة أكبر، تقليل المخاطر، واتخاذ قرارات أفضل.",
    requestDemo: "طلب عرض توضيحي",
    contactSales: "التواصل مع فريق المبيعات",
    customAgent: "وكيل مخصص",

    benefits: [
      "تقليل العمل اليدوي",
      "تحسين جودة القرارات",
      "توسيع العمليات باستخدام الذكاء الاصطناعي",
      "توحيد التحليل بين الفرق",
    ],

    buildTitle: "ما الذي نبنيه لشركتك",
    buildDesc:
      "تبني Runexa Systems وكلاء ذكاء اصطناعي مخصصين لسير العمل القانوني، المالي، الموارد البشرية، الأعمال، معالجة المستندات، المبيعات والتسويق.",

    customTitle: "نصمم وكلاء ذكاء اصطناعي حسب احتياجات شركتك",
    customDesc:
      "كل شركة مختلفة. لذلك ننشئ وكلاء ذكاء اصطناعي مخصصين ومتكيفين مع بياناتك وسير العمل والعمليات الداخلية.",

    howTitle: "كيف يعمل",
    howSteps: [
      "فهم احتياجاتك",
      "بناء الوكلاء",
      "النشر والتكامل",
      "التوسع باستخدام الذكاء الاصطناعي",
    ],

    featuresTitle: "ميزات Enterprise",
    features: [
      "وصول متعدد المستخدمين",
      "إدارة الفرق",
      "معالجة آمنة للبيانات",
      "لوحات تحكم مخصصة",
      "وصول API",
      "دعم ذو أولوية",
    ],

    ctaTitle: "هل أنت مستعد لإدخال الذكاء الاصطناعي إلى شركتك؟",
    ctaDesc: "لنقم ببناء وكلاء الذكاء الاصطناعي المخصصين لشركتك.",
    ctaButton: "ابدأ الآن",

    categories: [
      {
        title: "Legal AI Agents",
        description:
          "دعم فرق القانون والامتثال والمخاطر من خلال تحليل المستندات بالذكاء الاصطناعي.",
        agents: [
          {
            name: "Legal AI Agent",
            desc: "يحلل العقود الداخلية، يكشف المخاطر، ويساعد على ضمان الامتثال.",
          },
          {
            name: "Contract Review Agent",
            desc: "يراجع الاتفاقيات، يبرز البنود الرئيسية، ويحدد نقاط التفاوض.",
          },
          {
            name: "Compliance Agent",
            desc: "يفحص المستندات والعمليات وفق القواعد الداخلية ومتطلبات الامتثال.",
          },
          {
            name: "Risk Detection Agent",
            desc: "يكشف المخاطر التشغيلية والقانونية والتعاقدية قبل أن تصبح مكلفة.",
          },
        ],
      },
      {
        title: "Finance AI Agents",
        description:
          "أتمتة التقارير المالية، تحليل المصاريف، ودعم اتخاذ القرار.",
        agents: [
          {
            name: "Finance AI Agent",
            desc: "يؤتمت التحليل المالي وينشئ تقارير داخلية.",
          },
          {
            name: "Expense Optimization Agent",
            desc: "يكشف المصاريف غير الضرورية ويقترح فرص خفض التكاليف.",
          },
          {
            name: "Cashflow Forecast Agent",
            desc: "يتوقع اتجاهات التدفق النقدي ويحدد مخاطر السيولة المستقبلية.",
          },
          {
            name: "Financial Reporting Agent",
            desc: "ينشئ ملخصات ولوحات تحكم ورؤى مالية من بيانات الأعمال.",
          },
        ],
      },
      {
        title: "HR AI Agents",
        description:
          "تحسين سير عمل التوظيف والفرز وإدارة الموظفين.",
        agents: [
          {
            name: "HR AI Agent",
            desc: "يفرز السير الذاتية ويسهل عملية التوظيف.",
          },
          {
            name: "CV Screening Agent",
            desc: "يرتب المرشحين حسب متطلبات الدور والمهارات والخبرة.",
          },
          {
            name: "Interview Assistant Agent",
            desc: "ينشئ أسئلة مقابلات ويلخص تقييمات المرشحين.",
          },
          {
            name: "Employee Performance Agent",
            desc: "يحلل ملاحظات الموظفين وبيانات الأداء وخطط التطوير.",
          },
        ],
      },
      {
        title: "Business AI Agents",
        description:
          "مساعدة فرق القيادة على تحليل البيانات، مراقبة مؤشرات الأداء، واتخاذ قرارات أفضل.",
        agents: [
          {
            name: "Business Decision Agent",
            desc: "يحلل بيانات الأعمال ويدعم القرارات الاستراتيجية.",
          },
          {
            name: "Market Analysis Agent",
            desc: "يحلل إشارات السوق والمنافسين والفرص.",
          },
          {
            name: "KPI Monitoring Agent",
            desc: "يتابع مؤشرات الأداء ويبرز تغيرات الأداء.",
          },
          {
            name: "Strategy Recommendation Agent",
            desc: "ينشئ توصيات استراتيجية بناءً على بيانات وأهداف الأعمال.",
          },
        ],
      },
      {
        title: "Document AI Agents",
        description:
          "معالجة المستندات والفواتير والتقارير والملفات التشغيلية بسرعة أكبر.",
        agents: [
          {
            name: "Document Analysis Agent",
            desc: "يستخرج المعلومات الرئيسية من المستندات ويلخص النقاط المهمة.",
          },
          {
            name: "Invoice Processing Agent",
            desc: "يقرأ الفواتير، يستخرج المبالغ، يكشف الشذوذ، ويدعم سير عمل المحاسبة.",
          },
        ],
      },
      {
        title: "Sales & Marketing AI Agents",
        description:
          "دعم فرق النمو برؤى العملاء والمبيعات والحملات.",
        agents: [
          {
            name: "Sales Insights Agent",
            desc: "يحلل بيانات المبيعات، يكشف الفرص، ويدعم قرارات خط المبيعات.",
          },
          {
            name: "Customer Behavior Agent",
            desc: "يفهم أنماط العملاء ويحدد فرص النمو.",
          },
        ],
      },
    ],
  },
};

export default function EnterprisePage() {
  const [language, setLanguage] = useState("en");
  const t = labels[language] || labels.en;

  useEffect(() => {
    const saved = localStorage.getItem("locale");

    if (saved && labels[saved]) {
      setLanguage(saved);
    }

    const handleLocaleChange = () => {
      const nextLocale = localStorage.getItem("locale");

      if (nextLocale && labels[nextLocale]) {
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
