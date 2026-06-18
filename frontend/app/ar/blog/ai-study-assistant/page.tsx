import type { Metadata } from "next";
import AIStudyAssistantArticle from "../../../blog/ai-study-assistant/AIStudyAssistantArticle";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "مساعد الدراسة بالذكاء الاصطناعي: بناء مسارات تعلم أكثر فاعلية | Runexa",

  description:
    "تعرّف على كيف تساعد أدوات الدراسة بالذكاء الاصطناعي في إنشاء الملخصات والاختبارات والبطاقات التعليمية ومسارات التعلم المنظمة.",

  keywords: [
    "مساعد الدراسة بالذكاء الاصطناعي",
    "مسارات التعلم بالذكاء الاصطناعي",
    "ملخصات بالذكاء الاصطناعي",
    "بطاقات تعليمية بالذكاء الاصطناعي",
    "اختبارات بالذكاء الاصطناعي",
    "تخطيط الدراسة بالذكاء الاصطناعي",
    "Runexa Study Agent",
    "الذكاء الاصطناعي في التعليم",
  ],

  alternates: {
    canonical: "https://runexa.ai/ar/blog/ai-study-assistant",
    languages: {
      en: `${siteUrl}/en/blog/ai-study-assistant`,
      fr: `${siteUrl}/fr/blog/ai-study-assistant`,
      ar: `${siteUrl}/ar/blog/ai-study-assistant`,
      "x-default": `${siteUrl}/blog/ai-study-assistant`,
    },
  },

  openGraph: {
    title: "مساعد الدراسة بالذكاء الاصطناعي: بناء مسارات تعلم أكثر فاعلية | Runexa",

    description:
      "تعرّف على كيف تساعد أدوات الدراسة بالذكاء الاصطناعي في إنشاء الملخصات والاختبارات والبطاقات التعليمية ومسارات التعلم المنظمة.",

    url: "https://runexa.ai/ar/blog/ai-study-assistant",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa AI Study Assistant",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "article",
  },

  twitter: {
    card: "summary_large_image",

    title: "مساعد الدراسة بالذكاء الاصطناعي: بناء مسارات تعلم أكثر فاعلية | Runexa",

    description:
      "تعرّف على كيف تساعد أدوات الدراسة بالذكاء الاصطناعي في إنشاء الملخصات والاختبارات والبطاقات التعليمية ومسارات التعلم المنظمة.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function AIStudyAssistantPage() {
  return (
    <>
      <AIStudyAssistantArticle initialLocale="ar" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "Article",

            mainEntityOfPage: {
              "@type": "WebPage",
              "@id": "https://runexa.ai/ar/blog/ai-study-assistant",
            },

            headline:
              "مساعد الدراسة بالذكاء الاصطناعي: بناء مسارات تعلم أكثر فاعلية",

            description:
              "تعرّف على كيف تساعد أدوات الدراسة بالذكاء الاصطناعي في إنشاء الملخصات والاختبارات والبطاقات التعليمية ومسارات التعلم المنظمة.",

            datePublished: "2026-05-24",

            dateModified: "2026-05-24",

            inLanguage: "ar",

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
