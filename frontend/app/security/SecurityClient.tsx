"use client";

import { useEffect, useState } from "react";
import {
  defaultLocale,
  getSavedLocale,
} from "../../lib/i18n";

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

const securityCopy = {
  en: {
    title: "Security & Data Handling",
    updated: "Last updated: June 2026",
    eyebrow: "Trust by design",
    heroTitle: "Built for sensitive documents.",
    heroText:
      "Runexa is designed to process contracts, financial documents, study materials, and business files with privacy-focused controls. Uploaded files are used to generate the requested analysis, personal identifiers are anonymized before AI processing, customer content is not used to train public AI models, and uploaded files are removed from processing storage after analysis.",
    primaryCta: "Contact Runexa",
    secondaryCta: "Read Privacy Policy",

    flowTitle: "How Runexa handles your files",
    flowSubtitle:
      "A clear processing flow designed to reduce unnecessary exposure of sensitive information.",
    flow: [
      ["1", "Upload", "You upload a document for a selected AI agent."],
      ["2", "Extract", "Runexa extracts the text needed for analysis."],
      ["3", "Protect", "Personal identifiers are replaced with neutral placeholders before AI processing."],
      ["4", "Analyze", "AI systems generate the requested report or insight."],
      ["5", "Delete file", "The uploaded file is removed from processing storage after analysis."],
    ],

    commitmentsTitle: "Core security commitments",
    commitments: [
      {
        title: "No public model training",
        text:
          "Customer-uploaded documents, financial records, contracts, study materials, and business files are not used to train public AI models.",
      },
      {
        title: "Privacy protection before AI analysis",
        text:
          "Personal identifiers such as names, email addresses, phone numbers, organization names, and any other information that could identify an individual or entity are replaced with neutral placeholders before AI processing.",
      },
      {
        title: "Automatic file deletion",
        text:
          "Uploaded files are removed from processing storage after the requested analysis is completed. Generated results may remain available in the user workspace unless deleted or otherwise required for operational, billing, security, or legal reasons.",
      },
      {
        title: "Workspace isolation",
        text:
          "Customer data is logically isolated across users and workspaces. No user can access another user’s analysis results through the platform.",
      },
      {
        title: "Limited operational access",
        text:
          "Runexa personnel do not access customer documents. Uploaded files are used solely to generate the requested analysis and are automatically deleted from processing storage once the analysis is complete.",
      },
      {
        title: "Secure infrastructure",
        text:
          "Runexa uses cloud, database, payment, and AI infrastructure providers to operate the platform, with safeguards designed to protect accounts, uploads, analysis workflows, and platform integrity.",
      },
    ],

    piiTitle: "Examples of privacy protection",
    piiText:
      "Before AI analysis, Runexa transforms direct identifiers and any other information that could identify an individual or entity into neutral placeholders. This allows the AI to analyze the document’s content and structure without access to the real identity of the parties involved.",
    examples: [
      ["John Smith", "[PERSON]"],
      ["Acme Corporation", "[ORGANIZATION]"],
      ["john@example.com", "[EMAIL]"],
      ["+1 555 123 4567", "[PHONE]"],
    ],

    aiTitle: "AI processing and limitations",
    aiText:
      "Runexa uses AI-assisted systems to extract, classify, summarize, analyze, and generate outputs. AI results may be incomplete or inaccurate and should be independently reviewed before important legal, financial, educational, or business decisions.",
    responsibleTitle: "Responsible uploads",
    responsibleText:
      "Users should upload only information reasonably necessary for the requested analysis and should avoid including unrelated sensitive data.",
    paymentsTitle: "Payment security",
    paymentsText:
      "Payments are processed by Stripe, a secure third-party payment provider. Runexa does not store payment card information on its own servers.",
    reportingTitle: "Reporting security issues",
    reportingText:
      "Security concerns, suspected abuse, or vulnerability reports may be sent to:",
    guaranteeTitle: "No absolute security guarantee",
    guaranteeText:
      "No internet-based platform, software system, AI system, or storage system can be guaranteed to be completely secure. Runexa implements reasonable safeguards, but users should always use appropriate judgment when uploading sensitive content.",
  },

  fr: {
    title: "Sécurité et traitement des données",
    updated: "Dernière mise à jour : juin 2026",
    eyebrow: "Confiance dès la conception",
    heroTitle: "Conçu pour les documents sensibles.",
    heroText:
      "Runexa est conçu pour traiter des contrats, documents financiers, supports d’apprentissage et fichiers professionnels avec des contrôles orientés confidentialité. Les fichiers importés sont utilisés pour générer l’analyse demandée, les identifiants personnels sont anonymisés avant le traitement IA, les contenus clients ne servent pas à entraîner des modèles IA publics, et les fichiers importés sont supprimés du stockage de traitement après analyse.",
    primaryCta: "Contacter Runexa",
    secondaryCta: "Lire la politique de confidentialité",

    flowTitle: "Comment Runexa traite vos fichiers",
    flowSubtitle:
      "Un flux de traitement clair, conçu pour réduire l’exposition inutile des informations sensibles.",
    flow: [
      ["1", "Import", "Vous importez un document pour un agent IA sélectionné."],
      ["2", "Extraction", "Runexa extrait le texte nécessaire à l’analyse."],
      ["3", "Protection", "Les identifiants personnels sont remplacés par des libellés neutres avant le traitement par l’IA."],
      ["4", "Analyse IA", "Les systèmes IA génèrent le rapport ou l’insight demandé."],
      ["5", "Suppression", "Le fichier importé est supprimé du stockage de traitement après analyse."],
    ],

    commitmentsTitle: "Engagements de sécurité principaux",
    commitments: [
      {
        title: "Pas d’entraînement de modèles publics",
        text:
          "Les documents clients, relevés financiers, contrats, supports d’apprentissage et fichiers professionnels importés ne servent pas à entraîner des modèles IA publics.",
      },
      {
        title: "Protection avant l’analyse IA",
        text:
          "Les identifiants personnels tels que les noms, adresses e-mail, numéros de téléphone, noms d’organisations et toute autre information permettant d’identifier une personne ou une entité sont remplacés par des libellés neutres avant le traitement par l’IA.",
      },
      {
        title: "Suppression automatique des fichiers",
        text:
          "Les fichiers importés sont supprimés du stockage de traitement une fois l’analyse demandée terminée. Les résultats générés peuvent rester disponibles dans l’espace utilisateur, sauf suppression ou nécessité opérationnelle, de facturation, de sécurité ou légale.",
      },
      {
        title: "Isolation des espaces",
        text:
          "Les données clients sont logiquement isolées entre les utilisateurs et les espaces de travail. Aucun utilisateur ne peut accéder aux résultats d’analyse appartenant à un autre utilisateur via la plateforme.",
      },
      {
        title: "Accès opérationnel limité",
        text:
          "Les équipes Runexa ne consultent pas les documents clients. Les fichiers importés sont utilisés uniquement pour générer l’analyse demandée puis sont automatiquement supprimés du stockage de traitement une fois l’analyse terminée.",
      },
      {
        title: "Infrastructure sécurisée",
        text:
          "Runexa utilise des fournisseurs cloud, base de données, paiement et IA pour opérer la plateforme, avec des mesures conçues pour protéger les comptes, imports, workflows d’analyse et l’intégrité de la plateforme.",
      },
    ],

    piiTitle: "Exemples de protection de la confidentialité",
    piiText:
      "Avant l’analyse par l’IA, Runexa transforme les identifiants directs et toute autre information permettant d’identifier une personne ou une entité en libellés neutres. L’IA analyse ainsi le contenu et la structure du document sans avoir accès à l’identité réelle des parties concernées.",
    examples: [
      ["Jean Dupont", "[PERSON]"],
      ["Société Exemple SAS", "[ORGANIZATION]"],
      ["jean@example.com", "[EMAIL]"],
      ["+33 6 12 34 56 78", "[PHONE]"],
    ],

    aiTitle: "Traitement IA et limites",
    aiText:
      "Runexa utilise des systèmes assistés par IA pour extraire, classifier, résumer, analyser et générer des résultats. Les résultats IA peuvent être incomplets ou inexacts et doivent être vérifiés indépendamment avant toute décision juridique, financière, éducative ou professionnelle importante.",
    responsibleTitle: "Imports responsables",
    responsibleText:
      "Les utilisateurs doivent importer uniquement les informations raisonnablement nécessaires à l’analyse demandée et éviter d’inclure des données sensibles non pertinentes.",
    paymentsTitle: "Sécurité des paiements",
    paymentsText:
      "Les paiements sont traités par Stripe, prestataire de paiement tiers sécurisé. Runexa ne stocke pas les informations de carte bancaire sur ses propres serveurs.",
    reportingTitle: "Signaler un problème de sécurité",
    reportingText:
      "Les préoccupations de sécurité, abus suspectés ou rapports de vulnérabilité peuvent être envoyés à :",
    guaranteeTitle: "Aucune garantie de sécurité absolue",
    guaranteeText:
      "Aucune plateforme internet, aucun logiciel, système IA ou système de stockage ne peut être garanti comme totalement sécurisé. Runexa met en œuvre des mesures raisonnables, mais les utilisateurs doivent toujours faire preuve de discernement lorsqu’ils importent du contenu sensible.",
  },

  ar: {
    title: "الأمان ومعالجة البيانات",
    updated: "آخر تحديث: يونيو 2026",
    eyebrow: "الثقة منذ التصميم",
    heroTitle: "مصمم للمستندات الحساسة.",
    heroText:
      "تم تصميم Runexa لمعالجة العقود والمستندات المالية ومواد الدراسة وملفات الأعمال مع ضوابط تركّز على الخصوصية. تُستخدم الملفات المرفوعة لإنشاء التحليل المطلوب، ويتم إخفاء الهوية عن المعرّفات الشخصية قبل المعالجة بالذكاء الاصطناعي، ولا تُستخدم محتويات العملاء لتدريب نماذج ذكاء اصطناعي عامة، ويتم حذف الملفات المرفوعة من تخزين المعالجة بعد اكتمال التحليل.",
    primaryCta: "تواصل مع Runexa",
    secondaryCta: "قراءة سياسة الخصوصية",

    flowTitle: "كيف يعالج Runexa ملفاتك",
    flowSubtitle:
      "مسار معالجة واضح مصمم لتقليل التعرض غير الضروري للمعلومات الحساسة.",
    flow: [
      ["1", "رفع", "ترفع مستنداً لاستخدامه مع وكيل ذكاء اصطناعي محدد."],
      ["2", "استخراج", "يستخرج Runexa النص اللازم للتحليل."],
      ["3", "حماية", "يتم استبدال المعرّفات الشخصية بتسميات محايدة قبل المعالجة بالذكاء الاصطناعي."],
      ["4", "تحليل IA", "تنشئ أنظمة الذكاء الاصطناعي التقرير أو النتيجة المطلوبة."],
      ["5", "حذف الملف", "يتم حذف الملف المرفوع من تخزين المعالجة بعد التحليل."],
    ],

    commitmentsTitle: "التزامات الأمان الأساسية",
    commitments: [
      {
        title: "لا تدريب لنماذج عامة",
        text:
          "لا تُستخدم مستندات العملاء أو السجلات المالية أو العقود أو مواد الدراسة أو ملفات الأعمال المرفوعة لتدريب نماذج ذكاء اصطناعي عامة.",
      },
      {
        title: "حماية الخصوصية قبل التحليل",
        text:
        "يتم استبدال المعرّفات الشخصية، مثل الأسماء وعناوين البريد الإلكتروني وأرقام الهواتف وأسماء المؤسسات، وأي معلومات أخرى يمكن أن تُستخدم لتحديد هوية شخص أو كيان، بعلامات تعريف محايدة قبل المعالجة بالذكاء الاصطناعي.",
      },
            {
        title: "حذف تلقائي للملفات",
        text:
          "تُحذف الملفات المرفوعة من تخزين المعالجة بعد اكتمال التحليل المطلوب. وقد تبقى النتائج المولدة متاحة في مساحة المستخدم ما لم يتم حذفها أو يلزم الاحتفاظ بها لأسباب تشغيلية أو متعلقة بالفوترة أو الأمان أو الالتزامات القانونية.",
      },
      {
        title: "عزل مساحات العمل",
        text:
          "يتم عزل بيانات العملاء منطقياً بين المستخدمين ومساحات العمل. ولا يمكن لأي مستخدم الوصول إلى نتائج التحليل الخاصة بمستخدم آخر عبر المنصة.",
      },
      {
        title: "وصول تشغيلي محدود",
        text:
          "لا يطّلع فريق Runexa على مستندات العملاء. تُستخدم الملفات المرفوعة حصرياً لإنشاء التحليل المطلوب، ثم تُحذف تلقائياً من مساحة تخزين المعالجة فور اكتمال التحليل.",
      },
      {
        title: "بنية تحتية آمنة",
        text:
          "يستخدم Runexa مزودي بنية تحتية سحابية وقواعد بيانات ودفع وذكاء اصطناعي لتشغيل المنصة، مع ضوابط مصممة لحماية الحسابات والملفات وسير عمل التحليل وسلامة المنصة.",
      },
    ],

    piiTitle: "أمثلة على حماية الخصوصية",
    piiText:
      "قبل التحليل بالذكاء الاصطناعي، تقوم Runexa بتحويل المعرّفات المباشرة وأي معلومات أخرى يمكن أن تُستخدم لتحديد هوية شخص أو كيان إلى علامات تعريف محايدة. وبذلك يتمكن الذكاء الاصطناعي من تحليل محتوى المستند وبنيته دون الوصول إلى الهوية الحقيقية للأطراف المعنية.",
    examples: [
      ["محمد علي", "[PERSON]"],
      ["شركة المثال", "[ORGANIZATION]"],
      ["user@example.com", "[EMAIL]"],
      ["+212 600 000 000", "[PHONE]"],
    ],

    aiTitle: "معالجة الذكاء الاصطناعي وحدودها",
    aiText:
      "يستخدم Runexa أنظمة مدعومة بالذكاء الاصطناعي لاستخراج المعلومات وتصنيفها وتلخيصها وتحليلها وإنشاء النتائج. قد تكون مخرجات الذكاء الاصطناعي غير مكتملة أو غير دقيقة، ويجب مراجعتها بشكل مستقل قبل اتخاذ قرارات قانونية أو مالية أو تعليمية أو مهنية مهمة.",
    responsibleTitle: "رفع مسؤول للملفات",
    responsibleText:
      "يجب على المستخدمين رفع المعلومات الضرورية فقط وبشكل معقول للتحليل المطلوب، وتجنب تضمين بيانات حساسة غير مرتبطة بالتحليل.",
    paymentsTitle: "أمان المدفوعات",
    paymentsText:
      "تتم معالجة المدفوعات عبر Stripe، وهو مزود دفع خارجي آمن. ولا تخزن Runexa معلومات بطاقة الدفع على خوادمها الخاصة.",
    reportingTitle: "الإبلاغ عن مشكلات الأمان",
    reportingText:
      "يمكن إرسال المخاوف الأمنية أو الاشتباه في إساءة الاستخدام أو تقارير الثغرات إلى:",
    guaranteeTitle: "لا توجد ضمانة أمان مطلقة",
    guaranteeText:
      "لا يمكن ضمان أن أي منصة قائمة على الإنترنت أو برنامج أو نظام ذكاء اصطناعي أو نظام تخزين آمن بالكامل. يطبق Runexa إجراءات حماية معقولة، لكن يجب على المستخدمين دائماً استخدام الحكم المناسب عند رفع محتوى حساس.",
  },
} satisfies Record<Locale, {
  title: string;
  updated: string;
  eyebrow: string;
  heroTitle: string;
  heroText: string;
  primaryCta: string;
  secondaryCta: string;
  flowTitle: string;
  flowSubtitle: string;
  flow: string[][];
  commitmentsTitle: string;
  commitments: { title: string; text: string }[];
  piiTitle: string;
  piiText: string;
  examples: string[][];
  aiTitle: string;
  aiText: string;
  responsibleTitle: string;
  responsibleText: string;
  paymentsTitle: string;
  paymentsText: string;
  reportingTitle: string;
  reportingText: string;
  guaranteeTitle: string;
  guaranteeText: string;
}>;

