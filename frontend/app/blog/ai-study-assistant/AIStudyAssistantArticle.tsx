"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getSavedLocale } from "../../../lib/i18n";



const translations = {
  en: {
    back: "← Back to Blog",

    category: "Learning Intelligence",

    title:
      "AI Study Assistant: Building Smarter Learning Workflows",

    intro:
      "Learning large amounts of information can be difficult, repetitive, and time-consuming. AI study assistants help students and professionals organize knowledge, generate summaries, create quizzes, and build more effective learning workflows.",

    whatIs:
      "What is an AI study assistant?",

    whatIsText:
      "An AI study assistant uses artificial intelligence to analyze learning materials and generate structured educational support such as summaries, flashcards, quizzes, explanations, revision plans, and personalized learning recommendations.",

    why:
      "Why traditional studying can be inefficient",

    whyText:
      "Many learners spend hours manually summarizing documents, organizing notes, rewriting concepts, and preparing revision material. AI can reduce repetitive study tasks and help create clearer learning structures.",

    aiSummaries:
      "AI summaries",

    aiSummariesText:
      "AI can transform long study documents into concise, structured, and easier-to-review summaries.",

    flashcards:
      "Flashcards & quizzes",

    flashcardsText:
      "AI can generate revision exercises automatically to support memory, recall, and concept reinforcement.",

    studyPlanning:
      "Study planning",

    studyPlanningText:
      "AI can help organize learning sessions, revision schedules, priorities, and progress tracking.",

    knowledgeOrganization:
      "Knowledge organization",

    knowledgeOrganizationText:
      "AI can structure complex information into clearer learning paths and more understandable study flows.",

    workflows:
      "AI learning workflows for modern education",

    workflowsText:
      "AI-powered learning systems can support students, professionals, researchers, and organizations by simplifying content review, accelerating knowledge acquisition, and improving educational productivity.",

    runexa:
      "How Runexa Study Agent helps",

    runexaText:
      "Runexa Study Agent helps users upload learning materials and generate AI-powered summaries, quizzes, flashcards, study plans, and structured learning workflows designed to improve productivity and understanding.",

    support:
      "AI should support learning, not replace thinking",

    supportText:
      "The most effective educational AI systems help learners understand concepts more efficiently while keeping human reasoning, critical thinking, and active learning at the center of the process.",

    ctaTitle:
      "Learn more effectively with AI study workflows",

    ctaText:
      "Use Runexa Study Agent to generate summaries, quizzes, flashcards, study plans, and structured learning workflows with AI.",

    ctaButton:
      "Start Studying",

    features: [
      "AI study summaries",
      "Flashcard generation",
      "Quiz generation",
      "Study planning",
      "Learning workflows",
      "Educational productivity tools",
    ],
  },

  fr: {
    back: "← Retour au blog",

    category: "Intelligence pédagogique",

    title:
      "Assistant d’étude par IA : construire des workflows d’apprentissage plus efficaces",

    intro:
      "Assimiler de grandes quantités d’informations peut être complexe, répétitif et chronophage. Les assistants d’étude basés sur l’IA aident les étudiants, professionnels et apprenants à organiser les connaissances, générer des résumés, créer des exercices et structurer des méthodes d’apprentissage plus efficaces.",

    whatIs:
      "Qu’est-ce qu’un assistant d’étude par IA ?",

    whatIsText:
      "Un assistant d’étude par IA utilise l’intelligence artificielle pour analyser des supports pédagogiques et générer un accompagnement structuré sous forme de résumés, flashcards, quiz, explications, plans de révision et recommandations d’apprentissage personnalisées.",

    why:
      "Pourquoi les méthodes d’étude traditionnelles peuvent être inefficaces",

    whyText:
      "De nombreux apprenants passent des heures à résumer des documents, organiser leurs notes, reformuler des concepts et préparer leurs révisions. L’IA peut réduire ces tâches répétitives et contribuer à créer une structure d’apprentissage plus claire et plus efficace.",

    aiSummaries:
      "Résumés générés par IA",

    aiSummariesText:
      "L’IA peut transformer de longs documents pédagogiques en résumés concis, structurés et faciles à réviser.",

    flashcards:
      "Flashcards et quiz",

    flashcardsText:
      "L’IA peut générer automatiquement des exercices de révision pour renforcer la mémorisation, le rappel des connaissances et la compréhension des concepts.",

    studyPlanning:
      "Planification des études",

    studyPlanningText:
      "L’IA peut aider à organiser les sessions d’apprentissage, les calendriers de révision, les priorités et le suivi de la progression.",

    knowledgeOrganization:
      "Organisation des connaissances",

    knowledgeOrganizationText:
      "L’IA peut structurer des informations complexes en parcours d’apprentissage plus clairs et en workflows pédagogiques plus faciles à suivre.",

    workflows:
      "Workflows d’apprentissage IA pour l’éducation moderne",

    workflowsText:
      "Les systèmes d’apprentissage alimentés par l’IA peuvent accompagner les étudiants, professionnels, chercheurs et organisations en simplifiant la révision des contenus, en accélérant l’acquisition des connaissances et en améliorant la productivité éducative.",

    runexa:
      "Comment Runexa Study Agent aide",

    runexaText:
      "Runexa Study Agent permet aux utilisateurs de téléverser des supports pédagogiques et de générer des résumés, quiz, flashcards, plans d’étude et workflows d’apprentissage structurés conçus pour améliorer la compréhension et la productivité.",

    support:
      "L’IA doit soutenir l’apprentissage, pas remplacer la réflexion",

    supportText:
      "Les systèmes éducatifs les plus efficaces utilisent l’IA pour aider les apprenants à comprendre les concepts plus rapidement tout en conservant le raisonnement humain, l’esprit critique et l’apprentissage actif au cœur du processus.",

    ctaTitle:
      "Apprenez plus efficacement grâce aux workflows IA",

    ctaText:
      "Utilisez Runexa Study Agent pour générer des résumés, quiz, flashcards, plans d’étude et workflows d’apprentissage structurés avec l’IA.",

    ctaButton:
      "Commencer à étudier",

    features: [
      "Résumés pédagogiques par IA",
      "Génération de flashcards",
      "Génération de quiz",
      "Planification des études",
      "Workflows d’apprentissage",
      "Outils de productivité éducative",
    ],
  },

  ar: {
    back: "← العودة إلى المدونة",

    category: "الذكاء التعليمي",

    title:
      "مساعد الدراسة بالذكاء الاصطناعي: بناء مسارات تعلم أكثر فاعلية",

    intro:
      "قد يكون استيعاب كميات كبيرة من المعلومات أمراً معقداً ومتكرراً ويستغرق وقتاً طويلاً. تساعد أدوات الدراسة المدعومة بالذكاء الاصطناعي الطلاب والمهنيين والمتعلمين على تنظيم المعرفة وإنشاء الملخصات وإعداد التمارين وبناء أساليب تعلم أكثر كفاءة.",

    whatIs:
      "ما هو مساعد الدراسة بالذكاء الاصطناعي؟",

    whatIsText:
      "يستخدم مساعد الدراسة بالذكاء الاصطناعي تقنيات الذكاء الاصطناعي لتحليل المواد التعليمية وتقديم دعم تعليمي منظم يشمل الملخصات والبطاقات التعليمية والاختبارات والشروحات وخطط المراجعة والتوصيات التعليمية المخصصة.",

    why:
      "لماذا قد تكون أساليب الدراسة التقليدية غير فعالة؟",

    whyText:
      "يقضي العديد من المتعلمين ساعات طويلة في تلخيص المستندات وتنظيم الملاحظات وإعادة صياغة المفاهيم وإعداد مواد المراجعة. ويمكن للذكاء الاصطناعي تقليل هذه المهام المتكررة والمساعدة في بناء هيكل تعلم أكثر وضوحاً وفعالية.",

    aiSummaries:
      "الملخصات المدعومة بالذكاء الاصطناعي",

    aiSummariesText:
      "يمكن للذكاء الاصطناعي تحويل المواد التعليمية الطويلة إلى ملخصات موجزة ومنظمة وأسهل للمراجعة.",

    flashcards:
      "البطاقات التعليمية والاختبارات",

    flashcardsText:
      "يمكن للذكاء الاصطناعي إنشاء تمارين مراجعة تلقائياً لدعم التذكر واسترجاع المعلومات وتعزيز فهم المفاهيم.",

    studyPlanning:
      "تخطيط الدراسة",

    studyPlanningText:
      "يمكن للذكاء الاصطناعي المساعدة في تنظيم جلسات التعلم وجداول المراجعة والأولويات التعليمية ومتابعة التقدم.",

    knowledgeOrganization:
      "تنظيم المعرفة",

    knowledgeOrganizationText:
      "يمكن للذكاء الاصطناعي تنظيم المعلومات المعقدة ضمن مسارات تعلم أوضح وتجارب تعليمية أكثر سهولة في المتابعة.",

    workflows:
      "مسارات التعلم بالذكاء الاصطناعي للتعليم الحديث",

    workflowsText:
      "يمكن لأنظمة التعلم المدعومة بالذكاء الاصطناعي مساعدة الطلاب والمهنيين والباحثين والمؤسسات من خلال تبسيط مراجعة المحتوى وتسريع اكتساب المعرفة وتحسين الإنتاجية التعليمية.",

    runexa:
      "كيف يساعد Runexa Study Agent",

    runexaText:
      "يُمكّن Runexa Study Agent المستخدمين من رفع المواد التعليمية وإنشاء ملخصات واختبارات وبطاقات تعليمية وخطط دراسة ومسارات تعلم منظمة مصممة لتحسين الفهم والإنتاجية.",

    support:
      "يجب أن يدعم الذكاء الاصطناعي التعلم لا أن يحل محل التفكير",

    supportText:
      "تساعد أفضل الأنظمة التعليمية المدعومة بالذكاء الاصطناعي المتعلمين على فهم المفاهيم بشكل أكثر كفاءة مع الحفاظ على التفكير النقدي والاستدلال البشري والتعلم النشط في صميم العملية التعليمية.",

    ctaTitle:
      "تعلّم بفاعلية أكبر مع مسارات التعلم الذكية",

    ctaText:
      "استخدم Runexa Study Agent لإنشاء الملخصات والاختبارات والبطاقات التعليمية وخطط الدراسة ومسارات التعلم المنظمة بالذكاء الاصطناعي.",

    ctaButton:
      "ابدأ الدراسة",

    features: [
      "ملخصات تعليمية بالذكاء الاصطناعي",
      "إنشاء البطاقات التعليمية",
      "إنشاء الاختبارات",
      "تخطيط الدراسة",
      "مسارات التعلم",
      "أدوات الإنتاجية التعليمية",
    ],
  },
};

