import type { Metadata } from "next";
import EnterpriseAIWorkflowsArticle from "../../../blog/enterprise-ai-workflows/EnterpriseAIWorkflowsArticle";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "تدفقات عمل الذكاء الاصطناعي للمؤسسات: بناء عمليات مدعومة بالذكاء الاصطناعي | Runexa",

  description:
    "تعرّف على كيف تساعد تدفقات عمل الذكاء الاصطناعي للمؤسسات على أتمتة التحليل وتحسين اتخاذ القرار وتقليل العمل المتكرر وتوسيع الذكاء التشغيلي.",

  keywords: [
    "تدفقات عمل الذكاء الاصطناعي للمؤسسات",
    "الذكاء الاصطناعي للمؤسسات",
    "عمليات مدعومة بالذكاء الاصطناعي",
    "أتمتة سير العمل بالذكاء الاصطناعي",
    "ذكاء المستندات بالذكاء الاصطناعي",
    "دعم القرار بالذكاء الاصطناعي",
    "Runexa enterprise AI",
    "سير عمل الأعمال بالذكاء الاصطناعي",
  ],

  alternates: {
    canonical: "https://runexa.ai/ar/blog/enterprise-ai-workflows",
    languages: {
      en: `${siteUrl}/en/blog/enterprise-ai-workflows`,
      fr: `${siteUrl}/fr/blog/enterprise-ai-workflows`,
      ar: `${siteUrl}/ar/blog/enterprise-ai-workflows`,
      "x-default": `${siteUrl}/blog/enterprise-ai-workflows`,
    },
  },

  openGraph: {
    title: "تدفقات عمل الذكاء الاصطناعي للمؤسسات: بناء عمليات مدعومة بالذكاء الاصطناعي | Runexa",

    description:
      "تعرّف على كيف تساعد تدفقات عمل الذكاء الاصطناعي للمؤسسات على أتمتة التحليل وتحسين اتخاذ القرار وتقليل العمل المتكرر وتوسيع الذكاء التشغيلي.",

    url: "https://runexa.ai/ar/blog/enterprise-ai-workflows",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Enterprise AI Workflows",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "article",
  },

  twitter: {
    card: "summary_large_image",

    title: "تدفقات عمل الذكاء الاصطناعي للمؤسسات: بناء عمليات مدعومة بالذكاء الاصطناعي | Runexa",

    description:
      "تعرّف على كيف تساعد تدفقات عمل الذكاء الاصطناعي للمؤسسات على أتمتة التحليل وتحسين اتخاذ القرار وتقليل العمل المتكرر وتوسيع الذكاء التشغيلي.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function EnterpriseAIWorkflowsPage() {
  return (
    <>
      <EnterpriseAIWorkflowsArticle initialLocale="ar" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "Article",

            mainEntityOfPage: {
              "@type": "WebPage",
              "@id": "https://runexa.ai/ar/blog/enterprise-ai-workflows",
            },

            headline:
              "تدفقات عمل الذكاء الاصطناعي للمؤسسات: كيف تبني المؤسسات عمليات مدعومة بالذكاء الاصطناعي",

            description:
              "تعرّف على كيف تساعد تدفقات عمل الذكاء الاصطناعي للمؤسسات على أتمتة التحليل وتحسين اتخاذ القرار وتقليل العمل المتكرر وتوسيع الذكاء التشغيلي.",

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
