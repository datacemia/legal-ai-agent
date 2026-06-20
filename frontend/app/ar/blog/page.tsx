import type { Metadata } from "next";
import BlogClient from "../../blog/BlogClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "مدونة ورؤى الذكاء الاصطناعي للمؤسسات | Runexa",

  description:
    "رؤى حول الذكاء القانوني والذكاء المالي وتدفقات عمل الذكاء الاصطناعي للمؤسسات وذكاء الأعمال والأنظمة التشغيلية المدعومة بالذكاء الاصطناعي.",

  keywords: [
    "مدونة الذكاء الاصطناعي",
    "الذكاء الاصطناعي للمؤسسات",
    "الذكاء القانوني",
    "الذكاء المالي",
    "تدفقات عمل الذكاء الاصطناعي",
    "ذكاء الأعمال بالذكاء الاصطناعي",
    "مدونة Runexa",
    "رؤى أتمتة الذكاء الاصطناعي",

    "أخبار الذكاء الاصطناعي",
    "مقالات الذكاء الاصطناعي",
    "التحول الرقمي",
    "أتمتة الأعمال",
    "إنتاجية الذكاء الاصطناعي",
    "وكلاء الذكاء الاصطناعي",
    "الذكاء الاصطناعي المسؤول",
    "حوكمة الذكاء الاصطناعي",
    "استخدام الذكاء الاصطناعي في الشركات",
    "حلول الذكاء الاصطناعي للمؤسسات",
    "Legal AI",
    "Finance AI",
    "Study AI",
    "Business AI",
    "تحليل العقود بالذكاء الاصطناعي",
    "مراجعة العقود بالذكاء الاصطناعي",
    "تحليل مالي بالذكاء الاصطناعي",
    "التعليم بالذكاء الاصطناعي",
    "التعلم الذكي",
    "دعم اتخاذ القرار بالذكاء الاصطناعي",
    "تحليل مؤشرات الأداء",
    "التحليل الاستراتيجي بالذكاء الاصطناعي",
    "أتمتة المستندات",
    "معالجة المستندات بالذكاء الاصطناعي",
    "أدوات الذكاء الاصطناعي",
    "أفضل ممارسات الذكاء الاصطناعي",
    "الامتثال للذكاء الاصطناعي",
    "أمن الذكاء الاصطناعي",
    "خصوصية الذكاء الاصطناعي",
    "Runexa AI",
    "Runexa Systems",
  ],

  alternates: {
    canonical: "https://runexa.ai/ar/blog",
    languages: {
      en: `${siteUrl}/en/blog`,
      fr: `${siteUrl}/fr/blog`,
      ar: `${siteUrl}/ar/blog`,
      "x-default": `${siteUrl}/blog`,
    },
  },

  openGraph: {
    title: "مدونة ورؤى الذكاء الاصطناعي للمؤسسات | Runexa",

    description:
      "رؤى حول الذكاء القانوني والذكاء المالي وتدفقات عمل الذكاء الاصطناعي للمؤسسات وذكاء الأعمال والأنظمة التشغيلية المدعومة بالذكاء الاصطناعي.",

    url: "https://runexa.ai/ar/blog",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa AI Blog",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "مدونة ورؤى الذكاء الاصطناعي للمؤسسات | Runexa",

    description:
      "رؤى حول الذكاء القانوني والذكاء المالي وتدفقات عمل الذكاء الاصطناعي للمؤسسات وذكاء الأعمال والأنظمة التشغيلية المدعومة بالذكاء الاصطناعي.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function BlogPage() {
  return (
    <>
      <BlogClient initialLocale="ar" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "Blog",

            name: "مدونة Runexa للذكاء الاصطناعي",

            description:
              "رؤى حول الذكاء القانوني والذكاء المالي وتدفقات عمل الذكاء الاصطناعي للمؤسسات وذكاء الأعمال والأنظمة التشغيلية المدعومة بالذكاء الاصطناعي.",

            url: "https://runexa.ai/ar/blog",

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
