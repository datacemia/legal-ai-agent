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

const refundCopy = {
  en: {
    title: "Refund Policy",
    updated: "Last updated: June 2026",
    eyebrow: "Refunds & billing",
    heroTitle: "Transparent billing for credits, trials, and subscriptions.",
    heroText:
      "This Refund Policy explains how Runexa Systems LLC handles paid trials, credits, subscriptions, billing errors, duplicate charges, and refund requests. Runexa reviews reasonable billing issues case by case and respects consumer rights where required by applicable law.",
    primaryCta: "Contact billing support",
    secondaryCta: "View Terms",

    highlightsTitle: "Billing principles",
    highlightsSubtitle:
      "Runexa uses a credit-based platform model with clear access rules and billing review channels.",
    highlights: [
      [
        "Credit-Based Platform",
        "Credits are used to access AI agents and analysis workflows. Credit usage may depend on the selected agent, task, file type, or plan.",
      ],
      [
        "Trial Access",
        "Introductory trials are intended to let users evaluate Runexa before purchasing larger credit packages or subscriptions.",
      ],
      [
        "Billing Review",
        "Duplicate charges, failed payments, payment processor errors, or incorrect charges can be reviewed by contacting Runexa.",
      ],
      [
        "Consumer Rights",
        "Nothing in this Policy limits non-waivable consumer protection, cancellation, or refund rights under applicable law.",
      ],
    ],

    howTitle: "How Runexa billing works",
    howText:
      "Runexa may offer paid trials, AI credits, subscriptions, enterprise plans, or other paid access options. Pricing, included credits, renewal terms, and plan limits are shown at the time of purchase or in the relevant product, pricing, or checkout page.",
    howItems: [
      "Credits may be consumed when an AI agent performs an analysis or generates an output",
      "Subscriptions may renew automatically unless canceled before the next billing cycle",
      "Enterprise or custom plans may be governed by separate written terms",
      "Payment processing may be handled by third-party payment providers",
    ],

    trialTitle: "Trials and introductory offers",
    trialText:
      "The introductory trial is designed to help users evaluate the platform before purchasing larger credit packages or subscriptions. Trial fees are generally non-refundable once access has been activated, except where required by law or where a billing error occurred.",
    trialItems: [
      "Review the trial description before purchase",
      "Use the trial to test the relevant agent and output format",
      "Cancel before renewal if you do not want continued access",
      "Contact Runexa if you believe a technical billing issue occurred",
    ],

    creditsTitle: "Credits and usage-based purchases",
    creditsText:
      "AI credits and usage-based purchases are generally non-refundable once consumed or used for AI processing, because the requested analysis, compute, processing, or output has already been delivered.",
    creditsCards: [
      [
        "Unused Credits",
        "Unused credits may remain available according to the applicable plan, offer, account rules, or expiration terms shown at purchase.",
      ],
      [
        "Consumed Credits",
        "Credits used for completed AI processing, document analysis, report generation, or agent workflows are generally not refundable.",
      ],
      [
        "Processing Failures",
        "If a technical failure prevents delivery of a paid analysis, Runexa may review the issue and may provide credits, correction, or adjustment where appropriate.",
      ],
      [
        "Plan Limits",
        "Credits, quotas, and plan access may be subject to fair-use, abuse-prevention, product, or enterprise rules.",
      ],
    ],

    subscriptionsTitle: "Subscriptions and renewals",
    subscriptionsText:
      "Subscription plans may renew automatically unless canceled before the next billing cycle. Canceling a subscription usually stops future renewals, but does not automatically refund fees already paid for the current billing period unless required by law.",
    subscriptionsItems: [
      "Users are responsible for canceling subscriptions before renewal",
      "Cancellation normally applies to future billing periods",
      "Already-paid subscription periods are generally non-refundable once access has been provided",
      "If you believe a renewal happened due to an error, contact Runexa for review",
    ],

    errorsTitle: "Billing errors and duplicate charges",
    errorsText:
      "If you believe you were charged incorrectly, charged more than once, charged after cancellation, or affected by a payment processor issue, contact Runexa with the account email, charge date, amount, and a brief explanation.",
    errorsItems: [
      "Duplicate charge",
      "Incorrect amount",
      "Payment processor error",
      "Failed payment showing as charged",
      "Subscription renewal concern",
      "Technical issue affecting paid access",
    ],

    consumerTitle: "Consumer rights",
    consumerText:
      "Consumer protection rights, cancellation rights, cooling-off periods, and refund rights vary by jurisdiction. Nothing in this Policy limits rights that cannot legally be excluded under applicable law.",
    consumerItems: [
      "EU, UK, US state, or other local consumer rules may apply depending on your location",
      "Some digital services may have special rules once access or processing has started",
      "Business, enterprise, or professional purchases may be treated differently from consumer purchases",
      "Runexa will review legally required refund or cancellation rights where applicable",
    ],

    notRefundableTitle: "What is generally not refundable",
    notRefundableText:
      "Unless required by law or approved by Runexa in a specific case, the following are generally not refundable:",
    notRefundableItems: [
      "Completed AI analyses or generated reports",
      "Credits already consumed for processing",
      "Trial access that has already been activated",
      "Subscription periods where access has already been provided",
      "Refund requests based only on AI output disagreement, model limitations, or expected variation",
      "Accounts suspended or terminated for abuse, fraud, chargeback misuse, or policy violations",
    ],

    caseByCaseTitle: "Case-by-case adjustments",
    caseByCaseText:
      "Runexa Systems LLC may, at its discretion, provide refunds, credits, extensions, or account adjustments in exceptional situations, including technical failures, duplicate charges, billing mistakes, or other reasonable circumstances.",

    chargebackTitle: "Chargebacks and payment abuse",
    chargebackText:
      "Fraudulent chargebacks, payment abuse, misuse of promotional offers, or attempts to improperly reverse legitimate payments may result in account restriction, suspension, termination, or recovery actions where permitted by law.",

    updatesTitle: "Policy updates",
    updatesText:
      "Runexa Systems LLC may update this Refund Policy from time to time. Updated versions will be posted on this page with a revised “Last updated” date.",

    contactTitle: "Contact",
    contactText:
      "Refund, billing, or subscription questions may be sent to contact@runexa.ai.",
  },

  fr: {
    title: "Politique de remboursement",
    updated: "Dernière mise à jour : juin 2026",
    eyebrow: "Remboursements & facturation",
    heroTitle: "Une facturation transparente pour les crédits, essais et abonnements.",
    heroText:
      "Cette Politique de remboursement explique comment Runexa Systems LLC traite les essais payants, crédits, abonnements, erreurs de facturation, doublons de paiement et demandes de remboursement. Runexa examine les problèmes de facturation raisonnables au cas par cas et respecte les droits consommateurs lorsque la loi applicable l’exige.",
    primaryCta: "Contacter le support facturation",
    secondaryCta: "Voir les conditions",

    highlightsTitle: "Principes de facturation",
    highlightsSubtitle:
      "Runexa utilise un modèle de plateforme basé sur les crédits, avec des règles d’accès claires et des canaux de revue de facturation.",
    highlights: [
      [
        "Plateforme basée sur les crédits",
        "Les crédits sont utilisés pour accéder aux agents IA et aux workflows d’analyse. L’utilisation des crédits peut dépendre de l’agent, de la tâche, du type de fichier ou du plan sélectionné.",
      ],
      [
        "Accès d’essai",
        "Les essais introductifs permettent aux utilisateurs d’évaluer Runexa avant d’acheter des packs de crédits plus importants ou des abonnements.",
      ],
      [
        "Revue de facturation",
        "Les doublons, paiements échoués, erreurs de prestataire de paiement ou frais incorrects peuvent être examinés en contactant Runexa.",
      ],
      [
        "Droits consommateurs",
        "Rien dans cette Politique ne limite les droits impératifs de protection, d’annulation ou de remboursement des consommateurs prévus par la loi applicable.",
      ],
    ],

    howTitle: "Fonctionnement de la facturation Runexa",
    howText:
      "Runexa peut proposer des essais payants, crédits IA, abonnements, plans entreprise ou autres options d’accès payant. Les prix, crédits inclus, conditions de renouvellement et limites de plan sont indiqués au moment de l’achat ou sur la page produit, tarifaire ou de paiement applicable.",
    howItems: [
      "Les crédits peuvent être consommés lorsqu’un agent IA effectue une analyse ou génère un résultat",
      "Les abonnements peuvent se renouveler automatiquement sauf annulation avant le prochain cycle de facturation",
      "Les plans entreprise ou personnalisés peuvent être régis par des conditions écrites séparées",
      "Le traitement des paiements peut être assuré par des prestataires de paiement tiers",
    ],

    trialTitle: "Essais et offres introductives",
    trialText:
      "L’essai introductif est conçu pour aider les utilisateurs à évaluer la plateforme avant d’acheter des packs de crédits plus importants ou des abonnements. Les frais d’essai sont généralement non remboursables une fois l’accès activé, sauf lorsque la loi l’exige ou en cas d’erreur de facturation.",
    trialItems: [
      "Vérifiez la description de l’essai avant l’achat",
      "Utilisez l’essai pour tester l’agent et le format de sortie concernés",
      "Annulez avant le renouvellement si vous ne souhaitez pas continuer l’accès",
      "Contactez Runexa si vous pensez qu’un problème technique de facturation est survenu",
    ],

    creditsTitle: "Crédits et achats à l’usage",
    creditsText:
      "Les crédits IA et achats à l’usage sont généralement non remboursables une fois consommés ou utilisés pour un traitement IA, car l’analyse, le calcul, le traitement ou le résultat demandé a déjà été fourni.",
    creditsCards: [
      [
        "Crédits non utilisés",
        "Les crédits non utilisés peuvent rester disponibles selon le plan, l’offre, les règles du compte ou les conditions d’expiration indiquées lors de l’achat.",
      ],
      [
        "Crédits consommés",
        "Les crédits utilisés pour un traitement IA terminé, une analyse documentaire, la génération d’un rapport ou un workflow agent sont généralement non remboursables.",
      ],
      [
        "Échecs de traitement",
        "Si une défaillance technique empêche la livraison d’une analyse payante, Runexa peut examiner le problème et fournir des crédits, une correction ou un ajustement si approprié.",
      ],
      [
        "Limites de plan",
        "Les crédits, quotas et accès au plan peuvent être soumis à des règles d’usage raisonnable, de prévention des abus, de produit ou d’entreprise.",
      ],
    ],

    subscriptionsTitle: "Abonnements et renouvellements",
    subscriptionsText:
      "Les abonnements peuvent se renouveler automatiquement sauf annulation avant le prochain cycle de facturation. L’annulation d’un abonnement arrête généralement les futurs renouvellements, mais ne rembourse pas automatiquement les frais déjà payés pour la période en cours, sauf lorsque la loi l’exige.",
    subscriptionsItems: [
      "Les utilisateurs sont responsables de l’annulation de leur abonnement avant le renouvellement",
      "L’annulation s’applique normalement aux périodes de facturation futures",
      "Les périodes d’abonnement déjà payées sont généralement non remboursables lorsque l’accès a été fourni",
      "Si vous pensez qu’un renouvellement résulte d’une erreur, contactez Runexa pour examen",
    ],

    errorsTitle: "Erreurs de facturation et doublons",
    errorsText:
      "Si vous pensez avoir été facturé incorrectement, plusieurs fois, après annulation ou à la suite d’un problème de prestataire de paiement, contactez Runexa avec l’adresse email du compte, la date du débit, le montant et une brève explication.",
    errorsItems: [
      "Double débit",
      "Montant incorrect",
      "Erreur du prestataire de paiement",
      "Paiement échoué apparaissant comme débité",
      "Question relative à un renouvellement d’abonnement",
      "Problème technique affectant un accès payant",
    ],

    consumerTitle: "Droits consommateurs",
    consumerText:
      "Les droits de protection des consommateurs, droits d’annulation, délais de rétractation et droits au remboursement varient selon la juridiction. Rien dans cette Politique ne limite les droits qui ne peuvent pas légalement être exclus par la loi applicable.",
    consumerItems: [
      "Les règles UE, Royaume-Uni, États américains ou autres règles locales peuvent s’appliquer selon votre localisation",
      "Certains services numériques peuvent être soumis à des règles particulières lorsque l’accès ou le traitement a commencé",
      "Les achats business, entreprise ou professionnels peuvent être traités différemment des achats consommateurs",
      "Runexa examinera les droits de remboursement ou d’annulation légalement requis lorsque cela est applicable",
    ],

    notRefundableTitle: "Ce qui n’est généralement pas remboursable",
    notRefundableText:
      "Sauf lorsque la loi l’exige ou lorsque Runexa l’approuve dans un cas spécifique, les éléments suivants ne sont généralement pas remboursables :",
    notRefundableItems: [
      "Analyses IA terminées ou rapports générés",
      "Crédits déjà consommés pour un traitement",
      "Accès d’essai déjà activé",
      "Périodes d’abonnement pour lesquelles l’accès a déjà été fourni",
      "Demandes fondées uniquement sur un désaccord avec le résultat IA, des limites du modèle ou une variation attendue",
      "Comptes suspendus ou résiliés pour abus, fraude, usage abusif de chargeback ou violation des politiques",
    ],

    caseByCaseTitle: "Ajustements au cas par cas",
    caseByCaseText:
      "Runexa Systems LLC peut, à sa discrétion, fournir des remboursements, crédits, extensions ou ajustements de compte dans des situations exceptionnelles, notamment défaillances techniques, doublons de facturation, erreurs de facturation ou autres circonstances raisonnables.",

    chargebackTitle: "Chargebacks et abus de paiement",
    chargebackText:
      "Les chargebacks frauduleux, abus de paiement, détournements d’offres promotionnelles ou tentatives d’annulation abusive de paiements légitimes peuvent entraîner restriction, suspension, résiliation du compte ou actions de recouvrement lorsque la loi le permet.",

    updatesTitle: "Mises à jour de la politique",
    updatesText:
      "Runexa Systems LLC peut mettre à jour cette Politique de remboursement de temps à autre. Les versions mises à jour seront publiées sur cette page avec une date de “Dernière mise à jour” révisée.",

    contactTitle: "Contact",
    contactText:
      "Les questions relatives aux remboursements, à la facturation ou aux abonnements peuvent être envoyées à contact@runexa.ai.",
  },

  ar: {
    title: "سياسة الاسترداد",
    updated: "آخر تحديث: يونيو 2026",
    eyebrow: "الاسترداد والفوترة",
    heroTitle: "فوترة واضحة للأرصدة والتجارب والاشتراكات.",
    heroText:
      "تشرح سياسة الاسترداد هذه كيف تتعامل Runexa Systems LLC مع التجارب المدفوعة والأرصدة والاشتراكات وأخطاء الفوترة والرسوم المكررة وطلبات الاسترداد. تراجع Runexa مشكلات الفوترة المعقولة حالة بحالة وتحترم حقوق المستهلك عندما يقتضي القانون المعمول به ذلك.",
    primaryCta: "تواصل مع دعم الفوترة",
    secondaryCta: "عرض الشروط",

    highlightsTitle: "مبادئ الفوترة",
    highlightsSubtitle:
      "تستخدم Runexa نموذج منصة قائم على الأرصدة مع قواعد وصول واضحة وقنوات لمراجعة الفوترة.",
    highlights: [
      [
        "منصة قائمة على الأرصدة",
        "تُستخدم الأرصدة للوصول إلى وكلاء الذكاء الاصطناعي وسير عمل التحليل. وقد يعتمد استخدام الأرصدة على الوكيل أو المهمة أو نوع الملف أو الخطة المختارة.",
      ],
      [
        "وصول تجريبي",
        "تهدف التجارب التمهيدية إلى تمكين المستخدمين من تقييم Runexa قبل شراء حزم أرصدة أكبر أو اشتراكات.",
      ],
      [
        "مراجعة الفوترة",
        "يمكن مراجعة الرسوم المكررة أو المدفوعات الفاشلة أو أخطاء مزود الدفع أو الرسوم غير الصحيحة من خلال التواصل مع Runexa.",
      ],
      [
        "حقوق المستهلك",
        "لا يحد أي شيء في هذه السياسة من حقوق حماية المستهلك أو الإلغاء أو الاسترداد غير القابلة للتنازل عنها بموجب القانون المعمول به.",
      ],
    ],

    howTitle: "كيف تعمل فوترة Runexa",
    howText:
      "قد تقدم Runexa تجارب مدفوعة أو أرصدة ذكاء اصطناعي أو اشتراكات أو خطط مؤسسات أو خيارات وصول مدفوعة أخرى. يتم عرض الأسعار والأرصدة المشمولة وشروط التجديد وحدود الخطة عند الشراء أو في صفحة المنتج أو الأسعار أو الدفع ذات الصلة.",
    howItems: [
      "قد تُستهلك الأرصدة عندما ينفذ وكيل ذكاء اصطناعي تحليلاً أو ينشئ مخرجاً",
      "قد تتجدد الاشتراكات تلقائياً ما لم يتم إلغاؤها قبل دورة الفوترة التالية",
      "قد تخضع خطط المؤسسات أو الخطط المخصصة لشروط مكتوبة منفصلة",
      "قد تتم معالجة المدفوعات بواسطة مزودي دفع تابعين لجهات خارجية",
    ],

    trialTitle: "التجارب والعروض التمهيدية",
    trialText:
      "تم تصميم التجربة التمهيدية لمساعدة المستخدمين على تقييم المنصة قبل شراء حزم أرصدة أكبر أو اشتراكات. تكون رسوم التجربة عموماً غير قابلة للاسترداد بعد تفعيل الوصول، إلا إذا اقتضى القانون ذلك أو حدث خطأ في الفوترة.",
    trialItems: [
      "راجع وصف التجربة قبل الشراء",
      "استخدم التجربة لاختبار الوكيل وصيغة المخرجات ذات الصلة",
      "قم بالإلغاء قبل التجديد إذا كنت لا ترغب في استمرار الوصول",
      "تواصل مع Runexa إذا كنت تعتقد أن مشكلة تقنية في الفوترة قد حدثت",
    ],

    creditsTitle: "الأرصدة والمشتريات القائمة على الاستخدام",
    creditsText:
      "تكون أرصدة الذكاء الاصطناعي والمشتريات القائمة على الاستخدام عموماً غير قابلة للاسترداد بعد استهلاكها أو استخدامها في معالجة الذكاء الاصطناعي، لأن التحليل أو الحوسبة أو المعالجة أو المخرجات المطلوبة قد تم تقديمها بالفعل.",
    creditsCards: [
      [
        "الأرصدة غير المستخدمة",
        "قد تبقى الأرصدة غير المستخدمة متاحة وفقاً للخطة أو العرض أو قواعد الحساب أو شروط الانتهاء المعروضة عند الشراء.",
      ],
      [
        "الأرصدة المستهلكة",
        "الأرصدة المستخدمة لمعالجة ذكاء اصطناعي مكتملة أو تحليل مستند أو إنشاء تقرير أو سير عمل وكيل تكون عموماً غير قابلة للاسترداد.",
      ],
      [
        "فشل المعالجة",
        "إذا منع عطل تقني تسليم تحليل مدفوع، قد تراجع Runexa المشكلة وقد تقدم أرصدة أو تصحيحاً أو تعديلاً عند الاقتضاء.",
      ],
      [
        "حدود الخطة",
        "قد تخضع الأرصدة والحصص والوصول إلى الخطة لقواعد الاستخدام العادل أو منع الإساءة أو المنتج أو المؤسسة.",
      ],
    ],

    subscriptionsTitle: "الاشتراكات والتجديدات",
    subscriptionsText:
      "قد تتجدد خطط الاشتراك تلقائياً ما لم يتم إلغاؤها قبل دورة الفوترة التالية. عادةً ما يوقف إلغاء الاشتراك التجديدات المستقبلية، لكنه لا يرد تلقائياً الرسوم المدفوعة بالفعل للفترة الحالية إلا إذا اقتضى القانون ذلك.",
    subscriptionsItems: [
      "يتحمل المستخدمون مسؤولية إلغاء الاشتراكات قبل التجديد",
      "ينطبق الإلغاء عادةً على فترات الفوترة المستقبلية",
      "فترات الاشتراك المدفوعة بالفعل تكون عموماً غير قابلة للاسترداد بعد توفير الوصول",
      "إذا كنت تعتقد أن التجديد حدث بسبب خطأ، تواصل مع Runexa للمراجعة",
    ],

    errorsTitle: "أخطاء الفوترة والرسوم المكررة",
    errorsText:
      "إذا كنت تعتقد أنه تم تحصيل مبلغ منك بشكل غير صحيح أو أكثر من مرة أو بعد الإلغاء أو بسبب مشكلة لدى مزود الدفع، فتواصل مع Runexa مع بريد الحساب وتاريخ الرسوم والمبلغ وشرح موجز.",
    errorsItems: [
      "رسوم مكررة",
      "مبلغ غير صحيح",
      "خطأ مزود الدفع",
      "دفعة فاشلة تظهر كأنها محصلة",
      "مشكلة تتعلق بتجديد الاشتراك",
      "مشكلة تقنية تؤثر على وصول مدفوع",
    ],

    consumerTitle: "حقوق المستهلك",
    consumerText:
      "تختلف حقوق حماية المستهلك وحقوق الإلغاء وفترات التراجع وحقوق الاسترداد حسب الولاية القضائية. لا يحد أي شيء في هذه السياسة من الحقوق التي لا يمكن قانوناً استبعادها بموجب القانون المعمول به.",
    consumerItems: [
      "قد تنطبق قواعد الاتحاد الأوروبي أو المملكة المتحدة أو الولايات الأمريكية أو قواعد محلية أخرى حسب موقعك",
      "قد تخضع بعض الخدمات الرقمية لقواعد خاصة بمجرد بدء الوصول أو المعالجة",
      "قد تُعامل مشتريات الأعمال أو المؤسسات أو المشتريات المهنية بشكل مختلف عن مشتريات المستهلكين",
      "ستراجع Runexa حقوق الاسترداد أو الإلغاء المطلوبة قانوناً عند الاقتضاء",
    ],

    notRefundableTitle: "ما لا يكون قابلاً للاسترداد عادةً",
    notRefundableText:
      "ما لم يقتض القانون ذلك أو توافق Runexa في حالة محددة، فإن ما يلي عموماً غير قابل للاسترداد:",
    notRefundableItems: [
      "تحليلات الذكاء الاصطناعي المكتملة أو التقارير المنشأة",
      "الأرصدة التي تم استهلاكها بالفعل للمعالجة",
      "الوصول التجريبي الذي تم تفعيله بالفعل",
      "فترات الاشتراك التي تم توفير الوصول لها بالفعل",
      "طلبات الاسترداد القائمة فقط على عدم الاتفاق مع مخرجات الذكاء الاصطناعي أو حدود النموذج أو الاختلاف المتوقع",
      "الحسابات المعلقة أو المنهية بسبب الإساءة أو الاحتيال أو إساءة استخدام استرداد المدفوعات أو انتهاك السياسات",
    ],

    caseByCaseTitle: "تعديلات حسب كل حالة",
    caseByCaseText:
      "يجوز لـ Runexa Systems LLC، وفقاً لتقديرها، تقديم استردادات أو أرصدة أو تمديدات أو تعديلات حساب في حالات استثنائية، بما في ذلك الأعطال التقنية أو الرسوم المكررة أو أخطاء الفوترة أو ظروف معقولة أخرى.",

    chargebackTitle: "استرداد المدفوعات وإساءة الدفع",
    chargebackText:
      "قد تؤدي عمليات استرداد المدفوعات الاحتيالية أو إساءة الدفع أو إساءة استخدام العروض الترويجية أو محاولات عكس المدفوعات المشروعة بشكل غير صحيح إلى تقييد الحساب أو تعليقه أو إنهائه أو اتخاذ إجراءات استرداد حيث يسمح القانون.",

    updatesTitle: "تحديثات السياسة",
    updatesText:
      "يجوز لـ Runexa Systems LLC تحديث سياسة الاسترداد هذه من وقت لآخر. سيتم نشر النسخ المحدثة على هذه الصفحة مع تاريخ “آخر تحديث” معدل.",

    contactTitle: "التواصل",
    contactText:
      "يمكن إرسال أسئلة الاسترداد أو الفوترة أو الاشتراك إلى contact@runexa.ai.",
  },
} satisfies Record<Locale, {
  title: string;
  updated: string;
  eyebrow: string;
  heroTitle: string;
  heroText: string;
  primaryCta: string;
  secondaryCta: string;
  highlightsTitle: string;
  highlightsSubtitle: string;
  highlights: string[][];
  howTitle: string;
  howText: string;
  howItems: string[];
  trialTitle: string;
  trialText: string;
  trialItems: string[];
  creditsTitle: string;
  creditsText: string;
  creditsCards: string[][];
  subscriptionsTitle: string;
  subscriptionsText: string;
  subscriptionsItems: string[];
  errorsTitle: string;
  errorsText: string;
  errorsItems: string[];
  consumerTitle: string;
  consumerText: string;
  consumerItems: string[];
  notRefundableTitle: string;
  notRefundableText: string;
  notRefundableItems: string[];
  caseByCaseTitle: string;
  caseByCaseText: string;
  chargebackTitle: string;
  chargebackText: string;
  updatesTitle: string;
  updatesText: string;
  contactTitle: string;
  contactText: string;
}>;

