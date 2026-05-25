"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import {
  Sparkles,
  ShieldCheck,
  Scale,
  GraduationCap,
  BarChart3,
  BriefcaseBusiness,
  Users,
  Lock,
  Zap,
  Globe,
} from "lucide-react";

const labels: any = {
  en: {
    platform: "Runexa AI Workspace",
    title: "Specialized AI agents for legal, finance, study, and business work.",
    desc: "Runexa helps individuals and professionals analyze documents, understand financial data, learn faster, and make smarter business decisions.",
    explore: "Explore AI Agents",
    pricing: "View Pricing",
    blog: "Insights",
    trustLine: "$1 trial per agent · Global credits · Secure AI workspace",
    tryLegal: "Runexa Legal Agent",
    tryFinance: "Runexa Finance Coach",
    tryStudy: "Runexa Study Agent",
    tryBusiness: "Runexa Business Decision Agent",
    choose: "Choose your AI agent",
    chooseDesc:
      "One Runexa account for specialized AI agents. Analyze legal documents, improve your finances, learn faster, and make smarter business decisions.",
    available: "Available",
    open: "Open agent",
    howTitle: "How Runexa works",
    howSteps: [
      "Upload your documents or data",
      "Runexa AI analyzes the content",
      "Receive actionable insights and recommendations",
    ],
    trustCards: [
      ["Secure & private", "Your data is protected"],
      ["Global credits", "Works across all agents"],
      ["Instant access", "Start using agents quickly"],
      ["Built for real work", "Individuals and professionals"],
    ],
    enterpriseBadge: "Custom AI Systems",
    enterpriseTitle: "Runexa for Organizations",
    enterpriseSubtitle: "Custom AI systems for teams and companies.",
    enterpriseDesc:
      "Runexa helps organizations automate document analysis, financial reporting, learning workflows, and strategic decision-making.",
    enterprisePrimary: "Request a demo",
    enterpriseSecondary: "Explore business solutions",
    enterpriseCards: [
      "Team workspace",
      "Organization dashboard",
      "Multi-user access",
      "Custom credits",
      "Priority support",
    ],
    enterpriseSystem: "Custom AI system",
    enterpriseWorkflow: "AI workflow",
    enterpriseFooter: "Connected workflows → unified insights → faster decisions",
    enterpriseTag: "Enterprise",
    enterpriseHeader: "Runexa Business AI",
    ctaTitle: "One platform. Multiple AI agents. Real-world results.",
    ctaDesc:
      "Runexa Systems is an AI workspace platform for legal, finance, study, and business productivity.",
    ctaButton: "Create your account",
    disclaimer: "AI-powered insights. Always verify before you act.",
    seoTitle: "Enterprise AI Workspace",
    seoHeading:
      "AI agents for document analysis, finance, study, and business intelligence",
    seoDesc:
      "Runexa Systems provides specialized AI agents for AI document analysis, AI contract review, financial analysis, study assistance, business intelligence, and enterprise AI workflow automation.",
    seoItems: [
      "AI document analysis",
      "AI contract review",
      "AI financial analysis",
      "AI study assistant",
      "AI business intelligence",
      "Enterprise AI workflows",
    ],
    faqTitle: "FAQ",
    faqHeading: "Frequently asked questions",
    faqItems: [
      [
        "What is an AI agent?",
        "An AI agent is a specialized AI system designed to complete a specific workflow, such as contract review, financial analysis, study planning, or business intelligence.",
      ],
      [
        "How does Runexa work?",
        "Upload a document or business file, choose the AI agent, and receive structured insights, summaries, risks, recommendations, and reports.",
      ],
      [
        "Is Runexa secure?",
        "Runexa is designed as a secure AI workspace for private document analysis and professional workflows.",
      ],
      [
        "Can businesses use Runexa?",
        "Yes. Runexa supports enterprise AI workflows, team workspaces, organization dashboards, custom credits, and business intelligence use cases.",
      ],
      [
        "What can Runexa analyze?",
        "Runexa can analyze legal documents, bank statements, study materials, and structured business data depending on the selected AI agent.",
      ],
      [
        "Does Runexa replace professionals?",
        "No. Runexa provides informational and decision-support output. Important decisions should be verified with qualified professionals.",
      ],
    ],
    agents: [
      [
        "Runexa Legal Agent",
        "Detect risky clauses before signing contracts.",
        "/legal-ai",
        "legal",
      ],
      [
        "Runexa Finance Coach",
        "Understand where your money goes and improve your financial habits.",
        "/finance-ai",
        "finance",
      ],
      [
        "Runexa Study Agent",
        "Learn faster with AI-generated summaries and revision plans.",
        "/study-ai",
        "study",
      ],
      [
        "Runexa Business Decision Agent",
        "Get AI support for smarter strategic decisions.",
        "/business-ai",
        "business",
      ],
    ],
  },

  fr: {
    platform: "Espace IA Runexa",
    title: "Des agents IA spécialisés pour le juridique, la finance, les études et le business.",
    desc: "Runexa aide les particuliers et les professionnels à analyser des documents, comprendre leurs finances, apprendre plus vite et prendre de meilleures décisions business.",
    explore: "Explorer les agents IA",
    pricing: "Voir les tarifs",
    blog: "Insights",
    trustLine: "Essai à 1 $ par agent · Crédits globaux · Espace IA sécurisé",
    tryLegal: "Runexa Legal Agent",
    tryFinance: "Runexa Finance Coach",
    tryStudy: "Runexa Study Agent",
    tryBusiness: "Runexa Business Decision Agent",
    choose: "Choisissez votre agent IA",
    chooseDesc:
      "Un seul compte Runexa pour des agents IA spécialisés. Analysez vos documents juridiques, améliorez vos finances, apprenez plus vite et prenez de meilleures décisions business.",
    available: "Disponible",
    open: "Ouvrir l’agent",
    howTitle: "Comment fonctionne Runexa",
    howSteps: [
      "Téléchargez vos documents ou données",
      "L’IA Runexa analyse le contenu",
      "Recevez des recommandations exploitables",
    ],
    trustCards: [
      ["Sécurisé et confidentiel", "Vos données sont protégées"],
      ["Crédits globaux", "Utilisables sur tous les agents"],
      ["Accès instantané", "Commencez rapidement"],
      ["Conçu pour le travail réel", "Particuliers et professionnels"],
    ],
    enterpriseBadge: "Systèmes IA personnalisés",
    enterpriseTitle: "Runexa pour les organisations",
    enterpriseSubtitle: "Des systèmes IA personnalisés pour les équipes et les entreprises.",
    enterpriseDesc:
      "Runexa aide les organisations à automatiser l’analyse documentaire, le reporting financier, les workflows d’apprentissage et la prise de décision stratégique.",
    enterprisePrimary: "Contacter l’équipe commerciale",
    enterpriseSecondary: "Découvrir Runexa pour les entreprises",
    enterpriseCards: [
      "Espace équipe",
      "Tableau de bord organisation",
      "Accès multi-utilisateurs",
      "Crédits personnalisés",
      "Support prioritaire",
    ],
    enterpriseSystem: "Système IA personnalisé",
    enterpriseWorkflow: "Workflow IA",
    enterpriseFooter: "Workflows connectés → vision unifiée → décisions plus rapides",
    enterpriseTag: "Entreprise",
    enterpriseHeader: "IA Business Runexa",
    ctaTitle: "Une plateforme. Plusieurs agents IA. Des résultats concrets.",
    ctaDesc:
      "Runexa Systems est un espace IA pour le juridique, la finance, les études et la productivité business.",
    ctaButton: "Créer votre compte",
    disclaimer: "Analyses générées par IA. Vérifiez toujours avant d’agir.",
    seoTitle: "Espace IA entreprise",
    seoHeading:
      "Agents IA pour l’analyse documentaire, la finance, les études et la business intelligence",
    seoDesc:
      "Runexa Systems propose des agents IA spécialisés pour l’analyse de documents, l’analyse de contrats, l’analyse financière, l’assistance aux études, la business intelligence et l’automatisation des workflows IA en entreprise.",
    seoItems: [
      "Analyse documentaire IA",
      "Analyse de contrats IA",
      "Analyse financière IA",
      "Assistant d’étude IA",
      "Business intelligence IA",
      "Workflows IA entreprise",
    ],
    faqTitle: "FAQ",
    faqHeading: "Questions fréquentes",
    faqItems: [
      [
        "Qu’est-ce qu’un agent IA ?",
        "Un agent IA est un système spécialisé conçu pour réaliser un workflow précis, comme l’analyse de contrats, l’analyse financière, la planification d’étude ou la business intelligence.",
      ],
      [
        "Comment fonctionne Runexa ?",
        "Importez un document ou un fichier business, choisissez l’agent IA, puis recevez des insights structurés, résumés, risques, recommandations et rapports.",
      ],
      [
        "Runexa est-il sécurisé ?",
        "Runexa est conçu comme un espace IA sécurisé pour l’analyse privée de documents et les workflows professionnels.",
      ],
      [
        "Les entreprises peuvent-elles utiliser Runexa ?",
        "Oui. Runexa prend en charge les workflows IA entreprise, les espaces équipe, les dashboards organisation, les crédits personnalisés et la business intelligence.",
      ],
      [
        "Que peut analyser Runexa ?",
        "Runexa peut analyser des documents juridiques, des relevés bancaires, des supports d’étude et des données business structurées selon l’agent choisi.",
      ],
      [
        "Runexa remplace-t-il les professionnels ?",
        "Non. Runexa fournit une aide informative et décisionnelle. Les décisions importantes doivent être vérifiées avec des professionnels qualifiés.",
      ],
    ],
    agents: [
      [
        "Runexa Legal Agent",
        "Détectez les clauses à risque avant de signer vos contrats.",
        "/legal-ai",
        "legal",
      ],
      [
        "Runexa Finance Coach",
        "Comprenez où va votre argent et améliorez vos habitudes financières.",
        "/finance-ai",
        "finance",
      ],
      [
        "Runexa Study Agent",
        "Apprenez plus vite grâce aux résumés IA et aux plans de révision intelligents.",
        "/study-ai",
        "study",
      ],
      [
        "Runexa Business Decision Agent",
        "Obtenez une assistance IA pour prendre de meilleures décisions stratégiques.",
        "/business-ai",
        "business",
      ],
    ],
  },

  ar: {
    platform: "مساحة Runexa للذكاء الاصطناعي",
    title: "وكلاء ذكاء اصطناعي متخصصون في القانون والمالية والدراسة والأعمال.",
    desc: "تساعد Runexa الأفراد والمحترفين على تحليل المستندات وفهم البيانات المالية والتعلم بشكل أسرع واتخاذ قرارات أعمال أكثر ذكاءً.",
    explore: "استكشاف وكلاء الذكاء الاصطناعي",
    pricing: "عرض الأسعار",
    blog: "الرؤى",
    trustLine: "تجربة مقابل 1 دولار لكل وكيل · أرصدة موحدة · مساحة ذكاء اصطناعي آمنة",
    tryLegal: "Runexa Legal Agent",
    tryFinance: "Runexa Finance Coach",
    tryStudy: "Runexa Study Agent",
    tryBusiness: "Runexa Business Decision Agent",
    choose: "اختر وكيلك الذكي",
    chooseDesc:
      "حساب Runexa واحد لوكلاء ذكاء اصطناعي متخصصين. حلل المستندات القانونية، افهم أموالك، تعلّم أسرع، واتخذ قرارات أعمال أفضل.",
    available: "متاح",
    open: "فتح الوكيل",
    howTitle: "كيف تعمل Runexa",
    howSteps: [
      "قم برفع مستنداتك أو بياناتك",
      "يقوم ذكاء Runexa بتحليل المحتوى",
      "احصل على توصيات ورؤى قابلة للتنفيذ",
    ],
    trustCards: [
      ["آمن وخاص", "بياناتك محمية"],
      ["أرصدة موحدة", "صالحة لكل الوكلاء"],
      ["وصول فوري", "ابدأ بسرعة"],
      ["مصمم للعمل الواقعي", "للأفراد والمحترفين"],
    ],
    enterpriseBadge: "أنظمة ذكاء اصطناعي مخصصة",
    enterpriseTitle: "Runexa للمؤسسات",
    enterpriseSubtitle: "أنظمة ذكاء اصطناعي مخصصة للفرق والشركات.",
    enterpriseDesc:
      "تساعد Runexa المؤسسات على أتمتة تحليل المستندات والتقارير المالية وعمليات التعلم واتخاذ القرارات الاستراتيجية.",
    enterprisePrimary: "طلب عرض",
    enterpriseSecondary: "استكشاف حلول الأعمال",
    enterpriseCards: [
      "مساحة عمل الفريق",
      "لوحة تحكم المؤسسة",
      "وصول متعدد المستخدمين",
      "أرصدة مخصصة",
      "دعم ذو أولوية",
    ],
    enterpriseSystem: "نظام ذكاء اصطناعي مخصص",
    enterpriseWorkflow: "سير عمل ذكي",
    enterpriseFooter: "ربط العمليات → رؤية موحدة → قرارات أسرع",
    enterpriseTag: "المؤسسات",
    enterpriseHeader: "Runexa Business AI",
    ctaTitle: "منصة واحدة. عدة وكلاء ذكاء اصطناعي. نتائج واقعية.",
    ctaDesc:
      "Runexa Systems هي مساحة ذكاء اصطناعي للقانون والمالية والدراسة وإنتاجية الأعمال.",
    ctaButton: "إنشاء حساب",
    disclaimer: "تحليلات مدعومة بالذكاء الاصطناعي. تحقق دائماً قبل اتخاذ أي قرار.",
    seoTitle: "مساحة ذكاء اصطناعي للمؤسسات",
    seoHeading:
      "وكلاء ذكاء اصطناعي لتحليل المستندات والمالية والدراسة وذكاء الأعمال",
    seoDesc:
      "تقدم Runexa Systems وكلاء ذكاء اصطناعي متخصصين لتحليل المستندات، مراجعة العقود، التحليل المالي، المساعدة في الدراسة، ذكاء الأعمال، وأتمتة سير العمل بالذكاء الاصطناعي داخل المؤسسات.",
    seoItems: [
      "تحليل المستندات بالذكاء الاصطناعي",
      "مراجعة العقود بالذكاء الاصطناعي",
      "التحليل المالي بالذكاء الاصطناعي",
      "مساعد دراسة ذكي",
      "ذكاء الأعمال بالذكاء الاصطناعي",
      "سير عمل ذكي للمؤسسات",
    ],
    faqTitle: "الأسئلة الشائعة",
    faqHeading: "أسئلة متكررة",
    faqItems: [
      [
        "ما هو وكيل الذكاء الاصطناعي؟",
        "وكيل الذكاء الاصطناعي هو نظام متخصص مصمم لتنفيذ مهمة محددة مثل مراجعة العقود، التحليل المالي، تخطيط الدراسة أو ذكاء الأعمال.",
      ],
      [
        "كيف تعمل Runexa؟",
        "ارفع مستنداً أو ملف بيانات، اختر الوكيل الذكي، ثم احصل على رؤى منظمة وملخصات ومخاطر وتوصيات وتقارير.",
      ],
      [
        "هل Runexa آمنة؟",
        "تم تصميم Runexa كمساحة ذكاء اصطناعي آمنة لتحليل المستندات الخاصة وسير العمل المهني.",
      ],
      [
        "هل يمكن للشركات استخدام Runexa؟",
        "نعم. تدعم Runexa سير العمل الذكي للمؤسسات، مساحات الفرق، لوحات تحكم المؤسسات، الأرصدة المخصصة وذكاء الأعمال.",
      ],
      [
        "ما الذي يمكن لـ Runexa تحليله؟",
        "يمكن لـ Runexa تحليل المستندات القانونية، كشوفات الحساب البنكية، مواد الدراسة والبيانات business المنظمة حسب الوكيل المختار.",
      ],
      [
        "هل تعوض Runexa الخبراء؟",
        "لا. تقدم Runexa مخرجات معلوماتية وداعمة للقرار. يجب التحقق من القرارات المهمة مع مختصين مؤهلين.",
      ],
    ],
    agents: [
      [
        "Runexa Legal Agent",
        "اكتشف البنود الخطرة قبل توقيع العقود.",
        "/legal-ai",
        "legal",
      ],
      [
        "Runexa Finance Coach",
        "افهم أين تذهب أموالك وحسّن عاداتك المالية.",
        "/finance-ai",
        "finance",
      ],
      [
        "Runexa Study Agent",
        "تعلّم بشكل أسرع باستخدام الملخصات وخطط المراجعة المدعومة بالذكاء الاصطناعي.",
        "/study-ai",
        "study",
      ],
      [
        "Runexa Business Decision Agent",
        "احصل على دعم بالذكاء الاصطناعي لاتخاذ قرارات استراتيجية أكثر ذكاءً.",
        "/business-ai",
        "business",
      ],
    ],
  },
};

