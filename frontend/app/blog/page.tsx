import Link from "next/link";
import type { Metadata } from "next";
import { cookies } from "next/headers";


type Locale = "en" | "fr" | "ar";

async function getPageLocale(): Promise<Locale> {
  const cookieStore = await cookies();
  const value =
    cookieStore.get("locale")?.value ||
    cookieStore.get("language")?.value ||
    "en";

  return value === "fr" || value === "ar" ? value : "en";
}

export async function generateMetadata(): Promise<Metadata> {
  const locale = await getPageLocale();

  const metadataTranslations = {
    en: {
      title:
        "Runexa AI Blog | Legal AI, Finance AI, Business Intelligence & Study AI",
      description:
        "Insights about AI contract analysis, finance AI, business intelligence, AI workflows, and enterprise AI systems.",
    },

    fr: {
      title:
        "Blog Runexa AI | IA juridique, IA finance, IA business et IA étude",
      description:
        "Insights sur l’analyse juridique IA, la finance IA, l’intelligence business, les workflows IA et les systèmes IA entreprise.",
    },

    ar: {
      title:
        "مدونة Runexa AI | الذكاء القانوني والمالي وذكاء الأعمال وذكاء الدراسة",
      description:
        "مقالات ورؤى حول التحليل القانوني بالذكاء الاصطناعي والذكاء المالي وذكاء الأعمال وتدفقات العمل الذكية.",
    },
  };

  const t =
    metadataTranslations[
      locale as keyof typeof metadataTranslations
    ] || metadataTranslations.en;

  return {
    title: t.title,
    description: t.description,
    keywords: [
      "AI blog",
      "legal AI",
      "finance AI",
      "business intelligence",
      "study AI",
      "enterprise AI",
    ],

    alternates: {
      canonical: "https://runexa.ai/blog",
    },

    openGraph: {
      title: t.title,
      description: t.description,
      url: "https://runexa.ai/blog",
      siteName: "Runexa",
      type: "website",
      images: [
        {
          url: "/og-image.png",
          width: 1200,
          height: 630,
          alt: "Runexa AI Blog",
        },
      ],
    },

    twitter: {
      card: "summary_large_image",
      title: t.title,
      description: t.description,
      images: ["/og-image.png"],
    },
  };
}


