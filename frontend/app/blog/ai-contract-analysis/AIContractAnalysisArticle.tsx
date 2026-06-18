"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getSavedLocale } from "../../../lib/i18n";


const translations = {
  en: {
    back: "← Back to Blog",

    category: "Legal Intelligence",

    title:
      "AI Contract Analysis: How AI Helps Review Legal Documents",

    intro:
      "Contract review is a critical part of legal, commercial, and professional decision-making. AI-powered contract analysis helps organizations review documents faster, identify potential risks, understand obligations, and improve decision-making before signing.",

    whatIs:
      "What is AI contract analysis?",

    whatIsText:
      "AI contract analysis uses artificial intelligence to review legal documents, extract key information, summarize obligations, identify sensitive clauses, and generate structured insights. It is designed to support legal workflows, not replace qualified legal professionals.",

    why:
      "Why contract review is challenging",

    whyText:
      "Contracts often contain complex legal language, cross-references, deadlines, liability provisions, termination rights, confidentiality obligations, payment terms, and dispute resolution clauses. Overlooking a single provision can create legal, financial, or operational risk.",

    common:
      "Common contract types AI can review",

    commonText:
      "AI contract analysis can support a wide range of legal workflows, including service agreements, NDAs, vendor contracts, employment agreements, consulting agreements, partnership agreements, lease agreements, and procurement contracts.",

    runexa:
      "How Runexa Legal Agent helps",

    runexaText:
      "Runexa Legal Agent enables users to upload legal documents, identify potential risks, understand obligations, review recommendations, and generate structured legal intelligence reports for decision support.",

    support:
      "AI should support legal review, not replace legal judgment",

    supportText:
      "AI can make contract review faster and easier to understand, but important legal decisions should always be reviewed by qualified legal professionals. The strongest use of AI is to improve preparation, visibility, and awareness before final decisions are made.",

    ctaTitle:
      "Review contracts with AI before signing",

    ctaText:
      "Use Runexa Legal Agent to analyze risks, obligations, key clauses, and recommendations across legal documents.",

    ctaButton:
      "Upload Contract",

    riskDetection:
      "Risk detection",

    riskDetectionText:
      "AI can identify clauses related to liability, termination rights, payment obligations, indemnification, and confidentiality requirements.",

    obligationSummaries:
      "Obligation summaries",

    obligationSummariesText:
      "AI can summarize deadlines, responsibilities, renewal provisions, payment commitments, and notice requirements in clear language.",

    negotiationSupport:
      "Negotiation support",

    negotiationSupportText:
      "AI can highlight areas that may require further review, including unclear obligations, unusual provisions, or one-sided contractual terms.",

    executiveSummaries:
      "Executive summaries",

    executiveSummariesText:
      "AI can transform lengthy contracts into structured summaries for executives, founders, legal teams, consultants, and decision-makers.",
  },
  fr: {
    back: "← Retour au blog",

    category: "Intelligence juridique",

    title:
      "Analyse de contrats par IA : comment l’IA aide à examiner les documents juridiques",

    intro:
      "L’examen des contrats est une étape essentielle de la prise de décision juridique, commerciale et professionnelle. L’analyse de contrats par IA aide les organisations à examiner les documents plus rapidement, à identifier les risques potentiels, à comprendre les obligations et à prendre des décisions plus éclairées avant la signature.",

    whatIs:
      "Qu’est-ce que l’analyse de contrats par IA ?",

    whatIsText:
      "L’analyse de contrats par IA utilise l’intelligence artificielle pour examiner les documents juridiques, extraire les informations clés, résumer les obligations, identifier les clauses sensibles et générer des insights structurés. Elle est conçue pour assister les workflows juridiques, et non pour remplacer les professionnels du droit.",

    why:
      "Pourquoi l’examen des contrats est complexe",

    whyText:
      "Les contrats contiennent souvent un langage juridique complexe, des renvois internes, des échéances, des clauses de responsabilité, des droits de résiliation, des obligations de confidentialité, des conditions de paiement et des mécanismes de résolution des litiges. Négliger une seule disposition peut entraîner des risques juridiques, financiers ou opérationnels.",

    common:
      "Types de contrats que l’IA peut analyser",

    commonText:
      "L’analyse de contrats par IA peut prendre en charge de nombreux workflows juridiques, notamment les contrats de services, accords de confidentialité (NDA), contrats fournisseurs, contrats de travail, contrats de conseil, accords de partenariat, baux et contrats d’approvisionnement.",

    runexa:
      "Comment Runexa Legal Agent aide",

    runexaText:
      "Runexa Legal Agent permet aux utilisateurs de téléverser des documents juridiques, d’identifier les risques potentiels, de comprendre leurs obligations, d’examiner des recommandations et de générer des rapports d’intelligence juridique structurés destinés à l’aide à la décision.",

    support:
      "L’IA doit soutenir l’analyse juridique, pas remplacer le jugement juridique",

    supportText:
      "L’IA peut rendre l’examen des contrats plus rapide et plus accessible, mais les décisions juridiques importantes doivent toujours être examinées par des professionnels qualifiés. Son utilisation la plus efficace consiste à améliorer la préparation, la visibilité et la compréhension avant toute décision finale.",

    ctaTitle:
      "Analysez vos contrats avec l’IA avant de signer",

    ctaText:
      "Utilisez Runexa Legal Agent pour analyser les risques, les obligations, les clauses clés et les recommandations dans vos documents juridiques.",

    ctaButton:
      "Téléverser un contrat",

    riskDetection:
      "Détection des risques",

    riskDetectionText:
      "L’IA peut identifier les clauses liées à la responsabilité, aux droits de résiliation, aux obligations de paiement, aux indemnisations et aux exigences de confidentialité.",

    obligationSummaries:
      "Synthèse des obligations",

    obligationSummariesText:
      "L’IA peut résumer les échéances, responsabilités, conditions de renouvellement, engagements financiers et obligations de notification dans un langage clair.",

    negotiationSupport:
      "Aide à la négociation",

    negotiationSupportText:
      "L’IA peut mettre en évidence les points nécessitant une attention particulière, notamment les obligations ambiguës, les clauses inhabituelles ou les dispositions contractuelles déséquilibrées.",

    executiveSummaries:
      "Résumés exécutifs",

    executiveSummariesText:
      "L’IA peut transformer des contrats volumineux en synthèses structurées destinées aux dirigeants, équipes juridiques, consultants et décideurs.",
  },

  ar: {
    back: "← العودة إلى المدونة",

    category: "الذكاء القانوني",

    title:
      "تحليل العقود بالذكاء الاصطناعي: كيف يساعد الذكاء الاصطناعي في مراجعة المستندات القانونية",

    intro:
      "تُعد مراجعة العقود جزءاً أساسياً من اتخاذ القرارات القانونية والتجارية والمهنية. يساعد تحليل العقود المدعوم بالذكاء الاصطناعي المؤسسات على مراجعة المستندات بسرعة أكبر، وتحديد المخاطر المحتملة، وفهم الالتزامات، واتخاذ قرارات أكثر وعياً قبل التوقيع.",

    whatIs:
      "ما هو تحليل العقود بالذكاء الاصطناعي؟",

    whatIsText:
      "يستخدم تحليل العقود بالذكاء الاصطناعي تقنيات الذكاء الاصطناعي لمراجعة المستندات القانونية واستخراج المعلومات الأساسية وتلخيص الالتزامات وتحديد البنود الحساسة وإنشاء رؤى قانونية منظمة. وقد صُمم لدعم سير العمل القانوني وليس لاستبدال المتخصصين القانونيين المؤهلين.",

    why:
      "لماذا تُعد مراجعة العقود معقدة؟",

    whyText:
      "غالباً ما تحتوي العقود على لغة قانونية معقدة وإحالات داخلية ومواعيد نهائية وبنود مسؤولية وحقوق إنهاء والتزامات سرية وشروط دفع وآليات لتسوية النزاعات. وقد يؤدي تجاهل بند واحد فقط إلى مخاطر قانونية أو مالية أو تشغيلية.",

    common:
      "أنواع العقود التي يمكن للذكاء الاصطناعي تحليلها",

    commonText:
      "يمكن لتحليل العقود بالذكاء الاصطناعي دعم مجموعة واسعة من سير العمل القانوني، بما في ذلك عقود الخدمات، واتفاقيات عدم الإفصاح (NDA)، وعقود الموردين، وعقود العمل، وعقود الاستشارات، واتفاقيات الشراكة، وعقود الإيجار، وعقود المشتريات.",

    runexa:
      "كيف يساعد Runexa Legal Agent",

    runexaText:
      "يُمكّن Runexa Legal Agent المستخدمين من رفع المستندات القانونية وتحديد المخاطر المحتملة وفهم الالتزامات ومراجعة التوصيات وإنشاء تقارير ذكاء قانوني منظمة لدعم اتخاذ القرار.",

    support:
      "يجب أن يدعم الذكاء الاصطناعي المراجعة القانونية لا أن يحل محل الحكم القانوني",

    supportText:
      "يمكن للذكاء الاصطناعي أن يجعل مراجعة العقود أسرع وأسهل فهماً، لكن القرارات القانونية المهمة يجب دائماً أن تُراجع من قبل متخصصين قانونيين مؤهلين. وتتمثل أفضل استخداماته في تحسين الاستعداد والوضوح والوعي قبل اتخاذ القرارات النهائية.",

    ctaTitle:
      "راجع العقود بالذكاء الاصطناعي قبل التوقيع",

    ctaText:
      "استخدم Runexa Legal Agent لتحليل المخاطر والالتزامات والبنود الرئيسية والتوصيات في المستندات القانونية.",

    ctaButton:
      "رفع عقد",

    riskDetection:
      "اكتشاف المخاطر",

    riskDetectionText:
      "يمكن للذكاء الاصطناعي تحديد البنود المتعلقة بالمسؤولية وحقوق الإنهاء والتزامات الدفع والتعويضات ومتطلبات السرية.",

    obligationSummaries:
      "ملخص الالتزامات",

    obligationSummariesText:
      "يمكن للذكاء الاصطناعي تلخيص المواعيد النهائية والمسؤوليات وشروط التجديد والالتزامات المالية ومتطلبات الإشعار بلغة واضحة.",

    negotiationSupport:
      "دعم التفاوض",

    negotiationSupportText:
      "يمكن للذكاء الاصطناعي إبراز النقاط التي قد تتطلب مراجعة إضافية، بما في ذلك الالتزامات غير الواضحة أو البنود غير المعتادة أو الشروط التعاقدية غير المتوازنة.",

    executiveSummaries:
      "الملخصات التنفيذية",

    executiveSummariesText:
      "يمكن للذكاء الاصطناعي تحويل العقود الطويلة إلى ملخصات منظمة موجهة للمديرين التنفيذيين والفرق القانونية والاستشاريين وصناع القرار.",
  },
};


