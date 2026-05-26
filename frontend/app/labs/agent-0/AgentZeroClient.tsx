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
    badge: "Concept Preview · Coming Soon",
    title: "Runexa Agent 0",
    subtitle:
      "The future AI safety infrastructure for homes, sensors, cameras, GPS, and intelligent home monitoring.",
    joinWaitlist: "Join Waitlist",
    viewConcept: "View Security Concept",

    commandEyebrow: "Intelligent Safety Command Center",
    commandTitle:
      "One AI layer for cameras, sensors, GPS, alerts, and future smart home systems.",

    thinkingTitle: "How Agent 0 thinks",
    thinkingDesc:
      "Agent 0 combines camera understanding, environmental sensors, GPS presence detection, and AI reasoning into a unified safety intelligence layer designed for future autonomous homes.",
    thinkingSteps: [
      "Cameras detect visual activity.",
      "Sensors confirm physical events.",
      "GPS understands trusted presence.",
      "AI reasoning turns events into risk levels and actions.",
    ],

    visionEyebrow: "System Vision",
    visionTitle: "Camera + Sensors + GPS + AI Reasoning",
    visionDesc:
      "A future command center that can help understand unusual movement, open doors, unknown visitors, sensor alerts, family presence, and security events in real time.",
    labsNotice:
      "Agent 0 is currently a research and concept initiative from Runexa Labs. Features shown on this page are experimental and not publicly available yet.",

    features: [
      {
        title: "AI Camera Reasoning",
        desc: "Understand movement, visitors, unusual activity, and visual events from connected cameras.",
      },
      {
        title: "Sensor Fusion Intelligence",
        desc: "Combine door sensors, motion sensors, vibration, sound, temperature, and environmental signals.",
      },
      {
        title: "GPS Geofencing",
        desc: "Detect trusted presence, family arrival, unknown movement zones, and location-based safety rules.",
      },
      {
        title: "Real-time Smart Alerts",
        desc: "Transform raw events into clear risk levels, explanations, and recommended actions.",
      },
      {
        title: "Smart Home Automation Ready",
        desc: "Future-ready architecture for smart home automation, intelligent monitoring, and connected safety systems.",
      },
      {
        title: "Privacy-first Architecture",
        desc: "Designed with local processing, permission control, and user-owned security data in mind.",
      },
    ],
  },

  fr: {
    badge: "Aperçu concept · Bientôt disponible",
    title: "Runexa Agent 0",
    subtitle:
      "La future infrastructure IA de sécurité pour maisons, capteurs, caméras, GPS et surveillance intelligente du domicile.",
    joinWaitlist: "Rejoindre la liste d’attente",
    viewConcept: "Voir le concept sécurité",

    commandEyebrow: "Centre de commande sécurité intelligent",
    commandTitle:
      "Une couche IA unique pour caméras, capteurs, GPS, alertes et futurs systèmes Smart Home.",

    thinkingTitle: "Comment Agent 0 raisonne",
    thinkingDesc:
      "Agent 0 combine la compréhension caméra, les capteurs environnementaux, la détection de présence GPS et le raisonnement IA dans une couche d’intelligence sécurité unifiée, pensée pour les maisons autonomes du futur.",
    thinkingSteps: [
      "Les caméras détectent l’activité visuelle.",
      "Les capteurs confirment les événements physiques.",
      "Le GPS comprend les présences de confiance.",
      "Le raisonnement IA transforme les événements en niveaux de risque et actions.",
    ],

    visionEyebrow: "Vision système",
    visionTitle: "Camera + Sensors + GPS + AI Reasoning",
    visionDesc:
      "Un futur centre de commande capable d’aider à comprendre les mouvements inhabituels, portes ouvertes, visiteurs inconnus, alertes capteurs, présence familiale et événements de sécurité en temps réel.",
    labsNotice:
      "Agent 0 est actuellement une initiative de recherche et de concept de Runexa Labs. Les fonctionnalités présentées sur cette page sont expérimentales et ne sont pas encore disponibles publiquement.",

    features: [
      {
        title: "AI Camera Reasoning",
        desc: "Comprendre les mouvements, visiteurs, activités inhabituelles et événements visuels provenant de caméras connectées.",
      },
      {
        title: "Sensor Fusion Intelligence",
        desc: "Combiner capteurs de porte, capteurs de mouvement, vibrations, sons, température et signaux environnementaux.",
      },
      {
        title: "GPS Geofencing",
        desc: "Détecter les présences de confiance, l’arrivée de la famille, les zones de mouvement inconnues et les règles de sécurité basées sur la localisation.",
      },
      {
        title: "Real-time Smart Alerts",
        desc: "Transformer les événements bruts en niveaux de risque clairs, explications et actions recommandées.",
      },
      {
        title: "Smart Home Automation Ready",
        desc: "Architecture prête pour l’automatisation Smart Home, la surveillance intelligente et les systèmes de sécurité connectés.",
      },
      {
        title: "Privacy-first Architecture",
        desc: "Conçu avec le traitement local, le contrôle des permissions et la propriété utilisateur des données de sécurité.",
      },
    ],
  },

  ar: {
    badge: "معاينة مفهومية · قريباً",
    title: "Runexa Agent 0",
    subtitle:
      "البنية المستقبلية للأمان بالذكاء الاصطناعي للمنازل والحساسات والكاميرات وGPS والمراقبة المنزلية الذكية.",
    joinWaitlist: "الانضمام إلى قائمة الانتظار",
    viewConcept: "عرض مفهوم الأمان",

    commandEyebrow: "مركز قيادة أمان ذكي",
    commandTitle:
      "طبقة ذكاء اصطناعي واحدة للكاميرات والحساسات وGPS والتنبيهات وأنظمة Smart Home المستقبلية.",

    thinkingTitle: "كيف يفكر Agent 0",
    thinkingDesc:
      "يجمع Agent 0 بين فهم الكاميرا، الحساسات البيئية، اكتشاف الحضور عبر GPS، والاستدلال بالذكاء الاصطناعي داخل طبقة موحدة لذكاء الأمان مصممة للمنازل الذاتية المستقبلية.",
    thinkingSteps: [
      "الكاميرات تكتشف النشاط البصري.",
      "الحساسات تؤكد الأحداث الفعلية.",
      "GPS يفهم الحضور الموثوق.",
      "الاستدلال بالذكاء الاصطناعي يحول الأحداث إلى مستويات خطر وإجراءات.",
    ],

    visionEyebrow: "رؤية النظام",
    visionTitle: "Camera + Sensors + GPS + AI Reasoning",
    visionDesc:
      "مركز قيادة مستقبلي يساعد على فهم الحركة غير المعتادة، الأبواب المفتوحة، الزوار غير المعروفين، تنبيهات الحساسات، حضور العائلة، وأحداث الأمان في الوقت الحقيقي.",
    labsNotice:
      "Agent 0 هو حالياً مبادرة بحثية ومفهومية من Runexa Labs. الميزات المعروضة في هذه الصفحة تجريبية وليست متاحة للعامة بعد.",

    features: [
      {
        title: "AI Camera Reasoning",
        desc: "فهم الحركة والزوار والنشاط غير المعتاد والأحداث البصرية من الكاميرات المتصلة.",
      },
      {
        title: "Sensor Fusion Intelligence",
        desc: "دمج حساسات الأبواب والحركة والاهتزاز والصوت والحرارة والإشارات البيئية.",
      },
      {
        title: "GPS Geofencing",
        desc: "اكتشاف الحضور الموثوق، وصول أفراد العائلة، مناطق الحركة غير المعروفة، وقواعد الأمان المعتمدة على الموقع.",
      },
      {
        title: "Real-time Smart Alerts",
        desc: "تحويل الأحداث الخام إلى مستويات خطر واضحة، تفسيرات، وإجراءات موصى بها.",
      },
      {
        title: "Smart Home Automation Ready",
        desc: "بنية جاهزة لمستقبل أتمتة Smart Home والمراقبة الذكية وأنظمة الأمان المتصلة.",
      },
      {
        title: "Privacy-first Architecture",
        desc: "مصممة مع مراعاة المعالجة المحلية، التحكم في الصلاحيات، وملكية المستخدم لبيانات الأمان.",
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
