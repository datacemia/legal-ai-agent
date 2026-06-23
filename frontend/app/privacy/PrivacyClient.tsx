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

type PolicySection = {
  title: string;
  text: string;
};

type PrivacyCopy = {
  title: string;
  updated: string;
  eyebrow: string;
  heroTitle: string;
  heroText: string;
  securityLink: string;
  contactLink: string;
  quickTitle: string;
  quickItems: string[];
  flowTitle: string;
  flowItems: string[][];
  sections: PolicySection[];
};

const privacyCopy: Record<Locale, PrivacyCopy> = {
  en: {
    title: "Privacy Policy",
    updated: "Last updated: June 2026",
    eyebrow: "Privacy by design",
    heroTitle: "How Runexa handles your data",
    heroText:
      "Runexa is designed for sensitive documents. Uploaded files are processed solely to provide the requested analysis. Personal identifiers are replaced with neutral placeholders before AI processing. Customer content is not used to train public AI models, and uploaded files are automatically removed from processing storage once the analysis is complete.",
    securityLink: "Security & Data Handling",
    contactLink: "Contact Runexa",
    quickTitle: "At a glance",
    quickItems: [
      "Customer files are not used to train public AI models.",
      "Personal identifiers are replaced with neutral placeholders before AI processing.",
      "Uploaded files are removed from processing storage after analysis.",
      "Generated results may remain available in your workspace until deleted or retained as required.",
      "Customer data is logically isolated between users and workspaces.",
      "Runexa does not sell personal information.",
    ],
    flowTitle: "Document processing flow",
    flowItems: [
      ["1", "Upload", "You upload a file or content for a selected Runexa agent."],
      ["2", "Extract", "Runexa extracts the text or data needed to generate the requested output."],
      ["3", "Protect", "Personal identifiers are replaced with neutral placeholders before AI processing."],
      ["4", "Analyze", "AI systems and supporting infrastructure generate the requested analysis."],
      ["5", "Delete file", "The uploaded file is removed from processing storage after analysis is completed."],
    ],
    sections: [
      {
        title: "1. Introduction",
        text:
          "Runexa Systems LLC (“Runexa”, “we”, “our”, or “us”) respects your privacy. This Privacy Policy explains how we collect, use, process, store, share, and protect information when you use Runexa websites, workspaces, AI agents, document analysis tools, and related services.",
      },
      {
        title: "2. Information We Collect",
        text:
          "We may collect account information, billing status, and information necessary to operate the services. Payments are processed by Stripe, and Runexa does not store payment card information on its own servers.",
      },
      {
        title: "3. Uploaded Content",
        text:
          "Uploaded content may include contracts, financial records, study materials, business documents, files, text, and other information provided for analysis. Uploaded files are processed solely to generate the analysis or output requested by the user. Runexa replaces personal identifiers with neutral placeholders before AI processing. Once the analysis is complete, uploaded content and associated files are automatically removed from processing storage.",
      },
      {
        title: "4. How We Use Your Data",
        text:
          "We use data to provide and maintain the services, generate AI-powered outputs, manage accounts and credits, process payments, improve reliability and user experience, detect abuse, prevent fraud, protect platform security, respond to support requests, and comply with legal, tax, accounting, and regulatory obligations.",
      },
      {
        title: "5. AI Processing",
        text:
          "Runexa services may use automated systems and AI models to extract, classify, summarize, analyze, transform, and generate information from uploaded content. AI-generated outputs may be incomplete or inaccurate and should be independently reviewed before important legal, financial, educational, or business decisions.",
      },
      {
        title: "6. AI Model Training",
        text:
          "Runexa does not use customer-uploaded documents, contracts, financial records, study materials, business data, or other private customer content to train public AI models unless explicitly authorized by the user or clearly disclosed where permitted by applicable law.",
      },
      {
        title: "7. Data Storage and Providers",
        text:
          "Runexa may use secure third-party infrastructure, hosting, database, analytics, payment, storage, and AI service providers to operate the platform. These providers process information only as needed to support the services, infrastructure, security, billing, and user-requested analysis workflows.",
      },
      {
        title: "8. Data Retention and Deletion",
        text:
          "Uploaded files are removed from processing storage once the requested analysis is complete. Certain account information, such as an email address, and billing information required to operate the account and comply with legal obligations may be retained for as long as necessary. Users may request deletion of their personal information, subject to applicable legal, security, billing, fraud-prevention, and operational retention requirements.",
      },
      {
        title: "9. Data Sharing",
        text:
          "We do not sell your personal information. Limited account information, such as your email address and authentication-related data, may be shared only with technical providers required to securely operate the service, payment providers such as Stripe, or competent authorities where required by law.",
      },
      {
        title: "10. Workspace Isolation and Internal Access",
        text:
          "Account data is logically separated between users and workspaces. Users cannot access information or results associated with another account through the platform. Operational access, when required for security, support, abuse prevention, or legal reasons, is restricted and controlled.",
      },
      {
        title: "11. Security",
        text:
          "We implement reasonable technical, administrative, and organizational safeguards designed to protect user information, uploaded content, accounts, and platform integrity. However, no internet-based platform, software system, AI system, or storage system can be guaranteed to be completely secure.",
      },
      {
        title: "12. International Users and Transfers",
        text:
          "Runexa Systems LLC is a United States company that provides services internationally. If you access the services from outside the United States, your information may be transferred to, stored in, or processed in the United States or other jurisdictions where our service providers operate. Where required, Runexa uses reasonable safeguards designed to protect personal information in accordance with applicable law.",
      },
      {
        title: "13. Your Rights",
        text:
          "Depending on your location, you may have rights to access, correct, delete, export, restrict, or object to certain processing of your personal information. You may contact us to exercise these rights. We may need to verify your identity before responding to certain requests.",
      },
      {
        title: "14. Cookies and Similar Technologies",
        text:
          "Cookies and similar technologies may be used to maintain sessions, remember preferences, secure accounts, analyze usage, detect abuse, and improve the user experience. You may manage cookies through your browser settings where available.",
      },
      {
        title: "15. Children and Minors",
        text:
          "Certain educational services provided by Runexa may be used by children and minors. Runexa only collects the account information necessary to access the service, such as an email address and authentication-related account information. Where required by applicable law, users who have not reached the age necessary to manage an account independently must use the service with authorization or supervision from a parent, legal guardian, or educational institution.",
      },
      {
        title: "16. Enterprise Data Handling",
        text:
          "Enterprise customers and organizations may request additional contractual, operational, retention, security, or infrastructure information where available. Organizations remain responsible for assessing their own compliance, governance, security, procurement, and regulatory obligations when using Runexa services.",
      },
      {
        title: "17. Changes to This Policy",
        text:
          "We may update this Privacy Policy from time to time. Updated versions will be posted on this page with a revised “Last updated” date. Continued use of the services after an update means the updated policy applies from its effective date.",
      },
      {
        title: "18. Contact",
        text:
          "Questions, privacy requests, deletion requests, or data protection inquiries may be sent to contact@runexa.ai.",
      },
    ],
  },

  fr: {
    title: "Politique de confidentialité",
    updated: "Dernière mise à jour : juin 2026",
    eyebrow: "Confidentialité dès la conception",
    heroTitle: "Comment Runexa traite vos données",
    heroText:
      "Runexa est conçu pour les documents sensibles. Les fichiers importés sont traités uniquement pour fournir l’analyse demandée. Les identifiants personnels sont remplacés par des libellés neutres avant le traitement par l’IA. Les contenus clients ne servent pas à entraîner des modèles IA publics, et les fichiers importés sont automatiquement supprimés du stockage de traitement une fois l’analyse terminée.",
    securityLink: "Sécurité et traitement des données",
    contactLink: "Contacter Runexa",
    quickTitle: "En résumé",
    quickItems: [
      "Les fichiers clients ne servent pas à entraîner des modèles IA publics.",
      "Les identifiants personnels sont remplacés par des libellés neutres avant le traitement par l’IA.",
      "Les fichiers importés sont supprimés du stockage de traitement après analyse.",
      "Les résultats générés peuvent rester disponibles dans votre espace jusqu’à leur suppression ou conservation nécessaire.",
      "Les données clients sont isolées logiquement entre utilisateurs et espaces de travail.",
      "Runexa ne vend pas les informations personnelles.",
    ],
    flowTitle: "Flux de traitement des documents",
    flowItems: [
      ["1", "Import", "Vous importez un fichier ou contenu pour un agent Runexa sélectionné."],
      ["2", "Extraction", "Runexa extrait le texte ou les données nécessaires pour générer le résultat demandé."],
      ["3", "Protection", "Les identifiants personnels sont remplacés par des libellés neutres avant le traitement par l’IA."],
      ["4", "Analyse", "Les systèmes IA et l’infrastructure associée génèrent l’analyse demandée."],
      ["5", "Suppression", "Le fichier importé est supprimé du stockage de traitement après analyse."],
    ],
    sections: [
      {
        title: "1. Introduction",
        text:
          "Runexa Systems LLC (« Runexa », « nous », « notre ») respecte votre confidentialité. Cette Politique de confidentialité explique comment nous collectons, utilisons, traitons, stockons, partageons et protégeons les informations lorsque vous utilisez les sites, espaces de travail, agents IA, outils d’analyse documentaire et services associés de Runexa.",
      },
      {
        title: "2. Informations collectées",
        text:
          "Nous pouvons collecter des informations de compte, le statut de facturation ainsi que les informations nécessaires au fonctionnement des services. Les paiements sont traités par Stripe, et Runexa ne stocke pas les informations de carte bancaire sur ses propres serveurs.",
      },
      {
        title: "3. Contenu importé",
        text:
          "Le contenu importé peut inclure des contrats, relevés financiers, supports d’apprentissage, documents professionnels, fichiers, textes et autres informations fournies pour analyse. Les fichiers importés sont traités uniquement afin de générer l’analyse ou le résultat demandé par l’utilisateur. Runexa remplace les identifiants personnels par des libellés neutres avant le traitement par l’IA. Une fois l’analyse terminée, le contenu importé et les fichiers associés sont automatiquement supprimés du stockage de traitement.",
      },
      {
        title: "4. Utilisation des données",
        text:
          "Nous utilisons les données pour fournir et maintenir les services, générer des résultats assistés par IA, gérer les comptes et crédits, traiter les paiements, améliorer la fiabilité et l’expérience utilisateur, détecter les abus, prévenir la fraude, protéger la sécurité de la plateforme, répondre aux demandes de support et respecter les obligations légales, fiscales, comptables et réglementaires.",
      },
      {
        title: "5. Traitement IA",
        text:
          "Les services Runexa peuvent utiliser des systèmes automatisés et des modèles IA pour extraire, classifier, résumer, analyser, transformer et générer des informations à partir du contenu importé. Les résultats générés par l’IA peuvent être incomplets ou inexacts et doivent être vérifiés indépendamment avant toute décision juridique, financière, éducative ou professionnelle importante.",
      },
      {
        title: "6. Entraînement des modèles IA",
        text:
          "Runexa n’utilise pas les documents clients importés, contrats, relevés financiers, supports d’apprentissage, données business ou autres contenus privés clients pour entraîner des modèles IA publics, sauf autorisation explicite de l’utilisateur ou information claire lorsque la loi applicable le permet.",
      },
      {
        title: "7. Stockage et prestataires",
        text:
          "Runexa peut utiliser des prestataires tiers d’infrastructure, d’hébergement, de base de données, d’analyse, de paiement, de stockage et d’IA pour opérer la plateforme. Ces prestataires traitent les informations uniquement lorsque cela est nécessaire pour soutenir les services, l’infrastructure, la sécurité, la facturation et les workflows d’analyse demandés par l’utilisateur.",
      },
      {
        title: "8. Conservation et suppression des données",
        text:
          "Les fichiers importés sont supprimés du stockage de traitement une fois l’analyse demandée terminée. Certaines informations de compte, telles que l’adresse e-mail, ainsi que les informations de facturation nécessaires au fonctionnement du compte et au respect des obligations légales, peuvent être conservées aussi longtemps que nécessaire. Les utilisateurs peuvent demander la suppression de leurs informations personnelles, sous réserve des exigences légales, de sécurité, de facturation, de prévention de la fraude et de conservation opérationnelle applicables.",
      },
      {
        title: "9. Partage des données",
        text:
          "Nous ne vendons pas vos informations personnelles. Les informations de compte limitées, telles que l’adresse e-mail et les données nécessaires à l’authentification, peuvent être partagées uniquement avec les prestataires techniques nécessaires au fonctionnement sécurisé du service, les prestataires de paiement comme Stripe, ou les autorités compétentes lorsque la loi l’exige.",
      },
      {
        title: "10. Isolation des espaces et accès interne",
        text:
          "Les données de compte sont séparées logiquement entre utilisateurs et espaces de travail. Les utilisateurs ne peuvent pas accéder aux informations ou résultats associés à un autre compte via la plateforme. Les accès opérationnels, lorsqu’ils sont nécessaires pour la sécurité, le support, la prévention des abus ou des raisons légales, sont restreints et contrôlés.",
      },
      {
        title: "11. Sécurité",
        text:
          "Nous mettons en œuvre des mesures techniques, administratives et organisationnelles raisonnables conçues pour protéger les informations utilisateur, contenus importés, comptes et l’intégrité de la plateforme. Toutefois, aucune plateforme internet, logiciel, système IA ou système de stockage ne peut être garanti comme totalement sécurisé.",
      },
      {
        title: "12. Utilisateurs internationaux et transferts",
        text:
          "Runexa Systems LLC est une société américaine qui fournit ses services à l’international. Si vous utilisez les services depuis l’extérieur des États-Unis, vos informations peuvent être transférées, stockées ou traitées aux États-Unis ou dans d’autres juridictions où nos prestataires opèrent. Lorsque cela est requis, Runexa utilise des garanties raisonnables conçues pour protéger les informations personnelles conformément à la loi applicable.",
      },
      {
        title: "13. Vos droits",
        text:
          "Selon votre localisation, vous pouvez disposer de droits d’accès, de rectification, de suppression, d’exportation, de limitation ou d’opposition à certains traitements de vos informations personnelles. Vous pouvez nous contacter pour exercer ces droits. Nous pouvons devoir vérifier votre identité avant de répondre à certaines demandes.",
      },
      {
        title: "14. Cookies et technologies similaires",
        text:
          "Les cookies et technologies similaires peuvent être utilisés pour maintenir les sessions, mémoriser les préférences, sécuriser les comptes, analyser l’usage, détecter les abus et améliorer l’expérience utilisateur. Vous pouvez gérer les cookies via les paramètres de votre navigateur lorsque cela est disponible.",
      },
      {
        title: "15. Enfants et mineurs",
        text:
          "Certains services éducatifs de Runexa peuvent être utilisés par des enfants et des mineurs. Runexa ne collecte que les informations de compte nécessaires à l’accès au service, telles que l’adresse e-mail et les informations d’authentification associées au compte. Lorsqu’un utilisateur n’a pas atteint l’âge requis par la législation applicable pour gérer un compte de manière autonome, l’utilisation du service doit être autorisée ou supervisée par un parent, un tuteur légal ou un établissement éducatif lorsque cela est requis.",
      },
      {
        title: "16. Traitement des données entreprise",
        text:
          "Les clients entreprise et organisations peuvent demander des informations contractuelles, opérationnelles, de conservation, de sécurité ou d’infrastructure supplémentaires lorsque disponibles. Les organisations restent responsables de l’évaluation de leurs propres obligations de conformité, gouvernance, sécurité, achat et réglementation lorsqu’elles utilisent les services Runexa.",
      },
      {
        title: "17. Modifications de cette politique",
        text:
          "Nous pouvons mettre à jour cette Politique de confidentialité périodiquement. Les versions mises à jour seront publiées sur cette page avec une date de dernière mise à jour révisée. La poursuite de l’utilisation des services après une mise à jour signifie que la politique mise à jour s’applique à partir de sa date d’entrée en vigueur.",
      },
      {
        title: "18. Contact",
        text:
          "Les questions, demandes relatives à la confidentialité, demandes de suppression ou demandes liées à la protection des données peuvent être envoyées à contact@runexa.ai.",
      },
    ],
  },

  ar: {
    title: "سياسة الخصوصية",
    updated: "آخر تحديث: يونيو 2026",
    eyebrow: "الخصوصية منذ التصميم",
    heroTitle: "كيف يتعامل Runexa مع بياناتك",
    heroText:
      "تم تصميم Runexa للمستندات الحساسة. تُعالج الملفات المرفوعة حصرياً لتقديم التحليل المطلوب. ويتم استبدال المعرّفات الشخصية بعلامات تعريف محايدة قبل المعالجة بالذكاء الاصطناعي. ولا تُستخدم محتويات العملاء لتدريب نماذج ذكاء اصطناعي عامة، كما تُحذف الملفات المرفوعة تلقائياً من مساحة تخزين المعالجة فور اكتمال التحليل.",
    securityLink: "الأمان ومعالجة البيانات",
    contactLink: "تواصل مع Runexa",
    quickTitle: "لمحة سريعة",
    quickItems: [
      "لا تُستخدم ملفات العملاء لتدريب نماذج ذكاء اصطناعي عامة.",
      "يتم استبدال المعرّفات الشخصية بعلامات تعريف محايدة قبل المعالجة بالذكاء الاصطناعي.",
      "تُحذف الملفات المرفوعة من تخزين المعالجة بعد التحليل.",
      "قد تبقى النتائج المولدة متاحة في مساحة العمل الخاصة بك إلى أن يتم حذفها أو يلزم الاحتفاظ بها.",
      "يتم عزل بيانات العملاء منطقياً بين المستخدمين ومساحات العمل.",
      "لا تبيع Runexa المعلومات الشخصية.",
    ],
    flowTitle: "مسار معالجة المستندات",
    flowItems: [
      ["1", "رفع", "ترفع ملفاً أو محتوى لاستخدامه مع وكيل Runexa محدد."],
      ["2", "استخراج", "يستخرج Runexa النص أو البيانات اللازمة لإنشاء النتيجة المطلوبة."],
      ["3", "حماية", "يتم استبدال المعرّفات الشخصية بعلامات تعريف محايدة قبل المعالجة بالذكاء الاصطناعي."],
      ["4", "تحليل", "تنشئ أنظمة الذكاء الاصطناعي والبنية الداعمة التحليل المطلوب."],
      ["5", "حذف الملف", "يتم حذف الملف المرفوع من تخزين المعالجة بعد اكتمال التحليل."],
    ],
    sections: [
      {
        title: "1. المقدمة",
        text:
          "تحترم Runexa Systems LLC («Runexa» أو «نحن») خصوصيتك. توضح سياسة الخصوصية هذه كيفية جمع المعلومات واستخدامها ومعالجتها وتخزينها ومشاركتها وحمايتها عند استخدام مواقع Runexa ومساحات العمل ووكلاء الذكاء الاصطناعي وأدوات تحليل المستندات والخدمات ذات الصلة.",
      },
      {
        title: "2. المعلومات التي نجمعها",
        text:
          "قد نجمع معلومات الحساب وحالة الفوترة والمعلومات اللازمة لتشغيل الخدمات. تتم معالجة المدفوعات عبر Stripe، ولا تخزن Runexa معلومات بطاقة الدفع على خوادمها الخاصة.",
      },
      {
        title: "3. المحتوى المرفوع",
        text:
          "قد يشمل المحتوى المرفوع العقود والسجلات المالية ومواد الدراسة ومستندات الأعمال والملفات والنصوص وغيرها من المعلومات المقدمة للتحليل. تُعالج الملفات المرفوعة حصرياً لإنشاء التحليل أو النتيجة التي يطلبها المستخدم. تستبدل Runexa المعرّفات الشخصية بعلامات تعريف محايدة قبل المعالجة بالذكاء الاصطناعي. وبعد اكتمال التحليل، يُحذف المحتوى المرفوع والملفات المرتبطة به تلقائياً من مساحة تخزين المعالجة.",
      },
      {
        title: "4. كيف نستخدم بياناتك",
        text:
          "نستخدم البيانات لتقديم الخدمات وصيانتها، وإنشاء مخرجات مدعومة بالذكاء الاصطناعي، وإدارة الحسابات والأرصدة، ومعالجة المدفوعات، وتحسين الاعتمادية وتجربة المستخدم، واكتشاف إساءة الاستخدام، ومنع الاحتيال، وحماية أمان المنصة، والرد على طلبات الدعم، والامتثال للالتزامات القانونية والضريبية والمحاسبية والتنظيمية.",
      },
      {
        title: "5. معالجة الذكاء الاصطناعي",
        text:
          "قد تستخدم خدمات Runexa أنظمة آلية ونماذج ذكاء اصطناعي لاستخراج المعلومات وتصنيفها وتلخيصها وتحليلها وتحويلها وإنشاء معلومات من المحتوى المرفوع. قد تكون مخرجات الذكاء الاصطناعي غير مكتملة أو غير دقيقة ويجب مراجعتها بشكل مستقل قبل اتخاذ قرارات قانونية أو مالية أو تعليمية أو مهنية مهمة.",
      },
      {
        title: "6. تدريب نماذج الذكاء الاصطناعي",
        text:
          "لا تستخدم Runexa المستندات التي يرفعها العملاء أو العقود أو السجلات المالية أو مواد الدراسة أو بيانات الأعمال أو أي محتوى خاص للعملاء لتدريب نماذج ذكاء اصطناعي عامة، ما لم يصرح المستخدم بذلك صراحةً أو يتم الإفصاح عنه بوضوح عندما يسمح القانون المعمول به.",
      },
      {
        title: "7. التخزين ومزودو الخدمة",
        text:
          "قد تستخدم Runexa مزودي بنية تحتية واستضافة وقواعد بيانات وتحليلات ودفع وتخزين وذكاء اصطناعي لتشغيل المنصة. يعالج هؤلاء المزودون المعلومات فقط عند الحاجة لدعم الخدمات والبنية التحتية والأمان والفوترة وسير عمل التحليل الذي يطلبه المستخدم.",
      },
      {
        title: "8. الاحتفاظ بالبيانات والحذف",
        text:
          "تُحذف الملفات المرفوعة من مساحة تخزين المعالجة فور اكتمال التحليل المطلوب. وقد يتم الاحتفاظ ببعض معلومات الحساب، مثل عنوان البريد الإلكتروني، ومعلومات الفوترة اللازمة لتشغيل الحساب والامتثال للالتزامات القانونية، طالما كان ذلك ضرورياً. ويمكن للمستخدمين طلب حذف معلوماتهم الشخصية، مع مراعاة المتطلبات القانونية والأمنية ومتطلبات الفوترة ومنع الاحتيال والاحتفاظ التشغيلي المعمول بها.",
      },
      {
        title: "9. مشاركة البيانات",
        text:
          "لا نبيع معلوماتك الشخصية. قد تتم مشاركة معلومات الحساب المحدودة، مثل عنوان البريد الإلكتروني والبيانات اللازمة للمصادقة، فقط مع المزودين التقنيين الضروريين لتشغيل الخدمة بشكل آمن، أو مزودي الدفع مثل Stripe، أو الجهات المختصة عندما يقتضي القانون ذلك.",
      },
      {
        title: "10. عزل مساحات العمل والوصول الداخلي",
        text:
          "يتم فصل بيانات الحسابات منطقياً بين المستخدمين ومساحات العمل. ولا يمكن لأي مستخدم الوصول إلى المعلومات أو النتائج المرتبطة بحساب مستخدم آخر عبر المنصة. ويكون الوصول التشغيلي، عند الحاجة لأسباب تتعلق بالأمان أو الدعم أو منع إساءة الاستخدام أو المتطلبات القانونية، مقيداً وخاضعاً للرقابة.",
      },
      {
        title: "11. الأمان",
        text:
          "نطبق إجراءات تقنية وإدارية وتنظيمية معقولة مصممة لحماية معلومات المستخدم والمحتوى المرفوع والحسابات وسلامة المنصة. ومع ذلك، لا يمكن ضمان أن أي منصة إنترنت أو برنامج أو نظام ذكاء اصطناعي أو نظام تخزين آمن بالكامل.",
      },
      {
        title: "12. المستخدمون الدوليون ونقل البيانات",
        text:
          "Runexa Systems LLC شركة أمريكية تقدم خدماتها دولياً. إذا كنت تستخدم الخدمات من خارج الولايات المتحدة، فقد يتم نقل معلوماتك أو تخزينها أو معالجتها في الولايات المتحدة أو في ولايات قضائية أخرى يعمل فيها مزودو الخدمة لدينا. عند الحاجة، تستخدم Runexa ضمانات معقولة مصممة لحماية المعلومات الشخصية وفقاً للقانون المعمول به.",
      },
      {
        title: "13. حقوقك",
        text:
          "اعتماداً على موقعك، قد تكون لديك حقوق الوصول أو التصحيح أو الحذف أو التصدير أو التقييد أو الاعتراض على بعض عمليات معالجة معلوماتك الشخصية. يمكنك التواصل معنا لممارسة هذه الحقوق. قد نحتاج إلى التحقق من هويتك قبل الرد على بعض الطلبات.",
      },
      {
        title: "14. ملفات تعريف الارتباط والتقنيات المشابهة",
        text:
          "قد تُستخدم ملفات تعريف الارتباط والتقنيات المشابهة للحفاظ على الجلسات وتذكر التفضيلات وتأمين الحسابات وتحليل الاستخدام واكتشاف إساءة الاستخدام وتحسين تجربة المستخدم. يمكنك إدارة ملفات تعريف الارتباط من خلال إعدادات المتصفح عند توفر ذلك.",
      },
      {
        title: "15. الأطفال والقاصرون",
        text:
          "يمكن استخدام بعض الخدمات التعليمية التي تقدمها Runexa من قبل الأطفال والقاصرين. ولا تجمع Runexa سوى معلومات الحساب اللازمة للوصول إلى الخدمة، مثل عنوان البريد الإلكتروني وبيانات المصادقة المرتبطة بالحساب. وعندما يقتضي القانون المعمول به ذلك، يجب أن يتم استخدام الخدمة من قبل من لم يبلغوا السن القانوني لإدارة الحساب بشكل مستقل بموافقة أو إشراف أحد الوالدين أو الوصي القانوني أو المؤسسة التعليمية.",
      },
      {
        title: "16. معالجة بيانات المؤسسات",
        text:
          "يمكن لعملاء المؤسسات والمنظمات طلب معلومات إضافية تعاقدية أو تشغيلية أو متعلقة بالاحتفاظ أو الأمان أو البنية التحتية عندما تكون متاحة. تبقى المنظمات مسؤولة عن تقييم التزاماتها الخاصة بالامتثال والحوكمة والأمان والمشتريات والمتطلبات التنظيمية عند استخدام خدمات Runexa.",
      },
      {
        title: "17. التغييرات على هذه السياسة",
        text:
          "قد نقوم بتحديث سياسة الخصوصية هذه من وقت لآخر. سيتم نشر النسخ المحدثة على هذه الصفحة مع تاريخ آخر تحديث معدل. يعني استمرار استخدام الخدمات بعد التحديث أن السياسة المحدثة تسري من تاريخ فعاليتها.",
      },
      {
        title: "18. التواصل",
        text:
          "يمكن إرسال الأسئلة أو طلبات الخصوصية أو طلبات الحذف أو استفسارات حماية البيانات إلى contact@runexa.ai.",
      },
    ],
  },
};

export default function PrivacyClient({
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

  const t = privacyCopy[locale];

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
                  href="/security"
                  className="inline-flex items-center justify-center rounded-xl bg-blue-600 px-5 py-3 text-sm font-semibold text-white shadow-sm hover:bg-blue-700"
                >
                  {t.securityLink}
                </a>

                <a
                  href="/contact-entreprise/contact"
                  className="inline-flex items-center justify-center rounded-xl border border-slate-300 bg-white px-5 py-3 text-sm font-semibold text-slate-800 hover:bg-slate-50"
                >
                  {t.contactLink}
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
            {t.flowTitle}
          </h2>

          <div className="mt-8 grid gap-4 md:grid-cols-5">
            {t.flowItems.map(([number, title, text]) => (
              <article
                key={`${number}-${title}`}
                className="rounded-2xl border border-slate-200 bg-slate-50 p-5"
              >
                <div className="flex h-9 w-9 items-center justify-center rounded-full bg-blue-600 text-sm font-bold text-white">
                  {number}
                </div>

                <h3 className="mt-4 font-semibold text-slate-950">
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