const agentStyles: any = {
  legal: {
    icon: Scale,
    card: "border-slate-200 bg-white hover:shadow-blue-100",
    iconBox: "bg-blue-50",
    iconColor: "text-blue-700",
    arrow: "text-blue-600",
    badge: "bg-blue-50 text-blue-700",
  },
  finance: {
    icon: BarChart3,
    card: "bg-gradient-to-br from-emerald-500 to-green-600 text-white hover:shadow-emerald-200",
    iconBox: "bg-white/15 backdrop-blur",
    iconColor: "text-white",
    arrow: "text-white",
    badge: "bg-white/10 text-emerald-50",
  },
  study: {
    icon: GraduationCap,
    card: "border-slate-200 bg-white hover:shadow-violet-100",
    iconBox: "bg-violet-50",
    iconColor: "text-violet-700",
    arrow: "text-violet-600",
    badge: "bg-violet-50 text-violet-700",
  },
  business: {
    icon: BriefcaseBusiness,
    card: "border-slate-200 bg-white hover:shadow-orange-100",
    iconBox: "bg-orange-50",
    iconColor: "text-orange-700",
    arrow: "text-orange-600",
    badge: "bg-orange-50 text-orange-700",
  },
};

export default function HomeClient() {
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

          <div className="flex flex-col sm:flex-row justify-center gap-3">
            <a
              href="#agents"
              className="inline-flex items-center justify-center rounded-xl bg-blue-600 px-6 py-3 text-sm font-semibold text-white hover:bg-blue-700 transition"
            >
              {t.explore}
            </a>

            <Link
              href="/pricing"
              className="inline-flex items-center justify-center rounded-xl border border-slate-200 bg-white px-6 py-3 text-sm font-semibold text-slate-900 hover:bg-slate-50 transition"
            >
              {t.pricing}
            </Link>

            <Link
              href="/blog"
              className="inline-flex items-center justify-center rounded-xl border border-slate-200 bg-white px-6 py-3 text-sm font-semibold text-slate-900 hover:bg-slate-50 transition"
            >
              {t.blog}
            </Link>
          </div>

          <p className="text-sm text-slate-500">{t.trustLine}</p>

          <div className="relative mt-10">
            <div className="absolute inset-0 bg-gradient-to-r from-blue-100/40 via-transparent to-emerald-100/30 blur-3xl" />

            <div className="relative rounded-[32px] border border-slate-200/80 bg-white/80 p-6 shadow-[0_20px_80px_rgba(15,23,42,0.08)] backdrop-blur-xl md:p-10">
              <div className="mb-8 flex justify-center">
                <div className="inline-flex items-center gap-2 rounded-full border border-blue-200 bg-blue-50 px-5 py-2 text-sm font-semibold text-blue-700">
                  <span><Users className="h-4 w-4" /></span>
                  <span>
                    {language === "fr"
                      ? "Pour particuliers & professionnels"
                      : language === "ar"
                      ? "للأفراد والمحترفين"
                      : "For individuals & professionals"}
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-5">
                <a
                  href="#agents"
                  className="group relative overflow-hidden rounded-3xl bg-gradient-to-br from-blue-600 to-blue-700 p-4 xl:p-5 text-white shadow-xl transition duration-300 hover:-translate-y-1 hover:shadow-blue-200"
                >
                  <div className="absolute inset-0 bg-white/5 opacity-0 transition group-hover:opacity-100" />

                  <div className="relative flex items-start justify-between">
                    <div className="space-y-2 text-left">
                      <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-white/15 text-2xl backdrop-blur">
                        <Sparkles className="h-6 w-6" />
                      </div>

                      <div>
                        <h3 className="text-base font-bold">{t.explore}</h3>

                        <p className="mt-1 text-sm text-blue-100">
                          {language === "fr"
                            ? "Agents spécialisés"
                            : language === "ar"
                            ? "وكلاء متخصصون"
                            : "Specialized agents"}
                        </p>
                      </div>
                    </div>

                    <span className="text-2xl transition group-hover:translate-x-1">
                      →
                    </span>
                  </div>

                  <div className="mt-5 inline-flex rounded-full bg-white/10 px-3 py-1 text-xs font-medium text-blue-100">
                    {language === "fr"
                      ? "Espace IA"
                      : language === "ar"
                      ? "مساحة ذكاء اصطناعي"
                      : "AI workspace"}
                  </div>
                </a>

                {t.agents.map((agent: string[]) => {
                  const style = agentStyles[agent[3]];
                  const Icon = style.icon;
                  const isDark = agent[3] === "finance";

                  return (
                    <Link
                      key={agent[0]}
                      href={agent[2]}
                      className={`group relative overflow-hidden rounded-3xl p-4 shadow-lg transition duration-300 hover:-translate-y-1 ${style.card}`}
                    >
                      {isDark && (
                        <div className="absolute inset-0 bg-white/5 opacity-0 transition group-hover:opacity-100" />
                      )}

                      <div className="relative flex items-start justify-between">
                        <div className="space-y-2 text-left">
                          <div className={`flex h-12 w-12 items-center justify-center rounded-2xl text-2xl ${style.iconBox}`}>
                            <Icon className={`h-6 w-6 ${style.iconColor}`} />
                          </div>

                          <div>
                            <h3 className={`text-base font-bold ${isDark ? "text-white" : "text-slate-900"}`}>
                              {agent[0]}
                            </h3>

                            <p className={`mt-1 text-sm ${isDark ? "text-emerald-100" : "text-slate-500"}`}>
                              {agent[1]}
                            </p>
                          </div>
                        </div>

                        <span className={`text-2xl transition group-hover:translate-x-1 ${style.arrow}`}>
                          →
                        </span>
                      </div>

                      <div className={`mt-5 inline-flex rounded-full px-3 py-1 text-xs font-medium ${style.badge}`}>
                        {t.available}
                      </div>
                    </Link>
                  );
                })}
              </div>

              <div className="mt-8 grid grid-cols-1 gap-4 border-t border-slate-200 pt-6 md:grid-cols-2 lg:grid-cols-4">
                {t.trustCards.map((card: string[], index: number) => {
                  const icons = [Lock, Globe, Zap, ShieldCheck];
                  const colors = [
                    "bg-violet-50 text-violet-700",
                    "bg-blue-50 text-blue-700",
                    "bg-emerald-50 text-emerald-700",
                    "bg-blue-50 text-blue-700",
                  ];
                  const Icon = icons[index];

                  return (
                    <div key={card[0]} className="flex items-center gap-3 text-left">
                      <div className={`flex h-12 w-12 items-center justify-center rounded-2xl text-xl ${colors[index]}`}>
                        <Icon className="h-6 w-6" />
                      </div>

                      <div>
                        <p className="font-semibold text-slate-900">
                          {card[0]}
                        </p>

                        <p className="text-sm text-slate-500">
                          {card[1]}
                        </p>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>

      </section>

      <section className="px-6 pb-8">
        <div className="max-w-6xl mx-auto">
          <div className="relative overflow-hidden rounded-[32px] border border-slate-200 bg-white shadow-[0_20px_80px_rgba(15,23,42,0.08)]">
            <div className="absolute inset-0 bg-gradient-to-br from-blue-50 via-white to-emerald-50" />

            <div className="relative grid gap-8 p-6 md:grid-cols-2 md:p-10">
              <div className="space-y-5">
                <div>
                  <p className="text-sm font-semibold text-blue-600">
                    {language === "fr"
                      ? "Aperçu de l’espace IA"
                      : language === "ar"
                      ? "معاينة مساحة الذكاء الاصطناعي"
                      : "AI Workspace Preview"}
                  </p>

                  <h2 className="mt-3 text-3xl font-bold text-slate-900">
                    {language === "fr"
                      ? "Analyse intelligente pour le juridique, la finance et le business"
                      : language === "ar"
                      ? "تحليل ذكي للقانون والمالية والأعمال"
                      : "Intelligent analysis for legal, finance, and business"}
                  </h2>

                  <p className="mt-4 text-slate-600 leading-7">
                    {language === "fr"
                      ? "Runexa combine plusieurs agents IA spécialisés dans un espace de travail unifié."
                      : language === "ar"
                      ? "تجمع Runexa عدة وكلاء ذكاء اصطناعي متخصصين داخل مساحة عمل موحدة."
                      : "Runexa combines multiple specialized AI agents inside a unified workspace."}
                  </p>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-5">
                    <p className="text-sm text-slate-500">
                      {language === "fr"
                        ? "Score de risque"
                        : language === "ar"
                        ? "مستوى المخاطر"
                        : "Risk score"}
                    </p>

                    <p className="mt-2 text-3xl font-bold text-blue-600">
                      82/100
                    </p>

                    <p className="mt-2 text-sm text-slate-500">
                      Legal AI
                    </p>
                  </div>

                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-5">
                    <p className="text-sm text-slate-500">
                      {language === "fr"
                        ? "Santé financière"
                        : language === "ar"
                        ? "الصحة المالية"
                        : "Financial health"}
                    </p>

                    <p className="mt-2 text-3xl font-bold text-emerald-600">
                      74%
                    </p>

                    <p className="mt-2 text-sm text-slate-500">
                      Finance AI
                    </p>
                  </div>

                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-5">
                    <p className="text-sm text-slate-500">
                      {language === "fr"
                        ? "Progression étude"
                        : language === "ar"
                        ? "تقدم الدراسة"
                        : "Study progress"}
                    </p>

                    <p className="mt-2 text-3xl font-bold text-violet-600">
                      91%
                    </p>

                    <p className="mt-2 text-sm text-slate-500">
                      Study AI
                    </p>
                  </div>

                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-5">
                    <p className="text-sm text-slate-500">
                      {language === "fr"
                        ? "Business insights"
                        : language === "ar"
                        ? "رؤى الأعمال"
                        : "Business insights"}
                    </p>

                    <p className="mt-2 text-3xl font-bold text-orange-600">
                      12
                    </p>

                    <p className="mt-2 text-sm text-slate-500">
                      Business AI
                    </p>
                  </div>
                </div>
              </div>

              <div className="rounded-3xl bg-slate-950 p-6 text-white shadow-2xl">
                <div className="flex items-center justify-between border-b border-white/10 pb-4">
                  <div>
                    <p className="text-sm text-slate-400">
                      Runexa AI Workspace
                    </p>

                    <p className="text-lg font-semibold">
                      {language === "fr" ? "Recommandations IA" : language === "ar" ? "توصيات الذكاء الاصطناعي" : "AI Recommendations"}
                    </p>
                  </div>

                  <span className="rounded-full bg-green-500/10 px-3 py-1 text-xs font-medium text-green-300">
                    Live
                  </span>
                </div>

                <div className="mt-6 space-y-4">
                  {[
                    language === "fr"
                      ? "Vérifier la clause de responsabilité du contrat fournisseur"
                      : language === "ar"
                      ? "مراجعة بند المسؤولية في عقد المورد"
                      : "Review liability clause in vendor contract",

                    language === "fr"
                      ? "Réduire les dépenses d’abonnements récurrents"
                      : language === "ar"
                      ? "تقليل نفقات الاشتراكات المتكررة"
                      : "Reduce recurring subscription expenses",

                    language === "fr"
                      ? "Améliorer la régularité des études cette semaine"
                      : language === "ar"
                      ? "تحسين انتظام الدراسة هذا الأسبوع"
                      : "Improve study consistency this week",

                    language === "fr"
                      ? "Surveiller les risques opérationnels business"
                      : language === "ar"
                      ? "مراقبة المخاطر التشغيلية للأعمال"
                      : "Monitor operational business risks",
                  ].map((item) => (
                    <div
                      key={item}
                      className="flex items-start gap-3 rounded-2xl border border-white/10 bg-white/5 p-4"
                    >
                      <div className="mt-1 h-2 w-2 rounded-full bg-blue-400" />

                      <p className="text-sm text-slate-200">
                        {item}
                      </p>
                    </div>
                  ))}
                </div>

                <div className="mt-6 rounded-2xl border border-blue-400/20 bg-blue-500/10 p-4 text-sm text-blue-100">
                  {language === "fr" ? "Workflows IA unifiés → analyses plus rapides → décisions plus intelligentes" : language === "ar" ? "سير عمل موحد بالذكاء الاصطناعي → تحليل أسرع → قرارات أذكى" : "Unified AI workflows → faster analysis → smarter decisions"}
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
            <p className="mt-3 text-slate-600 max-w-3xl mx-auto">
              {t.chooseDesc}
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {t.agents.map((agent: string[]) => {
              const style = agentStyles[agent[3]];
              const Icon = style.icon;

              return (
                <div
                  key={agent[0]}
                  className="bg-white p-6 rounded-2xl border shadow-sm flex flex-col justify-between"
                >
                  <div>
                    <div className="flex items-center justify-between gap-3">
                      <div className={`flex h-11 w-11 items-center justify-center rounded-2xl ${style.iconBox}`}>
                        <Icon className={`h-6 w-6 ${style.iconColor}`} />
                      </div>

                      <span className="text-xs bg-slate-100 text-slate-600 px-3 py-1 rounded-full">
                        {t.available}
                      </span>
                    </div>

                    <h3 className="mt-4 text-xl font-bold">
                      {agent[0]}
                    </h3>

                    <p className="mt-4 text-slate-600">{agent[1]}</p>
                  </div>

                  <Link
                    href={agent[2]}
                    className="inline-block mt-6 text-center px-4 py-2 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition"
                  >
                    {t.open}
                  </Link>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      <section className="px-6 py-12">
        <div className="max-w-6xl mx-auto">
          <div className="relative overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">
            <div className="absolute inset-0 bg-gradient-to-br from-blue-50 via-white to-slate-50" />

            <div className="relative p-8 md:p-12">
              <div className="text-center mb-10">
                <h2 className="text-3xl font-bold text-slate-900">
                  {t.howTitle}
                </h2>
              </div>

              <div className="grid gap-4 md:grid-cols-3">
                {t.howSteps.map((step: string, index: number) => (
                  <div
                    key={step}
                    className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"
                  >
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-600 text-sm font-bold text-white">
                      {index + 1}
                    </div>

                    <p className="mt-4 font-semibold text-slate-900">
                      {step}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>


      <section className="px-6 py-12">
        <div className="max-w-6xl mx-auto">
          <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm md:p-12">
            <p className="text-sm font-semibold text-blue-600">
              {t.seoTitle}
            </p>

            <h2 className="mt-3 text-3xl font-bold text-slate-900">
              {t.seoHeading}
            </h2>

            <p className="mt-4 max-w-4xl text-slate-600 leading-7">
              {t.seoDesc}
            </p>

            <div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {t.seoItems.map((item: string) => (
                <div
                  key={item}
                  className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm font-semibold text-slate-700"
                >
                  {item}
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="px-6 py-12">
        <div className="max-w-6xl mx-auto">
          <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm md:p-12">
            <p className="text-sm font-semibold text-blue-600">
              {t.faqTitle}
            </p>

            <h2 className="mt-3 text-3xl font-bold text-slate-900">
              {t.faqHeading}
            </h2>

            <div className="mt-8 grid gap-4 md:grid-cols-2">
              {t.faqItems.map((item: string[]) => (
                <div
                  key={item[0]}
                  className="rounded-2xl border border-slate-200 bg-slate-50 p-5"
                >
                  <h3 className="font-bold text-slate-900">
                    {item[0]}
                  </h3>

                  <p className="mt-2 text-sm leading-6 text-slate-600">
                    {item[1]}
                  </p>
                </div>
              ))}
            </div>
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

      <section className="px-6 py-16">
        <div className="max-w-5xl mx-auto bg-blue-600 text-white rounded-3xl p-10 text-center">
          <h2 className="text-3xl font-bold">{t.ctaTitle}</h2>
          <p className="mt-4 text-blue-100">{t.ctaDesc}</p>

          <Link
            href="/register"
            className="inline-block mt-6 px-6 py-3 bg-white text-blue-600 rounded-xl font-semibold"
          >
            {t.ctaButton}
          </Link>

          <p className="mt-8 text-center text-sm text-blue-100 max-w-2xl mx-auto">
            {t.disclaimer}
          </p>
        </div>
      </section>
    </main>
  );
}
