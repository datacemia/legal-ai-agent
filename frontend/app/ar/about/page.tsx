import type { Metadata } from "next";
import AboutClient from "../../about/AboutClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "عن Runexa | قصة المؤسس ووكلاء الذكاء الاصطناعي المتخصصون",

  description:
    "تعرّف على سبب إنشاء الدكتور رشيد الجامعي لشركة Runexa Systems LLC وكيف ألهمت التحديات الواقعية تطوير Study Agent وLegal Agent وFinance Coach وBusiness Decision Agent.",

  keywords: [
    "Runexa",
    "Runexa Systems LLC",
    "الدكتور رشيد الجامعي",
    "د. رشيد الجامعي",
    "تم الإنشاء بواسطة الدكتور رشيد الجامعي",
    "مؤسس Runexa",
    "وكلاء الذكاء الاصطناعي",
    "وكلاء ذكاء اصطناعي متخصصون",
    "مساحة عمل الذكاء الاصطناعي",
    "وكيل قانوني بالذكاء الاصطناعي",
    "مدرب مالي بالذكاء الاصطناعي",
    "وكيل ذكاء اصطناعي للدراسة",
    "ذكاء اصطناعي لدعم القرارات التجارية",
    "الذكاء الاصطناعي المسؤول",
    "الذكاء الاصطناعي للمؤسسات",
  ],

  alternates: {
    canonical: "https://runexa.ai/ar/about",
    languages: {
      en: `${siteUrl}/en/about`,
      fr: `${siteUrl}/fr/about`,
      ar: `${siteUrl}/ar/about`,
      "x-default": `${siteUrl}/about`,
    },
  },

  openGraph: {
    title: "عن Runexa | قصة المؤسس ووكلاء الذكاء الاصطناعي المتخصصون",

    description:
      "تعرّف على سبب إنشاء الدكتور رشيد الجامعي لشركة Runexa Systems LLC وكيف ألهمت التحديات الواقعية تطوير Study Agent وLegal Agent وFinance Coach وBusiness Decision Agent.",

    url: "https://runexa.ai/ar/about",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "About Runexa Systems",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "عن Runexa | قصة المؤسس ووكلاء الذكاء الاصطناعي المتخصصون",

    description:
      "تعرّف على سبب إنشاء الدكتور رشيد الجامعي لشركة Runexa Systems LLC وكيف ألهمت التحديات الواقعية تطوير Study Agent وLegal Agent وFinance Coach وBusiness Decision Agent.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function AboutPage() {
  return (
    <>
      <AboutClient initialLocale="ar" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify([
            {
              "@context": "https://schema.org",

              "@type": "AboutPage",

              name: "عن Runexa | قصة المؤسس ووكلاء الذكاء الاصطناعي المتخصصون",

              description:
                "تعرّف على سبب إنشاء الدكتور رشيد الجامعي لشركة Runexa Systems LLC وكيف ألهمت التحديات الواقعية تطوير Study Agent وLegal Agent وFinance Coach وBusiness Decision Agent.",

              url: "https://runexa.ai/ar/about",

              inLanguage: "ar",

              publisher: {
                "@type": "Organization",
                name: "Runexa Systems LLC",
                url: siteUrl,
              },
            },
            {
              "@context": "https://schema.org",

              "@type": "Organization",

              name: "Runexa Systems LLC",

              url: siteUrl,

              founder: {
                "@type": "Person",
                name: "الدكتور رشيد الجامعي",
                alternateName: "Dr. Rachid Ejjami",
                jobTitle: "المؤسس والعضو المدير",
              },

              address: {
                "@type": "PostalAddress",
                streetAddress: "1309 Coffeen Avenue, Suite 1200",
                addressLocality: "Sheridan",
                addressRegion: "WY",
                postalCode: "82801",
                addressCountry: "US",
              },

              description:
                "شركة Runexa Systems LLC تطور وكلاء ذكاء اصطناعي متخصصين لتحليل المستندات القانونية، ودعم التعلم، والإرشاد المالي الشخصي، ودعم اتخاذ القرارات التجارية، وتطبيقات الذكاء الاصطناعي المسؤول.",

              knowsAbout: [
                "Artificial Intelligence",
                "Legal AI",
                "Study AI",
                "Finance Coach AI",
                "Business Intelligence",
                "Responsible AI",
                "Enterprise AI Workflows"
              ],
            },
          ]),
        }}
      />
    </>
  );
}
