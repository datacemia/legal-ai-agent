"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { getToken } from "../../lib/auth";
import { getSavedLocale, setSavedLocale } from "../../lib/i18n";

const safeGetLocalStorage = (key: string, fallback = "") => {
  if (typeof window === "undefined") return fallback;

  return localStorage.getItem(key) || fallback;
};

const safeSetLocalStorage = (key: string, value: string) => {
  if (typeof window === "undefined") return;

  localStorage.setItem(key, value);
};


const LEVEL_LABELS: any = {
  en: {
    primary_school: "Primary school",
    middle_school: "Middle school",
    high_school: "High school",
    vocational_training: "Vocational training",
    university: "University",
  },
  fr: {
    primary_school: "École primaire",
    middle_school: "Collège",
    high_school: "Lycée",
    vocational_training: "Formation professionnelle",
    university: "Université",
  },
  ar: {
    primary_school: "المرحلة الابتدائية",
    middle_school: "المرحلة الإعدادية",
    high_school: "المرحلة الثانوية",
    vocational_training: "التكوين المهني",
    university: "الجامعة",
  },
};

const FeatureIcon = ({ index }: { index: number }) => {
  const icons = [
    <path key="summary" d="M7 4.75h10M7 8.5h10M7 12.25h6M5.5 19.25h13a1.75 1.75 0 0 0 1.75-1.75v-11A1.75 1.75 0 0 0 18.5 4.75h-13A1.75 1.75 0 0 0 3.75 6.5v11a1.75 1.75 0 0 0 1.75 1.75Z" />,
    <path key="audio" d="M5 14.25h3.25L13 18V6L8.25 9.75H5v4.5Zm11.5-5.5a4.5 4.5 0 0 1 0 6.5m2.5-9a8 8 0 0 1 0 11.5" />,
    <path key="mindmap" d="M12 5.25v4.5m0 4.5v4.5M7.5 9.75h9M6.25 6.5h1.5a1.75 1.75 0 0 1 1.75 1.75A1.75 1.75 0 0 1 7.75 10h-1.5A1.75 1.75 0 0 1 4.5 8.25 1.75 1.75 0 0 1 6.25 6.5Zm10 0h1.5a1.75 1.75 0 0 1 1.75 1.75A1.75 1.75 0 0 1 17.75 10h-1.5a1.75 1.75 0 0 1-1.75-1.75 1.75 1.75 0 0 1 1.75-1.75ZM6.25 14h1.5a1.75 1.75 0 0 1 1.75 1.75 1.75 1.75 0 0 1-1.75 1.75h-1.5a1.75 1.75 0 0 1-1.75-1.75A1.75 1.75 0 0 1 6.25 14Zm10 0h1.5a1.75 1.75 0 0 1 1.75 1.75 1.75 1.75 0 0 1-1.75 1.75h-1.5a1.75 1.75 0 0 1-1.75-1.75A1.75 1.75 0 0 1 16.25 14Z" />,
    <path key="target" d="M12 20.25a8.25 8.25 0 1 0 0-16.5 8.25 8.25 0 0 0 0 16.5Zm0-3.25a5 5 0 1 0 0-10 5 5 0 0 0 0 10Zm0-3.25a1.75 1.75 0 1 0 0-3.5 1.75 1.75 0 0 0 0 3.5Z" />,
    <path key="quiz" d="M8.25 7.25h7.5M8.25 12h7.5M8.25 16.75h4.5M5.25 7.25h.01M5.25 12h.01M5.25 16.75h.01M6 21h12a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2Z" />,
    <path key="score" d="M6.5 12.5 10 16l7.5-8M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Z" />,
    <path key="cards" d="M7.25 6.25h9.5A2.25 2.25 0 0 1 19 8.5v7a2.25 2.25 0 0 1-2.25 2.25h-9.5A2.25 2.25 0 0 1 5 15.5v-7a2.25 2.25 0 0 1 2.25-2.25Zm2 3.25h5.5M9.25 13h3.5M3.75 9.25v8.25A2.75 2.75 0 0 0 6.5 20.25h8.25" />,
    <path key="plan" d="M7 3.75v3M17 3.75v3M5.5 6.25h13A1.75 1.75 0 0 1 20.25 8v10.5a1.75 1.75 0 0 1-1.75 1.75h-13a1.75 1.75 0 0 1-1.75-1.75V8A1.75 1.75 0 0 1 5.5 6.25Zm-1.75 4.5h16.5M8 14h2.5M8 17h5" />,
    <path key="weak" d="M12 3.75 20.25 18a1.5 1.5 0 0 1-1.3 2.25H5.05A1.5 1.5 0 0 1 3.75 18L12 3.75Zm0 5.5v4.25m0 3.25h.01" />,
    <path key="adaptive" d="M5.5 12a6.5 6.5 0 0 1 11.25-4.44L18.75 9.5M18.5 12a6.5 6.5 0 0 1-11.25 4.44L5.25 14.5M18.75 6.25V9.5H15.5M5.25 17.75V14.5H8.5" />,
    <path key="cache" d="M12 3.75c4.28 0 7.75 1.34 7.75 3s-3.47 3-7.75 3-7.75-1.34-7.75-3 3.47-3 7.75-3Zm-7.75 3v5.25c0 1.66 3.47 3 7.75 3s7.75-1.34 7.75-3V6.75m-15.5 5.25v5.25c0 1.66 3.47 3 7.75 3s7.75-1.34 7.75-3V12" />,
  ];

  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
      className="h-5 w-5"
      aria-hidden="true"
    >
      {icons[index] || icons[0]}
    </svg>
  );
};

