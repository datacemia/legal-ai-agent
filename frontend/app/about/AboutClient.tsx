"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import {
  defaultLocale,
  getSavedLocale,
} from "../../lib/i18n";

type Locale = "en" | "fr" | "ar";

const normalizeLocale = (
  value: string | null | undefined,
  fallback: Locale = "en"
): Locale => {
  if (value === "en" || value === "fr" || value === "ar") {
    return value;
  }

  return fallback;
};

const getDefaultLocale = (): Locale => {
  return normalizeLocale(defaultLocale, "en");
};

const aboutContent = {
  en: {
    badge: "About Runexa",
    title: "AI agents built from real-world problems.",
    subtitle:
      "Runexa was created to help people learn, understand complex information, and make better-informed decisions with specialized AI agents.",

    storyTitle: "The story behind Runexa",
    storyIntro:
      "I am Dr. Rachid Ejjami, founder of Runexa Systems. Runexa did not begin as a technology project. It began with real-world challenges I encountered in my daily life.",

    studyTitle: "Why the Study Agent exists",
    studyText:
      "As a parent, I watched my children study different subjects and constantly move between websites, videos, social networks, search engines, and AI tools to understand their lessons. Information was everywhere, but its reliability was often uncertain, and explanations were not always tailored to their learning needs. I wanted a better way to help learners understand their courses. That idea became the Runexa Study Agent.",

    legalTitle: "Why the Legal Agent exists",
    legalText:
      "From time to time, I needed to review contracts and agreements that contained legal language I did not fully understand. I could read the documents, but understanding obligations, risks, and important clauses often required significant effort. That experience inspired the Runexa Legal Agent, designed to help users identify important clauses, understand potential risks, and navigate legal documents more confidently before seeking professional advice when appropriate.",

    financeTitle: "Why the Finance Coach exists",
    financeText:
      "Personal finance presented another challenge. Like many people, I sometimes found it difficult to clearly understand spending patterns, recurring expenses, and financial habits. I wanted a tool that could help organize financial information, highlight trends, and provide educational insights to support better money management. That became the Runexa Finance Coach.",

    businessTitle: "Why the Business Decision Agent exists",
    businessText:
      "As an entrepreneur and business professional, I also needed better ways to analyze business information, track key performance indicators, evaluate opportunities, and support strategic decision-making. That need led to the creation of the Runexa Business Decision Agent.",

    missionTitle: "Our mission",
    missionText:
      "Runexa’s mission is to transform complex documents, data, and information into structured, understandable, and actionable analysis through specialized AI agents.",

    outputsTitle: "What Runexa agents produce",
    outputsText: "Runexa agents generate structured analysis from documents and data provided by users. Depending on the agent used, outputs may include identification of contractual clauses and legal risks, extraction of obligations and recommendations, spending analysis and savings opportunities, educational summaries and study plans, as well as performance indicators, forecasts, and business recommendations. Public demonstrations are available for each agent.",

    approachTitle: "Our approach to responsible AI",
    approachItems: [
      "AI should assist people, not replace human judgment.",
      "Important outputs should be reviewed by humans before being relied upon.",
      "Users should understand that AI may produce errors or incomplete information.",
      "Privacy, security, and transparency should be part of the product experience.",
    ],

    agentsTitle: "Runexa agents",
    agents: [
      {
        name: "Runexa Legal Agent",
        description:
          "Identify risky clauses and understand legal risks before signing contracts.",
        href: "/legal-ai",
      },
      {
        name: "Runexa Finance Coach",
        description:
          "Analyze spending, uncover savings opportunities, and improve financial decisions.",
        href: "/finance-ai",
      },
      {
        name: "Runexa Study Agent",
        description:
          "Learn more effectively with AI-generated summaries, quizzes, and study plans.",
        href: "/study-ai",
      },
      {
        name: "Runexa Business Decision Agent",
        description:
          "Gain actionable insights to make faster and better-informed business decisions.",
        href: "/business-ai",
      },
    ],

    trustTitle: "Trust and responsibility",
    trustText:
      "Runexa Systems LLC is committed to responsible AI use, user privacy, security best practices, and clear limitations around AI-generated outputs. Runexa AI agents are designed to support analysis and decision workflows, not to replace qualified professionals or human review.",

    founderTitle: "Founder",
    founderName: "Dr. Rachid Ejjami",
    founderRole: "Founder and Managing Member",
    founderCompany: "Runexa Systems LLC",
    founderBio:
      "Doctor of Business Administration (DBA), applied artificial intelligence researcher, and Editor-in-Chief of the Journal of Next-Generation Research (JNGR). Author of multiple books and publications on the application of artificial intelligence in healthcare, finance, insurance, energy, and supply chain management. His work focuses on the responsible use of AI for document analysis, decision support, and knowledge automation.",

    companyTitle: "Company information",
    companyName: "Runexa Systems LLC",
    companyAddress:
      "1309 Coffeen Avenue, Suite 1200\nSheridan, WY 82801\nUnited States",
    contact: "contact@runexa.ai",

    linksTitle: "Learn more",
    privacy: "Privacy Policy",
    security: "Security",
    aiDisclaimer: "AI Disclaimer",
    productTerms: "Product Terms",
  },

  fr: {
    badge: "À propos de Runexa",
    title: "Des agents IA créés à partir de problèmes réels.",
    subtitle:
      "Runexa a été créé pour aider les personnes à apprendre, comprendre des informations complexes et prendre de meilleures décisions grâce à des agents IA spécialisés.",

    storyTitle: "L’histoire derrière Runexa",
    storyIntro:
      "Je suis Dr. Rachid Ejjami, fondateur de Runexa Systems. Runexa n’a pas commencé comme un simple projet technologique. Il est né de défis réels rencontrés dans ma vie quotidienne.",

    studyTitle: "Pourquoi le Study Agent existe",
    studyText:
      "En tant que parent, j’ai vu mes enfants étudier différentes matières en passant constamment d’un site web à une vidéo, d’un réseau social à un moteur de recherche ou à différents outils d’IA pour comprendre leurs cours. L’information était partout, mais sa fiabilité était souvent incertaine, et les explications n’étaient pas toujours adaptées à leurs besoins d’apprentissage. Je voulais une meilleure solution pour aider les apprenants à comprendre leurs cours. Cette idée est devenue le Runexa Study Agent.",

    legalTitle: "Pourquoi le Legal Agent existe",
    legalText:
      "De temps en temps, je devais examiner des contrats et accords contenant un langage juridique que je ne comprenais pas toujours entièrement. Je pouvais lire les documents, mais comprendre les obligations, les risques et les clauses importantes demandait souvent beaucoup d’effort. Cette expérience a inspiré le Runexa Legal Agent, conçu pour aider les utilisateurs à identifier les clauses importantes, comprendre les risques potentiels et parcourir les documents juridiques avec plus de confiance avant de consulter un professionnel lorsque cela est approprié.",

    financeTitle: "Pourquoi le Finance Coach existe",
    financeText:
      "Les finances personnelles représentaient un autre défi. Comme beaucoup de personnes, il m’arrivait d’avoir du mal à comprendre clairement mes habitudes de dépenses, les charges récurrentes et mes comportements financiers. Je voulais un outil capable d’organiser les informations financières, de mettre en évidence les tendances et de fournir des insights éducatifs pour soutenir une meilleure gestion de l’argent. C’est devenu le Runexa Finance Coach.",

    businessTitle: "Pourquoi le Business Decision Agent existe",
    businessText:
      "En tant qu’entrepreneur et professionnel du business, j’avais également besoin de meilleures façons d’analyser les informations commerciales, suivre les indicateurs clés de performance, évaluer les opportunités et soutenir les décisions stratégiques. Ce besoin a conduit à la création du Runexa Business Decision Agent.",

    missionTitle: "Notre mission",
    missionText:
      "La mission de Runexa est de transformer des documents, données et informations complexes en analyses structurées, compréhensibles et exploitables grâce à des agents IA spécialisés.",

    outputsTitle: "Ce que les agents Runexa produisent",
    outputsText: "Les agents Runexa génèrent des analyses structurées à partir des documents et données fournis par les utilisateurs. Selon l’agent utilisé, les résultats peuvent inclure l’identification des clauses contractuelles et des risques juridiques, l’extraction d’obligations et de recommandations, l’analyse des dépenses et des opportunités d’économies, des résumés pédagogiques et plans d’étude, ainsi que des indicateurs de performance, prévisions et recommandations business. Des démonstrations publiques sont disponibles pour chaque agent.",

    approachTitle: "Notre approche de l’IA responsable",
    approachItems: [
      "L’IA doit assister les personnes, pas remplacer le jugement humain.",
      "Les résultats importants doivent être examinés par des humains avant d’être utilisés.",
      "Les utilisateurs doivent comprendre que l’IA peut produire des erreurs ou des informations incomplètes.",
      "La confidentialité, la sécurité et la transparence doivent faire partie de l’expérience produit.",
    ],

    agentsTitle: "Agents Runexa",
    agents: [
      {
        name: "Runexa Legal Agent",
        description:
          "Identifier les clauses à risque et mieux comprendre les risques juridiques avant de signer des contrats.",
        href: "/fr/legal-ai",
      },
      {
        name: "Runexa Finance Coach",
        description:
          "Analyser les dépenses, découvrir des opportunités d’économie et améliorer les décisions financières.",
        href: "/fr/finance-ai",
      },
      {
        name: "Runexa Study Agent",
        description:
          "Apprendre plus efficacement avec des résumés, quiz et plans d’étude générés par l’IA.",
        href: "/fr/study-ai",
      },
      {
        name: "Runexa Business Decision Agent",
        description:
          "Obtenir des insights exploitables pour prendre des décisions business plus rapides et mieux informées.",
        href: "/fr/business-ai",
      },
    ],

    trustTitle: "Confiance et responsabilité",
    trustText:
      "Runexa Systems LLC s’engage à promouvoir une utilisation responsable de l’IA, la confidentialité des utilisateurs, les bonnes pratiques de sécurité et des limitations claires concernant les résultats générés par l’IA. Les agents IA Runexa sont conçus pour soutenir l’analyse et les workflows de décision, et non pour remplacer les professionnels qualifiés ou la vérification humaine.",

    founderTitle: "Fondateur",
    founderName: "Dr. Rachid Ejjami",
    founderRole: "Fondateur et Managing Member",
    founderCompany: "Runexa Systems LLC",
    founderBio:
      "Docteur en administration des affaires (DBA), chercheur en intelligence artificielle appliquée et rédacteur en chef du Journal of Next-Generation Research (JNGR). Auteur de plusieurs ouvrages et publications consacrés aux applications de l’intelligence artificielle dans la santé, la finance, l’assurance, l’énergie et la supply chain. Ses travaux portent sur l’utilisation responsable de l’IA pour l’analyse documentaire, l’aide à la décision et l’automatisation des connaissances.",

    companyTitle: "Informations sur l’entreprise",
    companyName: "Runexa Systems LLC",
    companyAddress:
      "1309 Coffeen Avenue, Suite 1200\nSheridan, WY 82801\nÉtats-Unis",
    contact: "contact@runexa.ai",

    linksTitle: "En savoir plus",
    privacy: "Politique de confidentialité",
    security: "Sécurité",
    aiDisclaimer: "Avertissement IA",
    productTerms: "Conditions produit",
  },

  ar: {
    badge: "عن Runexa",
    title: "وكلاء ذكاء اصطناعي صُمموا لحل مشاكل واقعية.",
    subtitle:
      "تم إنشاء Runexa لمساعدة الناس على التعلم وفهم المعلومات المعقدة واتخاذ قرارات أفضل من خلال وكلاء ذكاء اصطناعي متخصصين.",

    storyTitle: "القصة وراء Runexa",
    storyIntro:
      "أنا الدكتور رشيد الجامعي، مؤسس شركة Runexa Systems. لم تبدأ Runexa كمجرد مشروع تقني، بل انطلقت من تحديات واقعية واجهتها في حياتي اليومية.",
    studyTitle: "لماذا يوجد Study Agent",
    studyText:
      "كأب، رأيت أطفالي يدرسون مواد مختلفة ويتنقلون باستمرار بين المواقع والفيديوهات والشبكات الاجتماعية ومحركات البحث وأدوات الذكاء الاصطناعي المختلفة لفهم دروسهم. كانت المعلومات متوفرة في كل مكان، لكن موثوقيتها كانت غالباً غير مؤكدة، كما أن الشروحات لم تكن دائماً مصممة بما يناسب احتياجاتهم التعليمية. أردت طريقة أفضل لمساعدة المتعلمين على فهم دروسهم. ومن هنا جاءت فكرة Runexa Study Agent.",

    legalTitle: "لماذا يوجد Legal Agent",
    legalText:
      "من وقت لآخر، كنت أحتاج إلى مراجعة عقود واتفاقيات تحتوي على لغة قانونية لا أفهمها دائماً بشكل كامل. كنت أستطيع قراءة المستندات، لكن فهم الالتزامات والمخاطر والبنود المهمة كان يتطلب جهداً كبيراً. هذه التجربة ألهمت إنشاء Runexa Legal Agent، المصمم لمساعدة المستخدمين على تحديد البنود المهمة، وفهم المخاطر المحتملة، والتعامل مع المستندات القانونية بثقة أكبر قبل طلب المشورة المهنية عند الحاجة.",

    financeTitle: "لماذا يوجد Finance Coach",
    financeText:
      "كانت إدارة المال الشخصي تحدياً آخر. مثل كثير من الناس، كنت أجد أحياناً صعوبة في فهم أنماط الإنفاق والمصاريف المتكررة والعادات المالية بوضوح. أردت أداة تساعد على تنظيم المعلومات المالية، وإظهار الاتجاهات، وتقديم رؤى تعليمية لدعم إدارة مالية أفضل. وهكذا أصبح Runexa Finance Coach.",

    businessTitle: "لماذا يوجد Business Decision Agent",
    businessText:
      "كرائد أعمال ومهني في مجال الأعمال، كنت أحتاج أيضاً إلى طرق أفضل لتحليل معلومات الأعمال، ومتابعة مؤشرات الأداء الرئيسية، وتقييم الفرص، ودعم القرارات الاستراتيجية. هذا الاحتياج أدى إلى إنشاء Runexa Business Decision Agent.",

    missionTitle: "مهمتنا",
    missionText:
      "تتمثل مهمة Runexa في تحويل المستندات والبيانات والمعلومات المعقدة إلى تحليلات منظمة وواضحة وقابلة للتنفيذ من خلال وكلاء ذكاء اصطناعي متخصصين.",

    outputsTitle: "ما الذي ينتجه وكلاء Runexa",
    outputsText: "ينتج وكلاء Runexa تحليلات منظمة انطلاقاً من المستندات والبيانات التي يقدمها المستخدمون. وقد تشمل النتائج تحديد البنود التعاقدية والمخاطر القانونية، واستخراج الالتزامات والتوصيات، وتحليل النفقات وفرص التوفير، والملخصات التعليمية وخطط الدراسة، بالإضافة إلى مؤشرات الأداء والتوقعات والتوصيات التجارية. تتوفر عروض توضيحية عامة لكل وكيل.",

    approachTitle: "نهجنا في الذكاء الاصطناعي المسؤول",
    approachItems: [
      "يجب أن يساعد الذكاء الاصطناعي الناس، لا أن يستبدل الحكم البشري.",
      "يجب أن تتم مراجعة النتائج المهمة من قبل البشر قبل الاعتماد عليها.",
      "يجب أن يفهم المستخدمون أن الذكاء الاصطناعي قد ينتج أخطاء أو معلومات غير مكتملة.",
      "يجب أن تكون الخصوصية والأمان والشفافية جزءاً من تجربة المنتج.",
    ],

    agentsTitle: "وكلاء Runexa",
    agents: [
      {
        name: "Runexa Legal Agent",
        description:
          "تحديد البنود الخطرة وفهم المخاطر القانونية قبل توقيع العقود.",
        href: "/ar/legal-ai",
      },
      {
        name: "Runexa Finance Coach",
        description:
          "تحليل الإنفاق واكتشاف فرص التوفير وتحسين القرارات المالية.",
        href: "/ar/finance-ai",
      },
      {
        name: "Runexa Study Agent",
        description:
          "التعلم بفعالية أكبر من خلال ملخصات واختبارات وخطط دراسة مولدة بالذكاء الاصطناعي.",
        href: "/ar/study-ai",
      },
      {
        name: "Runexa Business Decision Agent",
        description:
          "الحصول على رؤى قابلة للتنفيذ لاتخاذ قرارات أعمال أسرع وأكثر وعياً.",
        href: "/ar/business-ai",
      },
    ],

    trustTitle: "الثقة والمسؤولية",
    trustText:
      "تلتزم Runexa Systems LLC بالاستخدام المسؤول للذكاء الاصطناعي، وخصوصية المستخدم، وأفضل ممارسات الأمان، وتوضيح حدود المخرجات التي يولدها الذكاء الاصطناعي. صُممت وكلاء Runexa لدعم التحليل وسير عمل اتخاذ القرار، وليس لاستبدال المتخصصين المؤهلين أو المراجعة البشرية.",

    founderTitle: "المؤسس",
    founderName: "الدكتور رشيد الجامعي",
    founderRole: "المؤسس والعضو الإداري",
    founderCompany: "Runexa Systems LLC",
    founderBio:
      "الدكتور رشيد الجامعي حاصل على دكتوراه إدارة الأعمال (DBA)، وباحث في الذكاء الاصطناعي التطبيقي، ورئيس تحرير Journal of Next-Generation Research (JNGR). وهو مؤلف لعدة كتب ومنشورات حول تطبيقات الذكاء الاصطناعي في الصحة والتمويل والتأمين والطاقة وسلاسل الإمداد. تركز أعماله على الاستخدام المسؤول للذكاء الاصطناعي في تحليل المستندات ودعم القرار وأتمتة المعرفة.",

    companyTitle: "معلومات الشركة",
    companyName: "Runexa Systems LLC",
    companyAddress:
      "1309 Coffeen Avenue, Suite 1200\nSheridan, WY 82801\nUnited States",
    contact: "contact@runexa.ai",

    linksTitle: "اعرف المزيد",
    privacy: "سياسة الخصوصية",
    security: "الأمان",
    aiDisclaimer: "إخلاء مسؤولية الذكاء الاصطناعي",
    productTerms: "شروط المنتج",
  },
};

