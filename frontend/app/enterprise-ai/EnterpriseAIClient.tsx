"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getSavedLocale } from "../../lib/i18n";

const translations = {
  en: {
    badge: "Runexa Enterprise AI",
    title: "Enterprise AI Workspace & Custom AI Systems",
    subtitle:
      "Runexa helps teams and organizations create secure AI workflows for document analysis, financial reporting, learning operations, business intelligence, and strategic decision support.",
    requestDemo: "Request a Demo",
    exploreEnterprise: "Explore Enterprise",

    teamWorkspaces: "Team workspaces",
    teamWorkspacesText:
      "Create shared AI workspaces for teams, departments, and organizations.",
    customAiWorkflows: "Custom AI workflows",
    customAiWorkflowsText:
      "Design AI systems for document analysis, reporting, learning, and decisions.",
    organizationDashboard: "Organization dashboard",
    organizationDashboardText:
      "Manage users, usage, credits, and AI workflows in one place.",
    enterpriseSupport: "Enterprise support",
    enterpriseSupportText:
      "Support for custom credits, priority workflows, and organization needs.",

    useCasesTitle: "Enterprise AI use cases",
    useCases: [
      "Legal document analysis and contract workflows",
      "Financial reporting and business intelligence",
      "Training, learning, and internal knowledge workflows",
    ],

    faqTitle: "Enterprise AI FAQ",
    faq: [
      [
        "Can Runexa support teams?",
        "Yes. Runexa is designed to support team workspaces, organization dashboards, multi-user access, and custom AI workflows.",
      ],
      [
        "What enterprise workflows can Runexa automate?",
        "Runexa can support legal analysis, financial reporting, business intelligence, learning operations, and internal decision-support workflows.",
      ],
      [
        "Is Runexa suitable for organizations?",
        "Yes. Runexa is positioned as a secure AI workspace for individuals, professionals, and organizations.",
      ],
      [
        "Can Runexa build custom AI systems?",
        "Runexa can support custom AI systems and workflows for teams and enterprise use cases.",
      ],
    ],

    jsonDescription:
      "Enterprise AI workspace for document analysis, financial reporting, learning workflows, business intelligence, and decision support.",
  },

  fr: {
    badge: "Runexa Enterprise AI",
    title: "Espace IA entreprise et systèmes IA personnalisés",
    subtitle:
      "Runexa aide les équipes et organisations à créer des workflows IA sécurisés pour l’analyse documentaire, le reporting financier, l’apprentissage, la business intelligence et l’aide à la décision stratégique.",
    requestDemo: "Demander une démo",
    exploreEnterprise: "Explorer Enterprise",

    teamWorkspaces: "Espaces de travail équipe",
    teamWorkspacesText:
      "Créez des espaces IA partagés pour les équipes, départements et organisations.",
    customAiWorkflows: "Workflows IA personnalisés",
    customAiWorkflowsText:
      "Concevez des systèmes IA pour l’analyse documentaire, le reporting, l’apprentissage et les décisions.",
    organizationDashboard: "Dashboard organisation",
    organizationDashboardText:
      "Gérez utilisateurs, utilisation, crédits et workflows IA au même endroit.",
    enterpriseSupport: "Support entreprise",
    enterpriseSupportText:
      "Support pour crédits personnalisés, workflows prioritaires et besoins organisationnels.",

    useCasesTitle: "Cas d’usage IA entreprise",
    useCases: [
      "Analyse de documents juridiques et workflows contractuels",
      "Reporting financier et business intelligence",
      "Formation, apprentissage et workflows de connaissances internes",
    ],

    faqTitle: "FAQ IA entreprise",
    faq: [
      [
        "Runexa peut-il prendre en charge les équipes ?",
        "Oui. Runexa est conçu pour prendre en charge les espaces de travail équipe, dashboards organisation, accès multi-utilisateurs et workflows IA personnalisés.",
      ],
      [
        "Quels workflows entreprise Runexa peut-il automatiser ?",
        "Runexa peut soutenir l’analyse juridique, le reporting financier, la business intelligence, les opérations d’apprentissage et les workflows internes d’aide à la décision.",
      ],
      [
        "Runexa est-il adapté aux organisations ?",
        "Oui. Runexa est positionné comme un espace IA sécurisé pour les individus, professionnels et organisations.",
      ],
      [
        "Runexa peut-il créer des systèmes IA personnalisés ?",
        "Runexa peut prendre en charge des systèmes et workflows IA personnalisés pour les équipes et cas d’usage entreprise.",
      ],
    ],

    jsonDescription:
      "Espace IA entreprise pour l’analyse documentaire, le reporting financier, les workflows d’apprentissage, la business intelligence et l’aide à la décision.",
  },

  ar: {
    badge: "Runexa Enterprise AI",
    title: "مساحة ذكاء اصطناعي للمؤسسات وأنظمة ذكاء اصطناعي مخصصة",
    subtitle:
      "يساعد Runexa الفرق والمؤسسات على إنشاء تدفقات عمل آمنة بالذكاء الاصطناعي لتحليل المستندات والتقارير المالية وعمليات التعلم وذكاء الأعمال ودعم القرار الاستراتيجي.",
    requestDemo: "طلب عرض توضيحي",
    exploreEnterprise: "استكشاف Enterprise",

    teamWorkspaces: "مساحات عمل الفرق",
    teamWorkspacesText:
      "أنشئ مساحات عمل ذكاء اصطناعي مشتركة للفرق والأقسام والمؤسسات.",
    customAiWorkflows: "تدفقات عمل ذكاء اصطناعي مخصصة",
    customAiWorkflowsText:
      "صمّم أنظمة ذكاء اصطناعي لتحليل المستندات والتقارير والتعلم واتخاذ القرارات.",
    organizationDashboard: "لوحة تحكم المؤسسة",
    organizationDashboardText:
      "أدر المستخدمين والاستخدام والأرصدة وتدفقات العمل الذكية في مكان واحد.",
    enterpriseSupport: "دعم المؤسسات",
    enterpriseSupportText:
      "دعم للأرصدة المخصصة وتدفقات العمل ذات الأولوية واحتياجات المؤسسة.",

    useCasesTitle: "حالات استخدام الذكاء الاصطناعي للمؤسسات",
    useCases: [
      "تحليل المستندات القانونية وتدفقات عمل العقود",
      "التقارير المالية وذكاء الأعمال",
      "التدريب والتعلم وتدفقات المعرفة الداخلية",
    ],

    faqTitle: "أسئلة شائعة حول ذكاء المؤسسات",
    faq: [
      [
        "هل يمكن لـ Runexa دعم الفرق؟",
        "نعم. تم تصميم Runexa لدعم مساحات عمل الفرق ولوحات تحكم المؤسسات والوصول متعدد المستخدمين وتدفقات العمل المخصصة بالذكاء الاصطناعي.",
      ],
      [
        "ما تدفقات العمل المؤسسية التي يمكن لـ Runexa أتمتتها؟",
        "يمكن لـ Runexa دعم التحليل القانوني والتقارير المالية وذكاء الأعمال وعمليات التعلم وتدفقات دعم القرار الداخلية.",
      ],
      [
        "هل Runexa مناسب للمؤسسات؟",
        "نعم. يتم تقديم Runexa كمساحة عمل آمنة بالذكاء الاصطناعي للأفراد والمهنيين والمؤسسات.",
      ],
      [
        "هل يمكن لـ Runexa بناء أنظمة ذكاء اصطناعي مخصصة؟",
        "يمكن لـ Runexa دعم أنظمة وتدفقات عمل مخصصة بالذكاء الاصطناعي للفرق وحالات استخدام المؤسسات.",
      ],
    ],

    jsonDescription:
      "مساحة ذكاء اصطناعي للمؤسسات لتحليل المستندات والتقارير المالية وتدفقات التعلم وذكاء الأعمال ودعم القرار.",
  },
};

