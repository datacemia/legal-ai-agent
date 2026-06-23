"use client";

import { useEffect, useState } from "react";
import {
  defaultLocale,
  getSavedLocale,
} from "../../../lib/i18n";

type Locale = "en" | "fr" | "ar";

const normalizeLocale = (
  value: string | null | undefined,
  fallback: Locale = "en"
): Locale => {
  if (value === "en" || value === "fr" || value === "ar") {
    return value;
  }

  return fallback;
};

const getDefaultLocale = (): Locale => {
  return normalizeLocale(defaultLocale, "en");
};

const companyCopy = {
  en: {
    title: "Company Information",
    updated: "Last updated: June 2026",
    eyebrow: "Company & trust",
    heroTitle: "Specialized AI agents for real-world work.",
    heroText:
      "Runexa Systems LLC builds AI agents designed to help individuals, professionals, and organizations analyze information, understand documents, learn faster, and make better decisions.",
    primaryCta: "Contact Runexa",
    secondaryCta: "View Security",

    quickFactsTitle: "Company quick facts",
    quickFacts: [
      ["Company", "Runexa Systems LLC"],
      ["Founded", "2026"],
      ["Headquarters", "Sheridan, Wyoming, United States"],
      ["Website", "https://runexa.ai"],
      ["Contact", "contact@runexa.ai"],
      ["Focus", "Legal AI · Finance AI · Study AI · Business AI"],
    ],

    missionTitle: "Why Runexa exists",
    missionText:
      "Runexa was born from real-life challenges. As a parent, professional, and entrepreneur, I often faced complex information that required time and expertise to understand. Runexa was created to make this information more accessible through specialized AI agents that help people learn, analyze, and make decisions with greater clarity and confidence.",

    founderTitle: "Founder",
    founderText:
      "Runexa was founded by Dr. Rachid Ejjami with the goal of building practical AI systems focused on real-world work rather than generic chat experiences.",

    approachTitle: "Our approach",
    approachSubtitle:
      "Runexa is built around specialized agents, responsible AI use, and clear user control.",
    approachCards: [
      [
        "Specialized AI Agents",
        "Designed for legal analysis, finance, learning, and business workflows instead of one generic chat experience.",
      ],
      [
        "Human Decision Making",
        "AI assists users with analysis and structure, but important decisions should remain subject to human review.",
      ],
      [
        "Privacy by Design",
        "Privacy, security, and responsible data handling are considered throughout the platform and explained in dedicated policy pages.",
      ],
      [
        "Continuous Improvement",
        "Agents evolve as models, workflows, infrastructure, evaluation methods, and safety systems improve.",
      ],
    ],

    responsibilityTitle: "Company responsibility",
    responsibilityText:
      "Runexa provides AI-powered software designed to assist users with analysis, understanding, and decision support. Users remain responsible for reviewing outputs and determining whether professional advice or additional review is appropriate.",

    trustTitle: "Trust resources",
    trustSubtitle:
      "Runexa separates trust, policy, and product information so users can quickly understand how the platform works.",
    trustCards: [
      ["Privacy Policy", "Explains data collection, use, retention, deletion, rights, and model-training position.", "/privacy"],
      ["Security", "Explains security safeguards, access controls, infrastructure, monitoring, and data handling.", "/security"],
      ["AI Disclaimer", "Explains AI limitations, human review, no professional advice, and responsible use.", "/legal/ai-disclaimer"],
      ["Terms of Service", "Explains account rules, acceptable use, billing, ownership, liability, and service conditions.", "/terms"],
    ],

    legalTitle: "Contact & legal information",
    legalRows: [
      ["Legal name", "Runexa Systems LLC"],
      ["Registered address", "1309 Coffeen Avenue, Suite 1200, Sheridan, WY 82801, United States"],
      ["General contact", "contact@runexa.ai"],
      ["Website", "https://runexa.ai"],
      ["Governing law", "State of Wyoming, United States, unless applicable law requires otherwise"],
    ],
  },

  fr: {
    title: "Informations sur l’entreprise",
    updated: "Dernière mise à jour : juin 2026",
    eyebrow: "Entreprise & confiance",
    heroTitle: "Des agents IA spécialisés pour le travail réel.",
    heroText:
      "Runexa Systems LLC développe des agents IA conçus pour aider les particuliers, professionnels et organisations à analyser l’information, comprendre les documents, apprendre plus vite et prendre de meilleures décisions.",
    primaryCta: "Contacter Runexa",
    secondaryCta: "Voir la sécurité",

    quickFactsTitle: "Informations clés",
    quickFacts: [
      ["Entreprise", "Runexa Systems LLC"],
      ["Création", "2026"],
      ["Siège", "Sheridan, Wyoming, États-Unis"],
      ["Site web", "https://runexa.ai"],
      ["Contact", "contact@runexa.ai"],
      ["Domaines", "IA juridique · IA finance · IA étude · IA business"],
    ],

    missionTitle: "Pourquoi Runexa existe",
    missionText:
      "Runexa est né de défis réels rencontrés au quotidien. En tant que parent, professionnel et entrepreneur, j’ai souvent été confronté à des informations complexes nécessitant du temps et de l’expertise pour être comprises. Runexa a été créé pour rendre ces informations plus accessibles grâce à des agents IA spécialisés qui aident les utilisateurs à apprendre, analyser et prendre des décisions avec plus de clarté et de confiance.",

    founderTitle: "Fondateur",
    founderText:
      "Runexa a été fondé par Dr. Rachid Ejjami avec l’objectif de créer des systèmes IA pratiques, centrés sur le travail réel plutôt que sur des expériences de chat génériques.",

    approachTitle: "Notre approche",
    approachSubtitle:
      "Runexa est construit autour d’agents spécialisés, d’une utilisation responsable de l’IA et d’un contrôle clair pour l’utilisateur.",
    approachCards: [
      [
        "Agents IA spécialisés",
        "Conçus pour l’analyse juridique, la finance, l’apprentissage et les workflows business plutôt qu’une seule expérience de chat générique.",
      ],
      [
        "Décision humaine",
        "L’IA aide à analyser et structurer l’information, mais les décisions importantes doivent rester soumises à une revue humaine.",
      ],
      [
        "Confidentialité dès la conception",
        "La confidentialité, la sécurité et le traitement responsable des données sont pris en compte dans la plateforme et expliqués dans des pages dédiées.",
      ],
      [
        "Amélioration continue",
        "Les agents évoluent avec les modèles, workflows, infrastructures, méthodes d’évaluation et systèmes de sécurité.",
      ],
    ],

    responsibilityTitle: "Responsabilité de l’entreprise",
    responsibilityText:
      "Runexa fournit un logiciel alimenté par l’IA conçu pour aider les utilisateurs dans l’analyse, la compréhension et l’aide à la décision. Les utilisateurs restent responsables de relire les résultats et de déterminer si un avis professionnel ou une revue supplémentaire est nécessaire.",

    trustTitle: "Ressources de confiance",
    trustSubtitle:
      "Runexa sépare les informations de confiance, de politique et de produit afin que les utilisateurs comprennent rapidement le fonctionnement de la plateforme.",
    trustCards: [
      ["Politique de confidentialité", "Explique la collecte, l’utilisation, la conservation, la suppression, les droits et la position sur l’entraînement des modèles.", "/privacy"],
      ["Sécurité", "Explique les mesures de sécurité, contrôles d’accès, infrastructure, surveillance et traitement des données.", "/security"],
      ["Avertissement IA", "Explique les limites de l’IA, la revue humaine, l’absence de conseil professionnel et l’utilisation responsable.", "/legal/ai-disclaimer"],
      ["Conditions d’utilisation", "Explique les règles de compte, l’utilisation acceptable, la facturation, la propriété, la responsabilité et les conditions du service.", "/terms"],
    ],

    legalTitle: "Contact et informations légales",
    legalRows: [
      ["Nom légal", "Runexa Systems LLC"],
      ["Adresse enregistrée", "1309 Coffeen Avenue, Suite 1200, Sheridan, WY 82801, États-Unis"],
      ["Contact général", "contact@runexa.ai"],
      ["Site web", "https://runexa.ai"],
      ["Droit applicable", "État du Wyoming, États-Unis, sauf si la loi applicable exige autrement"],
    ],
  },

  ar: {
    title: "معلومات الشركة",
    updated: "آخر تحديث: يونيو 2026",
    eyebrow: "الشركة والثقة",
    heroTitle: "وكلاء ذكاء اصطناعي متخصصون للعمل الواقعي.",
    heroText:
      "تطوّر Runexa Systems LLC وكلاء ذكاء اصطناعي مصممين لمساعدة الأفراد والمهنيين والمؤسسات على تحليل المعلومات وفهم المستندات والتعلم بشكل أسرع واتخاذ قرارات أفضل.",
    primaryCta: "تواصل مع Runexa",
    secondaryCta: "عرض الأمان",

    quickFactsTitle: "معلومات سريعة عن الشركة",
    quickFacts: [
      ["الشركة", "Runexa Systems LLC"],
      ["سنة التأسيس", "2026"],
      ["المقر", "Sheridan, Wyoming, United States"],
      ["الموقع", "https://runexa.ai"],
      ["التواصل", "contact@runexa.ai"],
      ["التركيز", "الذكاء القانوني · الذكاء المالي · ذكاء الدراسة · ذكاء الأعمال"],
    ],

    missionTitle: "لماذا توجد Runexa",
    missionText:
      "وُلدت Runexa من تحديات واقعية واجهتها في الحياة اليومية. بصفتي أبًا ومهنيًا ورائد أعمال، كنت أتعامل باستمرار مع معلومات معقدة تتطلب وقتًا وخبرة لفهمها. لذلك أُنشئت Runexa لجعل هذه المعلومات أكثر سهولة من خلال وكلاء ذكاء اصطناعي متخصصين يساعدون المستخدمين على التعلّم والتحليل واتخاذ القرارات بوضوح وثقة أكبر.",

    founderTitle: "المؤسس",
    founderText:
      "أسس Dr. Rachid Ejjami منصة Runexa بهدف بناء أنظمة ذكاء اصطناعي عملية تركز على العمل الواقعي بدلاً من تجارب الدردشة العامة.",

    approachTitle: "نهجنا",
    approachSubtitle:
      "تقوم Runexa على وكلاء متخصصين واستخدام مسؤول للذكاء الاصطناعي وتحكم واضح للمستخدم.",
    approachCards: [
      [
        "وكلاء ذكاء اصطناعي متخصصون",
        "مصممون للتحليل القانوني والمالية والتعلم وسير عمل الأعمال بدلاً من تجربة دردشة عامة واحدة.",
      ],
      [
        "اتخاذ القرار البشري",
        "يساعد الذكاء الاصطناعي في التحليل والتنظيم، لكن القرارات المهمة يجب أن تخضع للمراجعة البشرية.",
      ],
      [
        "الخصوصية منذ التصميم",
        "يتم أخذ الخصوصية والأمان والتعامل المسؤول مع البيانات في الاعتبار داخل المنصة وشرحها في صفحات مخصصة.",
      ],
      [
        "تحسين مستمر",
        "تتطور الوكلاء مع تحسن النماذج وسير العمل والبنية التحتية وطرق التقييم وأنظمة السلامة.",
      ],
    ],

    responsibilityTitle: "مسؤولية الشركة",
    responsibilityText:
      "توفر Runexa برنامجاً مدعوماً بالذكاء الاصطناعي لمساعدة المستخدمين في التحليل والفهم ودعم القرار. يبقى المستخدمون مسؤولين عن مراجعة المخرجات وتحديد ما إذا كانت هناك حاجة إلى مشورة مهنية أو مراجعة إضافية.",

    trustTitle: "موارد الثقة",
    trustSubtitle:
      "تفصل Runexa معلومات الثقة والسياسات والمنتج حتى يتمكن المستخدمون من فهم كيفية عمل المنصة بسرعة.",
    trustCards: [
      ["سياسة الخصوصية", "تشرح جمع البيانات واستخدامها والاحتفاظ بها وحذفها والحقوق وموقف تدريب النماذج.", "/privacy"],
      ["الأمان", "يشرح ضمانات الأمان وضوابط الوصول والبنية التحتية والمراقبة والتعامل مع البيانات.", "/security"],
      ["إخلاء مسؤولية الذكاء الاصطناعي", "يشرح حدود الذكاء الاصطناعي والمراجعة البشرية وعدم تقديم المشورة المهنية والاستخدام المسؤول.", "/legal/ai-disclaimer"],
      ["شروط الاستخدام", "تشرح قواعد الحساب والاستخدام المقبول والفوترة والملكية والمسؤولية وشروط الخدمة.", "/terms"],
    ],

    legalTitle: "معلومات التواصل والمعلومات القانونية",
    legalRows: [
      ["الاسم القانوني", "Runexa Systems LLC"],
      ["العنوان المسجل", "1309 Coffeen Avenue, Suite 1200, Sheridan, WY 82801, United States"],
      ["التواصل العام", "contact@runexa.ai"],
      ["الموقع", "https://runexa.ai"],
      ["القانون الواجب التطبيق", "ولاية وايومنغ، الولايات المتحدة، ما لم يقتض القانون المعمول به خلاف ذلك"],
    ],
  },
} satisfies Record<Locale, {
  title: string;
  updated: string;
  eyebrow: string;
  heroTitle: string;
  heroText: string;
  primaryCta: string;
  secondaryCta: string;
  quickFactsTitle: string;
  quickFacts: string[][];
  missionTitle: string;
  missionText: string;
  founderTitle: string;
  founderText: string;
  approachTitle: string;
  approachSubtitle: string;
  approachCards: string[][];
  responsibilityTitle: string;
  responsibilityText: string;
  trustTitle: string;
  trustSubtitle: string;
  trustCards: string[][];
  legalTitle: string;
  legalRows: string[][];
}>;

