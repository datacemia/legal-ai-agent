"use client";

import { useEffect, useState } from "react";
import { defaultLocale, getSavedLocale } from "../../../../lib/i18n";

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

const productTermsCopy = {
  en: {
    title: "Product Terms",
    updated: "Last updated: June 2026",
    eyebrow: "Product-specific terms",
    heroTitle: "Clear terms for each Runexa AI agent.",
    heroText:
      "These Product Terms explain how Runexa’s specialized AI agents may be used, what each agent is designed to do, and the product-specific limits users should understand before relying on outputs.",
    primaryCta: "Contact Runexa",
    secondaryCta: "Read Terms of Service",

    quickTitle: "What this page covers",
    quickItems: [
      "Agent-specific purpose and intended use",
      "Product limits for legal, finance, study, and business agents",
      "User responsibilities by agent type",
      "High-impact use restrictions",
      "Enterprise and workspace product conditions",
      "Relationship with the Terms of Service and AI Disclaimer",
    ],

    agentOverviewTitle: "Runexa agent family",
    agentOverviewSubtitle:
      "Each agent is designed for a specific workflow. These Product Terms should be read together with the Terms of Service, AI Disclaimer, Privacy Policy, Security page, and Acceptable Use Policy.",
    agentCards: [
      {
        name: "Runexa Legal Agent",
        tag: "Contract and legal-document intelligence",
        description:
          "Assists with contract review, risk signals, clause summaries, obligations, simplified explanations, and negotiation priorities.",
      },
      {
        name: "Runexa Finance Coach",
        tag: "Personal finance insights",
        description:
          "Assists with expense analysis, spending patterns, budgeting observations, and general financial awareness.",
      },
      {
        name: "Runexa Study Agent",
        tag: "Learning support",
        description:
          "Assists with study summaries, quizzes, revision plans, learning explanations, and educational organization.",
      },
      {
        name: "Runexa Business Decision Agent",
        tag: "Business decision support",
        description:
          "Assists with business analysis, scenario review, operational insights, decision briefs, and structured recommendations.",
      },
    ],

    sections: [
      {
        title: "1. Scope of These Product Terms",
        text:
          "These Product Terms apply to the AI agents, workflows, reports, dashboards, previews, generated outputs, and related product features provided through the Runexa platform. If these Product Terms conflict with the general Terms of Service, the more specific product condition applies only for the relevant agent or feature.",
      },
      {
        title: "2. Runexa Legal Agent",
        text:
          "The Runexa Legal Agent is designed to assist with legal-document review, including clause identification, risk indicators, simplified explanations, summaries, obligations, missing-clause observations, and negotiation priorities. It is not a law firm, lawyer, or legal adviser. Outputs should be reviewed by the user and, where appropriate, by a qualified legal professional before signing, rejecting, negotiating, or relying on a contract or legal document.",
      },
      {
        title: "3. Legal Agent Limits",
        text:
          "The Legal Agent may miss clauses, misclassify risk, misunderstand jurisdiction-specific rules, overstate or understate legal exposure, or produce incomplete interpretations. It should not be used as the sole basis for litigation strategy, contract execution, regulatory compliance, legal filings, legal disputes, employment decisions, immigration matters, criminal matters, or other high-impact legal decisions.",
      },
      {
        title: "4. Runexa Finance Coach",
        text:
          "The Runexa Finance Coach is designed to assist with expense analysis, spending patterns, budget awareness, recurring-payment observations, and general financial insights. It does not provide financial, investment, tax, accounting, credit, lending, insurance, or retirement advice. Users remain responsible for verifying transactions, amounts, categories, and recommendations before acting.",
      },
      {
        title: "5. Finance Coach Limits",
        text:
          "The Finance Coach may misclassify transactions, miss financial context, misunderstand income or expenses, overlook account-specific details, or generate incomplete suggestions. It should not be used as the sole basis for investment decisions, tax filings, loan decisions, debt restructuring, retirement planning, insurance decisions, emergency financial decisions, or regulated financial activity.",
      },
      {
        title: "6. Runexa Study Agent",
        text:
          "The Runexa Study Agent is designed to support learning by generating summaries, study plans, quizzes, explanations, revision structures, and learning assistance. It does not guarantee grades, admissions, certifications, exam success, academic progress, or learning outcomes. Users should compare outputs with official course materials, teacher instructions, and institution rules.",
      },
      {
        title: "7. Study Agent Limits and Academic Integrity",
        text:
          "The Study Agent may summarize content incorrectly, generate inaccurate quizzes, omit important context, or provide incomplete explanations. Users must not use the Study Agent to cheat, plagiarize, impersonate original work, bypass academic rules, or violate school, university, exam, or institutional policies.",
      },
      {
        title: "8. Runexa Business Decision Agent",
        text:
          "The Runexa Business Decision Agent is designed to assist with business analysis, structured decision briefs, scenario comparison, operational insights, trend review, and planning support. It does not provide management consulting, legal, tax, accounting, investment, employment, procurement, or regulated professional advice.",
      },
      {
        title: "9. Business Agent Limits",
        text:
          "The Business Decision Agent may misunderstand business context, miss operational constraints, misread market signals, generate incomplete recommendations, or rely on incomplete inputs. It should not be used as the sole basis for hiring, firing, financing, acquisitions, investments, legal disputes, compliance decisions, layoffs, safety-critical decisions, or major business commitments.",
      },
      {
        title: "10. Output Formats and Product Features",
        text:
          "Runexa outputs may include summaries, scores, classifications, risk levels, charts, graphs, recommendations, reports, action items, generated text, or structured data. These formats are designed to make information easier to review; they are not guarantees of accuracy, completeness, priority, risk, legality, financial outcome, academic outcome, or business success.",
      },
      {
        title: "11. Credits, Plans, and Usage",
        text:
          "Agent usage may consume credits or be subject to plan limits, file-size limits, usage quotas, fair-use restrictions, workspace limits, feature availability, or enterprise terms. Credit usage and available features may vary by agent, plan, file type, processing complexity, region, account status, or promotional offer.",
      },
      {
        title: "12. Experimental and Preview Features",
        text:
          "Some Runexa features may be experimental, beta, preview, limited-release, or subject to change. Experimental features may be less reliable, may change without notice, and may be removed, renamed, restricted, or replaced as the platform evolves.",
      },
      {
        title: "13. Enterprise and Workspace Use",
        text:
          "Organizations using Runexa are responsible for user access, internal approvals, workspace configuration, compliance review, professional review, data-governance decisions, and determining whether the product is appropriate for their use case. Enterprise features may be subject to separate written agreements or additional product conditions.",
      },
      {
        title: "14. User Responsibility",
        text:
          "Users are responsible for selecting the correct agent, providing accurate and lawful inputs, reviewing outputs, verifying important information, complying with applicable rules, and deciding whether professional advice or additional review is required before acting.",
      },
      {
        title: "15. Relationship With Other Terms",
        text:
          "These Product Terms supplement the Terms of Service. The AI Disclaimer explains general AI limitations and human-review requirements. The Privacy Policy explains data handling. The Security page explains safeguards. The Acceptable Use Policy explains prohibited uses. The Refund Policy explains refund conditions.",
      },
      {
        title: "16. Contact",
        text:
          "Questions about these Product Terms may be sent to contact@runexa.ai.",
      },
    ],
  },

  fr: {
    title: "Conditions du produit",
    updated: "Dernière mise à jour : juin 2026",
    eyebrow: "Conditions propres aux produits",
    heroTitle: "Des conditions claires pour chaque agent IA Runexa.",
    heroText:
      "Ces Conditions du produit expliquent comment les agents IA spécialisés de Runexa peuvent être utilisés, ce que chaque agent est conçu pour faire et les limites spécifiques à comprendre avant de s’appuyer sur les résultats.",
    primaryCta: "Contacter Runexa",
    secondaryCta: "Lire les Conditions d’utilisation",

    quickTitle: "Ce que couvre cette page",
    quickItems: [
      "Objectif et usage prévu de chaque agent",
      "Limites propres aux agents juridique, finance, étude et business",
      "Responsabilités utilisateur par type d’agent",
      "Restrictions pour les usages à impact élevé",
      "Conditions produit pour les entreprises et espaces de travail",
      "Lien avec les Conditions d’utilisation et l’Avertissement IA",
    ],

    agentOverviewTitle: "Famille d’agents Runexa",
    agentOverviewSubtitle:
      "Chaque agent est conçu pour un workflow spécifique. Ces Conditions du produit doivent être lues avec les Conditions d’utilisation, l’Avertissement IA, la Politique de confidentialité, la page Sécurité et la Politique d’utilisation acceptable.",
    agentCards: [
      {
        name: "Agent juridique Runexa",
        tag: "Intelligence contractuelle et documents juridiques",
        description:
          "Aide à la revue de contrats, aux signaux de risque, résumés de clauses, obligations, explications simplifiées et priorités de négociation.",
      },
      {
        name: "Coach financier Runexa",
        tag: "Insights de finances personnelles",
        description:
          "Aide à analyser les dépenses, repérer les habitudes de consommation, observer le budget et améliorer la compréhension financière.",
      },
      {
        name: "Agent étude Runexa",
        tag: "Soutien à l’apprentissage",
        description:
          "Aide à générer des résumés, quiz, plans de révision, explications pédagogiques et organisation de l’apprentissage.",
      },
      {
        name: "Agent de décision business Runexa",
        tag: "Aide à la décision business",
        description:
          "Aide à l’analyse business, aux scénarios, insights opérationnels, notes de décision et recommandations structurées.",
      },
    ],

    sections: [
      {
        title: "1. Champ d’application de ces Conditions du produit",
        text:
          "Ces Conditions du produit s’appliquent aux agents IA, workflows, rapports, tableaux de bord, aperçus, résultats générés et fonctionnalités liées fournis via la plateforme Runexa. En cas de conflit avec les Conditions d’utilisation générales, la condition produit la plus spécifique s’applique uniquement à l’agent ou à la fonctionnalité concernée.",
      },
      {
        title: "2. Agent juridique Runexa",
        text:
          "L’Agent juridique Runexa est conçu pour assister la revue de documents juridiques, notamment l’identification de clauses, les indicateurs de risque, les explications simplifiées, les résumés, les obligations, les observations sur clauses manquantes et les priorités de négociation. Il n’est pas un cabinet d’avocats, un avocat ou un conseiller juridique. Les résultats doivent être relus par l’utilisateur et, le cas échéant, par un professionnel du droit qualifié avant de signer, refuser, négocier ou s’appuyer sur un contrat ou document juridique.",
      },
      {
        title: "3. Limites de l’Agent juridique",
        text:
          "L’Agent juridique peut manquer des clauses, mal classifier un risque, mal comprendre des règles propres à une juridiction, surestimer ou sous-estimer une exposition juridique, ou produire des interprétations incomplètes. Il ne doit pas être utilisé comme base unique pour une stratégie contentieuse, la signature d’un contrat, la conformité réglementaire, des dépôts juridiques, des litiges, décisions d’emploi, sujets d’immigration, affaires pénales ou autres décisions juridiques à impact élevé.",
      },
      {
        title: "4. Coach financier Runexa",
        text:
          "Le Coach financier Runexa est conçu pour aider à analyser les dépenses, les habitudes de consommation, la compréhension budgétaire, les paiements récurrents et les insights financiers généraux. Il ne fournit pas de conseil financier, d’investissement, fiscal, comptable, de crédit, de prêt, d’assurance ou de retraite. Les utilisateurs restent responsables de vérifier les transactions, montants, catégories et recommandations avant d’agir.",
      },
      {
        title: "5. Limites du Coach financier",
        text:
          "Le Coach financier peut mal classifier des transactions, manquer un contexte financier, mal comprendre les revenus ou dépenses, ignorer des détails propres à un compte ou générer des suggestions incomplètes. Il ne doit pas être utilisé comme base unique pour des investissements, déclarations fiscales, décisions de prêt, restructuration de dettes, planification retraite, décisions d’assurance, décisions financières urgentes ou activités financières réglementées.",
      },
      {
        title: "6. Agent étude Runexa",
        text:
          "L’Agent étude Runexa est conçu pour soutenir l’apprentissage en générant des résumés, plans d’étude, quiz, explications, structures de révision et assistance pédagogique. Il ne garantit pas les notes, admissions, certifications, réussites d’examen, progrès académiques ou résultats d’apprentissage. Les utilisateurs doivent comparer les résultats avec les supports officiels, consignes des enseignants et règles de leur établissement.",
      },
      {
        title: "7. Limites de l’Agent étude et intégrité académique",
        text:
          "L’Agent étude peut résumer incorrectement un contenu, générer des quiz inexacts, omettre un contexte important ou fournir des explications incomplètes. Les utilisateurs ne doivent pas utiliser l’Agent étude pour tricher, plagier, présenter un contenu comme un travail original, contourner des règles académiques ou violer les politiques d’une école, université, examen ou institution.",
      },
      {
        title: "8. Agent de décision business Runexa",
        text:
          "L’Agent de décision business Runexa est conçu pour assister l’analyse business, les notes de décision structurées, la comparaison de scénarios, les insights opérationnels, l’examen de tendances et le soutien à la planification. Il ne fournit pas de conseil en management, juridique, fiscal, comptable, d’investissement, d’emploi, d’achat ou autre conseil professionnel réglementé.",
      },
      {
        title: "9. Limites de l’Agent business",
        text:
          "L’Agent de décision business peut mal comprendre le contexte, manquer des contraintes opérationnelles, mal lire des signaux de marché, générer des recommandations incomplètes ou s’appuyer sur des données incomplètes. Il ne doit pas être utilisé comme base unique pour l’embauche, le licenciement, le financement, les acquisitions, les investissements, les litiges, la conformité, les licenciements collectifs, les décisions critiques de sécurité ou les engagements business majeurs.",
      },
      {
        title: "10. Formats de sortie et fonctionnalités produit",
        text:
          "Les résultats Runexa peuvent inclure des résumés, scores, classifications, niveaux de risque, graphiques, recommandations, rapports, actions, texte généré ou données structurées. Ces formats visent à faciliter la revue de l’information ; ils ne garantissent pas l’exactitude, l’exhaustivité, la priorité, le risque, la légalité, le résultat financier, le résultat académique ou la réussite business.",
      },
      {
        title: "11. Crédits, plans et usage",
        text:
          "L’utilisation des agents peut consommer des crédits ou être soumise à des limites de plan, taille de fichier, quotas d’usage, restrictions d’usage raisonnable, limites d’espace de travail, disponibilité de fonctionnalités ou conditions entreprise. L’usage des crédits et les fonctionnalités disponibles peuvent varier selon l’agent, le plan, le type de fichier, la complexité du traitement, la région, le statut du compte ou l’offre promotionnelle.",
      },
      {
        title: "12. Fonctionnalités expérimentales et aperçus",
        text:
          "Certaines fonctionnalités Runexa peuvent être expérimentales, bêta, en aperçu, en diffusion limitée ou susceptibles d’évoluer. Les fonctionnalités expérimentales peuvent être moins fiables, changer sans préavis, être supprimées, renommées, restreintes ou remplacées à mesure que la plateforme évolue.",
      },
      {
        title: "13. Utilisation entreprise et espaces de travail",
        text:
          "Les organisations utilisant Runexa sont responsables de l’accès des utilisateurs, des approbations internes, de la configuration des espaces de travail, de la revue de conformité, de la revue professionnelle, des décisions de gouvernance des données et de l’évaluation de l’adéquation du produit à leur cas d’usage. Les fonctionnalités entreprise peuvent être soumises à des accords écrits séparés ou à des conditions produit additionnelles.",
      },
      {
        title: "14. Responsabilité de l’utilisateur",
        text:
          "Les utilisateurs sont responsables de choisir le bon agent, fournir des entrées exactes et licites, relire les résultats, vérifier les informations importantes, respecter les règles applicables et déterminer si un avis professionnel ou une revue supplémentaire est nécessaire avant d’agir.",
      },
      {
        title: "15. Relation avec les autres conditions",
        text:
          "Ces Conditions du produit complètent les Conditions d’utilisation. L’Avertissement IA explique les limites générales de l’IA et les exigences de revue humaine. La Politique de confidentialité explique le traitement des données. La page Sécurité explique les mesures de protection. La Politique d’utilisation acceptable explique les usages interdits. La Politique de remboursement explique les conditions de remboursement.",
      },
      {
        title: "16. Contact",
        text:
          "Les questions concernant ces Conditions du produit peuvent être envoyées à contact@runexa.ai.",
      },
    ],
  },

  ar: {
    title: "شروط المنتج",
    updated: "آخر تحديث: يونيو 2026",
    eyebrow: "شروط خاصة بالمنتج",
    heroTitle: "شروط واضحة لكل وكيل ذكاء اصطناعي في Runexa.",
    heroText:
      "توضح شروط المنتج هذه كيفية استخدام وكلاء Runexa المتخصصين، وما صُمم كل وكيل للقيام به، والحدود الخاصة بكل منتج التي يجب على المستخدمين فهمها قبل الاعتماد على المخرجات.",
    primaryCta: "تواصل مع Runexa",
    secondaryCta: "قراءة شروط الاستخدام",

    quickTitle: "ما الذي تغطيه هذه الصفحة",
    quickItems: [
      "الغرض والاستخدام المقصود لكل وكيل",
      "حدود المنتج للوكلاء القانوني والمالي والدراسي والتجاري",
      "مسؤوليات المستخدم حسب نوع الوكيل",
      "قيود الاستخدامات عالية التأثير",
      "شروط المنتج للمؤسسات ومساحات العمل",
      "العلاقة مع شروط الاستخدام وإخلاء مسؤولية الذكاء الاصطناعي",
    ],

    agentOverviewTitle: "مجموعة وكلاء Runexa",
    agentOverviewSubtitle:
      "تم تصميم كل وكيل لسير عمل محدد. يجب قراءة شروط المنتج هذه مع شروط الاستخدام وإخلاء مسؤولية الذكاء الاصطناعي وسياسة الخصوصية وصفحة الأمان وسياسة الاستخدام المقبول.",
    agentCards: [
      {
        name: "وكيل Runexa القانوني",
        tag: "ذكاء العقود والمستندات القانونية",
        description:
          "يساعد في مراجعة العقود وإشارات المخاطر وملخصات البنود والالتزامات والتفسيرات المبسطة وأولويات التفاوض.",
      },
      {
        name: "مدرب Runexa المالي",
        tag: "رؤى مالية شخصية",
        description:
          "يساعد في تحليل المصاريف وأنماط الإنفاق وملاحظات الميزانية والوعي المالي العام.",
      },
      {
        name: "وكيل Runexa للدراسة",
        tag: "دعم التعلم",
        description:
          "يساعد في الملخصات الدراسية والاختبارات وخطط المراجعة والتفسيرات التعليمية وتنظيم التعلم.",
      },
      {
        name: "وكيل Runexa لقرارات الأعمال",
        tag: "دعم قرارات الأعمال",
        description:
          "يساعد في تحليل الأعمال ومراجعة السيناريوهات والرؤى التشغيلية ومذكرات القرار والتوصيات المنظمة.",
      },
    ],

    sections: [
      {
        title: "1. نطاق شروط المنتج",
        text:
          "تنطبق شروط المنتج هذه على وكلاء الذكاء الاصطناعي وسير العمل والتقارير ولوحات المعلومات والمعاينات والمخرجات والميزات ذات الصلة المقدمة عبر منصة Runexa. إذا تعارضت شروط المنتج هذه مع شروط الاستخدام العامة، فإن الشرط الأكثر تحديداً ينطبق فقط على الوكيل أو الميزة ذات الصلة.",
      },
      {
        title: "2. وكيل Runexa القانوني",
        text:
          "تم تصميم وكيل Runexa القانوني للمساعدة في مراجعة المستندات القانونية، بما في ذلك تحديد البنود، ومؤشرات المخاطر، والتفسيرات المبسطة، والملخصات، والالتزامات، وملاحظات البنود المفقودة، وأولويات التفاوض. وهو ليس مكتب محاماة أو محامياً أو مستشاراً قانونياً. يجب على المستخدم مراجعة المخرجات، وعند الاقتضاء مراجعتها مع مهني قانوني مؤهل قبل توقيع أو رفض أو التفاوض بشأن أو الاعتماد على عقد أو مستند قانوني.",
      },
      {
        title: "3. حدود الوكيل القانوني",
        text:
          "قد يفوت الوكيل القانوني بعض البنود، أو يخطئ في تصنيف المخاطر، أو يسيء فهم قواعد خاصة بولاية قضائية، أو يبالغ أو يقلل من التعرض القانوني، أو ينتج تفسيرات غير مكتملة. لا ينبغي استخدامه كأساس وحيد لاستراتيجية التقاضي أو تنفيذ العقود أو الامتثال التنظيمي أو الإيداعات القانونية أو النزاعات أو قرارات العمل أو مسائل الهجرة أو القضايا الجنائية أو غيرها من القرارات القانونية عالية التأثير.",
      },
      {
        title: "4. مدرب Runexa المالي",
        text:
          "تم تصميم مدرب Runexa المالي للمساعدة في تحليل المصاريف وأنماط الإنفاق والوعي بالميزانية وملاحظات المدفوعات المتكررة والرؤى المالية العامة. لا يقدم مشورة مالية أو استثمارية أو ضريبية أو محاسبية أو ائتمانية أو متعلقة بالقروض أو التأمين أو التقاعد. يبقى المستخدمون مسؤولين عن التحقق من المعاملات والمبالغ والتصنيفات والتوصيات قبل اتخاذ أي إجراء.",
      },
      {
        title: "5. حدود المدرب المالي",
        text:
          "قد يخطئ المدرب المالي في تصنيف المعاملات، أو يفوّت سياقاً مالياً مهماً، أو يسيء فهم الدخل أو المصاريف، أو يتجاهل تفاصيل خاصة بالحساب، أو يولد اقتراحات غير مكتملة. لا ينبغي استخدامه كأساس وحيد للاستثمارات أو التصريحات الضريبية أو قرارات القروض أو إعادة هيكلة الديون أو تخطيط التقاعد أو قرارات التأمين أو القرارات المالية الطارئة أو الأنشطة المالية المنظمة.",
      },
      {
        title: "6. وكيل Runexa للدراسة",
        text:
          "تم تصميم وكيل Runexa للدراسة لدعم التعلم من خلال إنشاء ملخصات وخطط دراسة واختبارات وتفسيرات وهياكل مراجعة ومساعدة تعليمية. لا يضمن الدرجات أو القبول أو الشهادات أو النجاح في الامتحانات أو التقدم الأكاديمي أو نتائج التعلم. يجب على المستخدمين مقارنة المخرجات بالمواد الرسمية وتعليمات المدرسين وقواعد المؤسسة.",
      },
      {
        title: "7. حدود وكيل الدراسة والنزاهة الأكاديمية",
        text:
          "قد يلخص وكيل الدراسة المحتوى بشكل غير صحيح، أو ينشئ اختبارات غير دقيقة، أو يغفل سياقاً مهماً، أو يقدم تفسيرات غير مكتملة. يجب ألا يستخدم المستخدمون وكيل الدراسة للغش أو الانتحال أو تقديم محتوى كعمل أصلي أو تجاوز القواعد الأكاديمية أو انتهاك سياسات المدرسة أو الجامعة أو الامتحان أو المؤسسة.",
      },
      {
        title: "8. وكيل Runexa لقرارات الأعمال",
        text:
          "تم تصميم وكيل Runexa لقرارات الأعمال للمساعدة في تحليل الأعمال، ومذكرات القرار المنظمة، ومقارنة السيناريوهات، والرؤى التشغيلية، ومراجعة الاتجاهات، ودعم التخطيط. لا يقدم استشارات إدارية أو قانونية أو ضريبية أو محاسبية أو استثمارية أو متعلقة بالتوظيف أو المشتريات أو أي مشورة مهنية منظمة.",
      },
      {
        title: "9. حدود وكيل الأعمال",
        text:
          "قد يسيء وكيل قرارات الأعمال فهم سياق الأعمال، أو يفوت قيوداً تشغيلية، أو يقرأ إشارات السوق بشكل غير صحيح، أو يولد توصيات غير مكتملة، أو يعتمد على مدخلات غير كاملة. لا ينبغي استخدامه كأساس وحيد للتوظيف أو الفصل أو التمويل أو الاستحواذات أو الاستثمارات أو النزاعات القانونية أو قرارات الامتثال أو التسريح أو قرارات السلامة الحرجة أو الالتزامات التجارية الكبرى.",
      },
      {
        title: "10. صيغ المخرجات وميزات المنتج",
        text:
          "قد تشمل مخرجات Runexa ملخصات أو درجات أو تصنيفات أو مستويات مخاطر أو مخططات أو رسوم بيانية أو توصيات أو تقارير أو عناصر عمل أو نصوصاً مولدة أو بيانات منظمة. تهدف هذه الصيغ إلى تسهيل مراجعة المعلومات؛ ولا تمثل ضماناً للدقة أو الاكتمال أو الأولوية أو المخاطر أو القانونية أو النتيجة المالية أو النتيجة الأكاديمية أو النجاح التجاري.",
      },
      {
        title: "11. الأرصدة والخطط والاستخدام",
        text:
          "قد يستهلك استخدام الوكلاء أرصدة أو يخضع لحدود الخطة أو حجم الملف أو حصص الاستخدام أو قيود الاستخدام العادل أو حدود مساحة العمل أو توفر الميزات أو شروط المؤسسات. قد يختلف استخدام الأرصدة والميزات المتاحة حسب الوكيل والخطة ونوع الملف وتعقيد المعالجة والمنطقة وحالة الحساب أو العرض الترويجي.",
      },
      {
        title: "12. الميزات التجريبية والمعاينات",
        text:
          "قد تكون بعض ميزات Runexa تجريبية أو في مرحلة بيتا أو معاينة أو إصدار محدود أو قابلة للتغيير. قد تكون الميزات التجريبية أقل موثوقية، وقد تتغير دون إشعار، أو تُحذف أو يُعاد تسميتها أو تُقيّد أو تُستبدل مع تطور المنصة.",
      },
      {
        title: "13. استخدام المؤسسات ومساحات العمل",
        text:
          "تتحمل المؤسسات التي تستخدم Runexa مسؤولية وصول المستخدمين والموافقات الداخلية وإعداد مساحات العمل ومراجعة الامتثال والمراجعة المهنية وقرارات حوكمة البيانات وتحديد ما إذا كان المنتج مناسباً لحالة الاستخدام الخاصة بها. قد تخضع ميزات المؤسسات لاتفاقيات مكتوبة منفصلة أو شروط منتج إضافية.",
      },
      {
        title: "14. مسؤولية المستخدم",
        text:
          "يتحمل المستخدمون مسؤولية اختيار الوكيل الصحيح، وتقديم مدخلات دقيقة وقانونية، ومراجعة المخرجات، والتحقق من المعلومات المهمة، والامتثال للقواعد المعمول بها، وتحديد ما إذا كانت هناك حاجة إلى مشورة مهنية أو مراجعة إضافية قبل اتخاذ إجراء.",
      },
      {
        title: "15. العلاقة مع الشروط الأخرى",
        text:
          "تكمل شروط المنتج هذه شروط الاستخدام. يوضح إخلاء مسؤولية الذكاء الاصطناعي حدود الذكاء الاصطناعي العامة ومتطلبات المراجعة البشرية. توضح سياسة الخصوصية معالجة البيانات. تشرح صفحة الأمان الضمانات. توضح سياسة الاستخدام المقبول الاستخدامات المحظورة. وتوضح سياسة الاسترداد شروط الاسترداد.",
      },
      {
        title: "16. التواصل",
        text:
          "يمكن إرسال الأسئلة المتعلقة بشروط المنتج هذه إلى contact@runexa.ai.",
      },
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
  quickTitle: string;
  quickItems: string[];
  agentOverviewTitle: string;
  agentOverviewSubtitle: string;
  agentCards: {
    name: string;
    tag: string;
    description: string;
  }[];
  sections: { title: string; text: string }[];
}>;

export default function ProductTermsClient({
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

  const t = productTermsCopy[locale];

  return (
    <main
      dir={locale === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-950 px-4 py-10 text-slate-900"
    >
      <div className="mx-auto max-w-6xl space-y-8">
        <section className="overflow-hidden rounded-[2rem] border border-white/10 bg-white shadow-2xl">
          <div className="grid gap-0 lg:grid-cols-[1.15fr_0.85fr]">
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
                  href="/terms"
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
                {t.quickTitle}
              </h2>

              <div className="mt-8 space-y-4">
                {t.quickItems.map((item) => (
                  <div
                    key={item}
                    className="rounded-2xl border border-white/10 bg-white/5 p-4"
                  >
                    <p className="text-sm leading-6 text-slate-200">
                      {item}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        <section className="rounded-[2rem] border border-white/10 bg-white p-8 shadow-xl md:p-10">
          <h2 className="text-2xl font-bold text-slate-950">
            {t.agentOverviewTitle}
          </h2>

          <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-600">
            {t.agentOverviewSubtitle}
          </p>

          <div className="mt-8 grid gap-4 md:grid-cols-2">
            {t.agentCards.map((agent) => (
              <article
                key={agent.name}
                className="rounded-2xl border border-slate-200 bg-slate-50 p-5"
              >
                <p className="text-xs font-semibold uppercase tracking-wide text-blue-600">
                  {agent.tag}
                </p>

                <h3 className="mt-2 text-lg font-semibold text-slate-950">
                  {agent.name}
                </h3>

                <p className="mt-2 text-sm leading-6 text-slate-600">
                  {agent.description}
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
            {t.sections.map((section) => (
              <section key={section.title}>
                <h2 className="text-xl font-semibold text-slate-950">
                  {section.title}
                </h2>

                <p className="mt-2 whitespace-normal break-words text-slate-600">
                  {section.text}
                </p>
              </section>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}
