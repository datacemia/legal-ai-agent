import type { Metadata } from "next";
import AIBusinessIntelligenceArticle from "../../../blog/ai-business-intelligence/AIBusinessIntelligenceArticle";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "ذكاء الأعمال بالذكاء الاصطناعي: تحويل البيانات إلى قرارات أفضل | Runexa",

  description:
    "تعرّف على كيف يساعد ذكاء الأعمال المدعوم بالذكاء الاصطناعي الفرق على تحليل البيانات واكتشاف المخاطر والفرص وتحسين اتخاذ القرار الاستراتيجي.",

  keywords: [
    "ذكاء الأعمال بالذكاء الاصطناعي",
    "ذكاء الأعمال AI",
    "دعم القرار بالذكاء الاصطناعي",
    "تحليل مؤشرات الأداء بالذكاء الاصطناعي",
    "تحليل بيانات الأعمال",
    "ملخصات تنفيذية بالذكاء الاصطناعي",
    "Runexa Business Agent",
    "سير عمل الأعمال بالذكاء الاصطناعي",

    "وكيل الأعمال بالذكاء الاصطناعي",
    "تحليل الأداء المؤسسي",
    "اتخاذ القرارات التجارية",
    "التحليل الاستراتيجي بالذكاء الاصطناعي",
    "مؤشرات الأداء الرئيسية KPI",
    "تحليل المخاطر التجارية",
    "التنبؤ بالأعمال بالذكاء الاصطناعي",
    "ذكاء الأعمال للمؤسسات",
    "تحليل اتجاهات السوق",
    "دعم الإدارة التنفيذية",
    "لوحات المعلومات الذكية",
    "تقارير الأعمال الذكية",
    "تحليل الفرص التجارية",
    "تحليل المنافسين بالذكاء الاصطناعي",
    "تحسين الأداء المؤسسي",
    "مساعد اتخاذ القرار",
    "إدارة الأعمال الذكية",
    "تحليل البيانات المؤسسية",
    "التحول الرقمي للأعمال",
    "ذكاء اصطناعي للمديرين التنفيذيين",
    "أتمتة التحليل التجاري",
    "Runexa Business Decision Agent",
    "الذكاء الاصطناعي للأعمال",
  ],

  alternates: {
    canonical: "https://runexa.ai/ar/blog/ai-business-intelligence",
    languages: {
      en: `${siteUrl}/en/blog/ai-business-intelligence`,
      fr: `${siteUrl}/fr/blog/ai-business-intelligence`,
      ar: `${siteUrl}/ar/blog/ai-business-intelligence`,
      "x-default": `${siteUrl}/blog/ai-business-intelligence`,
    },
  },

  openGraph: {
    title: "ذكاء الأعمال بالذكاء الاصطناعي: تحويل البيانات إلى قرارات أفضل | Runexa",

    description:
      "تعرّف على كيف يساعد ذكاء الأعمال المدعوم بالذكاء الاصطناعي الفرق على تحليل البيانات واكتشاف المخاطر والفرص وتحسين اتخاذ القرار الاستراتيجي.",

    url: "https://runexa.ai/ar/blog/ai-business-intelligence",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa AI Business Intelligence",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "article",
  },

  twitter: {
    card: "summary_large_image",

    title: "ذكاء الأعمال بالذكاء الاصطناعي: تحويل البيانات إلى قرارات أفضل | Runexa",

    description:
      "تعرّف على كيف يساعد ذكاء الأعمال المدعوم بالذكاء الاصطناعي الفرق على تحليل البيانات واكتشاف المخاطر والفرص وتحسين اتخاذ القرار الاستراتيجي.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function AIBusinessIntelligencePage() {
  return (
    <>
      <AIBusinessIntelligenceArticle initialLocale="ar" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "Article",

            headline:
              "ذكاء الأعمال المدعوم بالذكاء الاصطناعي: تحويل البيانات إلى قرارات أفضل",

            description:
              "تعرّف على كيف يساعد ذكاء الأعمال المدعوم بالذكاء الاصطناعي الفرق على تحليل البيانات واكتشاف المخاطر والفرص وتحسين اتخاذ القرار الاستراتيجي.",

            datePublished: "2026-05-24",

            dateModified: "2026-05-24",

            inLanguage: "ar",

            mainEntityOfPage: {
              "@type": "WebPage",
              "@id": "https://runexa.ai/ar/blog/ai-business-intelligence",
            },

            author: {
              "@type": "Person",
              name: "Dr. Rachid Ejjami",
            },

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: siteUrl,
            },
          }),
        }}
      />
    </>
  );
}