const labels: any = {
  en: {
    title: "Study Agent",
    subtitle:
      "Upload a document to generate a summary, theoretical quiz, practical quiz, flashcards, and a study plan.",
    howTitle: "What the Study Agent does:",
    how1:
      "Upload a PDF, Word document, or scanned study file. The Study Agent turns it into a complete, personalized learning workspace in minutes.",
    how2:
      "Before analysis, choose your education level and output language. The agent adapts summaries, explanations, quizzes, flashcards, and study plans to your level.",
    items: [
      "Structured summary and detailed explanation",
      "Audio playback for the detailed summary",
      "Visual summary and interactive mind map",
      "Key learning points",
      "Theoretical and practical quizzes",
      "Instant scoring with explanations",
      "Flashcards for memorization",
      "Personalized study plan",
      "Weak-point tracking after quiz attempts",
      "Adaptive learning based on your mistakes",
      "Fast cached results for repeated documents",
    ],
    how3:
      "After each quiz, the system identifies your weak points and uses them to personalize future learning sessions.",
    disclaimer:
      "Runexa Study Agent is designed to support learning and revision. Always verify important academic information with your teacher, institution, or official course materials.",
    analyze: "Analyze",
    buyCredits: "Buy credits",
    chooseLevel: "Choose your level",
    selectLevel: "Select education level",
    levelHelp:
      "This helps the Study Agent adapt explanations and questions to your level.",
    cancel: "Cancel",
    continue: "Continue",
    results: "Results",
    level: "Level",
    language: "Language",
    summary: "Summary",
    writtenSummary: "Detailed Summary",
    visualSummary: "Visual Summary",
    visualDiagram: "Visual Diagram",
    diagramExplanations: "Diagram Explanations",
    keyPoints: "Key Points",
    quiz: "Quiz",
    theory: "Theoretical Questions",
    practice: "Practical Questions",
    submitQuiz: "Submit quiz",
    answerAll: "Answer all questions to submit",
    quizSubmitted: "Quiz submitted",
    score: "Score",
    learningFeedback: "Learning feedback",
    retryQuiz: "Retry quiz",
    noRetries: "No retries left",
    flashcards: "Flashcards",
    front: "Front",
    back: "Back",
    studyPlan: "Study Plan",
    quality: "Quality",
    qualityScore: "Quality score",
    qualityValid: "Output validated",
    qualityIssues: "Quality issues",
    correct: "Correct",
    incorrect: "Incorrect",
    answer: "Answer",
    paymentMessage:
      "Stripe is not configured yet. $1 trial activation, credits, and plans will be available soon.",
    proMessage:
      "Pro plan is not configured yet. Stripe will be activated soon.",
    trialInfo: "$1 trial per agent. After your trial, continue with credits or a plan.",
    startTrial: "Start $1 trial",
    trialUsed: "Trial already used for study",
    paymentRequired: "$1 Study trial activation required",
    proDirect: "Want Pro directly? Pro and Premium plans will be available soon for all agents.",
    errorMessage: "Failed to connect to Study Agent API.",
    noFile: "No file selected",
    chooseFile: "Choose a document (PDF, Word, or scanned)",
    loadingSteps: {
      extracting: "Extracting text...",
      summary: "Generating summary...",
      quiz: "Creating quiz...",
      finalizing: "Finalizing...",
      analyzing: "Analyzing...",
      analyzingStudy: "Analyzing study content...",
      savingResult: "Saving study result...",
      savingHistory: "Saving study history...",
    },
    remaining: "remaining",
    elapsed: "Elapsed",
  },
  fr: {
    title: "Agent étude",
    subtitle:
      "Téléchargez un document pour générer un résumé, un quiz théorique, un quiz pratique, des flashcards et un plan de révision.",
    howTitle: "Ce que fait l’Agent étude :",
    how1:
      "Téléchargez un PDF, un document Word ou un fichier scanné. L’Agent étude le transforme en espace d’apprentissage complet et personnalisé en quelques minutes.",
    how2:
      "Avant l’analyse, choisissez votre niveau d’étude et la langue de sortie. L’agent adapte les résumés, explications, quiz, flashcards et plans de révision à votre niveau.",
    items: [
      "Résumé structuré et explication détaillée",
      "Lecture audio du résumé détaillé",
      "Résumé visuel et carte mentale interactive",
      "Points clés à retenir",
      "Quiz théoriques et pratiques",
      "Score instantané avec explications",
      "Flashcards pour mémoriser",
      "Plan de révision personnalisé",
      "Détection des points faibles après chaque quiz",
      "Apprentissage adaptatif basé sur vos erreurs",
      "Résultats rapides grâce au cache intelligent",
    ],
    how3:
      "Après chaque quiz, le système identifie vos points faibles et les utilise pour personnaliser vos prochaines sessions d’apprentissage.",
    disclaimer:
      "Runexa Study Agent est conçu pour accompagner l’apprentissage et la révision. Vérifiez toujours les informations académiques importantes avec votre enseignant, votre établissement ou vos supports officiels.",
    analyze: "Analyser",
    buyCredits: "Acheter des crédits",
    chooseLevel: "Choisissez votre niveau",
    selectLevel: "Sélectionnez le niveau d’étude",
    levelHelp:
      "Cela aide l’agent étude à adapter les explications et les questions à votre niveau.",
    cancel: "Annuler",
    continue: "Continuer",
    results: "Résultats",
    level: "Niveau",
    language: "Langue",
    summary: "Résumé",
    writtenSummary: "Résumé détaillé",
    visualSummary: "Résumé graphique",
    visualDiagram: "Schéma visuel",
    diagramExplanations: "Explications du schéma",
    keyPoints: "Points clés",
    quiz: "Quiz",
    theory: "Questions théoriques",
    practice: "Questions pratiques",
    submitQuiz: "Soumettre le quiz",
    answerAll: "Répondez à toutes les questions pour soumettre",
    quizSubmitted: "Quiz soumis",
    score: "Score",
    learningFeedback: "Feedback d’apprentissage",
    retryQuiz: "Réessayer le quiz",
    noRetries: "Plus d’essais disponibles",
    flashcards: "Flashcards",
    front: "Recto",
    back: "Verso",
    studyPlan: "Plan de révision",
    quality: "Qualité",
    qualityScore: "Score qualité",
    qualityValid: "Résultat validé",
    qualityIssues: "Problèmes qualité",
    correct: "Correct",
    incorrect: "Incorrect",
    answer: "Réponse",
    paymentMessage:
      "Stripe n’est pas encore configuré. L’activation de l’essai à 1$, les crédits et les abonnements seront bientôt disponibles.",
    proMessage:
      "Le plan Pro n’est pas encore configuré. Stripe sera bientôt activé.",
    trialInfo: "Essai à 1$ par agent. Après l’essai, continuez avec des crédits ou un abonnement.",
    startTrial: "Activer l’essai à 1$",
    trialUsed: "Essai Study déjà utilisé",
    paymentRequired: "Activation de l’essai Study à 1$ requise",
    proDirect: "Vous voulez passer directement à Pro ? Les abonnements Pro et Premium seront bientôt disponibles pour tous les agents.",
    errorMessage: "Impossible de se connecter à l’API Study Agent.",
    noFile: "Aucun fichier sélectionné",
    chooseFile: "Choisir un document (PDF, Word ou scanné)",
    loadingSteps: {
      extracting: "Extraction du texte...",
      summary: "Génération du résumé...",
      quiz: "Création du quiz...",
      finalizing: "Finalisation...",
      analyzing: "Analyse en cours...",
      analyzingStudy: "Analyse du contenu...",
      savingResult: "Sauvegarde du résultat...",
      savingHistory: "Sauvegarde de l’historique...",
    },
    remaining: "restantes",
    elapsed: "Temps écoulé",
  },
  ar: {
    title: "وكيل الدراسة",
    subtitle:
      "ارفع ملف دراسة لإنشاء ملخص، اختبار نظري، اختبار تطبيقي، بطاقات مراجعة وخطة دراسة.",
    howTitle: "ما الذي يقدمه وكيل الدراسة:",
    how1:
      "ارفع ملف PDF أو Word أو مستنداً ممسوحاً ضوئياً. يحوّله وكيل الدراسة إلى مساحة تعلم كاملة وشخصية خلال دقائق.",
    how2:
      "قبل التحليل، اختر مستواك التعليمي ولغة النتائج. يقوم الوكيل بتكييف الملخصات، الشروحات، الاختبارات، بطاقات المراجعة وخطة الدراسة حسب مستواك.",
    items: [
      "ملخص منظم وشرح مفصل",
      "استماع صوتي للملخص المفصل",
      "ملخص بصري وخريطة ذهنية تفاعلية",
      "نقاط تعلم أساسية",
      "اختبارات نظرية وتطبيقية",
      "تصحيح فوري مع الشروحات",
      "بطاقات مراجعة للحفظ",
      "خطة دراسة مخصصة",
      "تحديد نقاط الضعف بعد كل اختبار",
      "تعلم تكيفي بناءً على أخطائك",
      "نتائج أسرع بفضل التخزين الذكي",
    ],
    how3:
      "بعد كل اختبار، يحدد النظام نقاط ضعفك ويستخدمها لتخصيص جلسات التعلم القادمة.",
    disclaimer:
      "تم تصميم Runexa Study Agent لدعم التعلم والمراجعة. تحقق دائماً من المعلومات الأكاديمية المهمة مع أستاذك أو مؤسستك أو المراجع الرسمية.",
    analyze: "تحليل",
    buyCredits: "شراء رصيد",
    chooseLevel: "اختر مستواك",
    selectLevel: "اختر المستوى التعليمي",
    levelHelp: "يساعد هذا وكيل الدراسة على تكييف الشرح والأسئلة مع مستواك.",
    cancel: "إلغاء",
    continue: "متابعة",
    results: "النتائج",
    level: "المستوى",
    language: "اللغة",
    summary: "الملخص",
    writtenSummary: "ملخص مفصل",
    visualSummary: "ملخص بصري",
    visualDiagram: "مخطط بصري",
    diagramExplanations: "شرح المخطط",
    keyPoints: "النقاط الأساسية",
    quiz: "الاختبار",
    theory: "أسئلة نظرية",
    practice: "أسئلة تطبيقية",
    submitQuiz: "إرسال الاختبار",
    answerAll: "أجب عن جميع الأسئلة للإرسال",
    quizSubmitted: "تم إرسال الاختبار",
    score: "النتيجة",
    learningFeedback: "تقييم التعلم",
    retryQuiz: "إعادة المحاولة",
    noRetries: "لا توجد محاولات متبقية",
    flashcards: "بطاقات المراجعة",
    front: "الوجه الأمامي",
    back: "الوجه الخلفي",
    studyPlan: "خطة الدراسة",
    quality: "الجودة",
    qualityScore: "درجة الجودة",
    qualityValid: "تم التحقق من النتيجة",
    qualityIssues: "ملاحظات الجودة",
    correct: "صحيح",
    incorrect: "غير صحيح",
    answer: "الإجابة",
    paymentMessage:
      "Stripe غير مفعّل حالياً. تفعيل تجربة 1 دولار، الأرصدة والاشتراكات ستكون متاحة قريباً.",
    proMessage:
      "خطة Pro غير مفعلة حالياً. سيتم تفعيل Stripe قريباً.",
    trialInfo: "تجربة بقيمة 1 دولار لكل وكيل. بعد التجربة يمكنك المتابعة بالأرصدة أو الاشتراك.",
    startTrial: "تفعيل تجربة 1 دولار",
    trialUsed: "تم استخدام تجربة وكيل الدراسة",
    paymentRequired: "يلزم تفعيل تجربة الدراسة بقيمة 1 دولار",
    proDirect: "هل تريد الاشتراك في Pro مباشرة؟ ستتوفر خطط Pro و Premium قريباً لجميع الوكلاء.",
    errorMessage: "تعذر الاتصال بواجهة Study Agent.",
    noFile: "لم يتم اختيار ملف (PDF أو Word أو ممسوح ضوئياً)",
    chooseFile: "اختيار ملف (PDF أو Word أو ممسوح ضوئياً)",
    loadingSteps: {
      extracting: "جارٍ استخراج النص...",
      summary: "جارٍ إنشاء الملخص...",
      quiz: "جارٍ إنشاء الاختبار...",
      finalizing: "جارٍ إنهاء العملية...",
      analyzing: "جارٍ التحليل...",
      analyzingStudy: "جارٍ تحليل المحتوى...",
      savingResult: "جارٍ حفظ النتيجة...",
      savingHistory: "جارٍ حفظ سجل الدراسة...",
    },
    remaining: "متبقية",
    elapsed: "الوقت المنقضي",
  },
};

function isValidMermaid(code: string) {
  return (
    typeof code === "string" &&
    code.trim().startsWith("mindmap") &&
    code.includes("\n")
  );
}

function fallbackDiagram() {
  return `mindmap
  root((Fallback))
    Idea 1
      Keyword
    Idea 2
      Keyword
    Idea 3
      Keyword`;
}

function normalizeExplanationKey(value: string) {
  return String(value || "")
    .replace(/\s+/g, " ")
    .trim()
    .toLowerCase()
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^\p{L}\p{N}\s]/gu, "");
}

function findDiagramExplanation(
  explanations: Record<string, unknown> | undefined,
  label: string | null
) {
  if (!explanations || !label) return null;

  if (Object.prototype.hasOwnProperty.call(explanations, label)) {
    return String(explanations[label]);
  }

  const normalizedLabel = normalizeExplanationKey(label);
  const matchedEntry = Object.entries(explanations).find(
    ([key]) => normalizeExplanationKey(key) === normalizedLabel
  );

  return matchedEntry ? String(matchedEntry[1]) : null;
}


