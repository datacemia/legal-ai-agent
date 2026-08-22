"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { getSavedLocale } from "../../../lib/i18n";

type Locale = "en" | "fr" | "ar";

const STUDY_DEMO_VIDEOS: Record<Locale, string> = {
  en: "https://drive.google.com/file/d/1KRkbdt21_81RSDWnsLZ9Um3FY5j2TRDX/preview",
  fr: "https://drive.google.com/file/d/178NFUtjiyfwhau-EwGqtYwUXn4pDaIxi/preview",
  ar: "https://drive.google.com/file/d/181w3pp1XkeiNRyPNBwAfuBxwAqBwu_eo/preview",
};

const content: Record<
  Locale,
  {
    badge: string;
    title: string;
    subtitle: string;
    videoTitle: string;
    videoDescription: string;
    capabilitiesTitle: string;
    capabilities: string[];
    ctaText: string;
    ctaButton: string;
    language: string;
  }
> = {
  en: {
    badge: "Demonstration",
    title: "Runexa Study Agent Demo",
    subtitle:
      "See how Runexa Study transforms study materials into a complete AI-powered learning workspace.",
    videoTitle: "Runexa Study Agent — English Demo",
    videoDescription:
      "Watch Runexa Study analyze learning material and generate summaries, quizzes, flashcards, visual learning maps, audio support, and personalized revision plans.",
    capabilitiesTitle: "What can Runexa Study Agent do?",
    capabilities: [
      "Generate structured summaries and detailed explanations",
      "Create theoretical and practical quizzes",
      "Build flashcards automatically",
      "Generate visual learning maps",
      "Provide audio learning support",
      "Create personalized revision plans",
      "Identify weak learning areas",
    ],
    ctaText: "Ready to analyze your own study materials?",
    ctaButton: "Try Runexa Study",
    language: "English",
  },

  fr: {
    badge: "Démonstration",
    title: "Démo Runexa Study Agent",
    subtitle:
      "Découvrez comment Runexa Study transforme vos supports de cours en un espace d’apprentissage complet propulsé par l’IA.",
    videoTitle: "Runexa Study Agent — Démo en français",
    videoDescription:
      "Regardez Runexa Study analyser un support pédagogique et générer des résumés, quiz, flashcards, cartes d’apprentissage, audio et plans de révision personnalisés.",
    capabilitiesTitle: "Que peut faire Runexa Study Agent ?",
    capabilities: [
      "Générer des résumés structurés et des explications détaillées",
      "Créer des quiz théoriques et pratiques",
      "Créer automatiquement des flashcards",
      "Générer des cartes d’apprentissage visuelles",
      "Fournir un support d’apprentissage audio",
      "Créer des plans de révision personnalisés",
      "Identifier les points faibles",
    ],
    ctaText: "Prêt à analyser vos propres supports d’étude ?",
    ctaButton: "Essayer Runexa Study",
    language: "Français",
  },

  ar: {
    badge: "عرض توضيحي",
    title: "عرض Runexa Study Agent",
    subtitle:
      "شاهد كيف يحوّل Runexa Study المواد الدراسية إلى مساحة تعلم متكاملة مدعومة بالذكاء الاصطناعي.",
    videoTitle: "Runexa Study Agent — العرض باللغة العربية",
    videoDescription:
      "شاهد Runexa Study وهو يحلل المواد الدراسية وينشئ الملخصات والاختبارات وبطاقات المراجعة وخرائط التعلم والصوت وخطط المراجعة المخصصة.",
    capabilitiesTitle: "ماذا يمكن أن يقدم Runexa Study Agent؟",
    capabilities: [
      "إنشاء ملخصات منظمة وشروحات مفصلة",
      "إنشاء اختبارات نظرية وتطبيقية",
      "إنشاء بطاقات مراجعة تلقائياً",
      "إنشاء خرائط تعلم بصرية",
      "دعم التعلم الصوتي",
      "إنشاء خطط مراجعة مخصصة",
      "تحديد نقاط الضعف",
    ],
    ctaText: "هل أنت مستعد لتحليل موادك الدراسية؟",
    ctaButton: "جرّب Runexa Study",
    language: "العربية",
  },
};

