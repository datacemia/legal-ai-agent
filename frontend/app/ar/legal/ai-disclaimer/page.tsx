import type { Metadata } from "next";
import AIDisclaimerClient from "../../../legal/ai-disclaimer/AIDisclaimerClient";

export const revalidate = 3600;

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "إخلاء مسؤولية الذكاء الاصطناعي والشفافية | Runexa",

  description:
    "راجع إخلاء مسؤولية Runexa Systems ومعلومات الشفافية حول مخرجات الذكاء الاصطناعي والقيود ومتطلبات المراجعة البشرية واستخدام الذكاء الاصطناعي للمؤسسات.",

  keywords: [
    "إخلاء مسؤولية الذكاء الاصطناعي",
    "شفافية الذكاء الاصطناعي",
    "قيود الذكاء الاصطناعي",
    "امتثال الذكاء الاصطناعي",
    "إخلاء مسؤولية الذكاء الاصطناعي للمؤسسات",
    "حوكمة الذكاء الاصطناعي",
    "إفصاح مخاطر الذكاء الاصطناعي",
    "سياسة Runexa للذكاء الاصطناعي",
  ],

  alternates: {
    canonical: "https://runexa.ai/ar/legal/ai-disclaimer",
    languages: {
      en: `${siteUrl}/en/legal/ai-disclaimer`,
      fr: `${siteUrl}/fr/legal/ai-disclaimer`,
      ar: `${siteUrl}/ar/legal/ai-disclaimer`,
      "x-default": `${siteUrl}/legal/ai-disclaimer`,
    },
  },

  openGraph: {
    title: "إخلاء مسؤولية الذكاء الاصطناعي والشفافية | Runexa",

    description:
      "راجع شفافية الذكاء الاصطناعي وقيوده ومتطلبات المراجعة البشرية لخدمات Runexa Systems ومنصات المؤسسات.",

    url: "https://runexa.ai/ar/legal/ai-disclaimer",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa AI Disclaimer",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "إخلاء مسؤولية الذكاء الاصطناعي والشفافية | Runexa",

    description:
      "راجع قيود الذكاء الاصطناعي وإشعارات الشفافية ومتطلبات المراجعة البشرية لأنظمة Runexa AI.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function AIDisclaimerPage() {
  return (
    <>
      <AIDisclaimerClient initialLocale="ar" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "إخلاء مسؤولية Runexa للذكاء الاصطناعي والشفافية",

            description:
              "معلومات إخلاء مسؤولية وشفافية تنظّم استخدام أنظمة Runexa للذكاء الاصطناعي ومنصات المؤسسات وواجهات API والخدمات الذكية.",

            url: "https://runexa.ai/ar/legal/ai-disclaimer",

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