type Locale = "en" | "fr" | "ar";

export default function AIContractAnalysisArticle({
  initialLocale = "en",
  lockInitialLocale = false,
}: {
  initialLocale?: Locale;
  lockInitialLocale?: boolean;
}) {
  const [locale, setLocale] =
    useState<Locale>(initialLocale);

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
      <article className="mx-auto max-w-4xl">
        <Link href="/blog" className="text-sm font-semibold text-blue-600">
          {t.back}
        </Link>

        <p className="mt-8 text-sm font-semibold uppercase tracking-wide text-blue-600">
          {t.category}
        </p>

        <h1 className="mt-4 text-5xl font-bold tracking-tight">
          {t.title}
        </h1>

        <p className="mt-6 text-lg leading-8 text-slate-600">
          {t.intro}
        </p>

        <div className="mt-10 rounded-3xl border bg-white p-8 shadow-sm">
          <h2 className="text-2xl font-bold">
            {t.whatIs}
          </h2>

          <p className="mt-4 leading-8 text-slate-600">
            {t.whatIsText}
          </p>
        </div>

        <section className="mt-10 space-y-8">
          <div>
            <h2 className="text-3xl font-bold">
              {t.why}
            </h2>

            <p className="mt-4 leading-8 text-slate-600">
              {t.whyText}
            </p>
          </div>

          <div className="grid gap-6 md:grid-cols-2">
            {[
              [
                t.riskDetection,
                t.riskDetectionText,
              ],
              [
                t.obligationSummaries,
                t.obligationSummariesText,
              ],
              [
                t.negotiationSupport,
                t.negotiationSupportText,
              ],
              [
                t.executiveSummaries,
                t.executiveSummariesText,
              ],
            ].map(([title, text]) => (
              <div
                key={title}
                className="rounded-2xl border bg-white p-6 shadow-sm"
              >
                <h3 className="font-bold">{title}</h3>

                <p className="mt-3 text-sm leading-6 text-slate-600">
                  {text}
                </p>
              </div>
            ))}
          </div>

          <div>
            <h2 className="text-3xl font-bold">
              {t.common}
            </h2>

            <p className="mt-4 leading-8 text-slate-600">
              {t.commonText}
            </p>
          </div>

          <div className="rounded-3xl border bg-white p-8 shadow-sm">
            <h2 className="text-2xl font-bold">
              {t.runexa}
            </h2>

            <p className="mt-4 leading-8 text-slate-600">
              {t.runexaText}
            </p>

            <div className="mt-6 grid gap-3 sm:grid-cols-2">
              {[
                locale === "fr" ? "Vue globale des risques" : locale === "ar" ? "نظرة عامة على المخاطر" : "Risk score overview",
                locale === "fr" ? "Analyse des clauses sensibles" : locale === "ar" ? "تحليل البنود الحساسة" : "Sensitive clause analysis",
                locale === "fr" ? "Résumé du contrat" : locale === "ar" ? "ملخص العقد" : "Contract summary",
                locale === "fr" ? "Extraction des obligations" : locale === "ar" ? "استخراج الالتزامات" : "Obligation extraction",
                locale === "fr" ? "Recommandations de négociation" : locale === "ar" ? "توصيات التفاوض" : "Negotiation recommendations",
                locale === "fr" ? "Rapport juridique IA structuré" : locale === "ar" ? "تقرير قانوني منظم بالذكاء الاصطناعي" : "Structured AI legal report",
              ].map((item) => (
                <div
                  key={item}
                  className="rounded-xl bg-slate-50 px-4 py-3 text-sm font-semibold text-slate-700"
                >
                  {item}
                </div>
              ))}
            </div>
          </div>

          <div>
            <h2 className="text-3xl font-bold">
              {t.support}
            </h2>

            <p className="mt-4 leading-8 text-slate-600">
              {t.supportText}
            </p>
          </div>
        </section>

        <section className="mt-12 rounded-3xl bg-blue-600 p-8 text-white">
          <h2 className="text-3xl font-bold">
            {t.ctaTitle}
          </h2>

          <p className="mt-4 text-blue-100">
            {t.ctaText}
          </p>

          <Link
            href="/upload"
            className="mt-6 inline-block rounded-xl bg-white px-6 py-3 text-sm font-semibold text-blue-600"
          >
            {t.ctaButton}
          </Link>
        </section>

        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "Article",
              mainEntityOfPage: {
                "@type": "WebPage",
                "@id":
                  "https://runexa.ai/blog/ai-contract-analysis",
              },
              headline:
                t.title,
              description:
                "Learn how AI contract analysis helps identify risky clauses, summarize obligations, and support legal document review workflows.",
              datePublished: "2026-05-24",
              dateModified: "2026-05-24",
              author: {
                "@type": "Person",
                name: "Dr. Rachid Ejjami",
              },
              publisher: {
                "@type": "Organization",
                name: "Runexa Systems",
              },
            }),
          }}
        />
      </article>
    </main>
  );
}