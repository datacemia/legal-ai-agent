"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { getToken } from "../../lib/auth";
import { getSavedLocale, setSavedLocale } from "../../lib/i18n";

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

const labels: any = {
  en: {
    title: "Study Agent",
    subtitle:
      "Upload a document to generate a summary, theoretical quiz, practical quiz, flashcards, and a study plan.",
    howTitle: "How this agent works:",
    how1:
      "Upload your study document (PDF, Word, or scanned document) and let the Study Agent transform it into an interactive learning experience.",
    how2:
      "Before analysis, you select your learning level and output language. The agent adapts the difficulty, vocabulary, explanations, and questions to match your level and language.",
    items: [
      "A clear and structured summary",
      "Key learning points",
      "Theoretical quiz (understanding)",
      "Practical quiz (real-world application)",
      "Flashcards for memorization",
      "A short study plan",
    ],
    how3:
      "You can answer the quiz directly, get instant feedback, explanations, and track your score.",
    disclaimer:
      "Results are for educational support only. Always verify important academic content with your teacher, course materials, or trusted sources.",
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
    correct: "Correct",
    incorrect: "Incorrect",
    answer: "Answer",
    paymentMessage:
      "Stripe is not configured yet. Credit purchase will be available soon.",
    errorMessage: "Failed to connect to Study Agent API.",
    noFile: "No file selected",
    chooseFile: "Choose a document (PDF, Word, or scanned)",
  },
  fr: {
    title: "Agent étude",
    subtitle:
      "Téléchargez un document pour générer un résumé, un quiz théorique, un quiz pratique, des flashcards et un plan de révision.",
    howTitle: "Comment fonctionne cet agent :",
    how1:
      "Téléchargez votre document de cours (PDF, Word ou document scanné) et laissez l’agent étude le transformer en une expérience d’apprentissage interactive.",
    how2:
      "Avant l’analyse, vous choisissez votre niveau et la langue de sortie. L’agent adapte la difficulté, le vocabulaire, les explications et les questions.",
    items: [
      "Un résumé clair et structuré",
      "Les points clés à retenir",
      "Un quiz théorique",
      "Un quiz pratique",
      "Des flashcards pour mémoriser",
      "Un court plan de révision",
    ],
    how3:
      "Vous pouvez répondre au quiz directement, recevoir un feedback instantané, des explications et suivre votre score.",
    disclaimer:
      "Les résultats sont fournis comme support éducatif uniquement. Vérifiez toujours les contenus importants avec vos supports de cours ou un enseignant.",
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
    correct: "Correct",
    incorrect: "Incorrect",
    answer: "Réponse",
    paymentMessage:
      "Stripe n’est pas encore configuré. L’achat de crédits sera bientôt disponible.",
    errorMessage: "Impossible de se connecter à l’API Study Agent.",
    noFile: "Aucun fichier sélectionné",
    chooseFile: "Choisir un document (PDF, Word ou scanné)",
  },
  ar: {
    title: "وكيل الدراسة",
    subtitle:
      "ارفع ملف دراسة لإنشاء ملخص، اختبار نظري، اختبار تطبيقي، بطاقات مراجعة وخطة دراسة.",
    howTitle: "كيف يعمل هذا الوكيل:",
    how1: "ارفع ملف دراستك (PDF أو Word أو ملف ممسوح ضوئياً) وسيحوّله وكيل الدراسة إلى تجربة تعلم تفاعلية.",
    how2:
      "قبل التحليل، اختر مستواك التعليمي ولغة النتائج. يقوم الوكيل بتكييف الصعوبة والمفردات والشرح والأسئلة حسب اختيارك.",
    items: [
      "ملخص واضح ومنظم",
      "النقاط الأساسية للتعلم",
      "اختبار نظري للفهم",
      "اختبار تطبيقي للاستخدام العملي",
      "بطاقات مراجعة للحفظ",
      "خطة دراسة قصيرة",
    ],
    how3:
      "يمكنك الإجابة على الاختبار مباشرة والحصول على تقييم فوري وشرح وتتبع نتيجتك.",
    disclaimer:
      "النتائج مخصصة للدعم التعليمي فقط. تحقق دائماً من المعلومات المهمة مع أستاذك أو مصادر الدورة.",
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
    correct: "صحيح",
    incorrect: "غير صحيح",
    answer: "الإجابة",
    paymentMessage:
      "Stripe غير مفعّل حالياً. شراء الرصيد سيكون متاحاً قريباً.",
    errorMessage: "تعذر الاتصال بواجهة Study Agent.",
    noFile: "لم يتم اختيار ملف (PDF أو Word أو ممسوح ضوئياً)",
    chooseFile: "اختيار ملف (PDF أو Word أو ممسوح ضوئياً)",
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

export default function StudyPage() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
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

  useEffect(() => {
    setLanguage(getSavedLocale());
  }, []);

  const t = labels[language] || labels.en;

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

  const handleAnalyze = async () => {
    if (!file || !educationLevel) return;

    setLoading(true);
    setShowLevelModal(false);
    setResult(null);
    setPaymentMessage("");
    setSelectedAnswers({});
    setQuizSubmitted(false);
    setRetryCount(0);
    setSelectedNode(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("education_level", educationLevel);
    formData.append("output_language", language);

    try {
      const token = getToken();

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
        setResult({
          detail: data.detail || "Study analysis failed.",
        });
      } else {
        setResult(data);
      }
    } catch (error) {
      console.error("Study analysis error:", error);
      setResult({
        detail: t.errorMessage,
      });
    } finally {
      setLoading(false);
    }
  };

  const theoryQuestions = result?.quiz?.theory_questions || [];
  const practiceQuestions = result?.quiz?.practice_questions || [];

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

  const handleSubmitQuiz = () => {
    if (Object.keys(selectedAnswers).length < totalQuestions) return;
    setQuizSubmitted(true);
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
            const isSelected = selected === opt;
            const isRightAnswer = quizSubmitted && opt === q.correct_answer;
            const isWrongSelected =
              quizSubmitted && isSelected && opt !== q.correct_answer;

            return (
              <button
                key={j}
                type="button"
                onClick={() => handleSelectAnswer(key, opt)}
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

            <ul className="list-disc ml-5 space-y-1">
              {t.items.map((item: string, index: number) => (
                <li key={index}>{item}</li>
              ))}
            </ul>

            <p>{t.how3}</p>

            <p className="text-xs text-slate-500">{t.disclaimer}</p>
          </div>

          <select
            value={language}
            onChange={(e) => {
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
              className="w-full bg-slate-900 text-white py-3 rounded-xl disabled:bg-slate-400"
            >
              {loading ? "Analyzing..." : t.analyze}
            </button>

            <button
              onClick={() => setPaymentMessage(t.paymentMessage)}
              className="w-full bg-green-600 text-white py-3 rounded-xl hover:bg-green-700 transition"
            >
              {t.buyCredits}
            </button>
          </div>

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
            </div>

            <div>
              <strong>{t.summary}:</strong>
              <p className="text-slate-600 mt-1">{result.summary}</p>
            </div>

            {result.written_summary && (
              <div>
                <strong>🧾 {t.writtenSummary}:</strong>
                <p className="text-slate-600 mt-1 leading-relaxed">
                  {result.written_summary}
                </p>
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

            <div>
              <strong>{t.studyPlan}:</strong>
              <ul className="list-disc ml-6">
                {result.study_plan?.map((s: string, i: number) => (
                  <li key={i}>{s}</li>
                ))}
              </ul>
            </div>

            <p className="text-xs text-slate-500 border-t pt-4">
              {result.disclaimer}
            </p>
          </div>
        )}
      </div>
    </main>
  );
}
