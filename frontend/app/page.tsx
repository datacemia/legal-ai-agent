"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

const labels: any = {
  en: {
    platform: "Runexa AI Agents Platform",
    title: "AI agents that help you get work done faster.",
    desc: "Runexa provides AI agents that help you analyze documents, make smarter decisions, and move faster.",
    explore: "Explore agents",
    tryLegal: "Start Legal Trial",
    tryStudy: "Start Study Trial",
    tryFinance: "Start Finance Trial",
    tryBusiness: "Start Business Trial",
    trySecurity: "Preview Security Agent",
    choose: "Choose your AI agent",

    // ✅ UPDATED
    chooseDesc:
      "One Runexa account for all AI agents. Activate each agent with a one-time $1 trial, then continue with global credits or a plan.",

    available: "Available",
    coming: "Coming soon",
    open: "Open agent",
    pricing: "See pricing",
    securityBadge: "Agent 0 · Coming soon",
    securityTitle: "Runexa Home Security Agent",
    securitySubtitle: "An AI guardian for smart homes, cameras, sensors, GPS, and future drone surveillance.",
    securityDesc:
      "Agent 0 is designed to understand what is happening at home: unusual movement, unknown visitors, open doors, GPS presence, sensor alerts, and real-time risk levels — before turning events into clear actions.",
    securityPrimary: "Join the waitlist",
    securitySecondary: "View security concept",
    securitySystem: "Smart security command center",
    securityFooter: "Cameras + sensors + GPS + AI reasoning → safer homes",
    futureSystems: "Future AI Systems",
    exploreAgent0: "Explore Agent 0",
    securityFeatures: [
      "Camera intelligence",
      "Sensor fusion",
      "GPS geofencing",
      "Smart alerts",
      "Drone-ready module",
      "Privacy-first design",
    ],
    enterpriseBadge: "Custom AI Agents",
    enterpriseTitle: "Runexa for Business",
    enterpriseSubtitle: "Custom AI agents built for your company.",
    enterpriseDesc:
      "We design AI agents tailored to your workflows, data, and business needs — helping your teams analyze faster, reduce risks, and make better decisions.",
    enterprisePrimary: "Request a demo",
    enterpriseSecondary: "Explore business solutions",
    enterpriseCards: [
      "Legal workflows",
      "Finance reporting",
      "HR screening",
      "Business intelligence",
    ],
    enterpriseSystem: "Custom agent system",
    enterpriseWorkflow: "Custom AI workflow",
    enterpriseFooter: "Connected workflows → unified insights → faster decisions",
    enterpriseTag: "Enterprise",
    enterpriseHeader: "Runexa Business AI",
    ctaTitle: "One platform. Multiple AI agents. Real business outcomes.",
    ctaDesc:
      "Runexa Systems is an AI agents platform that helps you analyze documents, learn faster, manage personal finances, and make smarter business decisions.",
    ctaButton: "Create your account",
    disclaimer: "AI-powered insights. Always verify before you act.",
    agents: [
      [
        "Agent 0 · Home Security",
        "AI-powered home security with cameras, sensors, GPS geofencing, smart alerts, and future drone surveillance.",
      ],
      [
        "Legal Agent",
        "Analyze contracts, detect risky clauses, and get clear recommendations before you sign.",
      ],
      [
        "Study Agent",
        "Analyze study materials, generate summaries, quizzes, and smart revision plans.",
      ],
      [
        "Personal Finance Coach Agent",
        "Analyze your expenses, detect waste, and provide actionable saving strategies.",
      ],
      [
        "Business Decision Agent",
        "Analyze business data, detect trends, and support smarter strategic decisions.",
      ],
    ],
  },

  fr: {
    platform: "Plateforme d’agents IA Runexa",
    title: "Des agents IA pour travailler plus vite.",
    desc: "Runexa propose des agents IA qui vous aident à analyser vos documents, prendre de meilleures décisions et avancer plus vite.",
    explore: "Explorer les agents",
    tryLegal: "Activer l’essai juridique",
    tryStudy: "Activer l’essai étude",
    tryFinance: "Activer l’essai finance",
    tryBusiness: "Activer l’essai business",
    trySecurity: "Voir l’agent sécurité",
    choose: "Choisissez votre agent IA",

    // ✅ UPDATED
    chooseDesc:
      "Un seul compte Runexa pour tous les agents IA. Activez chaque agent avec un essai unique à 1$, puis continuez avec des crédits globaux ou un abonnement.",

    available: "Disponible",
    coming: "Bientôt",
    open: "Ouvrir l’agent",
    pricing: "Voir les tarifs",
    securityBadge: "Agent 0 · Bientôt",
    securityTitle: "Agent IA de sécurité domestique Runexa",
    securitySubtitle: "Un gardien IA pour maison intelligente, caméras, capteurs, GPS et future surveillance par drone.",
    securityDesc:
      "Agent 0 est conçu pour comprendre ce qui se passe à la maison : mouvements inhabituels, visiteurs inconnus, portes ouvertes, présence GPS, alertes capteurs et niveau de risque en temps réel — puis transformer ces événements en actions claires.",
    securityPrimary: "Rejoindre la liste d’attente",
    securitySecondary: "Voir le concept sécurité",
    securitySystem: "Centre de commande sécurité intelligent",
    securityFooter: "Caméras + capteurs + GPS + raisonnement IA → maisons plus sûres",
    futureSystems: "Systèmes IA du futur",
    exploreAgent0: "Explorer Agent 0",
    securityFeatures: [
      "Intelligence caméra",
      "Fusion de capteurs",
      "Géofencing GPS",
      "Alertes intelligentes",
      "Module prêt pour drone",
      "Confidentialité d’abord",
    ],
    enterpriseBadge: "Agents IA personnalisés",
    enterpriseTitle: "Runexa Systems pour les entreprises",
    enterpriseSubtitle:
      "Des agents IA personnalisés pour vos équipes, vos données et vos workflows.",
    enterpriseDesc:
      "Nous concevons des agents IA sur mesure pour aider les entreprises à automatiser l’analyse documentaire, le reporting financier, le recrutement, la conformité et la prise de décision.",
    enterprisePrimary: "Contacter l’équipe commerciale",
    enterpriseSecondary: "Découvrir Runexa pour les entreprises",
    enterpriseCards: [
      "Workflows juridiques",
      "Reporting financier",
      "Recrutement RH",
      "Intelligence business",
    ],
    enterpriseSystem: "Système d’agents personnalisés",
    enterpriseWorkflow: "Workflow IA personnalisé",
    enterpriseFooter: "Workflows connectés → vision unifiée → décisions plus rapides",
    enterpriseTag: "Entreprise",
    enterpriseHeader: "IA Business Runexa",
    ctaTitle: "Une plateforme. Plusieurs agents IA. Des résultats concrets.",
    ctaDesc:
      "Runexa Systems est une plateforme d’agents IA qui vous permet d’analyser vos documents, apprendre plus vite, gérer vos finances personnelles et prendre des décisions business plus intelligentes.",
    ctaButton: "Créer votre compte",
    disclaimer: "Analyses générées par IA. Vérifiez toujours avant d’agir.",
    agents: [
      [
        "Agent 0 · Sécurité domestique",
        "Sécurité domestique par IA avec caméras, capteurs, géofencing GPS, alertes intelligentes et future surveillance par drone.",
      ],
      [
        "Agent juridique",
        "Analysez vos contrats, détectez les clauses à risque et obtenez des recommandations claires.",
      ],
      [
        "Agent étude",
        "Analysez vos cours, générez des résumés, quiz et plans de révision intelligents.",
      ],
      [
        "Agent coach financier personnel",
        "Analysez vos dépenses, détectez le gaspillage et recevez des stratégies d’épargne concrètes.",
      ],
      [
        "Agent décision business",
        "Analysez vos données business, identifiez les tendances et prenez de meilleures décisions stratégiques.",
      ],
    ],
  },

  ar: {
    platform: "منصة Runexa للوكلاء الذكيين",
    title: "وكلاء ذكاء اصطناعي يساعدونك على إنجاز العمل بسرعة.",
    desc: "توفر Runexa وكلاء ذكاء اصطناعي يساعدونك على تحليل المستندات واتخاذ قرارات أفضل والعمل بشكل أسرع.",
    explore: "استكشاف الوكلاء",
    tryLegal: "تفعيل التجربة القانونية",
    tryStudy: "تفعيل تجربة الدراسة",
    tryFinance: "تفعيل تجربة المالية",
    tryBusiness: "تفعيل تجربة الأعمال",
    trySecurity: "معاينة وكيل الأمان",
    choose: "اختر وكيلك الذكي",

    // ✅ UPDATED
    chooseDesc:
      "حساب Runexa واحد لجميع الوكلاء. فعّل كل وكيل بتجربة واحدة بقيمة 1 دولار، ثم تابع باستخدام الأرصدة العامة أو الاشتراك.",

    available: "متاح",
    coming: "قريباً",
    open: "فتح الوكيل",
    pricing: "عرض الأسعار",
    securityBadge: "الوكيل 0 · قريباً",
    securityTitle: "وكيل Runexa لأمان المنزل",
    securitySubtitle: "حارس ذكي للمنازل الذكية والكاميرات والحساسات وGPS والمراقبة المستقبلية بالطائرات الصغيرة.",
    securityDesc:
      "تم تصميم الوكيل 0 لفهم ما يحدث في المنزل: حركة غير عادية، زوار غير معروفين، أبواب مفتوحة، وجود عبر GPS، تنبيهات الحساسات ومستوى الخطر في الوقت الحقيقي — ثم تحويل الأحداث إلى إجراءات واضحة.",
    securityPrimary: "الانضمام إلى قائمة الانتظار",
    securitySecondary: "عرض مفهوم الأمان",
    securitySystem: "مركز تحكم ذكي للأمان",
    securityFooter: "كاميرات + حساسات + GPS + تفكير ذكاء اصطناعي → منازل أكثر أماناً",
    futureSystems: "أنظمة الذكاء الاصطناعي المستقبلية",
    exploreAgent0: "استكشاف الوكيل 0",
    securityFeatures: [
      "ذكاء الكاميرا",
      "دمج الحساسات",
      "تحديد النطاق عبر GPS",
      "تنبيهات ذكية",
      "وحدة جاهزة للطائرة الصغيرة",
      "الخصوصية أولاً",
    ],
    enterpriseBadge: "وكلاء ذكاء اصطناعي مخصصون",
    enterpriseTitle: "Runexa للأعمال",
    enterpriseSubtitle:
      "وكلاء ذكاء اصطناعي مخصصون لفرقك وبياناتك وسير عملك.",
    enterpriseDesc:
      "نصمم وكلاء ذكاء اصطناعي مخصصين لمساعدة الشركات على أتمتة تحليل المستندات، التقارير المالية، التوظيف، الامتثال، واتخاذ القرار.",
    enterprisePrimary: "طلب عرض",
    enterpriseSecondary: "استكشاف حلول الأعمال",
    enterpriseCards: [
      "العمليات القانونية والامتثال",
      "التقارير والتحليل المالي",
      "التوظيف والموارد البشرية",
      "تحليل واتخاذ قرارات الأعمال",
    ],
    enterpriseSystem: "نظام وكلاء مخصص",
    enterpriseWorkflow: "سير عمل ذكي مخصص",
    enterpriseFooter: "ربط العمليات → رؤية موحدة → قرارات أسرع",
    enterpriseTag: "المؤسسات",
    enterpriseHeader: "Runexa Business AI",
    ctaTitle: "منصة واحدة. عدة وكلاء ذكاء اصطناعي. نتائج عملية.",
    ctaDesc:
      "Runexa Systems هي منصة وكلاء ذكاء اصطناعي تساعدك على تحليل المستندات، التعلم بشكل أسرع، إدارة أموالك الشخصية، واتخاذ قرارات أعمال أكثر ذكاءً.",
    ctaButton: "إنشاء حساب",
    disclaimer: "تحليلات مدعومة بالذكاء الاصطناعي. تحقق دائماً قبل اتخاذ أي قرار.",
    agents: [
      [
        "الوكيل 0 · أمان المنزل",
        "أمان منزلي مدعوم بالذكاء الاصطناعي مع كاميرات وحساسات وتحديد نطاق GPS وتنبيهات ذكية ومراقبة مستقبلية بالطائرات الصغيرة.",
      ],
      [
        "الوكيل القانوني",
        "حلل العقود، واكتشف البنود الخطرة، واحصل على توصيات واضحة.",
      ],
      [
        "وكيل الدراسة",
        "حلل المواد الدراسية، وأنشئ ملخصات واختبارات وخطط مراجعة ذكية.",
      ],
      [
        "وكيل الإدارة المالية الشخصية",
        "حلل مصاريفك، واكتشف الهدر، واحصل على استراتيجيات ادخار فعالة.",
      ],
      [
        "وكيل قرارات الأعمال",
        "حلل بيانات الأعمال، واكتشف الاتجاهات، واتخذ قرارات استراتيجية أفضل.",
      ],
    ],
  },
};