export default function SecurityClient({
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

  const t = securityCopy[locale];

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
                  href="/privacy"
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
                {t.flowTitle}
              </h2>

              <p className="mt-3 text-sm leading-6 text-slate-300">
                {t.flowSubtitle}
              </p>

              <div className="mt-8 space-y-4">
                {t.flow.map(([number, title, text]) => (
                  <div
                    key={`${number}-${title}`}
                    className="flex gap-4 rounded-2xl border border-white/10 bg-white/5 p-4"
                  >
                    <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-blue-500 text-sm font-bold text-white">
                      {number}
                    </div>

                    <div>
                      <p className="font-semibold text-white">
                        {title}
                      </p>

                      <p className="mt-1 text-sm leading-6 text-slate-300">
                        {text}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        <section className="rounded-[2rem] border border-white/10 bg-white p-8 shadow-xl md:p-10">
          <h2 className="text-2xl font-bold text-slate-950">
            {t.commitmentsTitle}
          </h2>

          <div className="mt-8 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
            {t.commitments.map((item) => (
              <article
                key={item.title}
                className="rounded-2xl border border-slate-200 bg-slate-50 p-5"
              >
                <h3 className="font-semibold text-slate-950">
                  {item.title}
                </h3>

                <p className="mt-3 text-sm leading-6 text-slate-600">
                  {item.text}
                </p>
              </article>
            ))}
          </div>
        </section>

        <section className="grid gap-8 lg:grid-cols-2">
          <div className="rounded-[2rem] border border-white/10 bg-white p-8 shadow-xl md:p-10">
            <h2 className="text-2xl font-bold text-slate-950">
              {t.piiTitle}
            </h2>

            <p className="mt-3 text-sm leading-6 text-slate-600">
              {t.piiText}
            </p>

            <div className="mt-6 space-y-3">
              {t.examples.map(([before, after]) => (
                <div
                  key={`${before}-${after}`}
                  className="flex items-center justify-between gap-4 rounded-2xl border border-slate-200 bg-slate-50 p-4"
                >
                  <span className="break-all text-sm text-slate-700">
                    {before}
                  </span>

                  <span className="text-slate-400">→</span>

                  <span className="rounded-lg bg-slate-950 px-3 py-1 text-sm font-semibold text-white">
                    {after}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="space-y-8">
            <section className="rounded-[2rem] border border-white/10 bg-white p-8 shadow-xl md:p-10">
              <h2 className="text-2xl font-bold text-slate-950">
                {t.aiTitle}
              </h2>

              <p className="mt-3 text-sm leading-6 text-slate-600">
                {t.aiText}
              </p>
            </section>

            <section className="rounded-[2rem] border border-white/10 bg-white p-8 shadow-xl md:p-10">
              <h2 className="text-2xl font-bold text-slate-950">
                {t.responsibleTitle}
              </h2>

              <p className="mt-3 text-sm leading-6 text-slate-600">
                {t.responsibleText}
              </p>
            </section>
          </div>
        </section>

        <section className="grid gap-8 lg:grid-cols-3">
          <article className="rounded-[2rem] border border-white/10 bg-white p-8 shadow-xl">
            <h2 className="text-xl font-bold text-slate-950">
              {t.paymentsTitle}
            </h2>

            <p className="mt-3 text-sm leading-6 text-slate-600">
              {t.paymentsText}
            </p>
          </article>

          <article className="rounded-[2rem] border border-white/10 bg-white p-8 shadow-xl">
            <h2 className="text-xl font-bold text-slate-950">
              {t.reportingTitle}
            </h2>

            <p className="mt-3 text-sm leading-6 text-slate-600">
              {t.reportingText}
            </p>

            <p className="mt-3 text-sm font-semibold text-blue-600">
              contact@runexa.ai
            </p>
          </article>

          <article className="rounded-[2rem] border border-white/10 bg-white p-8 shadow-xl">
            <h2 className="text-xl font-bold text-slate-950">
              {t.guaranteeTitle}
            </h2>

            <p className="mt-3 text-sm leading-6 text-slate-600">
              {t.guaranteeText}
            </p>
          </article>
        </section>
      </div>
    </main>
  );
}
