import type { Metadata } from "next";
import AIFinanceAnalysisArticle from "../../../blog/ai-finance-analysis/AIFinanceAnalysisArticle";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "التحليل المالي بالذكاء الاصطناعي: فهم الإنفاق والاشتراكات وفرص الادخار | Runexa",

  description:
    "تعرّف على كيف يساعد التحليل المالي بالذكاء الاصطناعي المستخدمين على فهم أنماط الإنفاق والاشتراكات وفرص الادخار والعادات المالية.",

  keywords: [
    "التحليل المالي بالذكاء الاصطناعي",
    "التمويل الشخصي بالذكاء الاصطناعي",
    "تحليل كشف بنكي",
    "اكتشاف الاشتراكات بالذكاء الاصطناعي",
    "تحليل الادخار بالذكاء الاصطناعي",
    "العادات المالية بالذكاء الاصطناعي",
    "Runexa Finance Coach",
    "مساعد الميزانية بالذكاء الاصطناعي",
  ],

  alternates: {
    canonical: "https://runexa.ai/ar/blog/ai-finance-analysis",
    languages: {
      en: `${siteUrl}/en/blog/ai-finance-analysis`,
      fr: `${siteUrl}/fr/blog/ai-finance-analysis`,
      ar: `${siteUrl}/ar/blog/ai-finance-analysis`,
      "x-default": `${siteUrl}/blog/ai-finance-analysis`,
    },
  },

  openGraph: {
    title: "التحليل المالي بالذكاء الاصطناعي: فهم الإنفاق والاشتراكات وفرص الادخار | Runexa",

    description:
      "تعرّف على كيف يساعد التحليل المالي بالذكاء الاصطناعي المستخدمين على فهم أنماط الإنفاق والاشتراكات وفرص الادخار والعادات المالية.",

    url: "https://runexa.ai/ar/blog/ai-finance-analysis",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa AI Finance Analysis",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "article",
  },

  twitter: {
    card: "summary_large_image",

    title: "التحليل المالي بالذكاء الاصطناعي: فهم الإنفاق والاشتراكات وفرص الادخار | Runexa",

    description:
      "تعرّف على كيف يساعد التحليل المالي بالذكاء الاصطناعي المستخدمين على فهم أنماط الإنفاق والاشتراكات وفرص الادخار والعادات المالية.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function AIFinanceAnalysisPage() {
  return (
    <>
      <AIFinanceAnalysisArticle initialLocale="ar" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "Article",

            mainEntityOfPage: {
              "@type": "WebPage",
              "@id": "https://runexa.ai/ar/blog/ai-finance-analysis",
            },

            headline:
              "التحليل المالي بالذكاء الاصطناعي: فهم الإنفاق والاشتراكات وفرص الادخار",

            description:
              "تعرّف على كيف يساعد التحليل المالي بالذكاء الاصطناعي المستخدمين على فهم أنماط الإنفاق والاشتراكات وفرص الادخار والعادات المالية.",

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