export default function CompanyClient({
  initialLocale,
  lockInitialLocale = false,
}: {
  initialLocale?: Locale;
  lockInitialLocale?: boolean;
}) {
  const resolvedInitialLocale = initialLocale || getDefaultLocale();

  const [locale, setLocale] = useState<Locale>(resolvedInitialLocale);

  useEffect(() => {
    if (lockInitialLocale) {
      setLocale(resolvedInitialLocale);
      return;
    }

    setLocale(normalizeLocale(getSavedLocale(), resolvedInitialLocale));
  }, [resolvedInitialLocale, lockInitialLocale]);

  const t = companyCopy[locale];

  return (
    <main
      dir={locale === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-950 px-4 py-10 text-slate-900"
    >
      <div className="mx-auto max-w-6xl space-y-8">
        <section className="overflow-hidden rounded-[2rem] border border-white/10 bg-white shadow-2xl">
          <div className="grid gap-0 lg:grid-cols-[1.1fr_0.9fr]">
            <div className="p-8 md:p-12">
              <p className="text-sm font-semibold uppercase tracking-wide text-blue-600">
                {t.eyebrow}
              </p>

              <h1 className="mt-4 max-w-3xl text-4xl font-bold tracking-tight text-slate-950 md:text-5xl">
                {t.heroTitle}
              </h1>

              <p className="mt-5 max-w-3xl text-lg leading-8 text-slate-600">
                {t.heroText}
              </p>

              <div className="mt-8 flex flex-wrap gap-3">
                <a
                  href="/contact-entreprise/contact"
                  className="inline-flex items-center justify-center rounded-xl bg-blue-600 px-5 py-3 text-sm font-semibold text-white shadow-sm hover:bg-blue-700"
                >
                  {t.primaryCta}
                </a>

                <a
                  href="/security"
                  className="inline-flex items-center justify-center rounded-xl border border-slate-300 bg-white px-5 py-3 text-sm font-semibold text-slate-800 hover:bg-slate-50"
                >
                  {t.secondaryCta}
                </a>
              </div>

              <p className="mt-6 text-sm text-slate-500">
                {t.updated}
              </p>
            </div>

            <div className="bg-slate-950 p-8 text-white md:p-12">
              <h2 className="text-2xl font-bold">
                {t.quickFactsTitle}
              </h2>

              <div className="mt-8 space-y-4">
                {t.quickFacts.map(([label, value]) => (
                  <div
                    key={label}
                    className="rounded-2xl border border-white/10 bg-white/5 p-4"
                  >
                    <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
                      {label}
                    </p>

                    <p className="mt-1 text-sm font-medium leading-6 text-slate-100">
                      {value}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        <section className="rounded-[2rem] border border-white/10 bg-white p-8 shadow-xl md:p-10">
          <h2 className="text-2xl font-bold text-slate-950">
            {t.missionTitle}
          </h2>

          <p className="mt-4 max-w-4xl text-slate-600">
            {t.missionText}
          </p>
        </section>

        <section className="rounded-[2rem] border border-white/10 bg-white p-8 shadow-xl md:p-10">
          <h2 className="text-2xl font-bold text-slate-950">
            {t.founderTitle}
          </h2>

          <p className="mt-4 max-w-4xl text-slate-600">
            {t.founderText}
          </p>
        </section>

        <section className="rounded-[2rem] border border-white/10 bg-white p-8 shadow-xl md:p-10">
          <h2 className="text-2xl font-bold text-slate-950">
            {t.approachTitle}
          </h2>

          <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-600">
            {t.approachSubtitle}
          </p>

          <div className="mt-8 grid gap-4 md:grid-cols-2">
            {t.approachCards.map(([title, text]) => (
              <article
                key={title}
                className="rounded-2xl border border-slate-200 bg-slate-50 p-5"
              >
                <h3 className="font-semibold text-slate-950">
                  {title}
                </h3>

                <p className="mt-2 text-sm leading-6 text-slate-600">
                  {text}
                </p>
              </article>
            ))}
          </div>
        </section>

        <section className="rounded-[2rem] border border-white/10 bg-white p-8 shadow-xl md:p-10">
          <h2 className="text-2xl font-bold text-slate-950">
            {t.responsibilityTitle}
          </h2>

          <p className="mt-4 max-w-4xl text-slate-600">
            {t.responsibilityText}
          </p>
        </section>

        <section className="rounded-[2rem] border border-white/10 bg-white p-8 shadow-xl md:p-10">
          <h2 className="text-2xl font-bold text-slate-950">
            {t.trustTitle}
          </h2>

          <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-600">
            {t.trustSubtitle}
          </p>

          <div className="mt-8 grid gap-4 md:grid-cols-2">
            {t.trustCards.map(([title, text, href]) => (
              <a
                key={title}
                href={href}
                className="rounded-2xl border border-slate-200 bg-slate-50 p-5 transition hover:border-blue-300 hover:bg-blue-50"
              >
                <h3 className="font-semibold text-slate-950">
                  {title}
                </h3>

                <p className="mt-2 text-sm leading-6 text-slate-600">
                  {text}
                </p>
              </a>
            ))}
          </div>
        </section>

        <section className="rounded-[2rem] border border-white/10 bg-white p-8 shadow-xl md:p-10">
          <h1 className="text-3xl font-bold text-slate-950">
            {t.title}
          </h1>

          <p className="mt-2 text-sm text-slate-500">
            {t.updated}
          </p>

          <div className="mt-8 overflow-hidden rounded-2xl border border-slate-200">
            {t.legalRows.map(([label, value], index) => (
              <div
                key={label}
                className={`grid gap-2 p-5 md:grid-cols-[0.35fr_0.65fr] ${
                  index === 0 ? "" : "border-t border-slate-200"
                }`}
              >
                <div className="text-sm font-semibold text-slate-950">
                  {label}
                </div>

                <div className="break-words text-sm leading-6 text-slate-600">
                  {value}
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}
