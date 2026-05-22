export const defaultLocale = "en";

export const locales = ["en", "fr", "ar"];

export function getSavedLocale() {
  if (typeof window === "undefined") return defaultLocale;

  const saved = localStorage.getItem("locale");

  if (saved && locales.includes(saved)) {
    return saved;
  }

  return defaultLocale;
}

export function setSavedLocale(locale: string) {
  if (!locales.includes(locale)) return;

  localStorage.setItem("locale", locale);
  window.dispatchEvent(new Event("locale-change"));
}

export const translations: any = {
  en: {
    slogan: "AI agents that get things done",
    dashboard: "Dashboard",
    admin: "Admin",
    enterprise: "Business",
    pricing: "Pricing",
    logout: "Logout",
    login: "Login",
    register: "Register",

    footerDesc:
      "AI agents for legal analysis, learning, personal finance, and business decision-making.",

    companyAddress:
      "Runexa Systems LLC\n1309 Coffeen Avenue, Suite 1200\nSheridan, WY 82801, USA",

    products: "Products",
    legalAgent: "Legal Agent",
    studyAgent: "Study Agent",
    financeAgent: "Personal Finance Coach Agent",
    hrAgent: "HR Agent",
    businessAgent: "Business Decision Agent",
    available: "Available",
    comingSoon: "Coming soon",

    platform: "Platform",
    exploreAgents: "Explore agents",
    tryLegalAgent: "Try Legal Agent",
    tryStudyAgent: "Try Study Agent",
    tryFinanceAgent: "Try Finance Coach",

    about: "About",
    aboutText:
      "Runexa Systems is a platform of AI agents that help users analyze documents, learn faster, manage personal finance, and make smarter business decisions.",

    developedBy: "Developed by Dr. Rachid Ejjami",
    copyright: "© 2026 Runexa Systems LLC. All rights reserved.",

    privacy: "Privacy Policy",
    terms: "Terms of Service",
    contact: "Contact",

    securityTitle: "Security",
    securityUpdated: "Last Updated: May 2026",
    securityOverviewTitle: "1. Overview",
    securityOverviewText:
      "Runexa Systems LLC is committed to maintaining reasonable technical, organizational, and administrative safeguards designed to protect user information, platform integrity, and AI infrastructure.",

    securityInfrastructureTitle: "2. Infrastructure and Hosting",
    securityInfrastructureText:
      "Runexa services may use secure cloud infrastructure providers, hosting providers, database providers, AI providers, and payment processors to operate the platform.",

    securityEncryptionTitle: "3. Encryption and Secure Connections",
    securityEncryptionText:
      "Data transmitted between users and the platform may be protected using encrypted communication protocols such as HTTPS and TLS where applicable.",

    securityAccessTitle: "4. Access Controls",
    securityAccessText:
      "Access to systems, accounts, infrastructure, and operational tools may be restricted to authorized personnel and protected through authentication and security controls.",

    securityMonitoringTitle: "5. Monitoring and Abuse Prevention",
    securityMonitoringText:
      "Runexa Systems LLC may monitor platform activity, logs, access attempts, and system behavior to detect abuse, fraud, unauthorized access, or security threats.",

    securityPaymentTitle: "6. Payment Security",
    securityPaymentText:
      "Payments may be processed by trusted third-party payment providers. Runexa Systems LLC does not store full payment card information on its own servers.",

    securityUserTitle: "7. User Responsibility",
    securityUserText1:
      "Users are responsible for maintaining the confidentiality of their accounts, passwords, devices, and uploaded information.",

    securityUserText2:
      "Users should avoid uploading highly sensitive information unless necessary and appropriate safeguards are in place.",

    securityGuaranteeTitle: "8. No Absolute Security Guarantee",
    securityGuaranteeText:
      "While Runexa Systems LLC implements reasonable safeguards, no internet-based platform, software, AI system, or storage system can be guaranteed to be completely secure.",

    securityReportTitle: "9. Reporting Security Issues",
    securityReportText:
      "Security concerns, vulnerabilities, or suspected abuse may be reported to:",

    privacyTitle: "Privacy Policy",
    privacyUpdated: "Last Updated: May 2026",
    privacyIntroTitle: "1. Introduction",
    privacyIntroText:
      "Runexa Systems LLC (“we”, “our”, “us”) respects your privacy. This Privacy Policy explains how we collect, use, store, share, and protect information when you use Runexa and its AI-powered services.",

    privacyCollectTitle: "2. Information We Collect",
    privacyAccountTitle: "2.1 Account Information",
    privacyAccountText:
      "We may collect your email address, encrypted password, account status, billing status, and authentication-related information.",
    privacyUploadTitle: "2.2 Uploaded Content",
    privacyUploadText:
      "We may process documents, files, text, financial information, study materials, business data, and other content you upload for analysis.",
    privacyUsageTitle: "2.3 Usage Data",
    privacyUsageText:
      "We may collect IP address, browser type, device information, pages visited, feature usage, logs, error reports, and security-related data.",
    privacyPaymentTitle: "2.4 Payment Information",
    privacyPaymentText:
      "Payments may be processed by third-party payment providers. We do not store full payment card details on our servers.",

    privacyUseTitle: "3. How We Use Your Data",
    privacyUse1: "Provide, operate, and maintain the services",
    privacyUse2: "Analyze documents and generate AI-powered outputs",
    privacyUse3: "Manage accounts, credits, payments, and access",
    privacyUse4:
      "Improve product performance, reliability, and user experience",
    privacyUse5:
      "Detect abuse, prevent fraud, and protect platform security",
    privacyUse6:
      "Comply with legal, tax, accounting, and regulatory obligations",

    privacyAiTitle: "4. AI Processing",
    privacyAiText:
      "Uploaded content may be processed by AI systems and infrastructure providers for extraction, analysis, summarization, classification, and generation of outputs. AI-generated outputs may be inaccurate or incomplete and should be independently verified.",

    privacyStorageTitle: "5. Data Storage and Providers",
    privacyStorageText:
      "Data may be stored and processed using secure third-party infrastructure, hosting, analytics, payment, database, and AI service providers that help us operate the services.",

    privacySharingTitle: "6. Data Sharing",
    privacySharingText:
      "We do not sell your personal information. We may share information only with service providers, payment processors, infrastructure providers, legal authorities when required by law, or in connection with a business transaction such as a merger, acquisition, or asset transfer.",

    privacyRetentionTitle: "7. Data Retention",
    privacyRetentionText:
      "We retain information only as long as reasonably necessary to provide the services, comply with legal obligations, resolve disputes, prevent abuse, and enforce our agreements. You may request deletion of your data, subject to legal and operational retention requirements.",

    privacySecurityTitle: "8. Security",
    privacySecurityText:
      "We implement reasonable technical, administrative, and organizational measures designed to protect your information. However, no method of transmission or storage is completely secure, and we cannot guarantee absolute security.",

    privacyInternationalTitle: "9. International Users",
    privacyInternationalText:
      "If you access the services from outside the United States, your information may be transferred to, stored in, or processed in the United States or other jurisdictions where our service providers operate.",

    privacyRightsTitle: "10. Your Rights",
    privacyRightsText:
      "Depending on your location, you may have rights to access, correct, delete, export, restrict, or object to certain processing of your personal information. You may contact us to exercise these rights.",

    privacyCookiesTitle: "11. Cookies",
    privacyCookiesText:
      "Cookies and similar technologies may be used to maintain sessions, remember preferences, secure accounts, analyze usage, and improve the user experience.",

    privacyChildrenTitle: "12. Children",
    privacyChildrenText:
      "The services are not intended for users under 18 years old. We do not knowingly collect personal information from children under 18.",

    privacyChangesTitle: "13. Changes",
    privacyChangesText:
      "We may update this Privacy Policy from time to time. Updated versions will be posted on this page with a revised “Last updated” date.",

    privacyContactTitle: "14. Contact",

    termsTitle: "Terms of Service",
    termsUpdated: "Last updated: May 2026",

    termsOverviewTitle: "1. Overview",
    termsOverviewText1:
      "Runexa Systems LLC provides access to AI-powered tools designed to assist users in analyzing documents, generating insights, and using specialized AI agents.",
    termsOverviewText2:
      "By accessing or using Runexa, you agree to these Terms of Service.",

    termsEligibilityTitle: "2. Eligibility",
    termsEligibilityText:
      "You must be at least 18 years old to use the services.",

    termsAccountTitle: "3. Account",
    termsAccountText:
      "You are responsible for maintaining the security of your account, your login credentials, and all activity under your account.",

    termsUseTitle: "4. Use of Services",
    termsUse1:
      "You may not use the services for illegal, harmful, or fraudulent activity.",
    termsUse2:
      "You may not upload data, documents, or content that you do not have the right to use.",
    termsUse3:
      "You may not abuse, disrupt, reverse engineer, or attempt to bypass the platform.",
    termsUse4:
      "You may not use the services to infringe intellectual property, privacy, or third-party rights.",

    termsAiTitle: "5. AI Services",
    termsAiText1:
      "AI-generated outputs may be inaccurate, incomplete, outdated, or misleading. Outputs may contain errors or omissions.",
    termsAiText2:
      "You are responsible for independently reviewing and verifying all outputs before relying on them or taking action.",

    termsBillingTitle: "6. Payments, Credits, and Billing",
    termsBillingText:
      "Paid trials, credits, subscriptions, and plans are subject to the pricing shown at the time of purchase. Credits are non-refundable unless required by law.",

    termsDataTitle: "7. Data Usage",
    termsDataText:
      "You retain ownership of the data and content you upload. Runexa Systems LLC processes your data only to provide, secure, maintain, and improve the services, as described in the Privacy Policy.",

    termsIpTitle: "8. Intellectual Property",
    termsIpText:
      "Runexa Systems LLC owns all rights, title, and interest in the platform, software, interfaces, designs, branding, AI agent workflows, and related technology.",

    termsLiabilityTitle: "9. Limitation of Liability",
    termsLiabilityText:
      "To the maximum extent permitted by law, Runexa Systems LLC is not liable for indirect, incidental, special, consequential, or punitive damages, including business losses, financial losses, legal disputes, loss of data, or consequences resulting from misuse or reliance on AI outputs.",

    termsTerminationTitle: "10. Termination",
    termsTerminationText:
      "Runexa Systems LLC may suspend or terminate access to the services if these Terms are violated or if use of the services creates legal, security, operational, or reputational risk.",

    termsLawTitle: "11. Governing Law",
    termsLawText:
      "These Terms are governed by the laws of the State of Wyoming, United States, without regard to conflict of law principles.",

    termsChangesTitle: "12. Changes",
    termsChangesText:
      "Runexa Systems LLC may update these Terms from time to time. Updated Terms will be posted on this page with a revised “Last updated” date.",

    termsContactTitle: "13. Contact",
  },

  fr: {
    slogan: "Des agents IA qui vous aident à avancer",
    dashboard: "Tableau de bord",
    admin: "Admin",
    enterprise: "Entreprises",
    pricing: "Tarifs",
    logout: "Déconnexion",
    login: "Connexion",
    register: "Inscription",

    footerDesc:
      "Agents IA pour l’analyse juridique, l’apprentissage, la gestion financière personnelle et la prise de décision business.",

    companyAddress:
      "Runexa Systems LLC\n1309 Coffeen Avenue, Suite 1200\nSheridan, WY 82801, États-Unis",

    products: "Produits",
    legalAgent: "Agent juridique",
    studyAgent: "Agent étude",
    financeAgent: "Agent coach financier personnel",
    hrAgent: "Agent RH",
    businessAgent: "Agent décision business",
    available: "Disponible",
    comingSoon: "Bientôt",

    platform: "Plateforme",
    exploreAgents: "Explorer les agents",
    tryLegalAgent: "Tester l’agent juridique",
    tryStudyAgent: "Tester l’agent étude",
    tryFinanceAgent: "Tester le coach financier",

    about: "À propos",
    aboutText:
      "Runexa Systems est une plateforme d’agents IA qui aide les utilisateurs à analyser leurs documents, apprendre plus vite, gérer leurs finances personnelles et prendre de meilleures décisions business.",

    developedBy: "Développé par Dr. Rachid Ejjami",
    copyright: "© 2026 Runexa Systems LLC. Tous droits réservés.",

    privacy: "Confidentialité",
    terms: "Conditions",
    contact: "Contact",

    securityTitle: "Sécurité",
    securityUpdated: "Dernière mise à jour : mai 2026",
    securityOverviewTitle: "1. Présentation",
    securityOverviewText:
      "Runexa Systems LLC s’engage à maintenir des mesures techniques, organisationnelles et administratives raisonnables afin de protéger les informations des utilisateurs, l’intégrité de la plateforme et l’infrastructure IA.",

    securityInfrastructureTitle: "2. Infrastructure et hébergement",
    securityInfrastructureText:
      "Les services Runexa peuvent utiliser des fournisseurs sécurisés d’infrastructure cloud, d’hébergement, de bases de données, de services IA et de paiement afin d’exploiter la plateforme.",

    securityEncryptionTitle: "3. Chiffrement et connexions sécurisées",
    securityEncryptionText:
      "Les données transmises entre les utilisateurs et la plateforme peuvent être protégées via des protocoles de communication chiffrés tels que HTTPS et TLS lorsque cela est applicable.",

    securityAccessTitle: "4. Contrôles d’accès",
    securityAccessText:
      "L’accès aux systèmes, comptes, infrastructures et outils opérationnels peut être limité au personnel autorisé et protégé par des mécanismes d’authentification et de sécurité.",

    securityMonitoringTitle: "5. Surveillance et prévention des abus",
    securityMonitoringText:
      "Runexa Systems LLC peut surveiller l’activité de la plateforme, les journaux, les tentatives d’accès et le comportement système afin de détecter les abus, fraudes, accès non autorisés ou menaces de sécurité.",

    securityPaymentTitle: "6. Sécurité des paiements",
    securityPaymentText:
      "Les paiements peuvent être traités par des prestataires tiers de confiance. Runexa Systems LLC ne stocke pas les informations complètes des cartes de paiement sur ses propres serveurs.",

    securityUserTitle: "7. Responsabilité de l’utilisateur",
    securityUserText1:
      "Les utilisateurs sont responsables de la confidentialité de leurs comptes, mots de passe, appareils et informations téléchargées.",

    securityUserText2:
      "Les utilisateurs doivent éviter de télécharger des informations hautement sensibles sauf si cela est nécessaire et que des protections appropriées sont en place.",

    securityGuaranteeTitle: "8. Aucune garantie de sécurité absolue",
    securityGuaranteeText:
      "Bien que Runexa Systems LLC mette en œuvre des mesures de protection raisonnables, aucune plateforme internet, logiciel, système IA ou système de stockage ne peut être garanti totalement sécurisé.",

    securityReportTitle: "9. Signalement des problèmes de sécurité",
    securityReportText:
      "Les problèmes de sécurité, vulnérabilités ou abus suspects peuvent être signalés à :",

    privacyTitle: "Politique de confidentialité",
    privacyUpdated: "Dernière mise à jour : mai 2026",
    privacyIntroTitle: "1. Introduction",
    privacyIntroText:
      "Runexa Systems LLC (« nous », « notre », « nos ») respecte votre vie privée. Cette Politique de confidentialité explique comment nous collectons, utilisons, stockons, partageons et protégeons les informations lorsque vous utilisez Runexa et ses services alimentés par l’IA.",

    privacyCollectTitle: "2. Informations que nous collectons",
    privacyAccountTitle: "2.1 Informations de compte",
    privacyAccountText:
      "Nous pouvons collecter votre adresse e-mail, votre mot de passe chiffré, le statut de votre compte, le statut de facturation et les informations liées à l’authentification.",
    privacyUploadTitle: "2.2 Contenu téléchargé",
    privacyUploadText:
      "Nous pouvons traiter les documents, fichiers, textes, informations financières, supports d’étude, données business et autres contenus que vous téléchargez pour analyse.",
    privacyUsageTitle: "2.3 Données d’utilisation",
    privacyUsageText:
      "Nous pouvons collecter l’adresse IP, le type de navigateur, les informations sur l’appareil, les pages visitées, l’utilisation des fonctionnalités, les journaux, les rapports d’erreurs et les données liées à la sécurité.",
    privacyPaymentTitle: "2.4 Informations de paiement",
    privacyPaymentText:
      "Les paiements peuvent être traités par des prestataires de paiement tiers. Nous ne stockons pas les informations complètes des cartes de paiement sur nos serveurs.",

    privacyUseTitle: "3. Comment nous utilisons vos données",
    privacyUse1: "Fournir, exploiter et maintenir les services",
    privacyUse2: "Analyser les documents et générer des résultats alimentés par l’IA",
    privacyUse3: "Gérer les comptes, crédits, paiements et accès",
    privacyUse4:
      "Améliorer les performances, la fiabilité et l’expérience utilisateur du produit",
    privacyUse5:
      "Détecter les abus, prévenir la fraude et protéger la sécurité de la plateforme",
    privacyUse6:
      "Respecter les obligations légales, fiscales, comptables et réglementaires",

    privacyAiTitle: "4. Traitement par IA",
    privacyAiText:
      "Le contenu téléchargé peut être traité par des systèmes d’IA et des fournisseurs d’infrastructure pour l’extraction, l’analyse, la synthèse, la classification et la génération de résultats. Les résultats générés par l’IA peuvent être inexacts ou incomplets et doivent être vérifiés de manière indépendante.",

    privacyStorageTitle: "5. Stockage des données et prestataires",
    privacyStorageText:
      "Les données peuvent être stockées et traitées à l’aide de prestataires tiers sécurisés d’infrastructure, d’hébergement, d’analyse, de paiement, de base de données et de services IA qui nous aident à exploiter les services.",

    privacySharingTitle: "6. Partage des données",
    privacySharingText:
      "Nous ne vendons pas vos informations personnelles. Nous pouvons partager des informations uniquement avec des prestataires de services, processeurs de paiement, fournisseurs d’infrastructure, autorités légales lorsque la loi l’exige, ou dans le cadre d’une transaction commerciale telle qu’une fusion, acquisition ou cession d’actifs.",

    privacyRetentionTitle: "7. Conservation des données",
    privacyRetentionText:
      "Nous conservons les informations uniquement aussi longtemps que raisonnablement nécessaire pour fournir les services, respecter nos obligations légales, résoudre les litiges, prévenir les abus et faire respecter nos accords. Vous pouvez demander la suppression de vos données, sous réserve des exigences légales et opérationnelles de conservation.",

    privacySecurityTitle: "8. Sécurité",
    privacySecurityText:
      "Nous mettons en œuvre des mesures techniques, administratives et organisationnelles raisonnables destinées à protéger vos informations. Cependant, aucune méthode de transmission ou de stockage n’est totalement sécurisée et nous ne pouvons pas garantir une sécurité absolue.",

    privacyInternationalTitle: "9. Utilisateurs internationaux",
    privacyInternationalText:
      "Si vous accédez aux services depuis l’extérieur des États-Unis, vos informations peuvent être transférées, stockées ou traitées aux États-Unis ou dans d’autres juridictions où nos prestataires opèrent.",

    privacyRightsTitle: "10. Vos droits",
    privacyRightsText:
      "Selon votre localisation, vous pouvez disposer de droits d’accès, de correction, de suppression, d’exportation, de restriction ou d’opposition à certains traitements de vos informations personnelles. Vous pouvez nous contacter pour exercer ces droits.",

    privacyCookiesTitle: "11. Cookies",
    privacyCookiesText:
      "Les cookies et technologies similaires peuvent être utilisés pour maintenir les sessions, mémoriser les préférences, sécuriser les comptes, analyser l’utilisation et améliorer l’expérience utilisateur.",

    privacyChildrenTitle: "12. Enfants",
    privacyChildrenText:
      "Les services ne sont pas destinés aux utilisateurs de moins de 18 ans. Nous ne collectons pas sciemment d’informations personnelles auprès d’enfants de moins de 18 ans.",

    privacyChangesTitle: "13. Modifications",
    privacyChangesText:
      "Nous pouvons mettre à jour cette Politique de confidentialité de temps à autre. Les versions mises à jour seront publiées sur cette page avec une date de « Dernière mise à jour » révisée.",

    privacyContactTitle: "14. Contact",

    termsTitle: "Conditions d’utilisation",
    termsUpdated: "Dernière mise à jour : mai 2026",

    termsOverviewTitle: "1. Présentation",
    termsOverviewText1:
      "Runexa Systems LLC fournit un accès à des outils alimentés par l’IA conçus pour aider les utilisateurs à analyser des documents, générer des informations et utiliser des agents IA spécialisés.",
    termsOverviewText2:
      "En accédant à Runexa ou en l’utilisant, vous acceptez ces Conditions d’utilisation.",

    termsEligibilityTitle: "2. Éligibilité",
    termsEligibilityText:
      "Vous devez avoir au moins 18 ans pour utiliser les services.",

    termsAccountTitle: "3. Compte",
    termsAccountText:
      "Vous êtes responsable de la sécurité de votre compte, de vos identifiants de connexion et de toute activité effectuée sous votre compte.",

    termsUseTitle: "4. Utilisation des services",
    termsUse1:
      "Vous ne pouvez pas utiliser les services pour une activité illégale, nuisible ou frauduleuse.",
    termsUse2:
      "Vous ne pouvez pas téléverser des données, documents ou contenus que vous n’avez pas le droit d’utiliser.",
    termsUse3:
      "Vous ne pouvez pas abuser de la plateforme, la perturber, faire de l’ingénierie inverse ou tenter de contourner ses protections.",
    termsUse4:
      "Vous ne pouvez pas utiliser les services pour porter atteinte à la propriété intellectuelle, à la vie privée ou aux droits de tiers.",

    termsAiTitle: "5. Services d’IA",
    termsAiText1:
      "Les résultats générés par l’IA peuvent être inexacts, incomplets, obsolètes ou trompeurs. Ils peuvent contenir des erreurs ou omissions.",
    termsAiText2:
      "Vous êtes responsable de vérifier et d’examiner indépendamment tous les résultats avant de vous y fier ou d’agir sur leur base.",

    termsBillingTitle: "6. Paiements, crédits et facturation",
    termsBillingText:
      "Les essais payants, crédits, abonnements et plans sont soumis aux prix affichés au moment de l’achat. Les crédits ne sont pas remboursables sauf si la loi l’exige.",

    termsDataTitle: "7. Utilisation des données",
    termsDataText:
      "Vous conservez la propriété des données et contenus que vous téléversez. Runexa Systems LLC traite vos données uniquement pour fournir, sécuriser, maintenir et améliorer les services, comme décrit dans la Politique de confidentialité.",

    termsIpTitle: "8. Propriété intellectuelle",
    termsIpText:
      "Runexa Systems LLC détient tous les droits, titres et intérêts relatifs à la plateforme, aux logiciels, interfaces, designs, marques, workflows des agents IA et technologies associées.",

    termsLiabilityTitle: "9. Limitation de responsabilité",
    termsLiabilityText:
      "Dans toute la mesure permise par la loi, Runexa Systems LLC n’est pas responsable des dommages indirects, accessoires, spéciaux, consécutifs ou punitifs, y compris les pertes commerciales, pertes financières, litiges juridiques, pertes de données ou conséquences résultant d’une mauvaise utilisation ou d’une confiance accordée aux résultats de l’IA.",

    termsTerminationTitle: "10. Résiliation",
    termsTerminationText:
      "Runexa Systems LLC peut suspendre ou résilier l’accès aux services si ces Conditions sont violées ou si l’utilisation des services crée un risque juridique, de sécurité, opérationnel ou réputationnel.",

    termsLawTitle: "11. Droit applicable",
    termsLawText:
      "Ces Conditions sont régies par les lois de l’État du Wyoming, États-Unis, sans tenir compte des principes de conflit de lois.",

    termsChangesTitle: "12. Modifications",
    termsChangesText:
      "Runexa Systems LLC peut mettre à jour ces Conditions de temps à autre. Les Conditions mises à jour seront publiées sur cette page avec une date de « Dernière mise à jour » révisée.",

    termsContactTitle: "13. Contact",
  },

  ar: {
    slogan: "وكلاء ذكاء اصطناعي يساعدونك على إنجاز العمل",
    dashboard: "لوحة التحكم",
    admin: "الإدارة",
    enterprise: "الأعمال",
    pricing: "الأسعار",
    logout: "تسجيل الخروج",
    login: "تسجيل الدخول",
    register: "إنشاء حساب",

    footerDesc:
      "وكلاء ذكاء اصطناعي للتحليل القانوني والتعلم والإدارة المالية الشخصية واتخاذ قرارات الأعمال.",

    companyAddress:
      "Runexa Systems LLC\n1309 Coffeen Avenue, Suite 1200\nSheridan, WY 82801, الولايات المتحدة",

    products: "المنتجات",
    legalAgent: "الوكيل القانوني",
    studyAgent: "وكيل الدراسة",
    financeAgent: "وكيل الإدارة المالية الشخصية",
    hrAgent: "وكيل الموارد البشرية",
    businessAgent: "وكيل قرارات الأعمال",
    available: "متاح",
    comingSoon: "قريباً",

    platform: "المنصة",
    exploreAgents: "استكشاف الوكلاء",
    tryLegalAgent: "تجربة الوكيل القانوني",
    tryStudyAgent: "تجربة وكيل الدراسة",
    tryFinanceAgent: "تجربة وكيل الإدارة المالية",

    about: "حول",
    aboutText:
      "Runexa Systems منصة لوكلاء ذكاء اصطناعي تساعد المستخدمين على تحليل المستندات والتعلم بشكل أسرع وإدارة المالية الشخصية واتخاذ قرارات أعمال أكثر ذكاءً.",

    developedBy: "تم التطوير بواسطة Dr. Rachid Ejjami",
    copyright: "© 2026 Runexa Systems LLC. جميع الحقوق محفوظة.",

    privacy: "الخصوصية",
    terms: "الشروط",
    contact: "اتصال",

    securityTitle: "الأمان",
    securityUpdated: "آخر تحديث: مايو 2026",
    securityOverviewTitle: "1. نظرة عامة",
    securityOverviewText:
      "تلتزم Runexa Systems LLC بالحفاظ على تدابير تقنية وتنظيمية وإدارية معقولة لحماية معلومات المستخدم وسلامة المنصة والبنية التحتية للذكاء الاصطناعي.",

    securityInfrastructureTitle: "2. البنية التحتية والاستضافة",
    securityInfrastructureText:
      "قد تستخدم خدمات Runexa مزودي بنية تحتية سحابية واستضافة وقواعد بيانات وخدمات ذكاء اصطناعي ومعالجات دفع آمنة لتشغيل المنصة.",

    securityEncryptionTitle: "3. التشفير والاتصالات الآمنة",
    securityEncryptionText:
      "قد تتم حماية البيانات المنقولة بين المستخدمين والمنصة باستخدام بروتوكولات اتصال مشفرة مثل HTTPS وTLS عند الاقتضاء.",

    securityAccessTitle: "4. ضوابط الوصول",
    securityAccessText:
      "قد يقتصر الوصول إلى الأنظمة والحسابات والبنية التحتية والأدوات التشغيلية على الموظفين المصرح لهم مع حمايتها بوسائل المصادقة والأمان.",

    securityMonitoringTitle: "5. المراقبة ومنع إساءة الاستخدام",
    securityMonitoringText:
      "قد تقوم Runexa Systems LLC بمراقبة نشاط المنصة والسجلات ومحاولات الوصول وسلوك النظام لاكتشاف إساءة الاستخدام أو الاحتيال أو الوصول غير المصرح به أو التهديدات الأمنية.",

    securityPaymentTitle: "6. أمان المدفوعات",
    securityPaymentText:
      "قد تتم معالجة المدفوعات بواسطة مزودي خدمات دفع موثوقين من جهات خارجية. لا تقوم Runexa Systems LLC بتخزين معلومات بطاقات الدفع الكاملة على خوادمها الخاصة.",

    securityUserTitle: "7. مسؤولية المستخدم",
    securityUserText1:
      "المستخدمون مسؤولون عن الحفاظ على سرية حساباتهم وكلمات المرور والأجهزة والمعلومات المرفوعة.",

    securityUserText2:
      "يجب على المستخدمين تجنب رفع المعلومات شديدة الحساسية إلا عند الضرورة ومع وجود وسائل حماية مناسبة.",

    securityGuaranteeTitle: "8. عدم وجود ضمان أمني مطلق",
    securityGuaranteeText:
      "على الرغم من أن Runexa Systems LLC تطبق تدابير حماية معقولة، فلا يمكن ضمان أن أي منصة أو برنامج أو نظام ذكاء اصطناعي أو نظام تخزين متصل بالإنترنت آمن بالكامل.",

    securityReportTitle: "9. الإبلاغ عن المشكلات الأمنية",
    securityReportText:
      "يمكن الإبلاغ عن المخاوف الأمنية أو الثغرات أو حالات إساءة الاستخدام المشتبه بها عبر:",

    privacyTitle: "سياسة الخصوصية",
    privacyUpdated: "آخر تحديث: مايو 2026",
    privacyIntroTitle: "1. المقدمة",
    privacyIntroText:
      "تحترم Runexa Systems LLC (“نحن”) خصوصيتك. توضح سياسة الخصوصية هذه كيفية جمع المعلومات واستخدامها وتخزينها ومشاركتها وحمايتها عند استخدام Runexa وخدماتها المدعومة بالذكاء الاصطناعي.",

    privacyCollectTitle: "2. المعلومات التي نجمعها",
    privacyAccountTitle: "2.1 معلومات الحساب",
    privacyAccountText:
      "قد نجمع عنوان بريدك الإلكتروني وكلمة المرور المشفرة وحالة الحساب وحالة الفوترة والمعلومات المتعلقة بالمصادقة.",
    privacyUploadTitle: "2.2 المحتوى المرفوع",
    privacyUploadText:
      "قد نعالج المستندات والملفات والنصوص والمعلومات المالية ومواد الدراسة وبيانات الأعمال والمحتوى الآخر الذي ترفعه للتحليل.",
    privacyUsageTitle: "2.3 بيانات الاستخدام",
    privacyUsageText:
      "قد نجمع عنوان IP ونوع المتصفح ومعلومات الجهاز والصفحات التي تمت زيارتها واستخدام الميزات والسجلات وتقارير الأخطاء والبيانات المتعلقة بالأمان.",
    privacyPaymentTitle: "2.4 معلومات الدفع",
    privacyPaymentText:
      "قد تتم معالجة المدفوعات بواسطة مزودي خدمات دفع تابعين لجهات خارجية. نحن لا نخزن تفاصيل بطاقات الدفع الكاملة على خوادمنا.",

    privacyUseTitle: "3. كيفية استخدام بياناتك",
    privacyUse1: "توفير الخدمات وتشغيلها وصيانتها",
    privacyUse2: "تحليل المستندات وإنشاء مخرجات مدعومة بالذكاء الاصطناعي",
    privacyUse3: "إدارة الحسابات والأرصدة والمدفوعات والوصول",
    privacyUse4:
      "تحسين أداء المنتج وموثوقيته وتجربة المستخدم",
    privacyUse5:
      "اكتشاف إساءة الاستخدام ومنع الاحتيال وحماية أمان المنصة",
    privacyUse6:
      "الامتثال للالتزامات القانونية والضريبية والمحاسبية والتنظيمية",

    privacyAiTitle: "4. المعالجة بالذكاء الاصطناعي",
    privacyAiText:
      "قد تتم معالجة المحتوى المرفوع بواسطة أنظمة الذكاء الاصطناعي ومزودي البنية التحتية لأغراض الاستخراج والتحليل والتلخيص والتصنيف وإنشاء المخرجات. قد تكون المخرجات الناتجة عن الذكاء الاصطناعي غير دقيقة أو غير مكتملة ويجب التحقق منها بشكل مستقل.",

    privacyStorageTitle: "5. تخزين البيانات ومزودو الخدمات",
    privacyStorageText:
      "قد يتم تخزين البيانات ومعالجتها باستخدام مزودي خدمات آمنين من جهات خارجية للبنية التحتية والاستضافة والتحليلات والدفع وقواعد البيانات وخدمات الذكاء الاصطناعي التي تساعدنا على تشغيل الخدمات.",

    privacySharingTitle: "6. مشاركة البيانات",
    privacySharingText:
      "نحن لا نبيع معلوماتك الشخصية. قد نشارك المعلومات فقط مع مزودي الخدمات ومعالجي الدفع ومزودي البنية التحتية والسلطات القانونية عندما يقتضي القانون ذلك، أو فيما يتعلق بعملية تجارية مثل الاندماج أو الاستحواذ أو نقل الأصول.",

    privacyRetentionTitle: "7. الاحتفاظ بالبيانات",
    privacyRetentionText:
      "نحتفظ بالمعلومات فقط للمدة المعقولة اللازمة لتوفير الخدمات والامتثال للالتزامات القانونية وحل النزاعات ومنع إساءة الاستخدام وإنفاذ اتفاقياتنا. يمكنك طلب حذف بياناتك، مع مراعاة متطلبات الاحتفاظ القانونية والتشغيلية.",

    privacySecurityTitle: "8. الأمان",
    privacySecurityText:
      "نطبق تدابير تقنية وإدارية وتنظيمية معقولة مصممة لحماية معلوماتك. ومع ذلك، لا توجد طريقة نقل أو تخزين آمنة بالكامل، ولا يمكننا ضمان الأمان المطلق.",

    privacyInternationalTitle: "9. المستخدمون الدوليون",
    privacyInternationalText:
      "إذا كنت تصل إلى الخدمات من خارج الولايات المتحدة، فقد يتم نقل معلوماتك أو تخزينها أو معالجتها في الولايات المتحدة أو في ولايات قضائية أخرى يعمل فيها مزودو خدماتنا.",

    privacyRightsTitle: "10. حقوقك",
    privacyRightsText:
      "اعتمادًا على موقعك، قد تكون لديك حقوق في الوصول إلى معلوماتك الشخصية أو تصحيحها أو حذفها أو تصديرها أو تقييد معالجتها أو الاعتراض على بعض عمليات المعالجة. يمكنك التواصل معنا لممارسة هذه الحقوق.",

    privacyCookiesTitle: "11. ملفات تعريف الارتباط",
    privacyCookiesText:
      "قد تُستخدم ملفات تعريف الارتباط والتقنيات المشابهة للحفاظ على الجلسات وتذكر التفضيلات وتأمين الحسابات وتحليل الاستخدام وتحسين تجربة المستخدم.",

    privacyChildrenTitle: "12. الأطفال",
    privacyChildrenText:
      "الخدمات غير مخصصة للمستخدمين الذين تقل أعمارهم عن 18 عامًا. نحن لا نجمع عن علم معلومات شخصية من الأطفال دون سن 18 عامًا.",

    privacyChangesTitle: "13. التغييرات",
    privacyChangesText:
      "قد نقوم بتحديث سياسة الخصوصية هذه من وقت لآخر. سيتم نشر الإصدارات المحدثة على هذه الصفحة مع تاريخ “آخر تحديث” معدل.",

    privacyContactTitle: "14. الاتصال",

    termsTitle: "شروط الخدمة",
    termsUpdated: "آخر تحديث: مايو 2026",

    termsOverviewTitle: "1. نظرة عامة",
    termsOverviewText1:
      "توفر Runexa Systems LLC إمكانية الوصول إلى أدوات مدعومة بالذكاء الاصطناعي مصممة لمساعدة المستخدمين على تحليل المستندات وتوليد الرؤى واستخدام وكلاء ذكاء اصطناعي متخصصين.",
    termsOverviewText2:
      "من خلال الوصول إلى Runexa أو استخدامها، فإنك توافق على شروط الخدمة هذه.",

    termsEligibilityTitle: "2. الأهلية",
    termsEligibilityText:
      "يجب أن يكون عمرك 18 عامًا على الأقل لاستخدام الخدمات.",

    termsAccountTitle: "3. الحساب",
    termsAccountText:
      "أنت مسؤول عن الحفاظ على أمان حسابك وبيانات تسجيل الدخول الخاصة بك وجميع الأنشطة التي تتم من خلال حسابك.",

    termsUseTitle: "4. استخدام الخدمات",
    termsUse1:
      "لا يجوز لك استخدام الخدمات في أي نشاط غير قانوني أو ضار أو احتيالي.",
    termsUse2:
      "لا يجوز لك رفع بيانات أو مستندات أو محتوى لا تملك الحق في استخدامه.",
    termsUse3:
      "لا يجوز لك إساءة استخدام المنصة أو تعطيلها أو إجراء هندسة عكسية لها أو محاولة تجاوزها.",
    termsUse4:
      "لا يجوز لك استخدام الخدمات لانتهاك حقوق الملكية الفكرية أو الخصوصية أو حقوق الأطراف الثالثة.",

    termsAiTitle: "5. خدمات الذكاء الاصطناعي",
    termsAiText1:
      "قد تكون المخرجات الناتجة عن الذكاء الاصطناعي غير دقيقة أو غير مكتملة أو قديمة أو مضللة. وقد تحتوي على أخطاء أو سهو.",
    termsAiText2:
      "أنت مسؤول عن مراجعة جميع المخرجات والتحقق منها بشكل مستقل قبل الاعتماد عليها أو اتخاذ أي إجراء بناءً عليها.",

    termsBillingTitle: "6. المدفوعات والأرصدة والفوترة",
    termsBillingText:
      "تخضع التجارب المدفوعة والأرصدة والاشتراكات والخطط للأسعار المعروضة وقت الشراء. الأرصدة غير قابلة للاسترداد إلا إذا تطلب القانون ذلك.",

    termsDataTitle: "7. استخدام البيانات",
    termsDataText:
      "تحتفظ بملكية البيانات والمحتوى الذي ترفعه. تعالج Runexa Systems LLC بياناتك فقط لتوفير الخدمات وتأمينها وصيانتها وتحسينها، كما هو موضح في سياسة الخصوصية.",

    termsIpTitle: "8. الملكية الفكرية",
    termsIpText:
      "تمتلك Runexa Systems LLC جميع الحقوق والملكية والمصالح في المنصة والبرمجيات والواجهات والتصاميم والعلامات التجارية وسير عمل وكلاء الذكاء الاصطناعي والتقنيات ذات الصلة.",

    termsLiabilityTitle: "9. تحديد المسؤولية",
    termsLiabilityText:
      "إلى أقصى حد يسمح به القانون، لا تكون Runexa Systems LLC مسؤولة عن الأضرار غير المباشرة أو العرضية أو الخاصة أو التبعية أو العقابية، بما في ذلك خسائر الأعمال أو الخسائر المالية أو النزاعات القانونية أو فقدان البيانات أو العواقب الناتجة عن سوء الاستخدام أو الاعتماد على مخرجات الذكاء الاصطناعي.",

    termsTerminationTitle: "10. الإنهاء",
    termsTerminationText:
      "يجوز لـ Runexa Systems LLC تعليق أو إنهاء الوصول إلى الخدمات إذا تم انتهاك هذه الشروط أو إذا كان استخدام الخدمات يخلق مخاطر قانونية أو أمنية أو تشغيلية أو تتعلق بالسمعة.",

    termsLawTitle: "11. القانون الحاكم",
    termsLawText:
      "تخضع هذه الشروط لقوانين ولاية وايومنغ، الولايات المتحدة، دون اعتبار لمبادئ تنازع القوانين.",

    termsChangesTitle: "12. التغييرات",
    termsChangesText:
      "يجوز لـ Runexa Systems LLC تحديث هذه الشروط من وقت لآخر. سيتم نشر الشروط المحدثة على هذه الصفحة مع تاريخ “آخر تحديث” معدل.",

    termsContactTitle: "13. الاتصال",
  },
};

export function getTranslations(locale: string) {
  if (!locales.includes(locale)) return translations[defaultLocale];

  return translations[locale];
}
