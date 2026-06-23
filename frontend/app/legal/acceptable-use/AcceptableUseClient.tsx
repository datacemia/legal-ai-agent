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

const acceptableUseCopy = {
  en: {
    title: "Acceptable Use Policy",
    updated: "Last updated: June 2026",
    eyebrow: "Responsible platform use",
    heroTitle: "Use Runexa responsibly.",
    heroText:
      "This Acceptable Use Policy explains how Runexa may and may not be used. It helps protect users, organizations, uploaded content, workspace isolation, platform integrity, and responsible AI use.",
    primaryCta: "Report abuse",
    secondaryCta: "View Security",

    principlesTitle: "Use principles",
    principlesSubtitle:
      "Runexa is designed for legitimate analysis, learning, decision support, and productivity workflows.",
    principles: [
      [
        "Lawful Use",
        "Use Runexa only in ways that comply with applicable laws, regulations, contracts, and third-party rights.",
      ],
      [
        "Respect for Data Rights",
        "Upload only content you are allowed to use and only the information reasonably necessary for the requested analysis.",
      ],
      [
        "Platform Integrity",
        "Do not disrupt, bypass, scrape, overload, reverse engineer, or misuse Runexa systems, accounts, APIs, or safeguards.",
      ],
      [
        "Human Accountability",
        "Use AI outputs as decision-support information, not as the sole basis for high-impact decisions without review.",
      ],
    ],

    allowedTitle: "Permitted uses",
    allowedSubtitle:
      "Runexa may be used for practical, lawful, and reviewable workflows, including:",
    allowedUses: [
      "Contract and legal-document review support",
      "Financial-document understanding and budgeting insights",
      "Study support, summaries, quizzes, and learning plans",
      "Business analysis, decision briefs, and operational insights",
      "Document summarization and structured extraction",
      "Internal research, productivity, and workflow support",
    ],

    restrictedTitle: "Restricted activities",
    restrictedSubtitle:
      "You may not use Runexa services, agents, outputs, or infrastructure for the following activities.",
    restrictedCards: [
      [
        "Illegal Activity",
        "Using Runexa for unlawful, fraudulent, deceptive, or rights-violating activity.",
      ],
      [
        "Fraud & Misrepresentation",
        "Impersonation, identity fraud, misleading representations, scams, or deceptive business practices.",
      ],
      [
        "Cyber Abuse",
        "Malware, phishing, hacking, credential theft, unauthorized access, vulnerability exploitation, or cyber abuse.",
      ],
      [
        "Privacy Violations",
        "Unauthorized surveillance, tracking, profiling, doxxing, or processing personal data without a valid right or purpose.",
      ],
      [
        "Confidentiality Violations",
        "Uploading, processing, or sharing third-party confidential, proprietary, or restricted content without authorization.",
      ],
      [
        "Intellectual Property Abuse",
        "Using Runexa to infringe copyright, trademarks, trade secrets, database rights, or other intellectual property rights.",
      ],
      [
        "Harmful Content",
        "Generating or distributing content that promotes harm, abuse, harassment, discrimination, or unlawful conduct.",
      ],
      [
        "Platform Abuse",
        "Scraping, spam, automated abuse, excessive load, bypassing rate limits, or attempting to access another user's data.",
      ],
    ],

    customerProtectionTitle: "Protecting customers and organizations",
    customerProtectionText:
      "Runexa is designed for sensitive workflows. Users must not attempt to access another customer’s data, bypass workspace isolation, misuse uploaded documents, defeat security controls, or use AI systems to create harmful or deceptive activity.",
    customerProtectionItems: [
      "No attempts to access another user's files, outputs, accounts, or workspace",
      "No attempts to bypass authentication, authorization, rate limits, or data isolation",
      "No misuse of third-party confidential information",
      "No unauthorized monitoring, surveillance, or tracking",
      "No abuse of AI-generated outputs for deception, fraud, or harm",
    ],

    aiTitle: "AI and high-impact decisions",
    aiText:
      "Runexa may assist with analysis and decision support, but outputs should not replace required human review, professional oversight, organizational controls, or legal, financial, educational, business, or compliance review where appropriate.",
    aiItems: [
      "Do not rely on AI outputs as the only basis for high-impact decisions",
      "Review important outputs before acting",
      "Use qualified professionals where the decision requires professional judgment",
      "Respect laws, policies, institutional rules, and internal governance requirements",
    ],

    responsibilityTitle: "Content responsibility",
    responsibilityText:
      "Users are responsible for all content uploaded, processed, generated, or shared through Runexa. Users must ensure they have the legal right to use uploaded content and should provide only information reasonably necessary for the requested task.",
    responsibilityItems: [
      "You remain responsible for uploaded documents, datasets, prompts, and outputs",
      "You must have the right to upload and process the content",
      "Organizations remain responsible for their governance, compliance, confidentiality, and regulatory obligations",
      "You should avoid including unrelated sensitive data",
    ],

    enforcementTitle: "Enforcement",
    enforcementText:
      "Runexa Systems LLC may review suspected violations and take action where needed to protect users, the platform, service providers, and the integrity of the services.",
    enforcementCards: [
      ["Warning", "We may notify the user or organization about a suspected violation."],
      ["Restriction", "We may limit access to certain features, agents, files, uploads, or workspaces."],
      ["Suspension", "We may temporarily suspend access while an issue is reviewed."],
      ["Termination", "We may terminate access for serious, repeated, unlawful, or harmful violations."],
    ],

    reportingTitle: "Reporting violations",
    reportingText:
      "Suspected abuse, security concerns, or violations of this Policy may be reported to contact@runexa.ai.",

    changesTitle: "Policy updates",
    changesText:
      "Runexa Systems LLC may update this Acceptable Use Policy from time to time. Updated versions will be posted on this page with a revised “Last updated” date.",
  },

  fr: {
    title: "Politique d’utilisation acceptable",
    updated: "Dernière mise à jour : juin 2026",
    eyebrow: "Utilisation responsable de la plateforme",
    heroTitle: "Utilisez Runexa de manière responsable.",
    heroText:
      "Cette Politique d’utilisation acceptable explique comment Runexa peut et ne peut pas être utilisé. Elle aide à protéger les utilisateurs, les organisations, les contenus importés, l’isolation des espaces de travail, l’intégrité de la plateforme et l’usage responsable de l’IA.",
    primaryCta: "Signaler un abus",
    secondaryCta: "Voir la sécurité",

    principlesTitle: "Principes d’utilisation",
    principlesSubtitle:
      "Runexa est conçu pour des workflows légitimes d’analyse, d’apprentissage, d’aide à la décision et de productivité.",
    principles: [
      [
        "Utilisation licite",
        "Utilisez Runexa uniquement d’une manière conforme aux lois, réglementations, contrats et droits de tiers applicables.",
      ],
      [
        "Respect des droits sur les données",
        "Importez uniquement les contenus que vous êtes autorisé à utiliser et seulement les informations raisonnablement nécessaires à l’analyse demandée.",
      ],
      [
        "Intégrité de la plateforme",
        "Ne perturbez pas, ne contournez pas, ne scrapez pas, ne surchargez pas, ne rétroconcevez pas et n’abusez pas des systèmes, comptes, API ou protections Runexa.",
      ],
      [
        "Responsabilité humaine",
        "Utilisez les résultats IA comme informations d’aide à la décision, et non comme base unique pour des décisions à impact élevé sans revue.",
      ],
    ],

    allowedTitle: "Usages autorisés",
    allowedSubtitle:
      "Runexa peut être utilisé pour des workflows pratiques, licites et vérifiables, notamment :",
    allowedUses: [
      "Aide à la revue de contrats et documents juridiques",
      "Compréhension de documents financiers et insights budgétaires",
      "Aide à l’étude, résumés, quiz et plans d’apprentissage",
      "Analyse business, notes de décision et insights opérationnels",
      "Résumé documentaire et extraction structurée",
      "Recherche interne, productivité et support de workflows",
    ],

    restrictedTitle: "Activités restreintes",
    restrictedSubtitle:
      "Vous ne pouvez pas utiliser les services, agents, résultats ou infrastructures Runexa pour les activités suivantes.",
    restrictedCards: [
      [
        "Activité illégale",
        "Utiliser Runexa pour une activité illégale, frauduleuse, trompeuse ou portant atteinte aux droits de tiers.",
      ],
      [
        "Fraude et fausse représentation",
        "Usurpation d’identité, fraude d’identité, déclarations trompeuses, escroqueries ou pratiques commerciales trompeuses.",
      ],
      [
        "Abus cyber",
        "Malwares, phishing, piratage, vol d’identifiants, accès non autorisé, exploitation de vulnérabilités ou abus cyber.",
      ],
      [
        "Atteintes à la vie privée",
        "Surveillance, suivi, profilage, doxxing ou traitement de données personnelles sans droit ou finalité valide.",
      ],
      [
        "Violation de confidentialité",
        "Importer, traiter ou partager des contenus confidentiels, propriétaires ou restreints de tiers sans autorisation.",
      ],
      [
        "Atteinte à la propriété intellectuelle",
        "Utiliser Runexa pour violer des droits d’auteur, marques, secrets commerciaux, droits de base de données ou autres droits de propriété intellectuelle.",
      ],
      [
        "Contenus nuisibles",
        "Générer ou diffuser des contenus favorisant le préjudice, l’abus, le harcèlement, la discrimination ou une conduite illégale.",
      ],
      [
        "Abus de plateforme",
        "Scraping, spam, abus automatisé, surcharge excessive, contournement de limites ou tentative d’accès aux données d’un autre utilisateur.",
      ],
    ],

    customerProtectionTitle: "Protection des clients et organisations",
    customerProtectionText:
      "Runexa est conçu pour des workflows sensibles. Les utilisateurs ne doivent pas tenter d’accéder aux données d’un autre client, contourner l’isolation des espaces de travail, détourner des documents importés, neutraliser les contrôles de sécurité ou utiliser les systèmes IA pour créer une activité nuisible ou trompeuse.",
    customerProtectionItems: [
      "Aucune tentative d’accès aux fichiers, résultats, comptes ou espaces de travail d’un autre utilisateur",
      "Aucune tentative de contournement de l’authentification, de l’autorisation, des limites ou de l’isolation des données",
      "Aucun détournement d’informations confidentielles de tiers",
      "Aucune surveillance ou traque non autorisée",
      "Aucun abus des résultats IA à des fins de tromperie, fraude ou préjudice",
    ],

    aiTitle: "IA et décisions à impact élevé",
    aiText:
      "Runexa peut aider à l’analyse et à l’aide à la décision, mais les résultats ne doivent pas remplacer la revue humaine requise, la supervision professionnelle, les contrôles organisationnels ou les revues juridiques, financières, éducatives, business ou de conformité lorsque cela est approprié.",
    aiItems: [
      "Ne vous appuyez pas sur les résultats IA comme seule base pour des décisions à impact élevé",
      "Relisez les résultats importants avant d’agir",
      "Faites appel à des professionnels qualifiés lorsque la décision exige un jugement professionnel",
      "Respectez les lois, politiques, règles institutionnelles et exigences internes de gouvernance",
    ],

    responsibilityTitle: "Responsabilité relative au contenu",
    responsibilityText:
      "Les utilisateurs sont responsables de tout contenu importé, traité, généré ou partagé via Runexa. Les utilisateurs doivent s’assurer qu’ils ont le droit légal d’utiliser les contenus importés et ne doivent fournir que les informations raisonnablement nécessaires à la tâche demandée.",
    responsibilityItems: [
      "Vous restez responsable des documents, jeux de données, prompts et résultats importés",
      "Vous devez avoir le droit d’importer et de traiter le contenu",
      "Les organisations restent responsables de leur gouvernance, conformité, confidentialité et obligations réglementaires",
      "Vous devez éviter d’inclure des données sensibles non pertinentes",
    ],

    enforcementTitle: "Application",
    enforcementText:
      "Runexa Systems LLC peut examiner les violations présumées et prendre les mesures nécessaires pour protéger les utilisateurs, la plateforme, les prestataires de services et l’intégrité des services.",
    enforcementCards: [
      ["Avertissement", "Nous pouvons informer l’utilisateur ou l’organisation d’une violation présumée."],
      ["Restriction", "Nous pouvons limiter l’accès à certaines fonctionnalités, agents, fichiers, imports ou espaces de travail."],
      ["Suspension", "Nous pouvons suspendre temporairement l’accès pendant l’examen d’un problème."],
      ["Résiliation", "Nous pouvons mettre fin à l’accès en cas de violation grave, répétée, illégale ou nuisible."],
    ],

    reportingTitle: "Signalement des violations",
    reportingText:
      "Les abus présumés, préoccupations de sécurité ou violations de cette Politique peuvent être signalés à contact@runexa.ai.",

    changesTitle: "Mises à jour de la politique",
    changesText:
      "Runexa Systems LLC peut mettre à jour cette Politique d’utilisation acceptable de temps à autre. Les versions mises à jour seront publiées sur cette page avec une date de “Dernière mise à jour” révisée.",
  },

  ar: {
    title: "سياسة الاستخدام المقبول",
    updated: "آخر تحديث: يونيو 2026",
    eyebrow: "استخدام مسؤول للمنصة",
    heroTitle: "استخدم Runexa بمسؤولية.",
    heroText:
      "تشرح سياسة الاستخدام المقبول هذه كيف يمكن استخدام Runexa وما لا يجوز استخدامه من أجله. وهي تساعد في حماية المستخدمين والمؤسسات والمحتوى المرفوع وعزل مساحات العمل وسلامة المنصة والاستخدام المسؤول للذكاء الاصطناعي.",
    primaryCta: "الإبلاغ عن إساءة",
    secondaryCta: "عرض الأمان",

    principlesTitle: "مبادئ الاستخدام",
    principlesSubtitle:
      "تم تصميم Runexa لسير عمل مشروع في التحليل والتعلم ودعم القرار والإنتاجية.",
    principles: [
      [
        "استخدام قانوني",
        "استخدم Runexa فقط بطرق تمتثل للقوانين واللوائح والعقود وحقوق الأطراف الثالثة المعمول بها.",
      ],
      [
        "احترام حقوق البيانات",
        "ارفع فقط المحتوى الذي يحق لك استخدامه والمعلومات الضرورية بشكل معقول للتحليل المطلوب.",
      ],
      [
        "سلامة المنصة",
        "لا تعطل أو تتجاوز أو تجمع أو تثقل أو تعيد هندسة أو تسيء استخدام أنظمة Runexa أو الحسابات أو واجهات API أو الضمانات.",
      ],
      [
        "المساءلة البشرية",
        "استخدم مخرجات الذكاء الاصطناعي كمعلومات لدعم القرار، وليس كأساس وحيد للقرارات عالية التأثير دون مراجعة.",
      ],
    ],

    allowedTitle: "الاستخدامات المسموح بها",
    allowedSubtitle:
      "يمكن استخدام Runexa في سير عمل عملي وقانوني وقابل للمراجعة، بما في ذلك:",
    allowedUses: [
      "دعم مراجعة العقود والمستندات القانونية",
      "فهم المستندات المالية ورؤى الميزانية",
      "دعم الدراسة والملخصات والاختبارات وخطط التعلم",
      "تحليل الأعمال ومذكرات القرار والرؤى التشغيلية",
      "تلخيص المستندات والاستخراج المنظم",
      "البحث الداخلي والإنتاجية ودعم سير العمل",
    ],

    restrictedTitle: "الأنشطة المقيدة",
    restrictedSubtitle:
      "لا يجوز استخدام خدمات أو وكلاء أو مخرجات أو بنية Runexa للأنشطة التالية.",
    restrictedCards: [
      [
        "نشاط غير قانوني",
        "استخدام Runexa في نشاط غير قانوني أو احتيالي أو خادع أو منتهك للحقوق.",
      ],
      [
        "الاحتيال والتضليل",
        "انتحال الشخصية أو احتيال الهوية أو التمثيلات المضللة أو عمليات الاحتيال أو الممارسات التجارية الخادعة.",
      ],
      [
        "إساءة إلكترونية",
        "البرمجيات الخبيثة أو التصيد أو الاختراق أو سرقة بيانات الاعتماد أو الوصول غير المصرح به أو استغلال الثغرات أو إساءة الاستخدام السيبراني.",
      ],
      [
        "انتهاكات الخصوصية",
        "المراقبة أو التتبع أو التنميط أو كشف البيانات الشخصية أو معالجة البيانات الشخصية دون حق أو غرض صحيح.",
      ],
      [
        "انتهاكات السرية",
        "رفع أو معالجة أو مشاركة محتوى سري أو مملوك أو مقيد لطرف ثالث دون تصريح.",
      ],
      [
        "إساءة الملكية الفكرية",
        "استخدام Runexa لانتهاك حقوق النشر أو العلامات التجارية أو الأسرار التجارية أو حقوق قواعد البيانات أو حقوق الملكية الفكرية الأخرى.",
      ],
      [
        "محتوى ضار",
        "إنشاء أو توزيع محتوى يشجع على الضرر أو الإساءة أو المضايقة أو التمييز أو السلوك غير القانوني.",
      ],
      [
        "إساءة استخدام المنصة",
        "جمع البيانات أو الرسائل المزعجة أو الإساءة الآلية أو التحميل المفرط أو تجاوز الحدود أو محاولة الوصول إلى بيانات مستخدم آخر.",
      ],
    ],

    customerProtectionTitle: "حماية العملاء والمؤسسات",
    customerProtectionText:
      "تم تصميم Runexa لسير عمل حساس. يجب ألا يحاول المستخدمون الوصول إلى بيانات عميل آخر أو تجاوز عزل مساحات العمل أو إساءة استخدام المستندات المرفوعة أو تعطيل ضوابط الأمان أو استخدام أنظمة الذكاء الاصطناعي لإنشاء نشاط ضار أو خادع.",
    customerProtectionItems: [
      "عدم محاولة الوصول إلى ملفات أو مخرجات أو حسابات أو مساحة عمل مستخدم آخر",
      "عدم محاولة تجاوز المصادقة أو التفويض أو حدود الاستخدام أو عزل البيانات",
      "عدم إساءة استخدام المعلومات السرية الخاصة بأطراف ثالثة",
      "عدم إجراء مراقبة أو تتبع غير مصرح به",
      "عدم إساءة استخدام مخرجات الذكاء الاصطناعي للخداع أو الاحتيال أو الإضرار",
    ],

    aiTitle: "الذكاء الاصطناعي والقرارات عالية التأثير",
    aiText:
      "قد تساعد Runexa في التحليل ودعم القرار، لكن المخرجات لا ينبغي أن تحل محل المراجعة البشرية المطلوبة أو الإشراف المهني أو الضوابط التنظيمية أو المراجعة القانونية أو المالية أو التعليمية أو التجارية أو مراجعة الامتثال عند الاقتضاء.",
    aiItems: [
      "لا تعتمد على مخرجات الذكاء الاصطناعي كأساس وحيد للقرارات عالية التأثير",
      "راجع المخرجات المهمة قبل اتخاذ أي إجراء",
      "استخدم مهنيين مؤهلين عندما يتطلب القرار حكماً مهنياً",
      "احترم القوانين والسياسات وقواعد المؤسسات ومتطلبات الحوكمة الداخلية",
    ],

    responsibilityTitle: "مسؤولية المحتوى",
    responsibilityText:
      "يتحمل المستخدمون مسؤولية كل محتوى يتم رفعه أو معالجته أو إنشاؤه أو مشاركته عبر Runexa. يجب على المستخدمين التأكد من امتلاكهم الحق القانوني في استخدام المحتوى المرفوع، وتقديم المعلومات الضرورية فقط وبشكل معقول للمهمة المطلوبة.",
    responsibilityItems: [
      "تبقى مسؤولاً عن المستندات ومجموعات البيانات والمطالبات والمخرجات التي ترفعها",
      "يجب أن يكون لديك الحق في رفع المحتوى ومعالجته",
      "تظل المؤسسات مسؤولة عن الحوكمة والامتثال والسرية والالتزامات التنظيمية الخاصة بها",
      "يجب تجنب تضمين بيانات حساسة غير مرتبطة بالمهمة",
    ],

    enforcementTitle: "التنفيذ",
    enforcementText:
      "يجوز لـ Runexa Systems LLC مراجعة الانتهاكات المشتبه بها واتخاذ الإجراءات اللازمة لحماية المستخدمين والمنصة ومزودي الخدمة وسلامة الخدمات.",
    enforcementCards: [
      ["تحذير", "قد نقوم بإخطار المستخدم أو المؤسسة بوجود انتهاك مشتبه به."],
      ["تقييد", "قد نحد من الوصول إلى بعض الميزات أو الوكلاء أو الملفات أو عمليات الرفع أو مساحات العمل."],
      ["تعليق", "قد نعلق الوصول مؤقتاً أثناء مراجعة المشكلة."],
      ["إنهاء", "قد ننهي الوصول في حالة الانتهاكات الجسيمة أو المتكررة أو غير القانونية أو الضارة."],
    ],

    reportingTitle: "الإبلاغ عن الانتهاكات",
    reportingText:
      "يمكن الإبلاغ عن إساءة الاستخدام المشتبه بها أو المخاوف الأمنية أو انتهاكات هذه السياسة عبر contact@runexa.ai.",

    changesTitle: "تحديثات السياسة",
    changesText:
      "يجوز لـ Runexa Systems LLC تحديث سياسة الاستخدام المقبول هذه من وقت لآخر. سيتم نشر النسخ المحدثة على هذه الصفحة مع تاريخ “آخر تحديث” معدل.",
  },
} satisfies Record<Locale, {
  title: string;
  updated: string;
  eyebrow: string;
  heroTitle: string;
  heroText: string;
  primaryCta: string;
  secondaryCta: string;
  principlesTitle: string;
  principlesSubtitle: string;
  principles: string[][];
  allowedTitle: string;
  allowedSubtitle: string;
  allowedUses: string[];
  restrictedTitle: string;
  restrictedSubtitle: string;
  restrictedCards: string[][];
  customerProtectionTitle: string;
  customerProtectionText: string;
  customerProtectionItems: string[];
  aiTitle: string;
  aiText: string;
  aiItems: string[];
  responsibilityTitle: string;
  responsibilityText: string;
  responsibilityItems: string[];
  enforcementTitle: string;
  enforcementText: string;
  enforcementCards: string[][];
  reportingTitle: string;
  reportingText: string;
  changesTitle: string;
  changesText: string;
}>;

