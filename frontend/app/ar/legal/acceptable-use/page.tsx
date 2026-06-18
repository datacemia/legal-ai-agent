import type { Metadata } from "next";
import AcceptableUseClient from "../../../legal/acceptable-use/AcceptableUseClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "سياسة الاستخدام المقبول | Runexa",

  description:
    "سياسة الاستخدام المقبول من Runexa التي تنظّم الاستخدام القانوني والمسؤول لأنظمة الذكاء الاصطناعي وواجهات API وسير العمل وخدمات المؤسسات.",

  keywords: [
    "سياسة الاستخدام المقبول",
    "سياسة الذكاء الاصطناعي",
    "امتثال الذكاء الاصطناعي",
    "سياسة الذكاء الاصطناعي للمؤسسات",
    "قواعد استخدام الذكاء الاصطناعي",
    "سياسة Runexa",
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
      "سياسة الاستخدام المقبول من Runexa لأنظمة الذكاء الاصطناعي وواجهات API وسير عمل المؤسسات والخدمات الذكية.",

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
      "راجع متطلبات الاستخدام المقبول لخدمات Runexa للذكاء الاصطناعي وأنظمة المؤسسات.",

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

            name: "سياسة الاستخدام المقبول من Runexa",

            description:
              "سياسة استخدام مقبول لخدمات Runexa للذكاء الاصطناعي وواجهات API وسير عمل المؤسسات والأنظمة الذكية.",

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
