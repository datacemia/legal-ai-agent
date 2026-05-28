"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getSavedLocale } from "../../../lib/i18n";



const translations = {
  en: {
    back: "← Back to Blog",
    category: "Study AI",
    title: "AI Study Assistant: Smarter Learning With AI Workflows",

    intro:
      "Learning large amounts of information can be difficult, repetitive, and time-consuming. AI study assistants help students and professionals organize knowledge, generate summaries, create quizzes, and build more efficient learning workflows.",

    whatIs: "What is an AI study assistant?",

    whatIsText:
      "An AI study assistant uses artificial intelligence to analyze study materials and generate structured educational support such as summaries, flashcards, quizzes, explanations, revision plans, and learning recommendations.",

    why:
      "Why traditional studying is inefficient",

    whyText:
      "Many learners spend hours manually summarizing documents, organizing notes, rewriting concepts, and preparing revision material. AI can automate repetitive study tasks and improve learning structure.",

    aiSummaries: "AI summaries",

    aiSummariesText:
      "AI can transform long study documents into concise and structured summaries.",

    flashcards: "Flashcards & quizzes",

    flashcardsText:
      "AI can generate learning exercises automatically for revision and memory reinforcement.",

    studyPlanning: "Study planning",

    studyPlanningText:
      "AI can help organize learning sessions, revision schedules, and educational priorities.",

    knowledgeOrganization: "Knowledge organization",

    knowledgeOrganizationText:
      "AI can structure complex information into more understandable learning flows.",

    workflows:
      "AI learning workflows for modern education",

    workflowsText:
      "AI-powered learning systems can support students, professionals, researchers, and organizations by simplifying content review, accelerating knowledge acquisition, and improving educational productivity.",

    runexa:
      "How Runexa Study Agent helps",

    runexaText:
      "Runexa Study Agent helps users upload study materials and generate AI-powered summaries, quizzes, flashcards, study plans, and structured learning workflows designed to improve productivity and understanding.",

    support:
      "AI should support learning, not replace thinking",

    supportText:
      "The best educational AI systems help learners understand concepts more efficiently while keeping human reasoning, critical thinking, and active learning at the center of the process.",

    ctaTitle:
      "Learn faster with AI study workflows",

    ctaText:
      "Use Runexa Study Agent to generate summaries, quizzes, flashcards, and structured learning workflows with AI.",

    ctaButton: "Start Studying",

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
    category: "IA étude",
    title:
      "Assistant d’étude IA : apprendre plus intelligemment avec des workflows IA",

    intro:
      "Apprendre de grandes quantités d’informations peut être difficile et répétitif. Les assistants d’étude IA aident étudiants et professionnels à organiser les connaissances, générer des résumés, créer des quiz et améliorer les workflows d’apprentissage.",

    whatIs:
      "Qu’est-ce qu’un assistant d’étude IA ?",

    whatIsText:
      "Un assistant d’étude IA utilise l’intelligence artificielle pour analyser des supports pédagogiques et générer des résumés, flashcards, quiz, explications et recommandations d’apprentissage.",

    why:
      "Pourquoi les méthodes d’étude traditionnelles sont inefficaces",

    whyText:
      "Beaucoup d’apprenants passent des heures à résumer des documents, organiser des notes et préparer du matériel de révision. L’IA peut automatiser ces tâches répétitives.",

    aiSummaries: "Résumés IA",

    aiSummariesText:
      "L’IA peut transformer de longs documents d’étude en résumés structurés et concis.",

    flashcards: "Flashcards et quiz",

    flashcardsText:
      "L’IA peut générer automatiquement des exercices de révision et de mémorisation.",

    studyPlanning: "Planification des études",

    studyPlanningText:
      "L’IA peut aider à organiser les sessions d’apprentissage et les priorités éducatives.",

    knowledgeOrganization:
      "Organisation des connaissances",

    knowledgeOrganizationText:
      "L’IA peut structurer des informations complexes en workflows d’apprentissage plus compréhensibles.",

    workflows:
      "Workflows IA pour l’éducation moderne",

    workflowsText:
      "Les systèmes d’apprentissage IA peuvent aider étudiants, chercheurs et organisations à améliorer la productivité éducative.",

    runexa:
      "Comment Runexa Study Agent aide",

    runexaText:
      "Runexa Study Agent aide les utilisateurs à téléverser des supports pédagogiques et générer résumés, quiz, flashcards et workflows d’apprentissage structurés.",

    support:
      "L’IA doit soutenir l’apprentissage, pas remplacer la réflexion",

    supportText:
      "Les meilleurs systèmes IA éducatifs améliorent la compréhension tout en gardant la réflexion critique et l’apprentissage actif au centre du processus.",

    ctaTitle:
      "Apprenez plus vite avec les workflows IA",

    ctaText:
      "Utilisez Runexa Study Agent pour générer résumés, quiz, flashcards et workflows d’apprentissage structurés.",

    ctaButton: "Commencer à étudier",

    features: [
      "Résumés d’étude IA",
      "Génération de flashcards",
      "Génération de quiz",
      "Planification des études",
      "Workflows d’apprentissage",
      "Outils de productivité éducative",
    ],
  },

  ar: {
    back: "← العودة إلى المدونة",
    category: "ذكاء الدراسة",
    title:
      "مساعد الدراسة بالذكاء الاصطناعي: تعلم أكثر ذكاءً باستخدام تدفقات العمل الذكية",

    intro:
      "قد يكون تعلم كميات كبيرة من المعلومات صعبًا ومتكررًا ويستغرق وقتًا طويلًا. تساعد أدوات الدراسة بالذكاء الاصطناعي الطلاب والمهنيين على تنظيم المعرفة وإنشاء ملخصات واختبارات وتحسين تدفقات التعلم.",

    whatIs:
      "ما هو مساعد الدراسة بالذكاء الاصطناعي؟",

    whatIsText:
      "يستخدم مساعد الدراسة بالذكاء الاصطناعي تقنيات الذكاء الاصطناعي لتحليل المواد الدراسية وإنشاء ملخصات وبطاقات تعليمية واختبارات وخطط مراجعة.",

    why:
      "لماذا الدراسة التقليدية غير فعالة",

    whyText:
      "يقضي العديد من المتعلمين ساعات طويلة في تلخيص المستندات وتنظيم الملاحظات وإعادة كتابة المفاهيم. يمكن للذكاء الاصطناعي أتمتة هذه المهام وتحسين بنية التعلم.",

    aiSummaries: "ملخصات الذكاء الاصطناعي",

    aiSummariesText:
      "يمكن للذكاء الاصطناعي تحويل المستندات الدراسية الطويلة إلى ملخصات منظمة ومختصرة.",

    flashcards: "بطاقات تعليمية واختبارات",

    flashcardsText:
      "يمكن للذكاء الاصطناعي إنشاء تمارين تعليمية للمراجعة وتعزيز الذاكرة.",

    studyPlanning: "تخطيط الدراسة",

    studyPlanningText:
      "يمكن للذكاء الاصطناعي المساعدة في تنظيم جلسات التعلم والجداول التعليمية.",

    knowledgeOrganization:
      "تنظيم المعرفة",

    knowledgeOrganizationText:
      "يمكن للذكاء الاصطناعي تنظيم المعلومات المعقدة في تدفقات تعلم أكثر وضوحًا.",

    workflows:
      "تدفقات التعلم بالذكاء الاصطناعي للتعليم الحديث",

    workflowsText:
      "يمكن لأنظمة التعلم بالذكاء الاصطناعي دعم الطلاب والباحثين والمؤسسات وتحسين الإنتاجية التعليمية.",

    runexa:
      "كيف يساعد Runexa Study Agent",

    runexaText:
      "يساعد Runexa Study Agent المستخدمين على رفع المواد الدراسية وإنشاء ملخصات واختبارات وبطاقات تعليمية وخطط تعلم منظمة.",

    support:
      "يجب أن يدعم الذكاء الاصطناعي التعلم لا أن يستبدل التفكير",

    supportText:
      "تساعد أفضل أنظمة الذكاء الاصطناعي التعليمية المتعلمين على الفهم بشكل أفضل مع الحفاظ على التفكير النقدي والتعلم النشط.",

    ctaTitle:
      "تعلم بشكل أسرع باستخدام تدفقات الدراسة الذكية",

    ctaText:
      "استخدم Runexa Study Agent لإنشاء ملخصات واختبارات وبطاقات تعليمية وتدفقات تعلم منظمة.",

    ctaButton: "ابدأ الدراسة",

    features: [
      "ملخصات دراسية بالذكاء الاصطناعي",
      "إنشاء البطاقات التعليمية",
      "إنشاء الاختبارات",
      "تخطيط الدراسة",
      "تدفقات التعلم",
      "أدوات الإنتاجية التعليمية",
    ],
  },
};

export default function AIStudyAssistantArticle() {
  const [locale, setLocale] =
    useState<"en" | "fr" | "ar">("en");

  useEffect(() => {
    const saved = getSavedLocale();

    if (saved === "fr" || saved === "ar") setLocale(saved);

    const handleLocaleChange = () => {
      const updated = getSavedLocale();

      setLocale(
        updated === "fr" || updated === "ar"
          ? updated
          : "en"
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
  }, []);

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