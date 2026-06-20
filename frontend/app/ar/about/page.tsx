import type { Metadata } from "next";
import AboutClient from "../../about/AboutClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "عن Runexa | قصة المؤسس ووكلاء الذكاء الاصطناعي المتخصصون",

  description:
    "تعرّف على سبب إنشاء Dr. Rachid Ejjami لشركة Runexa Systems LLC وكيف ألهمت التحديات الواقعية إنشاء Study Agent وLegal Agent وFinance Coach وBusiness Decision Agent.",

  keywords: [
    "Runexa",
    "Runexa Systems LLC",
    "الدكتور رشيد الجامعي",
    "تم الإنشاء بواسطة الدكتور رشيد الجامعي",
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
      "تعرّف على سبب إنشاء Dr. Rachid Ejjami لشركة Runexa Systems LLC وكيف ألهمت التحديات الواقعية إنشاء Study Agent وLegal Agent وFinance Coach وBusiness Decision Agent.",

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
      "تعرّف على سبب إنشاء Dr. Rachid Ejjami لشركة Runexa Systems LLC وكيف ألهمت التحديات الواقعية إنشاء Study Agent وLegal Agent وFinance Coach وBusiness Decision Agent.",

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
                "تعرّف على سبب إنشاء Dr. Rachid Ejjami لشركة Runexa Systems LLC وكيف ألهمت التحديات الواقعية إنشاء Study Agent وLegal Agent وFinance Coach وBusiness Decision Agent.",

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
                name: "Dr. Rachid Ejjami",
                jobTitle: "Founder and Managing Member",
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
                "Runexa Systems LLC builds specialized AI agents for legal document analysis, learning support, personal finance coaching, business decision support, and responsible AI workflows.",

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
