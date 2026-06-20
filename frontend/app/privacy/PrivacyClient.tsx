"use client";

import { useEffect, useState } from "react";
import {
  defaultLocale,
  getSavedLocale,
  getTranslations,
} from "../../lib/i18n";

type Locale = "en" | "fr" | "ar";

type PrivacyTranslations = Record<string, string>;

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



const privacyChildrenAndMinorsText = {
  en: {
    title: "12. Children and Minors",
    text1:
      "The Services are not intended for children under the age of 13.",
    text2:
      "Individuals between the ages of 13 and 17 may use the Services only with the consent and supervision of a parent or legal guardian. By allowing a minor to use the Services, the parent or legal guardian represents that they have reviewed and accepted these Terms and the Privacy Policy on the minor’s behalf.",
    text3:
      "We do not knowingly collect personal information from children under 13. If we become aware that we have collected personal information from a child under 13 without appropriate parental consent, we will take reasonable steps to delete such information promptly.",
    text4:
      "Parents or legal guardians who believe that a child has provided us with personal information in violation of this section may contact us to request its deletion.",
  },

  fr: {
    title: "12. Enfants et mineurs",
    text1:
      "Les Services ne sont pas destinés aux enfants de moins de 13 ans.",
    text2:
      "Les personnes âgées de 13 à 17 ans peuvent utiliser les Services uniquement avec le consentement et la supervision d’un parent ou tuteur légal. En autorisant un mineur à utiliser les Services, le parent ou tuteur légal déclare avoir examiné et accepté les présentes Conditions et la Politique de confidentialité au nom du mineur.",
    text3:
      "Nous ne collectons pas sciemment d’informations personnelles auprès d’enfants de moins de 13 ans. Si nous apprenons que nous avons collecté des informations personnelles auprès d’un enfant de moins de 13 ans sans consentement parental approprié, nous prendrons des mesures raisonnables pour supprimer rapidement ces informations.",
    text4:
      "Les parents ou tuteurs légaux qui pensent qu’un enfant nous a fourni des informations personnelles en violation de cette section peuvent nous contacter pour demander leur suppression.",
  },

  ar: {
    title: "12. الأطفال والقاصرون",
    text1:
      "الخدمات غير مخصصة للأطفال دون سن 13 عاماً.",
    text2:
      "يمكن للأفراد الذين تتراوح أعمارهم بين 13 و17 عاماً استخدام الخدمات فقط بموافقة وإشراف أحد الوالدين أو الوصي القانوني. وبالسماح للقاصر باستخدام الخدمات، يقر الوالد أو الوصي القانوني بأنه قد راجع وقبل هذه الشروط وسياسة الخصوصية نيابة عن القاصر.",
    text3:
      "نحن لا نجمع عن علم معلومات شخصية من الأطفال دون سن 13 عاماً. إذا علمنا أننا جمعنا معلومات شخصية من طفل دون سن 13 عاماً دون موافقة أبوية مناسبة، فسنتخذ خطوات معقولة لحذف هذه المعلومات بسرعة.",
    text4:
      "يمكن للوالدين أو الأوصياء القانونيين الذين يعتقدون أن طفلاً قدم لنا معلومات شخصية بالمخالفة لهذا القسم التواصل معنا لطلب حذفها.",
  },
};


