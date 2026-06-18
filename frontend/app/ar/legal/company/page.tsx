import type { Metadata } from "next";
import CompanyClient from "../../../legal/company/CompanyClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "معلومات الشركة | Runexa",

  description:
    "معلومات رسمية عن Runexa Systems LLC، بما في ذلك العنوان المسجل وبيانات الاتصال والخدمات والقانون الحاكم.",

  keywords: [
    "Runexa Systems LLC",
    "معلومات شركة Runexa",
    "اتصال Runexa",
    "العنوان المسجل Runexa",
    "معلومات شركة ذكاء اصطناعي",
    "شركة ذكاء اصطناعي للمؤسسات",
    "معلومات Runexa القانونية",
  ],

  alternates: {
    canonical: "https://runexa.ai/ar/legal/company",
    languages: {
      en: `${siteUrl}/en/legal/company`,
      fr: `${siteUrl}/fr/legal/company`,
      ar: `${siteUrl}/ar/legal/company`,
      "x-default": `${siteUrl}/legal/company`,
    },
  },

  openGraph: {
    title: "معلومات الشركة | Runexa",

    description:
      "معلومات رسمية عن Runexa Systems LLC، بما في ذلك العنوان المسجل وبيانات الاتصال والخدمات والقانون الحاكم.",

    url: "https://runexa.ai/ar/legal/company",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Systems LLC",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "معلومات الشركة | Runexa",

    description:
      "تفاصيل الشركة الرسمية والعنوان والقانون الحاكم ومعلومات الاتصال الخاصة بـ Runexa Systems LLC.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function CompanyPage() {
  return (
    <>
      <CompanyClient initialLocale="ar" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "Organization",

            name: "Runexa Systems LLC",

            url: siteUrl,

            email: "contact@runexa.ai",

            address: {
              "@type": "PostalAddress",
              streetAddress: "1309 Coffeen Avenue, Suite 1200",
              addressLocality: "Sheridan",
              addressRegion: "WY",
              postalCode: "82801",
              addressCountry: "US",
            },

            sameAs: [siteUrl],

            description:
              "تقوم Runexa Systems LLC بتطوير وتشغيل أدوات مدعومة بالذكاء الاصطناعي ووكلاء ذكاء اصطناعي وسير عمل للمؤسسات وخدمات برمجية ذكية.",
          }),
        }}
      />
    </>
  );
}
