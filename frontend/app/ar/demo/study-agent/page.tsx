import Image from "next/image";
import Link from "next/link";

export default function StudyAgentDemoArPage() {
  return (
    <main
      dir="rtl"
      className="min-h-screen bg-slate-50 px-6 py-16"
    >
      <div className="mx-auto max-w-6xl">
        <h1 className="text-5xl font-bold tracking-tight text-slate-900">
          عرض توضيحي لوكيل الدراسة من Runexa
        </h1>

        <p className="mt-6 max-w-3xl text-lg text-slate-600">
          قم بتحليل ملفاتك الدراسية وموادك التعليمية باستخدام
          الذكاء الاصطناعي. أنشئ ملخصات واختبارات وبطاقات تعليمية
          وخطط دراسة مخصصة بسهولة.
        </p>

        <div className="mt-10">
          <Image
            src="/demo/study-agent-demo-ar.png"
            alt="عرض توضيحي لوكيل الدراسة من Runexa"
            width={1440}
            height={5000}
            sizes="(max-width: 768px) 100vw, (max-width: 1280px) 90vw, 1152px"
            className="h-auto w-full rounded-3xl border border-slate-200 shadow-lg"
          />
        </div>

        <div className="mt-10 text-center">
          <Link
            href="/ar/study"
            className="inline-flex rounded-xl bg-blue-600 px-6 py-3 font-semibold text-white transition hover:bg-blue-700"
          >
            جرّب وكيل الدراسة
          </Link>
        </div>
      </div>
    </main>
  );
}