const agentLinks = ["/security", "/upload", "/study", "/finance", "/business"];

export default function HomePage() {
  const [language, setLanguage] = useState("en");
  const t = labels[language] || labels.en;

  useEffect(() => {
    const saved = localStorage.getItem("locale");
    if (saved && labels[saved]) {
      setLanguage(saved);
    }
  }, []);

  const handleLanguageChange = (lang: string) => {
    setLanguage(lang);
    localStorage.setItem("locale", lang);
    window.dispatchEvent(new Event("locale-change"));
  };

  return (
    <main
      dir={language === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-slate-50 text-slate-900"
    >
      <section className="px-6 py-20">
        <div className="max-w-6xl mx-auto text-center space-y-8">
          <div className="flex justify-center">
            <select
              value={language}
              onChange={(e) => handleLanguageChange(e.target.value)}
              className="border rounded-lg px-3 py-2 bg-white"
            >
              <option value="en">English</option>
              <option value="fr">Français</option>
              <option value="ar">العربية</option>
            </select>
          </div>

          <p className="text-blue-600 font-semibold">{t.platform}</p>
          <h1 className="text-5xl font-bold leading-tight">{t.title}</h1>
          <p className="text-lg text-slate-600 max-w-3xl mx-auto">
            {t.desc}
          </p>

          <div className="flex flex-wrap justify-center gap-4">
            <a
              href="#agents"
              className="px-6 py-3 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition"
            >
              {t.explore}
            </a>

            <a href="#agent-0" className="px-6 py-3 bg-slate-900 text-white rounded-xl font-semibold hover:bg-slate-800 transition">
              {t.trySecurity}
            </a>

            <Link href="/upload" className="px-6 py-3 bg-white border border-slate-200 rounded-xl font-semibold hover:bg-slate-100 transition">
              {t.tryLegal}
            </Link>

            <Link href="/study" className="px-6 py-3 bg-white border border-slate-200 rounded-xl font-semibold hover:bg-slate-100 transition">
              {t.tryStudy}
            </Link>

            <Link href="/finance" className="px-6 py-3 bg-green-600 text-white rounded-xl font-semibold hover:bg-green-700 transition">
              {t.tryFinance}
            </Link>

            <Link href="/business" className="px-6 py-3 bg-white border border-slate-200 rounded-xl font-semibold hover:bg-slate-100 transition">
              {t.tryBusiness}
            </Link>
          </div>
        </div>
      </section>


      <section id="agent-0" className="px-6 py-12">
        <div className="max-w-6xl mx-auto">
          <div className="relative overflow-hidden rounded-3xl border border-slate-200 bg-slate-950 text-white shadow-xl">
            <div className="absolute inset-0 bg-gradient-to-br from-blue-600/20 via-slate-950 to-emerald-500/10" />

            <div className="relative grid gap-10 p-8 md:p-12 lg:grid-cols-2 lg:items-center">
              <div>
                <span className="inline-flex rounded-full border border-white/10 bg-white/10 px-3 py-1 text-xs font-semibold text-blue-100">
                  {t.securityBadge}
                </span>

                <h2 className="mt-5 text-3xl md:text-4xl font-bold tracking-tight">
                  {t.securityTitle}
                </h2>

                <p className="mt-3 text-lg font-medium text-blue-100">
                  {t.securitySubtitle}
                </p>

                <p className="mt-4 text-slate-300 leading-7">
                  {t.securityDesc}
                </p>

                <div className="mt-6 flex flex-wrap gap-3">
                  <Link
                    href="/register"
                    className="rounded-xl bg-white px-5 py-3 text-sm font-semibold text-slate-950 hover:bg-slate-100 transition"
                  >
                    {t.securityPrimary}
                  </Link>

                  <Link
                    href="/labs/agent-0"
                    className="rounded-xl border border-white/10 bg-white/5 px-5 py-3 text-sm font-semibold text-white hover:bg-white/10 transition"
                  >
                    {t.securitySecondary}
                  </Link>
                </div>
              </div>

              <div className="rounded-3xl border border-white/10 bg-white/5 p-6 shadow-2xl backdrop-blur">
                <div className="flex items-center justify-between border-b border-white/10 pb-4">
                  <div>
                    <p className="text-sm text-slate-400">Runexa Agent 0</p>
                    <p className="text-lg font-semibold">{t.securitySystem}</p>
                  </div>

                  <span className="rounded-full bg-amber-400/10 px-3 py-1 text-xs font-medium text-amber-200">
                    {t.coming}
                  </span>
                </div>

                <div className="mt-6 grid grid-cols-2 gap-3">
                  {t.securityFeatures.map((item: string, index: number) => (
                    <div
                      key={index}
                      className="rounded-2xl border border-white/10 bg-slate-900/60 p-4"
                    >
                      <div className="h-2 w-2 rounded-full bg-emerald-400" />
                      <p className="mt-3 text-sm font-medium">{item}</p>
                    </div>
                  ))}
                </div>

                <div className="mt-6 rounded-2xl border border-emerald-400/20 bg-emerald-500/10 p-4 text-sm text-emerald-100">
                  {t.securityFooter}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="agents" className="px-6 py-12">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-10">
            <h2 className="text-3xl font-bold">{t.choose}</h2>
            <p className="mt-3 text-slate-600">{t.chooseDesc}</p>
            <p className="mt-2 text-sm text-slate-500">
              $1 trial per agent · Global credits · Pro and Premium plans for all agents
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-5 gap-6">
            {t.agents.map((agent: string[], index: number) => {
              const isAvailable = index >= 1;

              return (
                <div key={agent[0]} className="bg-white p-6 rounded-2xl border shadow-sm flex flex-col justify-between">
                  <div>
                    <div className="flex items-center justify-between gap-3">
                      <h3 className="text-xl font-bold">
                        {agent[0]}
                      </h3>
                      <span className="text-xs bg-slate-100 text-slate-600 px-3 py-1 rounded-full">
                        {isAvailable ? t.available : t.coming}
                      </span>
                    </div>

                    {isAvailable && (
                      <div className="mt-3 inline-flex w-fit rounded-full bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-700">
                        $1 Trial
                      </div>
                    )}

                    <p className="mt-4 text-slate-600">{agent[1]}</p>
                  </div>

                  {isAvailable ? (
                    <Link
                      href={agentLinks[index]}
                      className="inline-block mt-6 text-center px-4 py-2 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition"
                    >
                      {t.open}
                    </Link>
                  ) : (
                    <button
                      disabled
                      className="mt-6 px-4 py-2 bg-slate-100 text-slate-400 rounded-xl font-semibold"
                    >
                      {t.coming}
                    </button>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </section>

      <section className="px-6 py-16">
        <div className="max-w-6xl mx-auto">
          <div className="relative overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">
            <div className="absolute inset-0 bg-gradient-to-br from-blue-50 via-white to-slate-50" />

            <div className="relative grid gap-10 p-8 md:p-12 lg:grid-cols-2 lg:items-center">
              <div>
                <span className="inline-flex rounded-full border border-blue-100 bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-700">
                  {t.enterpriseBadge}
                </span>

                <h2 className="mt-5 text-3xl font-bold tracking-tight text-slate-900">
                  {t.enterpriseTitle}
                </h2>

                <p className="mt-3 text-lg font-medium text-slate-700">
                  {t.enterpriseSubtitle}
                </p>

                <p className="mt-4 text-slate-600 leading-7">
                  {t.enterpriseDesc}
                </p>

                <div className="mt-6 flex flex-wrap gap-3">
                  <Link
                    href="/contact-entreprise/contact"
                    className="rounded-xl bg-blue-600 px-5 py-3 text-sm font-semibold text-white hover:bg-blue-700 transition"
                  >
                    {t.enterprisePrimary}
                  </Link>

                  <Link
                    href="/enterprise"
                    className="rounded-xl border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-slate-900 hover:bg-slate-50 transition"
                  >
                    {t.enterpriseSecondary}
                  </Link>
                </div>
              </div>

              <div className="rounded-3xl border border-slate-200 bg-slate-950 p-6 text-white shadow-xl">
                <div className="flex items-center justify-between border-b border-white/10 pb-4">
                  <div>
                    <p className="text-sm text-slate-400">{t.enterpriseHeader}</p>
                    <p className="text-lg font-semibold">{t.enterpriseSystem}</p>
                  </div>

                  <span className="rounded-full bg-green-500/10 px-3 py-1 text-xs font-medium text-green-300">
                    {t.enterpriseTag}
                  </span>
                </div>

                <div className="mt-6 grid grid-cols-2 gap-3">
                  {t.enterpriseCards.map((item: string, index: number) => (
                    <div
                      key={index}
                      className="rounded-2xl border border-white/10 bg-white/5 p-4"
                    >
                      <div className="h-2 w-2 rounded-full bg-blue-400" />
                      <p className="mt-3 text-sm font-medium">{item}</p>
                      <p className="mt-2 text-xs text-slate-400">
                        {t.enterpriseWorkflow}
                      </p>
                    </div>
                  ))}
                </div>

                <div className="mt-6 rounded-2xl border border-blue-400/20 bg-blue-500/10 p-4 text-sm text-blue-100">
                  {t.enterpriseFooter}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="px-6 py-10">
        <div className="max-w-6xl mx-auto">
          <div className="relative overflow-hidden rounded-3xl border border-slate-200 bg-gradient-to-br from-slate-950 via-slate-900 to-blue-950 p-8 md:p-12 text-white shadow-2xl">
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(59,130,246,0.25),transparent_40%)]" />

            <div className="relative flex flex-col lg:flex-row lg:items-center lg:justify-between gap-8">
              <div className="max-w-3xl">
                <span className="inline-flex rounded-full border border-white/10 bg-white/10 px-3 py-1 text-xs font-semibold text-blue-100">
                  Runexa Labs
                </span>

                <h2 className="mt-5 text-3xl md:text-4xl font-bold tracking-tight">
                  {t.futureSystems}
                </h2>

                <p className="mt-4 text-slate-300 leading-7 text-lg">
                  Agent 0 represents the future vision of autonomous AI systems for real-world environments, security orchestration, sensor intelligence, and proactive decision-making.
                </p>

                <div className="mt-6 flex flex-wrap gap-3">
                  <Link
                    href="/labs/agent-0"
                    className="rounded-xl bg-white px-6 py-3 text-sm font-semibold text-slate-950 hover:bg-slate-100 transition"
                  >
                    {t.exploreAgent0}
                  </Link>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 min-w-[280px]">
                <div className="rounded-2xl border border-white/10 bg-white/5 p-5 backdrop-blur">
                  <div className="h-2 w-2 rounded-full bg-emerald-400" />
                  <p className="mt-4 text-sm font-semibold">
                    AI Security Layer
                  </p>
                </div>

                <div className="rounded-2xl border border-white/10 bg-white/5 p-5 backdrop-blur">
                  <div className="h-2 w-2 rounded-full bg-blue-400" />
                  <p className="mt-4 text-sm font-semibold">
                    Sensor Intelligence
                  </p>
                </div>

                <div className="rounded-2xl border border-white/10 bg-white/5 p-5 backdrop-blur">
                  <div className="h-2 w-2 rounded-full bg-violet-400" />
                  <p className="mt-4 text-sm font-semibold">
                    Autonomous Monitoring
                  </p>
                </div>

                <div className="rounded-2xl border border-white/10 bg-white/5 p-5 backdrop-blur">
                  <div className="h-2 w-2 rounded-full bg-amber-400" />
                  <p className="mt-4 text-sm font-semibold">
                    Future Drone Systems
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>


      <section className="px-6 py-16">
        <div className="max-w-5xl mx-auto bg-blue-600 text-white rounded-3xl p-10 text-center">
          <h2 className="text-3xl font-bold">{t.ctaTitle}</h2>
          <p className="mt-4 text-blue-100">{t.ctaDesc}</p>

          <Link href="/register" className="inline-block mt-6 px-6 py-3 bg-white text-blue-600 rounded-xl font-semibold">
            {t.ctaButton}
          </Link>

          <p className="mt-8 text-center text-sm text-slate-500 max-w-2xl mx-auto">
            {t.disclaimer}
          </p>
        </div>
      </section>
    </main>
  );
}