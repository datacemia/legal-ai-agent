"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getSavedLocale } from "../../lib/i18n";

const translations = {
  en: {
    badge: "Runexa Legal Agent",
    title: "AI Contract Review & Legal Document Analysis",
    subtitle:
      "Runexa helps individuals and professionals analyze contracts, detect risky clauses, understand obligations, and receive practical legal document insights before signing.",
    tryLegalAgent: "Try Legal Agent",
    viewPricing: "View Pricing",

    riskyClause: "Risky clause detection",
    riskyClauseText:
      "Identify clauses that may create legal, financial, or operational risk.",
    obligationExtraction: "Obligation extraction",
    obligationExtractionText:
      "Understand payment terms, deadlines, duties, renewals, and termination rules.",
    executiveSummaries: "Executive summaries",
    executiveSummariesText:
      "Get plain-language summaries of complex contracts and agreements.",
    practicalRecommendations: "Practical recommendations",
    practicalRecommendationsText:
      "Receive suggested next steps and negotiation points before signing.",

    howItWorks: "How Runexa legal AI works",
    steps: [
      "Upload a contract or legal document",
      "Runexa AI analyzes clauses, obligations, and risk signals",
      "Receive a structured legal intelligence report",
    ],

    faqTitle: "Legal AI FAQ",
    faq: [
      [
        "Is Runexa a law firm?",
        "No. Runexa provides informational AI analysis and decision-support output. It does not replace professional legal advice.",
      ],
      [
        "Can AI review contracts?",
        "Runexa can help review contracts by highlighting clauses, obligations, risks, and recommendations for further review.",
      ],
      [
        "What documents can the Legal Agent analyze?",
        "Runexa Legal Agent is designed for contracts and legal agreements such as NDAs, service agreements, employment contracts, and vendor agreements.",
      ],
      [
        "Is legal document processing private?",
        "Runexa is designed as a secure AI workspace for private document analysis and professional workflows.",
      ],
    ],

    jsonDescription:
      "AI contract review and legal document analysis software for risky clause detection, obligation extraction, summaries, and recommendations.",
  },

  fr: {
    badge: "Runexa Legal Agent",
    title: "Analyse de contrats IA et documents juridiques",
    subtitle:
      "Runexa aide les particuliers et professionnels à analyser les contrats, détecter les clauses à risque, comprendre les obligations et obtenir des insights juridiques pratiques avant signature.",
    tryLegalAgent: "Tester l’agent juridique",
    viewPricing: "Voir les tarifs",

    riskyClause: "Détection des clauses à risque",
    riskyClauseText:
      "Identifiez les clauses pouvant créer un risque juridique, financier ou opérationnel.",
    obligationExtraction: "Extraction des obligations",
    obligationExtractionText:
      "Comprenez les conditions de paiement, délais, devoirs, renouvellements et règles de résiliation.",
    executiveSummaries: "Résumés exécutifs",
    executiveSummariesText:
      "Obtenez des résumés clairs en langage simple de contrats et accords complexes.",
    practicalRecommendations: "Recommandations pratiques",
    practicalRecommendationsText:
      "Recevez des prochaines étapes suggérées et des points de négociation avant signature.",

    howItWorks: "Comment fonctionne l’IA juridique Runexa",
    steps: [
      "Téléversez un contrat ou document juridique",
      "Runexa AI analyse les clauses, obligations et signaux de risque",
      "Recevez un rapport d’intelligence juridique structuré",
    ],

    faqTitle: "FAQ IA juridique",
    faq: [
      [
        "Runexa est-il un cabinet d’avocats ?",
        "Non. Runexa fournit une analyse IA informative et une aide à la décision. Il ne remplace pas un conseil juridique professionnel.",
      ],
      [
        "L’IA peut-elle examiner des contrats ?",
        "Runexa peut aider à examiner les contrats en mettant en évidence les clauses, obligations, risques et recommandations à revoir.",
      ],
      [
        "Quels documents l’agent juridique peut-il analyser ?",
        "Runexa Legal Agent est conçu pour les contrats et accords juridiques comme les NDA, contrats de service, contrats de travail et accords fournisseurs.",
      ],
      [
        "Le traitement des documents juridiques est-il privé ?",
        "Runexa est conçu comme un espace IA sécurisé pour l’analyse privée de documents et les workflows professionnels.",
      ],
    ],

    jsonDescription:
      "Logiciel d’analyse de contrats IA et documents juridiques pour détecter les clauses à risque, extraire les obligations, générer des résumés et recommandations.",
  },

  ar: {
    badge: "وكيل Runexa القانوني",
    title: "مراجعة العقود وتحليل المستندات القانونية بالذكاء الاصطناعي",
    subtitle:
      "يساعد Runexa الأفراد والمهنيين على تحليل العقود واكتشاف البنود الخطرة وفهم الالتزامات والحصول على رؤى قانونية عملية قبل التوقيع.",
    tryLegalAgent: "جرّب الوكيل القانوني",
    viewPricing: "عرض الأسعار",

    riskyClause: "اكتشاف البنود الخطرة",
    riskyClauseText:
      "حدد البنود التي قد تخلق مخاطر قانونية أو مالية أو تشغيلية.",
    obligationExtraction: "استخراج الالتزامات",
    obligationExtractionText:
      "افهم شروط الدفع والمواعيد والواجبات والتجديدات وقواعد الإنهاء.",
    executiveSummaries: "ملخصات تنفيذية",
    executiveSummariesText:
      "احصل على ملخصات واضحة بلغة بسيطة للعقود والاتفاقيات المعقدة.",
    practicalRecommendations: "توصيات عملية",
    practicalRecommendationsText:
      "احصل على خطوات مقترحة ونقاط تفاوض قبل التوقيع.",

    howItWorks: "كيف يعمل الذكاء الاصطناعي القانوني في Runexa",
    steps: [
      "ارفع عقدًا أو مستندًا قانونيًا",
      "يحلل Runexa AI البنود والالتزامات وإشارات المخاطر",
      "احصل على تقرير قانوني منظم",
    ],

    faqTitle: "أسئلة شائعة حول الذكاء القانوني",
    faq: [
      [
        "هل Runexa مكتب محاماة؟",
        "لا. يوفر Runexa تحليلاً معلوماتيًا بالذكاء الاصطناعي ومخرجات لدعم القرار، ولا يحل محل الاستشارة القانونية المهنية.",
      ],
      [
        "هل يمكن للذكاء الاصطناعي مراجعة العقود؟",
        "يمكن لـ Runexa المساعدة في مراجعة العقود من خلال إبراز البنود والالتزامات والمخاطر والتوصيات لمراجعتها.",
      ],
      [
        "ما المستندات التي يمكن للوكيل القانوني تحليلها؟",
        "تم تصميم Runexa Legal Agent للعقود والاتفاقيات القانونية مثل اتفاقيات السرية وعقود الخدمة والعمل والموردين.",
      ],
      [
        "هل معالجة المستندات القانونية خاصة؟",
        "تم تصميم Runexa كمساحة عمل آمنة لتحليل المستندات الخاصة والعمليات المهنية.",
      ],
    ],

    jsonDescription:
      "برنامج مراجعة عقود وتحليل مستندات قانونية بالذكاء الاصطناعي لاكتشاف البنود الخطرة واستخراج الالتزامات والملخصات والتوصيات.",
  },
};

