import type { Metadata } from "next";
import AIDisclaimerClient from "../../../legal/ai-disclaimer/AIDisclaimerClient";

export const revalidate = 3600;

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "إخلاء مسؤولية الذكاء الاصطناعي والشفافية | Runexa",

  description:
    "راجع إخلاء مسؤولية الذكاء الاصطناعي ومعلومات الشفافية من Runexa Systems بشأن المخرجات التي يولدها الذكاء الاصطناعي والقيود ومتطلبات المراجعة البشرية وعدم تقديم المشورة المهنية والاستخدام المسؤول للذكاء الاصطناعي.",

  keywords: [
    "إخلاء مسؤولية الذكاء الاصطناعي",
    "شفافية الذكاء الاصطناعي",
    "حدود الذكاء الاصطناعي",
    "امتثال الذكاء الاصطناعي",
    "إخلاء مسؤولية الذكاء الاصطناعي للمؤسسات",
    "حوكمة الذكاء الاصطناعي",
    "الإفصاح عن مخاطر الذكاء الاصطناعي",
    "سياسة Runexa للذكاء الاصطناعي",
    "الاستخدام المسؤول للذكاء الاصطناعي",
    "نصائح غير مهنية",
    "المراجعة البشرية لنتائج الذكاء الاصطناعي",

    "سياسة الذكاء الاصطناعي",
    "الذكاء الاصطناعي المسؤول",
    "إرشادات استخدام الذكاء الاصطناعي",
    "قيود الذكاء الاصطناعي",
    "مخاطر الذكاء الاصطناعي",
    "التحقق من نتائج الذكاء الاصطناعي",
    "المراجعة البشرية",
    "إشراف بشري على الذكاء الاصطناعي",
    "المحتوى المولد بالذكاء الاصطناعي",
    "أخطاء الذكاء الاصطناعي",
    "دقة الذكاء الاصطناعي",
    "موثوقية الذكاء الاصطناعي",
    "الإفصاح عن استخدام الذكاء الاصطناعي",
    "حوكمة النماذج الذكية",
    "سياسات الذكاء الاصطناعي للمؤسسات",
    "امتثال المؤسسات للذكاء الاصطناعي",
    "قواعد استخدام الذكاء الاصطناعي",
    "تحليل قانوني غير مهني",
    "إرشادات مالية غير مهنية",
    "محتوى تعليمي مولد بالذكاء الاصطناعي",
    "دعم القرار بالذكاء الاصطناعي",
    "Runexa AI Disclaimer",
    "Runexa AI Policy",
    "Responsible AI",
    "Enterprise AI Governance",
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
      "راجع إخلاء مسؤولية الذكاء الاصطناعي ومعلومات الشفافية من Runexa Systems بشأن المخرجات التي يولدها الذكاء الاصطناعي والقيود ومتطلبات المراجعة البشرية وعدم تقديم المشورة المهنية والاستخدام المسؤول للذكاء الاصطناعي.",

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
      "راجع إخلاء مسؤولية الذكاء الاصطناعي ومعلومات الشفافية من Runexa Systems بشأن المخرجات التي يولدها الذكاء الاصطناعي والقيود ومتطلبات المراجعة البشرية وعدم تقديم المشورة المهنية والاستخدام المسؤول للذكاء الاصطناعي.",

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

            name: "Runexa AI Disclaimer & Transparency",

            description:
              "معلومات إخلاء المسؤولية والشفافية الخاصة بالذكاء الاصطناعي التي تغطي المخرجات التي يولدها الذكاء الاصطناعي والقيود ومتطلبات المراجعة البشرية وعدم تقديم المشورة المهنية والاستخدام المسؤول للذكاء الاصطناعي.",

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
