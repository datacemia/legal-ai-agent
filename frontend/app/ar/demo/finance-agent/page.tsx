import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";

export const metadata: Metadata = {
  title: "عرض مدرب المالية من Runexa",

  description:
    "شاهد عرضًا توضيحيًا كاملًا لمدرب المالية من Runexa. حلّل المستندات المالية وأنماط الإنفاق والاشتراكات وفرص الادخار والرؤى المالية الشخصية باستخدام الذكاء الاصطناعي.",

  keywords: [
    "Runexa Finance Coach",
    "عرض توضيحي للذكاء الاصطناعي المالي",
    "تحليل مالي بالذكاء الاصطناعي",
    "الذكاء الاصطناعي للتمويل الشخصي",
    "اكتشاف الاشتراكات بالذكاء الاصطناعي",
    "تحليل الإنفاق بالذكاء الاصطناعي",
    "تحليل فرص التوفير بالذكاء الاصطناعي",
    "مدرب مالي بالذكاء الاصطناعي",
    "إدارة الميزانية بالذكاء الاصطناعي",
    "مساعد مالي ذكي",
    "متابعة المصروفات",
    "تحسين الادخار",
    "تحليل البيانات المالية الذكي",
    "إدارة الشؤون المالية الشخصية",
    "التخطيط المالي",
    "التثقيف المالي",
    "تحليل الدخل والمصروفات",
    "اكتشاف النفقات المتكررة",
    "تحديد فرص الادخار",
    "تحليل العادات المالية",
    "لوحة تحكم مالية بالذكاء الاصطناعي",
    "إرشاد مالي مدعوم بالذكاء الاصطناعي",
    "أداة التحليل المالي",
    "الذكاء الاصطناعي لإدارة الميزانية",
    "التمويل الشخصي الذكي",
  ],

  alternates: {
    canonical: "https://runexa.ai/ar/demo/finance-agent",
    languages: {
      en: "https://runexa.ai/en/demo/finance-agent",
      fr: "https://runexa.ai/fr/demo/finance-agent",
      ar: "https://runexa.ai/ar/demo/finance-agent",
      "x-default": "https://runexa.ai/demo/finance-agent",
    },
  },

  openGraph: {
    title: "عرض مدرب المالية من Runexa",

    description:
      "شاهد عرضًا توضيحيًا كاملًا لمدرب المالية من Runexa. حلّل المستندات المالية وأنماط الإنفاق والاشتراكات وفرص الادخار والرؤى المالية الشخصية باستخدام الذكاء الاصطناعي.",

    url: "https://runexa.ai/ar/demo/finance-agent",

    siteName: "Runexa Systems",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Finance Coach Demo",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "عرض مدرب المالية من Runexa",

    description:
      "شاهد عرضًا توضيحيًا كاملًا لمدرب المالية من Runexa. حلّل المستندات المالية وأنماط الإنفاق والاشتراكات وفرص الادخار والرؤى المالية الشخصية باستخدام الذكاء الاصطناعي.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

const jsonLd = {
  "@context": "https://schema.org",

  "@type": "SoftwareApplication",

  name: "مدرب المالية من Runexa",

  applicationCategory: "FinanceApplication",

  operatingSystem: "Web",

  url: "https://runexa.ai/ar/demo/finance-agent",

  inLanguage: "ar",

  description:
    "شاهد عرضًا توضيحيًا كاملًا لمدرب المالية من Runexa. حلّل المستندات المالية وأنماط الإنفاق والاشتراكات وفرص الادخار والرؤى المالية الشخصية باستخدام الذكاء الاصطناعي.",

  publisher: {
    "@type": "Organization",
    name: "Runexa Systems LLC",
    url: "https://runexa.ai",
  },
};

export default function FinanceAgentDemoPage() {
  return (
    <main
      dir="rtl"
      className="min-h-screen bg-slate-50 px-6 py-16"
    >
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(jsonLd),
        }}
      />

      <div className="mx-auto max-w-6xl">
        <h1 className="text-5xl font-bold tracking-tight text-slate-900">
          عرض مدرب المالية من Runexa
        </h1>

        <p className="mt-6 max-w-3xl text-lg text-slate-600">
          ارفع المستندات المالية وكشوف الحساب وملفات المصاريف وبيانات التمويل الشخصي لإنشاء رؤى مدعومة بالذكاء الاصطناعي حول الإنفاق، واكتشاف الاشتراكات، وفرص الادخار، والتوجيه المالي الشخصي.
        </p>

        <div className="mt-10">
          <Image
            src="/demo/finance-agent-demo-ar.png"
            alt="عرض مدرب المالية من Runexa"
            width={1440}
            height={5000}
            priority
            className="rounded-3xl border border-slate-200 shadow-lg"
          />
        </div>

        <div className="mt-10 rounded-3xl border bg-white p-8 shadow-sm">
          <h2 className="text-2xl font-bold text-slate-900">
            ماذا يمكن أن يفعل مدرب المالية؟
          </h2>

          <ul className="mt-4 space-y-3 text-slate-600">
            <li>✓ اكتشاف الاشتراكات المتكررة</li>
            <li>✓ تحليل أنماط الإنفاق</li>
            <li>✓ تحديد فرص الادخار</li>
            <li>✓ تلخيص النشاط المالي</li>
            <li>✓ إبراز المصاريف غير المعتادة أو عالية المخاطر</li>
            <li>✓ إنشاء رؤى مالية شخصية</li>
          </ul>
        </div>

        <div className="mt-10 text-center">
          <p className="mb-6 text-lg text-slate-600">
            هل أنت مستعد لتحليل مستنداتك المالية؟
          </p>

          <Link
            href="/ar/finance"
            className="inline-flex rounded-xl bg-blue-600 px-8 py-4 text-lg font-semibold text-white transition hover:bg-blue-700"
          >
            جرّب مدرب المالية
          </Link>
        </div>
      </div>
    </main>
  );
}
