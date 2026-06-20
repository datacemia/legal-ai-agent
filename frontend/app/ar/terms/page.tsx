import type { Metadata } from "next";
import TermsClient from "../../terms/TermsClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "شروط الاستخدام | Runexa",

  description:
    "شروط الاستخدام التي تنظم وكلاء Runexa للذكاء الاصطناعي وواجهات API والملفات المرفوعة والأرصدة والاشتراكات واستخدام القاصرين والفوترة والخدمات المدعومة بالذكاء الاصطناعي.",

  keywords: [
    "شروط الاستخدام",
    "شروط منصة الذكاء الاصطناعي",
    "شروط Runexa",
    "شروط خدمات SaaS للذكاء الاصطناعي",
    "شروط استخدام واجهة برمجة تطبيقات الذكاء الاصطناعي",
    "شروط الذكاء الاصطناعي للمؤسسات",
    "اشتراكات الذكاء الاصطناعي",
    "أرصدة الذكاء الاصطناعي",
    "استخدام القاصرين",
    "الملفات المرفوعة إلى الذكاء الاصطناعي",
    "شروط الفوترة",
  ],

  alternates: {
    canonical: "https://runexa.ai/ar/terms",
    languages: {
      en: `${siteUrl}/en/terms`,
      fr: `${siteUrl}/fr/terms`,
      ar: `${siteUrl}/ar/terms`,
      "x-default": `${siteUrl}/terms`,
    },
  },

  openGraph: {
    title: "شروط الاستخدام | Runexa",

    description:
      "شروط الاستخدام التي تنظم وكلاء Runexa للذكاء الاصطناعي وواجهات API والملفات المرفوعة والأرصدة والاشتراكات واستخدام القاصرين والفوترة والخدمات المدعومة بالذكاء الاصطناعي.",

    url: "https://runexa.ai/ar/terms",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Terms of Service",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "شروط الاستخدام | Runexa",

    description:
      "شروط الاستخدام التي تنظم وكلاء Runexa للذكاء الاصطناعي وواجهات API والملفات المرفوعة والأرصدة والاشتراكات واستخدام القاصرين والفوترة والخدمات المدعومة بالذكاء الاصطناعي.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function TermsPage() {
  return (
    <>
      <TermsClient initialLocale="ar" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "Runexa Terms of Service",

            description:
              "الشروط التي تنظم وكلاء Runexa للذكاء الاصطناعي وواجهات API والملفات المرفوعة وسير عمل المؤسسات والأرصدة والاشتراكات واستخدام القاصرين والفوترة والخدمات المدعومة بالذكاء الاصطناعي.",

            url: "https://runexa.ai/ar/terms",

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
