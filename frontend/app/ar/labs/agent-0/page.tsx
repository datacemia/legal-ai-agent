import type { Metadata } from "next";
import AgentZeroClient from "../../../labs/agent-0/AgentZeroClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title:
    "Runexa Agent 0 | بنية أمان بالذكاء الاصطناعي وذكاء المنزل",

  description:
    "Runexa Agent 0 هو مفهوم مستقبلي للأمان والمراقبة الذكية بالذكاء الاصطناعي يجمع بين الكاميرات وأجهزة الاستشعار وGPS وأنظمة الاستدلال الذكي.",

  keywords: [
    "نظام أمان بالذكاء الاصطناعي",
    "منزل ذكي بالذكاء الاصطناعي",
    "مراقبة بالذكاء الاصطناعي",
    "أجهزة استشعار بالذكاء الاصطناعي",
    "ذكاء الكاميرات بالذكاء الاصطناعي",
    "أتمتة المنزل بالذكاء الاصطناعي",
    "بنية أمان بالذكاء الاصطناعي",
    "Runexa Labs",
    "Agent 0",

    "أمن المنازل الذكي",
    "المراقبة الذكية",
    "كشف التهديدات بالذكاء الاصطناعي",
    "تحليل الفيديو بالذكاء الاصطناعي",
    "الرؤية الحاسوبية",
    "تحليل الكاميرات الذكي",
    "كاميرات مراقبة ذكية",
    "أنظمة مراقبة متقدمة",
    "التحكم الذكي بالمنازل",
    "أتمتة المباني الذكية",
    "إنترنت الأشياء",
    "أجهزة استشعار ذكية",
    "كشف الحركة بالذكاء الاصطناعي",
    "إدارة الأمن الذكي",
    "منصة أمان ذكية",
    "تحليل الأحداث الأمنية",
    "الأمن المادي بالذكاء الاصطناعي",
    "المراقبة المؤسسية",
    "البنية التحتية الأمنية",
    "الذكاء الاصطناعي للأمن",
    "أنظمة الحماية الذكية",
    "المنازل المتصلة",
    "المباني الذكية",
    "الأمن الذكي للمؤسسات",
    "حلول الذكاء الاصطناعي للأمن",
    "Runexa Agent 0",
    "Runexa Smart Security",
    "AI Security Platform",
    "Smart Home AI",
    "Computer Vision AI",
  ],

  alternates: {
    canonical: "https://runexa.ai/ar/labs/agent-0",
    languages: {
      en: `${siteUrl}/en/labs/agent-0`,
      fr: `${siteUrl}/fr/labs/agent-0`,
      ar: `${siteUrl}/ar/labs/agent-0`,
      "x-default": `${siteUrl}/labs/agent-0`,
    },
  },

  openGraph: {
    title:
      "Runexa Agent 0 | بنية أمان بالذكاء الاصطناعي وذكاء المنزل",

    description:
      "بنية مستقبلية للأمان بالذكاء الاصطناعي تجمع بين الكاميرات وأجهزة الاستشعار وGPS والاستدلال الذكي للمراقبة الذكية.",

    url: "https://runexa.ai/ar/labs/agent-0",

    siteName: "Runexa Systems",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Agent 0",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title:
      "Runexa Agent 0 | بنية أمان بالذكاء الاصطناعي وذكاء المنزل",

    description:
      "بنية تجريبية للأمان بالذكاء الاصطناعي تجمع بين الكاميرات وأجهزة الاستشعار وGPS وأنظمة الاستدلال الذكي.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function AgentZeroPage() {
  return (
    <>
      <AgentZeroClient initialLanguage="ar" lockInitialLanguage />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "ResearchProject",

            name: "Runexa Agent 0",

            description:
              "مفهوم تجريبي لبنية أمان بالذكاء الاصطناعي تجمع بين الكاميرات وأجهزة الاستشعار وGPS وأنظمة الاستدلال الذكي.",

            url: "https://runexa.ai/ar/labs/agent-0",

            inLanguage: "ar",

            creator: {
              "@type": "Organization",
              name: "Runexa Labs",
            },

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems",
              url: siteUrl,
            },
          }),
        }}
      />
    </>
  );
}