function sanitizeDiagramTitle(value: string, language: string) {
  const fallback =
    language === "ar"
      ? "موضوع الدرس"
      : language === "fr"
      ? "Sujet du cours"
      : "Course topic";

  const cleaned = String(value || "")
    .replace(/\s+/g, " ")
    .replace(/[(){}\[\]|<>`"]+/g, "")
    .trim();

  if (!cleaned) return fallback;

  return cleaned.slice(0, 55).trim() || fallback;
}

function extractDiagramTitle(result: any, language: string) {
  if (!result) {
    return language === "ar"
      ? "موضوع الدرس"
      : language === "fr"
      ? "Sujet du cours"
      : "Course topic";
  }

  const genericRootLabels = [
    "الموضوع الرئيسي",
    "موضوع رئيسي",
    "Sujet principal",
    "Main topic",
    "Résumé graphique",
    "Visual summary",
  ];

  const isGenericLabel = (value: string) => {
    const normalized = normalizeExplanationKey(value);
    return genericRootLabels.some(
      (label) => normalizeExplanationKey(label) === normalized
    );
  };

  const visualSummary = result?.visual_summary;
  const candidates: string[] = [];

  if (visualSummary && typeof visualSummary === "object" && !Array.isArray(visualSummary)) {
    candidates.push(
      String(
        visualSummary.title ||
          visualSummary.subject ||
          visualSummary.main_topic ||
          ""
      )
    );
  }

  if (typeof visualSummary === "string") {
    const firstMeaningfulLine = visualSummary
      .split("\n")
      .map((line) => line.trim())
      .find(Boolean);

    if (firstMeaningfulLine) {
      const colonIndex = firstMeaningfulLine.indexOf(":");

      if (colonIndex > -1) {
        const beforeColon = firstMeaningfulLine.slice(0, colonIndex).trim();
        const afterColon = firstMeaningfulLine.slice(colonIndex + 1).trim();

        if (isGenericLabel(beforeColon) && afterColon) {
          candidates.push(afterColon);
        } else {
          candidates.push(firstMeaningfulLine);
        }
      } else {
        candidates.push(firstMeaningfulLine);
      }
    }
  }

  candidates.push(result?.title, result?.topic, result?.main_topic);

  const summary = String(result?.summary || "").trim();
  if (summary) {
    const summaryMatch = summary.match(
      /(موضوع|حول|about|on|sur)\s+([^،,.؛:]{8,80})/i
    );
    candidates.push(summaryMatch?.[2] || summary);
  }

  const fallback =
    language === "ar"
      ? "موضوع الدرس"
      : language === "fr"
      ? "Sujet du cours"
      : "Course topic";

  const bestCandidate = candidates
    .map((candidate) => String(candidate || "").trim())
    .find((candidate) => candidate && !isGenericLabel(candidate));

  return sanitizeDiagramTitle(bestCandidate || fallback, language);
}

function replaceRootLabel(chart: string, title: string) {
  if (!chart || !title) return chart;

  return chart.replace(/root\(\((.*?)\)\)/, `root((${title}))`);
}

function buildDiagramExplanationsForFixedRoot(
  explanations: Record<string, unknown> | undefined,
  title: string,
  language: string
) {
  if (!explanations || !title) return explanations;

  const genericKeys =
    language === "ar"
      ? ["الموضوع الرئيسي", "موضوع رئيسي"]
      : language === "fr"
      ? ["Sujet principal", "sujet principal"]
      : ["Main topic", "main topic"];

  const existingTitleExplanation = findDiagramExplanation(explanations, title);
  if (existingTitleExplanation) return explanations;

  const genericExplanation = genericKeys
    .map((key) => findDiagramExplanation(explanations, key))
    .find(Boolean);

  if (!genericExplanation) return explanations;

  return {
    ...explanations,
    [title]: genericExplanation,
  };
}


type VisualSummaryBlock = {
  title: string;
  items: string[];
};

function parseVisualSummary(value: any) {
  if (!value) {
    return {
      title: "",
      blocks: [] as VisualSummaryBlock[],
    };
  }

  if (typeof value === "object" && !Array.isArray(value)) {
    const rawBlocks = value.blocks || value.sections || value.items || [];

    if (Array.isArray(value.key_points)) {
      return {
        title: String(value.title || value.subject || value.main_topic || ""),
        blocks: value.key_points
          .map((point: any) => ({
            title: String(point).trim(),
            items: [],
          }))
          .filter((block: VisualSummaryBlock) => block.title),
      };
    }

    return {
      title: String(value.title || value.subject || value.main_topic || ""),
      blocks: Array.isArray(rawBlocks)
        ? rawBlocks
            .map((block: any) => ({
              title: String(block.title || block.name || block.heading || "").trim(),
              items: Array.isArray(block.items || block.points || block.children)
                ? (block.items || block.points || block.children)
                    .map((item: any) => String(item).trim())
                    .filter(Boolean)
                : [],
            }))
            .filter((block: VisualSummaryBlock) => block.title || block.items.length)
        : [],
    };
  }

  const rawLines = String(value)
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);

  const genericTitleLabels = [
    "sujet principal",
    "main topic",
    "موضوع رئيسي",
    "الموضوع الرئيسي",
    "résumé graphique",
    "visual summary",
  ];

  const isGenericTitleLabel = (line: string) => {
    const normalized = normalizeExplanationKey(line);
    return genericTitleLabels.some(
      (label) => normalizeExplanationKey(label) === normalized
    );
  };

  const isNumberOnly = (line: string) => /^[0-9]+[.)]?$/.test(line.trim());
  const lines = rawLines.filter((line) => !isNumberOnly(line));

  let title = "";
  const blocks: VisualSummaryBlock[] = [];
  let currentBlock: VisualSummaryBlock | null = null;

  const splitDetails = (text: string) =>
    text
      .split(/[,;•|]+/)
      .map((item) => item.trim())
      .filter(Boolean);

  const addItems = (items: string[]) => {
    const cleanItems = items
      .map((item) => item.replace(/^[-•*]+\s*/, "").trim())
      .filter(Boolean);

    if (!cleanItems.length) return;

    if (!currentBlock) {
      currentBlock = {
        title: title || "Points clés",
        items: [],
      };
      blocks.push(currentBlock);
    }

    currentBlock.items.push(...cleanItems);
  };

  const isLikelyBlockTitle = (line: string) => {
    const cleanLine = line.replace(/^[-•*]+\s*/, "").trim();

    if (!cleanLine) return false;
    if (/^[IVXLCDM]+\s*[-–.]/i.test(cleanLine)) return true;
    if (/^[0-9]+\s*[-–.]/.test(cleanLine)) return true;
    if (cleanLine.includes(":")) return true;
    if (cleanLine.length <= 55 && cleanLine[0] === cleanLine[0].toUpperCase()) {
      return true;
    }

    return false;
  };

  const sameAsTitle = (line: string) => {
    return (
      title &&
      normalizeExplanationKey(line) === normalizeExplanationKey(title)
    );
  };

  lines.forEach((line) => {
    const cleanLine = line.replace(/^[-•*]+\s*/, "").trim();
    const isBullet = /^[-•*]+\s*/.test(line);

    if (!cleanLine || isGenericTitleLabel(cleanLine)) return;

    if (!title) {
      title = cleanLine.replace(/:$/, "");
      return;
    }

    if (sameAsTitle(cleanLine)) return;

    if (isBullet) {
      addItems([cleanLine]);
      return;
    }

    const colonIndex = cleanLine.indexOf(":");

    if (colonIndex > -1) {
      const rawTitle = cleanLine.slice(0, colonIndex).trim();
      const detailText = cleanLine.slice(colonIndex + 1).trim();

      if (rawTitle && rawTitle.length <= 70) {
        currentBlock = {
          title: rawTitle.replace(/:$/, ""),
          items: detailText ? splitDetails(detailText) : [],
        };
        blocks.push(currentBlock);
        return;
      }
    }

    if (isLikelyBlockTitle(cleanLine)) {
      currentBlock = {
        title: cleanLine.replace(/:$/, ""),
        items: [],
      };
      blocks.push(currentBlock);
      return;
    }

    addItems([cleanLine]);
  });

  if (!blocks.length && title) {
    return {
      title,
      blocks: [
        {
          title: "Points clés",
          items: lines
            .filter((line) => !isGenericTitleLabel(line))
            .filter(
              (line) =>
                normalizeExplanationKey(line) !== normalizeExplanationKey(title)
            )
            .map((line) => line.replace(/^[-•*]+\s*/, "").trim())
            .filter(Boolean),
        },
      ],
    };
  }

  return {
    title,
    blocks,
  };
}

function VisualSummaryGraphic({
  value,
  language = "en",
}: {
  value: any;
  language?: string;
}) {
  const visualSummary = parseVisualSummary(value);
  const blocks = visualSummary.blocks.slice(0, 6);

  const fallbackTitle =
    language === "fr"
      ? "Résumé du cours"
      : language === "ar"
      ? "ملخص الدرس"
      : "Course summary";

  const centerTitle = visualSummary.title || fallbackTitle;

  return (
    <div className="mt-3 rounded-3xl border border-slate-200 bg-gradient-to-br from-slate-50 via-white to-blue-50 p-5 shadow-sm">
      <div className="mx-auto mb-5 flex max-w-xl items-center justify-center">
        <div className="rounded-3xl border border-blue-200 bg-blue-600 px-6 py-4 text-center text-white shadow-lg shadow-blue-100">
          <p className="text-xs font-medium uppercase tracking-wide text-blue-100">
            {language === "fr"
              ? "Sujet principal"
              : language === "ar"
              ? "الموضوع الرئيسي"
              : "Main topic"}
          </p>
          <h3 className="mt-1 text-lg font-bold leading-snug">{centerTitle}</h3>
        </div>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {blocks.map((block, index) => (
          <div
            key={`${block.title}-${index}`}
            className="relative rounded-2xl border border-slate-200 bg-white p-4 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md"
          >
            <div className="mb-3 flex items-center gap-3">
              <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-2xl bg-blue-50 text-sm font-bold text-blue-700 ring-1 ring-blue-100">
                {index + 1}
              </div>
              <h4 className="font-semibold leading-snug text-slate-900">
                {block.title ||
                  (language === "fr"
                    ? "Idée clé"
                    : language === "ar"
                    ? "فكرة أساسية"
                    : "Key idea")}
              </h4>
            </div>

            {block.items.length > 0 && (
              <div className="space-y-2">
                {block.items.slice(0, 4).map((item, itemIndex) => (
                  <div
                    key={`${item}-${itemIndex}`}
                    className="flex items-start gap-2 rounded-xl bg-slate-50 px-3 py-2 text-sm text-slate-700"
                  >
                    <span className="mt-1 h-2 w-2 shrink-0 rounded-full bg-blue-400" />
                    <span className="leading-relaxed">{item}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

function MermaidDiagram({
  chart,
  onNodeClick,
  selectedLabel,
  language = "en",
}: {
  chart: string;
  onNodeClick?: (label: string) => void;
  selectedLabel?: string | null;
  language?: string;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const viewportRef = useRef<HTMLDivElement>(null);
  const overlayRef = useRef<HTMLDivElement>(null);
  const lastActivationRef = useRef<{ label: string; time: number } | null>(null);
  const [focusMode, setFocusMode] = useState(false);
  const [zoom, setZoom] = useState(1);

  const ui = {
    tip:
      language === "fr"
        ? "Astuce : cliquez sur un nœud pour voir son explication. Utilisez les boutons pour zoomer."
        : language === "ar"
        ? "نصيحة: اضغط على أي عقدة لعرض شرحها. استخدم الأزرار للتكبير."
        : "Tip: click a node to see its explanation. Use the buttons to zoom.",
    zoomIn: language === "fr" ? "Zoom +" : language === "ar" ? "تكبير +" : "Zoom +",
    zoomOut: language === "fr" ? "Zoom -" : language === "ar" ? "تصغير -" : "Zoom -",
    reset:
      language === "fr" ? "Réinitialiser" : language === "ar" ? "إعادة ضبط" : "Reset",
    focusOn:
      language === "fr" ? "Focus activé" : language === "ar" ? "التركيز مفعل" : "Focus on",
    focusOff:
      language === "fr" ? "Focus désactivé" : language === "ar" ? "التركيز معطل" : "Focus off",
  };

  const getLabelFromElement = (element: Element | null) => {
    return (element?.textContent || "").replace(/\s+/g, " ").trim();
  };

  const getClickableLabelElements = () => {
    if (!ref.current) return [] as Element[];

    const candidates = Array.from(
      ref.current.querySelectorAll(
        "svg text, svg foreignObject, svg g[class*='mindmap'] text, svg g[class*='node'] text"
      )
    ) as Element[];

    const seen = new Set<string>();

    return candidates.filter((element) => {
      const label = getLabelFromElement(element);
      if (!label) return false;

      const normalized = normalizeExplanationKey(label);
      if (!normalized || seen.has(normalized)) return false;

      const box = element.getBoundingClientRect();
      if (!box.width && !box.height) return false;

      seen.add(normalized);
      return true;
    });
  };

  const clearHighlights = () => {
    if (!ref.current) return;

    ref.current
      .querySelectorAll(".runexa-diagram-active")
      .forEach((el) => el.classList.remove("runexa-diagram-active"));

    ref.current
      .querySelectorAll(".runexa-diagram-active-text")
      .forEach((el) => el.classList.remove("runexa-diagram-active-text"));

    ref.current.querySelectorAll("svg text, svg foreignObject").forEach((el) => {
      const svgElement = el as SVGElement;
      svgElement.style.fill = "";
      svgElement.style.fontWeight = "";
      svgElement.style.textDecoration = "";
    });

    ref.current
      .querySelectorAll("rect, polygon, circle, ellipse, path")
      .forEach((shape) => {
        const svgShape = shape as SVGElement;
        svgShape.style.stroke = "";
        svgShape.style.strokeWidth = "";
        svgShape.style.opacity = "";
        svgShape.style.filter = "";
      });
  };

  const applyHighlight = (element: Element, label: string) => {
    clearHighlights();

    const group = element.closest("g") || element;

    group.classList.add("runexa-diagram-active");
    element.classList.add("runexa-diagram-active-text");

    const svgElement = element as SVGElement;
    svgElement.style.fill = "#2563eb";
    svgElement.style.fontWeight = "900";
    svgElement.style.textDecoration = "underline";

    group.querySelectorAll("rect, polygon, circle, ellipse, path").forEach((shape) => {
      const svgShape = shape as SVGElement;
      svgShape.style.stroke = "#2563eb";
      svgShape.style.strokeWidth = "3px";
      svgShape.style.opacity = "1";
      svgShape.style.filter = "drop-shadow(0 8px 18px rgba(37, 99, 235, 0.28))";
    });

    onNodeClick?.(label);
  };

  const activateLabel = (label: string) => {
    const cleanLabel = String(label || "").replace(/\s+/g, " ").trim();
    if (!cleanLabel) return;

    const now = Date.now();
    const last = lastActivationRef.current;

    if (last && last.label === cleanLabel && now - last.time < 200) {
      return;
    }

    lastActivationRef.current = { label: cleanLabel, time: now };

    const normalizedLabel = normalizeExplanationKey(cleanLabel);
    const element = getClickableLabelElements().find(
      (candidate) => normalizeExplanationKey(getLabelFromElement(candidate)) === normalizedLabel
    );

    if (element) {
      applyHighlight(element, cleanLabel);
    } else {
      onNodeClick?.(cleanLabel);
    }
  };

  const getNearestLabelFromPoint = (clientX: number, clientY: number) => {
    const elements = getClickableLabelElements();

    let nearestLabel = "";
    let nearestDistance = Number.POSITIVE_INFINITY;

    for (const element of elements) {
      const box = element.getBoundingClientRect();

      if (!box.width && !box.height) continue;

      const centerX = box.left + box.width / 2;
      const centerY = box.top + box.height / 2;
      const distance = Math.hypot(clientX - centerX, clientY - centerY);

      if (distance < nearestDistance) {
        nearestDistance = distance;
        nearestLabel = getLabelFromElement(element);
      }
    }

    return nearestDistance <= 120 ? nearestLabel : "";
  };

  const rebuildHtmlOverlay = () => {
    if (!viewportRef.current || !overlayRef.current) return;

    overlayRef.current.innerHTML = "";

    const viewportBox = viewportRef.current.getBoundingClientRect();
    const elements = getClickableLabelElements();

    elements.forEach((element) => {
      const label = getLabelFromElement(element);
      if (!label) return;

      const box = element.getBoundingClientRect();
      if (!box.width && !box.height) return;

      const button = document.createElement("button");
      button.type = "button";
      button.setAttribute("aria-label", label);
      button.setAttribute("title", label);
      button.style.position = "absolute";
      button.style.left = `${box.left - viewportBox.left - 12}px`;
      button.style.top = `${box.top - viewportBox.top - 10}px`;
      button.style.width = `${Math.max(box.width + 24, 48)}px`;
      button.style.height = `${Math.max(box.height + 20, 32)}px`;
      button.style.background = "transparent";
      button.style.border = "0";
      button.style.padding = "0";
      button.style.margin = "0";
      button.style.cursor = "pointer";
      button.style.pointerEvents = "auto";
      button.style.zIndex = "20";

      const trigger = (event: Event) => {
        event.preventDefault();
        event.stopPropagation();
        activateLabel(label);
      };

      button.addEventListener("click", trigger, true);
      button.addEventListener("pointerdown", trigger, true);
      button.addEventListener("pointerup", trigger, true);

      overlayRef.current?.appendChild(button);
    });
  };

  const handleViewportClick = (event: React.MouseEvent<HTMLDivElement>) => {
    const label = getNearestLabelFromPoint(event.clientX, event.clientY);

    if (!label) return;

    event.preventDefault();
    event.stopPropagation();
    activateLabel(label);
  };

  useEffect(() => {
    let cancelled = false;
    let resizeObserver: ResizeObserver | null = null;

    const renderDiagram = async () => {
      if (!ref.current) return;

      if (!chart) {
        ref.current.innerHTML =
          "<div class='animate-pulse h-40 bg-slate-100 rounded-xl'></div>";
        return;
      }

      try {
        const mermaid = (await import("mermaid")).default;

        mermaid.initialize({
          startOnLoad: false,
          theme: "default",
          securityLevel: "loose",
        });

        const safeChart = isValidMermaid(chart) ? chart : fallbackDiagram();
        const id = `mermaid-${Date.now()}-${Math.random()
          .toString(36)
          .slice(2)}`;

        const { svg } = await mermaid.render(id, safeChart);

        if (!cancelled && ref.current) {
          ref.current.innerHTML = svg;

          const svgElement = ref.current.querySelector("svg") as SVGSVGElement | null;

          if (svgElement) {
            svgElement.style.maxWidth = "none";
            svgElement.style.width = "max-content";
            svgElement.style.minWidth = "100%";
            svgElement.style.height = "auto";
            svgElement.style.cursor = "default";
            svgElement.style.pointerEvents = "none";
            svgElement.style.transformOrigin = "0 0";
            svgElement.style.transform = `scale(${zoom})`;
          }

          getClickableLabelElements().forEach((element) => {
            element.classList.add("runexa-diagram-text");
            (element as SVGElement).style.cursor = "pointer";
          });

          window.setTimeout(rebuildHtmlOverlay, 80);

          if (viewportRef.current) {
            resizeObserver = new ResizeObserver(() => rebuildHtmlOverlay());
            resizeObserver.observe(viewportRef.current);
          }
        }
      } catch (error) {
        console.error("Mermaid render error:", error);

        try {
          const mermaid = (await import("mermaid")).default;
          const fallbackId = `mermaid-fallback-${Date.now()}-${Math.random()
            .toString(36)
            .slice(2)}`;

          const { svg } = await mermaid.render(fallbackId, fallbackDiagram());

          if (!cancelled && ref.current) {
            ref.current.innerHTML = svg;
            window.setTimeout(rebuildHtmlOverlay, 80);
          }
        } catch {
          if (!cancelled && ref.current) {
            ref.current.innerHTML =
              "<p style='color:#64748b;font-size:14px'>Diagram unavailable</p>";
          }
        }
      }
    };

    renderDiagram();

    return () => {
      cancelled = true;

      if (resizeObserver) {
        resizeObserver.disconnect();
      }
    };
  }, [chart]);

  useEffect(() => {
    const svgElement = ref.current?.querySelector("svg") as SVGSVGElement | null;

    if (svgElement) {
      svgElement.style.transform = `scale(${zoom})`;
    }

    window.setTimeout(rebuildHtmlOverlay, 80);
  }, [zoom]);

  useEffect(() => {
    if (!selectedLabel) return;
    activateLabel(selectedLabel);
  }, [selectedLabel]);

  return (
    <div className="rounded-2xl border bg-white p-4 shadow-sm">
      <div className="mb-3 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <p className="text-xs text-slate-500">{ui.tip}</p>

        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={() => setZoom((value) => Math.min(value + 0.25, 4))}
            className="rounded-lg border px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50"
          >
            {ui.zoomIn}
          </button>

          <button
            type="button"
            onClick={() => setZoom((value) => Math.max(value - 0.25, 0.45))}
            className="rounded-lg border px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50"
          >
            {ui.zoomOut}
          </button>

          <button
            type="button"
            onClick={() => setZoom(1)}
            className="rounded-lg border px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50"
          >
            {ui.reset}
          </button>

          <button
            type="button"
            onClick={() => setFocusMode((prev) => !prev)}
            className={`rounded-lg border px-3 py-1.5 text-xs font-medium transition ${
              focusMode
                ? "border-blue-300 bg-blue-50 text-blue-700"
                : "text-slate-700 hover:bg-slate-50"
            }`}
          >
            {focusMode ? ui.focusOn : ui.focusOff}
          </button>
        </div>
      </div>

      <div
        ref={viewportRef}
        onClick={handleViewportClick}
        className={`runexa-diagram-viewport relative min-h-[360px] overflow-auto rounded-xl border bg-slate-50 p-4 ${
          focusMode ? "runexa-focus-mode" : ""
        }`}
      >
        <div ref={ref} className="runexa-diagram-canvas min-w-full" />
        <div
          ref={overlayRef}
          className="absolute inset-0 z-20 pointer-events-none"
        />
      </div>

      <style>{`
        .runexa-diagram-viewport {
          cursor: default;
          user-select: none;
        }

        .runexa-diagram-viewport svg {
          transition: transform 180ms ease;
          transform-origin: 0 0;
        }

        .runexa-diagram-viewport svg,
        .runexa-diagram-viewport svg * {
          pointer-events: none !important;
        }

        .runexa-diagram-text {
          transition: fill 160ms ease, opacity 160ms ease, font-weight 160ms ease;
        }

        .runexa-diagram-active-text {
          fill: #2563eb !important;
          font-weight: 900 !important;
          text-decoration: underline;
        }

        .runexa-diagram-active rect,
        .runexa-diagram-active polygon,
        .runexa-diagram-active circle,
        .runexa-diagram-active ellipse,
        .runexa-diagram-active path {
          stroke: #2563eb !important;
          stroke-width: 3px !important;
          filter: drop-shadow(0 8px 18px rgba(37, 99, 235, 0.28));
        }

        .runexa-focus-mode .runexa-diagram-text {
          opacity: 0.28;
        }

        .runexa-focus-mode .runexa-diagram-active-text {
          opacity: 1;
        }
      `}</style>
    </div>
  );
}

function resolveAudioUrl(payload: any): string {
  const result = payload?.result;

  if (typeof payload?.audio_url === "string") {
    return payload.audio_url;
  }

  if (typeof result?.audio_url === "string") {
    return result.audio_url;
  }

  if (typeof result?.audio_path === "string") {
    return result.audio_path;
  }

  if (typeof result?.audio_path?.audio_url === "string") {
    return result.audio_path.audio_url;
  }

  if (typeof result === "string") {
    try {
      const parsed = JSON.parse(result);
      return resolveAudioUrl({ result: parsed });
    } catch {
      return "";
    }
  }

  return "";
}


export default function StudyPage() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [startTime, setStartTime] = useState<number | null>(null);
  const [elapsed, setElapsed] = useState(0);
  const [remaining, setRemaining] = useState(90);
  const [loadingStep, setLoadingStep] = useState("");
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [paymentMessage, setPaymentMessage] = useState("");
  const [showLevelModal, setShowLevelModal] = useState(false);
  const [educationLevel, setEducationLevel] = useState("");
  const [language, setLanguage] = useState("en");
  const [selectedAnswers, setSelectedAnswers] = useState<Record<string, string>>(
    {}
  );
  const [quizSubmitted, setQuizSubmitted] = useState(false);
  const [retryCount, setRetryCount] = useState(0);
  const [selectedNode, setSelectedNode] = useState<string | null>(null);
  const [audioLoading, setAudioLoading] = useState(false);
  const [audioUrl, setAudioUrl] = useState("");
  const [userPlan, setUserPlan] = useState("trial");
  const [userRole, setUserRole] = useState("user");
  const [creditsBalance, setCreditsBalance] = useState(0);

  const t = labels[language] || labels.en;

  const hasCredits = creditsBalance > 0;

  const hasActiveAccess =
    userRole === "admin" ||
    userRole === "enterprise_admin" ||
    userRole === "enterprise_member" ||
    userPlan === "paid" ||
    userPlan === "pro" ||
    userPlan === "premium" ||
    hasCredits;

  const primaryCtaLabel = hasActiveAccess
    ? t.analyze
    : t.startTrial;

  const featureStyles = [
    {
      icon: "from-blue-700 to-sky-500",
      glow: "shadow-blue-200",
      accent: "from-blue-600 to-sky-400",
      hover: "hover:border-blue-200 hover:bg-blue-50/40",
    },
    {
      icon: "from-cyan-700 to-teal-500",
      glow: "shadow-cyan-200",
      accent: "from-cyan-600 to-teal-400",
      hover: "hover:border-cyan-200 hover:bg-cyan-50/40",
    },
    {
      icon: "from-indigo-700 to-violet-500",
      glow: "shadow-indigo-200",
      accent: "from-indigo-600 to-violet-400",
      hover: "hover:border-indigo-200 hover:bg-indigo-50/40",
    },
    {
      icon: "from-emerald-700 to-green-500",
      glow: "shadow-emerald-200",
      accent: "from-emerald-600 to-green-400",
      hover: "hover:border-emerald-200 hover:bg-emerald-50/40",
    },
    {
      icon: "from-slate-800 to-slate-600",
      glow: "shadow-slate-200",
      accent: "from-slate-700 to-slate-400",
      hover: "hover:border-slate-300 hover:bg-slate-50",
    },
    {
      icon: "from-green-700 to-lime-500",
      glow: "shadow-green-200",
      accent: "from-green-600 to-lime-400",
      hover: "hover:border-green-200 hover:bg-green-50/40",
    },
    {
      icon: "from-amber-700 to-orange-500",
      glow: "shadow-amber-200",
      accent: "from-amber-600 to-orange-400",
      hover: "hover:border-amber-200 hover:bg-amber-50/40",
    },
    {
      icon: "from-purple-700 to-fuchsia-500",
      glow: "shadow-purple-200",
      accent: "from-purple-600 to-fuchsia-400",
      hover: "hover:border-purple-200 hover:bg-purple-50/40",
    },
    {
      icon: "from-rose-700 to-pink-500",
      glow: "shadow-rose-200",
      accent: "from-rose-600 to-pink-400",
      hover: "hover:border-rose-200 hover:bg-rose-50/40",
    },
    {
      icon: "from-violet-700 to-indigo-500",
      glow: "shadow-violet-200",
      accent: "from-violet-600 to-indigo-400",
      hover: "hover:border-violet-200 hover:bg-violet-50/40",
    },
    {
      icon: "from-teal-700 to-cyan-500",
      glow: "shadow-teal-200",
      accent: "from-teal-600 to-cyan-400",
      hover: "hover:border-teal-200 hover:bg-teal-50/40",
    },
  ];

  useEffect(() => {
    setLanguage(getSavedLocale());

    const syncBillingState = () => {
      setUserPlan(
        (safeGetLocalStorage("plan", "trial"))
          .toLowerCase()
          .trim()
      );

      setUserRole(
        (safeGetLocalStorage("role", "user"))
          .toLowerCase()
          .trim()
      );

      setCreditsBalance(
        Number(safeGetLocalStorage("credits_balance", "0"))
      );
    };

    syncBillingState();
    refreshUserBilling();

    window.addEventListener("storage", syncBillingState);

    return () => {
      window.removeEventListener("storage", syncBillingState);
    };
  }, []);

  useEffect(() => {
    return () => {
      setAudioUrl("");
    };
  }, []);

  useEffect(() => {
    if (!loading || !startTime) return;

    const interval = setInterval(() => {
      const elapsedSec = Math.floor((Date.now() - startTime) / 1000);
      setElapsed(elapsedSec);
      setRemaining(Math.max(90 - elapsedSec, 0));
    }, 1000);

    return () => clearInterval(interval);
  }, [loading, startTime]);

  useEffect(() => {
    if (!loading) return;

    const timers = [
      setTimeout(() => {
        setLoadingStep(t.loadingSteps.extracting);
        setLoadingProgress(15);
      }, 0),
      setTimeout(() => {
        setLoadingStep(t.loadingSteps.summary);
        setLoadingProgress(40);
      }, 15000),
      setTimeout(() => {
        setLoadingStep(t.loadingSteps.quiz);
        setLoadingProgress(70);
      }, 35000),
      setTimeout(() => {
        setLoadingStep(t.loadingSteps.finalizing);
        setLoadingProgress(90);
      }, 60000),
    ];

    return () => timers.forEach(clearTimeout);
  }, [loading, language, t.loadingSteps]);

  const diagramTitle = result ? extractDiagramTitle(result, language) : "";

  const fixedDiagram = result?.visual_diagram
    ? replaceRootLabel(result.visual_diagram, diagramTitle)
    : "";

  const fixedDiagramExplanations = buildDiagramExplanationsForFixedRoot(
    result?.diagram_explanations,
    diagramTitle,
    language
  );

  const selectedNodeExplanation = findDiagramExplanation(
    fixedDiagramExplanations,
    selectedNode
  );

  const getLevelLabel = (level: string) =>
    LEVEL_LABELS[language]?.[level] || LEVEL_LABELS.en[level] || level;

  const refreshUserBilling = async () => {
    const token = getToken?.() || safeGetLocalStorage("token");

    if (!token) return;

    const res = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/users/me`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!res.ok) return;

    const data = await res.json();

    const nextPlan = String(data.plan || "trial")
      .toLowerCase()
      .trim();

    const nextRole = String(data.role || "user")
      .toLowerCase()
      .trim();

    const nextCreditsBalance = Number(data.credits_balance || 0);

    safeSetLocalStorage(
      "credits_balance",
      String(nextCreditsBalance)
    );

    safeSetLocalStorage("plan", nextPlan);
    safeSetLocalStorage("role", nextRole);

    setUserPlan(nextPlan);
    setUserRole(nextRole);
    setCreditsBalance(nextCreditsBalance);

    window.dispatchEvent(new Event("storage"));
  };

  const handleAnalyze = async () => {
    if (!file || !educationLevel) return;

    setLoading(true);
    setStartTime(Date.now());
    setElapsed(0);
    setRemaining(180);
    setLoadingStep(t.loadingSteps.extracting);
    setLoadingProgress(15);
    setShowLevelModal(false);
    setResult(null);
    setPaymentMessage("");
    setSelectedAnswers({});
    setQuizSubmitted(false);
    setRetryCount(0);
    setSelectedNode(null);
    stopAudio();

    const formData = new FormData();
    formData.append("file", file);
    formData.append("education_level", educationLevel);
    formData.append("output_language", language);

    try {
      const token = getToken();

      if (!token) {
        throw new Error(
          "You must be logged in to analyze documents."
        );
      }

      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/study/analyze`,
        {
          method: "POST",
          headers: token ? { Authorization: `Bearer ${token}` } : {},
          body: formData,
        }
      );

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Study analysis failed.");
      }

      if (!data.job_id) {
        setResult(data);

        await refreshUserBilling();

        return;
      }

      const jobId = data.job_id;

      let attempts = 0;
      let completed = false;

      while (attempts < 90 && !completed) {
        await new Promise((resolve) => setTimeout(resolve, 2000));

        const statusRes = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/jobs/${jobId}`,
          {
            headers: token ? { Authorization: `Bearer ${token}` } : {},
          }
        );

        if (!statusRes.ok) {
          const errorData = await statusRes.json().catch(() => ({}));

          throw new Error(
            errorData.detail || "Could not check job status"
          );
        }

        const statusData = await statusRes.json();

        if (typeof statusData.progress === "number") {
          setLoadingProgress(statusData.progress);
        }

        if (statusData.status_message) {
          setLoadingStep(statusData.status_message);
        }

        if (statusData.status === "running" && !statusData.status_message) {
          setLoadingStep(t.loadingSteps.summary);
          setLoadingProgress(45);
        }

        if (statusData.status === "completed") {
          setResult(statusData.result);

          await refreshUserBilling();

          setLoadingProgress(100);
          completed = true;
        }

        if (statusData.status === "failed") {
          throw new Error(statusData.error || "Study analysis failed.");
        }

        attempts++;
      }

      if (!completed) {
        throw new Error("Study analysis timeout.");
      }
    } catch (error) {
      console.error("Study analysis error:", error);

      const errorMessage =
        error instanceof Error ? error.message : t.errorMessage;

      if (errorMessage.includes("Trial already used")) {
        setPaymentMessage(t.trialUsed);
      } else if (errorMessage.includes("$1 trial payment required")) {
        setPaymentMessage(t.paymentRequired);
      } else {
        setPaymentMessage(errorMessage);
      }

      setResult({
        detail: errorMessage,
      });
    } finally {
      setLoadingStep("");
      setLoading(false);
      setStartTime(null);
    }
  };

  const theoryQuestions = result?.theoretical_quiz || [];
  const practiceQuestions = result?.practical_quiz || [];
  const allQuestions = [
    ...theoryQuestions.map((q: any, index: number) => ({
      ...q,
      type: "theory",
      key: `theory-${index}`,
    })),
    ...practiceQuestions.map((q: any, index: number) => ({
      ...q,
      type: "practice",
      key: `practice-${index}`,
    })),
  ];

  const totalQuestions = allQuestions.length;

  const correctAnswers = allQuestions.filter((q: any) => {
    return selectedAnswers[q.key] === q.correct_answer;
  }).length;

  const score =
    totalQuestions > 0 ? Math.round((correctAnswers / totalQuestions) * 100) : 0;

  const getScoreColor = () => {
    if (score >= 80) return "bg-green-50 text-green-700 border-green-200";
    if (score >= 50) return "bg-yellow-50 text-yellow-700 border-yellow-200";
    return "bg-red-50 text-red-700 border-red-200";
  };

  const getScoreFeedback = () => {
    if (score >= 80) {
      if (language === "fr")
        return "Excellent travail. Vous avez bien compris le contenu.";
      if (language === "ar") return "عمل ممتاز. لقد فهمت المحتوى جيداً.";
      return "Excellent work. You understood the material well.";
    }

    if (score >= 50) {
      if (language === "fr")
        return "Bon effort. Relisez les explications puis réessayez.";
      if (language === "ar") return "مجهود جيد. راجع الشروحات ثم أعد المحاولة.";
      return "Good effort. Review the explanations and retry.";
    }

    if (language === "fr")
      return "Vous avez besoin de plus de pratique. Concentrez-vous sur les points clés et les flashcards.";
    if (language === "ar")
      return "تحتاج إلى المزيد من التدريب. ركز على النقاط الأساسية وبطاقات المراجعة.";
    return "Needs more practice. Focus on the key points and flashcards.";
  };

  const getQualityColor = (quality: any) => {
    const qualityScore = Number(quality?.score || 0);

    if (qualityScore >= 90) return "bg-green-50 text-green-700 border-green-200";
    if (qualityScore >= 80) return "bg-blue-50 text-blue-700 border-blue-200";
    if (qualityScore >= 60) return "bg-yellow-50 text-yellow-700 border-yellow-200";
    return "bg-red-50 text-red-700 border-red-200";
  };

  const getQualityLabel = (quality: any) => {
    if (!quality) return "";

    const qualityScore = Number(quality?.score || 0);

    if (quality?.valid) {
      if (language === "fr") return `Validé (${qualityScore}/100)`;
      if (language === "ar") return `تم التحقق (${qualityScore}/100)`;
      return `Validated (${qualityScore}/100)`;
    }

    if (language === "fr") return `À revoir (${qualityScore}/100)`;
    if (language === "ar") return `يحتاج مراجعة (${qualityScore}/100)`;
    return `Needs review (${qualityScore}/100)`;
  };

  const getVisibleQualityErrors = (errors: any) => {
    if (!Array.isArray(errors)) return [];

    const hiddenPatterns = [
      "Study task should start with an action verb",
      "Duplicate flashcard front",
      "duplicate questions",
      "missing focus",
      "must contain exactly",
      "must have exactly",
      "should contain exactly",
      "invalid study task content",
      "visual_summary.key_points should contain",
    ];

    return errors.filter((error: string) => {
      const cleanError = String(error || "").trim();

      if (!cleanError) return false;

      return !hiddenPatterns.some((pattern) =>
        cleanError.toLowerCase().includes(pattern.toLowerCase())
      );
    });
  };

  const handleNodeClick = useCallback((label: string) => {
    setSelectedNode(label);
  }, []);

  const handleRetryQuiz = () => {
    if (retryCount >= 2) return;

    setSelectedAnswers({});
    setQuizSubmitted(false);
    setRetryCount((prev) => prev + 1);
  };

  const handleSelectAnswer = (key: string, answer: string) => {
    if (quizSubmitted) return;

    setSelectedAnswers((prev) => ({
      ...prev,
      [key]: answer,
    }));
  };

  const generateAudio = async (text: string) => {
    if (!text) return;

    setAudioLoading(true);

    try {
      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
        setAudioUrl("");
      }

      const token = getToken();

      // 1. CREATE AUDIO JOB
      const createRes = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/study/audio`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            ...(token ? { Authorization: `Bearer ${token}` } : {}),
          },
          body: JSON.stringify({
            text,
            language,
          }),
        }
      );

      if (!createRes.ok) {
        throw new Error("Failed to create audio job");
      }

      const createData = await createRes.json();

      const jobId = createData.job_id;

      if (!jobId) {
        throw new Error("Missing job ID");
      }

      // 2. POLLING
      let attempts = 0;
      let completed = false;

      while (attempts < 60 && !completed) {
        await new Promise((resolve) => setTimeout(resolve, 2000));

        const statusRes = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/jobs/${jobId}`,
          {
            headers: token
              ? { Authorization: `Bearer ${token}` }
              : {},
          }
        );

        if (!statusRes.ok) {
          attempts++;
          continue;
        }

        const statusData = await statusRes.json();

        if (statusData.status === "completed") {
          const resolvedAudioUrl = resolveAudioUrl(statusData);

          if (!resolvedAudioUrl) {
            console.error("Missing audio URL payload:", statusData);
            throw new Error("Missing audio URL");
          }

          setAudioUrl(resolvedAudioUrl);

          completed = true;
        }

        if (statusData.status === "failed") {
          throw new Error(statusData.error || "Audio job failed");
        }

        attempts++;
      }

      if (!completed) {
        throw new Error("Audio generation timeout");
      }
    } catch (error) {
      console.error("Audio error:", error);
    } finally {
      setAudioLoading(false);
    }
  };

  const stopAudio = () => {
    setAudioUrl("");
  };

  const handleSubmitQuiz = () => {
    if (Object.keys(selectedAnswers).length < totalQuestions) return;

    setQuizSubmitted(true);

    const answersPayload = allQuestions.map((q: any) => ({
      question: q.question,
      concept: q.question,
      selected_answer: selectedAnswers[q.key],
      correct_answer: q.correct_answer,
      is_correct: selectedAnswers[q.key] === q.correct_answer,
      type: q.type,
    }));

    fetch(`${process.env.NEXT_PUBLIC_API_URL}/study/attempt`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${getToken()}`,
      },
      body: JSON.stringify({
        document_hash: result?.document_hash || null,
        language,
        education_level: educationLevel,
        score,
        total_questions: totalQuestions,
        correct_answers: correctAnswers,
        answers: answersPayload,
      }),
    }).catch((error) => {
      console.error("Failed to save study attempt:", error);
    });
  };

  const renderQuestion = (q: any, i: number, type: "theory" | "practice") => {
    const key = `${type}-${i}`;
    const selected = selectedAnswers[key];
    const isCorrect = selected === q.correct_answer;

    return (
      <div
        key={key}
        dir={language === "ar" ? "rtl" : "ltr"}
        className="mt-3 rounded-xl border p-4 bg-white"
      >
        <p className={`${language === "ar" ? "text-right" : "text-left"} font-medium`}>
          {i + 1}. {q.question}
        </p>

        <div className="grid gap-2 mt-3">
          {q.options.map((opt: string, j: number) => {
            const optionLetter = ["A", "B", "C", "D"][j];

            const isSelected = selected === optionLetter;
            const isRightAnswer = quizSubmitted && optionLetter === q.correct_answer;
            const isWrongSelected =
             quizSubmitted && isSelected && optionLetter !== q.correct_answer;
            return (
              <button
                key={j}
                type="button"
                onClick={() => handleSelectAnswer(key, optionLetter)}
                className={`${
                  language === "ar" ? "text-right" : "text-left"
                } rounded-xl border px-4 py-2 text-sm transition ${
                  isRightAnswer
                    ? "bg-green-50 border-green-300 text-green-700"
                    : isWrongSelected
                    ? "bg-red-50 border-red-300 text-red-700"
                    : isSelected
                    ? "bg-blue-50 border-blue-300 text-blue-700"
                    : "bg-slate-50 hover:bg-slate-100"
                }`}
              >
                {opt}
              </button>
            );
          })}
        </div>

        {quizSubmitted && selected && (
          <div className="mt-3 text-sm">
            <p
              className={
                isCorrect
                  ? "text-green-600 font-medium"
                  : "text-red-600 font-medium"
              }
            >
              {isCorrect ? t.correct : t.incorrect} — {t.answer}:{" "}
              {q.correct_answer}
            </p>
            <p className="text-slate-500 mt-1">{q.explanation}</p>
          </div>
        )}
      </div>
    );
  };

  return (
    <main
      dir={language === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-4 py-10"
    >
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold">{t.title}</h1>
          <p className="text-slate-500 mt-2">{t.subtitle}</p>
        </div>

        <div className="bg-white p-6 rounded-2xl border space-y-4">
          <div className="rounded-xl bg-slate-50 border border-slate-200 p-4 text-sm text-slate-600 space-y-3">
            <p>
              <strong>{t.howTitle}</strong> {t.how1}
            </p>

            <p>{t.how2}</p>

            <div className="grid gap-3 sm:grid-cols-2">
              {t.items.map((item: string, index: number) => {
                const style = featureStyles[index] || featureStyles[0];

                return (
                  <div
                    key={index}
                    className={`group relative overflow-hidden rounded-2xl border border-slate-200/80 bg-white p-4 shadow-[0_1px_2px_rgba(15,23,42,0.06)] transition duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_40px_rgba(15,23,42,0.10)] ${style.hover}`}
                  >
                    <div
                      className={`absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent ${style.accent} to-transparent opacity-0 transition group-hover:opacity-100`}
                    />

                    <div
                      className={`flex items-start gap-3 ${
                        language === "ar" ? "text-right" : "text-left"
                      }`}
                    >
                      <span
                        className={`relative flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br ${style.icon} text-white shadow-sm ${style.glow} ring-1 ring-slate-900/5 transition group-hover:scale-105`}
                      >
                        <FeatureIcon index={index} />
                      </span>

                      <div className="min-w-0">
                        <p className="text-sm font-semibold leading-relaxed text-slate-900">
                          {item}
                        </p>
                        <div
                          className={`mt-2 h-1 w-10 rounded-full bg-gradient-to-r ${style.accent} opacity-70 transition group-hover:w-14`}
                        />
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>

            <p>{t.how3}</p>

            <p className="text-xs text-slate-500">{t.disclaimer}</p>
          </div>

          <select
            value={language}
            onChange={(e) => {
              stopAudio();
              setLanguage(e.target.value);
              setSavedLocale(e.target.value);
              setResult(null);
              setSelectedAnswers({});
              setQuizSubmitted(false);
              setRetryCount(0);
              setSelectedNode(null);
            }}
            className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
          >
            <option value="en">English</option>
            <option value="fr">Français</option>
            <option value="ar">العربية</option>
          </select>

          <div className="space-y-2">
            <input
              id="file-upload"
              type="file"
              accept=".pdf,.docx"
              onChange={(e) => {
                stopAudio();
                setFile(e.target.files?.[0] || null);
                setResult(null);
                setPaymentMessage("");
                setSelectedAnswers({});
                setQuizSubmitted(false);
                setEducationLevel("");
                setRetryCount(0);
                setSelectedNode(null);
              }}
              className="hidden"
            />

            <label
              htmlFor="file-upload"
              className="flex items-center justify-between cursor-pointer rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm hover:bg-slate-50"
            >
              <span className="text-slate-600">
                {file ? file.name : t.noFile}
              </span>

              <span className="text-blue-600 font-medium">
                {t.chooseFile}
              </span>
            </label>
          </div>

          {!hasActiveAccess && (
            <div className="rounded-xl border border-blue-100 bg-blue-50 p-3 text-sm text-blue-700">
              {t.trialInfo}
            </div>
          )}

          <p className="text-xs text-slate-500">
            {t.proDirect}
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <button
              onClick={() => {
                setResult(null);
                setSelectedAnswers({});
                setQuizSubmitted(false);
                setPaymentMessage("");
                setRetryCount(0);
                setSelectedNode(null);
                setShowLevelModal(true);
              }}
              disabled={!file || loading}
              className="flex w-full items-center justify-center gap-2 bg-slate-900 text-white py-3 rounded-xl disabled:bg-slate-400"
            >
              {loading ? (
                <>
                  <span className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
                  {t.loadingSteps.analyzing}
                </>
              ) : (
                primaryCtaLabel
              )}
            </button>

            <button
              onClick={() => setPaymentMessage(t.paymentMessage)}
              className="w-full bg-green-600 text-white py-3 rounded-xl hover:bg-green-700 transition"
            >
              {t.buyCredits}
            </button>
          </div>

          {loading && (
            <div className="mt-4 rounded-2xl border border-blue-100 bg-blue-50 p-4 text-center">
              <div className="flex items-center justify-between gap-3 text-sm">
                <span className="font-medium text-blue-700">{loadingStep}</span>
                <span className="text-blue-600">
                  {loadingProgress}%
                </span>
              </div>

              <div className="mt-3 h-2 bg-blue-100 rounded-full overflow-hidden">
                <div
                  className="h-full bg-blue-600 transition-all duration-700"
                  style={{
                    width: `${Math.max(
                      loadingProgress,
                      Math.min((elapsed / 90) * 100, 95)
                    )}%`,
                  }}
                />
              </div>

              <div className="mt-2 flex justify-between text-xs text-slate-500">
                <span>
                  ⏳ {remaining > 0 ? `${remaining}s ${t.remaining}` : t.loadingSteps.finalizing}
                </span>
                <span>{t.elapsed}: {elapsed}s</span>
              </div>
            </div>
          )}

          {paymentMessage && (
            <p className="text-sm text-amber-700 bg-amber-50 border border-amber-200 rounded-xl px-4 py-3">
              {paymentMessage}
            </p>
          )}
        </div>

        {showLevelModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4">
            <div className="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl space-y-4">
              <div>
                <h2 className="text-xl font-semibold">{t.selectLevel}</h2>
                <p className="text-sm text-slate-500 mt-1">{t.levelHelp}</p>
              </div>

              <select
                value={educationLevel}
                onChange={(e) => setEducationLevel(e.target.value)}
                className="w-full rounded-xl border border-slate-300 px-4 py-3 text-sm"
              >
                <option value="">{t.chooseLevel}</option>
                <option value="primary_school">
                  {getLevelLabel("primary_school")}
                </option>
                <option value="middle_school">
                  {getLevelLabel("middle_school")}
                </option>
                <option value="high_school">
                  {getLevelLabel("high_school")}
                </option>
                <option value="vocational_training">
                  {getLevelLabel("vocational_training")}
                </option>
                <option value="university">
                  {getLevelLabel("university")}
                </option>
              </select>

              <div className="grid grid-cols-2 gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setShowLevelModal(false)}
                  className="w-full rounded-xl border border-slate-300 py-3 text-slate-700 hover:bg-slate-50"
                >
                  {t.cancel}
                </button>

                <button
                  type="button"
                  onClick={handleAnalyze}
                  disabled={!educationLevel || loading}
                  className="w-full rounded-xl bg-slate-900 py-3 text-white disabled:bg-slate-400"
                >
                  {t.continue}
                </button>
              </div>
            </div>
          </div>
        )}

        {result?.detail && (
          <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-xl">
            {result.detail}
          </div>
        )}

        {result && result.summary && (
          <div className="bg-white p-6 rounded-2xl border space-y-6">
            <h2 className="text-xl font-semibold">{t.results}</h2>

            <div className="flex flex-wrap gap-2">
              {educationLevel && (
                <span className="inline-flex rounded-full bg-blue-50 px-3 py-1 text-xs font-medium text-blue-700 border border-blue-200">
                  {t.level}: {getLevelLabel(educationLevel)}
                </span>
              )}

              {language && (
                <span className="inline-flex rounded-full bg-slate-50 px-3 py-1 text-xs font-medium text-slate-700 border border-slate-200">
                  {t.language}:{" "}
                  {language === "en"
                    ? "English"
                    : language === "fr"
                    ? "Français"
                    : "العربية"}
                </span>
              )}

              {result.quality && (
                <span
                  className={`inline-flex rounded-full px-3 py-1 text-xs font-medium border ${getQualityColor(
                    result.quality
                  )}`}
                >
                  {t.qualityScore}: {Number(result.quality.score || 0)}/100
                </span>
              )}
            </div>

            {result.quality && (
              <section className={`rounded-2xl border p-4 ${getQualityColor(result.quality)}`}>
                <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
                  <strong>✅ {t.quality}</strong>
                  <span className="text-sm font-semibold">
                    {getQualityLabel(result.quality)}
                  </span>
                </div>

                {getVisibleQualityErrors(result.quality.errors).length > 0 && (
                  <ul className="mt-3 list-disc space-y-1 text-sm ml-6">
                    {getVisibleQualityErrors(result.quality.errors).map(
                      (error: string, index: number) => (
                        <li key={index}>{error}</li>
                      )
                    )}
                  </ul>
                )}

                {getVisibleQualityErrors(result.quality.errors).length === 0 && (
                  <p className="mt-2 text-sm">
                    {language === "fr"
                      ? "La sortie est complète et respecte les règles de qualité."
                      : language === "ar"
                      ? "النتيجة كاملة وتحترم قواعد الجودة."
                      : "The output is complete and passes the quality rules."}
                  </p>
                )}
              </section>
            )}

            <div>
              <strong>{t.summary}:</strong>
              <p className="text-slate-600 mt-1">{result.summary}</p>
            </div>

            {result.detailed_summary && (
              <div>
                <strong>🧾 {t.writtenSummary}:</strong>
                <p className="text-slate-600 mt-1 leading-relaxed">
                  {result.detailed_summary}
                </p>

                <div className="mt-3 flex flex-wrap items-center gap-2">
                  <button
                    type="button"
                    onClick={() => generateAudio(result.detailed_summary)}
                    disabled={audioLoading}
                    className="rounded-xl bg-blue-600 px-4 py-2 text-sm text-white disabled:bg-slate-400"
                  >
                    {audioLoading
                      ? language === "fr"
                        ? "Génération audio..."
                        : language === "ar"
                        ? "جاري إنشاء الصوت..."
                        : "Generating audio..."
                      : language === "fr"
                      ? "🔊 Écouter"
                      : language === "ar"
                      ? "🔊 استمع"
                      : "🔊 Listen"}
                  </button>

                  {audioUrl && (
                    <button
                      type="button"
                      onClick={stopAudio}
                      className="rounded-xl border px-4 py-2 text-sm text-slate-700"
                    >
                      {language === "fr"
                        ? "Arrêter"
                        : language === "ar"
                        ? "إيقاف"
                        : "Stop"}
                    </button>
                  )}
                </div>

                {audioUrl && (
                  <audio controls autoPlay className="mt-3 w-full">
                    <source src={audioUrl} type="audio/mpeg" />
                  </audio>
                )}
              </div>
            )}

            {result.visual_summary && (
              <div>
                <strong>📊 {t.visualSummary}:</strong>
                <VisualSummaryGraphic
                  value={result.visual_summary}
                  language={language}
                />
              </div>
            )}

            {result.visual_diagram && (
              <div>
                <strong>🧠 {t.visualDiagram}:</strong>
                <div className="mt-2">
                  <MermaidDiagram
                    chart={fixedDiagram}
                    onNodeClick={handleNodeClick}
                    selectedLabel={selectedNode}
                    language={language}
                  />
                </div>

                {selectedNode && (
                  <div className="mt-4 rounded-xl border border-blue-200 bg-blue-50 p-4">
                    <p className="text-xs font-medium uppercase tracking-wide text-blue-600">
                      {t.diagramExplanations}
                    </p>
                    <h4 className="mt-1 font-semibold text-slate-900">
                      {selectedNode}
                    </h4>
                    {selectedNodeExplanation ? (
                      <p className="mt-1 text-sm text-slate-700">
                        {selectedNodeExplanation}
                      </p>
                    ) : (
                      <p className="mt-1 text-sm text-slate-500">
                        {language === "fr"
                          ? "Aucune explication disponible pour ce nœud."
                          : language === "ar"
                          ? "لا يوجد شرح متاح لهذه العقدة."
                          : "No explanation available for this node."}
                      </p>
                    )}
                  </div>
                )}
              </div>
            )}

            <div>
              <strong>{t.keyPoints}:</strong>
              <ul className="list-disc ml-6">
                {result.key_points?.map((p: string, i: number) => (
                  <li key={i}>{p}</li>
                ))}
              </ul>
            </div>

            <div>
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                <strong>{t.quiz}:</strong>

                {quizSubmitted && Object.keys(selectedAnswers).length > 0 && (
                  <div
                    className={`rounded-xl border px-4 py-2 text-sm ${getScoreColor()}`}
                  >
                    {t.score}:{" "}
                    <strong>
                      {correctAnswers}/{totalQuestions} ({score}%)
                    </strong>
                  </div>
                )}
              </div>

              <div className="mt-4">
                <h3 className="font-semibold">{t.theory}</h3>
                {theoryQuestions.map((q: any, i: number) =>
                  renderQuestion(q, i, "theory")
                )}
              </div>

              <div className="mt-6">
                <h3 className="font-semibold">{t.practice}</h3>
                {practiceQuestions.map((q: any, i: number) =>
                  renderQuestion(q, i, "practice")
                )}
              </div>

              {totalQuestions > 0 && (
                <button
                  onClick={handleSubmitQuiz}
                  disabled={
                    quizSubmitted ||
                    Object.keys(selectedAnswers).length < totalQuestions
                  }
                  className="mt-5 w-full bg-blue-600 text-white py-3 rounded-xl disabled:bg-slate-400"
                >
                  {quizSubmitted
                    ? t.quizSubmitted
                    : Object.keys(selectedAnswers).length < totalQuestions
                    ? t.answerAll
                    : t.submitQuiz}
                </button>
              )}

              {quizSubmitted && (
                <div className="mt-4 rounded-xl border bg-slate-50 p-4 text-sm">
                  <p className="font-semibold">{t.learningFeedback}</p>
                  <p className="text-slate-600 mt-1">{getScoreFeedback()}</p>

                  <button
                    onClick={handleRetryQuiz}
                    disabled={retryCount >= 2}
                    className="mt-3 px-4 py-2 rounded-xl bg-slate-900 text-white text-sm disabled:bg-slate-400"
                  >
                    {retryCount >= 2 ? t.noRetries : t.retryQuiz}
                  </button>
                </div>
              )}
            </div>

            <div>
              <strong>{t.flashcards}:</strong>

              <div className="grid sm:grid-cols-2 gap-4 mt-3">
                {result.flashcards?.map((f: any, i: number) => (
                  <div key={i} className="border rounded-xl p-4 bg-slate-50">
                    <p className="text-sm text-slate-500 mb-1">{t.front}</p>
                    <p className="font-semibold">{f.front}</p>

                    <div className="mt-3 border-t pt-3">
                      <p className="text-sm text-slate-500 mb-1">{t.back}</p>
                      <p className="text-slate-700">{f.back}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <section>
              <strong>{t.studyPlan}:</strong>

              <ul className="mt-3 space-y-4">
                {result.study_plan?.map((day: any, i: number) => (
                  <li key={i} className="rounded-xl border bg-slate-50 p-4">
                    <p className="font-semibold text-slate-900">{day.day}</p>
                    <p className="mt-1 text-sm text-slate-600">{day.focus}</p>

                    <ul className="mt-3 list-disc ml-6 space-y-1 text-sm text-slate-700">
                      {day.tasks?.map((task: string, j: number) => (
                        <li key={j}>{task}</li>
                      ))}
                    </ul>
                  </li>
                ))}
              </ul>
            </section>

            <p className="text-xs text-slate-500 border-t pt-4">
              {result.disclaimer || t.disclaimer}
            </p>
          </div>
        )}
      </div>
    </main>
  );
}
