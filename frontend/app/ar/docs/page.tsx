import type { Metadata } from "next";
import DocsClient from "../../docs/DocsClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "توثيق واجهات API للذكاء الاصطناعي | Runexa",

  description:
    "توثيق تقني لواجهات Runexa AI API يشمل التحليل القانوني والذكاء المالي وتدفقات الأعمال والمهام غير المتزامنة والمصادقة وتكاملات المؤسسات.",

  keywords: [
    "توثيق Runexa",
    "توثيق API الذكاء الاصطناعي",
    "توثيق API الذكاء القانوني",
    "توثيق API الذكاء المالي",
    "توثيق API ذكاء الأعمال",
    "توثيق المطورين",
    "واجهات API ذكاء اصطناعي غير متزامنة",
    "تكامل ذكاء اصطناعي للمؤسسات",
  ],

  alternates: {
    canonical: `${siteUrl}/ar/docs`,
    languages: {
      en: `${siteUrl}/en/docs`,
      fr: `${siteUrl}/fr/docs`,
      ar: `${siteUrl}/ar/docs`,
      "x-default": `${siteUrl}/docs`,
    },
  },

  openGraph: {
    title: "توثيق واجهات API للذكاء الاصطناعي | Runexa",

    description:
      "توثيق تقني لواجهات Runexa AI API يشمل التحليل القانوني والذكاء المالي وتدفقات الأعمال والمهام غير المتزامنة والمصادقة وتكاملات المؤسسات.",

    url: `${siteUrl}/ar/docs`,

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa API Documentation",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "توثيق واجهات API للذكاء الاصطناعي | Runexa",

    description:
      "توثيق تقني للمطورين لواجهات Runexa API غير المتزامنة للذكاء الاصطناعي.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function DocsPage() {
  return (
    <>
      <DocsClient initialLocale="ar" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "TechArticle",

            headline: "توثيق واجهات API للذكاء الاصطناعي | Runexa",

            name: "Runexa API Documentation",

            description:
              "توثيق تقني لواجهات Runexa API غير المتزامنة للذكاء الاصطناعي والمصادقة والمهام والتحليل القانوني والذكاء المالي وأتمتة الدراسة وتدفقات الأعمال وتكاملات المؤسسات.",

            url: `${siteUrl}/ar/docs`,

            inLanguage: "ar",

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: siteUrl,
            },

            about: [
              "AI API Documentation",
              "Async AI APIs",
              "Legal AI API Docs",
              "Finance AI API Docs",
              "Business AI API Docs",
              "Enterprise AI Integration",
            ],
          }),
        }}
      />
    </>
  );
}
