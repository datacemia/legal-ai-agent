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

const cookieCopy = {
  en: {
    title: "Cookie Policy",
    updated: "Last updated: June 2026",
    eyebrow: "Cookies & platform preferences",
    heroTitle: "Clear, practical cookie use.",
    heroText:
      "This Cookie Policy explains how Runexa Systems LLC uses cookies and similar technologies to operate the platform, keep sessions secure, remember preferences, understand reliability, and improve the user experience.",
    primaryCta: "Contact Runexa",
    secondaryCta: "View Privacy",

    overviewTitle: "How Runexa uses cookies",
    overviewText:
      "Cookies are small files or similar browser technologies that help websites and applications work properly. Runexa uses cookies for essential platform functions, security, authentication, language preferences, session handling, reliability, and limited analytics where applicable.",

    typesTitle: "Cookie categories",
    typesSubtitle:
      "Runexa uses cookies and similar technologies for specific operational purposes.",
    cookieTypes: [
      [
        "Essential Cookies",
        "Required for login, authentication, account access, session management, routing, and core platform functionality.",
      ],
      [
        "Security Cookies",
        "Used to help detect abuse, protect sessions, reduce fraud, support rate limiting, and maintain platform integrity.",
      ],
      [
        "Preference Cookies",
        "Used to remember choices such as language, interface settings, and session-related preferences.",
      ],
      [
        "Performance & Reliability Cookies",
        "Used to understand errors, loading issues, service availability, and general reliability of the platform.",
      ],
      [
        "Analytics Cookies",
        "May be used to understand aggregated usage patterns and improve user experience, where enabled and permitted.",
      ],
      [
        "Payment & Service Provider Cookies",
        "May be placed by providers that support payments, authentication, hosting, security, or other operational services.",
      ],
    ],

    notForTitle: "What cookies are not used for",
    notForSubtitle:
      "Runexa’s cookie use is designed to support the service, not to expand the use of private uploaded content.",
    notForItems: [
      "Cookies do not give Runexa the right to train public AI models on customer-uploaded content",
      "Cookies are not a substitute for the Privacy Policy or user rights described there",
      "Cookies are not intended to expose one user’s files, outputs, or workspace to another user",
      "Cookies are not used to publish, sell, or publicly disclose private uploaded documents",
    ],

    thirdPartyTitle: "Third-party technologies",
    thirdPartyText:
      "Some cookies or similar technologies may be set by third-party providers that help Runexa operate the platform, including hosting, authentication, analytics, security, payment, infrastructure, or support providers. These providers may process limited technical information according to their own terms and privacy practices.",

    controlsTitle: "Managing cookies",
    controlsText:
      "Most browsers let you block, delete, or manage cookies through browser settings. Blocking essential cookies may prevent login, file upload, analysis workflows, payment flows, or other core features from working correctly.",
    controlsCards: [
      [
        "Browser Settings",
        "Use your browser controls to delete, block, or limit cookies.",
      ],
      [
        "Device Settings",
        "Some devices provide additional privacy, tracking, or storage controls.",
      ],
      [
        "Session Impact",
        "Disabling cookies may log you out or prevent secure sessions from working.",
      ],
      [
        "Feature Impact",
        "Some Runexa features may be unavailable or unreliable without required cookies.",
      ],
    ],

    doNotTrackTitle: "Do Not Track signals",
    doNotTrackText:
      "Some browsers offer “Do Not Track” or similar signals. Because there is no universally accepted standard for these signals, Runexa may not respond to all such requests. Users can still manage cookies using browser or device settings.",

    relationTitle: "Relationship with other policies",
    relationSubtitle:
      "This Cookie Policy should be read together with Runexa’s broader trust and legal pages.",
    relationCards: [
      [
        "Privacy Policy",
        "Explains personal information, uploaded content, retention, deletion, rights, and model-training position.",
        "/privacy",
      ],
      [
        "Security",
        "Explains safeguards, infrastructure, access controls, monitoring, and platform protection.",
        "/security",
      ],
      [
        "AI Disclaimer",
        "Explains AI limitations, human review, no professional advice, and responsible use.",
        "/legal/ai-disclaimer",
      ],
      [
        "Terms of Service",
        "Explains account rules, platform use, billing, ownership, and service conditions.",
        "/terms",
      ],
    ],

    updatesTitle: "Policy updates",
    updatesText:
      "Runexa Systems LLC may update this Cookie Policy from time to time. Updated versions will be posted on this page with a revised “Last updated” date.",

    contactTitle: "Contact",
    contactText:
      "Questions about this Cookie Policy may be sent to contact@runexa.ai.",
  },

  fr: {
    title: "Politique relative aux cookies",
    updated: "Dernière mise à jour : juin 2026",
    eyebrow: "Cookies & préférences de plateforme",
    heroTitle: "Une utilisation claire et pratique des cookies.",
    heroText:
      "Cette Politique relative aux cookies explique comment Runexa Systems LLC utilise les cookies et technologies similaires pour exploiter la plateforme, sécuriser les sessions, mémoriser les préférences, comprendre la fiabilité et améliorer l’expérience utilisateur.",
    primaryCta: "Contacter Runexa",
    secondaryCta: "Voir la confidentialité",

    overviewTitle: "Comment Runexa utilise les cookies",
    overviewText:
      "Les cookies sont de petits fichiers ou technologies similaires du navigateur qui aident les sites et applications à fonctionner correctement. Runexa utilise les cookies pour les fonctions essentielles de la plateforme, la sécurité, l’authentification, les préférences linguistiques, la gestion des sessions, la fiabilité et des analyses limitées lorsque cela est applicable.",

    typesTitle: "Catégories de cookies",
    typesSubtitle:
      "Runexa utilise des cookies et technologies similaires pour des objectifs opérationnels précis.",
    cookieTypes: [
      [
        "Cookies essentiels",
        "Nécessaires pour la connexion, l’authentification, l’accès au compte, la gestion des sessions, le routage et les fonctionnalités principales.",
      ],
      [
        "Cookies de sécurité",
        "Utilisés pour aider à détecter les abus, protéger les sessions, réduire la fraude, soutenir la limitation de débit et maintenir l’intégrité de la plateforme.",
      ],
      [
        "Cookies de préférences",
        "Utilisés pour mémoriser des choix comme la langue, les paramètres d’interface et les préférences liées à la session.",
      ],
      [
        "Cookies de performance et fiabilité",
        "Utilisés pour comprendre les erreurs, problèmes de chargement, disponibilité du service et fiabilité générale de la plateforme.",
      ],
      [
        "Cookies d’analyse",
        "Peuvent être utilisés pour comprendre des tendances d’utilisation agrégées et améliorer l’expérience utilisateur, lorsque cela est activé et autorisé.",
      ],
      [
        "Cookies de paiement et fournisseurs",
        "Peuvent être placés par des fournisseurs qui soutiennent les paiements, l’authentification, l’hébergement, la sécurité ou d’autres services opérationnels.",
      ],
    ],

    notForTitle: "Ce que les cookies ne font pas",
    notForSubtitle:
      "L’utilisation des cookies par Runexa est conçue pour soutenir le service, non pour élargir l’utilisation des contenus privés importés.",
    notForItems: [
      "Les cookies ne donnent pas à Runexa le droit d’entraîner des modèles IA publics avec les contenus clients importés",
      "Les cookies ne remplacent pas la Politique de confidentialité ni les droits des utilisateurs qui y sont décrits",
      "Les cookies ne sont pas destinés à exposer les fichiers, résultats ou espaces de travail d’un utilisateur à un autre utilisateur",
      "Les cookies ne sont pas utilisés pour publier, vendre ou divulguer publiquement des documents privés importés",
    ],

    thirdPartyTitle: "Technologies tierces",
    thirdPartyText:
      "Certains cookies ou technologies similaires peuvent être définis par des fournisseurs tiers qui aident Runexa à exploiter la plateforme, notamment l’hébergement, l’authentification, l’analyse, la sécurité, le paiement, l’infrastructure ou le support. Ces fournisseurs peuvent traiter des informations techniques limitées selon leurs propres conditions et pratiques de confidentialité.",

    controlsTitle: "Gestion des cookies",
    controlsText:
      "La plupart des navigateurs permettent de bloquer, supprimer ou gérer les cookies via les paramètres du navigateur. Le blocage des cookies essentiels peut empêcher la connexion, l’import de fichiers, les workflows d’analyse, les paiements ou d’autres fonctionnalités principales de fonctionner correctement.",
    controlsCards: [
      [
        "Paramètres du navigateur",
        "Utilisez les contrôles de votre navigateur pour supprimer, bloquer ou limiter les cookies.",
      ],
      [
        "Paramètres de l’appareil",
        "Certains appareils fournissent des contrôles supplémentaires de confidentialité, de suivi ou de stockage.",
      ],
      [
        "Impact sur la session",
        "La désactivation des cookies peut vous déconnecter ou empêcher les sessions sécurisées de fonctionner.",
      ],
      [
        "Impact sur les fonctionnalités",
        "Certaines fonctionnalités Runexa peuvent être indisponibles ou peu fiables sans les cookies requis.",
      ],
    ],

    doNotTrackTitle: "Signaux Do Not Track",
    doNotTrackText:
      "Certains navigateurs proposent des signaux “Do Not Track” ou similaires. Comme il n’existe pas de norme universellement acceptée pour ces signaux, Runexa peut ne pas répondre à toutes ces demandes. Les utilisateurs peuvent toutefois gérer les cookies via les paramètres du navigateur ou de l’appareil.",

    relationTitle: "Lien avec les autres politiques",
    relationSubtitle:
      "Cette Politique relative aux cookies doit être lue avec les autres pages de confiance et pages juridiques de Runexa.",
    relationCards: [
      [
        "Politique de confidentialité",
        "Explique les informations personnelles, contenus importés, conservation, suppression, droits et position sur l’entraînement des modèles.",
        "/privacy",
      ],
      [
        "Sécurité",
        "Explique les garanties, l’infrastructure, les contrôles d’accès, la surveillance et la protection de la plateforme.",
        "/security",
      ],
      [
        "Avertissement IA",
        "Explique les limites de l’IA, la revue humaine, l’absence de conseil professionnel et l’utilisation responsable.",
        "/legal/ai-disclaimer",
      ],
      [
        "Conditions d’utilisation",
        "Explique les règles de compte, l’utilisation de la plateforme, la facturation, la propriété et les conditions du service.",
        "/terms",
      ],
    ],

    updatesTitle: "Mises à jour de la politique",
    updatesText:
      "Runexa Systems LLC peut mettre à jour cette Politique relative aux cookies de temps à autre. Les versions mises à jour seront publiées sur cette page avec une date de “Dernière mise à jour” révisée.",

    contactTitle: "Contact",
    contactText:
      "Les questions concernant cette Politique relative aux cookies peuvent être envoyées à contact@runexa.ai.",
  },

  ar: {
    title: "سياسة ملفات تعريف الارتباط",
    updated: "آخر تحديث: يونيو 2026",
    eyebrow: "ملفات تعريف الارتباط وتفضيلات المنصة",
    heroTitle: "استخدام واضح وعملي لملفات تعريف الارتباط.",
    heroText:
      "تشرح سياسة ملفات تعريف الارتباط هذه كيف تستخدم Runexa Systems LLC ملفات تعريف الارتباط والتقنيات المشابهة لتشغيل المنصة، وتأمين الجلسات، وتذكر التفضيلات، وفهم موثوقية الخدمة، وتحسين تجربة المستخدم.",
    primaryCta: "تواصل مع Runexa",
    secondaryCta: "عرض الخصوصية",

    overviewTitle: "كيف تستخدم Runexa ملفات تعريف الارتباط",
    overviewText:
      "ملفات تعريف الارتباط هي ملفات صغيرة أو تقنيات مشابهة في المتصفح تساعد المواقع والتطبيقات على العمل بشكل صحيح. تستخدم Runexa ملفات تعريف الارتباط للوظائف الأساسية للمنصة، والأمان، والمصادقة، وتفضيلات اللغة، وإدارة الجلسات، والموثوقية، والتحليلات المحدودة عند الاقتضاء.",

    typesTitle: "فئات ملفات تعريف الارتباط",
    typesSubtitle:
      "تستخدم Runexa ملفات تعريف الارتباط والتقنيات المشابهة لأغراض تشغيلية محددة.",
    cookieTypes: [
      [
        "ملفات تعريف ارتباط أساسية",
        "مطلوبة لتسجيل الدخول والمصادقة والوصول إلى الحساب وإدارة الجلسات والتوجيه والوظائف الأساسية للمنصة.",
      ],
      [
        "ملفات تعريف ارتباط أمنية",
        "تُستخدم للمساعدة في اكتشاف الإساءة وحماية الجلسات وتقليل الاحتيال ودعم حدود الاستخدام والحفاظ على سلامة المنصة.",
      ],
      [
        "ملفات تعريف ارتباط التفضيلات",
        "تُستخدم لتذكر اختيارات مثل اللغة وإعدادات الواجهة والتفضيلات المرتبطة بالجلسة.",
      ],
      [
        "ملفات تعريف ارتباط الأداء والموثوقية",
        "تُستخدم لفهم الأخطاء ومشكلات التحميل وتوفر الخدمة والموثوقية العامة للمنصة.",
      ],
      [
        "ملفات تعريف ارتباط التحليلات",
        "قد تُستخدم لفهم أنماط الاستخدام المجمعة وتحسين تجربة المستخدم، عندما تكون مفعلة ومسموحاً بها.",
      ],
      [
        "ملفات تعريف ارتباط الدفع ومزودي الخدمة",
        "قد يضعها مزودون يدعمون الدفع أو المصادقة أو الاستضافة أو الأمان أو خدمات تشغيلية أخرى.",
      ],
    ],

    notForTitle: "ما لا تُستخدم ملفات تعريف الارتباط من أجله",
    notForSubtitle:
      "تم تصميم استخدام Runexa لملفات تعريف الارتباط لدعم الخدمة، وليس لتوسيع استخدام المحتوى الخاص المرفوع.",
    notForItems: [
      "لا تمنح ملفات تعريف الارتباط Runexa الحق في تدريب نماذج ذكاء اصطناعي عامة على محتوى العملاء المرفوع",
      "ملفات تعريف الارتباط ليست بديلاً عن سياسة الخصوصية أو حقوق المستخدم الموضحة فيها",
      "ليست ملفات تعريف الارتباط مصممة لكشف ملفات أو مخرجات أو مساحة عمل مستخدم لمستخدم آخر",
      "لا تُستخدم ملفات تعريف الارتباط لنشر أو بيع أو الإفصاح العلني عن مستندات خاصة مرفوعة",
    ],

    thirdPartyTitle: "تقنيات الأطراف الثالثة",
    thirdPartyText:
      "قد يتم تعيين بعض ملفات تعريف الارتباط أو التقنيات المشابهة بواسطة مزودين خارجيين يساعدون Runexa في تشغيل المنصة، بما في ذلك الاستضافة والمصادقة والتحليلات والأمان والدفع والبنية التحتية أو الدعم. قد يعالج هؤلاء المزودون معلومات تقنية محدودة وفقاً لشروطهم وممارسات الخصوصية الخاصة بهم.",

    controlsTitle: "إدارة ملفات تعريف الارتباط",
    controlsText:
      "تتيح معظم المتصفحات للمستخدمين حظر ملفات تعريف الارتباط أو حذفها أو إدارتها من خلال إعدادات المتصفح. قد يؤدي حظر ملفات تعريف الارتباط الأساسية إلى منع تسجيل الدخول أو رفع الملفات أو سير عمل التحليل أو عمليات الدفع أو ميزات أساسية أخرى من العمل بشكل صحيح.",
    controlsCards: [
      [
        "إعدادات المتصفح",
        "استخدم عناصر التحكم في المتصفح لحذف ملفات تعريف الارتباط أو حظرها أو تقييدها.",
      ],
      [
        "إعدادات الجهاز",
        "توفر بعض الأجهزة عناصر تحكم إضافية للخصوصية أو التتبع أو التخزين.",
      ],
      [
        "تأثير الجلسة",
        "قد يؤدي تعطيل ملفات تعريف الارتباط إلى تسجيل خروجك أو منع الجلسات الآمنة من العمل.",
      ],
      [
        "تأثير الميزات",
        "قد لا تكون بعض ميزات Runexa متاحة أو موثوقة دون ملفات تعريف الارتباط المطلوبة.",
      ],
    ],

    doNotTrackTitle: "إشارات عدم التتبع",
    doNotTrackText:
      "توفر بعض المتصفحات إشارات “عدم التتبع” أو إشارات مشابهة. ونظراً لعدم وجود معيار مقبول عالمياً لهذه الإشارات، قد لا تستجيب Runexa لجميع هذه الطلبات. يمكن للمستخدمين مع ذلك إدارة ملفات تعريف الارتباط من خلال إعدادات المتصفح أو الجهاز.",

    relationTitle: "العلاقة مع السياسات الأخرى",
    relationSubtitle:
      "ينبغي قراءة سياسة ملفات تعريف الارتباط هذه مع صفحات الثقة والصفحات القانونية الأخرى الخاصة بـ Runexa.",
    relationCards: [
      [
        "سياسة الخصوصية",
        "تشرح المعلومات الشخصية والمحتوى المرفوع والاحتفاظ والحذف والحقوق وموقف تدريب النماذج.",
        "/privacy",
      ],
      [
        "الأمان",
        "يشرح الضمانات والبنية التحتية وضوابط الوصول والمراقبة وحماية المنصة.",
        "/security",
      ],
      [
        "إخلاء مسؤولية الذكاء الاصطناعي",
        "يشرح حدود الذكاء الاصطناعي والمراجعة البشرية وعدم تقديم المشورة المهنية والاستخدام المسؤول.",
        "/legal/ai-disclaimer",
      ],
      [
        "شروط الاستخدام",
        "تشرح قواعد الحساب واستخدام المنصة والفوترة والملكية وشروط الخدمة.",
        "/terms",
      ],
    ],

    updatesTitle: "تحديثات السياسة",
    updatesText:
      "يجوز لـ Runexa Systems LLC تحديث سياسة ملفات تعريف الارتباط هذه من وقت لآخر. سيتم نشر النسخ المحدثة على هذه الصفحة مع تاريخ “آخر تحديث” معدل.",

    contactTitle: "التواصل",
    contactText:
      "يمكن إرسال الأسئلة المتعلقة بسياسة ملفات تعريف الارتباط هذه إلى contact@runexa.ai.",
  },
} satisfies Record<Locale, {
  title: string;
  updated: string;
  eyebrow: string;
  heroTitle: string;
  heroText: string;
  primaryCta: string;
  secondaryCta: string;
  overviewTitle: string;
  overviewText: string;
  typesTitle: string;
  typesSubtitle: string;
  cookieTypes: string[][];
  notForTitle: string;
  notForSubtitle: string;
  notForItems: string[];
  thirdPartyTitle: string;
  thirdPartyText: string;
  controlsTitle: string;
  controlsText: string;
  controlsCards: string[][];
  doNotTrackTitle: string;
  doNotTrackText: string;
  relationTitle: string;
  relationSubtitle: string;
  relationCards: string[][];
  updatesTitle: string;
  updatesText: string;
  contactTitle: string;
  contactText: string;
}>;

