import Image from "next/image";
import Link from "next/link";

export default function StudyAgentDemoFrPage() {
  return (
    <main className="min-h-screen bg-slate-50 px-6 py-16">
      <div className="mx-auto max-w-6xl">
        <h1 className="text-5xl font-bold tracking-tight text-slate-900">
          Démonstration de l’Agent d’Étude Runexa
        </h1>

        <p className="mt-6 max-w-3xl text-lg text-slate-600">
          Analysez vos cours, PDF et supports pédagogiques grâce à
          l’intelligence artificielle. Générez des résumés, quiz,
          flashcards et plans d’étude personnalisés.
        </p>

        <div className="mt-10">
          <Image
            src="/demo/study-agent-demo-fr.png"
            alt="Démonstration Agent d’Étude Runexa"
            width={1440}
            height={5000}
            sizes="(max-width: 768px) 100vw, (max-width: 1280px) 90vw, 1152px"
            className="h-auto w-full rounded-3xl border border-slate-200 shadow-lg"
          />
        </div>

        <div className="mt-10 text-center">
          <Link
            href="/fr/study"
            className="inline-flex rounded-xl bg-blue-600 px-6 py-3 font-semibold text-white transition hover:bg-blue-700"
          >
            Essayer l’Agent d’Étude
          </Link>
        </div>
      </div>
    </main>
  );
}