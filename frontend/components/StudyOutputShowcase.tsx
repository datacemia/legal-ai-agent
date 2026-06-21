"use client";

type Locale = "en" | "fr" | "ar";

type StudyOutputShowcaseProps = {
  locale?: Locale;
};

const copy = {
  en: {
    badge: "Real Runexa output",
    title: "From a 2-page lesson to a complete study workspace",
    subtitle:
      "A real Arabic geography lesson was transformed into a summary, visual map, quizzes, flashcards, and a 5-day revision plan in less than 2 minutes.",
    source: "Source document",
    sourceValue: "2-page Arabic geography lesson",
    time: "Processing time",
    timeValue: "< 2 minutes",
    output: "Generated output",
    outputValue: "Summary, quiz, flashcards, mind map, study plan",
    summaryTitle: "AI Summary",
    detailedTitle: "Detailed explanation",
    summary:
      "This university-level lesson discusses the concept of development, its evolution, and various approaches to studying it, including economic, social, demographic, political, environmental, and cultural perspectives.",
    detailed:
      "The lesson explains that development evolved from a focus on economic growth to a broader human-centered approach. It covers GDP, income per capita, literacy, health, democracy, sustainability, and country classification.",
    visualTitle: "Visual Summary",
    visualMain: "Concepts and Approaches to Development",
    visualItems: [
      "Definition of Development",
      "Economic Approach",
      "Social and Demographic Approaches",
      "Political and Environmental Approaches",
      "Country Classification",
      "Sustainable Development",
    ],
    quizTitle: "Exam-style questions",
    quizQuestion:
      "Which development approach best combines quality of life, healthcare, education, and sustainable use of resources?",
    quizOptions: [
      "Economic approach focusing on GDP growth",
      "Social approach emphasizing literacy and health indicators",
      "Environmental approach prioritizing sustainable resource management",
      "Integrated approach combining economic, social, and environmental indicators",
    ],
    correct: "Correct answer",
    flashcardsTitle: "Smart Flashcards",
    front: "Front",
    back: "Back",
    flashcards: [
      ["Economic Growth", "Increase in production and income in a country over time"],
      ["Human Development", "Improvement of individuals' living conditions and capabilities"],
      ["Gross Domestic Product (GDP)", "Total value of goods and services produced in a country"],
      ["Sustainable Development", "Development meeting present needs without harming future generations"],
    ],
    planTitle: "5-Day Study Plan",
    days: [
      ["Day 1", "Understand basic development concepts and approaches"],
      ["Day 2", "Analyze different development approaches and their indicators"],
      ["Day 3", "Apply classification of countries based on development indicators"],
      ["Day 4", "Evaluate the interconnection of development approaches"],
      ["Day 5", "Create a plan for sustainable development focused on human well-being"],
    ],
    cta: "View the result",
  },

  fr: {
    badge: "Résultat réel Runexa",
    title: "D’un cours de 2 pages à un espace d’étude complet",
    subtitle:
      "Un vrai cours de géographie en arabe a été transformé en résumé, carte visuelle, quiz, flashcards et plan de révision en moins de 2 minutes.",
    source: "Document source",
    sourceValue: "Cours de géographie arabe de 2 pages",
    time: "Temps de traitement",
    timeValue: "< 2 minutes",
    output: "Résultat généré",
    outputValue: "Résumé, quiz, flashcards, carte mentale, plan d’étude",
    summaryTitle: "Résumé IA",
    detailedTitle: "Explication détaillée",
    summary:
      "Ce cours universitaire présente le concept de développement, son évolution et les différentes approches utilisées pour l’étudier : économique, sociale, démographique, politique, environnementale et culturelle.",
    detailed:
      "Le cours montre que le développement est passé d’une vision centrée sur la croissance économique à une approche plus humaine. Il couvre le PIB, le revenu par habitant, l’alphabétisation, la santé, la démocratie, la durabilité et la classification des pays.",
    visualTitle: "Résumé visuel",
    visualMain: "Concepts et approches du développement",
    visualItems: [
      "Définition du développement",
      "Approche économique",
      "Approches sociale et démographique",
      "Approches politique et environnementale",
      "Classification des pays",
      "Développement durable",
    ],
    quizTitle: "Questions type examen",
    quizQuestion:
      "Quelle approche du développement combine le mieux qualité de vie, santé, éducation et utilisation durable des ressources ?",
    quizOptions: [
      "Approche économique centrée sur la croissance du PIB",
      "Approche sociale basée sur l’alphabétisation et la santé",
      "Approche environnementale centrée sur la gestion durable des ressources",
      "Approche intégrée combinant indicateurs économiques, sociaux et environnementaux",
    ],
    correct: "Bonne réponse",
    flashcardsTitle: "Flashcards intelligentes",
    front: "Recto",
    back: "Verso",
    flashcards: [
      ["Croissance économique", "Augmentation de la production et du revenu dans le temps"],
      ["Développement humain", "Amélioration des conditions de vie et des capacités des individus"],
      ["Produit intérieur brut (PIB)", "Valeur totale des biens et services produits dans un pays"],
      ["Développement durable", "Développement répondant aux besoins présents sans nuire aux générations futures"],
    ],
    planTitle: "Plan de révision sur 5 jours",
    days: [
      ["Jour 1", "Comprendre les concepts de base du développement"],
      ["Jour 2", "Analyser les différentes approches du développement"],
      ["Jour 3", "Appliquer les indicateurs de classification des pays"],
      ["Jour 4", "Évaluer l’interconnexion entre les approches"],
      ["Jour 5", "Créer une synthèse sur le développement durable"],
    ],
    cta: "Voir le résultat",
  },

  ar: {
    badge: "نتيجة حقيقية من Runexa",
    title: "من درس من صفحتين إلى مساحة دراسة كاملة",
    subtitle:
      "تم تحويل درس جغرافيا حقيقي باللغة العربية إلى ملخص وخريطة بصرية واختبارات وبطاقات مراجعة وخطة دراسة في أقل من دقيقتين.",
    source: "الملف الأصلي",
    sourceValue: "درس جغرافيا عربي من صفحتين",
    time: "وقت المعالجة",
    timeValue: "أقل من دقيقتين",
    output: "النتيجة المولدة",
    outputValue: "ملخص، اختبار، بطاقات مراجعة، خريطة ذهنية، خطة دراسة",
    summaryTitle: "ملخص بالذكاء الاصطناعي",
    detailedTitle: "شرح مفصل",
    summary:
      "يتناول هذا الدرس الجامعي مفهوم التنمية وتطوره والمقاربات المختلفة لدراسته، بما في ذلك المقاربة الاقتصادية والاجتماعية والديمغرافية والسياسية والبيئية والثقافية.",
    detailed:
      "يوضح الدرس أن مفهوم التنمية انتقل من التركيز على النمو الاقتصادي إلى مقاربة أوسع تتمحور حول الإنسان. ويغطي الناتج الداخلي الخام والدخل الفردي والتعليم والصحة والديمقراطية والاستدامة وتصنيف الدول.",
    visualTitle: "ملخص بصري",
    visualMain: "مفاهيم ومقاربات التنمية",
    visualItems: [
      "تعريف التنمية",
      "المقاربة الاقتصادية",
      "المقاربات الاجتماعية والديمغرافية",
      "المقاربات السياسية والبيئية",
      "تصنيف الدول",
      "التنمية المستدامة",
    ],
    quizTitle: "أسئلة بأسلوب الامتحان",
    quizQuestion:
      "أي مقاربة للتنمية تجمع بشكل أفضل بين جودة الحياة والصحة والتعليم والاستخدام المستدام للموارد؟",
    quizOptions: [
      "مقاربة اقتصادية تركز على نمو الناتج الداخلي الخام",
      "مقاربة اجتماعية تركز على محو الأمية والصحة",
      "مقاربة بيئية تعطي الأولوية لتدبير الموارد بشكل مستدام",
      "مقاربة متكاملة تجمع بين المؤشرات الاقتصادية والاجتماعية والبيئية",
    ],
    correct: "الإجابة الصحيحة",
    flashcardsTitle: "بطاقات مراجعة ذكية",
    front: "الوجه الأمامي",
    back: "الوجه الخلفي",
    flashcards: [
      ["النمو الاقتصادي", "زيادة الإنتاج والدخل في بلد معين مع مرور الوقت"],
      ["التنمية البشرية", "تحسين ظروف عيش الأفراد وقدراتهم"],
      ["الناتج الداخلي الخام", "القيمة الإجمالية للسلع والخدمات المنتجة داخل بلد معين"],
      ["التنمية المستدامة", "تنمية تلبي حاجات الحاضر دون الإضرار بالأجيال القادمة"],
    ],
    planTitle: "خطة دراسة لمدة 5 أيام",
    days: [
      ["اليوم 1", "فهم المفاهيم الأساسية للتنمية"],
      ["اليوم 2", "تحليل المقاربات المختلفة للتنمية"],
      ["اليوم 3", "تطبيق مؤشرات تصنيف الدول"],
      ["اليوم 4", "تقييم الترابط بين المقاربات"],
      ["اليوم 5", "إنشاء ملخص حول التنمية المستدامة"],
    ],
    cta: "عرض النتيجة",
  },
};

