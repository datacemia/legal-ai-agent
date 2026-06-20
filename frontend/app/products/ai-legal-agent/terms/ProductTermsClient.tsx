"use client";

import { useEffect, useState } from "react";
import { defaultLocale, getSavedLocale } from "../../../../lib/i18n";

const productTermsTranslations: any = {
  en: {
    title: "Runexa Systems LLC — Product Terms",
    updated: "Last updated: April 2026",
    intro:
      "These Product Terms apply to AI agents and services provided by Runexa Systems LLC through the Runexa platform.",

    legalTitle: "Runexa Legal Agent",
    studyTitle: "Runexa Study Agent",
    financeTitle: "Runexa Finance Coach",
    businessTitle: "Runexa Business Decision Agent",

    descriptionTitle: "1. Description",
    legalDescription1:
      "The Runexa Legal Agent is an AI-powered tool designed to assist users in reviewing legal documents, identifying potential risks, and generating simplified explanations.",
    legalDescription2:
      "It is part of the Runexa platform of specialized AI agents.",

    legalAdviceTitle: "2. No Legal Advice",
    legalAdvice1:
      "The Runexa Legal Agent is not a law firm and does not provide legal advice.",
    legalAdvice2:
      "Outputs should not be considered a substitute for professional legal counsel.",

    accuracyTitle: "3. Accuracy Disclaimer",
    legalAccuracy1: "May misinterpret clauses",
    legalAccuracy2: "May miss important risks",
    legalAccuracy3: "May provide incomplete summaries",

    userResponsibilityTitle: "4. User Responsibility",
    legalResponsibility:
      "Users are responsible for reviewing all outputs, making their own legal decisions, and consulting qualified professionals when necessary.",

    highRiskTitle: "5. High-Risk Use",
    legalHighRisk:
      "Do not rely solely on this tool for contracts, legal disputes, financial decisions, or other high-impact matters.",

    liabilityTitle: "6. Liability Limitation",
    legalLiability:
      "Runexa Systems LLC is not responsible for legal disputes, contract issues, financial losses, or legal consequences resulting from AI outputs.",

    studyDescription:
      "The Runexa Study Agent is an AI-powered tool designed to help users analyze study materials, generate summaries, create quizzes, and build revision plans.",

    studyGuaranteeTitle: "2. No Educational Guarantee",
    studyGuarantee:
      "The Runexa Study Agent does not guarantee academic success, exam results, grades, admissions, or certifications.",

    studyAccuracy1: "May summarize content incorrectly",
    studyAccuracy2: "May generate inaccurate quizzes or explanations",
    studyAccuracy3: "May provide incomplete learning recommendations",

    studyResponsibility:
      "Users are responsible for verifying educational content and using official learning materials where necessary.",

    studyIntegrityTitle: "5. Academic Integrity",
    studyIntegrity:
      "Users must not use the Runexa Study Agent to cheat, plagiarize, or violate academic rules or institutional policies.",

    studyLiability:
      "Runexa Systems LLC is not responsible for academic penalties, poor grades, failed exams, or educational outcomes resulting from AI outputs.",

    financeDescription:
      "The Runexa Finance Coach is an AI-powered tool designed to help users analyze expenses, identify spending patterns, and generate saving suggestions.",

    financeAdviceTitle: "2. No Financial Advice",
    financeAdvice:
      "The Runexa Finance Coach does not provide financial, tax, accounting, investment, or legal advice.",

    financeAccuracy1: "May misclassify transactions",
    financeAccuracy2: "May miss important financial context",
    financeAccuracy3: "May provide incomplete recommendations",

    financeHighRiskTitle: "4. High-Risk Use",
    financeHighRisk:
      "Do not rely solely on this tool for investments, taxes, loans, retirement planning, or other major financial decisions.",

    financeLiabilityTitle: "5. Liability Limitation",
    financeLiability:
      "Runexa Systems LLC is not responsible for financial losses, tax issues, missed payments, or financial consequences resulting from AI outputs.",

    businessDescription:
      "The Runexa Business Decision Agent is an AI-powered tool designed to help users analyze business information, detect trends, and support strategic decision-making.",

    businessAdviceTitle: "2. No Professional Advice",
    businessAdvice:
      "The Runexa Business Decision Agent does not provide legal, accounting, tax, financial, or management consulting advice.",

    businessAccuracy1: "May misinterpret business data",
    businessAccuracy2: "May miss market risks or operational issues",
    businessAccuracy3: "May generate incomplete recommendations",

    businessResponsibility:
      "Users are responsible for validating outputs and making their own operational and strategic business decisions.",

    businessHighRisk:
      "Do not rely solely on this tool for investments, hiring decisions, financing, acquisitions, legal disputes, or other high-impact business matters.",

    businessLiability:
      "Runexa Systems LLC is not responsible for business losses, operational issues, financial damages, or legal consequences resulting from AI outputs.",

    additionalTermsTitle: "Additional AI Terms",

    humanReviewTitle: "7. Human Review Required",
    humanReview:
      "Users must independently review, verify, and validate all AI-generated outputs before relying on them or taking action.",

    dataProcessingTitle: "8. Data Processing",
    dataProcessing:
      "Uploaded files may be processed by AI systems and infrastructure providers solely to provide the requested analysis and related functionality in accordance with the Privacy Policy.",

    trainingTitle: "9. Model Training",
    trainingText:
      "User-uploaded content is not used to train proprietary AI models unless explicitly disclosed and permitted by applicable law.",

    transparencyTitle: "10. AI Transparency",
    transparencyText:
      "Users are interacting with AI-generated systems. Outputs are generated by machine-learning models and may contain errors, omissions, inaccurate interpretations, or incomplete information.",

    enterpriseTitle: "11. Enterprise Use",
    enterpriseText:
      "Organizations remain responsible for their own compliance, governance, security reviews, internal approvals, and regulatory obligations when using Runexa services.",
  },

  fr: {
    title: "Runexa Systems LLC — Conditions produit",
    updated: "Dernière mise à jour : avril 2026",
    intro:
      "Ces Conditions produit s’appliquent aux agents IA et services fournis par Runexa Systems LLC via la plateforme Runexa.",

    legalTitle: "Agent juridique Runexa",
    studyTitle: "Agent étude Runexa",
    financeTitle: "Coach financier Runexa",
    businessTitle: "Agent de décision business Runexa",

    descriptionTitle: "1. Description",
    legalDescription1:
      "L’Agent juridique Runexa est un outil alimenté par l’IA conçu pour aider les utilisateurs à examiner des documents juridiques, identifier des risques potentiels et générer des explications simplifiées.",
    legalDescription2:
      "Il fait partie de la plateforme Runexa d’agents IA spécialisés.",

    legalAdviceTitle: "2. Absence de conseil juridique",
    legalAdvice1:
      "L’Agent juridique Runexa n’est pas un cabinet d’avocats et ne fournit pas de conseil juridique.",
    legalAdvice2:
      "Les résultats ne doivent pas être considérés comme un substitut à un conseil juridique professionnel.",

    accuracyTitle: "3. Avertissement sur l’exactitude",
    legalAccuracy1: "Peut mal interpréter certaines clauses",
    legalAccuracy2: "Peut manquer des risques importants",
    legalAccuracy3: "Peut fournir des résumés incomplets",

    userResponsibilityTitle: "4. Responsabilité de l’utilisateur",
    legalResponsibility:
      "Les utilisateurs sont responsables de l’examen de tous les résultats, de leurs propres décisions juridiques et de la consultation de professionnels qualifiés si nécessaire.",

    highRiskTitle: "5. Utilisation à haut risque",
    legalHighRisk:
      "Ne vous fiez pas uniquement à cet outil pour des contrats, litiges juridiques, décisions financières ou autres sujets à fort impact.",

    liabilityTitle: "6. Limitation de responsabilité",
    legalLiability:
      "Runexa Systems LLC n’est pas responsable des litiges juridiques, problèmes contractuels, pertes financières ou conséquences juridiques résultant des sorties IA.",

    studyDescription:
      "L’Agent étude Runexa est un outil alimenté par l’IA conçu pour aider les utilisateurs à analyser des supports d’étude, générer des résumés, créer des quiz et construire des plans de révision.",

    studyGuaranteeTitle: "2. Aucune garantie éducative",
    studyGuarantee:
      "L’Agent étude Runexa ne garantit pas la réussite académique, les résultats d’examen, les notes, les admissions ou les certifications.",

    studyAccuracy1: "Peut résumer le contenu de manière incorrecte",
    studyAccuracy2: "Peut générer des quiz ou explications inexacts",
    studyAccuracy3:
      "Peut fournir des recommandations d’apprentissage incomplètes",

    studyResponsibility:
      "Les utilisateurs sont responsables de vérifier le contenu éducatif et d’utiliser les supports officiels lorsque nécessaire.",

    studyIntegrityTitle: "5. Intégrité académique",
    studyIntegrity:
      "Les utilisateurs ne doivent pas utiliser l’Agent étude Runexa pour tricher, plagier ou violer des règles académiques ou politiques institutionnelles.",

    studyLiability:
      "Runexa Systems LLC n’est pas responsable des sanctions académiques, mauvaises notes, examens échoués ou résultats éducatifs découlant des sorties IA.",

    financeDescription:
      "Le Coach financier Runexa est un outil alimenté par l’IA conçu pour aider les utilisateurs à analyser leurs dépenses, identifier des habitudes de dépense et générer des suggestions d’épargne.",

    financeAdviceTitle: "2. Absence de conseil financier",
    financeAdvice:
      "Le Coach financier Runexa ne fournit pas de conseil financier, fiscal, comptable, d’investissement ou juridique.",

    financeAccuracy1: "Peut mal classer des transactions",
    financeAccuracy2: "Peut manquer un contexte financier important",
    financeAccuracy3: "Peut fournir des recommandations incomplètes",

    financeHighRiskTitle: "4. Utilisation à haut risque",
    financeHighRisk:
      "Ne vous fiez pas uniquement à cet outil pour les investissements, impôts, prêts, planification de retraite ou autres décisions financières majeures.",

    financeLiabilityTitle: "5. Limitation de responsabilité",
    financeLiability:
      "Runexa Systems LLC n’est pas responsable des pertes financières, problèmes fiscaux, paiements manqués ou conséquences financières résultant des sorties IA.",

    businessDescription:
      "L’Agent de décision business Runexa est un outil alimenté par l’IA conçu pour aider les utilisateurs à analyser des informations business, détecter des tendances et soutenir la prise de décision stratégique.",

    businessAdviceTitle: "2. Absence de conseil professionnel",
    businessAdvice:
      "L’Agent de décision business Runexa ne fournit pas de conseil juridique, comptable, fiscal, financier ou en management.",

    businessAccuracy1: "Peut mal interpréter des données business",
    businessAccuracy2:
      "Peut manquer des risques de marché ou problèmes opérationnels",
    businessAccuracy3: "Peut générer des recommandations incomplètes",

    businessResponsibility:
      "Les utilisateurs sont responsables de valider les résultats et de prendre leurs propres décisions opérationnelles et stratégiques.",

    businessHighRisk:
      "Ne vous fiez pas uniquement à cet outil pour les investissements, décisions d’embauche, financements, acquisitions, litiges juridiques ou autres sujets business à fort impact.",

    businessLiability:
      "Runexa Systems LLC n’est pas responsable des pertes business, problèmes opérationnels, dommages financiers ou conséquences juridiques résultant des sorties IA.",

    additionalTermsTitle: "Conditions IA supplémentaires",

    humanReviewTitle: "7. Vérification humaine requise",
    humanReview:
      "Les utilisateurs doivent examiner, vérifier et valider de manière indépendante tous les résultats générés par l’IA avant de s’y fier ou de prendre une décision.",

    dataProcessingTitle: "8. Traitement des données",
    dataProcessing:
      "Les fichiers téléchargés peuvent être traités par des systèmes d’intelligence artificielle et des fournisseurs d’infrastructure uniquement afin de fournir l’analyse demandée et les fonctionnalités associées conformément à la Politique de confidentialité.",

    trainingTitle: "9. Entraînement des modèles",
    trainingText:
      "Le contenu téléchargé par les utilisateurs n’est pas utilisé pour entraîner des modèles d’IA propriétaires sauf indication contraire explicite et lorsque la loi applicable le permet.",

    transparencyTitle: "10. Transparence de l’IA",
    transparencyText:
      "Les utilisateurs interagissent avec des systèmes générés par intelligence artificielle. Les résultats sont produits par des modèles d’apprentissage automatique et peuvent contenir des erreurs, omissions, interprétations inexactes ou informations incomplètes.",

    enterpriseTitle: "11. Utilisation entreprise",
    enterpriseText:
      "Les organisations restent responsables de leur propre conformité, gouvernance, vérification de sécurité, approbations internes et obligations réglementaires lorsqu’elles utilisent les services Runexa.",
  },

  ar: {
    title: "Runexa Systems LLC — شروط المنتج",
    updated: "آخر تحديث: أبريل 2026",
    intro:
      "تنطبق شروط المنتج هذه على وكلاء الذكاء الاصطناعي والخدمات المقدمة من Runexa Systems LLC عبر منصة Runexa.",

    legalTitle: "وكيل Runexa القانوني",
    studyTitle: "وكيل Runexa للدراسة",
    financeTitle: "مدرب Runexa المالي",
    businessTitle: "وكيل Runexa لقرارات الأعمال",

    descriptionTitle: "1. الوصف",
    legalDescription1:
      "وكيل Runexa القانوني هو أداة مدعومة بالذكاء الاصطناعي مصممة لمساعدة المستخدمين في مراجعة المستندات القانونية وتحديد المخاطر المحتملة وإنشاء تفسيرات مبسطة.",
    legalDescription2:
      "وهو جزء من منصة Runexa لوكلاء الذكاء الاصطناعي المتخصصين.",

    legalAdviceTitle: "2. لا توجد نصيحة قانونية",
    legalAdvice1:
      "وكيل Runexa القانوني ليس مكتب محاماة ولا يقدم نصائح قانونية.",
    legalAdvice2:
      "لا ينبغي اعتبار المخرجات بديلاً عن الاستشارة القانونية المهنية.",

    accuracyTitle: "3. إخلاء مسؤولية الدقة",
    legalAccuracy1: "قد يسيء تفسير البنود",
    legalAccuracy2: "قد يغفل مخاطر مهمة",
    legalAccuracy3: "قد يقدم ملخصات غير مكتملة",

    userResponsibilityTitle: "4. مسؤولية المستخدم",
    legalResponsibility:
      "المستخدمون مسؤولون عن مراجعة جميع المخرجات واتخاذ قراراتهم القانونية الخاصة واستشارة المتخصصين المؤهلين عند الحاجة.",

    highRiskTitle: "5. الاستخدام عالي المخاطر",
    legalHighRisk:
      "لا تعتمد على هذه الأداة وحدها في العقود أو النزاعات القانونية أو القرارات المالية أو غيرها من المسائل عالية التأثير.",

    liabilityTitle: "6. تحديد المسؤولية",
    legalLiability:
      "لا تتحمل Runexa Systems LLC مسؤولية النزاعات القانونية أو مشكلات العقود أو الخسائر المالية أو العواقب القانونية الناتجة عن مخرجات الذكاء الاصطناعي.",

    studyDescription:
      "وكيل Runexa للدراسة هو أداة مدعومة بالذكاء الاصطناعي مصممة لمساعدة المستخدمين على تحليل مواد الدراسة وإنشاء ملخصات واختبارات وخطط مراجعة.",

    studyGuaranteeTitle: "2. لا توجد ضمانات تعليمية",
    studyGuarantee:
      "لا يضمن وكيل Runexa للدراسة النجاح الأكاديمي أو نتائج الامتحانات أو الدرجات أو القبول أو الشهادات.",

    studyAccuracy1: "قد يلخص المحتوى بشكل غير صحيح",
    studyAccuracy2: "قد ينشئ اختبارات أو تفسيرات غير دقيقة",
    studyAccuracy3: "قد يقدم توصيات تعلم غير مكتملة",

    studyResponsibility:
      "المستخدمون مسؤولون عن التحقق من المحتوى التعليمي واستخدام المواد التعليمية الرسمية عند الحاجة.",

    studyIntegrityTitle: "5. النزاهة الأكاديمية",
    studyIntegrity:
      "يجب ألا يستخدم المستخدمون وكيل Runexa للدراسة للغش أو الانتحال أو انتهاك القواعد الأكاديمية أو سياسات المؤسسات.",

    studyLiability:
      "لا تتحمل Runexa Systems LLC مسؤولية العقوبات الأكاديمية أو الدرجات الضعيفة أو الامتحانات الفاشلة أو النتائج التعليمية الناتجة عن مخرجات الذكاء الاصطناعي.",

    financeDescription:
      "مدرب Runexa المالي هو أداة مدعومة بالذكاء الاصطناعي مصممة لمساعدة المستخدمين على تحليل المصاريف وتحديد أنماط الإنفاق وإنشاء اقتراحات للتوفير.",

    financeAdviceTitle: "2. لا توجد نصيحة مالية",
    financeAdvice:
      "لا يقدم مدرب Runexa المالي نصائح مالية أو ضريبية أو محاسبية أو استثمارية أو قانونية.",

    financeAccuracy1: "قد يصنف المعاملات بشكل غير صحيح",
    financeAccuracy2: "قد يغفل سياقًا ماليًا مهمًا",
    financeAccuracy3: "قد يقدم توصيات غير مكتملة",

    financeHighRiskTitle: "4. الاستخدام عالي المخاطر",
    financeHighRisk:
      "لا تعتمد على هذه الأداة وحدها للاستثمارات أو الضرائب أو القروض أو تخطيط التقاعد أو غيرها من القرارات المالية الكبرى.",

    financeLiabilityTitle: "5. تحديد المسؤولية",
    financeLiability:
      "لا تتحمل Runexa Systems LLC مسؤولية الخسائر المالية أو المشكلات الضريبية أو المدفوعات الفائتة أو العواقب المالية الناتجة عن مخرجات الذكاء الاصطناعي.",

    businessDescription:
      "وكيل Runexa لقرارات الأعمال هو أداة مدعومة بالذكاء الاصطناعي مصممة لمساعدة المستخدمين على تحليل معلومات الأعمال واكتشاف الاتجاهات ودعم اتخاذ القرارات الاستراتيجية.",

    businessAdviceTitle: "2. لا توجد نصيحة مهنية",
    businessAdvice:
      "لا يقدم وكيل Runexa لقرارات الأعمال نصائح قانونية أو محاسبية أو ضريبية أو مالية أو استشارية إدارية.",

    businessAccuracy1: "قد يسيء تفسير بيانات الأعمال",
    businessAccuracy2: "قد يغفل مخاطر السوق أو المشكلات التشغيلية",
    businessAccuracy3: "قد ينشئ توصيات غير مكتملة",

    businessResponsibility:
      "المستخدمون مسؤولون عن التحقق من المخرجات واتخاذ قراراتهم التشغيلية والاستراتيجية الخاصة.",

    businessHighRisk:
      "لا تعتمد على هذه الأداة وحدها للاستثمارات أو قرارات التوظيف أو التمويل أو الاستحواذات أو النزاعات القانونية أو غيرها من مسائل الأعمال عالية التأثير.",

    businessLiability:
      "لا تتحمل Runexa Systems LLC مسؤولية خسائر الأعمال أو المشكلات التشغيلية أو الأضرار المالية أو العواقب القانونية الناتجة عن مخرجات الذكاء الاصطناعي.",

    additionalTermsTitle: "شروط إضافية للذكاء الاصطناعي",

    humanReviewTitle: "7. المراجعة البشرية مطلوبة",
    humanReview:
      "يجب على المستخدمين مراجعة جميع المخرجات التي ينتجها الذكاء الاصطناعي والتحقق منها بشكل مستقل قبل الاعتماد عليها أو اتخاذ أي إجراء.",

    dataProcessingTitle: "8. معالجة البيانات",
    dataProcessing:
      "قد تتم معالجة الملفات المرفوعة بواسطة أنظمة الذكاء الاصطناعي ومزودي البنية التحتية فقط لتقديم التحليل المطلوب والوظائف المرتبطة به وفقًا لسياسة الخصوصية.",

    trainingTitle: "9. تدريب النماذج",
    trainingText:
      "لا يتم استخدام المحتوى الذي يرفعه المستخدمون لتدريب نماذج الذكاء الاصطناعي الخاصة إلا إذا تم الإفصاح عن ذلك صراحةً وكان مسموحًا به بموجب القانون.",

    transparencyTitle: "10. شفافية الذكاء الاصطناعي",
    transparencyText:
      "يتفاعل المستخدمون مع أنظمة تعتمد على الذكاء الاصطناعي. قد تحتوي المخرجات التي يتم إنشاؤها بواسطة نماذج التعلم الآلي على أخطاء أو سهو أو تفسيرات غير دقيقة أو معلومات غير مكتملة.",

    enterpriseTitle: "11. استخدام المؤسسات",
    enterpriseText:
      "تظل المؤسسات مسؤولة عن امتثالها وحوكمتها ومراجعاتها الأمنية وموافقاتها الداخلية والتزاماتها التنظيمية عند استخدام خدمات Runexa.",
  },
};

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

