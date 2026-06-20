import type { Metadata } from "next";
import AcceptableUseClient from "../../../legal/acceptable-use/AcceptableUseClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "سياسة الاستخدام المقبول | Runexa",

  description:
    "سياسة الاستخدام المقبول من Runexa التي تنظم الاستخدام القانوني والمسؤول والمصرح به لأنظمة الذكاء الاصطناعي وواجهات API والملفات المرفوعة وسير العمل وخدمات المؤسسات.",

 keywords: [
  "سياسة الاستخدام المقبول",
  "سياسة الذكاء الاصطناعي",
  "امتثال الذكاء الاصطناعي",
  "سياسة الذكاء الاصطناعي للمؤسسات",
  "قواعد استخدام الذكاء الاصطناعي",
  "سياسة Runexa",
  "الملفات المرفوعة المصرح بها",
  "الاستخدام المسؤول للذكاء الاصطناعي",
  "قواعد منصة الذكاء الاصطناعي",

  "شروط استخدام الذكاء الاصطناعي",
  "سياسة استخدام منصة Runexa",
  "إرشادات استخدام الذكاء الاصطناعي",
  "حوكمة الذكاء الاصطناعي",
  "الامتثال التنظيمي للذكاء الاصطناعي",
  "أمن الذكاء الاصطناعي",
  "خصوصية الذكاء الاصطناعي",
  "المحتوى المحظور",
  "الاستخدام المسموح به",
  "الملفات المصرح برفعها",
  "تحميل المستندات القانونية",
  "رفع المستندات بالذكاء الاصطناعي",
  "سياسة المحتوى",
  "الاستخدام التجاري للذكاء الاصطناعي",
  "الاستخدام المهني للذكاء الاصطناعي",
  "منصة ذكاء اصطناعي للمؤسسات",
  "وكلاء الذكاء الاصطناعي",
  "الذكاء الاصطناعي المسؤول",
  "إدارة مخاطر الذكاء الاصطناعي",
  "الامتثال القانوني للذكاء الاصطناعي",
  "سياسات المؤسسات للذكاء الاصطناعي",
  "شروط استخدام Runexa",
  "Runexa Acceptable Use Policy",
  "Runexa AI Policy",
  "Enterprise AI Compliance",
  ],

  alternates: {
    canonical: "https://runexa.ai/ar/legal/acceptable-use",
    languages: {
      en: `${siteUrl}/en/legal/acceptable-use`,
      fr: `${siteUrl}/fr/legal/acceptable-use`,
      ar: `${siteUrl}/ar/legal/acceptable-use`,
      "x-default": `${siteUrl}/legal/acceptable-use`,
    },
  },

  openGraph: {
    title: "سياسة الاستخدام المقبول | Runexa",

    description:
      "سياسة الاستخدام المقبول من Runexa التي تنظم الاستخدام القانوني والمسؤول والمصرح به لأنظمة الذكاء الاصطناعي وواجهات API والملفات المرفوعة وسير العمل وخدمات المؤسسات.",

    url: "https://runexa.ai/ar/legal/acceptable-use",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Acceptable Use Policy",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "سياسة الاستخدام المقبول | Runexa",

    description:
      "سياسة الاستخدام المقبول من Runexa التي تنظم الاستخدام القانوني والمسؤول والمصرح به لأنظمة الذكاء الاصطناعي وواجهات API والملفات المرفوعة وسير العمل وخدمات المؤسسات.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function AcceptableUsePage() {
  return (
    <>
      <AcceptableUseClient initialLocale="ar" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "Runexa Acceptable Use Policy",

            description:
              "سياسة الاستخدام المقبول للاستخدام القانوني والمسؤول والمصرح به لخدمات Runexa للذكاء الاصطناعي وواجهات API والملفات المرفوعة وسير عمل المؤسسات والأنظمة الذكية.",

            url: "https://runexa.ai/ar/legal/acceptable-use",

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
