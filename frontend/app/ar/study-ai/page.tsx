import type { Metadata } from "next";
import StudyAIClient from "../../study-ai/StudyAIClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "مساعد دراسة بالذكاء الاصطناعي ومساحة تعلم | Runexa",

  description:
    "أنشئ ملخصات واختبارات وبطاقات تعليمية وخطط دراسة وتدفقات تعلم منظمة باستخدام Runexa Study AI.",

  keywords: [
    "ذكاء اصطناعي للدراسة",
    "مساعد دراسة بالذكاء الاصطناعي",
    "بطاقات تعليمية بالذكاء الاصطناعي",
    "اختبارات بالذكاء الاصطناعي",
    "ملخصات بالذكاء الاصطناعي",
    "خطط دراسة بالذكاء الاصطناعي",
    "تدفقات تعلم بالذكاء الاصطناعي",
    "Runexa study AI",

    "Runexa Study Agent",
    "التعلم الذكي",
    "التعلم المدعوم بالذكاء الاصطناعي",
    "التعلم الشخصي بالذكاء الاصطناعي",
    "التعلم التكيفي بالذكاء الاصطناعي",
    "مساعد تعليمي بالذكاء الاصطناعي",
    "منصة تعليمية بالذكاء الاصطناعي",
    "التعليم الذكي",
    "التعليم الرقمي",
    "التعلم الإلكتروني",
    "تحسين التحصيل الدراسي",
    "إدارة الدراسة",
    "تنظيم الدراسة",
    "إنشاء ملخصات دراسية",
    "تلخيص الدروس بالذكاء الاصطناعي",
    "إنشاء أسئلة اختبار",
    "اختبارات تفاعلية",
    "اختبارات تدريبية",
    "بطاقات مراجعة ذكية",
    "بطاقات تعليمية ذكية",
    "مراجعة الدروس",
    "تحضير الامتحانات",
    "مساعد الطلاب",
    "أداة تعليمية للطلاب",
    "الدراسة الجامعية",
    "التعلم الذاتي",
    "مسارات تعلم مخصصة",
    "إنشاء خطط دراسية",
    "تحليل المحتوى التعليمي",
    "تحويل الملفات إلى ملخصات",
    "منصة تعلم ذكية",
    "ذكاء اصطناعي للتعليم",
    "AI Education",
    "AI Learning Platform",
    "Enterprise Learning AI",
  ],

  alternates: {
    canonical: "https://runexa.ai/ar/study-ai",
    languages: {
      en: `${siteUrl}/en/study-ai`,
      fr: `${siteUrl}/fr/study-ai`,
      ar: `${siteUrl}/ar/study-ai`,
      "x-default": `${siteUrl}/study-ai`,
    },
  },

  openGraph: {
    title: "مساعد دراسة بالذكاء الاصطناعي ومساحة تعلم | Runexa",

    description:
      "أنشئ ملخصات واختبارات وبطاقات تعليمية وخطط دراسة وتدفقات تعلم منظمة باستخدام Runexa Study AI.",

    url: "https://runexa.ai/ar/study-ai",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Study AI",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "مساعد دراسة بالذكاء الاصطناعي ومساحة تعلم | Runexa",

    description:
      "مساعد دراسة بالذكاء الاصطناعي لإنشاء الملخصات والاختبارات والبطاقات التعليمية وخطط الدراسة وتدفقات التعلم المنظمة.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function StudyAIPage() {
  return (
    <>
      <StudyAIClient initialLocale="ar" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify([
            {
              "@context": "https://schema.org",

              "@type": "SoftwareApplication",

              name: "Runexa Study AI",

              applicationCategory: "EducationalApplication",

              operatingSystem: "Web",

              url: "https://runexa.ai/ar/study-ai",

              inLanguage: "ar",

              description:
                "مساعد دراسة بالذكاء الاصطناعي لإنشاء الملخصات والاختبارات والبطاقات التعليمية وخطط الدراسة وتدفقات التعلم المنظمة.",

              publisher: {
                "@type": "Organization",
                name: "Runexa Systems LLC",
                url: siteUrl,
              },

              knowsAbout: [
                "Study AI",
                "AI Study Assistant",
                "AI Flashcards",
                "AI Quizzes",
                "AI Summaries",
                "AI Study Plans",
                "Learning Workflows AI",
              ],
            },
          ]),
        }}
      />
    </>
  );
}