type Locale = "en" | "fr" | "ar";

export default function EnterpriseAIClient({
  initialLocale = "en",
  lockInitialLocale = false,
}: {
  initialLocale?: Locale;
  lockInitialLocale?: boolean;
}) {
  const [locale, setLocale] = useState<Locale>(initialLocale);

  useEffect(() => {
    if (lockInitialLocale) {
      setLocale(initialLocale);
      return;
    }

    const saved = getSavedLocale();

    if (saved === "fr" || saved === "ar") {
      setLocale(saved);
    } else {
      setLocale(initialLocale);
    }

    const handleLocaleChange = () => {
      const updated = getSavedLocale();

      if (updated === "fr" || updated === "ar") {
        setLocale(updated);
      } else {
        setLocale(initialLocale);
      }
    };

    window.addEventListener(
      "locale-change",
      handleLocaleChange
    );

    return () => {
      window.removeEventListener(
        "locale-change",
        handleLocaleChange
      );
    };
  }, [initialLocale, lockInitialLocale]);

  const t = translations[locale];

  return (
    <main
      dir={locale === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-6 py-20 text-slate-900"
    >
      <section className="mx-auto max-w-6xl text-center">
        <p className="font-semibold text-blue-600">
          {t.badge}
        </p>

        <h1 className="mt-4 text-5xl font-bold tracking-tight">
          {t.title}
        </h1>

        <p className="mx-auto mt-6 max-w-3xl text-lg text-slate-600">
          {t.subtitle}
        </p>

        <div className="mt-8 flex flex-wrap justify-center gap-3">
          <Link
            href="/contact-entreprise/contact"
            className="rounded-xl bg-blue-600 px-6 py-3 text-sm font-semibold text-white hover:bg-blue-700"
          >
            {t.requestDemo}
          </Link>

          <Link
            href="/enterprise"
            className="rounded-xl border border-slate-200 bg-white px-6 py-3 text-sm font-semibold text-slate-900 hover:bg-slate-50"
          >
            {t.exploreEnterprise}
          </Link>
        </div>
      </section>

      <section className="mx-auto mt-16 grid max-w-6xl gap-6 md:grid-cols-4">
        {[
          [t.teamWorkspaces, t.teamWorkspacesText],
          [t.customAiWorkflows, t.customAiWorkflowsText],
          [t.organizationDashboard, t.organizationDashboardText],
          [t.enterpriseSupport, t.enterpriseSupportText],
        ].map(([title, desc]) => (
          <div
            key={title}
            className="rounded-2xl border bg-white p-6 shadow-sm"
          >
            <h2 className="font-bold">
              {title}
            </h2>

            <p className="mt-3 text-sm leading-6 text-slate-600">
              {desc}
            </p>
          </div>
        ))}
      </section>

      <section className="mx-auto mt-16 max-w-6xl rounded-3xl border bg-white p-8 shadow-sm md:p-12">
        <h2 className="text-3xl font-bold">
          {t.useCasesTitle}
        </h2>

        <div className="mt-8 grid gap-4 md:grid-cols-3">
          {t.useCases.map((item) => (
            <div
              key={item}
              className="rounded-2xl bg-slate-50 p-6"
            >
              <p className="font-semibold">
                {item}
              </p>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto mt-16 max-w-6xl rounded-3xl border bg-white p-8 shadow-sm md:p-12">
        <h2 className="text-3xl font-bold">
          {t.faqTitle}
        </h2>

        <div className="mt-8 grid gap-4 md:grid-cols-2">
          {t.faq.map(([q, a]) => (
            <div
              key={q}
              className="rounded-2xl bg-slate-50 p-6"
            >
              <h3 className="font-bold">
                {q}
              </h3>

              <p className="mt-2 text-sm leading-6 text-slate-600">
                {a}
              </p>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
