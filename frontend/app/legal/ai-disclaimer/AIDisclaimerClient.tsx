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

const aiDisclaimerCopy = {
  en: {
    title: "AI Disclaimer & Transparency",
    updated: "Last updated: June 2026",
    eyebrow: "AI transparency",
    heroTitle: "AI can help. Human judgment still matters.",
    heroText:
      "Runexa uses artificial intelligence to assist with document analysis, learning support, financial insights, business intelligence, and decision support. AI-generated outputs are designed to support human review, not replace qualified professionals or independent judgment.",
    primaryCta: "Contact Runexa",
    secondaryCta: "Read Product Terms",
    quickTitle: "Key points",
    quickItems: [
      "Runexa AI outputs are informational and decision-support outputs.",
      "AI may produce inaccurate, incomplete, outdated, or misleading results.",
      "Important outputs should be independently reviewed before use.",
      "Runexa does not provide legal, financial, tax, accounting, medical, investment, or regulated professional advice.",
      "Output quality may depend on document quality, OCR quality, language, missing context, and model limitations.",
      "Users remain responsible for decisions, actions, and interpretations based on AI outputs.",
    ],
    workflowTitle: "How to use Runexa AI responsibly",
    workflowSubtitle:
      "Runexa is most useful when AI analysis is combined with human review and professional judgment where required.",
    workflow: [
      ["1", "Ask", "Choose the agent and submit the document, question, or task."],
      ["2", "Analyze", "Runexa generates structured insights, summaries, classifications, or recommendations."],
      ["3", "Review", "Check the output against the source material and your own context."],
      ["4", "Verify", "Confirm important facts, risks, assumptions, and calculations independently."],
      ["5", "Decide", "Use human judgment or qualified professional advice before important decisions."],
    ],
    sections: [
      {
        title: "1. Purpose of Runexa AI",
        text:
          "Runexa uses artificial intelligence to assist users with document analysis, learning support, financial insights, business intelligence, and decision support. Runexa AI agents help users understand information more efficiently, identify patterns, summarize content, and generate structured insights. AI-generated outputs are intended to support human review and decision-making, not replace it.",
      },
      {
        title: "2. How AI Outputs Are Generated",
        text:
          "Runexa agents use automated systems and artificial intelligence models to process information provided by users and generate outputs such as summaries, classifications, risk assessments, recommendations, explanations, educational content, business insights, and financial observations. Outputs are generated algorithmically and may differ between analyses, even when similar inputs are provided.",
      },
      {
        title: "3. AI Is Not Human Judgment",
        text:
          "Artificial intelligence does not reason, understand context, or exercise judgment in the same way a qualified human professional does. AI systems generate outputs based on patterns and may misinterpret context, miss important information, overlook exceptions, produce incorrect conclusions, or generate misleading recommendations.",
      },
      {
        title: "4. AI Can Make Mistakes",
        text:
          "AI-generated outputs may contain factual inaccuracies, incomplete information, incorrect assumptions, misclassifications, hallucinated content, outdated information, or inconsistent interpretations. No AI-generated output should be considered error-free or guaranteed to be accurate.",
      },
      {
        title: "5. Human Review Is Required",
        text:
          "Users are responsible for reviewing and validating outputs before relying on them. Human review is especially important when dealing with contracts, legal documents, financial decisions, business decisions, compliance matters, educational evaluations, sensitive situations, or other high-impact use cases. Important decisions should never rely exclusively on AI-generated outputs.",
      },
      {
        title: "6. Not Professional Advice",
        text:
          "Runexa provides software tools and AI-generated informational outputs. Runexa does not provide legal advice, financial advice, tax advice, accounting advice, investment advice, medical advice, regulatory advice, security advice, or professional consulting services. Users should consult qualified professionals when professional advice is required.",
      },
      {
        title: "7. Output Quality May Vary",
        text:
          "The quality of AI-generated outputs may depend on document quality, OCR quality, missing information, input accuracy, language complexity, context provided by the user, and limitations of underlying AI models. Results may vary across analyses and over time.",
      },
      {
        title: "8. Responsible Use",
        text:
          "Users remain responsible for reviewing outputs, verifying important facts, evaluating recommendations, complying with applicable laws and regulations, and determining whether outputs are appropriate for their intended use. Runexa should be used as a decision-support tool, not as an autonomous decision-maker.",
      },
      {
        title: "9. Continuous Improvement",
        text:
          "Runexa continuously improves its systems, workflows, prompts, evaluation methods, and AI infrastructure. As a result, platform behavior, feature behavior, analysis methods, and output quality may evolve over time.",
      },
      {
        title: "10. Contact",
        text:
          "For questions regarding AI transparency or this AI Disclaimer, please contact contact@runexa.ai.",
      },
    ],
  },

  fr: {
    title: "Avertissement relatif à l’IA et transparence",
    updated: "Dernière mise à jour : juin 2026",
    eyebrow: "Transparence IA",
    heroTitle: "L’IA peut aider. Le jugement humain reste essentiel.",
    heroText:
      "Runexa utilise l’intelligence artificielle pour assister l’analyse documentaire, l’apprentissage, les insights financiers, la business intelligence et l’aide à la décision. Les résultats générés par l’IA sont conçus pour soutenir la revue humaine, et non pour remplacer des professionnels qualifiés ou le jugement indépendant.",
    primaryCta: "Contacter Runexa",
    secondaryCta: "Lire les conditions du produit",
    quickTitle: "Points clés",
    quickItems: [
      "Les résultats IA de Runexa sont des contenus informatifs et d’aide à la décision.",
      "L’IA peut produire des résultats inexacts, incomplets, obsolètes ou trompeurs.",
      "Les résultats importants doivent être vérifiés indépendamment avant utilisation.",
      "Runexa ne fournit pas de conseil juridique, financier, fiscal, comptable, médical, d’investissement ou autre conseil professionnel réglementé.",
      "La qualité des résultats peut dépendre de la qualité du document, de l’OCR, de la langue, du contexte manquant et des limites du modèle.",
      "Les utilisateurs restent responsables des décisions, actions et interprétations fondées sur les résultats IA.",
    ],
    workflowTitle: "Comment utiliser l’IA Runexa de manière responsable",
    workflowSubtitle:
      "Runexa est le plus utile lorsque l’analyse IA est combinée avec une revue humaine et, si nécessaire, un jugement professionnel.",
    workflow: [
      ["1", "Demander", "Choisissez l’agent et soumettez le document, la question ou la tâche."],
      ["2", "Analyser", "Runexa génère des insights structurés, résumés, classifications ou recommandations."],
      ["3", "Relire", "Comparez le résultat avec le document source et votre propre contexte."],
      ["4", "Vérifier", "Confirmez indépendamment les faits, risques, hypothèses et calculs importants."],
      ["5", "Décider", "Utilisez le jugement humain ou un avis professionnel qualifié avant les décisions importantes."],
    ],
    sections: [
      {
        title: "1. Objectif de l’IA Runexa",
        text:
          "Runexa utilise l’intelligence artificielle pour assister les utilisateurs dans l’analyse documentaire, l’apprentissage, les insights financiers, la business intelligence et l’aide à la décision. Les agents IA Runexa aident les utilisateurs à comprendre l’information plus efficacement, identifier des modèles, résumer du contenu et générer des insights structurés. Les résultats générés par l’IA sont destinés à soutenir la revue humaine et la prise de décision, pas à les remplacer.",
      },
      {
        title: "2. Comment les résultats IA sont générés",
        text:
          "Les agents Runexa utilisent des systèmes automatisés et des modèles d’intelligence artificielle pour traiter les informations fournies par les utilisateurs et générer des résultats tels que des résumés, classifications, évaluations de risques, recommandations, explications, contenus éducatifs, insights business et observations financières. Les résultats sont générés algorithmiquement et peuvent différer entre plusieurs analyses, même lorsque les entrées sont similaires.",
      },
      {
        title: "3. L’IA n’est pas un jugement humain",
        text:
          "L’intelligence artificielle ne raisonne pas, ne comprend pas le contexte et n’exerce pas un jugement comme le ferait un professionnel qualifié. Les systèmes IA génèrent des résultats à partir de modèles et peuvent mal interpréter le contexte, manquer des informations importantes, ignorer des exceptions, produire des conclusions incorrectes ou générer des recommandations trompeuses.",
      },
      {
        title: "4. L’IA peut se tromper",
        text:
          "Les résultats générés par l’IA peuvent contenir des inexactitudes factuelles, des informations incomplètes, des hypothèses incorrectes, des erreurs de classification, du contenu halluciné, des informations obsolètes ou des interprétations incohérentes. Aucun résultat IA ne doit être considéré comme exempt d’erreur ou garanti exact.",
      },
      {
        title: "5. Une revue humaine est nécessaire",
        text:
          "Les utilisateurs sont responsables de relire et valider les résultats avant de s’y fier. La revue humaine est particulièrement importante pour les contrats, documents juridiques, décisions financières, décisions business, sujets de conformité, évaluations éducatives, situations sensibles ou autres cas à impact élevé. Les décisions importantes ne doivent jamais reposer exclusivement sur des résultats générés par l’IA.",
      },
      {
        title: "6. Pas de conseil professionnel",
        text:
          "Runexa fournit des outils logiciels et des résultats informatifs générés par IA. Runexa ne fournit pas de conseil juridique, financier, fiscal, comptable, d’investissement, médical, réglementaire, de sécurité ou de services de conseil professionnel. Les utilisateurs doivent consulter des professionnels qualifiés lorsqu’un avis professionnel est nécessaire.",
      },
      {
        title: "7. La qualité des résultats peut varier",
        text:
          "La qualité des résultats générés par l’IA peut dépendre de la qualité du document, de la qualité de l’OCR, des informations manquantes, de l’exactitude des entrées, de la complexité linguistique, du contexte fourni par l’utilisateur et des limites des modèles IA sous-jacents. Les résultats peuvent varier selon les analyses et évoluer avec le temps.",
      },
      {
        title: "8. Utilisation responsable",
        text:
          "Les utilisateurs restent responsables de la revue des résultats, de la vérification des faits importants, de l’évaluation des recommandations, du respect des lois et réglementations applicables, et de la décision de savoir si les résultats conviennent à l’usage prévu. Runexa doit être utilisé comme un outil d’aide à la décision, pas comme un décideur autonome.",
      },
      {
        title: "9. Amélioration continue",
        text:
          "Runexa améliore continuellement ses systèmes, workflows, prompts, méthodes d’évaluation et infrastructure IA. Par conséquent, le comportement de la plateforme, les fonctionnalités, les méthodes d’analyse et la qualité des résultats peuvent évoluer avec le temps.",
      },
      {
        title: "10. Contact",
        text:
          "Pour toute question concernant la transparence IA ou cet avertissement relatif à l’IA, veuillez contacter contact@runexa.ai.",
      },
    ],
  },

  ar: {
    title: "إخلاء مسؤولية الذكاء الاصطناعي والشفافية",
    updated: "آخر تحديث: يونيو 2026",
    eyebrow: "شفافية الذكاء الاصطناعي",
    heroTitle: "يمكن للذكاء الاصطناعي أن يساعد. لكن الحكم البشري يبقى ضرورياً.",
    heroText:
      "تستخدم Runexa الذكاء الاصطناعي للمساعدة في تحليل المستندات ودعم التعلم والرؤى المالية وذكاء الأعمال ودعم اتخاذ القرار. صُممت المخرجات التي يولدها الذكاء الاصطناعي لدعم المراجعة البشرية، وليس لاستبدال المهنيين المؤهلين أو الحكم المستقل.",
    primaryCta: "تواصل مع Runexa",
    secondaryCta: "قراءة شروط المنتج",
    quickTitle: "نقاط أساسية",
    quickItems: [
      "مخرجات Runexa IA هي مخرجات معلوماتية وداعمة لاتخاذ القرار.",
      "قد ينتج الذكاء الاصطناعي نتائج غير دقيقة أو غير مكتملة أو قديمة أو مضللة.",
      "يجب مراجعة النتائج المهمة بشكل مستقل قبل استخدامها.",
      "لا تقدم Runexa مشورة قانونية أو مالية أو ضريبية أو محاسبية أو طبية أو استثمارية أو أي مشورة مهنية منظمة.",
      "قد تعتمد جودة المخرجات على جودة المستند وجودة OCR واللغة والسياق الناقص وحدود النموذج.",
      "يبقى المستخدمون مسؤولين عن القرارات والإجراءات والتفسيرات المبنية على مخرجات الذكاء الاصطناعي.",
    ],
    workflowTitle: "كيفية استخدام ذكاء Runexa الاصطناعي بمسؤولية",
    workflowSubtitle:
      "تكون Runexa أكثر فائدة عندما يتم الجمع بين تحليل الذكاء الاصطناعي والمراجعة البشرية والحكم المهني عند الحاجة.",
    workflow: [
      ["1", "اطلب", "اختر الوكيل وأرسل المستند أو السؤال أو المهمة."],
      ["2", "حلّل", "تنشئ Runexa رؤى منظمة أو ملخصات أو تصنيفات أو توصيات."],
      ["3", "راجع", "قارن النتيجة بالمصدر والسياق الخاص بك."],
      ["4", "تحقق", "أكد الحقائق والمخاطر والافتراضات والحسابات المهمة بشكل مستقل."],
      ["5", "قرّر", "استخدم الحكم البشري أو رأي مهني مؤهل قبل القرارات المهمة."],
    ],
    sections: [
      {
        title: "1. هدف ذكاء Runexa الاصطناعي",
        text:
          "تستخدم Runexa الذكاء الاصطناعي لمساعدة المستخدمين في تحليل المستندات ودعم التعلم والرؤى المالية وذكاء الأعمال ودعم اتخاذ القرار. تساعد وكلاء Runexa IA المستخدمين على فهم المعلومات بكفاءة أكبر، واكتشاف الأنماط، وتلخيص المحتوى، وإنشاء رؤى منظمة. تهدف مخرجات الذكاء الاصطناعي إلى دعم المراجعة البشرية واتخاذ القرار، وليس استبدالهما.",
      },
      {
        title: "2. كيف يتم إنشاء مخرجات الذكاء الاصطناعي",
        text:
          "تستخدم وكلاء Runexa أنظمة آلية ونماذج ذكاء اصطناعي لمعالجة المعلومات التي يقدمها المستخدمون وإنشاء مخرجات مثل الملخصات والتصنيفات وتقييمات المخاطر والتوصيات والشروحات والمحتوى التعليمي ورؤى الأعمال والملاحظات المالية. يتم إنشاء المخرجات بطريقة خوارزمية وقد تختلف بين التحليلات حتى عند تقديم مدخلات متشابهة.",
      },
      {
        title: "3. الذكاء الاصطناعي ليس حكماً بشرياً",
        text:
          "لا يفكر الذكاء الاصطناعي ولا يفهم السياق ولا يمارس الحكم بالطريقة نفسها التي يفعلها مهني مؤهل. تولد أنظمة الذكاء الاصطناعي مخرجات بناءً على أنماط، وقد تسيء تفسير السياق أو تفوت معلومات مهمة أو تتجاهل استثناءات أو تنتج استنتاجات غير صحيحة أو توصيات مضللة.",
      },
      {
        title: "4. يمكن للذكاء الاصطناعي أن يخطئ",
        text:
          "قد تحتوي مخرجات الذكاء الاصطناعي على أخطاء واقعية أو معلومات غير مكتملة أو افتراضات غير صحيحة أو تصنيفات خاطئة أو محتوى مولد غير دقيق أو معلومات قديمة أو تفسيرات غير متسقة. لا ينبغي اعتبار أي مخرج من الذكاء الاصطناعي خالياً من الخطأ أو مضمون الدقة.",
      },
      {
        title: "5. المراجعة البشرية مطلوبة",
        text:
          "يتحمل المستخدمون مسؤولية مراجعة المخرجات والتحقق منها قبل الاعتماد عليها. تكون المراجعة البشرية مهمة بشكل خاص عند التعامل مع العقود والمستندات القانونية والقرارات المالية وقرارات الأعمال ومسائل الامتثال والتقييمات التعليمية والحالات الحساسة أو الاستخدامات عالية التأثير. يجب ألا تعتمد القرارات المهمة حصراً على مخرجات الذكاء الاصطناعي.",
      },
      {
        title: "6. ليست مشورة مهنية",
        text:
          "توفر Runexa أدوات برمجية ومخرجات معلوماتية مولدة بالذكاء الاصطناعي. لا تقدم Runexa مشورة قانونية أو مالية أو ضريبية أو محاسبية أو استثمارية أو طبية أو تنظيمية أو أمنية أو خدمات استشارية مهنية. يجب على المستخدمين استشارة مهنيين مؤهلين عندما تكون المشورة المهنية مطلوبة.",
      },
      {
        title: "7. قد تختلف جودة المخرجات",
        text:
          "قد تعتمد جودة المخرجات التي يولدها الذكاء الاصطناعي على جودة المستند، وجودة OCR، والمعلومات الناقصة، ودقة المدخلات، وتعقيد اللغة، والسياق الذي يقدمه المستخدم، وحدود نماذج الذكاء الاصطناعي الأساسية. قد تختلف النتائج بين التحليلات ومع مرور الوقت.",
      },
      {
        title: "8. الاستخدام المسؤول",
        text:
          "يبقى المستخدمون مسؤولين عن مراجعة المخرجات، والتحقق من الحقائق المهمة، وتقييم التوصيات، والامتثال للقوانين واللوائح المعمول بها، وتحديد ما إذا كانت المخرجات مناسبة للاستخدام المقصود. يجب استخدام Runexa كأداة لدعم القرار، وليس كصانع قرار مستقل.",
      },
      {
        title: "9. التحسين المستمر",
        text:
          "تعمل Runexa باستمرار على تحسين أنظمتها وسير العمل والتعليمات وطرق التقييم والبنية التحتية للذكاء الاصطناعي. ونتيجة لذلك، قد يتطور سلوك المنصة والميزات وطرق التحليل وجودة المخرجات بمرور الوقت.",
      },
      {
        title: "10. التواصل",
        text:
          "لأي أسئلة بخصوص شفافية الذكاء الاصطناعي أو إخلاء المسؤولية هذا، يرجى التواصل عبر contact@runexa.ai.",
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
  workflowTitle: string;
  workflowSubtitle: string;
  workflow: string[][];
  sections: { title: string; text: string }[];
}>;

export default function AIDisclaimerClient({
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

  const t = aiDisclaimerCopy[locale];

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
                  href="/product-terms"
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
            {t.workflowTitle}
          </h2>

          <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-600">
            {t.workflowSubtitle}
          </p>

          <div className="mt-8 grid gap-4 md:grid-cols-5">
            {t.workflow.map(([number, title, text]) => (
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
