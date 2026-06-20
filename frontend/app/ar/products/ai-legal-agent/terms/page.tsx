import type { Metadata } from "next";
import ProductTermsClient from "../../../../products/ai-legal-agent/terms/ProductTermsClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "شروط منتجات الذكاء الاصطناعي | Runexa Systems LLC",

  description:
    "شروط خاصة بالمنتج وقيود وإخلاءات مسؤولية ومتطلبات مراجعة بشرية وإشعارات معالجة البيانات ومعلومات المسؤولية لوكلاء Runexa للذكاء الاصطناعي.",

keywords: [
  "شروط استخدام الذكاء الاصطناعي",
  "إخلاء مسؤولية الذكاء الاصطناعي",
  "إخلاء مسؤولية قانونية للذكاء الاصطناعي",
  "إخلاء مسؤولية مالية للذكاء الاصطناعي",
  "إخلاء مسؤولية تعليمية للذكاء الاصطناعي",
  "إخلاء مسؤولية تجارية للذكاء الاصطناعي",
  "شروط Runexa",
  "تحديد مسؤولية الذكاء الاصطناعي",
  "المراجعة البشرية لنتائج الذكاء الاصطناعي",
  "شفافية الذكاء الاصطناعي",
  "معالجة بيانات الذكاء الاصطناعي",
  "امتثال الذكاء الاصطناعي للمؤسسات",

  "سياسة الذكاء الاصطناعي",
  "الذكاء الاصطناعي المسؤول",
  "الاستخدام المسؤول للذكاء الاصطناعي",
  "حوكمة الذكاء الاصطناعي",
  "إدارة مخاطر الذكاء الاصطناعي",
  "الإشراف البشري",
  "التحقق من نتائج الذكاء الاصطناعي",
  "حدود الذكاء الاصطناعي",
  "مخاطر الذكاء الاصطناعي",
  "أخطاء الذكاء الاصطناعي",
  "دقة الذكاء الاصطناعي",
  "موثوقية الذكاء الاصطناعي",
  "المحتوى المولد بالذكاء الاصطناعي",
  "دعم اتخاذ القرار بالذكاء الاصطناعي",
  "تحليل قانوني غير مهني",
  "معلومات مالية غير مهنية",
  "محتوى تعليمي مولد بالذكاء الاصطناعي",
  "قرارات أعمال مدعومة بالذكاء الاصطناعي",
  "الإفصاح عن استخدام الذكاء الاصطناعي",
  "الشفافية الخوارزمية",
  "الامتثال التنظيمي للذكاء الاصطناعي",
  "سياسات الذكاء الاصطناعي للمؤسسات",
  "Runexa AI Disclaimer",
  "Runexa AI Policy",
  "Responsible AI",
  "Enterprise AI Governance",
  ],
  alternates: {
    canonical: "https://runexa.ai/ar/products/ai-legal-agent/terms",
    languages: {
      en: `${siteUrl}/en/products/ai-legal-agent/terms`,
      fr: `${siteUrl}/fr/products/ai-legal-agent/terms`,
      ar: `${siteUrl}/ar/products/ai-legal-agent/terms`,
      "x-default": `${siteUrl}/products/ai-legal-agent/terms`,
    },
  },

  openGraph: {
    title: "شروط منتجات الذكاء الاصطناعي | Runexa Systems LLC",

    description:
      "شروط خاصة بالمنتج وقيود وإخلاءات مسؤولية ومتطلبات مراجعة بشرية وإشعارات معالجة البيانات ومعلومات المسؤولية لوكلاء Runexa للذكاء الاصطناعي.",

    url: "https://runexa.ai/ar/products/ai-legal-agent/terms",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa AI Product Terms",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "شروط منتجات الذكاء الاصطناعي | Runexa Systems LLC",

    description:
      "AI product limitations, human review requirements, data-processing notices, and operational terms for Runexa AI systems.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function ProductTermsPage() {
  return (
    <>
      <ProductTermsClient initialLocale="ar" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "شروط منتجات Runexa للذكاء الاصطناعي",

            description:
              "شروط المنتج وإفصاحات قيود الذكاء الاصطناعي ومتطلبات المراجعة البشرية وإشعارات معالجة البيانات وتوضيح تدريب النماذج وعدم تقديم المشورة المهنية لوكلاء Runexa للذكاء الاصطناعي.",

            url: "https://runexa.ai/ar/products/ai-legal-agent/terms",

            inLanguage: "ar",

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
