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

const termsCopy = {
  en: {
    title: "Terms of Service",
    updated: "Last updated: June 2026",
    eyebrow: "Service terms",
    heroTitle: "Clear terms for using Runexa.",
    heroText:
      "These Terms explain the rules for using Runexa, including accounts, acceptable use, AI outputs, credits, ownership, and service limitations. They work together with the Privacy Policy, Security page, Product Terms, Acceptable Use Policy, AI Disclaimer, Cookie Policy, and Refund Policy.",
    primaryCta: "Contact Runexa",
    secondaryCta: "Read AI Disclaimer",

    quickTitle: "Key terms",
    quickItems: [
      "You must use Runexa lawfully and only upload content you have the right to use.",
      "You keep ownership of the content you upload.",
      "Runexa provides AI-assisted informational and decision-support outputs.",
      "AI outputs must be reviewed before important decisions.",
      "Credits, trials, and subscriptions follow the pricing and refund terms shown at purchase.",
      "Runexa may suspend access for misuse, security risk, fraud, or violation of these Terms.",
    ],

    frameworkTitle: "How these terms fit together",
    frameworkSubtitle:
      "Runexa separates legal topics so each page has a clear role.",
    framework: [
      ["Privacy", "Explains what data is collected, used, retained, deleted, and shared."],
      ["Security", "Explains technical, operational, and data-handling safeguards."],
      ["AI Disclaimer", "Explains AI limitations, human review, and no professional advice."],
      ["Product Terms", "Explains agent-specific and plan-specific product conditions."],
    ],

    sections: [
      {
        title: "1. Overview",
        text:
          "Runexa Systems LLC provides access to AI-powered tools, workspaces, agents, workflows, and reports designed to assist users with document analysis, learning support, financial insights, business analysis, and decision support. By accessing or using Runexa, you agree to these Terms of Service.",
      },
      {
        title: "2. Eligibility",
        text:
          "Certain educational services provided by Runexa may be used by children and minors. Where a user has not reached the minimum age required under applicable law to independently manage an account, access to and use of the services must be authorized or supervised by a parent, legal guardian, or educational institution where such authorization or supervision is required. By permitting a minor to use the services, the responsible parent, legal guardian, or educational institution acknowledges and accepts responsibility for the minor’s use of the services and compliance with these Terms.",
      },
      {
        title: "3. Account Responsibilities",
        text:
          "You are responsible for maintaining the security of your account, login credentials, devices, workspace access, and all activity under your account. You must provide accurate account information and promptly notify Runexa of unauthorized access or suspected account compromise.",
      },
      {
        title: "4. Acceptable Use",
        text:
          "You may not use Runexa for illegal, harmful, fraudulent, abusive, infringing, or unauthorized activity. You may not upload content you do not have the right to use, disrupt the platform, bypass usage limits, reverse engineer the services, attack the infrastructure, or use the services in ways that violate applicable law or third-party rights.",
      },
      {
        title: "5. User Content and Ownership",
        text:
          "You retain ownership of the documents, data, text, files, and other content you upload to Runexa. You grant Runexa the limited rights necessary to process your content, provide the requested services, generate outputs, secure the platform, troubleshoot issues, enforce these Terms, and operate the services as described in the Privacy Policy.",
      },
      {
        title: "6. AI Services and Outputs",
        text:
          "Runexa provides AI-assisted informational and decision-support outputs. AI-generated outputs may be inaccurate, incomplete, outdated, inconsistent, or misleading. You are responsible for independently reviewing and verifying outputs before relying on them. AI outputs should not be used as the sole basis for important legal, financial, educational, employment, compliance, business, or other high-impact decisions.",
      },
      {
        title: "7. No Professional Advice",
        text:
          "Runexa is a software platform and does not provide legal, financial, tax, accounting, investment, medical, regulatory, security, or other regulated professional advice. You should consult qualified professionals when professional advice is required.",
      },
      {
        title: "8. Payments, Credits, Trials, and Billing",
        text:
          "Paid trials, credits, subscriptions, plans, and enterprise arrangements are subject to the pricing, quotas, renewal terms, limitations, and refund rules shown at the time of purchase or agreed in writing. Credits may expire, be limited by plan, or be non-refundable except where required by law or stated in the applicable Refund Policy.",
      },
      {
        title: "9. Plans, Availability, and Changes",
        text:
          "Runexa may add, modify, limit, suspend, discontinue, or rename features, agents, workflows, usage limits, plans, pricing, and availability over time. Some features may be experimental, beta, region-limited, usage-limited, or available only to certain plans or enterprise customers.",
      },
      {
        title: "10. Intellectual Property",
        text:
          "Runexa Systems LLC owns all rights, title, and interest in the platform, software, interfaces, designs, branding, AI agent workflows, prompts, evaluation methods, templates, documentation, technology, and related intellectual property. These Terms do not grant you ownership of Runexa technology.",
      },
      {
        title: "11. Third-Party Services",
        text:
          "Runexa may rely on third-party providers for hosting, storage, databases, payments, analytics, communications, AI processing, authentication, and security. Your use of some features may also be subject to third-party terms or availability.",
      },
      {
        title: "12. Suspension and Termination",
        text:
          "Runexa may suspend or terminate access to the services if you violate these Terms, fail to pay amounts due, create legal or security risk, abuse the services, attempt unauthorized access, infringe third-party rights, or use the platform in a way that may harm Runexa, users, providers, or the public.",
      },
      {
        title: "13. Disclaimers",
        text:
          "The services are provided on an “as is” and “as available” basis to the maximum extent permitted by law. Runexa does not guarantee that the services will be uninterrupted, error-free, secure, accurate, complete, or suitable for every use case.",
      },
      {
        title: "14. Limitation of Liability",
        text:
          "To the maximum extent permitted by law, Runexa Systems LLC is not liable for indirect, incidental, special, consequential, exemplary, or punitive damages, including loss of profits, revenue, business opportunities, data, goodwill, legal disputes, financial losses, or consequences resulting from misuse or reliance on AI outputs.",
      },
      {
        title: "15. Indemnity",
        text:
          "You agree to defend, indemnify, and hold harmless Runexa Systems LLC from claims, damages, liabilities, losses, and expenses arising from your misuse of the services, violation of these Terms, violation of law, uploaded content, or infringement of third-party rights.",
      },
      {
        title: "16. Governing Law",
        text:
          "These Terms are governed by the laws of the State of Wyoming, United States, without regard to conflict of law principles, unless applicable consumer protection law requires otherwise.",
      },
      {
        title: "17. Changes to These Terms",
        text:
          "Runexa may update these Terms from time to time. Updated Terms will be posted on this page with a revised “Last updated” date. Continued use of the services after an update means the updated Terms apply from their effective date.",
      },
      {
        title: "18. Contact",
        text:
          "Questions about these Terms may be sent to contact@runexa.ai.",
      },
    ],
  },

  fr: {
    title: "Conditions d’utilisation",
    updated: "Dernière mise à jour : juin 2026",
    eyebrow: "Conditions du service",
    heroTitle: "Des conditions claires pour utiliser Runexa.",
    heroText:
      "Ces Conditions expliquent les règles d’utilisation de Runexa, notamment les comptes, l’utilisation acceptable, les résultats IA, les crédits, la propriété et les limites du service. Elles fonctionnent avec la Politique de confidentialité, la page Sécurité, les Conditions du produit, la Politique d’utilisation acceptable, l’Avertissement relatif à l’IA, la Politique cookies et la Politique de remboursement.",
    primaryCta: "Contacter Runexa",
    secondaryCta: "Lire l’avertissement IA",

    quickTitle: "Points clés",
    quickItems: [
      "Vous devez utiliser Runexa légalement et importer uniquement du contenu que vous avez le droit d’utiliser.",
      "Vous conservez la propriété du contenu que vous importez.",
      "Runexa fournit des résultats assistés par IA à titre informatif et d’aide à la décision.",
      "Les résultats IA doivent être vérifiés avant toute décision importante.",
      "Les crédits, essais et abonnements suivent les prix et règles de remboursement indiqués lors de l’achat.",
      "Runexa peut suspendre l’accès en cas d’abus, risque de sécurité, fraude ou violation de ces Conditions.",
    ],

    frameworkTitle: "Comment ces conditions s’articulent",
    frameworkSubtitle:
      "Runexa sépare les sujets juridiques afin que chaque page ait un rôle clair.",
    framework: [
      ["Confidentialité", "Explique quelles données sont collectées, utilisées, conservées, supprimées et partagées."],
      ["Sécurité", "Explique les mesures techniques, opérationnelles et de traitement des données."],
      ["Avertissement IA", "Explique les limites de l’IA, la revue humaine et l’absence de conseil professionnel."],
      ["Conditions du produit", "Explique les conditions spécifiques aux agents et aux plans."],
    ],

    sections: [
      {
        title: "1. Vue d’ensemble",
        text:
          "Runexa Systems LLC fournit l’accès à des outils, espaces de travail, agents, workflows et rapports alimentés par l’IA, conçus pour assister les utilisateurs dans l’analyse documentaire, l’apprentissage, les insights financiers, l’analyse business et l’aide à la décision. En accédant à Runexa ou en l’utilisant, vous acceptez ces Conditions d’utilisation.",
      },
      {
        title: "2. Éligibilité",
        text:
          "Certains services éducatifs de Runexa peuvent être utilisés par des enfants et des mineurs. Lorsqu’un utilisateur n’a pas atteint l’âge requis par la législation applicable pour gérer un compte de manière autonome, l’utilisation des services doit être autorisée ou supervisée par un parent, un tuteur légal ou un établissement éducatif lorsque cela est requis. En autorisant un mineur à utiliser les services, le parent, le tuteur ou l’établissement responsable assume la responsabilité de cette utilisation et du respect des présentes Conditions.",
      },
      {
        title: "3. Responsabilités liées au compte",
        text:
          "Vous êtes responsable de la sécurité de votre compte, de vos identifiants, appareils, accès à l’espace de travail et de toute activité effectuée via votre compte. Vous devez fournir des informations de compte exactes et informer rapidement Runexa de tout accès non autorisé ou compromission suspectée.",
      },
      {
        title: "4. Utilisation acceptable",
        text:
          "Vous ne pouvez pas utiliser Runexa pour une activité illégale, nuisible, frauduleuse, abusive, contrefaisante ou non autorisée. Vous ne pouvez pas importer du contenu que vous n’avez pas le droit d’utiliser, perturber la plateforme, contourner les limites d’usage, faire de l’ingénierie inverse, attaquer l’infrastructure ou utiliser les services d’une manière contraire à la loi applicable ou aux droits de tiers.",
      },
      {
        title: "5. Contenu utilisateur et propriété",
        text:
          "Vous conservez la propriété des documents, données, textes, fichiers et autres contenus que vous importez dans Runexa. Vous accordez à Runexa les droits limités nécessaires pour traiter votre contenu, fournir les services demandés, générer les résultats, sécuriser la plateforme, résoudre les problèmes, appliquer ces Conditions et opérer les services comme décrit dans la Politique de confidentialité.",
      },
      {
        title: "6. Services IA et résultats",
        text:
          "Runexa fournit des résultats assistés par IA à titre informatif et d’aide à la décision. Les résultats générés par l’IA peuvent être inexacts, incomplets, obsolètes, incohérents ou trompeurs. Vous êtes responsable de relire et vérifier les résultats avant de vous y fier. Les résultats IA ne doivent pas être utilisés comme base unique pour des décisions juridiques, financières, éducatives, professionnelles, de conformité, business ou autres décisions à impact élevé.",
      },
      {
        title: "7. Pas de conseil professionnel",
        text:
          "Runexa est une plateforme logicielle et ne fournit pas de conseil juridique, financier, fiscal, comptable, d’investissement, médical, réglementaire, de sécurité ou autre conseil professionnel réglementé. Vous devez consulter des professionnels qualifiés lorsqu’un avis professionnel est nécessaire.",
      },
      {
        title: "8. Paiements, crédits, essais et facturation",
        text:
          "Les essais payants, crédits, abonnements, plans et accords entreprise sont soumis aux prix, quotas, conditions de renouvellement, limites et règles de remboursement indiqués lors de l’achat ou convenus par écrit. Les crédits peuvent expirer, être limités par plan ou être non remboursables sauf obligation légale ou disposition contraire dans la Politique de remboursement applicable.",
      },
      {
        title: "9. Plans, disponibilité et changements",
        text:
          "Runexa peut ajouter, modifier, limiter, suspendre, arrêter ou renommer des fonctionnalités, agents, workflows, limites d’usage, plans, prix et disponibilités au fil du temps. Certaines fonctionnalités peuvent être expérimentales, bêta, limitées par région, limitées par usage ou réservées à certains plans ou clients entreprise.",
      },
      {
        title: "10. Propriété intellectuelle",
        text:
          "Runexa Systems LLC détient tous les droits, titres et intérêts relatifs à la plateforme, aux logiciels, interfaces, designs, marques, workflows d’agents IA, prompts, méthodes d’évaluation, modèles, documentation, technologies et propriété intellectuelle associée. Ces Conditions ne vous transfèrent aucun droit de propriété sur la technologie Runexa.",
      },
      {
        title: "11. Services tiers",
        text:
          "Runexa peut s’appuyer sur des prestataires tiers pour l’hébergement, le stockage, les bases de données, les paiements, l’analyse, les communications, le traitement IA, l’authentification et la sécurité. L’utilisation de certaines fonctionnalités peut également être soumise aux conditions ou à la disponibilité de tiers.",
      },
      {
        title: "12. Suspension et résiliation",
        text:
          "Runexa peut suspendre ou résilier l’accès aux services si vous violez ces Conditions, ne payez pas les montants dus, créez un risque juridique ou de sécurité, abusez des services, tentez un accès non autorisé, violez les droits de tiers ou utilisez la plateforme d’une manière susceptible de nuire à Runexa, aux utilisateurs, aux prestataires ou au public.",
      },
      {
        title: "13. Exclusions de garantie",
        text:
          "Les services sont fournis « tels quels » et « selon disponibilité » dans la mesure maximale permise par la loi. Runexa ne garantit pas que les services seront ininterrompus, exempts d’erreurs, sécurisés, exacts, complets ou adaptés à chaque cas d’usage.",
      },
      {
        title: "14. Limitation de responsabilité",
        text:
          "Dans la mesure maximale permise par la loi, Runexa Systems LLC n’est pas responsable des dommages indirects, accessoires, spéciaux, consécutifs, exemplaires ou punitifs, y compris pertes de bénéfices, revenus, opportunités business, données, réputation, litiges juridiques, pertes financières ou conséquences résultant d’un mauvais usage ou d’une confiance accordée aux résultats IA.",
      },
      {
        title: "15. Indemnisation",
        text:
          "Vous acceptez de défendre, indemniser et dégager Runexa Systems LLC de toute responsabilité concernant les réclamations, dommages, responsabilités, pertes et dépenses résultant de votre mauvais usage des services, violation de ces Conditions, violation de la loi, contenu importé ou atteinte aux droits de tiers.",
      },
      {
        title: "16. Droit applicable",
        text:
          "Ces Conditions sont régies par les lois de l’État du Wyoming, États-Unis, sans égard aux principes de conflit de lois, sauf si une loi de protection des consommateurs applicable impose autrement.",
      },
      {
        title: "17. Modifications de ces Conditions",
        text:
          "Runexa peut mettre à jour ces Conditions périodiquement. Les Conditions mises à jour seront publiées sur cette page avec une date de dernière mise à jour révisée. La poursuite de l’utilisation des services après une mise à jour signifie que les Conditions mises à jour s’appliquent à partir de leur date d’entrée en vigueur.",
      },
      {
        title: "18. Contact",
        text:
          "Les questions concernant ces Conditions peuvent être envoyées à contact@runexa.ai.",
      },
    ],
  },

  ar: {
    title: "شروط الاستخدام",
    updated: "آخر تحديث: يونيو 2026",
    eyebrow: "شروط الخدمة",
    heroTitle: "شروط واضحة لاستخدام Runexa.",
    heroText:
      "توضح هذه الشروط قواعد استخدام Runexa، بما في ذلك الحسابات والاستخدام المقبول ومخرجات الذكاء الاصطناعي والأرصدة والملكية وحدود الخدمة. تعمل هذه الشروط مع سياسة الخصوصية وصفحة الأمان وشروط المنتج وسياسة الاستخدام المقبول وإخلاء مسؤولية الذكاء الاصطناعي وسياسة ملفات تعريف الارتباط وسياسة الاسترداد.",
    primaryCta: "تواصل مع Runexa",
    secondaryCta: "قراءة إخلاء مسؤولية الذكاء الاصطناعي",

    quickTitle: "شروط أساسية",
    quickItems: [
      "يجب استخدام Runexa بشكل قانوني ورفع المحتوى الذي لديك الحق في استخدامه فقط.",
      "تحتفظ بملكية المحتوى الذي ترفعه.",
      "توفر Runexa مخرجات مدعومة بالذكاء الاصطناعي لأغراض معلوماتية ودعم القرار.",
      "يجب مراجعة مخرجات الذكاء الاصطناعي قبل اتخاذ قرارات مهمة.",
      "تخضع الأرصدة والتجارب والاشتراكات للأسعار وشروط الاسترداد المعروضة عند الشراء.",
      "يمكن لـ Runexa تعليق الوصول في حالة إساءة الاستخدام أو مخاطر الأمان أو الاحتيال أو انتهاك هذه الشروط.",
    ],

    frameworkTitle: "كيف ترتبط هذه الشروط بباقي الصفحات",
    frameworkSubtitle:
      "تفصل Runexa المواضيع القانونية حتى يكون لكل صفحة دور واضح.",
    framework: [
      ["الخصوصية", "توضح ما هي البيانات التي يتم جمعها واستخدامها والاحتفاظ بها وحذفها ومشاركتها."],
      ["الأمان", "يوضح الضمانات التقنية والتشغيلية وضوابط معالجة البيانات."],
      ["إخلاء مسؤولية الذكاء الاصطناعي", "يوضح حدود الذكاء الاصطناعي والمراجعة البشرية وعدم تقديم المشورة المهنية."],
      ["شروط المنتج", "توضح الشروط الخاصة بالوكلاء والخطط."],
    ],

    sections: [
      {
        title: "1. نظرة عامة",
        text:
          "توفر Runexa Systems LLC إمكانية الوصول إلى أدوات ومساحات عمل ووكلاء وسير عمل وتقارير مدعومة بالذكاء الاصطناعي، مصممة لمساعدة المستخدمين في تحليل المستندات ودعم التعلم والرؤى المالية وتحليل الأعمال ودعم اتخاذ القرار. باستخدام Runexa أو الوصول إليها، فإنك توافق على شروط الاستخدام هذه.",
      },
      {
        title: "2. الأهلية",
        text:
          "قد تُستخدم بعض الخدمات التعليمية التي تقدمها Runexa من قبل الأطفال والقُصَّر. وإذا لم يكن المستخدم قد بلغ السن القانونية التي تسمح له بإدارة حسابه بشكل مستقل وفقًا للقوانين المعمول بها، فيجب أن يكون استخدام الخدمات مصرحًا به أو خاضعًا لإشراف أحد الوالدين أو الوصي القانوني أو المؤسسة التعليمية، متى كان ذلك مطلوبًا قانونًا. ومن خلال السماح لقاصر باستخدام الخدمات، يقرّ الوالد أو الوصي القانوني أو المؤسسة التعليمية المسؤولة بمسؤوليته عن استخدام القاصر للخدمات والتزامه بهذه الشروط.",
      },
      {
        title: "3. مسؤوليات الحساب",
        text:
          "أنت مسؤول عن الحفاظ على أمان حسابك وبيانات الدخول والأجهزة والوصول إلى مساحة العمل وجميع الأنشطة التي تتم عبر حسابك. يجب عليك تقديم معلومات حساب دقيقة وإبلاغ Runexa فوراً بأي وصول غير مصرح به أو اشتباه في اختراق الحساب.",
      },
      {
        title: "4. الاستخدام المقبول",
        text:
          "لا يجوز استخدام Runexa في أنشطة غير قانونية أو ضارة أو احتيالية أو مسيئة أو منتهكة أو غير مصرح بها. لا يجوز رفع محتوى لا تملك الحق في استخدامه، أو تعطيل المنصة، أو تجاوز حدود الاستخدام، أو إجراء هندسة عكسية، أو مهاجمة البنية التحتية، أو استخدام الخدمات بطريقة تخالف القانون المعمول به أو حقوق الغير.",
      },
      {
        title: "5. محتوى المستخدم والملكية",
        text:
          "تحتفظ بملكية المستندات والبيانات والنصوص والملفات والمحتوى الآخر الذي ترفعه إلى Runexa. تمنح Runexa الحقوق المحدودة اللازمة لمعالجة محتواك، وتقديم الخدمات المطلوبة، وإنشاء النتائج، وتأمين المنصة، وحل المشكلات، وتنفيذ هذه الشروط، وتشغيل الخدمات كما هو موضح في سياسة الخصوصية.",
      },
      {
        title: "6. خدمات الذكاء الاصطناعي والمخرجات",
        text:
          "توفر Runexa مخرجات مدعومة بالذكاء الاصطناعي لأغراض معلوماتية ودعم القرار. قد تكون المخرجات التي يولدها الذكاء الاصطناعي غير دقيقة أو غير مكتملة أو قديمة أو غير متسقة أو مضللة. أنت مسؤول عن مراجعة المخرجات والتحقق منها بشكل مستقل قبل الاعتماد عليها. لا ينبغي استخدام مخرجات الذكاء الاصطناعي كأساس وحيد للقرارات القانونية أو المالية أو التعليمية أو المهنية أو المتعلقة بالامتثال أو الأعمال أو غيرها من القرارات عالية التأثير.",
      },
      {
        title: "7. عدم تقديم مشورة مهنية",
        text:
          "Runexa منصة برمجية ولا تقدم مشورة قانونية أو مالية أو ضريبية أو محاسبية أو استثمارية أو طبية أو تنظيمية أو أمنية أو أي مشورة مهنية منظمة. يجب عليك استشارة مهنيين مؤهلين عندما تكون المشورة المهنية مطلوبة.",
      },
      {
        title: "8. المدفوعات والأرصدة والتجارب والفوترة",
        text:
          "تخضع التجارب المدفوعة والأرصدة والاشتراكات والخطط وترتيبات المؤسسات للأسعار والحصص وشروط التجديد والقيود وقواعد الاسترداد المعروضة عند الشراء أو المتفق عليها كتابياً. قد تنتهي صلاحية الأرصدة أو تكون محدودة حسب الخطة أو غير قابلة للاسترداد إلا عندما يقتضي القانون أو تنص سياسة الاسترداد المعمول بها على خلاف ذلك.",
      },
      {
        title: "9. الخطط والتوفر والتغييرات",
        text:
          "يمكن لـ Runexa إضافة أو تعديل أو تقييد أو تعليق أو إيقاف أو إعادة تسمية الميزات والوكلاء وسير العمل وحدود الاستخدام والخطط والأسعار والتوفر بمرور الوقت. قد تكون بعض الميزات تجريبية أو في مرحلة بيتا أو محدودة حسب المنطقة أو الاستخدام أو متاحة فقط لبعض الخطط أو عملاء المؤسسات.",
      },
      {
        title: "10. الملكية الفكرية",
        text:
          "تمتلك Runexa Systems LLC جميع الحقوق والملكية والمصالح في المنصة والبرمجيات والواجهات والتصاميم والعلامات التجارية وسير عمل وكلاء الذكاء الاصطناعي والتعليمات وطرق التقييم والقوالب والوثائق والتقنيات والملكية الفكرية ذات الصلة. لا تمنحك هذه الشروط ملكية تقنية Runexa.",
      },
      {
        title: "11. خدمات الطرف الثالث",
        text:
          "قد تعتمد Runexa على مزودي خدمات خارجيين للاستضافة والتخزين وقواعد البيانات والمدفوعات والتحليلات والاتصالات ومعالجة الذكاء الاصطناعي والمصادقة والأمان. قد يخضع استخدام بعض الميزات أيضاً لشروط أو توفر أطراف ثالثة.",
      },
      {
        title: "12. التعليق والإنهاء",
        text:
          "يمكن لـ Runexa تعليق أو إنهاء الوصول إلى الخدمات إذا انتهكت هذه الشروط، أو لم تدفع المبالغ المستحقة، أو تسببت في مخاطر قانونية أو أمنية، أو أسأت استخدام الخدمات، أو حاولت الوصول غير المصرح به، أو انتهكت حقوق الغير، أو استخدمت المنصة بطريقة قد تضر Runexa أو المستخدمين أو المزودين أو الجمهور.",
      },
      {
        title: "13. إخلاء الضمانات",
        text:
          "تُقدم الخدمات كما هي وحسب التوفر إلى أقصى حد يسمح به القانون. لا تضمن Runexa أن الخدمات ستكون مستمرة أو خالية من الأخطاء أو آمنة أو دقيقة أو كاملة أو مناسبة لكل حالة استخدام.",
      },
      {
        title: "14. تحديد المسؤولية",
        text:
          "إلى أقصى حد يسمح به القانون، لا تكون Runexa Systems LLC مسؤولة عن الأضرار غير المباشرة أو العرضية أو الخاصة أو التبعية أو النموذجية أو العقابية، بما في ذلك خسارة الأرباح أو الإيرادات أو فرص الأعمال أو البيانات أو السمعة أو النزاعات القانونية أو الخسائر المالية أو العواقب الناتجة عن سوء الاستخدام أو الاعتماد على مخرجات الذكاء الاصطناعي.",
      },
      {
        title: "15. التعويض",
        text:
          "توافق على الدفاع عن Runexa Systems LLC وتعويضها وإبراء ذمتها من المطالبات والأضرار والمسؤوليات والخسائر والمصاريف الناتجة عن سوء استخدامك للخدمات أو انتهاك هذه الشروط أو مخالفة القانون أو المحتوى المرفوع أو انتهاك حقوق الغير.",
      },
      {
        title: "16. القانون الواجب التطبيق",
        text:
          "تخضع هذه الشروط لقوانين ولاية وايومنغ، الولايات المتحدة، دون اعتبار لمبادئ تنازع القوانين، ما لم يقتض قانون حماية المستهلك المعمول به خلاف ذلك.",
      },
      {
        title: "17. التغييرات على هذه الشروط",
        text:
          "قد تقوم Runexa بتحديث هذه الشروط من وقت لآخر. سيتم نشر الشروط المحدثة على هذه الصفحة مع تاريخ آخر تحديث معدل. يعني استمرار استخدام الخدمات بعد التحديث أن الشروط المحدثة تسري من تاريخ فعاليتها.",
      },
      {
        title: "18. التواصل",
        text:
          "يمكن إرسال الأسئلة المتعلقة بهذه الشروط إلى contact@runexa.ai.",
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
  frameworkTitle: string;
  frameworkSubtitle: string;
  framework: string[][];
  sections: { title: string; text: string }[];
}>;

export default function TermsClient({
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

  const t = termsCopy[locale];

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
                  href="mailto:contact@runexa.ai"
                  className="inline-flex items-center justify-center rounded-xl bg-blue-600 px-5 py-3 text-sm font-semibold text-white shadow-sm hover:bg-blue-700"
                >
                  {t.primaryCta}
                </a>

                <a
                  href="/ai-disclaimer"
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
            {t.frameworkTitle}
          </h2>

          <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-600">
            {t.frameworkSubtitle}
          </p>

          <div className="mt-8 grid gap-4 md:grid-cols-4">
            {t.framework.map(([title, text]) => (
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
