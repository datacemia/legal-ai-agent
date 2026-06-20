import type { Metadata } from "next";
import FinanceAIClient from "../../finance-ai/FinanceAIClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "تحليل مالي بالذكاء الاصطناعي ومدرب للمالية الشخصية | Runexa",

  description:
    "حلّل كشوف الحساب البنكية، واكتشف الاشتراكات، وحدد فرص الادخار، وحسّن عاداتك المالية باستخدام Runexa Finance AI.",

 keywords: [
  "ذكاء اصطناعي مالي",
  "تحليل مالي بالذكاء الاصطناعي",
  "تحليل كشف حساب بنكي",
  "اكتشاف الاشتراكات بالذكاء الاصطناعي",
  "ذكاء اصطناعي للمالية الشخصية",
  "تحليل الادخار بالذكاء الاصطناعي",
  "Runexa finance AI",
  "مدرب مالي بالذكاء الاصطناعي",

  "Runexa Finance Coach",
  "الذكاء الاصطناعي المالي",
  "إدارة الميزانية الشخصية",
  "مساعد مالي ذكي",
  "مستشار مالي بالذكاء الاصطناعي",
  "تحليل المصروفات",
  "تحليل الإنفاق الشهري",
  "تحليل الدخل والمصروفات",
  "إدارة الأموال الشخصية",
  "التخطيط المالي الذكي",
  "تحسين العادات المالية",
  "تحليل العادات المالية",
  "إدارة الاشتراكات",
  "اكتشاف النفقات المتكررة",
  "تحديد فرص الادخار",
  "إدارة النفقات الشخصية",
  "مراقبة الإنفاق",
  "تحليل الحسابات البنكية",
  "تحليل البيانات المالية",
  "تحليل التدفقات النقدية",
  "لوحة تحكم مالية ذكية",
  "التثقيف المالي",
  "التخطيط للميزانية",
  "تحسين القرارات المالية",
  "إدارة الثروة الشخصية",
  "التمويل الذكي",
  "التحليل المالي الشخصي",
  "إدارة مالية ذكية",
  "مساعد الادخار الذكي",
  "أتمتة الإدارة المالية",
  "الذكاء الاصطناعي للتمويل الشخصي",
  "منصة مالية بالذكاء الاصطناعي",
  "أداة تحليل مالي",
  "Finance AI",
  ],

  alternates: {
    canonical: "https://runexa.ai/ar/finance-ai",
    languages: {
      en: `${siteUrl}/en/finance-ai`,
      fr: `${siteUrl}/fr/finance-ai`,
      ar: `${siteUrl}/ar/finance-ai`,
      "x-default": `${siteUrl}/finance-ai`,
    },
  },

  openGraph: {
    title: "تحليل مالي بالذكاء الاصطناعي ومدرب للمالية الشخصية | Runexa",

    description:
      "حلّل كشوف الحساب البنكية، واكتشف الاشتراكات، وحدد فرص الادخار، وحسّن عاداتك المالية باستخدام Runexa Finance AI.",

    url: "https://runexa.ai/ar/finance-ai",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Finance AI",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "تحليل مالي بالذكاء الاصطناعي ومدرب للمالية الشخصية | Runexa",

    description:
      "تحليل مالي بالذكاء الاصطناعي لكشوف الحسابات والاشتراكات وفرص الادخار والتوجيه المالي الشخصي.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function FinanceAIPage() {
  return (
    <>
      <FinanceAIClient initialLocale="ar" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify([
            {
              "@context": "https://schema.org",

              "@type": "SoftwareApplication",

              name: "Runexa Finance AI",

              applicationCategory: "FinanceApplication",

              operatingSystem: "Web",

              url: "https://runexa.ai/ar/finance-ai",

              inLanguage: "ar",

              description:
                "مدرب مالي بالذكاء الاصطناعي لتحليل الكشوف البنكية واكتشاف الاشتراكات وفرص الادخار والعادات المالية.",

              publisher: {
                "@type": "Organization",
                name: "Runexa Systems LLC",
                url: siteUrl,
              },

              knowsAbout: [
                "Finance AI",
                "AI Financial Analysis",
                "Bank Statement Analysis",
                "Subscription Detection",
                "Personal Finance AI",
                "Financial Coaching AI",
              ],
            },
          ]),
        }}
      />
    </>
  );
}
