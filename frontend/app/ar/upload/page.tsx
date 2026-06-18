import type { Metadata } from "next";
import UploadClient from "../../upload/UploadClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "مراجعة العقود وتحليل المستندات القانونية بالذكاء الاصطناعي | Runexa",

  description:
    "حلّل العقود، واكتشف البنود الخطرة، وافهم الالتزامات، واحصل على ذكاء قانوني منظم باستخدام Runexa AI Legal Agent.",

  keywords: [
    "مراجعة العقود بالذكاء الاصطناعي",
    "ذكاء اصطناعي قانوني",
    "تحليل العقود بالذكاء الاصطناعي",
    "تحليل المستندات القانونية",
    "مساعد قانوني بالذكاء الاصطناعي",
    "تحليل مخاطر العقود",
    "ذكاء قانوني للمؤسسات",
    "Runexa legal agent",
    "ذكاء العقود بالذكاء الاصطناعي",
  ],

  alternates: {
    canonical: "https://runexa.ai/ar/upload",
    languages: {
      en: `${siteUrl}/en/upload`,
      fr: `${siteUrl}/fr/upload`,
      ar: `${siteUrl}/ar/upload`,
      "x-default": `${siteUrl}/upload`,
    },
  },

  openGraph: {
    title: "Runexa Legal AI",

    description:
      "تحليل عقود بالذكاء الاصطناعي، واكتشاف المخاطر القانونية، واستخراج الالتزامات، وذكاء قانوني منظم.",

    url: "https://runexa.ai/ar/upload",

    siteName: "Runexa Systems",

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

    title: "Runexa Legal AI",

    description:
      "حلّل العقود والمستندات القانونية باستخدام ذكاء قانوني مدعوم بالذكاء الاصطناعي.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function UploadPage() {
  return (
    <>
      <UploadClient initialLocale="ar" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "SoftwareApplication",

            name: "Runexa Legal AI",

            applicationCategory: "BusinessApplication",

            operatingSystem: "Web",

            description:
              "منصة تحليل مستندات قانونية بالذكاء الاصطناعي للعقود والالتزامات واكتشاف المخاطر ورؤى التفاوض.",

            url: "https://runexa.ai/ar/upload",

            inLanguage: "ar",

            provider: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: siteUrl,
            },

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: siteUrl,
            },

            offers: {
              "@type": "Offer",
              price: "1",
              priceCurrency: "USD",
            },

            knowsAbout: [
              "AI Contract Review",
              "Legal AI",
              "Contract Analysis",
              "Legal Document Analysis",
              "Contract Risk Analysis",
              "Obligation Extraction",
            ],
          }),
        }}
      />
    </>
  );
}
