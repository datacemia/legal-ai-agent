import type { Metadata } from "next";
import StudyClient from "../../study/StudyClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "مساحة دراسة ومساعد تعلم بالذكاء الاصطناعي | Runexa",

  description:
    "أنشئ ملخصات واختبارات وبطاقات مراجعة وشرحاً صوتياً وخرائط ذهنية وخطط دراسة مخصصة باستخدام Runexa Study Agent.",

  keywords: [
    "مساعد دراسة بالذكاء الاصطناعي",
    "مساحة تعلم بالذكاء الاصطناعي",
    "بطاقات مراجعة بالذكاء الاصطناعي",
    "اختبارات بالذكاء الاصطناعي",
    "خطة دراسة بالذكاء الاصطناعي",
    "تعليم بالذكاء الاصطناعي",
    "ملخصات بالذكاء الاصطناعي",
    "منصة تعلم بالذكاء الاصطناعي",
    "Runexa study AI",
    "تعلم تكيفي بالذكاء الاصطناعي",

    "Runexa Study Agent",
    "التعلم الذكي",
    "التعلم الشخصي بالذكاء الاصطناعي",
    "مساعد تعليمي بالذكاء الاصطناعي",
    "منصة تعليمية ذكية",
    "تحسين التحصيل الدراسي",
    "إدارة الدراسة",
    "تنظيم الدراسة",
    "خطة تعلم مخصصة",
    "تلخيص الدروس بالذكاء الاصطناعي",
    "إنشاء ملخصات دراسية",
    "إنشاء أسئلة اختبار",
    "اختبارات تفاعلية",
    "مراجعة الدروس",
    "بطاقات تعليمية ذكية",
    "بطاقات مراجعة ذكية",
    "تحضير الامتحانات",
    "مساعد الطلاب",
    "أداة تعليمية للطلاب",
    "التعليم الرقمي",
    "التعليم المدعوم بالذكاء الاصطناعي",
    "التعلم الإلكتروني",
    "التعلم الذاتي",
    "التعلم الجامعي",
    "تحليل المحتوى التعليمي",
    "تحويل الملفات إلى ملخصات",
    "إنشاء خطط دراسية",
    "إنشاء اختبارات تدريبية",
    "مسارات تعلم مخصصة",
    "ذكاء اصطناعي للتعليم",
    "AI Education Platform",
    "Enterprise Learning AI",
  ],

  alternates: {
    canonical: "https://runexa.ai/ar/study",
    languages: {
      en: `${siteUrl}/en/study`,
      fr: `${siteUrl}/fr/study`,
      ar: `${siteUrl}/ar/study`,
      "x-default": `${siteUrl}/study`,
    },
  },

  openGraph: {
    title: "Runexa Study Agent",

    description:
      "مساحة دراسة بالذكاء الاصطناعي مع ملخصات واختبارات وبطاقات مراجعة وتعلم تكيفي.",

    url: "https://runexa.ai/ar/study",

    siteName: "Runexa Systems",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Study Agent",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Runexa Study Agent",

    description:
      "ملخصات واختبارات وبطاقات مراجعة وشرح صوتي وتدفقات تعلم تكيفية بالذكاء الاصطناعي.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function StudyPage() {
  return (
    <>
      <StudyClient initialLocale="ar" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "SoftwareApplication",

            name: "Runexa Study Agent",

            applicationCategory: "EducationalApplication",

            operatingSystem: "Web",

            description:
              "مساحة دراسة مدعومة بالذكاء الاصطناعي مع ملخصات واختبارات وبطاقات مراجعة وتعلم بصري وخطط دراسة تكيفية.",

            url: "https://runexa.ai/ar/study",

            inLanguage: "ar",

            creator: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
            },

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: siteUrl,
            },

            knowsAbout: [
              "AI Study Assistant",
              "AI Learning Workspace",
              "AI Flashcards",
              "AI Quizzes",
              "AI Study Plans",
              "Adaptive Learning AI",
            ],
          }),
        }}
      />
    </>
  );
}