export default async function BlogPage() {
  const locale = await getPageLocale();

  const translations = {
    en: {
      badge: "Runexa Blog",
      title: "Enterprise AI Insights & Workflows",
      subtitle:
        "Insights about AI document analysis, finance AI, legal AI, business intelligence, enterprise AI systems, and intelligent workflows.",

      readArticle: "Read article →",

      ctaTitle:
        "Explore enterprise AI workflows with Runexa",

      ctaDescription:
        "Analyze contracts, financial statements, business data, and study materials with specialized AI agents.",

      pricing: "View Pricing",
      developers: "Developers",

      legalAi: "Legal AI",
      financeAi: "Finance AI",
      studyAi: "Study AI",
      enterpriseAi: "Enterprise AI",
      businessAi: "Business AI",
    },

    fr: {
      badge: "Blog Runexa",
      title: "Insights et workflows IA entreprise",
      subtitle:
        "Insights sur l’analyse documentaire IA, la finance IA, l’IA juridique, l’intelligence business et les workflows intelligents.",

      readArticle: "Lire l’article →",

      ctaTitle:
        "Explorez les workflows IA entreprise avec Runexa",

      ctaDescription:
        "Analysez contrats, données financières, business et contenus pédagogiques avec des agents IA spécialisés.",

      pricing: "Voir les tarifs",
      developers: "Développeurs",

      legalAi: "IA juridique",
      financeAi: "IA finance",
      studyAi: "IA étude",
      enterpriseAi: "IA entreprise",
      businessAi: "IA business",
    },

    ar: {
      badge: "مدونة Runexa",
      title: "رؤى وتدفقات عمل الذكاء الاصطناعي للمؤسسات",
      subtitle:
        "رؤى حول تحليل المستندات بالذكاء الاصطناعي والذكاء المالي والذكاء القانوني وذكاء الأعمال وتدفقات العمل الذكية.",

      readArticle: "قراءة المقال ←",

      ctaTitle:
        "استكشف تدفقات عمل الذكاء الاصطناعي للمؤسسات مع Runexa",

      ctaDescription:
        "حلّل العقود والبيانات المالية وبيانات الأعمال والمواد الدراسية باستخدام وكلاء ذكاء اصطناعي متخصصين.",

      pricing: "عرض الأسعار",
      developers: "المطورون",

      legalAi: "الذكاء القانوني",
      financeAi: "الذكاء المالي",
      studyAi: "ذكاء الدراسة",
      enterpriseAi: "ذكاء المؤسسات",
      businessAi: "ذكاء الأعمال",
    },
  };

  const t =
    translations[
      locale as keyof typeof translations
    ] || translations.en;

  const articles = [
    {
      title:
        locale === "fr"
          ? "Analyse de contrats IA"
          : locale === "ar"
          ? "تحليل العقود بالذكاء الاصطناعي"
          : "AI Contract Analysis",
  
      category: t.legalAi,
  
      href: "/blog/ai-contract-analysis",
  
      description:
        locale === "fr"
          ? "Comment l’IA analyse les contrats, clauses à risque et obligations juridiques."
          : locale === "ar"
          ? "كيف يساعد الذكاء الاصطناعي في تحليل العقود والبنود الخطرة والالتزامات القانونية."
          : "How AI helps analyze contracts, risky clauses, and legal obligations.",
    },
  
    {
      title:
        locale === "fr"
          ? "Analyse financière IA"
          : locale === "ar"
          ? "التحليل المالي بالذكاء الاصطناعي"
          : "AI Finance Analysis",
  
      category: t.financeAi,
  
      href: "/blog/ai-finance-analysis",
  
      description:
        locale === "fr"
          ? "Utiliser l’IA pour comprendre dépenses, abonnements et habitudes financières."
          : locale === "ar"
          ? "استخدام الذكاء الاصطناعي لفهم المصاريف والاشتراكات والعادات المالية."
          : "Using AI to understand spending patterns, subscriptions, and financial habits.",
    },
  
    {
      title:
        locale === "fr"
          ? "Assistant IA pour les études"
          : locale === "ar"
          ? "مساعد الدراسة بالذكاء الاصطناعي"
          : "AI Study Assistant",
  
      category: t.studyAi,
  
      href: "/blog/ai-study-assistant",
  
      description:
        locale === "fr"
          ? "Comment l’IA améliore résumés, quiz, flashcards et workflows d’apprentissage."
          : locale === "ar"
          ? "كيف يحسن الذكاء الاصطناعي الملخصات والاختبارات والبطاقات التعليمية."
          : "How AI improves summaries, quizzes, flashcards, and learning workflows.",
    },
  
    {
      title:
        locale === "fr"
          ? "Workflows IA entreprise"
          : locale === "ar"
          ? "تدفقات عمل الذكاء الاصطناعي للمؤسسات"
          : "Enterprise AI Workflows",
  
      category: t.enterpriseAi,
  
      href: "/blog/enterprise-ai-workflows",
  
      description:
        locale === "fr"
          ? "Comment les organisations construisent des workflows IA pour les opérations business."
          : locale === "ar"
          ? "كيف تبني المؤسسات تدفقات عمل ذكاء اصطناعي للعمليات واتخاذ القرار."
          : "How organizations build AI workflows for business operations and decision support.",
    },
  
    {
      title:
        locale === "fr"
          ? "Business Intelligence IA"
          : locale === "ar"
          ? "ذكاء الأعمال بالذكاء الاصطناعي"
          : "AI Business Intelligence",
  
      category: t.businessAi,
  
      href: "/blog/ai-business-intelligence",
  
      description:
        locale === "fr"
          ? "Utiliser l’IA pour analyser les données business, risques et opportunités stratégiques."
          : locale === "ar"
          ? "استخدام الذكاء الاصطناعي لتحليل بيانات الأعمال والمخاطر والفرص."
          : "Using AI to analyze business data, risks, and strategic opportunities.",
    },
  ];
  return (
    <main
      dir={locale === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-6 py-20 text-slate-900"
    >
      <section className="mx-auto max-w-6xl">
        <p className="font-semibold text-blue-600">
          {t.badge}
        </p>

        <h1 className="mt-4 text-5xl font-bold tracking-tight">
          {t.title}
        </h1>

        <p className="mt-6 max-w-3xl text-lg text-slate-600">
          {t.subtitle}
        </p>

        <div className="mt-12 grid gap-6 md:grid-cols-2">
          {articles.map((article) => (
            <Link
              key={article.href}
              href={article.href}
              className="rounded-3xl border bg-white p-8 shadow-sm transition hover:-translate-y-1 hover:shadow-md"
            >
              <p className="text-sm font-semibold text-blue-600">
                {article.category}
              </p>

              <h2 className="mt-3 text-2xl font-bold">
                {article.title}
              </h2>

              <p className="mt-4 leading-7 text-slate-600">
                {article.description}
              </p>

              <div className="mt-6 text-sm font-semibold text-blue-600">
                {t.readArticle}
              </div>
            </Link>
          ))}
        </div>

        <section className="mt-20 rounded-3xl bg-blue-600 p-10 text-white">
          <h2 className="text-3xl font-bold">
            {t.ctaTitle}
          </h2>

          <p className="mt-4 max-w-2xl text-blue-100">
            {t.ctaDescription}
          </p>

          <div className="mt-8 flex flex-wrap gap-4">
            <Link
              href="/pricing"
              className="rounded-xl bg-white px-6 py-3 text-sm font-semibold text-blue-600"
            >
              {t.pricing}
            </Link>

            <Link
              href="/developers"
              className="rounded-xl border border-blue-300 px-6 py-3 text-sm font-semibold text-white"
            >
              {t.developers}
            </Link>
          </div>
        </section>
      </section>

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "Blog",
            name: "Runexa AI Blog",
            description:
              "Insights about legal AI, finance AI, enterprise AI workflows, business intelligence, and AI-powered operational systems.",
            url: "https://runexa.ai/blog",
            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
            },
          }),
        }}
      />
    </main>
  );
}
