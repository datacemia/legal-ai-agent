import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Démo Coach Finance Runexa",

  description:
    "Découvrez une démonstration complète du Coach Finance Runexa. Analysez documents financiers, habitudes de dépenses, abonnements, opportunités d’économies et insights financiers personnels avec l’IA.",

  keywords: [
  "Runexa Finance Coach",
  "démo IA finance",
  "analyse financière par IA",
  "IA pour finances personnelles",
  "détection d’abonnements par IA",
  "analyse des dépenses par IA",
  "analyse des économies par IA",
  "coach financier IA",
  "gestion budgétaire par IA",
  "assistant financier IA",
  "suivi des dépenses",
  "optimisation des économies",
  "analyse bancaire intelligente",
  "gestion des finances personnelles",
  "planification financière",
  "éducation financière",
  "analyse des revenus et dépenses",
  "détection des dépenses récurrentes",
  "identification des opportunités d’épargne",
  "analyse des habitudes financières",
  "tableau de bord financier IA",
  "conseils financiers assistés par IA",
  "outil d’analyse financière",
  "IA pour la gestion de budget",
  "finance personnelle intelligente",
 ],
  alternates: {
    canonical: "https://runexa.ai/fr/demo/finance-agent",
    languages: {
      en: "https://runexa.ai/en/demo/finance-agent",
      fr: "https://runexa.ai/fr/demo/finance-agent",
      ar: "https://runexa.ai/ar/demo/finance-agent",
      "x-default": "https://runexa.ai/demo/finance-agent",
    },
  },

  openGraph: {
    title: "Démo Coach Finance Runexa",

    description:
      "Découvrez une démonstration complète du Coach Finance Runexa. Analysez documents financiers, habitudes de dépenses, abonnements, opportunités d’économies et insights financiers personnels avec l’IA.",

    url: "https://runexa.ai/fr/demo/finance-agent",

    siteName: "Runexa Systems",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Finance Coach Demo",
      },
    ],

    locale: "fr_FR",

    alternateLocale: ["en_US", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Démo Coach Finance Runexa",

    description:
      "Découvrez une démonstration complète du Coach Finance Runexa. Analysez documents financiers, habitudes de dépenses, abonnements, opportunités d’économies et insights financiers personnels avec l’IA.",

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

  name: "Coach Finance Runexa",

  applicationCategory: "FinanceApplication",

  operatingSystem: "Web",

  url: "https://runexa.ai/fr/demo/finance-agent",

  inLanguage: "fr",

  description:
    "Découvrez une démonstration complète du Coach Finance Runexa. Analysez documents financiers, habitudes de dépenses, abonnements, opportunités d’économies et insights financiers personnels avec l’IA.",

  publisher: {
    "@type": "Organization",
    name: "Runexa Systems LLC",
    url: "https://runexa.ai",
  },
};

export default function FinanceAgentDemoPage() {
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
          Démo Coach Finance Runexa
        </h1>

        <p className="mt-6 max-w-3xl text-lg text-slate-600">
          Importez des documents financiers, relevés, fichiers de dépenses et données de finance personnelle pour générer des insights de dépenses, détecter les abonnements, trouver des opportunités d’économies et obtenir un coaching financier personnalisé par IA.
        </p>

        <div className="mt-10">
          <Image
            src="/demo/finance-agent-demo-fr.png"
            alt="Démo Coach Finance Runexa"
            width={1440}
            height={5000}
            priority
            className="rounded-3xl border border-slate-200 shadow-lg"
          />
        </div>

        <div className="mt-10 rounded-3xl border bg-white p-8 shadow-sm">
          <h2 className="text-2xl font-bold text-slate-900">
            Que peut faire le Coach Finance ?
          </h2>

          <ul className="mt-4 space-y-3 text-slate-600">
            <li>✓ Détecter les abonnements récurrents</li>
            <li>✓ Analyser les habitudes de dépenses</li>
            <li>✓ Identifier des opportunités d’économies</li>
            <li>✓ Résumer l’activité financière</li>
            <li>✓ Signaler les dépenses inhabituelles ou risquées</li>
            <li>✓ Générer des insights financiers personnalisés</li>
          </ul>
        </div>

        <div className="mt-10 text-center">
          <p className="mb-6 text-lg text-slate-600">
            Prêt à analyser vos propres documents financiers ?
          </p>

          <Link
            href="/fr/finance"
            className="inline-flex rounded-xl bg-blue-600 px-8 py-4 text-lg font-semibold text-white transition hover:bg-blue-700"
          >
            Essayer le Coach Finance
          </Link>
        </div>
      </div>
    </main>
  );
}
