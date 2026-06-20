import type { Metadata } from "next";
import HomeClient from "../HomeClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Runexa | منصة ذكاء اصطناعي بوكلاء متخصصين",

  description:
    "Runexa منصة ذكاء اصطناعي تضم وكلاء متخصصين للتحليل القانوني والمالي والتعلّم ودعم قرارات الأعمال.",

  keywords: [
    "منصة ذكاء اصطناعي",
    "وكلاء ذكاء اصطناعي",
    "ذكاء اصطناعي قانوني",
    "ذكاء اصطناعي مالي",
    "ذكاء اصطناعي للتعلم",
    "ذكاء اصطناعي للأعمال",
    "ذكاء اصطناعي للمؤسسات",
    "أتمتة سير العمل بالذكاء الاصطناعي",
    "ذكاء الأعمال بالذكاء الاصطناعي",
    "Runexa",
    "بنية تحتية للذكاء الاصطناعي",

    "Runexa AI",
    "Runexa Systems",
    "وكلاء ذكاء اصطناعي متخصصون",
    "منصة وكلاء الذكاء الاصطناعي",
    "مساحة عمل بالذكاء الاصطناعي",
    "منصة ذكاء اصطناعي للمؤسسات",
    "حلول الذكاء الاصطناعي للمؤسسات",
    "الذكاء الاصطناعي المسؤول",
    "حوكمة الذكاء الاصطناعي",
    "إنتاجية مدعومة بالذكاء الاصطناعي",
    "أتمتة الأعمال بالذكاء الاصطناعي",
    "إدارة المعرفة بالذكاء الاصطناعي",
    "معالجة المستندات بالذكاء الاصطناعي",
    "تحليل المستندات بالذكاء الاصطناعي",
    "دعم اتخاذ القرار بالذكاء الاصطناعي",
    "تحليل البيانات بالذكاء الاصطناعي",
    "التحول الرقمي للمؤسسات",
    "الوكلاء الذكيون",
    "المساعدون الأذكياء",
    "Legal AI",
    "Finance AI",
    "Study AI",
    "Business AI",
    "Runexa Legal Agent",
    "Runexa Finance Coach",
    "Runexa Study Agent",
    "Runexa Business Decision Agent",
    "البنية السحابية للذكاء الاصطناعي",
    "Enterprise AI Platform",
    "AI Workspace",
    "AI Agents Platform",
  ],

  alternates: {
    canonical: `${siteUrl}/ar`,
    languages: {
      en: `${siteUrl}/en`,
      fr: `${siteUrl}/fr`,
      ar: `${siteUrl}/ar`,
      "x-default": siteUrl,
    },
  },

  openGraph: {
    title: "Runexa | منصة ذكاء اصطناعي بوكلاء متخصصين",

    description:
      "وكلاء ذكاء اصطناعي متخصصون للتحليل القانوني والمالي والتعلّم وقرارات الأعمال.",

    url: `${siteUrl}/ar`,

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa AI Workspace",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Runexa | منصة ذكاء اصطناعي بوكلاء متخصصين",

    description:
      "منصة ذكاء اصطناعي للتحليل القانوني والمالي والتعلّم وسير العمل التجاري.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function Page() {
  return (
    <>
      <HomeClient initialLanguage="ar" lockInitialLanguage />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify([
            {
              "@context": "https://schema.org",

              "@type": "Organization",

              name: "Runexa Systems LLC",

              url: siteUrl,

              logo: `${siteUrl}/logo.png`,

              sameAs: [],

              description:
                "منصة ذكاء اصطناعي تضم وكلاء متخصصين للتحليل القانوني والمالي والتعلّم ودعم قرارات الأعمال.",

              knowsAbout: [
                "Artificial Intelligence",
                "Legal AI",
                "Finance AI",
                "Business Intelligence",
                "Study AI",
                "Enterprise AI Workflows",
              ],
            },

            {
              "@context": "https://schema.org",

              "@type": "WebSite",

              name: "Runexa",

              url: `${siteUrl}/ar`,

              inLanguage: "ar",

              publisher: {
                "@type": "Organization",
                name: "Runexa Systems LLC",
                url: siteUrl,
              },
            },
          ]),
        }}
      />
    </>
  );
}