export default function CookiePolicyClient({
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

  const t = cookieCopy[locale];

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
                {t.overviewTitle}
              </h2>

              <p className="mt-4 text-sm leading-7 text-slate-300">
                {t.overviewText}
              </p>
            </div>
          </div>
        </section>

        <section className="rounded-[2rem] border border-white/10 bg-white p-8 shadow-xl md:p-10">
          <h2 className="text-2xl font-bold text-slate-950">
            {t.typesTitle}
          </h2>

          <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-600">
            {t.typesSubtitle}
          </p>

          <div className="mt-8 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {t.cookieTypes.map(([title, text]) => (
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
            {t.notForTitle}
          </h2>

          <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-600">
            {t.notForSubtitle}
          </p>

          <div className="mt-6 grid gap-3 md:grid-cols-2">
            {t.notForItems.map((item) => (
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
            {t.thirdPartyTitle}
          </h2>

          <p className="mt-4 max-w-4xl text-slate-600">
            {t.thirdPartyText}
          </p>
        </section>

        <section className="rounded-[2rem] border border-white/10 bg-white p-8 shadow-xl md:p-10">
          <h2 className="text-2xl font-bold text-slate-950">
            {t.controlsTitle}
          </h2>

          <p className="mt-4 max-w-4xl text-slate-600">
            {t.controlsText}
          </p>

          <div className="mt-8 grid gap-4 md:grid-cols-4">
            {t.controlsCards.map(([title, text]) => (
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
            {t.doNotTrackTitle}
          </h2>

          <p className="mt-4 max-w-4xl text-slate-600">
            {t.doNotTrackText}
          </p>
        </section>

        <section className="rounded-[2rem] border border-white/10 bg-white p-8 shadow-xl md:p-10">
          <h2 className="text-2xl font-bold text-slate-950">
            {t.relationTitle}
          </h2>

          <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-600">
            {t.relationSubtitle}
          </p>

          <div className="mt-8 grid gap-4 md:grid-cols-2">
            {t.relationCards.map(([title, text, href]) => (
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
