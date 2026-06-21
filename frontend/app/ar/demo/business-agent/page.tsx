import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";

export const metadata: Metadata = {
  title: "عرض وكيل قرارات الأعمال من Runexa",

  description:
    "شاهد عرضًا توضيحيًا كاملًا لوكيل قرارات الأعمال من Runexa. حلّل بيانات الأعمال ومؤشرات الأداء والمخاطر والفرص والتوقعات والرؤى التنفيذية باستخدام الذكاء الاصطناعي.",

  keywords: [
    "Runexa Business Decision Agent",
    "عرض توضيحي للذكاء الاصطناعي للأعمال",
    "ذكاء الأعمال بالذكاء الاصطناعي",
    "دعم اتخاذ القرارات التجارية",
    "تحليل مؤشرات الأداء بالذكاء الاصطناعي",
    "تحليل مخاطر الأعمال",
    "التنبؤ بالذكاء الاصطناعي",
    "ذكاء اصطناعي للمديرين التنفيذيين",
    "التحليل الاستراتيجي بالذكاء الاصطناعي",
    "لوحة معلومات ذكية",
    "تحليل أداء الشركات",
    "متابعة مؤشرات الأداء الرئيسية",
    "اتخاذ القرار بمساعدة الذكاء الاصطناعي",
    "تحليل الفرص التجارية",
    "التحليل التنافسي بالذكاء الاصطناعي",
    "توقعات النمو",
    "تحسين الأداء المؤسسي",
    "ذكاء أعمال ذكي",
    "إدارة الأعمال بالذكاء الاصطناعي",
    "تحليل بيانات الشركات",
    "إدارة المخاطر الاستراتيجية",
    "مساعد اتخاذ القرار بالذكاء الاصطناعي",
    "الذكاء الاصطناعي لرواد الأعمال",
    "تحليل اتجاهات السوق",
    "أداة دعم القرار",
  ],

  alternates: {
    canonical: "https://runexa.ai/ar/demo/business-agent",
    languages: {
      en: "https://runexa.ai/en/demo/business-agent",
      fr: "https://runexa.ai/fr/demo/business-agent",
      ar: "https://runexa.ai/ar/demo/business-agent",
      "x-default": "https://runexa.ai/demo/business-agent",
    },
  },

  openGraph: {
    title: "عرض وكيل قرارات الأعمال من Runexa",

    description:
      "شاهد عرضًا توضيحيًا كاملًا لوكيل قرارات الأعمال من Runexa. حلّل بيانات الأعمال ومؤشرات الأداء والمخاطر والفرص والتوقعات والرؤى التنفيذية باستخدام الذكاء الاصطناعي.",

    url: "https://runexa.ai/ar/demo/business-agent",

    siteName: "Runexa Systems",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Business Decision Agent Demo",
      },
    ],

    locale: "ar_AR",

    alternateLocale: ["en_US", "fr_FR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "عرض وكيل قرارات الأعمال من Runexa",

    description:
      "شاهد عرضًا توضيحيًا كاملًا لوكيل قرارات الأعمال من Runexa. حلّل بيانات الأعمال ومؤشرات الأداء والمخاطر والفرص والتوقعات والرؤى التنفيذية باستخدام الذكاء الاصطناعي.",

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

  name: "وكيل قرارات الأعمال من Runexa",

  applicationCategory: "BusinessApplication",

  operatingSystem: "Web",

  url: "https://runexa.ai/ar/demo/business-agent",

  inLanguage: "ar",

  description:
    "شاهد عرضًا توضيحيًا كاملًا لوكيل قرارات الأعمال من Runexa. حلّل بيانات الأعمال ومؤشرات الأداء والمخاطر والفرص والتوقعات والرؤى التنفيذية باستخدام الذكاء الاصطناعي.",

  publisher: {
    "@type": "Organization",
    name: "Runexa Systems LLC",
    url: "https://runexa.ai",
  },
};

export default function BusinessAgentDemoPage() {
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
          عرض وكيل قرارات الأعمال من Runexa
        </h1>

        <p className="mt-6 max-w-3xl text-lg text-slate-600">
          ارفع تقارير الأعمال وملفات مؤشرات الأداء وبيانات المبيعات والمستندات التشغيلية والملاحظات الاستراتيجية لإنشاء ملخصات تنفيذية، وتحليل المخاطر، واكتشاف الفرص، ودعم التوقعات واتخاذ القرار بالذكاء الاصطناعي.
        </p>

        <div className="mt-10">
          <Image
            src="/demo/business-agent-demo-ar.png"
            alt="عرض وكيل قرارات الأعمال من Runexa"
            width={1440}
            height={5000}
            sizes="(max-width: 768px) 100vw, (max-width: 1280px) 90vw, 1152px"
            className="h-auto w-full rounded-3xl border border-slate-200 shadow-lg"
          />
        </div>

        <div className="mt-10 rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
          <h2 className="text-2xl font-bold text-slate-900">
            ماذا يمكن أن يفعل وكيل قرارات الأعمال؟
          </h2>

          <ul className="mt-4 space-y-3 text-slate-600">
            <li>✓ تحليل مؤشرات الأداء وأداء الأعمال</li>
            <li>✓ اكتشاف المخاطر والمشكلات التشغيلية</li>
            <li>✓ تحديد الفرص الاستراتيجية</li>
            <li>✓ إنشاء ملخصات تنفيذية</li>
            <li>✓ دعم التوقعات واتخاذ القرار</li>
            <li>✓ تحويل بيانات الأعمال إلى رؤى واضحة</li>
          </ul>
        </div>

        <div className="mt-10 text-center">
          <p className="mb-6 text-lg text-slate-600">
            هل أنت مستعد لتحليل بيانات أعمالك؟
          </p>

          <Link
            href="/ar/business"
            className="inline-flex rounded-xl bg-blue-600 px-8 py-4 text-lg font-semibold text-white transition hover:bg-blue-700"
          >
            جرّب وكيل الأعمال
          </Link>
        </div>
      </div>
    </main>
  );
}
