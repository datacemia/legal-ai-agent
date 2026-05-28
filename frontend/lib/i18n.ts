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
    slogan: "Specialized AI agents for real-world work",
    dashboard: "Dashboard",
    admin: "Admin",
    enterprise: "Enterprise",
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

    acceptableUseTitle: "Acceptable Use Policy",
    acceptableUseUpdated: "Last updated: May 2026",

    acceptableUseOverviewTitle: "1. Overview",
    acceptableUseOverviewText1:
      "This Acceptable Use Policy (“Policy”) governs the use of services, products, software, AI agents, and platforms operated by Runexa Systems LLC (“Runexa”).",

    acceptableUseOverviewText2:
      "By using Runexa services, you agree to comply with this Policy.",

    acceptableUseComplianceTitle: "2. Compliance With Laws",
    acceptableUseComplianceText:
      "You may only use the services in compliance with applicable laws, regulations, and third-party rights.",

    acceptableUseProhibitedTitle: "3. Prohibited Activities",
    acceptableUseProhibitedIntro:
      "You may not use Runexa services for:",

    acceptableUseProhibited1:
      "Illegal, fraudulent, or deceptive activity",

    acceptableUseProhibited2:
      "Malware, phishing, hacking, unauthorized access, or cyber abuse",

    acceptableUseProhibited3:
      "Harassment, threats, abuse, discrimination, or harmful conduct",

    acceptableUseProhibited4:
      "Uploading or processing content that violates intellectual property, privacy, confidentiality, or contractual rights",

    acceptableUseProhibited5:
      "Impersonation, identity fraud, or misleading representations",

    acceptableUseProhibited6:
      "Unauthorized surveillance, monitoring, or tracking of individuals",

    acceptableUseProhibited7:
      "Generating harmful, dangerous, or unlawful content",

    acceptableUseProhibited8:
      "Attempting to reverse engineer, disrupt, overload, or bypass the platform or security protections",

    acceptableUseProhibited9:
      "Using automated systems to abuse, scrape, spam, or excessively overload the services",

    acceptableUseAiTitle: "4. AI Usage Restrictions",
    acceptableUseAiText1:
      "AI-generated outputs may not be used as the sole basis for legal, financial, medical, employment, security, or other high-impact decisions without independent human review.",

    acceptableUseAiText2:
      "Users remain fully responsible for verifying outputs before relying on them.",

    acceptableUseResponsibilityTitle: "5. User Responsibility",
    acceptableUseResponsibilityText:
      "Users are responsible for all content uploaded, processed, generated, or shared through the services and for ensuring they have the legal right to use such content.",

    acceptableUseEnforcementTitle: "6. Enforcement",
    acceptableUseEnforcementText:
      "Runexa Systems LLC may investigate suspected violations of this Policy and may suspend, restrict, or terminate access to the services at its sole discretion.",

    acceptableUseReportingTitle: "7. Reporting Violations",
    acceptableUseReportingText:
      "Suspected violations or abuse may be reported to:",

    acceptableUseChangesTitle: "8. Changes",
    acceptableUseChangesText:
      "Runexa Systems LLC may update this Policy at any time. Updated versions will be posted with a revised “Last updated” date.",

    aiDisclaimerTitle: "AI Disclaimer & Transparency",
    aiDisclaimerUpdated: "Last updated: May 2026",

    aiDisclaimerOverviewTitle: "1. Overview",
    aiDisclaimerOverviewText1:
      "Runexa Systems LLC provides AI-powered tools and agents designed to assist users with document analysis, learning support, financial insights, business analysis, and related tasks.",
    aiDisclaimerOverviewText2:
      "AI systems are probabilistic technologies and may produce inaccurate, incomplete, inconsistent, or misleading outputs.",

    aiDisclaimerAdviceTitle: "2. No Professional Advice",
    aiDisclaimerAdviceText1:
      "Runexa AI agents do not provide legal, financial, accounting, tax, medical, investment, security, or other regulated professional advice.",
    aiDisclaimerAdviceText2:
      "AI-generated outputs should not be considered a substitute for qualified professionals or independent human judgment.",

    aiDisclaimerLimitationsTitle: "3. AI Limitations",
    aiDisclaimerLimitations1:
      "AI outputs may contain factual inaccuracies or hallucinations",
    aiDisclaimerLimitations2:
      "AI systems may omit important context, risks, or details",
    aiDisclaimerLimitations3:
      "AI-generated summaries, recommendations, or classifications may be incomplete or misleading",
    aiDisclaimerLimitations4:
      "AI systems may generate outdated information or incorrect interpretations",
    aiDisclaimerLimitations5:
      "AI outputs may vary between requests and are not guaranteed to be consistent",

    aiDisclaimerReviewTitle: "4. Human Review Required",
    aiDisclaimerReviewText1:
      "Users are solely responsible for independently reviewing, verifying, and validating all outputs before relying on them or taking action.",
    aiDisclaimerReviewText2:
      "AI outputs should not be used as the sole basis for legal, financial, employment, educational, medical, security, compliance, or other high-impact decisions.",

    aiDisclaimerResponsibilityTitle: "5. User Responsibility",
    aiDisclaimerResponsibilityText:
      "Users remain fully responsible for how they use AI-generated outputs, including any decisions, actions, interpretations, or consequences resulting from use of the services.",

    aiDisclaimerGuaranteesTitle: "6. No Guarantees",
    aiDisclaimerGuaranteesText:
      "Runexa Systems LLC does not guarantee the accuracy, completeness, reliability, legality, availability, or fitness of AI-generated outputs for any purpose.",

    aiDisclaimerImprovementTitle: "7. Continuous Improvement",
    aiDisclaimerImprovementText:
      "AI systems may evolve, change, improve, or behave differently over time as models, infrastructure, and safety systems are updated.",

    aiDisclaimerContactTitle: "8. Contact",

    cookiesTitle: "Cookie Policy",
    cookiesUpdated: "Last updated: May 2026",

    cookiesOverviewTitle: "1. Overview",
    cookiesOverviewText:
      "This Cookie Policy explains how Runexa Systems LLC (“Runexa”, “we”, “our”, or “us”) uses cookies and similar technologies when you access or use our services, websites, and AI platforms.",

    cookiesWhatTitle: "2. What Are Cookies",
    cookiesWhatText:
      "Cookies are small text files stored on your device by your web browser. Cookies help websites recognize users, maintain sessions, remember preferences, and improve functionality and security.",

    cookiesTypesTitle: "3. Types of Cookies We Use",

    cookiesEssentialTitle: "3.1 Essential Cookies",
    cookiesEssentialText:
      "These cookies are necessary for the operation of the services, including authentication, account access, security, and session management.",

    cookiesAnalyticsTitle: "3.2 Performance and Analytics Cookies",
    cookiesAnalyticsText:
      "These cookies help us understand how users interact with the platform, improve reliability, monitor performance, and detect technical issues.",

    cookiesPreferenceTitle: "3.3 Preference Cookies",
    cookiesPreferenceText:
      "These cookies may store user preferences such as language settings, interface preferences, or session-related choices.",

    cookiesSecurityTitle: "3.4 Security Cookies",
    cookiesSecurityText:
      "Security-related cookies may be used to prevent fraud, abuse, unauthorized access, and suspicious activity.",

    cookiesThirdPartyTitle: "4. Third-Party Services",
    cookiesThirdPartyText:
      "Some cookies may be placed by third-party providers that support infrastructure, analytics, authentication, hosting, AI processing, or payment services used by Runexa Systems LLC.",

    cookiesManagingTitle: "5. Managing Cookies",
    cookiesManagingText:
      "Most web browsers allow users to control, disable, or delete cookies through browser settings. Disabling cookies may affect functionality, availability, or performance of certain services.",

    cookiesTrackTitle: "6. Do Not Track",
    cookiesTrackText:
      "Some browsers offer “Do Not Track” settings. Because there is no universally accepted standard for these signals, our services may not respond to all Do Not Track requests.",

    cookiesChangesTitle: "7. Changes",
    cookiesChangesText:
      "Runexa Systems LLC may update this Cookie Policy from time to time. Updated versions will be posted with a revised “Last updated” date.",

    cookiesContactTitle: "8. Contact",

    refundTitle: "Refund Policy",
    refundUpdated: "Last updated: May 2026",

    refundOverviewTitle: "1. Overview",
    refundOverviewText:
      "This Refund Policy applies to purchases, credits, subscriptions, trials, and other paid services offered by Runexa Systems LLC.",

    refundTrialsTitle: "2. Trials and Credits",
    refundTrialsText1:
      "Trial purchases, activation fees, AI credits, and usage-based purchases are generally non-refundable unless required by applicable law.",
    refundTrialsText2:
      "Users are responsible for reviewing product descriptions and pricing before purchasing.",

    refundSubscriptionTitle: "3. Subscription Services",
    refundSubscriptionText1:
      "Subscription plans may renew automatically unless canceled before the next billing cycle.",
    refundSubscriptionText2:
      "Users may cancel subscriptions at any time, but fees already paid are generally non-refundable.",

    refundChargesTitle: "4. Failed or Duplicate Charges",
    refundChargesText:
      "If you believe you were charged incorrectly, charged multiple times, or experienced a billing error, please contact us for review.",

    refundAbuseTitle: "5. Chargebacks and Abuse",
    refundAbuseText:
      "Fraudulent chargebacks, payment abuse, or attempts to improperly reverse payments may result in suspension or termination of access to the services.",

    refundAvailabilityTitle: "6. Service Availability",
    refundAvailabilityText:
      "Temporary outages, AI inaccuracies, delays, model limitations, or feature changes do not automatically qualify for refunds.",

    refundExceptionsTitle: "7. Exceptions",
    refundExceptionsText:
      "Runexa Systems LLC may, at its sole discretion, provide refunds, credits, or account adjustments in exceptional situations.",

    refundChangesTitle: "8. Changes",
    refundChangesText:
      "Runexa Systems LLC may update this Refund Policy from time to time. Updated versions will be posted with a revised “Last updated” date.",

    refundContactTitle: "9. Contact",

    companyInfoTitle: "Company Information",
    companyInfoUpdated: "Last updated: May 2026",

    companySectionTitle: "1. Company",
    companySectionText:
      "AI agents platform providing AI-powered tools and services.",

    companyAddressTitle: "2. Registered Address",

    companyContactTitle: "3. Contact Information",
    companyContactText: "General Contact",

    companyServicesTitle: "4. Services",
    companyServicesText:
      "Runexa Systems LLC develops and operates AI-powered tools, applications, AI agents, and related software services.",

    companyLawTitle: "5. Governing Law",
    companyLawText:
      "Services provided by Runexa Systems LLC are governed by the laws of the State of Wyoming, United States.",

    resources: "Resources",
    developers: "Developers",
    docs: "Docs",
    blog: "Blog",
    legalAi: "Legal AI",
    financeAi: "Finance AI",
    studyAi: "Study AI",
    businessAi: "Business AI",
    builtBy: "Built by Dr. Rachid Ejjami",
    apiDashboard: "API Dashboard",


  },

  fr: {
    slogan: "Des agents IA spécialisés pour le travail réel",
    dashboard: "Tableau de bord",
    admin: "Admin",
    enterprise: "Entreprise",
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

    acceptableUseTitle: "Politique d’utilisation acceptable",
    acceptableUseUpdated: "Dernière mise à jour : mai 2026",

    acceptableUseOverviewTitle: "1. Présentation",
    acceptableUseOverviewText1:
      "Cette Politique d’utilisation acceptable (« Politique ») régit l’utilisation des services, produits, logiciels, agents IA et plateformes exploités par Runexa Systems LLC (« Runexa »).",

    acceptableUseOverviewText2:
      "En utilisant les services Runexa, vous acceptez de respecter cette Politique.",

    acceptableUseComplianceTitle: "2. Respect des lois",
    acceptableUseComplianceText:
      "Vous ne pouvez utiliser les services qu’en conformité avec les lois applicables, réglementations et droits des tiers.",

    acceptableUseProhibitedTitle: "3. Activités interdites",
    acceptableUseProhibitedIntro:
      "Vous ne pouvez pas utiliser les services Runexa pour :",

    acceptableUseProhibited1:
      "Une activité illégale, frauduleuse ou trompeuse",

    acceptableUseProhibited2:
      "Des logiciels malveillants, phishing, piratage, accès non autorisé ou abus cyber",

    acceptableUseProhibited3:
      "Le harcèlement, les menaces, abus, discriminations ou comportements nuisibles",

    acceptableUseProhibited4:
      "Téléverser ou traiter du contenu violant la propriété intellectuelle, la vie privée, la confidentialité ou des droits contractuels",

    acceptableUseProhibited5:
      "L’usurpation d’identité, fraude identitaire ou représentations trompeuses",

    acceptableUseProhibited6:
      "La surveillance, le suivi ou l’espionnage non autorisé d’individus",

    acceptableUseProhibited7:
      "La génération de contenu nuisible, dangereux ou illégal",

    acceptableUseProhibited8:
      "Tenter de contourner, perturber, surcharger ou compromettre la plateforme ou ses protections de sécurité",

    acceptableUseProhibited9:
      "Utiliser des systèmes automatisés pour abuser, scraper, spammer ou surcharger excessivement les services",

    acceptableUseAiTitle: "4. Restrictions liées à l’IA",
    acceptableUseAiText1:
      "Les résultats générés par l’IA ne peuvent pas être utilisés comme seule base pour des décisions juridiques, financières, médicales, professionnelles, de sécurité ou autres décisions à fort impact sans examen humain indépendant.",

    acceptableUseAiText2:
      "Les utilisateurs restent entièrement responsables de la vérification des résultats avant de s’y fier.",

    acceptableUseResponsibilityTitle: "5. Responsabilité de l’utilisateur",
    acceptableUseResponsibilityText:
      "Les utilisateurs sont responsables de tout contenu téléversé, traité, généré ou partagé via les services et doivent s’assurer qu’ils disposent des droits légaux nécessaires pour utiliser ce contenu.",

    acceptableUseEnforcementTitle: "6. Application",
    acceptableUseEnforcementText:
      "Runexa Systems LLC peut enquêter sur les violations présumées de cette Politique et peut suspendre, restreindre ou résilier l’accès aux services à sa seule discrétion.",

    acceptableUseReportingTitle: "7. Signalement des violations",
    acceptableUseReportingText:
      "Les violations ou abus présumés peuvent être signalés à :",

    acceptableUseChangesTitle: "8. Modifications",
    acceptableUseChangesText:
      "Runexa Systems LLC peut mettre à jour cette Politique à tout moment. Les versions mises à jour seront publiées avec une date de « Dernière mise à jour » révisée.",

    aiDisclaimerTitle: "Avertissement et transparence sur l’IA",
    aiDisclaimerUpdated: "Dernière mise à jour : mai 2026",

    aiDisclaimerOverviewTitle: "1. Présentation",
    aiDisclaimerOverviewText1:
      "Runexa Systems LLC fournit des outils et agents alimentés par l’IA conçus pour aider les utilisateurs dans l’analyse de documents, le support d’apprentissage, les analyses financières, les analyses business et d’autres tâches associées.",
    aiDisclaimerOverviewText2:
      "Les systèmes d’IA sont des technologies probabilistes pouvant produire des résultats inexacts, incomplets, incohérents ou trompeurs.",

    aiDisclaimerAdviceTitle: "2. Absence de conseil professionnel",
    aiDisclaimerAdviceText1:
      "Les agents IA de Runexa ne fournissent pas de conseils juridiques, financiers, comptables, fiscaux, médicaux, d’investissement, de sécurité ou autres conseils professionnels réglementés.",
    aiDisclaimerAdviceText2:
      "Les résultats générés par l’IA ne doivent pas être considérés comme un substitut à des professionnels qualifiés ou au jugement humain indépendant.",

    aiDisclaimerLimitationsTitle: "3. Limites de l’IA",
    aiDisclaimerLimitations1:
      "Les résultats IA peuvent contenir des erreurs factuelles ou des hallucinations",
    aiDisclaimerLimitations2:
      "Les systèmes IA peuvent omettre des contextes, risques ou détails importants",
    aiDisclaimerLimitations3:
      "Les résumés, recommandations ou classifications générés par l’IA peuvent être incomplets ou trompeurs",
    aiDisclaimerLimitations4:
      "Les systèmes IA peuvent générer des informations obsolètes ou des interprétations incorrectes",
    aiDisclaimerLimitations5:
      "Les résultats IA peuvent varier entre les requêtes et ne sont pas garantis cohérents",

    aiDisclaimerReviewTitle: "4. Vérification humaine requise",
    aiDisclaimerReviewText1:
      "Les utilisateurs sont seuls responsables de l’examen, de la vérification et de la validation indépendants de tous les résultats avant de s’y fier ou d’agir.",
    aiDisclaimerReviewText2:
      "Les résultats IA ne doivent pas être utilisés comme seule base pour des décisions juridiques, financières, professionnelles, éducatives, médicales, de sécurité, de conformité ou autres décisions à fort impact.",

    aiDisclaimerResponsibilityTitle: "5. Responsabilité de l’utilisateur",
    aiDisclaimerResponsibilityText:
      "Les utilisateurs restent entièrement responsables de la manière dont ils utilisent les résultats générés par l’IA, y compris les décisions, actions, interprétations ou conséquences résultant de l’utilisation des services.",

    aiDisclaimerGuaranteesTitle: "6. Absence de garanties",
    aiDisclaimerGuaranteesText:
      "Runexa Systems LLC ne garantit pas l’exactitude, l’exhaustivité, la fiabilité, la légalité, la disponibilité ou l’adéquation des résultats générés par l’IA à un usage particulier.",

    aiDisclaimerImprovementTitle: "7. Amélioration continue",
    aiDisclaimerImprovementText:
      "Les systèmes IA peuvent évoluer, changer, s’améliorer ou se comporter différemment au fil du temps à mesure que les modèles, infrastructures et systèmes de sécurité sont mis à jour.",

    aiDisclaimerContactTitle: "8. Contact",

    cookiesTitle: "Politique relative aux cookies",
    cookiesUpdated: "Dernière mise à jour : mai 2026",

    cookiesOverviewTitle: "1. Présentation",
    cookiesOverviewText:
      "Cette Politique relative aux cookies explique comment Runexa Systems LLC (« Runexa », « nous », « notre » ou « nos ») utilise les cookies et technologies similaires lorsque vous accédez à nos services, sites web et plateformes IA ou les utilisez.",

    cookiesWhatTitle: "2. Que sont les cookies",
    cookiesWhatText:
      "Les cookies sont de petits fichiers texte stockés sur votre appareil par votre navigateur web. Ils aident les sites web à reconnaître les utilisateurs, maintenir les sessions, mémoriser les préférences et améliorer les fonctionnalités et la sécurité.",

    cookiesTypesTitle: "3. Types de cookies que nous utilisons",

    cookiesEssentialTitle: "3.1 Cookies essentiels",
    cookiesEssentialText:
      "Ces cookies sont nécessaires au fonctionnement des services, notamment l’authentification, l’accès au compte, la sécurité et la gestion des sessions.",

    cookiesAnalyticsTitle: "3.2 Cookies de performance et d’analyse",
    cookiesAnalyticsText:
      "Ces cookies nous aident à comprendre comment les utilisateurs interagissent avec la plateforme, à améliorer la fiabilité, surveiller les performances et détecter les problèmes techniques.",

    cookiesPreferenceTitle: "3.3 Cookies de préférences",
    cookiesPreferenceText:
      "Ces cookies peuvent stocker les préférences utilisateur telles que les paramètres de langue, les préférences d’interface ou les choix liés aux sessions.",

    cookiesSecurityTitle: "3.4 Cookies de sécurité",
    cookiesSecurityText:
      "Les cookies liés à la sécurité peuvent être utilisés pour prévenir la fraude, les abus, l’accès non autorisé et les activités suspectes.",

    cookiesThirdPartyTitle: "4. Services tiers",
    cookiesThirdPartyText:
      "Certains cookies peuvent être placés par des prestataires tiers qui prennent en charge l’infrastructure, l’analyse, l’authentification, l’hébergement, le traitement IA ou les services de paiement utilisés par Runexa Systems LLC.",

    cookiesManagingTitle: "5. Gestion des cookies",
    cookiesManagingText:
      "La plupart des navigateurs web permettent aux utilisateurs de contrôler, désactiver ou supprimer les cookies via les paramètres du navigateur. La désactivation des cookies peut affecter les fonctionnalités, la disponibilité ou les performances de certains services.",

    cookiesTrackTitle: "6. Do Not Track",
    cookiesTrackText:
      "Certains navigateurs proposent des paramètres « Do Not Track ». Comme il n’existe pas de norme universellement acceptée pour ces signaux, nos services peuvent ne pas répondre à toutes les demandes Do Not Track.",

    cookiesChangesTitle: "7. Modifications",
    cookiesChangesText:
      "Runexa Systems LLC peut mettre à jour cette Politique relative aux cookies de temps à autre. Les versions mises à jour seront publiées avec une date de « Dernière mise à jour » révisée.",

    cookiesContactTitle: "8. Contact",

    refundTitle: "Politique de remboursement",
    refundUpdated: "Dernière mise à jour : mai 2026",

    refundOverviewTitle: "1. Présentation",
    refundOverviewText:
      "Cette Politique de remboursement s’applique aux achats, crédits, abonnements, essais et autres services payants proposés par Runexa Systems LLC.",

    refundTrialsTitle: "2. Essais et crédits",
    refundTrialsText1:
      "Les achats d’essai, frais d’activation, crédits IA et achats basés sur l’utilisation sont généralement non remboursables sauf si la loi applicable l’exige.",
    refundTrialsText2:
      "Les utilisateurs sont responsables de consulter les descriptions des produits et les tarifs avant l’achat.",

    refundSubscriptionTitle: "3. Services d’abonnement",
    refundSubscriptionText1:
      "Les abonnements peuvent être renouvelés automatiquement sauf annulation avant le prochain cycle de facturation.",
    refundSubscriptionText2:
      "Les utilisateurs peuvent annuler leur abonnement à tout moment, mais les frais déjà payés sont généralement non remboursables.",

    refundChargesTitle: "4. Paiements échoués ou en double",
    refundChargesText:
      "Si vous pensez avoir été facturé incorrectement, facturé plusieurs fois ou avoir subi une erreur de facturation, veuillez nous contacter pour examen.",

    refundAbuseTitle: "5. Contestations et abus",
    refundAbuseText:
      "Les contestations frauduleuses, abus de paiement ou tentatives d’annulation abusive des paiements peuvent entraîner la suspension ou la résiliation de l’accès aux services.",

    refundAvailabilityTitle: "6. Disponibilité du service",
    refundAvailabilityText:
      "Les interruptions temporaires, erreurs IA, retards, limitations des modèles ou modifications des fonctionnalités ne donnent pas automatiquement droit à un remboursement.",

    refundExceptionsTitle: "7. Exceptions",
    refundExceptionsText:
      "Runexa Systems LLC peut, à sa seule discrétion, accorder des remboursements, crédits ou ajustements de compte dans des situations exceptionnelles.",

    refundChangesTitle: "8. Modifications",
    refundChangesText:
      "Runexa Systems LLC peut mettre à jour cette Politique de remboursement de temps à autre. Les versions mises à jour seront publiées avec une date de « Dernière mise à jour » révisée.",

    refundContactTitle: "9. Contact",

    companyInfoTitle: "Informations société",
    companyInfoUpdated: "Dernière mise à jour : mai 2026",

    companySectionTitle: "1. Société",
    companySectionText:
      "Plateforme d’agents IA fournissant des outils et services alimentés par l’intelligence artificielle.",

    companyAddressTitle: "2. Adresse enregistrée",

    companyContactTitle: "3. Informations de contact",
    companyContactText: "Contact général",

    companyServicesTitle: "4. Services",
    companyServicesText:
      "Runexa Systems LLC développe et exploite des outils alimentés par l’IA, des applications, des agents IA et des services logiciels associés.",

    companyLawTitle: "5. Droit applicable",
    companyLawText:
      "Les services fournis par Runexa Systems LLC sont régis par les lois de l’État du Wyoming, États-Unis.",

    resources: "Ressources",
    developers: "Développeurs",
    docs: "Documentation",
    blog: "Blog",
    legalAi: "IA juridique",
    financeAi: "IA finance",
    studyAi: "IA étude",
    businessAi: "IA business",
    builtBy: "Créé par Dr. Rachid Ejjami",
    apiDashboard: "Dashboard API",


  },

  ar: {
    slogan: "وكلاء ذكاء اصطناعي متخصصون للعمل الواقعي",
    dashboard: "لوحة التحكم",
    admin: "الإدارة",
    enterprise: "المؤسسات",
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

    acceptableUseTitle: "سياسة الاستخدام المقبول",
    acceptableUseUpdated: "آخر تحديث: مايو 2026",

    acceptableUseOverviewTitle: "1. نظرة عامة",
    acceptableUseOverviewText1:
      "تنظم سياسة الاستخدام المقبول هذه («السياسة») استخدام الخدمات والمنتجات والبرمجيات ووكلاء الذكاء الاصطناعي والمنصات التي تديرها Runexa Systems LLC («Runexa»).",

    acceptableUseOverviewText2:
      "باستخدام خدمات Runexa، فإنك توافق على الالتزام بهذه السياسة.",

    acceptableUseComplianceTitle: "2. الامتثال للقوانين",
    acceptableUseComplianceText:
      "لا يجوز لك استخدام الخدمات إلا بما يتوافق مع القوانين المعمول بها واللوائح وحقوق الأطراف الثالثة.",

    acceptableUseProhibitedTitle: "3. الأنشطة المحظورة",
    acceptableUseProhibitedIntro:
      "لا يجوز استخدام خدمات Runexa من أجل:",

    acceptableUseProhibited1:
      "الأنشطة غير القانونية أو الاحتيالية أو المضللة",

    acceptableUseProhibited2:
      "البرمجيات الخبيثة أو التصيد الاحتيالي أو الاختراق أو الوصول غير المصرح به أو إساءة الاستخدام السيبراني",

    acceptableUseProhibited3:
      "المضايقة أو التهديدات أو الإساءة أو التمييز أو السلوك الضار",

    acceptableUseProhibited4:
      "رفع أو معالجة محتوى ينتهك الملكية الفكرية أو الخصوصية أو السرية أو الحقوق التعاقدية",

    acceptableUseProhibited5:
      "انتحال الهوية أو الاحتيال أو التمثيل المضلل",

    acceptableUseProhibited6:
      "المراقبة أو التتبع غير المصرح به للأفراد",

    acceptableUseProhibited7:
      "إنشاء محتوى ضار أو خطير أو غير قانوني",

    acceptableUseProhibited8:
      "محاولة إجراء هندسة عكسية أو تعطيل أو تجاوز المنصة أو وسائل الحماية الأمنية",

    acceptableUseProhibited9:
      "استخدام الأنظمة الآلية لإساءة الاستخدام أو جمع البيانات أو إرسال الرسائل المزعجة أو تحميل الخدمات بشكل مفرط",

    acceptableUseAiTitle: "4. قيود استخدام الذكاء الاصطناعي",
    acceptableUseAiText1:
      "لا يجوز استخدام المخرجات الناتجة عن الذكاء الاصطناعي كأساس وحيد لاتخاذ قرارات قانونية أو مالية أو طبية أو وظيفية أو أمنية أو قرارات عالية التأثير دون مراجعة بشرية مستقلة.",

    acceptableUseAiText2:
      "يبقى المستخدمون مسؤولين بالكامل عن التحقق من المخرجات قبل الاعتماد عليها.",

    acceptableUseResponsibilityTitle: "5. مسؤولية المستخدم",
    acceptableUseResponsibilityText:
      "المستخدمون مسؤولون عن جميع المحتويات التي يتم رفعها أو معالجتها أو إنشاؤها أو مشاركتها عبر الخدمات، وعن التأكد من امتلاكهم الحق القانوني لاستخدام هذا المحتوى.",

    acceptableUseEnforcementTitle: "6. التنفيذ",
    acceptableUseEnforcementText:
      "يجوز لـ Runexa Systems LLC التحقيق في الانتهاكات المشتبه بها لهذه السياسة، وقد تقوم بتعليق أو تقييد أو إنهاء الوصول إلى الخدمات وفقًا لتقديرها الخاص.",

    acceptableUseReportingTitle: "7. الإبلاغ عن الانتهاكات",
    acceptableUseReportingText:
      "يمكن الإبلاغ عن الانتهاكات أو إساءة الاستخدام المشتبه بها عبر:",

    acceptableUseChangesTitle: "8. التغييرات",
    acceptableUseChangesText:
      "يجوز لـ Runexa Systems LLC تحديث هذه السياسة في أي وقت. سيتم نشر الإصدارات المحدثة مع تاريخ «آخر تحديث» معدل.",

    aiDisclaimerTitle: "إخلاء المسؤولية والشفافية الخاصة بالذكاء الاصطناعي",
    aiDisclaimerUpdated: "آخر تحديث: مايو 2026",

    aiDisclaimerOverviewTitle: "1. نظرة عامة",
    aiDisclaimerOverviewText1:
      "توفر Runexa Systems LLC أدوات ووكلاء مدعومين بالذكاء الاصطناعي لمساعدة المستخدمين في تحليل المستندات ودعم التعلم والتحليلات المالية وتحليل الأعمال والمهام ذات الصلة.",
    aiDisclaimerOverviewText2:
      "أنظمة الذكاء الاصطناعي تقنيات احتمالية وقد تنتج مخرجات غير دقيقة أو غير مكتملة أو غير متسقة أو مضللة.",

    aiDisclaimerAdviceTitle: "2. لا توجد نصائح مهنية",
    aiDisclaimerAdviceText1:
      "لا يقدم وكلاء Runexa للذكاء الاصطناعي نصائح قانونية أو مالية أو محاسبية أو ضريبية أو طبية أو استثمارية أو أمنية أو أي نصائح مهنية منظمة أخرى.",
    aiDisclaimerAdviceText2:
      "لا ينبغي اعتبار المخرجات الناتجة عن الذكاء الاصطناعي بديلاً عن المهنيين المؤهلين أو الحكم البشري المستقل.",

    aiDisclaimerLimitationsTitle: "3. حدود الذكاء الاصطناعي",
    aiDisclaimerLimitations1:
      "قد تحتوي مخرجات الذكاء الاصطناعي على أخطاء أو هلوسات",
    aiDisclaimerLimitations2:
      "قد تغفل أنظمة الذكاء الاصطناعي سياقات أو مخاطر أو تفاصيل مهمة",
    aiDisclaimerLimitations3:
      "قد تكون الملخصات أو التوصيات أو التصنيفات الناتجة عن الذكاء الاصطناعي غير مكتملة أو مضللة",
    aiDisclaimerLimitations4:
      "قد تولد أنظمة الذكاء الاصطناعي معلومات قديمة أو تفسيرات غير صحيحة",
    aiDisclaimerLimitations5:
      "قد تختلف مخرجات الذكاء الاصطناعي بين الطلبات ولا يوجد ضمان لاتساقها",

    aiDisclaimerReviewTitle: "4. المراجعة البشرية مطلوبة",
    aiDisclaimerReviewText1:
      "المستخدمون مسؤولون وحدهم عن مراجعة جميع المخرجات والتحقق منها واعتمادها بشكل مستقل قبل الاعتماد عليها أو اتخاذ أي إجراء.",
    aiDisclaimerReviewText2:
      "لا ينبغي استخدام مخرجات الذكاء الاصطناعي كأساس وحيد لاتخاذ قرارات قانونية أو مالية أو وظيفية أو تعليمية أو طبية أو أمنية أو تنظيمية أو أي قرارات عالية التأثير.",

    aiDisclaimerResponsibilityTitle: "5. مسؤولية المستخدم",
    aiDisclaimerResponsibilityText:
      "يبقى المستخدمون مسؤولين بالكامل عن كيفية استخدامهم للمخرجات الناتجة عن الذكاء الاصطناعي، بما في ذلك أي قرارات أو إجراءات أو تفسيرات أو عواقب ناتجة عن استخدام الخدمات.",

    aiDisclaimerGuaranteesTitle: "6. عدم وجود ضمانات",
    aiDisclaimerGuaranteesText:
      "لا تضمن Runexa Systems LLC دقة أو اكتمال أو موثوقية أو قانونية أو توفر أو ملاءمة المخرجات الناتجة عن الذكاء الاصطناعي لأي غرض.",

    aiDisclaimerImprovementTitle: "7. التحسين المستمر",
    aiDisclaimerImprovementText:
      "قد تتطور أنظمة الذكاء الاصطناعي أو تتغير أو تتحسن أو تتصرف بشكل مختلف مع مرور الوقت مع تحديث النماذج والبنية التحتية وأنظمة الأمان.",

    aiDisclaimerContactTitle: "8. الاتصال",

    cookiesTitle: "سياسة ملفات تعريف الارتباط",
    cookiesUpdated: "آخر تحديث: مايو 2026",

    cookiesOverviewTitle: "1. نظرة عامة",
    cookiesOverviewText:
      "توضح سياسة ملفات تعريف الارتباط هذه كيفية استخدام Runexa Systems LLC («Runexa» أو «نحن») لملفات تعريف الارتباط والتقنيات المشابهة عند الوصول إلى خدماتنا أو مواقعنا أو منصات الذكاء الاصطناعي أو استخدامها.",

    cookiesWhatTitle: "2. ما هي ملفات تعريف الارتباط",
    cookiesWhatText:
      "ملفات تعريف الارتباط هي ملفات نصية صغيرة يخزنها متصفح الويب على جهازك. تساعد هذه الملفات المواقع على التعرف على المستخدمين والحفاظ على الجلسات وتذكر التفضيلات وتحسين الوظائف والأمان.",

    cookiesTypesTitle: "3. أنواع ملفات تعريف الارتباط التي نستخدمها",

    cookiesEssentialTitle: "3.1 ملفات تعريف الارتباط الأساسية",
    cookiesEssentialText:
      "هذه الملفات ضرورية لتشغيل الخدمات، بما في ذلك المصادقة والوصول إلى الحساب والأمان وإدارة الجلسات.",

    cookiesAnalyticsTitle: "3.2 ملفات الأداء والتحليلات",
    cookiesAnalyticsText:
      "تساعدنا هذه الملفات على فهم كيفية تفاعل المستخدمين مع المنصة وتحسين الموثوقية ومراقبة الأداء واكتشاف المشكلات التقنية.",

    cookiesPreferenceTitle: "3.3 ملفات التفضيلات",
    cookiesPreferenceText:
      "قد تخزن هذه الملفات تفضيلات المستخدم مثل إعدادات اللغة أو تفضيلات الواجهة أو الخيارات المتعلقة بالجلسة.",

    cookiesSecurityTitle: "3.4 ملفات الأمان",
    cookiesSecurityText:
      "قد تُستخدم ملفات تعريف الارتباط المتعلقة بالأمان لمنع الاحتيال وإساءة الاستخدام والوصول غير المصرح به والأنشطة المشبوهة.",

    cookiesThirdPartyTitle: "4. خدمات الطرف الثالث",
    cookiesThirdPartyText:
      "قد يتم وضع بعض ملفات تعريف الارتباط بواسطة مزودي خدمات تابعين لجهات خارجية يدعمون البنية التحتية أو التحليلات أو المصادقة أو الاستضافة أو معالجة الذكاء الاصطناعي أو خدمات الدفع التي تستخدمها Runexa Systems LLC.",

    cookiesManagingTitle: "5. إدارة ملفات تعريف الارتباط",
    cookiesManagingText:
      "تسمح معظم متصفحات الويب للمستخدمين بالتحكم في ملفات تعريف الارتباط أو تعطيلها أو حذفها من خلال إعدادات المتصفح. قد يؤثر تعطيل ملفات تعريف الارتباط على وظائف بعض الخدمات أو توفرها أو أدائها.",

    cookiesTrackTitle: "6. عدم التتبع",
    cookiesTrackText:
      "تقدم بعض المتصفحات إعدادات “Do Not Track”. ونظرًا لعدم وجود معيار مقبول عالميًا لهذه الإشارات، فقد لا تستجيب خدماتنا لجميع طلبات عدم التتبع.",

    cookiesChangesTitle: "7. التغييرات",
    cookiesChangesText:
      "يجوز لـ Runexa Systems LLC تحديث سياسة ملفات تعريف الارتباط هذه من وقت لآخر. سيتم نشر الإصدارات المحدثة مع تاريخ “آخر تحديث” معدل.",

    cookiesContactTitle: "8. الاتصال",

    refundTitle: "سياسة الاسترداد",
    refundUpdated: "آخر تحديث: مايو 2026",

    refundOverviewTitle: "1. نظرة عامة",
    refundOverviewText:
      "تنطبق سياسة الاسترداد هذه على المشتريات والأرصدة والاشتراكات والتجارب والخدمات المدفوعة الأخرى التي تقدمها Runexa Systems LLC.",

    refundTrialsTitle: "2. التجارب والأرصدة",
    refundTrialsText1:
      "عمليات الشراء التجريبية ورسوم التفعيل وأرصدة الذكاء الاصطناعي والمشتريات القائمة على الاستخدام غير قابلة للاسترداد عمومًا ما لم يتطلب القانون المعمول به خلاف ذلك.",
    refundTrialsText2:
      "المستخدمون مسؤولون عن مراجعة أوصاف المنتجات والأسعار قبل الشراء.",

    refundSubscriptionTitle: "3. خدمات الاشتراك",
    refundSubscriptionText1:
      "قد يتم تجديد خطط الاشتراك تلقائيًا ما لم يتم إلغاؤها قبل دورة الفوترة التالية.",
    refundSubscriptionText2:
      "يمكن للمستخدمين إلغاء الاشتراكات في أي وقت، لكن الرسوم المدفوعة مسبقًا غير قابلة للاسترداد عمومًا.",

    refundChargesTitle: "4. الرسوم المكررة أو الفاشلة",
    refundChargesText:
      "إذا كنت تعتقد أنه تم تحصيل رسوم منك بشكل غير صحيح أو عدة مرات أو حدث خطأ في الفوترة، يرجى التواصل معنا للمراجعة.",

    refundAbuseTitle: "5. إساءة الاستخدام واسترجاع المدفوعات",
    refundAbuseText:
      "قد تؤدي عمليات استرجاع المدفوعات الاحتيالية أو إساءة استخدام الدفع أو محاولات عكس المدفوعات بشكل غير صحيح إلى تعليق أو إنهاء الوصول إلى الخدمات.",

    refundAvailabilityTitle: "6. توفر الخدمة",
    refundAvailabilityText:
      "الانقطاعات المؤقتة أو أخطاء الذكاء الاصطناعي أو التأخيرات أو قيود النماذج أو تغييرات الميزات لا تؤهل تلقائيًا للحصول على استرداد.",

    refundExceptionsTitle: "7. الاستثناءات",
    refundExceptionsText:
      "يجوز لـ Runexa Systems LLC، وفقًا لتقديرها الخاص، تقديم استردادات أو أرصدة أو تعديلات على الحساب في الحالات الاستثنائية.",

    refundChangesTitle: "8. التغييرات",
    refundChangesText:
      "يجوز لـ Runexa Systems LLC تحديث سياسة الاسترداد هذه من وقت لآخر. سيتم نشر الإصدارات المحدثة مع تاريخ “آخر تحديث” معدل.",

    refundContactTitle: "9. الاتصال",

    companyInfoTitle: "معلومات الشركة",
    companyInfoUpdated: "آخر تحديث: مايو 2026",

    companySectionTitle: "1. الشركة",
    companySectionText:
      "منصة وكلاء ذكاء اصطناعي توفر أدوات وخدمات مدعومة بالذكاء الاصطناعي.",

    companyAddressTitle: "2. العنوان المسجل",

    companyContactTitle: "3. معلومات الاتصال",
    companyContactText: "الاتصال العام",

    companyServicesTitle: "4. الخدمات",
    companyServicesText:
      "تقوم Runexa Systems LLC بتطوير وتشغيل أدوات وتطبيقات ووكلاء ذكاء اصطناعي وخدمات برمجية مرتبطة بها.",

    companyLawTitle: "5. القانون الحاكم",
    companyLawText:
      "تخضع الخدمات المقدمة من Runexa Systems LLC لقوانين ولاية وايومنغ، الولايات المتحدة.",

    resources: "الموارد",
    developers: "المطورون",
    docs: "التوثيق",
    blog: "المدونة",
    legalAi: "الذكاء القانوني",
    financeAi: "الذكاء المالي",
    studyAi: "ذكاء الدراسة",
    businessAi: "ذكاء الأعمال",
   builtBy: "تم التطوير بواسطة الدكتور رشيد الجامعي",
    apiDashboard: "لوحة API",


  },
};

export function getTranslations(locale: string) {
  if (!locales.includes(locale)) return translations[defaultLocale];

  return translations[locale];
}
