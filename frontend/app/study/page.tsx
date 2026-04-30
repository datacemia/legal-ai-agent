"use client";

import { useState } from "react";
import { getToken } from "../../lib/auth";

export default function StudyPage() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [paymentMessage, setPaymentMessage] = useState("");
  const [showLevelModal, setShowLevelModal] = useState(false);
  const [educationLevel, setEducationLevel] = useState("");
  const [selectedAnswers, setSelectedAnswers] = useState<Record<string, string>>(
    {}
  );
  const [quizSubmitted, setQuizSubmitted] = useState(false);
  const [retryCount, setRetryCount] = useState(0);

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

    try {
      const token = getToken();

      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/study/analyze`,
        {
          method: "POST",
          headers: token
            ? {
                Authorization: `Bearer ${token}`,
              }
            : {},
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
        detail: "Failed to connect to Study Agent API.",
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

  const formatLevel = (level: string) =>
    level.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

  const getScoreColor = () => {
    if (score >= 80) return "bg-green-50 text-green-700 border-green-200";
    if (score >= 50) return "bg-yellow-50 text-yellow-700 border-yellow-200";
    return "bg-red-50 text-red-700 border-red-200";
  };

  const getScoreFeedback = () => {
    if (score >= 80) return "Excellent work. You understood the material well.";
    if (score >= 50) return "Good effort. Review the explanations and retry.";
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
              {isCorrect ? "Correct" : "Incorrect"} — Answer:{" "}
              {q.correct_answer}
            </p>
            <p className="text-slate-500 mt-1">{q.explanation}</p>
          </div>
        )}
      </div>
    );
  };

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-10">
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold">Study Agent</h1>
          <p className="text-slate-500 mt-2">
            Upload a PDF to generate a summary, theoretical quiz, practical
            quiz, flashcards, and a study plan.
          </p>
        </div>

        <div className="bg-white p-6 rounded-2xl border space-y-4">
          <div className="rounded-xl bg-slate-50 border border-slate-200 p-4 text-sm text-slate-600 space-y-3">
            <p>
              <strong>How this agent works:</strong> Upload your study PDF and let the Study Agent transform it into an interactive learning experience.
            </p>

            <p>
              Before analysis, you select your learning level. The agent adapts the difficulty, vocabulary, explanations, and questions to match your level.
            </p>

            <ul className="list-disc ml-5 space-y-1">
              <li>A clear and structured summary</li>
              <li>Key learning points</li>
              <li>Theoretical quiz (understanding)</li>
              <li>Practical quiz (real-world application)</li>
              <li>Flashcards for memorization</li>
              <li>A short study plan</li>
            </ul>

            <p>
              You can answer the quiz directly, get instant feedback, explanations, and track your score.
            </p>

            <p className="text-xs text-slate-500">
              Results are for educational support only. Always verify important academic content with your teacher, course materials, or trusted sources.
            </p>
          </div>

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
              {loading ? "Analyzing..." : "Analyze"}
            </button>

            <button
              onClick={() =>
                setPaymentMessage(
                  "Stripe is not configured yet. Credit purchase will be available soon."
                )
              }
              className="w-full bg-green-600 text-white py-3 rounded-xl hover:bg-green-700 transition"
            >
              Buy credits
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
                <h2 className="text-xl font-semibold">Select education level</h2>
                <p className="text-sm text-slate-500 mt-1">
                  This helps the Study Agent adapt explanations and questions to
                  your level.
                </p>
              </div>

              <select
                value={educationLevel}
                onChange={(e) => setEducationLevel(e.target.value)}
                className="w-full rounded-xl border border-slate-300 px-4 py-3 text-sm"
              >
                <option value="">Choose your level</option>
                <option value="primary_school">Primary school</option>
                <option value="middle_school">Middle school</option>
                <option value="high_school">High school</option>
                <option value="vocational_training">Vocational training</option>
                <option value="university">University</option>
              </select>

              <div className="grid grid-cols-2 gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setShowLevelModal(false)}
                  className="w-full rounded-xl border border-slate-300 py-3 text-slate-700 hover:bg-slate-50"
                >
                  Cancel
                </button>

                <button
                  type="button"
                  onClick={handleAnalyze}
                  disabled={!educationLevel || loading}
                  className="w-full rounded-xl bg-slate-900 py-3 text-white disabled:bg-slate-400"
                >
                  Continue
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
            <h2 className="text-xl font-semibold">Results</h2>

            {educationLevel && (
              <p className="text-sm text-slate-500">
                Adapted level:{" "}
                <span className="font-medium text-slate-700">
                  {formatLevel(educationLevel)}
                </span>
              </p>
            )}

            <div>
              <strong>Summary:</strong>
              <p className="text-slate-600 mt-1">{result.summary}</p>
            </div>

            <div>
              <strong>Key Points:</strong>
              <ul className="list-disc ml-6">
                {result.key_points?.map((p: string, i: number) => (
                  <li key={i}>{p}</li>
                ))}
              </ul>
            </div>

            <div>
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                <strong>Quiz:</strong>

                {quizSubmitted && Object.keys(selectedAnswers).length > 0 && (
                  <div
                    className={`rounded-xl border px-4 py-2 text-sm ${getScoreColor()}`}
                  >
                    Score:{" "}
                    <strong>
                      {correctAnswers}/{totalQuestions} ({score}%)
                    </strong>
                  </div>
                )}
              </div>

              <div className="mt-4">
                <h3 className="font-semibold">Theoretical Questions</h3>
                {theoryQuestions.map((q: any, i: number) =>
                  renderQuestion(q, i, "theory")
                )}
              </div>

              <div className="mt-6">
                <h3 className="font-semibold">Practical Questions</h3>
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
                    ? "Quiz submitted"
                    : Object.keys(selectedAnswers).length < totalQuestions
                    ? "Answer all questions to submit"
                    : "Submit quiz"}
                </button>
              )}

              {quizSubmitted && (
                <div className="mt-4 rounded-xl border bg-slate-50 p-4 text-sm">
                  <p className="font-semibold">Learning feedback</p>
                  <p className="text-slate-600 mt-1">{getScoreFeedback()}</p>

                  <button
                    onClick={handleRetryQuiz}
                    disabled={retryCount >= 2}
                    className="mt-3 px-4 py-2 rounded-xl bg-slate-900 text-white text-sm disabled:bg-slate-400"
                  >
                    {retryCount >= 2 ? "No retries left" : "Retry quiz"}
                  </button>
                </div>
              )}
            </div>

            <div>
              <strong>Flashcards:</strong>

              <div className="grid sm:grid-cols-2 gap-4 mt-3">
                {result.flashcards?.map((f: any, i: number) => (
                  <div key={i} className="border rounded-xl p-4 bg-slate-50">
                    <p className="text-sm text-slate-500 mb-1">Front</p>
                    <p className="font-semibold">{f.front}</p>

                    <div className="mt-3 border-t pt-3">
                      <p className="text-sm text-slate-500 mb-1">Back</p>
                      <p className="text-slate-700">{f.back}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <strong>Study Plan:</strong>
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