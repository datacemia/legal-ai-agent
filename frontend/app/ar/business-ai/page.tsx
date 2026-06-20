import type { Metadata } from "next";
import BusinessAIClient from "../../business-ai/BusinessAIClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "ذكاء الأعمال ودعم القرار بالذكاء الاصطناعي | Runexa",

  description:
    "حلّل بيانات الأعمال، واكتشف المخاطر والفرص، وحسّن القرارات الاستراتيجية باستخدام Runexa Business AI.",

  keywords: [
    "ذكاء اصطناعي للأعمال",
    "ذكاء الأعمال بالذكاء الاصطناعي",
    "دعم اتخاذ القرار",
    "تحليل مؤشرات الأداء بالذكاء الاصطناعي",
    "تحليل مخاطر الأعمال",
    "التوقعات بالذكاء الاصطناعي",
    "Runexa business AI",
    "سير عمل الأعمال بالذكاء الاصطناعي",

    "Runexa Business Decision Agent",
    "وكيل الأعمال بالذكاء الاصطناعي",
    "تحليل البيانات التجارية",
    "تحليل الأداء المؤسسي",
    "التحليل الاستراتيجي بالذكاء الاصطناعي",
    "إدارة الأداء المؤسسي",
    "مؤشرات الأداء الرئيسية KPI",
    "لوحات المعلومات التنفيذية",
    "التقارير التنفيذية الذكية",
    "تحليل اتجاهات السوق",
    "تحليل المنافسين",
    "تحليل الفرص التجارية",
    "إدارة المخاطر بالذكاء الاصطناعي",
    "التخطيط الاستراتيجي",
    "التنبؤ بالإيرادات",
    "تحليل الربحية",
    "تحسين الأداء التشغيلي",
    "أتمتة التحليل التجاري",
    "تحليل الشركات بالذكاء الاصطناعي",
    "الذكاء الاصطناعي للمديرين التنفيذيين",
    "ذكاء الأعمال للمؤسسات",
    "إدارة الأعمال الذكية",
    "تحليل البيانات المؤسسية",
    "رؤى الأعمال بالذكاء الاصطناعي",
    "التحول الرقمي للأعمال",
    "منصة ذكاء الأعمال",
    "مساعد اتخاذ القرار بالذكاء الاصطناعي",
    "دعم الإدارة التنفيذية",
    "الذكاء الاصطناعي للمؤسسات",
    "Business Intelligence AI",
  ],

  alternates: {
    canonical: "https://runexa.ai/ar/business-ai",
    languages: {
      en: `${siteUrl}/en/business-ai`,
      fr: `${siteUrl}/fr/business-ai`,
      ar: `${siteUrl}/ar/business-ai`,
      "x-default": `${siteUrl}/business-ai`,
    },
  },

  openGraph: {
    title: "ذكاء الأعمال ودعم القرار بالذكاء الاصطناعي | Runexa",

    description:
      "حلّل بيانات الأعمال، واكتشف المخاطر والفرص، وحسّن القرارات الاستراتيجية باستخدام Runexa Business AI.",

    url: "https://runexa.ai/ar/business-ai",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Business AI",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "ذكاء الأعمال ودعم القرار بالذكاء الاصطناعي | Runexa",

    description:
      "ذكاء أعمال مدعوم بالذكاء الاصطناعي لتحليل مؤشرات الأداء، والرؤى الاستراتيجية، والتوقعات، ودعم القرار التشغيلي.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function BusinessAIPage() {
  return (
    <>
      <BusinessAIClient initialLocale="ar" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify([
            {
              "@context": "https://schema.org",

              "@type": "SoftwareApplication",

              name: "Runexa Business AI",

              applicationCategory: "BusinessApplication",

              operatingSystem: "Web",

              url: "https://runexa.ai/ar/business-ai",

              inLanguage: "ar",

              description:
                "برنامج ذكاء أعمال ودعم قرار بالذكاء الاصطناعي لتحليل مؤشرات الأداء واكتشاف المخاطر والفرص والتوقعات والرؤى التشغيلية.",

              publisher: {
                "@type": "Organization",
                name: "Runexa Systems LLC",
                url: siteUrl,
              },

              knowsAbout: [
                "Business AI",
                "AI Business Intelligence",
                "Decision Support",
                "KPI Analysis",
                "Business Risk Analysis",
                "AI Forecasting",
              ],
            },
          ]),
        }}
      />
    </>
  );
}
