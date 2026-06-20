import type { Metadata } from "next";
import PricingClient from "../../pricing/PricingClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "أسعار Runexa | وكلاء الذكاء الاصطناعي والأرصدة وخطط API",

  description:
    "قارن خطط أسعار Runexa AI بما في ذلك تجارب الذكاء الاصطناعي والأرصدة العامة واشتراكات Pro وسير عمل API للمؤسسات.",

  keywords: [
    "أسعار الذكاء الاصطناعي",
    "أسعار وكلاء الذكاء الاصطناعي",
    "أسعار الذكاء الاصطناعي القانوني",
    "أسعار الذكاء الاصطناعي المالي",
    "أسعار API الذكاء الاصطناعي",
    "أسعار الذكاء الاصطناعي للمؤسسات",
    "أسعار Runexa",
    "أرصدة الذكاء الاصطناعي",
    "اشتراكات الذكاء الاصطناعي",

    "خطط أسعار Runexa",
    "باقات الذكاء الاصطناعي",
    "أسعار Runexa Legal Agent",
    "أسعار Runexa Finance Coach",
    "أسعار Runexa Study Agent",
    "أسعار Runexa Business Decision Agent",
    "تكلفة الذكاء الاصطناعي",
    "تكلفة وكلاء الذكاء الاصطناعي",
    "اشتراكات Runexa",
    "اشتراك شهري للذكاء الاصطناعي",
    "اشتراك سنوي للذكاء الاصطناعي",
    "فوترة الذكاء الاصطناعي",
    "فوترة المؤسسات",
    "أرصدة Runexa",
    "شراء أرصدة الذكاء الاصطناعي",
    "استهلاك أرصدة الذكاء الاصطناعي",
    "أسعار SaaS",
    "تسعير SaaS",
    "تسعير API",
    "أسعار المطورين",
    "أسعار API للمؤسسات",
    "أسعار الذكاء الاصطناعي للشركات",
    "خطط المؤسسات",
    "منصة ذكاء اصطناعي للمؤسسات",
    "التسعير حسب الاستخدام",
    "الدفع حسب الاستخدام",
    "Runexa Pricing",
    "Runexa API Pricing",
    "Enterprise AI Pricing",
    "AI Subscription Plans",
  ],

  alternates: {
    canonical: "https://runexa.ai/ar/pricing",
    languages: {
      en: `${siteUrl}/en/pricing`,
      fr: `${siteUrl}/fr/pricing`,
      ar: `${siteUrl}/ar/pricing`,
      "x-default": `${siteUrl}/pricing`,
    },
  },

  openGraph: {
    title: "أسعار Runexa | وكلاء الذكاء الاصطناعي والأرصدة وخطط API",

    description:
      "قارن خطط أسعار Runexa AI بما في ذلك تجارب الذكاء الاصطناعي والأرصدة العامة واشتراكات Pro وسير عمل API للمؤسسات.",

    url: "https://runexa.ai/ar/pricing",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Pricing",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "أسعار Runexa | وكلاء الذكاء الاصطناعي والأرصدة وخطط API",

    description:
      "قارن اشتراكات الذكاء الاصطناعي والأرصدة وخطط API وأسعار المؤسسات من Runexa.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function PricingPage() {
  return (
    <>
      <PricingClient initialLanguage="ar" lockInitialLanguage />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "SoftwareApplication",

            name: "Runexa Pricing",

            applicationCategory: "BusinessApplication",

            operatingSystem: "Web",

            description:
              "منصة ذكاء اصطناعي للتحليل القانوني والذكاء المالي وسير عمل الدراسة ودعم قرارات الأعمال.",

            url: "https://runexa.ai/ar/pricing",

            inLanguage: "ar",

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: siteUrl,
            },

            offers: [
              {
                "@type": "Offer",

                name: "Pro",

                price: "49",

                priceCurrency: "USD",
              },
            ],

            knowsAbout: [
              "AI Pricing",
              "AI Agents Pricing",
              "AI Credits",
              "AI API Plans",
              "Enterprise AI Pricing",
              "AI Subscriptions",
            ],
          }),
        }}
      />
    </>
  );
}
