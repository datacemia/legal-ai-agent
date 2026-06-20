import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Démo Agent Décision Business Runexa",

  description:
    "Découvrez une démonstration complète de l’Agent Décision Business Runexa. Analysez les données business, KPI, risques, opportunités, prévisions et insights exécutifs avec l’IA.",

  keywords: [
  "Runexa Business Decision Agent",
  "démo IA business",
  "intelligence d’affaires par IA",
  "aide à la décision commerciale",
  "analyse des KPI par IA",
  "analyse des risques commerciaux",
  "prévisions par IA",
  "IA pour dirigeants",
  "analyse stratégique par IA",
  "tableau de bord intelligent",
  "analyse de performance d’entreprise",
  "suivi des indicateurs clés",
  "prise de décision assistée par IA",
  "analyse des opportunités commerciales",
  "analyse concurrentielle par IA",
  "prévisions de croissance",
  "optimisation des performances",
  "business intelligence intelligente",
  "pilotage d’entreprise par IA",
  "analyse de données d’entreprise",
  "gestion des risques stratégiques",
  "assistant décisionnel IA",
  "IA pour entrepreneurs",
  "analyse des tendances du marché",
  "outil d’aide à la décision",
 ],

  alternates: {
    canonical: "https://runexa.ai/fr/demo/business-agent",
    languages: {
      en: "https://runexa.ai/en/demo/business-agent",
      fr: "https://runexa.ai/fr/demo/business-agent",
      ar: "https://runexa.ai/ar/demo/business-agent",
      "x-default": "https://runexa.ai/demo/business-agent",
    },
  },

  openGraph: {
    title: "Démo Agent Décision Business Runexa",

    description:
      "Découvrez une démonstration complète de l’Agent Décision Business Runexa. Analysez les données business, KPI, risques, opportunités, prévisions et insights exécutifs avec l’IA.",

    url: "https://runexa.ai/fr/demo/business-agent",

    siteName: "Runexa Systems",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Business Decision Agent Demo",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Démo Agent Décision Business Runexa",

    description:
      "Découvrez une démonstration complète de l’Agent Décision Business Runexa. Analysez les données business, KPI, risques, opportunités, prévisions et insights exécutifs avec l’IA.",

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

  name: "Agent Décision Business Runexa",

  applicationCategory: "BusinessApplication",

  operatingSystem: "Web",

  url: "https://runexa.ai/fr/demo/business-agent",

  inLanguage: "fr",

  description:
    "Découvrez une démonstration complète de l’Agent Décision Business Runexa. Analysez les données business, KPI, risques, opportunités, prévisions et insights exécutifs avec l’IA.",

  publisher: {
    "@type": "Organization",
    name: "Runexa Systems LLC",
    url: "https://runexa.ai",
  },
};

export default function BusinessAgentDemoPage() {
  return (
    <main
      dir="ltr"
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
          Démo Agent Décision Business Runexa
        </h1>

        <p className="mt-6 max-w-3xl text-lg text-slate-600">
          Importez des rapports business, fichiers KPI, données de ventes, documents opérationnels et notes stratégiques pour générer des résumés exécutifs, risques, opportunités, prévisions et aides à la décision avec l’IA.
        </p>

        <div className="mt-10">
          <Image
            src="/demo/business-agent-demo-fr.png"
            alt="Démo Agent Décision Business Runexa"
            width={1440}
            height={5000}
            priority
            className="rounded-3xl border border-slate-200 shadow-lg"
          />
        </div>

        <div className="mt-10 rounded-3xl border bg-white p-8 shadow-sm">
          <h2 className="text-2xl font-bold text-slate-900">
            Que peut faire l’Agent Décision Business ?
          </h2>

          <ul className="mt-4 space-y-3 text-slate-600">
            <li>✓ Analyser les KPI et la performance business</li>
            <li>✓ Détecter les risques et problèmes opérationnels</li>
            <li>✓ Identifier les opportunités stratégiques</li>
            <li>✓ Générer des résumés exécutifs</li>
            <li>✓ Soutenir les prévisions et la prise de décision</li>
            <li>✓ Transformer les données business en insights clairs</li>
          </ul>
        </div>

        <div className="mt-10 text-center">
          <p className="mb-6 text-lg text-slate-600">
            Prêt à analyser vos propres données business ?
          </p>

          <Link
            href="/fr/business"
            className="inline-flex rounded-xl bg-blue-600 px-8 py-4 text-lg font-semibold text-white transition hover:bg-blue-700"
          >
            Essayer l’Agent Business
          </Link>
        </div>
      </div>
    </main>
  );
}
