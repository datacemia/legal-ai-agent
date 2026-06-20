import type { Metadata } from "next";
import EnterpriseAIClient from "../../enterprise-ai/EnterpriseAIClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "مساحة ذكاء اصطناعي للمؤسسات وأنظمة مخصصة | Runexa",

  description:
    "تدفقات عمل آمنة بالذكاء الاصطناعي للمؤسسات للتحليل القانوني والتقارير المالية وذكاء الأعمال وعمليات التعلم ودعم القرار المؤسسي.",

 keywords: [
  "ذكاء اصطناعي للمؤسسات",
  "أنظمة ذكاء اصطناعي مخصصة",
  "مساحة عمل بالذكاء الاصطناعي",
  "تدفقات عمل بالذكاء الاصطناعي",
  "ذكاء الأعمال بالذكاء الاصطناعي",
  "ذكاء اصطناعي تنظيمي",
  "Runexa enterprise AI",
  "دعم القرار بالذكاء الاصطناعي",

  "منصة ذكاء اصطناعي للمؤسسات",
  "حلول الذكاء الاصطناعي للمؤسسات",
  "وكلاء ذكاء اصطناعي متخصصون",
  "أتمتة العمليات بالذكاء الاصطناعي",
  "إدارة المعرفة بالذكاء الاصطناعي",
  "التحول الرقمي للمؤسسات",
  "مساعد مؤسسي بالذكاء الاصطناعي",
  "إنتاجية المؤسسات بالذكاء الاصطناعي",
  "تحليل البيانات المؤسسية",
  "إدارة المستندات بالذكاء الاصطناعي",
  "معالجة المستندات بالذكاء الاصطناعي",
  "البنية التحتية للذكاء الاصطناعي",
  "الذكاء الاصطناعي المسؤول",
  "حوكمة الذكاء الاصطناعي",
  "امتثال الذكاء الاصطناعي",
  "أمن الذكاء الاصطناعي",
  "الذكاء الاصطناعي للأعمال",
  "دعم الإدارة التنفيذية",
  "تحليل مؤشرات الأداء KPI",
  "تحليل المخاطر بالذكاء الاصطناعي",
  "التحليل الاستراتيجي بالذكاء الاصطناعي",
  "التنبؤ بالأعمال بالذكاء الاصطناعي",
  "ذكاء الأعمال للمؤسسات",
  "منصة عمل ذكية",
  "مساحة عمل رقمية مدعومة بالذكاء الاصطناعي",
  "وكلاء الذكاء الاصطناعي للمؤسسات",
  "Runexa AI Workspace",
  "Runexa Systems",
  "Enterprise AI Platform",
  "Enterprise AI Solutions",
  ],

  alternates: {
    canonical: "https://runexa.ai/ar/enterprise-ai",
    languages: {
      en: `${siteUrl}/en/enterprise-ai`,
      fr: `${siteUrl}/fr/enterprise-ai`,
      ar: `${siteUrl}/ar/enterprise-ai`,
      "x-default": `${siteUrl}/enterprise-ai`,
    },
  },

  openGraph: {
    title: "مساحة ذكاء اصطناعي للمؤسسات وأنظمة مخصصة | Runexa",

    description:
      "تدفقات عمل آمنة بالذكاء الاصطناعي للمؤسسات للتحليل القانوني والتقارير المالية وذكاء الأعمال وعمليات التعلم ودعم القرار المؤسسي.",

    url: "https://runexa.ai/ar/enterprise-ai",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Enterprise AI",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "مساحة ذكاء اصطناعي للمؤسسات وأنظمة مخصصة | Runexa",

    description:
      "تدفقات عمل ذكاء اصطناعي للمؤسسات لتحليل المستندات والذكاء المالي وعمليات التعلم ودعم قرارات الأعمال.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function EnterpriseAIPage() {
  return (
    <>
      <EnterpriseAIClient initialLocale="ar" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify([
            {
              "@context": "https://schema.org",

              "@type": "SoftwareApplication",

              name: "Runexa Enterprise AI",

              applicationCategory: "BusinessApplication",

              operatingSystem: "Web",

              url: "https://runexa.ai/ar/enterprise-ai",

              inLanguage: "ar",

              description:
                "مساحة ذكاء اصطناعي للمؤسسات لتحليل المستندات والتقارير المالية وتدفقات التعلم وذكاء الأعمال ودعم القرار.",

              publisher: {
                "@type": "Organization",
                name: "Runexa Systems LLC",
                url: siteUrl,
              },

              knowsAbout: [
                "Enterprise AI",
                "Custom AI Systems",
                "AI Workspace",
                "Enterprise AI Workflows",
                "Business Intelligence AI",
                "AI Decision Support",
              ],
            },
          ]),
        }}
      />
    </>
  );
}
