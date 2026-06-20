import type { Metadata } from "next";
import RefundPolicyClient from "../../../legal/refunds/RefundPolicyClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "سياسة الاسترداد | Runexa",

  description:
    "سياسة الاسترداد الخاصة بـ Runexa Systems LLC التي تغطي أرصدة الذكاء الاصطناعي والاشتراكات ونزاعات الفوترة وعمليات رد المبالغ وحقوق المستهلك عند انطباقها وخدمات المؤسسات.",

  keywords: [
    "سياسة الاسترداد",
    "استرداد اشتراكات الذكاء الاصطناعي",
    "فوترة Runexa",
    "استرداد أرصدة الذكاء الاصطناعي",
    "فوترة الذكاء الاصطناعي للمؤسسات",
    "سياسة استرداد خدمات SaaS",
    "نزاعات فوترة الذكاء الاصطناعي",
    "إلغاء الاشتراك",
    "حماية المستهلك",
    "حق التراجع",
    "شفافية الفوترة",
  ],

  alternates: {
    canonical: "https://runexa.ai/ar/legal/refunds",
    languages: {
      en: `${siteUrl}/en/legal/refunds`,
      fr: `${siteUrl}/fr/legal/refunds`,
      ar: `${siteUrl}/ar/legal/refunds`,
      "x-default": `${siteUrl}/legal/refunds`,
    },
  },

  openGraph: {
    title: "سياسة الاسترداد | Runexa",

    description:
      "سياسة الاسترداد الخاصة بـ Runexa Systems LLC التي تغطي أرصدة الذكاء الاصطناعي والاشتراكات ونزاعات الفوترة وعمليات رد المبالغ وحقوق المستهلك عند انطباقها وخدمات المؤسسات.",

    url: "https://runexa.ai/ar/legal/refunds",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Refund Policy",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "سياسة الاسترداد | Runexa",

    description:
      "سياسة الاسترداد الخاصة بـ Runexa Systems LLC التي تغطي أرصدة الذكاء الاصطناعي والاشتراكات ونزاعات الفوترة وعمليات رد المبالغ وحقوق المستهلك عند انطباقها وخدمات المؤسسات.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function RefundPolicyPage() {
  return (
    <>
      <RefundPolicyClient initialLocale="ar" lockInitialLocale />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "Runexa Refund Policy",

            description:
              "سياسة الاسترداد والفوترة لخدمات Runexa للذكاء الاصطناعي والاشتراكات وأرصدة الذكاء الاصطناعي وسير عمل المؤسسات ونزاعات الفوترة والإلغاء وحقوق المستهلك عند انطباقها.",

            url: "https://runexa.ai/ar/legal/refunds",

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
