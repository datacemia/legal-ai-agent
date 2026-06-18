import type { Metadata } from "next";
import ProductTermsClient from "../../../../products/ai-legal-agent/terms/ProductTermsClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "شروط منتجات الذكاء الاصطناعي | Runexa Systems LLC",

  description:
    "شروط خاصة بالمنتج وقيود وإخلاءات مسؤولية ومعلومات المسؤولية لوكلاء Runexa للذكاء الاصطناعي، بما في ذلك الأنظمة القانونية والمالية والدراسية وأنظمة الأعمال.",

  keywords: [
    "شروط منتجات الذكاء الاصطناعي",
    "إخلاء مسؤولية الذكاء القانوني",
    "إخلاء مسؤولية الذكاء المالي",
    "إخلاء مسؤولية ذكاء الدراسة",
    "إخلاء مسؤولية ذكاء الأعمال",
    "شروط Runexa",
    "تحديد مسؤولية الذكاء الاصطناعي",
    "امتثال الذكاء الاصطناعي للمؤسسات",
  ],

  alternates: {
    canonical: "https://runexa.ai/ar/products/ai-legal-agent/terms",
    languages: {
      en: `${siteUrl}/en/products/ai-legal-agent/terms`,
      fr: `${siteUrl}/fr/products/ai-legal-agent/terms`,
      ar: `${siteUrl}/ar/products/ai-legal-agent/terms`,
      "x-default": `${siteUrl}/products/ai-legal-agent/terms`,
    },
  },

  openGraph: {
    title: "شروط منتجات الذكاء الاصطناعي | Runexa Systems LLC",

    description:
      "شروط خاصة وقيود وإخلاءات مسؤولية ومعلومات المسؤولية لوكلاء Runexa للذكاء الاصطناعي بما في ذلك القانون والمالية والدراسة والأعمال.",

    url: "https://runexa.ai/ar/products/ai-legal-agent/terms",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa AI Product Terms",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "شروط منتجات الذكاء الاصطناعي | Runexa Systems LLC",

    description:
      "قيود منتجات الذكاء الاصطناعي وإفصاحات المسؤولية والشروط التشغيلية لأنظمة Runexa للذكاء الاصطناعي.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function ProductTermsPage() {
  return (
    <>
      <ProductTermsClient initialLocale="ar" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "شروط منتجات Runexa للذكاء الاصطناعي",

            description:
              "شروط المنتج وإفصاحات قيود الذكاء الاصطناعي لوكلاء Runexa للذكاء الاصطناعي وخدمات المؤسسات.",

            url: "https://runexa.ai/ar/products/ai-legal-agent/terms",

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
