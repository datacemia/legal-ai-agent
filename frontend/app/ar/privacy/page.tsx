import type { Metadata } from "next";
import PrivacyClient from "../../privacy/PrivacyClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "سياسة الخصوصية | Runexa",

  description:
    "سياسة الخصوصية التي توضّح كيف تقوم Runexa Systems LLC بجمع واستخدام وتخزين وحماية ومعالجة ونقل وتأمين المعلومات الشخصية والمحتوى المرفوع للمستخدمين الدوليين.",

  keywords: [
    "privacy policy",
    "AI privacy",
    "Runexa privacy",
    "AI data processing",
    "enterprise AI privacy",
    "AI platform privacy",
    "AI uploads privacy",
    "AI compliance",
    "AI model training",
    "international data transfers",
    "automated processing",
    "GDPR",
    "UK GDPR",
  ],

  alternates: {
    canonical: "https://runexa.ai/ar/privacy",
    languages: {
      en: `${siteUrl}/en/privacy`,
      fr: `${siteUrl}/fr/privacy`,
      ar: `${siteUrl}/ar/privacy`,
      "x-default": `${siteUrl}/privacy`,
    },
  },

  openGraph: {
    title: "سياسة الخصوصية | Runexa",

    description:
      "سياسة الخصوصية التي توضّح كيف تقوم Runexa Systems LLC بجمع واستخدام وتخزين وحماية ومعالجة ونقل وتأمين المعلومات الشخصية والمحتوى المرفوع للمستخدمين الدوليين.",

    url: "https://runexa.ai/ar/privacy",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Privacy Policy",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "سياسة الخصوصية | Runexa",

    description:
      "سياسة الخصوصية التي توضّح كيف تقوم Runexa Systems LLC بجمع واستخدام وتخزين وحماية ومعالجة ونقل وتأمين المعلومات الشخصية والمحتوى المرفوع للمستخدمين الدوليين.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function PrivacyPage() {
  return (
    <>
      <PrivacyClient initialLocale="ar" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "PrivacyPolicy",

            name: "Runexa Privacy Policy",

            description:
              "سياسة الخصوصية التي توضّح كيف تقوم Runexa Systems LLC بجمع واستخدام وتخزين وحماية ومعالجة ونقل وتأمين المعلومات الشخصية والمحتوى المرفوع للمستخدمين الدوليين.",

            url: "https://runexa.ai/ar/privacy",

            inLanguage: "ar",

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: siteUrl,
            },

            jurisdiction: [
              "United States",
              "European Union",
              "United Kingdom",
              "International",
            ],
          }),
        }}
      />
    </>
  );
}
