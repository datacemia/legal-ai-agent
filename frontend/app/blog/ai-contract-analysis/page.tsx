"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getSavedLocale } from "../../../lib/i18n";


const translations = {
  en: {
    back: "{t.back}",
    category: "{t.category}",
    title:
      "{t.title}",
    intro:
      "Contract review is one of the most important workflows in legal, business, and professional decision-making. AI contract analysis can help users review legal documents faster, identify risky clauses, and understand obligations before signing.",

    whatIs: "{t.whatIs}",
    whatIsText:
      "AI contract analysis uses artificial intelligence to read legal documents, extract key information, summarize obligations, highlight sensitive clauses, and generate practical recommendations. It is designed to support legal review workflows, not replace qualified legal professionals.",

    why: "{t.why}",

    whyText:
      "Contracts often contain dense language, legal terminology, cross-references, deadlines, liability terms, termination clauses, confidentiality obligations, payment rules, and dispute resolution provisions. Missing a single clause can create legal, financial, or operational risk.",

    common:
      "{t.common}",

    commonText:
      "AI contract analysis can support many professional workflows, including service agreements, NDAs, vendor contracts, employment agreements, consulting agreements, partnership documents, lease terms, and procurement documents.",

    runexa: "{t.runexa}",

    runexaText:
      "Runexa Legal Agent helps users upload legal documents, detect risky clauses, understand obligations, review recommendations, and generate structured legal intelligence reports. It is built for informational and decision-support use.",

    support:
      "{t.support}",

    supportText:
      "AI can make contract review faster and easier to understand, but important legal decisions should always be reviewed with qualified professionals. The best use of AI contract analysis is to improve preparation, clarity, and awareness before final decisions.",

    ctaTitle:
      "{t.ctaTitle}",

    ctaText:
      "Use Runexa Legal Agent to analyze risky clauses, obligations, and recommendations in legal documents.",

    ctaButton: "{t.ctaButton}",
  },

  fr: {
    back: "← Retour au blog",
    category: "IA juridique",
    title:
      "Analyse de contrats IA : comment l’IA aide à examiner les documents juridiques",
    intro:
      "La revue de contrats est l’un des workflows les plus importants dans le juridique et le business. L’analyse de contrats IA aide à examiner les documents plus rapidement, détecter les clauses à risque et comprendre les obligations avant signature.",

    whatIs: "Qu’est-ce que l’analyse de contrats IA ?",
    whatIsText:
      "L’analyse de contrats IA utilise l’intelligence artificielle pour lire des documents juridiques, extraire les informations clés, résumer les obligations et mettre en évidence les clauses sensibles.",

    why: "Pourquoi la revue de contrats est difficile",

    whyText:
      "Les contrats contiennent souvent un langage dense, des termes juridiques, des délais, clauses de responsabilité, confidentialité et règles de paiement.",

    common:
      "Types de contrats que l’IA peut aider à analyser",

    commonText:
      "L’IA peut aider à examiner les accords de services, NDA, contrats fournisseurs, contrats de travail et documents de partenariat.",

    runexa:
      "Comment Runexa Legal Agent aide",

    runexaText:
      "Runexa Legal Agent aide les utilisateurs à téléverser des documents juridiques, détecter les clauses à risque et générer des rapports structurés.",

    support:
      "L’IA doit assister les juristes, pas les remplacer",

    supportText:
      "L’IA améliore la rapidité et la compréhension, mais les décisions juridiques importantes doivent être validées par des professionnels qualifiés.",

    ctaTitle:
      "Analysez vos contrats avec l’IA avant signature",

    ctaText:
      "Utilisez Runexa Legal Agent pour analyser les clauses à risque et obligations des documents juridiques.",

    ctaButton: "Téléverser un contrat",
  },

  ar: {
    back: "← العودة إلى المدونة",
    category: "الذكاء القانوني",
    title:
      "تحليل العقود بالذكاء الاصطناعي: كيف يساعد الذكاء الاصطناعي في مراجعة المستندات القانونية",
    intro:
      "تُعد مراجعة العقود من أهم تدفقات العمل القانونية والتجارية. يساعد الذكاء الاصطناعي في تحليل العقود بسرعة أكبر واكتشاف البنود الخطرة وفهم الالتزامات قبل التوقيع.",

    whatIs: "ما هو تحليل العقود بالذكاء الاصطناعي؟",
    whatIsText:
      "يستخدم تحليل العقود بالذكاء الاصطناعي تقنيات الذكاء الاصطناعي لقراءة المستندات القانونية واستخراج المعلومات المهمة وتلخيص الالتزامات.",

    why:
      "لماذا تعتبر مراجعة العقود صعبة",

    whyText:
      "غالبًا ما تحتوي العقود على لغة قانونية معقدة وبنود مسؤولية وسرية ومدفوعات ومواعيد نهائية.",

    common:
      "أنواع العقود التي يمكن للذكاء الاصطناعي مراجعتها",

    commonText:
      "يمكن للذكاء الاصطناعي دعم مراجعة عقود الخدمات واتفاقيات السرية وعقود العمل والشراكات.",

    runexa:
      "كيف يساعد Runexa Legal Agent",

    runexaText:
      "يساعد Runexa Legal Agent المستخدمين على رفع المستندات القانونية واكتشاف البنود الخطرة وإنشاء تقارير قانونية منظمة.",

    support:
      "يجب أن يدعم الذكاء الاصطناعي المراجعة القانونية لا أن يستبدل المحامين",

    supportText:
      "يمكن للذكاء الاصطناعي تسريع مراجعة العقود، لكن القرارات القانونية المهمة يجب مراجعتها من قبل متخصصين مؤهلين.",

    ctaTitle:
      "راجع العقود بالذكاء الاصطناعي قبل التوقيع",

    ctaText:
      "استخدم Runexa Legal Agent لتحليل البنود الخطرة والالتزامات في المستندات القانونية.",

    ctaButton: "رفع عقد",
  },
};


export default function AIContractAnalysisArticle() {
  const [locale, setLocale] =
    useState<"en" | "fr" | "ar">("en");

  useEffect(() => {
    const saved = getSavedLocale();

    if (saved === "fr" || saved === "ar") {
      setLocale(saved);
    }

    const handleLocaleChange = () => {
      const updated = getSavedLocale();

      if (updated === "fr" || updated === "ar") {
        setLocale(updated);
      } else {
        setLocale("en");
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
  }, []);

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
                "Risky clause detection",
                "AI can help flag clauses related to liability, termination, payment, confidentiality, ownership, jurisdiction, or penalties.",
              ],
              [
                "Obligation summaries",
                "AI can summarize deadlines, duties, renewal terms, payment obligations, and notice requirements in plain language.",
              ],
              [
                "Negotiation support",
                "AI can suggest areas to review before signing, such as unclear obligations or one-sided termination rights.",
              ],
              [
                "Executive summaries",
                "AI can turn long contracts into structured summaries for founders, teams, consultants, and professionals.",
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
                "Risk score overview",
                "Sensitive clause analysis",
                "Contract summary",
                "Obligation extraction",
                "Negotiation recommendations",
                "Structured AI legal report",
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
                "{t.title}",
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