const privacyGovernanceText = {
  en: {
    aiTrainingTitle: "15. AI Model Training",
    aiTrainingText:
      "Runexa Systems LLC does not use customer-uploaded documents, contracts, financial records, study materials, business data, or other private content to train public AI models unless explicitly authorized by the user or clearly disclosed where permitted by applicable law.",

    automatedProcessingTitle: "16. Automated Processing",
    automatedProcessingText:
      "Runexa services may use automated systems and AI models to analyze, classify, summarize, extract, transform, and generate information from uploaded content. Users should independently review AI-generated outputs before relying on them.",

    internationalTransfersTitle: "17. International Data Transfers",
    internationalTransfersText:
      "Runexa Systems LLC is a United States company that provides services internationally. If you access the services from outside the United States, your information may be transferred to, stored in, or processed in the United States or other jurisdictions where our service providers operate. Where required, Runexa uses reasonable safeguards designed to protect personal information in accordance with applicable law.",

    enterpriseHandlingTitle: "18. Enterprise Data Handling",
    enterpriseHandlingText:
      "Enterprise customers and organizations may request additional contractual, operational, or security information where available. Organizations remain responsible for assessing their own compliance, governance, security, and regulatory obligations when using Runexa services.",

    deletionRequestsTitle: "19. Deletion Requests",
    deletionRequestsText:
      "Users may contact Runexa to request deletion of personal information or uploaded content, subject to legal, security, billing, fraud-prevention, backup, and operational retention requirements.",
  },

  fr: {
    aiTrainingTitle: "15. Entraînement des modèles IA",
    aiTrainingText:
      "Runexa Systems LLC n’utilise pas les documents téléchargés par les clients, contrats, relevés financiers, supports d’étude, données business ou autres contenus privés pour entraîner des modèles d’IA publics, sauf autorisation explicite de l’utilisateur ou information claire lorsque la loi applicable le permet.",

    automatedProcessingTitle: "16. Traitement automatisé",
    automatedProcessingText:
      "Les services Runexa peuvent utiliser des systèmes automatisés et des modèles d’IA pour analyser, classer, résumer, extraire, transformer et générer des informations à partir du contenu téléchargé. Les utilisateurs doivent vérifier indépendamment les résultats générés par l’IA avant de s’y fier.",

    internationalTransfersTitle: "17. Transferts internationaux de données",
    internationalTransfersText:
      "Runexa Systems LLC est une société américaine qui fournit ses services à l’international. Si vous accédez aux services depuis l’extérieur des États-Unis, vos informations peuvent être transférées, stockées ou traitées aux États-Unis ou dans d’autres juridictions où nos prestataires opèrent. Lorsque cela est requis, Runexa utilise des garanties raisonnables conçues pour protéger les informations personnelles conformément à la loi applicable.",

    enterpriseHandlingTitle: "18. Traitement des données entreprise",
    enterpriseHandlingText:
      "Les clients entreprise et les organisations peuvent demander des informations contractuelles, opérationnelles ou de sécurité supplémentaires lorsqu’elles sont disponibles. Les organisations restent responsables de l’évaluation de leurs propres obligations de conformité, gouvernance, sécurité et réglementation lorsqu’elles utilisent les services Runexa.",

    deletionRequestsTitle: "19. Demandes de suppression",
    deletionRequestsText:
      "Les utilisateurs peuvent contacter Runexa pour demander la suppression de leurs informations personnelles ou contenus téléchargés, sous réserve des obligations légales, de sécurité, de facturation, de prévention de la fraude, de sauvegarde et de conservation opérationnelle.",
  },

  ar: {
    aiTrainingTitle: "15. تدريب نماذج الذكاء الاصطناعي",
    aiTrainingText:
      "لا تستخدم Runexa Systems LLC المستندات التي يرفعها العملاء أو العقود أو السجلات المالية أو مواد الدراسة أو بيانات الأعمال أو أي محتوى خاص آخر لتدريب نماذج ذكاء اصطناعي عامة، ما لم يصرّح المستخدم بذلك صراحةً أو يتم الإفصاح عنه بوضوح عندما يسمح القانون المعمول به.",

    automatedProcessingTitle: "16. المعالجة الآلية",
    automatedProcessingText:
      "قد تستخدم خدمات Runexa أنظمة آلية ونماذج ذكاء اصطناعي لتحليل المحتوى المرفوع وتصنيفه وتلخيصه واستخراج المعلومات منه وتحويله وإنشاء مخرجات بناءً عليه. يجب على المستخدمين مراجعة المخرجات التي يولدها الذكاء الاصطناعي بشكل مستقل قبل الاعتماد عليها.",

    internationalTransfersTitle: "17. نقل البيانات دولياً",
    internationalTransfersText:
      "Runexa Systems LLC شركة أمريكية تقدم خدماتها دولياً. إذا كنت تستخدم الخدمات من خارج الولايات المتحدة، فقد يتم نقل معلوماتك أو تخزينها أو معالجتها في الولايات المتحدة أو في ولايات قضائية أخرى يعمل فيها مزودو الخدمة لدينا. عند الحاجة، تستخدم Runexa ضمانات معقولة مصممة لحماية المعلومات الشخصية وفقاً للقانون المعمول به.",

    enterpriseHandlingTitle: "18. معالجة بيانات المؤسسات",
    enterpriseHandlingText:
      "يمكن لعملاء المؤسسات والمنظمات طلب معلومات تعاقدية أو تشغيلية أو أمنية إضافية عندما تكون متاحة. تبقى المنظمات مسؤولة عن تقييم التزاماتها الخاصة بالامتثال والحوكمة والأمن والمتطلبات التنظيمية عند استخدام خدمات Runexa.",

    deletionRequestsTitle: "19. طلبات الحذف",
    deletionRequestsText:
      "يمكن للمستخدمين التواصل مع Runexa لطلب حذف المعلومات الشخصية أو المحتوى المرفوع، مع مراعاة متطلبات الاحتفاظ القانونية والأمنية والفوترة ومنع الاحتيال والنسخ الاحتياطي والتشغيل.",
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

  const t = getTranslations(locale) as PrivacyTranslations;
  const c = privacyChildrenAndMinorsText[locale] || privacyChildrenAndMinorsText.en;
  const g = privacyGovernanceText[locale] || privacyGovernanceText.en;

  return (
    <main
      dir={locale === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-4 py-12"
    >
      <div className="max-w-3xl mx-auto bg-white p-8 rounded-3xl border shadow-sm space-y-8">

        <div>
          <h1 className="text-3xl font-bold text-slate-900">
            {t.privacyTitle || "Privacy Policy"}
          </h1>

          <p className="text-sm text-slate-500 mt-2">
            {t.privacyUpdated || "Last updated: May 2026"}
          </p>
        </div>

        <section>
          <h2 className="text-xl font-semibold">
            {t.privacyIntroTitle || "1. Introduction"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.privacyIntroText ||
              "Runexa Systems LLC (“we”, “our”, “us”) respects your privacy. This Privacy Policy explains how we collect, use, store, share, and protect information when you use Runexa and its AI-powered services."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.privacyCollectTitle || "2. Information We Collect"}
          </h2>

          <h3 className="mt-4 font-medium">
            {t.privacyAccountTitle || "2.1 Account Information"}
          </h3>

          <p className="text-slate-600 mt-1 break-words whitespace-normal">
            {t.privacyAccountText ||
              "We may collect your email address, encrypted password, account status, billing status, and authentication-related information."}
          </p>

          <h3 className="mt-4 font-medium">
            {t.privacyUploadTitle || "2.2 Uploaded Content"}
          </h3>

          <p className="text-slate-600 mt-1 break-words whitespace-normal">
            {t.privacyUploadText ||
              "We may process documents, files, text, financial information, study materials, business data, and other content you upload for analysis."}
          </p>

          <h3 className="mt-4 font-medium">
            {t.privacyUsageTitle || "2.3 Usage Data"}
          </h3>

          <p className="text-slate-600 mt-1 break-words whitespace-normal">
            {t.privacyUsageText ||
              "We may collect IP address, browser type, device information, pages visited, feature usage, logs, error reports, and security-related data."}
          </p>

          <h3 className="mt-4 font-medium">
            {t.privacyPaymentTitle || "2.4 Payment Information"}
          </h3>

          <p className="text-slate-600 mt-1 break-words whitespace-normal">
            {t.privacyPaymentText ||
              "Payments may be processed by third-party payment providers. We do not store full payment card details on our servers."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.privacyUseTitle || "3. How We Use Your Data"}
          </h2>

          <ul className="mt-2 list-disc pl-5 text-slate-600 space-y-1">
            <li>
              {t.privacyUse1 ||
                "Provide, operate, and maintain the services"}
            </li>

            <li>
              {t.privacyUse2 ||
                "Analyze documents and generate AI-powered outputs"}
            </li>

            <li>
              {t.privacyUse3 ||
                "Manage accounts, credits, payments, and access"}
            </li>

            <li>
              {t.privacyUse4 ||
                "Improve product performance, reliability, and user experience"}
            </li>

            <li>
              {t.privacyUse5 ||
                "Detect abuse, prevent fraud, and protect platform security"}
            </li>

            <li>
              {t.privacyUse6 ||
                "Comply with legal, tax, accounting, and regulatory obligations"}
            </li>
          </ul>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.privacyAiTitle || "4. AI Processing"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.privacyAiText ||
              "Uploaded content may be processed by AI systems and infrastructure providers for extraction, analysis, summarization, classification, and generation of outputs. AI-generated outputs may be inaccurate or incomplete and should be independently verified."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.privacyStorageTitle || "5. Data Storage and Providers"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.privacyStorageText ||
              "Data may be stored and processed using secure third-party infrastructure, hosting, analytics, payment, database, and AI service providers that help us operate the services."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.privacySharingTitle || "6. Data Sharing"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.privacySharingText ||
              "We do not sell your personal information. We may share information only with service providers, payment processors, infrastructure providers, legal authorities when required by law, or in connection with a business transaction such as a merger, acquisition, or asset transfer."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.privacyRetentionTitle || "7. Data Retention"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.privacyRetentionText ||
              "We retain information only as long as reasonably necessary to provide the services, comply with legal obligations, resolve disputes, prevent abuse, and enforce our agreements. You may request deletion of your data, subject to legal and operational retention requirements."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.privacySecurityTitle || "8. Security"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.privacySecurityText ||
              "We implement reasonable technical, administrative, and organizational measures designed to protect your information. However, no method of transmission or storage is completely secure, and we cannot guarantee absolute security."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.privacyInternationalTitle || "9. International Users"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.privacyInternationalText ||
              "If you access the services from outside the United States, your information may be transferred to, stored in, or processed in the United States or other jurisdictions where our service providers operate."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.privacyRightsTitle || "10. Your Rights"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.privacyRightsText ||
              "Depending on your location, you may have rights to access, correct, delete, export, restrict, or object to certain processing of your personal information. You may contact us to exercise these rights."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.privacyCookiesTitle || "11. Cookies"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.privacyCookiesText ||
              "Cookies and similar technologies may be used to maintain sessions, remember preferences, secure accounts, analyze usage, and improve the user experience."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {c.title}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {c.text1}
          </p>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {c.text2}
          </p>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {c.text3}
          </p>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {c.text4}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.privacyChangesTitle || "13. Changes"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {t.privacyChangesText ||
              "We may update this Privacy Policy from time to time. Updated versions will be posted on this page with a revised “Last updated” date."}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {t.privacyContactTitle || "14. Contact"}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            contact@runexa.ai
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {g.aiTrainingTitle}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {g.aiTrainingText}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {g.automatedProcessingTitle}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {g.automatedProcessingText}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {g.internationalTransfersTitle}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {g.internationalTransfersText}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {g.enterpriseHandlingTitle}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {g.enterpriseHandlingText}
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold">
            {g.deletionRequestsTitle}
          </h2>

          <p className="mt-2 text-slate-600 break-words whitespace-normal">
            {g.deletionRequestsText}
          </p>
        </section>

      </div>
    </main>
  );
}