type Locale = "en" | "fr" | "ar";

export default function AIStudyAssistantArticle({
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

      setLocale(
        updated === "fr" || updated === "ar"
          ? updated
          : initialLocale
      );
    };

    window.addEventListener(
      "locale-change",
      handleLocaleChange
    );

    return () =>
      window.removeEventListener(
        "locale-change",
        handleLocaleChange
      );
  }, [initialLocale, lockInitialLocale]);

  const t = translations[locale];
  return (
    <main
      dir={locale === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-6 py-20 text-slate-900"
    >
      <article className="mx-auto max-w-4xl">
        <Link href="/blog" className="text-sm font-semibold text-violet-600">
          {t.back}
        </Link>

        <p className="mt-8 text-sm font-semibold uppercase tracking-wide text-violet-600">
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
              [t.aiSummaries, t.aiSummariesText],
              [t.flashcards, t.flashcardsText],
              [t.studyPlanning, t.studyPlanningText],
              [t.knowledgeOrganization, t.knowledgeOrganizationText],
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
              {t.workflows}
            </h2>

            <p className="mt-4 leading-8 text-slate-600">
              {t.workflowsText}
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
              {t.features.map((item) => (
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

        <section className="mt-12 rounded-3xl bg-violet-600 p-8 text-white">
          <h2 className="text-3xl font-bold">
            {t.ctaTitle}
          </h2>

          <p className="mt-4 text-violet-100">
            {t.ctaText}
          </p>

          <Link
            href="/study"
            className="mt-6 inline-block rounded-xl bg-white px-6 py-3 text-sm font-semibold text-violet-600"
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
                  "https://runexa.ai/blog/ai-study-assistant",
              },

              headline:
                t.title,

              description:
                "Learn how AI study assistants help generate summaries, quizzes, flashcards, and structured learning workflows.",

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