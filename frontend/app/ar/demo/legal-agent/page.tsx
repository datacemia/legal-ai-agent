import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";

export const metadata: Metadata = {
  title: "عرض وكيل Runexa القانوني",

  description:
    "شاهد عرضًا توضيحيًا كاملًا لوكيل Runexa القانوني. حلّل العقود واكتشف البنود عالية المخاطر واستخرج الالتزامات ولخّص المستندات القانونية وراجع مواد الامتثال باستخدام الذكاء الاصطناعي.",

  keywords: [
    "Runexa Legal Agent",
    "عرض توضيحي للذكاء الاصطناعي القانوني",
    "تحليل العقود بالذكاء الاصطناعي",
    "مراجعة العقود بالذكاء الاصطناعي",
    "تحليل المستندات القانونية",
    "اكتشاف المخاطر التعاقدية",
    "مساعد قانوني بالذكاء الاصطناعي",
    "الذكاء الاصطناعي لسير العمل القانوني",
    "التحليل القانوني الآلي",
    "تلخيص العقود بالذكاء الاصطناعي",
    "تحديد البنود المهمة",
    "تقييم المخاطر القانونية",
    "فحص العقود",
    "قراءة العقود بذكاء",
    "تحليل الوثائق القانونية",
    "الامتثال التعاقدي",
    "أداة ذكاء اصطناعي للمحامين",
    "مساعد التحليل القانوني",
    "سير عمل قانوني ذكي",
    "مراجعة المستندات بالذكاء الاصطناعي",
    "تحليل الشروط التعاقدية",
    "اكتشاف البنود الخطرة",
    "الذكاء الاصطناعي للمكاتب القانونية",
    "إدارة العقود",
    "الذكاء الاصطناعي القانوني",
  ],

  alternates: {
    canonical: "https://runexa.ai/ar/demo/legal-agent",
    languages: {
      en: "https://runexa.ai/en/demo/legal-agent",
      fr: "https://runexa.ai/fr/demo/legal-agent",
      ar: "https://runexa.ai/ar/demo/legal-agent",
      "x-default": "https://runexa.ai/demo/legal-agent",
    },
  },

  openGraph: {
    title: "عرض وكيل Runexa القانوني",
    description:
      "شاهد عرضًا توضيحيًا كاملًا لوكيل Runexa القانوني. حلّل العقود واكتشف البنود عالية المخاطر واستخرج الالتزامات ولخّص المستندات القانونية وراجع مواد الامتثال باستخدام الذكاء الاصطناعي.",
    url: "https://runexa.ai/ar/demo/legal-agent",
    siteName: "Runexa Systems",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Legal Agent Demo",
      },
    ],
    locale: "ar_AR",
    alternateLocale: ["en_US", "fr_FR"],
    type: "website",
  },

  twitter: {
    card: "summary_large_image",
    title: "عرض وكيل Runexa القانوني",
    description:
      "شاهد عرضًا توضيحيًا كاملًا لوكيل Runexa القانوني. حلّل العقود واكتشف البنود عالية المخاطر واستخرج الالتزامات ولخّص المستندات القانونية وراجع مواد الامتثال باستخدام الذكاء الاصطناعي.",
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
  name: "وكيل Runexa القانوني",
  applicationCategory: "BusinessApplication",
  operatingSystem: "Web",
  url: "https://runexa.ai/ar/demo/legal-agent",
  inLanguage: "ar",
  description:
    "شاهد عرضًا توضيحيًا كاملًا لوكيل Runexa القانوني. حلّل العقود واكتشف البنود عالية المخاطر واستخرج الالتزامات ولخّص المستندات القانونية وراجع مواد الامتثال باستخدام الذكاء الاصطناعي.",
  publisher: {
    "@type": "Organization",
    name: "Runexa Systems LLC",
    url: "https://runexa.ai",
  },
};

export default function LegalAgentDemoPage() {
  return (
    <main dir="rtl" className="min-h-screen bg-slate-50 px-6 py-16">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(jsonLd),
        }}
      />

      <div className="mx-auto max-w-6xl">
        <h1 className="text-5xl font-bold tracking-tight text-slate-900">
          عرض وكيل Runexa القانوني
        </h1>

        <p className="mt-6 max-w-3xl text-lg text-slate-600">
          ارفع العقود والاتفاقيات والسياسات والمستندات القانونية لإنشاء ملخصات
          مدعومة بالذكاء الاصطناعي، واكتشاف البنود عالية المخاطر، واستخراج
          الالتزامات والمواعيد النهائية، والحصول على تحليل قانوني منظم.
        </p>

        <div className="mt-10">
          <Image
            src="/demo/legal-agent-demo-ar.png"
            alt="عرض وكيل Runexa القانوني"
            width={1440}
            height={5000}
            sizes="(max-width: 768px) 100vw, (max-width: 1280px) 90vw, 1152px"
            className="h-auto w-full rounded-3xl border border-slate-200 shadow-lg"
          />
        </div>

        <div className="mt-10 rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
          <h2 className="text-2xl font-bold text-slate-900">
            ماذا يمكن أن يفعل الوكيل القانوني؟
          </h2>

          <ul className="mt-4 space-y-3 text-slate-600">
            <li>✓ تحليل العقود والاتفاقيات</li>
            <li>✓ اكتشاف البنود عالية المخاطر</li>
            <li>✓ استخراج الالتزامات والمواعيد النهائية</li>
            <li>✓ تلخيص المستندات القانونية</li>
            <li>✓ مراجعة السياسات ووثائق الامتثال</li>
            <li>✓ إنشاء رؤى قانونية منظمة</li>
          </ul>
        </div>

        <div className="mt-10 text-center">
          <p className="mb-6 text-lg text-slate-600">
            هل أنت مستعد لتحليل مستنداتك القانونية؟
          </p>

          <Link
            href="/ar/upload"
            className="inline-flex rounded-xl bg-blue-600 px-8 py-4 text-lg font-semibold text-white transition hover:bg-blue-700"
          >
            جرّب الوكيل القانوني
          </Link>
        </div>
      </div>
    </main>
  );
}