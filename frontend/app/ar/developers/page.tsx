import type { Metadata } from "next";
import DevelopersClient from "../../developers/DevelopersClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "المطورون وواجهات API للذكاء الاصطناعي | Runexa",

  description:
    "أنشئ تدفقات عمل مدعومة بالذكاء الاصطناعي باستخدام واجهات Runexa API للتحليل القانوني والذكاء المالي وأتمتة التعلم ودعم قرارات الأعمال.",

 keywords: [
  "مطورو Runexa",
  "API الذكاء الاصطناعي",
  "API الذكاء القانوني",
  "API الذكاء المالي",
  "API الدراسة الذكية",
  "API ذكاء الأعمال",
  "API سير عمل الذكاء الاصطناعي",
  "أدوات ذكاء اصطناعي للمطورين",
  "API الذكاء الاصطناعي للمؤسسات",

  "واجهة برمجة تطبيقات الذكاء الاصطناعي",
  "منصة Runexa للمطورين",
  "Runexa API",
  "تكامل الذكاء الاصطناعي",
  "واجهات برمجة التطبيقات للمؤسسات",
  "خدمات الذكاء الاصطناعي للمطورين",
  "منصة API للذكاء الاصطناعي",
  "API تحليل العقود",
  "API تحليل المستندات القانونية",
  "API تحليل مالي",
  "API تحليل الإنفاق",
  "API التعلّم الذكي",
  "API إنشاء الاختبارات",
  "API الملخصات التعليمية",
  "API دعم اتخاذ القرار",
  "API تحليل الأعمال",
  "API مؤشرات الأداء KPI",
  "API ذكاء الأعمال",
  "معالجة المستندات بالذكاء الاصطناعي",
  "أتمتة سير العمل",
  "وكلاء الذكاء الاصطناعي",
  "API الوكلاء الذكيين",
  "البنية التحتية للذكاء الاصطناعي",
  "معالجة غير متزامنة",
  "تكامل SaaS بالذكاء الاصطناعي",
  "REST API للذكاء الاصطناعي",
  "منصة مطورين",
  "حلول الذكاء الاصطناعي للمؤسسات",
  "نماذج ذكاء اصطناعي متخصصة",
  "Runexa Developers",
  ],

  alternates: {
    canonical: "https://runexa.ai/ar/developers",
    languages: {
      en: `${siteUrl}/en/developers`,
      fr: `${siteUrl}/fr/developers`,
      ar: `${siteUrl}/ar/developers`,
      "x-default": `${siteUrl}/developers`,
    },
  },

  openGraph: {
    title: "المطورون وواجهات API للذكاء الاصطناعي | Runexa",

    description:
      "أنشئ تدفقات عمل مدعومة بالذكاء الاصطناعي باستخدام واجهات Runexa API للتحليل القانوني والذكاء المالي وأتمتة التعلم ودعم قرارات الأعمال.",

    url: "https://runexa.ai/ar/developers",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Developers",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "المطورون وواجهات API للذكاء الاصطناعي | Runexa",

    description:
      "أنشئ تدفقات عمل مدعومة بالذكاء الاصطناعي باستخدام واجهات Runexa API للتحليل القانوني والذكاء المالي وأتمتة التعلم ودعم قرارات الأعمال.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function DevelopersPage() {
  return (
    <>
      <DevelopersClient initialLocale="ar" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "TechArticle",

            headline: "المطورون وواجهات API للذكاء الاصطناعي | Runexa",

            name: "Runexa Developers",

            description:
              "منصة مطورين لإنشاء تدفقات عمل مدعومة بالذكاء الاصطناعي باستخدام واجهات Runexa API للتحليل القانوني والذكاء المالي وأتمتة التعلم ودعم قرارات الأعمال.",

            url: "https://runexa.ai/ar/developers",

            inLanguage: "ar",

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: siteUrl,
            },

            about: [
              "AI APIs",
              "Developer APIs",
              "Legal AI API",
              "Finance AI API",
              "Study AI API",
              "Business AI API",
              "AI Workflow Automation",
            ],
          }),
        }}
      />
    </>
  );
}
