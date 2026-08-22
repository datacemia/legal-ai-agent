import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "عرض Runexa Study Agent | Runexa Systems",
  description:
    "شاهد Runexa Study Agent وهو يحول المواد الدراسية إلى ملخصات واختبارات وبطاقات مراجعة وخرائط تعلم وخطط مراجعة مخصصة بالذكاء الاصطناعي.",

  alternates: {
    canonical: "https://runexa.ai/ar/demo/study-agent",
    languages: {
      en: "https://runexa.ai/en/demo/study-agent",
      fr: "https://runexa.ai/fr/demo/study-agent",
      ar: "https://runexa.ai/ar/demo/study-agent",
      "x-default": "https://runexa.ai/demo/study-agent",
    },
  },

  openGraph: {
    title: "عرض Runexa Study Agent",
    description:
      "شاهد كيف يحوّل Runexa Study المواد الدراسية إلى مساحة تعلم متكاملة مدعومة بالذكاء الاصطناعي.",
    url: "https://runexa.ai/ar/demo/study-agent",
    siteName: "Runexa Systems",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "عرض Runexa Study Agent",
      },
    ],
    locale: "ar_AR",
    type: "website",
  },

  twitter: {
    card: "summary_large_image",
    title: "عرض Runexa Study Agent",
    description:
      "ملخصات، اختبارات، بطاقات مراجعة، خرائط تعلم وخطط مراجعة مخصصة بالذكاء الاصطناعي.",
    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

const STUDY_DEMO_VIDEO =
  "https://drive.google.com/file/d/181w3pp1XkeiNRyPNBwAfuBxwAqBwu_eo/preview";

const jsonLd = {
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  name: "Runexa Study Agent",
  applicationCategory: "EducationalApplication",
  operatingSystem: "Web",
  url: "https://runexa.ai/ar/demo/study-agent",
  inLanguage: "ar",
  description:
    "مساعد دراسي بالذكاء الاصطناعي لإنشاء الملخصات والاختبارات وبطاقات المراجعة وخرائط التعلم والصوت وخطط المراجعة المخصصة.",
};

export default function StudyAgentDemoArPage() {
  return (
    <main
      dir="rtl"
      lang="ar"
      className="min-h-screen bg-slate-50 px-4 py-14 sm:px-6 sm:py-16"
    >
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(jsonLd),
        }}
      />

      <div className="mx-auto max-w-6xl">
        <div className="text-center">
          <span className="inline-flex rounded-full border border-blue-200 bg-blue-50 px-4 py-1.5 text-xs font-bold tracking-[0.18em] text-blue-700">
            عرض توضيحي
          </span>

          <h1 className="mx-auto mt-5 max-w-4xl text-4xl font-black tracking-tight text-slate-950 sm:text-5xl">
            عرض Runexa Study Agent
          </h1>

          <p className="mx-auto mt-5 max-w-3xl text-base leading-8 text-slate-600 sm:text-lg">
            شاهد كيف يحوّل Runexa Study المواد الدراسية إلى مساحة تعلم متكاملة
            مدعومة بالذكاء الاصطناعي.
          </p>
        </div>

        <section className="mt-10 overflow-hidden rounded-[2rem] border border-slate-200 bg-white shadow-xl">
          <div className="border-b border-slate-100 px-6 py-5 sm:px-8">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h2 className="text-xl font-black text-slate-950 sm:text-2xl">
                  Runexa Study Agent — العرض باللغة العربية
                </h2>

                <p className="mt-2 max-w-3xl text-sm leading-7 text-slate-600">
                  شاهد Runexa Study وهو يحلل المواد الدراسية وينشئ الملخصات
                  والاختبارات وبطاقات المراجعة وخرائط التعلم والصوت وخطط
                  المراجعة المخصصة.
                </p>
              </div>

              <span className="inline-flex w-fit rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-bold text-slate-600">
                العربية
              </span>
            </div>
          </div>

          <div className="bg-slate-950 p-2 sm:p-4">
            <iframe
              src={STUDY_DEMO_VIDEO}
              title="عرض Runexa Study Agent باللغة العربية"
              className="aspect-video w-full rounded-2xl bg-black"
              allow="autoplay; fullscreen"
              referrerPolicy="strict-origin-when-cross-origin"
              allowFullScreen
            />
          </div>
        </section>

        <section className="mt-10 rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
          <h2 className="text-2xl font-black text-slate-950">
            ماذا يمكن أن يقدم Runexa Study Agent؟
          </h2>

          <div className="mt-6 grid gap-3 sm:grid-cols-2">
            {[
              "إنشاء ملخصات منظمة وشروحات مفصلة",
              "إنشاء اختبارات نظرية وتطبيقية",
              "إنشاء بطاقات مراجعة تلقائياً",
              "إنشاء خرائط تعلم بصرية",
              "دعم التعلم الصوتي",
              "إنشاء خطط مراجعة مخصصة",
              "تحديد نقاط الضعف بعد الاختبارات",
            ].map((item) => (
              <div
                key={item}
                className="flex items-start gap-3 rounded-2xl border border-slate-100 bg-slate-50 px-4 py-3"
              >
                <span className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-green-100 text-sm font-black text-green-700">
                  ✓
                </span>

                <span className="text-sm font-medium leading-7 text-slate-700">
                  {item}
                </span>
              </div>
            ))}
          </div>
        </section>

        <section className="mt-10 rounded-[2rem] bg-slate-950 px-6 py-10 text-center text-white sm:px-10">
          <p className="text-lg font-semibold text-slate-200">
            هل أنت مستعد لتحليل موادك الدراسية؟
          </p>

          <Link
            href="/ar/study"
            className="mt-6 inline-flex rounded-2xl bg-blue-600 px-8 py-4 text-base font-black text-white transition hover:-translate-y-0.5 hover:bg-blue-500"
          >
            جرّب Runexa Study
          </Link>
        </section>
      </div>
    </main>
  );
}