export default function RefundPolicyClient({
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

  const t = refundCopy[locale];

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
                {t.highlightsTitle}
              </h2>

              <p className="mt-3 text-sm leading-6 text-slate-300">
                {t.highlightsSubtitle}
              </p>

              <div className="mt-8 space-y-4">
                {t.highlights.map(([title, text]) => (
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
            {t.howTitle}
          </h2>

          <p className="mt-4 max-w-4xl text-slate-600">
            {t.howText}
          </p>

          <div className="mt-6 grid gap-3 md:grid-cols-2">
            {t.howItems.map((item) => (
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
            {t.trialTitle}
          </h2>

          <p className="mt-4 max-w-4xl text-slate-600">
            {t.trialText}
          </p>

          <div className="mt-6 grid gap-3 md:grid-cols-2">
            {t.trialItems.map((item) => (
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
            {t.creditsTitle}
          </h2>

          <p className="mt-4 max-w-4xl text-slate-600">
            {t.creditsText}
          </p>

          <div className="mt-8 grid gap-4 md:grid-cols-2">
            {t.creditsCards.map(([title, text]) => (
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
            {t.subscriptionsTitle}
          </h2>

          <p className="mt-4 max-w-4xl text-slate-600">
            {t.subscriptionsText}
          </p>

          <div className="mt-6 grid gap-3 md:grid-cols-2">
            {t.subscriptionsItems.map((item) => (
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
            {t.errorsTitle}
          </h2>

          <p className="mt-4 max-w-4xl text-slate-600">
            {t.errorsText}
          </p>

          <div className="mt-6 grid gap-3 md:grid-cols-3">
            {t.errorsItems.map((item) => (
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
            {t.consumerTitle}
          </h2>

          <p className="mt-4 max-w-4xl text-slate-600">
            {t.consumerText}
          </p>

          <div className="mt-6 grid gap-3 md:grid-cols-2">
            {t.consumerItems.map((item) => (
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
            {t.notRefundableTitle}
          </h2>

          <p className="mt-4 max-w-4xl text-slate-600">
            {t.notRefundableText}
          </p>

          <div className="mt-6 grid gap-3 md:grid-cols-2">
            {t.notRefundableItems.map((item) => (
              <div
                key={item}
                className="rounded-xl border border-slate-200 bg-slate-50 p-4 text-sm leading-6 text-slate-700"
              >
                {item}
              </div>
            ))}
          </div>
        </section>

        <section className="grid gap-8 md:grid-cols-2">
          <article className="rounded-[2rem] border border-white/10 bg-white p-8 shadow-xl md:p-10">
            <h2 className="text-2xl font-bold text-slate-950">
              {t.caseByCaseTitle}
            </h2>

            <p className="mt-4 text-slate-600">
              {t.caseByCaseText}
            </p>
          </article>

          <article className="rounded-[2rem] border border-white/10 bg-white p-8 shadow-xl md:p-10">
            <h2 className="text-2xl font-bold text-slate-950">
              {t.chargebackTitle}
            </h2>

            <p className="mt-4 text-slate-600">
              {t.chargebackText}
            </p>
          </article>
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
                {t.updatesTitle}
              </h2>

              <p className="mt-2 whitespace-normal break-words text-slate-600">
                {t.updatesText}
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-slate-950">
                {t.contactTitle}
              </h2>

              <p className="mt-2 whitespace-normal break-words text-slate-600">
                {t.contactText}
              </p>
            </section>
          </div>
        </section>
      </div>
    </main>
  );
}
