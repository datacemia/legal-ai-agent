import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Démo Agent Juridique Runexa",

  description:
    "Découvrez une démonstration complète de l’Agent Juridique Runexa. Analysez des contrats, détectez les clauses à risque, extrayez les obligations, résumez les documents juridiques et examinez les documents de conformité avec l’IA.",

  keywords: [
    "Runexa Legal Agent",
    "démo IA juridique",
    "analyse de contrats par IA",
    "révision de contrats par IA",
    "analyse de documents juridiques",
    "détection des risques contractuels",
    "assistant juridique IA",
    "IA pour les processus juridiques",
    "analyse juridique automatisée",
    "résumé de contrats par IA",
    "identification des clauses importantes",
    "évaluation des risques contractuels",
    "vérification de contrats",
    "lecture intelligente de contrats",
    "analyse de documents légaux",
    "conformité contractuelle",
    "outil IA pour juristes",
    "assistant d’analyse juridique",
    "workflow juridique intelligent",
    "revue de documents par IA",
    "analyse de conditions contractuelles",
    "détection de clauses à risque",
    "IA pour cabinets juridiques",
    "gestion des contrats",
    "intelligence artificielle juridique",
  ],

  alternates: {
    canonical: "https://runexa.ai/fr/demo/legal-agent",
    languages: {
      en: "https://runexa.ai/en/demo/legal-agent",
      fr: "https://runexa.ai/fr/demo/legal-agent",
      ar: "https://runexa.ai/ar/demo/legal-agent",
      "x-default": "https://runexa.ai/demo/legal-agent",
    },
  },

  openGraph: {
    title: "Démo Agent Juridique Runexa",
    description:
      "Découvrez une démonstration complète de l’Agent Juridique Runexa. Analysez des contrats, détectez les clauses à risque, extrayez les obligations, résumez les documents juridiques et examinez les documents de conformité avec l’IA.",
    url: "https://runexa.ai/fr/demo/legal-agent",
    siteName: "Runexa Systems",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Legal Agent Demo",
      },
    ],
    locale: "fr_FR",
    alternateLocale: ["en_US", "ar_AR"],
    type: "website",
  },

  twitter: {
    card: "summary_large_image",
    title: "Démo Agent Juridique Runexa",
    description:
      "Découvrez une démonstration complète de l’Agent Juridique Runexa. Analysez des contrats, détectez les clauses à risque, extrayez les obligations, résumez les documents juridiques et examinez les documents de conformité avec l’IA.",
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
  name: "Agent Juridique Runexa",
  applicationCategory: "BusinessApplication",
  operatingSystem: "Web",
  url: "https://runexa.ai/fr/demo/legal-agent",
  inLanguage: "fr",
  description:
    "Découvrez une démonstration complète de l’Agent Juridique Runexa. Analysez des contrats, détectez les clauses à risque, extrayez les obligations, résumez les documents juridiques et examinez les documents de conformité avec l’IA.",
  publisher: {
    "@type": "Organization",
    name: "Runexa Systems LLC",
    url: "https://runexa.ai",
  },
};

export default function LegalAgentDemoPage() {
  return (
    <main dir="ltr" className="min-h-screen bg-slate-50 px-6 py-16">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(jsonLd),
        }}
      />

      <div className="mx-auto max-w-6xl">
        <h1 className="text-5xl font-bold tracking-tight text-slate-900">
          Démo Agent Juridique Runexa
        </h1>

        <p className="mt-6 max-w-3xl text-lg text-slate-600">
          Importez des contrats, accords, politiques et documents juridiques
          pour générer des résumés IA, détecter les clauses à risque, extraire
          les obligations, identifier les échéances et obtenir une analyse
          juridique structurée.
        </p>

        <div className="mt-10">
          <Image
            src="/demo/legal-agent-demo-fr.png"
            alt="Démo Agent Juridique Runexa"
            width={1440}
            height={5000}
            sizes="(max-width: 768px) 100vw, (max-width: 1280px) 90vw, 1152px"
            className="h-auto w-full rounded-3xl border border-slate-200 shadow-lg"
          />
        </div>

        <div className="mt-10 rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
          <h2 className="text-2xl font-bold text-slate-900">
            Que peut faire l’Agent Juridique ?
          </h2>

          <ul className="mt-4 space-y-3 text-slate-600">
            <li>✓ Analyser les contrats et accords</li>
            <li>✓ Détecter les clauses à risque</li>
            <li>✓ Extraire les obligations et échéances</li>
            <li>✓ Résumer les documents juridiques</li>
            <li>✓ Examiner les politiques et documents de conformité</li>
            <li>✓ Générer des insights juridiques structurés</li>
          </ul>
        </div>

        <div className="mt-10 text-center">
          <p className="mb-6 text-lg text-slate-600">
            Prêt à analyser vos propres documents juridiques ?
          </p>

          <Link
            href="/fr/upload"
            className="inline-flex rounded-xl bg-blue-600 px-8 py-4 text-lg font-semibold text-white transition hover:bg-blue-700"
          >
            Essayer l’Agent Juridique
          </Link>
        </div>
      </div>
    </main>
  );
}