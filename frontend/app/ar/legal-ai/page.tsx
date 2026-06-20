import type { Metadata } from "next";
import LegalAIClient from "../../legal-ai/LegalAIClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "مراجعة العقود وتحليل المستندات القانونية بالذكاء الاصطناعي | Runexa",

  description:
    "حلّل العقود، واكتشف البنود الخطرة، واستخرج الالتزامات، وأنشئ ملخصات للمستندات القانونية باستخدام Runexa Legal AI.",

  keywords: [
    "ذكاء اصطناعي قانوني",
    "مراجعة العقود بالذكاء الاصطناعي",
    "تحليل المستندات القانونية",
    "تحليل مخاطر العقود",
    "مساعد قانوني بالذكاء الاصطناعي",
    "ملخصات العقود",
    "Runexa legal AI",
    "سير العمل القانوني بالذكاء الاصطناعي",

    "Runexa Legal Agent",
    "تحليل العقود بالذكاء الاصطناعي",
    "فحص العقود",
    "التحليل القانوني الآلي",
    "اكتشاف البنود الخطرة",
    "تقييم المخاطر القانونية",
    "تحليل الاتفاقيات القانونية",
    "تحليل الشروط والأحكام",
    "تحليل البنود التعاقدية",
    "الامتثال التعاقدي",
    "إدارة العقود",
    "تلخيص المستندات القانونية",
    "فهم العقود القانونية",
    "قراءة العقود بذكاء",
    "مراجعة العقود التجارية",
    "تحليل المسؤوليات التعاقدية",
    "تحليل الالتزامات القانونية",
    "دعم اتخاذ القرار القانوني",
    "الأتمتة القانونية",
    "تقنية القانون",
    "LegalTech",
    "الذكاء الاصطناعي للمحامين",
    "أداة تحليل قانوني",
    "تحليل الوثائق القانونية",
    "مراجعة المستندات القانونية",
    "اكتشاف المخاطر القانونية",
    "تحليل المخاطر التجارية",
    "تحليل المستندات بالذكاء الاصطناعي",
    "منصة قانونية بالذكاء الاصطناعي",
    "وكلاء الذكاء الاصطناعي القانونيون",
    "Enterprise Legal AI",
  ],

  alternates: {
    canonical: "https://runexa.ai/ar/legal-ai",
    languages: {
      en: `${siteUrl}/en/legal-ai`,
      fr: `${siteUrl}/fr/legal-ai`,
      ar: `${siteUrl}/ar/legal-ai`,
      "x-default": `${siteUrl}/legal-ai`,
    },
  },

  openGraph: {
    title: "مراجعة العقود وتحليل المستندات القانونية بالذكاء الاصطناعي | Runexa",

    description:
      "حلّل العقود، واكتشف البنود الخطرة، واستخرج الالتزامات، وأنشئ ملخصات للمستندات القانونية باستخدام Runexa Legal AI.",

    url: "https://runexa.ai/ar/legal-ai",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Legal AI",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "مراجعة العقود وتحليل المستندات القانونية بالذكاء الاصطناعي | Runexa",

    description:
      "مراجعة العقود بالذكاء الاصطناعي، واكتشاف المخاطر القانونية، واستخراج الالتزامات، وتحليل سير العمل القانوني.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function LegalAIPage() {
  return (
    <>
      <LegalAIClient initialLocale="ar" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify([
            {
              "@context": "https://schema.org",

              "@type": "SoftwareApplication",

              name: "Runexa Legal AI",

              applicationCategory: "BusinessApplication",

              operatingSystem: "Web",

              url: "https://runexa.ai/ar/legal-ai",

              inLanguage: "ar",

              description:
                "برنامج مراجعة عقود وتحليل مستندات قانونية بالذكاء الاصطناعي لاكتشاف البنود الخطرة واستخراج الالتزامات والملخصات والتوصيات.",

              publisher: {
                "@type": "Organization",
                name: "Runexa Systems LLC",
                url: siteUrl,
              },

              knowsAbout: [
                "Legal AI",
                "Contract Review",
                "Legal Document Analysis",
                "Contract Risk Analysis",
                "Obligation Extraction",
                "AI Legal Workflows",
              ],
            },
          ]),
        }}
      />
    </>
  );
}
