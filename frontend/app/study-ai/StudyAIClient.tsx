"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getSavedLocale } from "../../lib/i18n";

const translations = {
  en: {
    badge: "Runexa Study Agent",
    title: "AI Study Assistant & Learning Workspace",
    subtitle:
      "Runexa Study Agent helps students and professionals generate summaries, quizzes, flashcards, study plans, and structured learning workflows with AI.",
    startStudying: "Start Studying",
    viewPricing: "View Pricing",

    aiSummaries: "AI summaries",
    aiSummariesText:
      "Generate structured summaries from study materials and documents.",
    flashcardsQuizzes: "Flashcards & quizzes",
    flashcardsQuizzesText:
      "Create interactive learning material automatically with AI.",
    studyPlans: "Study plans",
    studyPlansText:
      "Organize revision sessions and learning goals more efficiently.",
    learningWorkflows: "Learning workflows",
    learningWorkflowsText:
      "Build faster and more structured study workflows with AI assistance.",

    howItWorks: "How Runexa study AI works",
    steps: [
      "Upload study material or notes",
      "Runexa generates summaries, quizzes, and study tools",
      "Learn faster with structured AI learning workflows",
    ],

    faqTitle: "Study AI FAQ",
    faq: [
      [
        "Can Runexa replace a teacher?",
        "No. Runexa supports learning and revision, but it does not replace teachers, official materials, or academic guidance.",
      ],
      [
        "What can the Study Agent generate?",
        "Runexa can generate summaries, quizzes, flashcards, study plans, visual summaries, and learning workflows.",
      ],
      [
        "Can Runexa help with exam preparation?",
        "Yes. Runexa can help organize revision, identify key points, and create practice questions for study sessions.",
      ],
      [
        "Does Runexa support different education levels?",
        "Yes. Runexa Study Agent can adapt explanations and questions based on the selected education level.",
      ],
    ],

    jsonDescription:
      "AI study assistant for summaries, quizzes, flashcards, study plans, and structured learning workflows.",
  },

  fr: {
    badge: "Runexa Study Agent",
    title: "Assistant d’étude IA et espace d’apprentissage",
    subtitle:
      "Runexa Study Agent aide les étudiants et professionnels à générer des résumés, quiz, flashcards, plans d’étude et workflows d’apprentissage structurés avec l’IA.",
    startStudying: "Commencer à étudier",
    viewPricing: "Voir les tarifs",

    aiSummaries: "Résumés IA",
    aiSummariesText:
      "Générez des résumés structurés à partir de supports d’étude et de documents.",
    flashcardsQuizzes: "Flashcards et quiz",
    flashcardsQuizzesText:
      "Créez automatiquement du matériel d’apprentissage interactif avec l’IA.",
    studyPlans: "Plans d’étude",
    studyPlansText:
      "Organisez plus efficacement les sessions de révision et objectifs d’apprentissage.",
    learningWorkflows: "Workflows d’apprentissage",
    learningWorkflowsText:
      "Construisez des workflows d’étude plus rapides et structurés avec l’assistance IA.",

    howItWorks: "Comment fonctionne l’IA d’étude Runexa",
    steps: [
      "Téléversez un support d’étude ou des notes",
      "Runexa génère des résumés, quiz et outils d’étude",
      "Apprenez plus vite avec des workflows d’apprentissage IA structurés",
    ],

    faqTitle: "FAQ IA étude",
    faq: [
      [
        "Runexa peut-il remplacer un enseignant ?",
        "Non. Runexa soutient l’apprentissage et la révision, mais ne remplace pas les enseignants, supports officiels ou conseils académiques.",
      ],
      [
        "Que peut générer le Study Agent ?",
        "Runexa peut générer des résumés, quiz, flashcards, plans d’étude, résumés visuels et workflows d’apprentissage.",
      ],
      [
        "Runexa peut-il aider à préparer les examens ?",
        "Oui. Runexa peut aider à organiser les révisions, identifier les points clés et créer des questions d’entraînement.",
      ],
      [
        "Runexa prend-il en charge différents niveaux d’éducation ?",
        "Oui. Runexa Study Agent peut adapter les explications et questions selon le niveau d’éducation sélectionné.",
      ],
    ],

    jsonDescription:
      "Assistant d’étude IA pour générer résumés, quiz, flashcards, plans d’étude et workflows d’apprentissage structurés.",
  },

  ar: {
    badge: "وكيل Runexa للدراسة",
    title: "مساعد دراسة بالذكاء الاصطناعي ومساحة تعلم",
    subtitle:
      "يساعد Runexa Study Agent الطلاب والمهنيين على إنشاء ملخصات واختبارات وبطاقات تعليمية وخطط دراسة وتدفقات تعلم منظمة باستخدام الذكاء الاصطناعي.",
    startStudying: "ابدأ الدراسة",
    viewPricing: "عرض الأسعار",

    aiSummaries: "ملخصات بالذكاء الاصطناعي",
    aiSummariesText:
      "أنشئ ملخصات منظمة من المواد الدراسية والمستندات.",
    flashcardsQuizzes: "بطاقات تعليمية واختبارات",
    flashcardsQuizzesText:
      "أنشئ مواد تعليمية تفاعلية تلقائيًا باستخدام الذكاء الاصطناعي.",
    studyPlans: "خطط الدراسة",
    studyPlansText:
      "نظّم جلسات المراجعة وأهداف التعلم بكفاءة أكبر.",
    learningWorkflows: "تدفقات التعلم",
    learningWorkflowsText:
      "ابنِ تدفقات دراسة أسرع وأكثر تنظيمًا بمساعدة الذكاء الاصطناعي.",

    howItWorks: "كيف يعمل الذكاء الاصطناعي للدراسة في Runexa",
    steps: [
      "ارفع مادة دراسية أو ملاحظات",
      "ينشئ Runexa ملخصات واختبارات وأدوات دراسة",
      "تعلّم بشكل أسرع باستخدام تدفقات تعلم منظمة بالذكاء الاصطناعي",
    ],

    faqTitle: "أسئلة شائعة حول ذكاء الدراسة",
    faq: [
      [
        "هل يمكن لـ Runexa أن يحل محل المعلم؟",
        "لا. يدعم Runexa التعلم والمراجعة، لكنه لا يحل محل المعلمين أو المواد الرسمية أو التوجيه الأكاديمي.",
      ],
      [
        "ماذا يمكن أن ينشئ Study Agent؟",
        "يمكن لـ Runexa إنشاء ملخصات واختبارات وبطاقات تعليمية وخطط دراسة وملخصات بصرية وتدفقات تعلم.",
      ],
      [
        "هل يمكن لـ Runexa المساعدة في التحضير للامتحانات؟",
        "نعم. يمكن لـ Runexa المساعدة في تنظيم المراجعة وتحديد النقاط المهمة وإنشاء أسئلة تدريبية.",
      ],
      [
        "هل يدعم Runexa مستويات تعليمية مختلفة؟",
        "نعم. يمكن لـ Runexa Study Agent تكييف الشروحات والأسئلة حسب المستوى التعليمي المحدد.",
      ],
    ],

    jsonDescription:
      "مساعد دراسة بالذكاء الاصطناعي لإنشاء الملخصات والاختبارات والبطاقات التعليمية وخطط الدراسة وتدفقات التعلم المنظمة.",
  },
};

export default function StudyAIClient() {
  const [locale, setLocale] =
    useState<"en" | "fr" | "ar">("en");

  useEffect(() => {
    const saved = getSavedLocale();

    if (saved === "fr" || saved === "ar") {
      setLocale(saved);
    } else {
      setLocale("en");
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
      <section className="mx-auto max-w-6xl text-center">
        <p className="font-semibold text-violet-600">
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
            href="/study"
            className="rounded-xl bg-violet-600 px-6 py-3 text-sm font-semibold text-white hover:bg-violet-700"
          >
            {t.startStudying}
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
          [t.aiSummaries, t.aiSummariesText],
          [t.flashcardsQuizzes, t.flashcardsQuizzesText],
          [t.studyPlans, t.studyPlansText],
          [t.learningWorkflows, t.learningWorkflowsText],
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
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-violet-600 text-sm font-bold text-white">
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
