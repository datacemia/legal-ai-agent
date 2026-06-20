import type { Metadata } from "next";
import CookiePolicyClient from "../../../legal/cookies/CookiePolicyClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "سياسة ملفات تعريف الارتباط | Runexa",

  description:
    "سياسة ملفات تعريف الارتباط التي توضّح كيف تستخدم Runexa Systems LLC ملفات تعريف الارتباط والتحليلات والمصادقة وتقنيات الأمان والخدمات المرتبطة عبر منصات الذكاء الاصطناعي.",

  keywords: [
    "سياسة ملفات تعريف الارتباط",
    "ملفات تعريف ارتباط Runexa",
    "ملفات تعريف ارتباط منصة الذكاء الاصطناعي",
    "ملفات تعريف ارتباط الموقع",
    "ملفات تعريف ارتباط التحليلات",
    "ملفات تعريف ارتباط الخصوصية",
    "ملفات تعريف ارتباط الأمان",
    "امتثال الذكاء الاصطناعي للمؤسسات",

    "ملفات تعريف الارتباط",
    "إعدادات ملفات تعريف الارتباط",
    "إدارة ملفات تعريف الارتباط",
    "ملفات تعريف الارتباط الأساسية",
    "ملفات تعريف الارتباط الوظيفية",
    "ملفات تعريف الارتباط الإحصائية",
    "ملفات تعريف الارتباط التسويقية",
    "ملفات تعريف الارتباط الخاصة بالأداء",
    "ملفات تعريف الارتباط الخاصة بالجلسات",
    "تتبع استخدام الموقع",
    "تحليلات الموقع الإلكتروني",
    "حماية الخصوصية",
    "خصوصية المستخدم",
    "أمن البيانات",
    "إدارة موافقة ملفات تعريف الارتباط",
    "الامتثال للخصوصية",
    "امتثال GDPR",
    "امتثال UK GDPR",
    "سياسة الخصوصية",
    "أمان منصة الذكاء الاصطناعي",
    "منصة ذكاء اصطناعي للمؤسسات",
    "Runexa Cookie Policy",
    "Runexa Privacy",
    "Runexa Security",
    "إدارة تفضيلات ملفات تعريف الارتباط",
    "شفافية البيانات",
    "سياسة التتبع",
    "ملفات تعريف ارتباط الطرف الثالث",
    "ملفات تعريف ارتباط التحليلات",
    "سياسة بيانات Runexa",
  ],

  alternates: {
    canonical: "https://runexa.ai/ar/legal/cookies",
    languages: {
      en: `${siteUrl}/en/legal/cookies`,
      fr: `${siteUrl}/fr/legal/cookies`,
      ar: `${siteUrl}/ar/legal/cookies`,
      "x-default": `${siteUrl}/legal/cookies`,
    },
  },

  openGraph: {
    title: "سياسة ملفات تعريف الارتباط | Runexa",

    description:
      "راجع كيف تستخدم Runexa Systems LLC ملفات تعريف الارتباط والتحليلات والمصادقة وتقنيات الأمان عبر منصات الذكاء الاصطناعي.",

    url: "https://runexa.ai/ar/legal/cookies",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Cookie Policy",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "سياسة ملفات تعريف الارتباط | Runexa",

    description:
      "راجع استخدام ملفات تعريف الارتباط وتقنيات التحليلات وأنظمة المصادقة وخدمات الأمان المستخدمة من Runexa.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function CookiePolicyPage() {
  return (
    <>
      <CookiePolicyClient initialLocale="ar" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "سياسة ملفات تعريف الارتباط من Runexa",

            description:
              "إفصاحات حول استخدام ملفات تعريف الارتباط وتقنيات التحليلات وأنظمة المصادقة وتتبع المتصفح لخدمات Runexa للذكاء الاصطناعي ومنصات المؤسسات.",

            url: "https://runexa.ai/ar/legal/cookies",

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