type Locale = "en" | "fr" | "ar";

export default function LegalAIClient({
  initialLocale = "en",
  lockInitialLocale = false,
}: {
  initialLocale?: Locale;
  lockInitialLocale?: boolean;
}) {
  const [locale, setLocale] = useState<Locale>(initialLocale);

  useEffect(() => {
    if (lockInitialLocale) {
      setLocale(initialLocale);
      return;
    }

    const saved = getSavedLocale();

    if (saved === "fr" || saved === "ar") {
      setLocale(saved);
    } else {
      setLocale(initialLocale);
    }

    const handleLocaleChange = () => {
      const updated = getSavedLocale();

      if (updated === "fr" || updated === "ar") {
        setLocale(updated);
      } else {
        setLocale(initialLocale);
      }
    };

    window.addEventListener(
      "locale-change",
      handleLocaleChange
    );

    return () => {
      window.removeEventListener(
        "locale-change",
        handleLocaleChange
      );
    };
  }, [initialLocale, lockInitialLocale]);

  const t = translations[locale];

  return (
    <main
      dir={locale === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-6 py-20 text-slate-900"
    >
      <section className="mx-auto max-w-6xl text-center">
        <p className="font-semibold text-blue-600">
          {t.badge}
        </p>

        <h1 className="mt-4 text-5xl font-bold tracking-tight">
          {t.title}
        </h1>

        <p className="mx-auto mt-6 max-w-3xl text-lg text-slate-600">
          {t.subtitle}
        </p>

        <div className="mt-8 flex flex-wrap justify-center gap-3">
          <Link
            href="/upload"
            className="rounded-xl bg-blue-600 px-6 py-3 text-sm font-semibold text-white hover:bg-blue-700"
          >
            {t.tryLegalAgent}
          </Link>

          <Link
            href="/pricing"
            className="rounded-xl border border-slate-200 bg-white px-6 py-3 text-sm font-semibold text-slate-900 hover:bg-slate-50"
          >
            {t.viewPricing}
          </Link>
        </div>
      </section>

      <section className="mx-auto mt-16 grid max-w-6xl gap-6 md:grid-cols-4">
        {[
          [t.riskyClause, t.riskyClauseText],
          [t.obligationExtraction, t.obligationExtractionText],
          [t.executiveSummaries, t.executiveSummariesText],
          [t.practicalRecommendations, t.practicalRecommendationsText],
        ].map(([title, desc]) => (
          <div
            key={title}
            className="rounded-2xl border bg-white p-6 shadow-sm"
          >
            <h2 className="font-bold">
              {title}
            </h2>

            <p className="mt-3 text-sm leading-6 text-slate-600">
              {desc}
            </p>
          </div>
        ))}
      </section>

      <section className="mx-auto mt-16 max-w-6xl rounded-3xl border bg-white p-8 shadow-sm md:p-12">
        <h2 className="text-3xl font-bold">
          {t.howItWorks}
        </h2>

        <div className="mt-8 grid gap-4 md:grid-cols-3">
          {t.steps.map((step, index) => (
            <div
              key={step}
              className="rounded-2xl bg-slate-50 p-6"
            >
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-600 text-sm font-bold text-white">
                {index + 1}
              </div>

              <p className="mt-4 font-semibold">
                {step}
              </p>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto mt-16 max-w-6xl rounded-3xl border bg-white p-8 shadow-sm md:p-12">
        <h2 className="text-3xl font-bold">
          {t.faqTitle}
        </h2>

        <div className="mt-8 grid gap-4 md:grid-cols-2">
          {t.faq.map(([q, a]) => (
            <div
              key={q}
              className="rounded-2xl bg-slate-50 p-6"
            >
              <h3 className="font-bold">
                {q}
              </h3>

              <p className="mt-2 text-sm leading-6 text-slate-600">
                {a}
              </p>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
