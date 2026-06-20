import type { Metadata } from "next";
import SecurityClient from "../../security/SecurityClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "الأمان والبنية التحتية | Runexa",

  description:
    "تعرّف على ممارسات الأمان في Runexa والتشفير وضمانات البنية التحتية وضوابط الوصول وأمان الدفع والرفع المسؤول للملفات وحماية منصة الذكاء الاصطناعي.",

  keywords: [
    "أمن الذكاء الاصطناعي",
    "أمن الذكاء الاصطناعي للمؤسسات",
    "البنية التحتية للذكاء الاصطناعي",
    "أمن Runexa",
    "أمن منصة الذكاء الاصطناعي",
    "تشفير الذكاء الاصطناعي",
    "حماية بيانات الذكاء الاصطناعي",
    "امتثال الذكاء الاصطناعي للمؤسسات",
    "الملفات المرفوعة بشكل مسؤول",
    "سير العمل الآمن للذكاء الاصطناعي",
  ],

  alternates: {
    canonical: "https://runexa.ai/ar/security",
    languages: {
      en: `${siteUrl}/en/security`,
      fr: `${siteUrl}/fr/security`,
      ar: `${siteUrl}/ar/security`,
      "x-default": `${siteUrl}/security`,
    },
  },

  openGraph: {
    title: "الأمان والبنية التحتية | Runexa",

    description:
      "تعرّف على ممارسات الأمان في Runexa والتشفير وضمانات البنية التحتية وضوابط الوصول وأمان الدفع والرفع المسؤول للملفات وحماية منصة الذكاء الاصطناعي.",

    url: "https://runexa.ai/ar/security",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Security",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "الأمان والبنية التحتية | Runexa",

    description:
      "تعرّف على ممارسات الأمان في Runexa والتشفير وضمانات البنية التحتية وضوابط الوصول وأمان الدفع والرفع المسؤول للملفات وحماية منصة الذكاء الاصطناعي.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function SecurityPage() {
  return (
    <>
      <SecurityClient initialLocale="ar" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "Runexa Security",

            description:
              "ممارسات الأمان وإرشادات الرفع المسؤول وحماية البنية التحتية لأنظمة Runexa للذكاء الاصطناعي وسير عمل الذكاء الاصطناعي للمؤسسات.",

            url: "https://runexa.ai/ar/security",

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