export default function StudyOutputShowcase({
  locale = "en",
}: StudyOutputShowcaseProps) {
  const t = copy[locale] || copy.en;
  const isRtl = locale === "ar";

  const resultHref =
    locale === "fr"
      ? "/fr/demo/study-agent"
      : locale === "ar"
      ? "/ar/demo/study-agent"
      : locale === "en"
      ? "/en/demo/study-agent"
      : "/demo/study-agent";

  return (
    <section
      id="study-real-result"
      dir={isRtl ? "rtl" : "ltr"}
      className="relative overflow-hidden rounded-[2rem] border border-slate-200 bg-white px-5 py-10 shadow-2xl shadow-slate-200/70 sm:px-8 lg:px-10"
    >
      <div className="pointer-events-none absolute -top-24 left-1/2 h-72 w-72 -translate-x-1/2 rounded-full bg-blue-200/30 blur-3xl" />

      <div className="relative mx-auto max-w-4xl text-center">
        <span className="inline-flex rounded-full border border-blue-200 bg-blue-50 px-4 py-2 text-sm font-semibold text-blue-700">
          {t.badge}
        </span>

        <h2 className="mt-5 break-words text-3xl font-bold tracking-tight text-slate-950 sm:text-4xl lg:text-5xl">
          {t.title}
        </h2>

        <p className="mx-auto mt-5 max-w-3xl break-words text-base leading-8 text-slate-600 sm:text-lg">
          {t.subtitle}
        </p>
      </div>

      <div className="relative mt-10 grid gap-4 md:grid-cols-3">
        {[
          [t.source, t.sourceValue],
          [t.time, t.timeValue],
          [t.output, t.outputValue],
        ].map(([label, value]) => (
          <div
            key={label}
            className="min-w-0 rounded-3xl border border-slate-200 bg-slate-50/80 p-5 text-center"
          >
            <p className="break-words text-sm font-semibold text-slate-500">{label}</p>
            <p className="mt-2 break-words text-lg font-bold text-slate-950">{value}</p>
          </div>
        ))}
      </div>

      <div className="relative mt-10 grid gap-6 lg:grid-cols-2">
        <article className="min-w-0 rounded-[1.75rem] border border-slate-200 bg-gradient-to-br from-white to-blue-50 p-6">
          <div className="flex items-center gap-3">
            <span className="flex h-10 w-10 items-center justify-center rounded-2xl bg-blue-600 text-white">
              ✦
            </span>
            <h3 className="break-words text-xl font-bold text-slate-950">
              {t.summaryTitle}
            </h3>
          </div>

          <p className="mt-5 break-words leading-8 text-slate-700">{t.summary}</p>

          <div className="mt-6 rounded-2xl border border-slate-200 bg-white p-5">
            <p className="text-sm font-bold uppercase tracking-wide text-blue-700">
              {t.detailedTitle}
            </p>
            <p className="mt-3 break-words leading-8 text-slate-700">{t.detailed}</p>
          </div>
        </article>

        <article className="min-w-0 rounded-[1.75rem] border border-slate-200 bg-white p-6">
          <div className="flex items-center gap-3">
            <span className="flex h-10 w-10 items-center justify-center rounded-2xl bg-indigo-600 text-white">
              ◎
            </span>
            <h3 className="break-words text-xl font-bold text-slate-950">
              {t.visualTitle}
            </h3>
          </div>

          <div className="mt-6 rounded-3xl border border-blue-200 bg-blue-600 px-5 py-5 text-center text-white shadow-lg shadow-blue-100">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-blue-100">
              {locale === "fr"
                ? "Sujet principal"
                : locale === "ar"
                ? "الموضوع الرئيسي"
                : "Main topic"}
            </p>
            <p className="mt-2 break-words text-sm font-bold leading-6 sm:text-base">{t.visualMain}</p>
          </div>

          <div className="mt-5 grid gap-3 sm:grid-cols-2">
            {t.visualItems.map((item, index) => (
              <div
                key={item}
                className="flex items-center gap-3 rounded-2xl border border-slate-200 bg-slate-50 p-4"
              >
                <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-blue-50 text-sm font-bold text-blue-700 ring-1 ring-blue-100">
                  {index + 1}
                </span>
                <span className="min-w-0 break-words text-sm font-medium leading-5 text-slate-800">{item}</span>
              </div>
            ))}
          </div>
        </article>

        <article className="min-w-0 rounded-[1.75rem] border border-slate-200 bg-white p-6">
          <div className="flex items-center gap-3">
            <span className="flex h-10 w-10 items-center justify-center rounded-2xl bg-emerald-600 text-white">
              ?
            </span>
            <h3 className="break-words text-xl font-bold text-slate-950">
              {t.quizTitle}
            </h3>
          </div>

          <div className="mt-6 rounded-3xl border border-slate-200 bg-slate-50 p-5">
            <p className="break-words font-bold leading-8 text-slate-950">
              {t.quizQuestion}
            </p>

            <div className="mt-5 space-y-3">
              {t.quizOptions.map((option, index) => {
                const isCorrect = index === 3;

                return (
                  <div
                    key={option}
                    className={`break-words rounded-2xl border px-4 py-3 text-sm font-medium ${
                      isCorrect
                        ? "border-emerald-200 bg-emerald-50 text-emerald-800"
                        : "border-slate-200 bg-white text-slate-700"
                    }`}
                  >
                    {isCorrect ? "✓ " : ""}
                    {option}
                  </div>
                );
              })}
            </div>

            <p className="mt-4 break-words text-sm font-semibold text-emerald-700">
              {t.correct}: {t.quizOptions[3]}
            </p>
          </div>
        </article>

        <article className="min-w-0 rounded-[1.75rem] border border-slate-200 bg-white p-6">
          <div className="flex items-center gap-3">
            <span className="flex h-10 w-10 items-center justify-center rounded-2xl bg-purple-600 text-white">
              ◫
            </span>
            <h3 className="break-words text-xl font-bold text-slate-950">
              {t.flashcardsTitle}
            </h3>
          </div>

          <div className="mt-6 grid gap-3">
            {t.flashcards.map(([front, back]) => (
              <div
                key={front}
                className="rounded-3xl border border-slate-200 bg-slate-50 p-4"
              >
                <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                  {t.front}
                </p>
                <p className="mt-1 break-words font-bold text-slate-950">{front}</p>
                <div className="my-3 h-px bg-slate-300" />
                <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                  {t.back}
                </p>
                <p className="mt-1 break-words leading-7 text-slate-700">{back}</p>
              </div>
            ))}
          </div>
        </article>
      </div>

      <div className="relative mt-6 rounded-[1.75rem] border border-slate-800 bg-slate-950 p-6 text-white">
        <h3 className="text-xl font-bold">{t.planTitle}</h3>

        <div className="mt-5 grid gap-3 md:grid-cols-5">
          {t.days.map(([day, task]) => (
            <div
              key={day}
              className="rounded-2xl border border-white/10 bg-white/5 p-4"
            >
              <p className="text-sm font-bold text-blue-200">{day}</p>
              <p className="mt-2 break-words text-sm leading-6 text-slate-200">{task}</p>
            </div>
          ))}
        </div>

        <a
          href={resultHref}
          className="mt-6 inline-flex max-w-full whitespace-normal break-words rounded-xl bg-white px-5 py-3 text-center text-sm font-semibold text-slate-950 transition hover:bg-blue-50"
        >
          {t.cta}
        </a>
      </div>
    </section>
  );
}