export default function ProductTermsClient({
  initialLocale,
  lockInitialLocale = false,
}: {
  initialLocale?: Locale;
  lockInitialLocale?: boolean;
}) {
  const resolvedInitialLocale = normalizeLocale(initialLocale, normalizeLocale(defaultLocale));

  const [locale, setLocale] = useState<Locale>(resolvedInitialLocale);

  useEffect(() => {
    if (lockInitialLocale) {
      setLocale(resolvedInitialLocale);
      return;
    }

    setLocale(normalizeLocale(getSavedLocale(), resolvedInitialLocale));
  }, [resolvedInitialLocale, lockInitialLocale]);

  const t =
    productTermsTranslations[locale] ||
    productTermsTranslations[normalizeLocale(defaultLocale)];

  return (
    <main
      dir={locale === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-4 py-12"
    >
      <div className="max-w-3xl mx-auto bg-white p-8 rounded-3xl border shadow-sm space-y-14">
        <div>
          <h1 className="text-4xl font-bold text-slate-900">{t.title}</h1>

          <p className="text-sm text-slate-500 mt-2">{t.updated}</p>

          <p className="mt-4 text-slate-600">{t.intro}</p>
        </div>

        {/* LEGAL AGENT */}

        <div className="border-t pt-10">
          <h2 className="text-3xl font-bold text-slate-900">
            {t.legalTitle}
          </h2>
        </div>

        <section>
          <h3 className="text-xl font-semibold">{t.descriptionTitle}</h3>

          <p className="mt-2 text-slate-600">{t.legalDescription1}</p>

          <p className="mt-2 text-slate-600">{t.legalDescription2}</p>
        </section>

        <section>
          <h3 className="text-xl font-semibold">{t.legalAdviceTitle}</h3>

          <p className="mt-2 text-slate-600">{t.legalAdvice1}</p>

          <p className="mt-2 text-slate-600">{t.legalAdvice2}</p>
        </section>

        <section>
          <h3 className="text-xl font-semibold">{t.accuracyTitle}</h3>

          <ul className="mt-2 list-disc pl-5 text-slate-600 space-y-1">
            <li>{t.legalAccuracy1}</li>
            <li>{t.legalAccuracy2}</li>
            <li>{t.legalAccuracy3}</li>
          </ul>
        </section>

        <section>
          <h3 className="text-xl font-semibold">
            {t.userResponsibilityTitle}
          </h3>

          <p className="mt-2 text-slate-600">{t.legalResponsibility}</p>
        </section>

        <section>
          <h3 className="text-xl font-semibold">{t.highRiskTitle}</h3>

          <p className="mt-2 text-slate-600">{t.legalHighRisk}</p>
        </section>

        <section>
          <h3 className="text-xl font-semibold">{t.liabilityTitle}</h3>

          <p className="mt-2 text-slate-600">{t.legalLiability}</p>
        </section>

        {/* STUDY AGENT */}

        <div className="border-t pt-10">
          <h2 className="text-3xl font-bold text-slate-900">
            {t.studyTitle}
          </h2>
        </div>

        <section>
          <h3 className="text-xl font-semibold">{t.descriptionTitle}</h3>

          <p className="mt-2 text-slate-600">{t.studyDescription}</p>
        </section>

        <section>
          <h3 className="text-xl font-semibold">{t.studyGuaranteeTitle}</h3>

          <p className="mt-2 text-slate-600">{t.studyGuarantee}</p>
        </section>

        <section>
          <h3 className="text-xl font-semibold">{t.accuracyTitle}</h3>

          <ul className="mt-2 list-disc pl-5 text-slate-600 space-y-1">
            <li>{t.studyAccuracy1}</li>
            <li>{t.studyAccuracy2}</li>
            <li>{t.studyAccuracy3}</li>
          </ul>
        </section>

        <section>
          <h3 className="text-xl font-semibold">
            {t.userResponsibilityTitle}
          </h3>

          <p className="mt-2 text-slate-600">{t.studyResponsibility}</p>
        </section>

        <section>
          <h3 className="text-xl font-semibold">{t.studyIntegrityTitle}</h3>

          <p className="mt-2 text-slate-600">{t.studyIntegrity}</p>
        </section>

        <section>
          <h3 className="text-xl font-semibold">{t.liabilityTitle}</h3>

          <p className="mt-2 text-slate-600">{t.studyLiability}</p>
        </section>

        {/* FINANCE AGENT */}

        <div className="border-t pt-10">
          <h2 className="text-3xl font-bold text-slate-900">
            {t.financeTitle}
          </h2>
        </div>

        <section>
          <h3 className="text-xl font-semibold">{t.descriptionTitle}</h3>

          <p className="mt-2 text-slate-600">{t.financeDescription}</p>
        </section>

        <section>
          <h3 className="text-xl font-semibold">{t.financeAdviceTitle}</h3>

          <p className="mt-2 text-slate-600">{t.financeAdvice}</p>
        </section>

        <section>
          <h3 className="text-xl font-semibold">{t.accuracyTitle}</h3>

          <ul className="mt-2 list-disc pl-5 text-slate-600 space-y-1">
            <li>{t.financeAccuracy1}</li>
            <li>{t.financeAccuracy2}</li>
            <li>{t.financeAccuracy3}</li>
          </ul>
        </section>

        <section>
          <h3 className="text-xl font-semibold">{t.financeHighRiskTitle}</h3>

          <p className="mt-2 text-slate-600">{t.financeHighRisk}</p>
        </section>

        <section>
          <h3 className="text-xl font-semibold">{t.financeLiabilityTitle}</h3>

          <p className="mt-2 text-slate-600">{t.financeLiability}</p>
        </section>

        {/* BUSINESS AGENT */}

        <div className="border-t pt-10">
          <h2 className="text-3xl font-bold text-slate-900">
            {t.businessTitle}
          </h2>
        </div>

        <section>
          <h3 className="text-xl font-semibold">{t.descriptionTitle}</h3>

          <p className="mt-2 text-slate-600">{t.businessDescription}</p>
        </section>

        <section>
          <h3 className="text-xl font-semibold">{t.businessAdviceTitle}</h3>

          <p className="mt-2 text-slate-600">{t.businessAdvice}</p>
        </section>

        <section>
          <h3 className="text-xl font-semibold">{t.accuracyTitle}</h3>

          <ul className="mt-2 list-disc pl-5 text-slate-600 space-y-1">
            <li>{t.businessAccuracy1}</li>
            <li>{t.businessAccuracy2}</li>
            <li>{t.businessAccuracy3}</li>
          </ul>
        </section>

        <section>
          <h3 className="text-xl font-semibold">
            {t.userResponsibilityTitle}
          </h3>

          <p className="mt-2 text-slate-600">{t.businessResponsibility}</p>
        </section>

        <section>
          <h3 className="text-xl font-semibold">{t.highRiskTitle}</h3>

          <p className="mt-2 text-slate-600">{t.businessHighRisk}</p>
        </section>

        <section>
          <h3 className="text-xl font-semibold">{t.liabilityTitle}</h3>

          <p className="mt-2 text-slate-600">{t.businessLiability}</p>
        </section>

        {/* ADDITIONAL AI TERMS */}

        <div className="border-t pt-10">
          <h2 className="text-3xl font-bold text-slate-900">
            {t.additionalTermsTitle}
          </h2>
        </div>

        <section>
          <h3 className="text-xl font-semibold">{t.humanReviewTitle}</h3>

          <p className="mt-2 text-slate-600">{t.humanReview}</p>
        </section>

        <section>
          <h3 className="text-xl font-semibold">{t.dataProcessingTitle}</h3>

          <p className="mt-2 text-slate-600">{t.dataProcessing}</p>
        </section>

        <section>
          <h3 className="text-xl font-semibold">{t.trainingTitle}</h3>

          <p className="mt-2 text-slate-600">{t.trainingText}</p>
        </section>

        <section>
          <h3 className="text-xl font-semibold">{t.transparencyTitle}</h3>

          <p className="mt-2 text-slate-600">{t.transparencyText}</p>
        </section>

        <section>
          <h3 className="text-xl font-semibold">{t.enterpriseTitle}</h3>

          <p className="mt-2 text-slate-600">{t.enterpriseText}</p>
        </section>
      </div>
    </main>
  );
}
