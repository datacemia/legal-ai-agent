import type { Metadata } from "next";
import TermsClient from "../../terms/TermsClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "شروط الخدمة | Runexa",

  description:
    "شروط الخدمة التي تنظّم استخدام وكلاء Runexa للذكاء الاصطناعي وواجهات API وسير عمل المؤسسات والأرصدة والاشتراكات والخدمات المدعومة بالذكاء الاصطناعي.",

  keywords: [
    "شروط الخدمة",
    "شروط منصة الذكاء الاصطناعي",
    "شروط Runexa",
    "شروط SaaS الذكاء الاصطناعي",
    "شروط API الذكاء الاصطناعي",
    "شروط الذكاء الاصطناعي للمؤسسات",
    "اشتراكات الذكاء الاصطناعي",
    "أرصدة الذكاء الاصطناعي",
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
    title: "شروط الخدمة | Runexa",

    description:
      "شروط تنظّم استخدام أنظمة Runexa للذكاء الاصطناعي وواجهات API وسير عمل الذكاء الاصطناعي للمؤسسات.",

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

    title: "شروط خدمة Runexa",

    description:
      "شروط تنظّم استخدام أنظمة Runexa للذكاء الاصطناعي وواجهات API وسير عمل المؤسسات.",

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

            name: "شروط خدمة Runexa",

            description:
              "شروط تنظّم وكلاء Runexa للذكاء الاصطناعي وواجهات API وسير عمل المؤسسات والخدمات المدعومة بالذكاء الاصطناعي.",

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