const normalizeLocale = (
  value: string | null | undefined,
  fallback: Locale = "en"
): Locale => {
  if (value === "en" || value === "fr" || value === "ar") {
    return value;
  }

  return fallback;
};

export default function StudyAgentDemoClient() {
  const pathname = usePathname();
  const [locale, setLocale] = useState<Locale>("en");

  useEffect(() => {
    const resolveLocale = (): Locale => {
      if (pathname === "/fr" || pathname?.startsWith("/fr/")) {
        return "fr";
      }

      if (pathname === "/ar" || pathname?.startsWith("/ar/")) {
        return "ar";
      }

      if (pathname === "/en" || pathname?.startsWith("/en/")) {
        return "en";
      }

      return normalizeLocale(getSavedLocale(), "en");
    };

    setLocale(resolveLocale());

    const handleLocaleChange = () => {
      setLocale(resolveLocale());
    };

    window.addEventListener("locale-change", handleLocaleChange);

    return () => {
      window.removeEventListener("locale-change", handleLocaleChange);
    };
  }, [pathname]);

  const t = content[locale];
  const videoUrl = STUDY_DEMO_VIDEOS[locale];

  const studyHref =
    locale === "fr"
      ? "/fr/study"
      : locale === "ar"
      ? "/ar/study"
      : "/en/study";

  return (
    <main
      dir={locale === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-4 py-14 sm:px-6 sm:py-16"
    >
      <div className="mx-auto max-w-6xl">
        <div className="text-center">
          <span className="inline-flex rounded-full border border-blue-200 bg-blue-50 px-4 py-1.5 text-xs font-bold uppercase tracking-[0.18em] text-blue-700">
            {t.badge}
          </span>

          <h1 className="mx-auto mt-5 max-w-4xl text-4xl font-black tracking-tight text-slate-950 sm:text-5xl">
            {t.title}
          </h1>

          <p className="mx-auto mt-5 max-w-3xl text-base leading-7 text-slate-600 sm:text-lg">
            {t.subtitle}
          </p>
        </div>

        <section className="mt-10 overflow-hidden rounded-[2rem] border border-slate-200 bg-white shadow-xl">
          <div className="border-b border-slate-100 px-6 py-5 sm:px-8">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h2 className="text-xl font-black text-slate-950 sm:text-2xl">
                  {t.videoTitle}
                </h2>

                <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-600">
                  {t.videoDescription}
                </p>
              </div>

              <span className="inline-flex w-fit rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-bold text-slate-600">
                {t.language}
              </span>
            </div>
          </div>

          <div className="bg-slate-950 p-2 sm:p-4">
            <iframe
              key={`${locale}-${videoUrl}`}
              src={videoUrl}
              title={t.videoTitle}
              className="aspect-video w-full rounded-2xl bg-black"
              allow="autoplay; fullscreen"
              referrerPolicy="strict-origin-when-cross-origin"
              allowFullScreen
            />
          </div>
        </section>

        <section className="mt-10 rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
          <h2 className="text-2xl font-black text-slate-950">
            {t.capabilitiesTitle}
          </h2>

          <div className="mt-6 grid gap-3 sm:grid-cols-2">
            {t.capabilities.map((item) => (
              <div
                key={item}
                className="flex items-start gap-3 rounded-2xl border border-slate-100 bg-slate-50 px-4 py-3"
              >
                <span className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-green-100 text-sm font-black text-green-700">
                  ✓
                </span>

                <span className="text-sm font-medium leading-6 text-slate-700">
                  {item}
                </span>
              </div>
            ))}
          </div>
        </section>

        <section className="mt-10 rounded-[2rem] bg-slate-950 px-6 py-10 text-center text-white sm:px-10">
          <p className="text-lg font-semibold text-slate-200">{t.ctaText}</p>

          <Link
            href={studyHref}
            className="mt-6 inline-flex rounded-2xl bg-blue-600 px-8 py-4 text-base font-black text-white transition hover:-translate-y-0.5 hover:bg-blue-500"
          >
            {t.ctaButton}
          </Link>
        </section>
      </div>
    </main>
  );
}
