import type { Metadata } from "next";
import SecurityClient from "../../security/SecurityClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "الأمان والبنية التحتية | Runexa",

  description:
    "تعرّف على ممارسات الأمان لدى Runexa والتشفير وضمانات البنية التحتية وضوابط الوصول وأمان الدفع وحماية منصة الذكاء الاصطناعي.",

  keywords: [
    "أمان الذكاء الاصطناعي",
    "أمان الذكاء الاصطناعي للمؤسسات",
    "بنية الذكاء الاصطناعي",
    "أمان Runexa",
    "أمان منصة الذكاء الاصطناعي",
    "تشفير الذكاء الاصطناعي",
    "حماية بيانات الذكاء الاصطناعي",
    "امتثال الذكاء الاصطناعي للمؤسسات",
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
      "تعرّف على ممارسات الأمان لدى Runexa والتشفير وضمانات البنية التحتية وضوابط الوصول وأمان الدفع وحماية منصة الذكاء الاصطناعي.",

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
      "أمان الذكاء الاصطناعي للمؤسسات والتشفير وضمانات البنية التحتية وحماية منصة الذكاء الاصطناعي من Runexa.",

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

            name: "أمان Runexa",

            description:
              "ممارسات الأمان وحماية البنية التحتية لأنظمة Runexa للذكاء الاصطناعي وسير عمل المؤسسات.",

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
