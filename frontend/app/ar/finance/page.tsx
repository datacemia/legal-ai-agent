import type { Metadata } from "next";
import FinanceClient from "../../finance/FinanceClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "مدرب مالي بالذكاء الاصطناعي وذكاء مالي | Runexa",

  description:
    "حلّل كشوف الحسابات البنكية، واكتشف الاشتراكات، وراقب الإنفاق، وحدد فرص الادخار، واحصل على توجيه مالي بالذكاء الاصطناعي مع Runexa Finance AI.",

  keywords: [
    "مدرب مالي بالذكاء الاصطناعي",
    "تحليل مالي بالذكاء الاصطناعي",
    "تحليل كشف حساب بنكي",
    "ذكاء اصطناعي للمالية الشخصية",
    "مساعد ميزانية بالذكاء الاصطناعي",
    "اكتشاف الاشتراكات بالذكاء الاصطناعي",
    "ذكاء مالي",
    "تحليل الادخار بالذكاء الاصطناعي",
  ],

  alternates: {
    canonical: "https://runexa.ai/ar/finance",
    languages: {
      en: `${siteUrl}/en/finance`,
      fr: `${siteUrl}/fr/finance`,
      ar: `${siteUrl}/ar/finance`,
      "x-default": `${siteUrl}/finance`,
    },
  },

  openGraph: {
    title: "مدرب مالي بالذكاء الاصطناعي وذكاء مالي | Runexa",

    description:
      "حلّل كشوف الحسابات البنكية، واكتشف الاشتراكات، وراقب الإنفاق، وحدد فرص الادخار، واحصل على توجيه مالي بالذكاء الاصطناعي مع Runexa Finance AI.",

    url: "https://runexa.ai/ar/finance",

    siteName: "Runexa Systems",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Finance AI",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "مدرب مالي بالذكاء الاصطناعي وذكاء مالي | Runexa",

    description:
      "ذكاء مالي بالذكاء الاصطناعي لتحليل كشوف الحسابات، والميزانية، واكتشاف الاشتراكات، وتحسين الادخار.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function FinancePage() {
  return (
    <>
      <FinanceClient initialLocale="ar" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "SoftwareApplication",

            name: "Runexa Finance AI",

            applicationCategory: "FinanceApplication",

            operatingSystem: "Web",

            description:
              "منصة ذكاء مالي بالذكاء الاصطناعي لتحليل كشوف الحسابات واكتشاف الاشتراكات والميزانية وتحسين الادخار.",

            url: "https://runexa.ai/ar/finance",

            inLanguage: "ar",

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems",
              url: siteUrl,
            },

            knowsAbout: [
              "AI Finance Coach",
              "Financial Analysis",
              "Bank Statement Analysis",
              "Personal Finance AI",
              "Budgeting AI",
              "Savings Optimization",
            ],
          }),
        }}
      />
    </>
  );
}
