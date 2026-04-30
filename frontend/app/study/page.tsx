"use client";

import { useEffect, useState } from "react";
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
      "Upload a PDF to generate a summary, theoretical quiz, practical quiz, flashcards, and a study plan.",
    howTitle: "How this agent works:",
    how1:
      "Upload your study PDF and let the Study Agent transform it into an interactive learning experience.",
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
  },
  fr: {
    title: "Agent étude",
    subtitle:
      "Téléchargez un PDF pour générer un résumé, un quiz théorique, un quiz pratique, des flashcards et un plan de révision.",
    howTitle: "Comment fonctionne cet agent :",
    how1:
      "Téléchargez votre PDF de cours et laissez l’agent étude le transformer en expérience d’apprentissage interactive.",
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
  },
  ar: {
    title: "وكيل الدراسة",
    subtitle:
      "ارفع ملف PDF لإنشاء ملخص، اختبار نظري، اختبار تطبيقي، بطاقات مراجعة وخطة دراسة.",
    howTitle: "كيف يعمل هذا الوكيل:",
    how1: "ارفع ملف الدراسة وسيحوّله وكيل الدراسة إلى تجربة تعلم تفاعلية.",
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
  },
};

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

  useEffect(() => {
    setLanguage(getSavedLocale());
  }, []);

  const t = labels[language] || labels.en;

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
      <div key={key} className="mt-3 rounded-xl border p-4 bg-white">
        <p className="font-medium">
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
                className={`text-left rounded-xl border px-4 py-2 text-sm transition ${
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
            }}
            className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
          >
            <option value="en">English</option>
            <option value="fr">Français</option>
            <option value="ar">العربية</option>
          </select>

          <input
            type="file"
            accept=".pdf"
            onChange={(e) => {
              setFile(e.target.files?.[0] || null);
              setResult(null);
              setPaymentMessage("");
              setSelectedAnswers({});
              setQuizSubmitted(false);
              setEducationLevel("");
              setRetryCount(0);
            }}
            className="w-full rounded-xl border px-4 py-3"
          />

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <button
              onClick={() => {
                setResult(null);
                setSelectedAnswers({});
                setQuizSubmitted(false);
                setPaymentMessage("");
                setRetryCount(0);
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