import type { Metadata } from "next";
import PrivacyClient from "../../privacy/PrivacyClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "سياسة الخصوصية | Runexa",

  description:
    "سياسة الخصوصية التي توضّح كيف تجمع Runexa Systems LLC المعلومات الشخصية والمحتوى المرفوع وتستخدمه وتخزنه وتحميه وتعالجه.",

  keywords: [
    "privacy policy",
    "AI privacy",
    "Runexa privacy",
    "AI data processing",
    "enterprise AI privacy",
    "AI platform privacy",
    "AI uploads privacy",
    "AI compliance",
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
      "سياسة الخصوصية التي توضّح كيف تجمع Runexa Systems LLC المعلومات الشخصية والمحتوى المرفوع وتستخدمه وتخزنه وتحميه وتعالجه.",

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
      "Privacy and data processing disclosures for Runexa AI services, APIs, uploads, and enterprise workflows.",

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

            "@type": "WebPage",

            name: "سياسة الخصوصية من Runexa",

            description:
              "Privacy and data processing disclosures for Runexa AI services, APIs, uploads, and enterprise workflows.",

            url: "https://runexa.ai/ar/privacy",

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