export default function AboutClient({
  initialLocale,
  lockInitialLocale = false,
}: {
  initialLocale?: Locale;
  lockInitialLocale?: boolean;
}) {
  const resolvedInitialLocale = initialLocale || getDefaultLocale();

  const [locale, setLocale] = useState<Locale>(resolvedInitialLocale);

  useEffect(() => {
    if (lockInitialLocale) {
      setLocale(resolvedInitialLocale);
      return;
    }

    setLocale(normalizeLocale(getSavedLocale(), resolvedInitialLocale));
  }, [resolvedInitialLocale, lockInitialLocale]);

  const t = aboutContent[locale] || aboutContent.en;

  return (
    <main
      dir={locale === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 px-6 py-20 text-slate-900"
    >
      <section className="mx-auto max-w-6xl">
        <p className="font-semibold text-blue-600">
          {t.badge}
        </p>

        <h1 className="mt-4 max-w-4xl text-5xl font-bold tracking-tight">
          {t.title}
        </h1>

        <p className="mt-6 max-w-3xl text-lg leading-8 text-slate-600">
          {t.subtitle}
        </p>
      </section>

      <section className="mx-auto mt-16 grid max-w-6xl gap-8 lg:grid-cols-[1.2fr_0.8fr]">
        <div className="rounded-3xl border bg-white p-8 shadow-sm">
          <h2 className="text-3xl font-bold">
            {t.storyTitle}
          </h2>

          <p className="mt-5 leading-8 text-slate-600">
            {t.storyIntro}
          </p>

          <div className="mt-8 space-y-8">
            <div>
              <h3 className="text-xl font-semibold">
                {t.studyTitle}
              </h3>

              <p className="mt-3 leading-8 text-slate-600">
                {t.studyText}
              </p>
            </div>

            <div>
              <h3 className="text-xl font-semibold">
                {t.legalTitle}
              </h3>

              <p className="mt-3 leading-8 text-slate-600">
                {t.legalText}
              </p>
            </div>

            <div>
              <h3 className="text-xl font-semibold">
                {t.financeTitle}
              </h3>

              <p className="mt-3 leading-8 text-slate-600">
                {t.financeText}
              </p>
            </div>

            <div>
              <h3 className="text-xl font-semibold">
                {t.businessTitle}
              </h3>

              <p className="mt-3 leading-8 text-slate-600">
                {t.businessText}
              </p>
            </div>
          </div>
        </div>

        <aside className="space-y-6">
          <div className="rounded-3xl border bg-white p-8 shadow-sm">
            <h2 className="text-2xl font-bold">
              {t.founderTitle}
            </h2>

            <p className="mt-4 text-lg font-semibold">
              {t.founderName}
            </p>

            <p className="mt-1 text-slate-600">
              {t.founderRole}
            </p>

            <p className="mt-1 text-slate-600">
              {t.founderCompany}
            </p>

            <p className="mt-4 text-sm leading-7 text-slate-600">
              {t.founderBio}
            </p>
          </div>

          <div className="rounded-3xl border bg-white p-8 shadow-sm">
            <h2 className="text-2xl font-bold">
              {t.companyTitle}
            </h2>

            <p className="mt-4 font-semibold">
              {t.companyName}
            </p>

            <p className="mt-3 whitespace-pre-line leading-7 text-slate-600">
              {t.companyAddress}
            </p>

            <p className="mt-3 text-slate-600">
              {t.contact}
            </p>
          </div>

          <div className="rounded-3xl border bg-white p-8 shadow-sm">
            <h2 className="text-2xl font-bold">
              {t.linksTitle}
            </h2>

            <div className="mt-4 space-y-3 text-sm font-medium text-blue-600">
              <Link href="/privacy" className="block hover:text-blue-800">
                {t.privacy}
              </Link>

              <Link href="/security" className="block hover:text-blue-800">
                {t.security}
              </Link>

              <Link href="/legal/ai-disclaimer" className="block hover:text-blue-800">
                {t.aiDisclaimer}
              </Link>

              <Link href="/products/ai-legal-agent/terms" className="block hover:text-blue-800">
                {t.productTerms}
              </Link>
            </div>
          </div>
        </aside>
      </section>

      <section className="mx-auto mt-16 grid max-w-6xl gap-8 lg:grid-cols-2">
        <div className="rounded-3xl border bg-white p-8 shadow-sm">
          <h2 className="text-3xl font-bold">
            {t.missionTitle}
          </h2>

          <p className="mt-4 leading-8 text-slate-600">
            {t.missionText}
          </p>
        </div>

        <div className="rounded-3xl border bg-white p-8 shadow-sm">
          <h2 className="text-3xl font-bold">
            {t.approachTitle}
          </h2>

          <ul className="mt-4 list-disc space-y-3 pl-5 text-slate-600">
            {t.approachItems.map((item) => (
              <li key={item}>
                {item}
              </li>
            ))}
          </ul>
        </div>
      </section>

      <section className="mx-auto mt-16 max-w-6xl rounded-3xl border bg-white p-8 shadow-sm">
        <h2 className="text-3xl font-bold">
          {t.outputsTitle}
        </h2>

        <p className="mt-4 leading-8 text-slate-600">
          {t.outputsText}
        </p>
      </section>

      <section className="mx-auto mt-16 max-w-6xl">
        <h2 className="text-3xl font-bold">
          {t.agentsTitle}
        </h2>

        <div className="mt-8 grid gap-6 md:grid-cols-2">
          {t.agents.map((agent) => (
            <Link
              key={agent.name}
              href={agent.href}
              className="rounded-3xl border bg-white p-8 shadow-sm transition hover:-translate-y-1 hover:shadow-md"
            >
              <h3 className="text-2xl font-bold">
                {agent.name}
              </h3>

              <p className="mt-4 leading-7 text-slate-600">
                {agent.description}
              </p>
            </Link>
          ))}
        </div>
      </section>

      <section className="mx-auto mt-16 max-w-6xl rounded-3xl bg-slate-950 p-10 text-white">
        <h2 className="text-3xl font-bold">
          {t.trustTitle}
        </h2>

        <p className="mt-4 max-w-4xl leading-8 text-slate-300">
          {t.trustText}
        </p>
      </section>
    </main>
  );
}
