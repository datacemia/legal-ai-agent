import type { Metadata } from "next";
import BusinessClient from "../../business/BusinessClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "ذكاء قرارات الأعمال | Runexa",

  description:
    "حلّل بيانات الأعمال باستخدام Runexa Business Agent واحصل على مؤشرات الأداء والمخاطر والفرص والتوقعات والرسوم ودعم القرار التنفيذي بالذكاء الاصطناعي.",

  keywords: [
    "ذكاء اصطناعي للأعمال",
    "ذكاء الأعمال بالذكاء الاصطناعي",
    "تحليل مؤشرات الأداء بالذكاء الاصطناعي",
    "ذكاء قرارات الأعمال",
    "تحليل الأعمال بالذكاء الاصطناعي",
    "توقعات الأعمال بالذكاء الاصطناعي",
    "لوحة تنفيذية بالذكاء الاصطناعي",
    "Runexa Business Agent",
  ],

  alternates: {
    canonical: "https://runexa.ai/ar/business",
    languages: {
      en: `${siteUrl}/en/business`,
      fr: `${siteUrl}/fr/business`,
      ar: `${siteUrl}/ar/business`,
      "x-default": `${siteUrl}/business`,
    },
  },

  openGraph: {
    title: "ذكاء قرارات الأعمال | Runexa",

    description:
      "ارفع بيانات الأعمال واحصل على تحليل تنفيذي بالذكاء الاصطناعي يتضمن مؤشرات الأداء والمخاطر والفرص والتوقعات والقرارات ذات الأولوية.",

    url: "https://runexa.ai/ar/business",

    siteName: "Runexa Systems",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Business Agent",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "ذكاء قرارات الأعمال | Runexa",

    description:
      "ذكاء أعمال بالذكاء الاصطناعي لمؤشرات الأداء والمخاطر والفرص والتوقعات والقرارات التنفيذية.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function BusinessPage() {
  return (
    <>
      <BusinessClient initialLocale="ar" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "SoftwareApplication",

            name: "Runexa Business Agent",

            applicationCategory: "BusinessApplication",

            operatingSystem: "Web",

            description:
              "منصة ذكاء أعمال بالذكاء الاصطناعي لتحليل مؤشرات الأداء والمخاطر والفرص والتوقعات والرسوم ودعم القرار التنفيذي.",

            url: "https://runexa.ai/ar/business",

            inLanguage: "ar",

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems",
              url: siteUrl,
            },

            knowsAbout: [
              "Business AI",
              "Business Intelligence AI",
              "KPI Analysis",
              "Business Forecasting AI",
              "Executive Dashboard",
              "Decision Support",
            ],
          }),
        }}
      />
    </>
  );
}
