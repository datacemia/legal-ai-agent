import type { Metadata } from "next";
import ApiClient from "../../api/ApiClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "واجهات API للذكاء الاصطناعي وبنية الوكلاء | Runexa",

  description:
    "ادمج واجهات Runexa AI API للتحليل القانوني والذكاء المالي وأتمتة الدراسة وتدفقات دعم قرارات الأعمال.",

  keywords: [
  "Runexa API",
  "واجهات API للذكاء الاصطناعي",
  "API الذكاء القانوني",
  "API الذكاء المالي",
  "API الدراسة الذكية",
  "API ذكاء الأعمال",
  "معالجة ذكاء اصطناعي غير متزامنة",
  "بنية ذكاء اصطناعي",

  "واجهة برمجة تطبيقات الذكاء الاصطناعي",
  "تكامل الذكاء الاصطناعي",
  "خدمات الذكاء الاصطناعي للمطورين",
  "منصة API للذكاء الاصطناعي",
  "واجهات Runexa للمطورين",
  "API تحليل العقود",
  "API تحليل المستندات القانونية",
  "API إدارة الشؤون المالية",
  "API تحليل الإنفاق",
  "API التعلّم الذكي",
  "API إنشاء الاختبارات التعليمية",
  "API دعم اتخاذ القرار",
  "API تحليل الأعمال",
  "معالجة المستندات بالذكاء الاصطناعي",
  "أتمتة سير العمل بالذكاء الاصطناعي",
  "خدمات الذكاء الاصطناعي للمؤسسات",
  "واجهات برمجة التطبيقات للمؤسسات",
  "بنية تحتية للذكاء الاصطناعي",
  "تكامل SaaS بالذكاء الاصطناعي",
  "نماذج الذكاء الاصطناعي المتخصصة",
  "وكلاء الذكاء الاصطناعي",
  "API الوكلاء الذكيين",
  "Runexa Systems API",
  "منصة Runexa للمطورين",
 ],
  alternates: {
    canonical: "https://runexa.ai/ar/api",
    languages: {
      en: `${siteUrl}/en/api`,
      fr: `${siteUrl}/fr/api`,
      ar: `${siteUrl}/ar/api`,
      "x-default": `${siteUrl}/api`,
    },
  },

  openGraph: {
    title: "واجهات API للذكاء الاصطناعي وبنية الوكلاء | Runexa",

    description:
      "ادمج واجهات Runexa AI API للتحليل القانوني والذكاء المالي وأتمتة الدراسة وتدفقات دعم قرارات الأعمال.",

    url: "https://runexa.ai/ar/api",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa API Platform",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "واجهات API للذكاء الاصطناعي وبنية الوكلاء | Runexa",

    description:
      "واجهات API للذكاء الاصطناعي لأتمتة القانون والمالية والدراسة والأعمال.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function ApiPage() {
  return (
    <>
      <ApiClient initialLocale="ar" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "SoftwareApplication",

            name: "Runexa API Platform",

            applicationCategory: "DeveloperApplication",

            operatingSystem: "Web",

            description:
              "منصة Runexa API للذكاء الاصطناعي للتحليل القانوني والذكاء المالي وأتمتة الدراسة ودعم قرارات الأعمال والمعالجة غير المتزامنة وبنية الوكلاء.",

            url: "https://runexa.ai/ar/api",

            inLanguage: "ar",

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: siteUrl,
            },

            knowsAbout: [
              "AI APIs",
              "Legal AI API",
              "Finance AI API",
              "Study AI API",
              "Business AI API",
              "Async AI Processing",
              "AI Infrastructure",
            ],
          }),
        }}
      />
    </>
  );
}
