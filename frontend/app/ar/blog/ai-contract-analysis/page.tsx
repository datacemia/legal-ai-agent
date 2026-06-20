import type { Metadata } from "next";
import AIContractAnalysisArticle from "../../../blog/ai-contract-analysis/AIContractAnalysisArticle";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "تحليل العقود بالذكاء الاصطناعي: كيف يساعد الذكاء الاصطناعي في مراجعة المستندات القانونية | Runexa",

  description:
    "تعرّف على كيف يساعد تحليل العقود بالذكاء الاصطناعي في تحديد البنود الخطرة وتلخيص الالتزامات ودعم سير عمل مراجعة المستندات القانونية.",

  keywords: [
    "تحليل العقود بالذكاء الاصطناعي",
    "مراجعة العقود بالذكاء الاصطناعي",
    "تحليل المستندات القانونية",
    "الذكاء الاصطناعي القانوني",
    "اكتشاف مخاطر العقود",
    "مساعد قانوني بالذكاء الاصطناعي",
    "ملخصات العقود",
    "Runexa Legal Agent",

    "تحليل البنود التعاقدية",
    "اكتشاف البنود الخطرة",
    "تقييم المخاطر القانونية",
    "مراجعة الوثائق القانونية",
    "تحليل الاتفاقيات القانونية",
    "فحص العقود",
    "قراءة العقود بذكاء",
    "تحليل الشروط والأحكام",
    "تلخيص المستندات القانونية",
    "إدارة العقود",
    "الامتثال التعاقدي",
    "تحليل الالتزامات القانونية",
    "تحليل المسؤوليات التعاقدية",
    "تحليل المخاطر التجارية",
    "التحقق من العقود",
    "دعم اتخاذ القرار القانوني",
    "الأتمتة القانونية",
    "سير العمل القانوني بالذكاء الاصطناعي",
    "تقنية القانون",
    "LegalTech",
    "ذكاء اصطناعي للمحامين",
    "أداة تحليل قانوني",
    "تحليل المستندات بالذكاء الاصطناعي",
    "مراجعة العقود التجارية",
    "فهم العقود القانونية",
    "Runexa Legal AI",
  ],

  alternates: {
    canonical: "https://runexa.ai/ar/blog/ai-contract-analysis",
    languages: {
      en: `${siteUrl}/en/blog/ai-contract-analysis`,
      fr: `${siteUrl}/fr/blog/ai-contract-analysis`,
      ar: `${siteUrl}/ar/blog/ai-contract-analysis`,
      "x-default": `${siteUrl}/blog/ai-contract-analysis`,
    },
  },

  openGraph: {
    title: "تحليل العقود بالذكاء الاصطناعي: كيف يساعد الذكاء الاصطناعي في مراجعة المستندات القانونية | Runexa",

    description:
      "تعرّف على كيف يساعد تحليل العقود بالذكاء الاصطناعي في تحديد البنود الخطرة وتلخيص الالتزامات ودعم سير عمل مراجعة المستندات القانونية.",

    url: "https://runexa.ai/ar/blog/ai-contract-analysis",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa AI Contract Analysis",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "article",
  },

  twitter: {
    card: "summary_large_image",

    title: "تحليل العقود بالذكاء الاصطناعي: كيف يساعد الذكاء الاصطناعي في مراجعة المستندات القانونية | Runexa",

    description:
      "تعرّف على كيف يساعد تحليل العقود بالذكاء الاصطناعي في تحديد البنود الخطرة وتلخيص الالتزامات ودعم سير عمل مراجعة المستندات القانونية.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function AIContractAnalysisPage() {
  return (
    <>
      <AIContractAnalysisArticle initialLocale="ar" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "Article",

            mainEntityOfPage: {
              "@type": "WebPage",
              "@id": "https://runexa.ai/ar/blog/ai-contract-analysis",
            },

            headline:
              "تحليل العقود بالذكاء الاصطناعي: كيف يساعد الذكاء الاصطناعي في مراجعة المستندات القانونية",

            description:
              "تعرّف على كيف يساعد تحليل العقود بالذكاء الاصطناعي في تحديد البنود الخطرة وتلخيص الالتزامات ودعم سير عمل مراجعة المستندات القانونية.",

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
