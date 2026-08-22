import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Démo Runexa Study Agent | Runexa Systems",
  description:
    "Découvrez Runexa Study Agent en action. Transformez vos supports d’étude en résumés IA, quiz, flashcards, cartes d’apprentissage, audio et plans de révision personnalisés.",

  alternates: {
    canonical: "https://runexa.ai/fr/demo/study-agent",
    languages: {
      en: "https://runexa.ai/en/demo/study-agent",
      fr: "https://runexa.ai/fr/demo/study-agent",
      ar: "https://runexa.ai/ar/demo/study-agent",
      "x-default": "https://runexa.ai/demo/study-agent",
    },
  },

  openGraph: {
    title: "Démo Runexa Study Agent",
    description:
      "Découvrez comment Runexa Study transforme vos supports de cours en un espace d’apprentissage complet propulsé par l’IA.",
    url: "https://runexa.ai/fr/demo/study-agent",
    siteName: "Runexa Systems",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Démo Runexa Study Agent",
      },
    ],
    locale: "fr_FR",
    type: "website",
  },

  twitter: {
    card: "summary_large_image",
    title: "Démo Runexa Study Agent",
    description:
      "Résumés IA, quiz, flashcards, cartes d’apprentissage, audio et plans de révision personnalisés.",
    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

const STUDY_DEMO_VIDEO =
  "https://drive.google.com/file/d/178NFUtjiyfwhau-EwGqtYwUXn4pDaIxi/preview";

const jsonLd = {
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  name: "Runexa Study Agent",
  applicationCategory: "EducationalApplication",
  operatingSystem: "Web",
  url: "https://runexa.ai/fr/demo/study-agent",
  inLanguage: "fr",
  description:
    "Assistant d’étude IA pour générer des résumés, quiz, flashcards, cartes d’apprentissage, audio et plans de révision personnalisés.",
};

export default function StudyAgentDemoFrPage() {
  return (
    <main
      lang="fr"
      className="min-h-screen bg-slate-50 px-4 py-14 sm:px-6 sm:py-16"
    >
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(jsonLd),
        }}
      />

      <div className="mx-auto max-w-6xl">
        {/* Hero */}
        <div className="text-center">
          <span className="inline-flex rounded-full border border-blue-200 bg-blue-50 px-4 py-1.5 text-xs font-bold uppercase tracking-[0.18em] text-blue-700">
            Démonstration
          </span>

          <h1 className="mx-auto mt-5 max-w-4xl text-4xl font-black tracking-tight text-slate-950 sm:text-5xl">
            Démo Runexa Study Agent
          </h1>

          <p className="mx-auto mt-5 max-w-3xl text-base leading-7 text-slate-600 sm:text-lg">
            Découvrez comment Runexa Study transforme vos supports de cours en
            un espace d’apprentissage complet propulsé par l’IA.
          </p>
        </div>

        {/* Video */}
        <section className="mt-10 overflow-hidden rounded-[2rem] border border-slate-200 bg-white shadow-xl">
          <div className="border-b border-slate-100 px-6 py-5 sm:px-8">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h2 className="text-xl font-black text-slate-950 sm:text-2xl">
                  Runexa Study Agent — Démo en français
                </h2>

                <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-600">
                  Regardez Runexa Study analyser un support pédagogique et
                  générer des résumés, quiz, flashcards, cartes
                  d’apprentissage, audio et plans de révision personnalisés.
                </p>
              </div>

              <span className="inline-flex w-fit rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-bold text-slate-600">
                Français
              </span>
            </div>
          </div>

          <div className="bg-slate-950 p-2 sm:p-4">
            <iframe
              src={STUDY_DEMO_VIDEO}
              title="Démonstration Runexa Study Agent en français"
              className="aspect-video w-full rounded-2xl bg-black"
              allow="autoplay; fullscreen"
              referrerPolicy="strict-origin-when-cross-origin"
              allowFullScreen
            />
          </div>
        </section>

        {/* Capabilities */}
        <section className="mt-10 rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
          <h2 className="text-2xl font-black text-slate-950">
            Que peut faire Runexa Study Agent ?
          </h2>

          <div className="mt-6 grid gap-3 sm:grid-cols-2">
            {[
              "Générer des résumés structurés et des explications détaillées",
              "Créer des quiz théoriques et pratiques",
              "Créer automatiquement des flashcards",
              "Générer des cartes d’apprentissage visuelles",
              "Fournir un support d’apprentissage audio",
              "Créer des plans de révision personnalisés",
              "Identifier les points faibles après les quiz",
            ].map((item) => (
              <div
                key={item}
                className="flex items-start gap-3 rounded-2xl border border-slate-100 bg-slate-50 px-4 py-3"
              >
                <span className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-green-100 text-sm font-black text-green-700">
                  ✓
                </span>

                <span className="text-sm font-medium leading-6 text-slate-700">
                  {item}
                </span>
              </div>
            ))}
          </div>
        </section>

        {/* CTA */}
        <section className="mt-10 rounded-[2rem] bg-slate-950 px-6 py-10 text-center text-white sm:px-10">
          <p className="text-lg font-semibold text-slate-200">
            Prêt à analyser vos propres supports d’étude ?
          </p>

          <Link
            href="/fr/study"
            className="mt-6 inline-flex rounded-2xl bg-blue-600 px-8 py-4 text-base font-black text-white transition hover:-translate-y-0.5 hover:bg-blue-500"
          >
            Essayer Runexa Study
          </Link>
        </section>
      </div>
    </main>
  );
}