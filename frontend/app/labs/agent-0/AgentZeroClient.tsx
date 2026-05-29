"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Runexa Agent 0 | AI Safety Infrastructure & Smart Home Intelligence",

  description:
    "Runexa Agent 0 is a future AI safety infrastructure concept combining cameras, sensors, GPS, and intelligent reasoning for smart home monitoring and autonomous safety systems.",

  keywords: [
    "AI smart home",
    "AI security infrastructure",
    "AI home monitoring",
    "AI camera reasoning",
    "sensor fusion AI",
    "GPS geofencing AI",
    "smart home AI",
    "AI safety system",
    "Runexa Labs",
    "Agent 0",
  ],

  alternates: {
    canonical: "https://runexa.ai/labs/agent-0",
  },

  openGraph: {
    title:
      "Runexa Agent 0 | AI Safety Infrastructure & Smart Home Intelligence",
    description:
      "Future AI infrastructure combining cameras, sensors, GPS, and intelligent reasoning for smart home safety systems.",
    url: "https://runexa.ai/labs/agent-0",
    siteName: "Runexa Systems",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Agent 0",
      },
    ],
    locale: "en_US",
    type: "website",
  },

  twitter: {
    card: "summary_large_image",
    title:
      "Runexa Agent 0 | AI Safety Infrastructure & Smart Home Intelligence",
    description:
      "Future AI infrastructure for cameras, sensors, GPS, and autonomous home monitoring.",
    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

const labels: any = {
  en: {
    badge: "Research Preview · Runexa Labs",

    title: "Runexa Agent 0",

    subtitle:
      "Exploring the future of AI-powered safety, monitoring, and intelligent home awareness.",

    joinWaitlist: "Join Waitlist",

    viewConcept: "Explore the Concept",

    commandEyebrow:
      "Intelligent Safety Platform",

    commandTitle:
      "A unified intelligence layer for cameras, sensors, GPS, and connected environments.",

    thinkingTitle:
      "How Agent 0 works",

    thinkingDesc:
      "Agent 0 explores how visual understanding, environmental sensing, location awareness, and AI reasoning can work together to support future safety and monitoring systems.",

    thinkingSteps: [
      "Visual systems detect activity and changes.",
      "Sensors provide environmental context.",
      "Location awareness helps identify trusted presence.",
      "AI reasoning transforms signals into actionable insights.",
    ],

    visionEyebrow:
      "Product Vision",

    visionTitle:
      "Connected Awareness Through AI",

    visionDesc:
      "A future platform designed to help understand unusual activity, access events, environmental changes, trusted presence, and safety-related situations in real time.",

    labsNotice:
      "Agent 0 is an active research and development initiative from Runexa Labs. Concepts presented on this page are experimental and not currently available as a public product.",

    features: [
      {
        title: "Visual Intelligence",
        desc:
          "Analyze movement, activity, visitors, and events through connected camera systems.",
      },

      {
        title: "Sensor Intelligence",
        desc:
          "Combine signals from environmental, motion, access, and safety sensors into a unified view.",
      },

      {
        title: "Location Awareness",
        desc:
          "Support trusted presence detection, geofencing, and context-aware safety rules.",
      },

      {
        title: "Real-Time Insights",
        desc:
          "Transform raw signals into understandable events, explanations, and recommendations.",
      },

      {
        title: "Automation-Ready Architecture",
        desc:
          "Designed to support future intelligent environments and connected automation systems.",
      },

      {
        title: "Privacy-First Design",
        desc:
          "Built with transparency, user control, and privacy-conscious system design.",
      },
    ],
  },
  fr: {
    badge: "Aperçu recherche · Runexa Labs",

    title: "Runexa Agent 0",

    subtitle:
      "Explorer l’avenir de la sécurité, de la surveillance et de l’intelligence environnementale assistées par l’IA.",

    joinWaitlist: "Rejoindre la liste d’attente",

    viewConcept: "Explorer le concept",

    commandEyebrow:
      "Plateforme de sécurité intelligente",

    commandTitle:
      "Une couche d’intelligence unifiée pour les caméras, les capteurs, le GPS et les environnements connectés.",

    thinkingTitle:
      "Comment fonctionne Agent 0",

    thinkingDesc:
      "Agent 0 explore comment la compréhension visuelle, les capteurs environnementaux, la localisation et le raisonnement IA peuvent fonctionner ensemble pour soutenir les futurs systèmes de sécurité et de surveillance.",

    thinkingSteps: [
      "Les systèmes visuels détectent les activités et les changements.",
      "Les capteurs apportent un contexte environnemental.",
      "La localisation aide à identifier les présences de confiance.",
      "Le raisonnement IA transforme les signaux en informations exploitables.",
    ],

    visionEyebrow:
      "Vision produit",

    visionTitle:
      "Une intelligence connectée grâce à l’IA",

    visionDesc:
      "Une future plateforme conçue pour aider à comprendre les activités inhabituelles, les événements d’accès, les changements environnementaux, les présences de confiance et les situations liées à la sécurité en temps réel.",

    labsNotice:
      "Agent 0 est une initiative active de recherche et développement menée par Runexa Labs. Les concepts présentés sur cette page sont expérimentaux et ne sont actuellement pas disponibles en tant que produit public.",

    features: [
      {
        title: "Intelligence visuelle",
        desc:
          "Analyser les mouvements, les activités, les visiteurs et les événements grâce à des systèmes de caméras connectés.",
      },

      {
        title: "Intelligence des capteurs",
        desc:
          "Combiner les signaux issus des capteurs environnementaux, de mouvement, d’accès et de sécurité dans une vue unifiée.",
      },

      {
        title: "Conscience de la localisation",
        desc:
          "Prendre en charge la détection de présence de confiance, le géorepérage et les règles de sécurité contextuelles.",
      },

      {
        title: "Informations en temps réel",
        desc:
          "Transformer les signaux bruts en événements compréhensibles, explications et recommandations.",
      },

      {
        title: "Architecture prête pour l’automatisation",
        desc:
          "Conçue pour prendre en charge les futurs environnements intelligents et systèmes d’automatisation connectés.",
      },

      {
        title: "Conception axée sur la confidentialité",
        desc:
          "Développée autour de la transparence, du contrôle utilisateur et du respect de la vie privée.",
      },
    ],
  },

 ar: {
    badge:
      "معاينة بحثية · Runexa Labs",

    title:
      "Runexa Agent 0",

    subtitle:
      "استكشاف مستقبل الأمان والمراقبة والوعي البيئي المدعوم بالذكاء الاصطناعي.",

    joinWaitlist:
      "الانضمام إلى قائمة الانتظار",

    viewConcept:
      "استكشاف المفهوم",

    commandEyebrow:
      "منصة أمان ذكية",

    commandTitle:
      "طبقة ذكاء موحدة للكاميرات وأجهزة الاستشعار والموقع والبيئات المتصلة.",

    thinkingTitle:
      "كيف يعمل Agent 0",

    thinkingDesc:
      "يستكشف Agent 0 كيفية دمج الفهم البصري والاستشعار البيئي والوعي بالموقع والاستدلال بالذكاء الاصطناعي لدعم أنظمة الأمان والمراقبة المستقبلية.",

    thinkingSteps: [
      "تكتشف الأنظمة البصرية الأنشطة والتغيرات.",
      "توفر أجهزة الاستشعار سياقاً بيئياً إضافياً.",
      "يساعد الوعي بالموقع على تحديد الحضور الموثوق.",
      "يحوّل الاستدلال بالذكاء الاصطناعي الإشارات إلى رؤى قابلة للتنفيذ.",
    ],

    visionEyebrow:
      "رؤية المنتج",

    visionTitle:
      "وعي متصل مدعوم بالذكاء الاصطناعي",

    visionDesc:
      "منصة مستقبلية مصممة للمساعدة في فهم الأنشطة غير المعتادة وأحداث الوصول والتغيرات البيئية والحضور الموثوق والحالات المرتبطة بالأمان في الوقت الفعلي.",

    labsNotice:
      "Agent 0 هو مبادرة بحث وتطوير نشطة من Runexa Labs. المفاهيم المعروضة في هذه الصفحة تجريبية وليست متاحة حالياً كمنتج عام.",

    features: [
      {
        title: "الذكاء البصري",
        desc:
          "تحليل الحركة والأنشطة والزوار والأحداث من خلال أنظمة الكاميرات المتصلة.",
      },

      {
        title: "ذكاء أجهزة الاستشعار",
        desc:
          "دمج الإشارات القادمة من أجهزة الاستشعار البيئية والحركية وأنظمة الوصول والأمان ضمن رؤية موحدة.",
      },

      {
        title: "الوعي بالموقع",
        desc:
          "دعم اكتشاف الحضور الموثوق والتسييج الجغرافي وقواعد الأمان المعتمدة على السياق.",
      },

      {
        title: "رؤى فورية",
        desc:
          "تحويل الإشارات الخام إلى أحداث مفهومة وتفسيرات وتوصيات عملية.",
      },

      {
        title: "بنية جاهزة للأتمتة",
        desc:
          "مصممة لدعم البيئات الذكية المستقبلية وأنظمة الأتمتة المتصلة.",
      },

      {
        title: "تصميم يركز على الخصوصية",
        desc:
          "مبنية على الشفافية وتحكم المستخدم واحترام خصوصية البيانات.",
      },
    ],
  },
};

const jsonLd = {
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  name: "Runexa Agent 0",
  applicationCategory: "SecurityApplication",
  operatingSystem: "Web",
  description:
    "Future AI safety infrastructure combining cameras, sensors, GPS, and intelligent reasoning for smart homes.",
  url: "https://runexa.ai/labs/agent-0",
  publisher: {
    "@type": "Organization",
    name: "Runexa Systems",
    url: "https://runexa.ai",
  },
};

export default function AgentZeroClient() {
  const [language, setLanguage] = useState("en");
  const t = labels[language] || labels.en;

  useEffect(() => {
    const saved = localStorage.getItem("locale");

    if (saved && labels[saved]) {
      setLanguage(saved);
    }

    const handleLocaleChange = () => {
      const nextLocale = localStorage.getItem("locale");

      if (nextLocale && labels[nextLocale]) {
        setLanguage(nextLocale);
      }
    };

    window.addEventListener("locale-change", handleLocaleChange);

    return () => {
      window.removeEventListener("locale-change", handleLocaleChange);
    };
  }, []);

  return (
    <main
      dir={language === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-950 text-white"
    >
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(jsonLd),
        }}
      />

      <section className="relative overflow-hidden px-6 py-24">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-600/20 via-slate-950 to-cyan-500/10" />
        <div className="absolute left-1/2 top-20 h-72 w-72 -translate-x-1/2 rounded-full bg-blue-500/20 blur-3xl" />

        <div className="relative mx-auto max-w-6xl">
          <span className="inline-flex rounded-full border border-white/10 bg-white/10 px-4 py-2 text-sm font-semibold text-blue-100">
            {t.badge}
          </span>

          <h1 className="mt-8 max-w-4xl text-5xl font-bold tracking-tight md:text-7xl">
            {t.title}
          </h1>

          <p className="mt-6 max-w-3xl text-xl leading-8 text-slate-300">
            {t.subtitle}
          </p>

          <div className="mt-10 flex flex-wrap gap-4">
            <Link
              href="/labs/agent-0/waitlist"
              className="rounded-xl bg-white px-6 py-3 font-semibold text-slate-950 hover:bg-slate-100"
            >
              {t.joinWaitlist}
            </Link>

            <a
              href="#concept"
              className="rounded-xl border border-white/10 bg-white/5 px-6 py-3 font-semibold text-white hover:bg-white/10"
            >
              {t.viewConcept}
            </a>
          </div>
        </div>
      </section>

      <section className="px-6 py-16">
        <div className="mx-auto max-w-6xl">
          <div className="mb-10 max-w-3xl">
            <p className="text-sm font-semibold uppercase tracking-wide text-cyan-300">
              {t.commandEyebrow}
            </p>

            <h2 className="mt-3 text-3xl font-bold md:text-4xl">
              {t.commandTitle}
            </h2>
          </div>

          <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
            {t.features.map((feature: any) => (
              <div
                key={feature.title}
                className="rounded-3xl border border-white/10 bg-white/[0.04] p-6 shadow-2xl shadow-blue-950/20"
              >
                <div className="mb-5 h-2 w-2 rounded-full bg-cyan-300" />

                <h3 className="text-lg font-semibold">
                  {feature.title}
                </h3>

                <p className="mt-3 text-sm leading-6 text-slate-400">
                  {feature.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="concept" className="px-6 py-16">
        <div className="mx-auto grid max-w-6xl gap-8 lg:grid-cols-2">
          <div className="rounded-3xl border border-white/10 bg-white/[0.04] p-8">
            <h2 className="text-3xl font-bold">
              {t.thinkingTitle}
            </h2>

            <p className="mt-5 leading-8 text-slate-300">
              {t.thinkingDesc}
            </p>

            <div className="mt-8 space-y-4 text-sm text-slate-300">
              {t.thinkingSteps.map((step: string, index: number) => (
                <div
                  key={step}
                  className={`rounded-2xl border p-4 ${
                    index === t.thinkingSteps.length - 1
                      ? "border-cyan-400/20 bg-cyan-500/10 text-cyan-100"
                      : "border-white/10 bg-slate-900/80"
                  }`}
                >
                  {step}
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-3xl border border-cyan-400/20 bg-cyan-500/10 p-8">
            <p className="text-sm font-semibold uppercase tracking-wide text-cyan-200">
              {t.visionEyebrow}
            </p>

            <h3 className="mt-4 text-2xl font-bold">
              {t.visionTitle}
            </h3>

            <p className="mt-5 leading-8 text-cyan-50">
              {t.visionDesc}
            </p>

            <div className="mt-8 rounded-2xl border border-white/10 bg-slate-950/70 p-5 text-sm text-slate-300">
              {t.labsNotice}
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