export default function AcceptableUseClient({
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

  const t = acceptableUseCopy[locale];

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
                  href="mailto:contact@runexa.ai"
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
                {t.principlesTitle}
              </h2>

              <p className="mt-3 text-sm leading-6 text-slate-300">
                {t.principlesSubtitle}
              </p>

              <div className="mt-8 space-y-4">
                {t.principles.map(([title, text]) => (
                  <div
                    key={title}
                    className="rounded-2xl border border-white/10 bg-white/5 p-4"
                  >
                    <p className="text-sm font-semibold text-white">
                      {title}
                    </p>

                    <p className="mt-1 text-sm leading-6 text-slate-300">
                      {text}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        <section className="rounded-[2rem] border border-white/10 bg-white p-8 shadow-xl md:p-10">
          <h2 className="text-2xl font-bold text-slate-950">
            {t.allowedTitle}
          </h2>

          <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-600">
            {t.allowedSubtitle}
          </p>

          <div className="mt-8 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {t.allowedUses.map((item) => (
              <div
                key={item}
                className="rounded-2xl border border-slate-200 bg-slate-50 p-5"
              >
                <p className="text-sm font-medium leading-6 text-slate-700">
                  {item}
                </p>
              </div>
            ))}
          </div>
        </section>

        <section className="rounded-[2rem] border border-white/10 bg-white p-8 shadow-xl md:p-10">
          <h2 className="text-2xl font-bold text-slate-950">
            {t.restrictedTitle}
          </h2>

          <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-600">
            {t.restrictedSubtitle}
          </p>

          <div className="mt-8 grid gap-4 md:grid-cols-2">
            {t.restrictedCards.map(([title, text]) => (
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
            {t.customerProtectionTitle}
          </h2>

          <p className="mt-4 max-w-4xl text-slate-600">
            {t.customerProtectionText}
          </p>

          <div className="mt-6 grid gap-3 md:grid-cols-2">
            {t.customerProtectionItems.map((item) => (
              <div
                key={item}
                className="rounded-xl border border-slate-200 bg-slate-50 p-4 text-sm leading-6 text-slate-700"
              >
                {item}
              </div>
            ))}
          </div>
        </section>

        <section className="rounded-[2rem] border border-white/10 bg-white p-8 shadow-xl md:p-10">
          <h2 className="text-2xl font-bold text-slate-950">
            {t.aiTitle}
          </h2>

          <p className="mt-4 max-w-4xl text-slate-600">
            {t.aiText}
          </p>

          <div className="mt-6 grid gap-3 md:grid-cols-2">
            {t.aiItems.map((item) => (
              <div
                key={item}
                className="rounded-xl border border-slate-200 bg-slate-50 p-4 text-sm leading-6 text-slate-700"
              >
                {item}
              </div>
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

          <div className="mt-6 grid gap-3 md:grid-cols-2">
            {t.responsibilityItems.map((item) => (
              <div
                key={item}
                className="rounded-xl border border-slate-200 bg-slate-50 p-4 text-sm leading-6 text-slate-700"
              >
                {item}
              </div>
            ))}
          </div>
        </section>

        <section className="rounded-[2rem] border border-white/10 bg-white p-8 shadow-xl md:p-10">
          <h2 className="text-2xl font-bold text-slate-950">
            {t.enforcementTitle}
          </h2>

          <p className="mt-4 max-w-4xl text-slate-600">
            {t.enforcementText}
          </p>

          <div className="mt-8 grid gap-4 md:grid-cols-4">
            {t.enforcementCards.map(([title, text]) => (
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
          <h1 className="text-3xl font-bold text-slate-950">
            {t.title}
          </h1>

          <p className="mt-2 text-sm text-slate-500">
            {t.updated}
          </p>

          <div className="mt-8 space-y-8">
            <section>
              <h2 className="text-xl font-semibold text-slate-950">
                {t.reportingTitle}
              </h2>

              <p className="mt-2 whitespace-normal break-words text-slate-600">
                {t.reportingText}
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-slate-950">
                {t.changesTitle}
              </h2>

              <p className="mt-2 whitespace-normal break-words text-slate-600">
                {t.changesText}
              </p>
            </section>
          </div>
        </section>
      </div>
    </main>
  );
}
