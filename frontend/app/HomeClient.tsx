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
  MessageSquareQuote,
  CheckCircle2,
} from "lucide-react";

type Locale = "en" | "fr" | "ar";
type AgentKey = "legal" | "finance" | "study" | "business";

type Agent = [string, string, string, AgentKey];

const labels: Record<Locale, any> = {
  en: {
    platform: "Runexa AI Platform",
    title: "Upload Your Document.\nGet the Intelligence You Need to Decide.",
    explore: "Explore AI Agents",
    pricing: "Plans & Pricing",
    blog: "Insights",
    trustLine: "$1 trial per account · Unified credits · Privacy-first AI platform",
    privacyIntroTitle: "Privacy-First Document Processing",
    privacyIntroDesc:
      "Runexa is designed for document analysis workflows where privacy matters. Uploaded files are processed only to generate the requested analysis. Personal identifiers may be replaced with neutral labels before AI processing when applicable. Customer content is never used to train public AI models. Uploaded files are automatically deleted from processing storage after analysis, and customer data remains isolated between users and workspaces.",
    privacyPromises: [
      "Personal identifiers may be anonymized before AI processing when applicable",
      "Customer content is never used to train public AI models",
      "Uploaded files are automatically deleted after analysis",
      "Customer data remains isolated between users and workspaces",
    ],
    privacyFlow: ["Upload", "Anonymize", "Analyze", "Report", "Delete"],
    available: "Available",
    ctaTitle: "One Platform. Multiple AI Agents. Smarter Decisions.",
    ctaDesc:
      "Runexa is a unified AI platform for document analysis, financial intelligence, learning, and enterprise decision support.",
    ctaButton: "Create Account",
    disclaimer:
      "AI-generated insights may contain errors. Always verify information before making important decisions.",
    faqTitle: "Frequently Asked Questions",
    agents: [
      ["Runexa Legal Agent", "Contract review with clause risk scoring, red flags, obligations, negotiation priorities, and practical guidance before signing.", "/legal-ai", "legal"],
      ["Runexa Finance Intelligence Agent", "Bank statement intelligence with cashflow, spending categories, subscriptions, savings opportunities, budgets, risks, and AI coaching.", "/finance-ai", "finance"],
      ["Runexa Study Workspace", "Turn lessons, PDFs, Word files, or scanned documents into summaries, audio lessons, mind maps, quizzes, flashcards, and study plans.", "/study-ai", "study"],
      ["Runexa Business Decision Intelligence", "Upload CSV or Excel files and receive KPI dashboards, forecasts, risks, opportunities, charts, and export-ready reports.", "/business-ai", "business"],
    ] as Agent[],
    faqItems: [
      ["What is Runexa?", "Runexa is an AI workspace with specialized agents for legal, finance, study, and business workflows."],
      ["How does it work?", "Upload a document or dataset, choose an agent, and receive structured analysis, recommendations, and reports."],
      ["Is Runexa secure?", "Runexa is designed around privacy-first document workflows, customer data isolation, and automatic file deletion after analysis."],
      ["Does it replace professionals?", "No. Runexa provides decision support. Important decisions should be verified by qualified professionals."],
    ],
  },
  fr: {
    platform: "Plateforme IA Runexa",
    title: "Importez votre document.\nObtenez l’intelligence nécessaire pour décider.",
    explore: "Découvrir les agents IA",
    pricing: "Plans et tarifs",
    blog: "Ressources",
    trustLine: "Un essai à 1 $ par compte · Crédits unifiés · Plateforme IA conçue pour la confidentialité",
    privacyIntroTitle: "Traitement documentaire conçu pour la confidentialité",
    privacyIntroDesc:
      "Runexa est conçu pour les workflows d’analyse documentaire où la confidentialité est essentielle. Les fichiers importés sont traités uniquement pour générer l’analyse demandée. Les identifiants personnels peuvent être remplacés par des libellés neutres avant le traitement par l’IA lorsque cela est applicable. Les contenus clients ne servent jamais à entraîner des modèles IA publics. Les fichiers importés sont automatiquement supprimés du stockage de traitement après analyse, et les données restent isolées entre utilisateurs et espaces de travail.",
    privacyPromises: [
      "Les identifiants personnels peuvent être anonymisés avant le traitement par l’IA lorsque cela est applicable",
      "Les contenus clients ne servent jamais à entraîner des modèles IA publics",
      "Les fichiers importés sont supprimés automatiquement après analyse",
      "Les données restent isolées entre utilisateurs et espaces de travail",
    ],
    privacyFlow: ["Importer", "Anonymiser", "Analyser", "Rapport", "Supprimer"],
    available: "Disponible",
    ctaTitle: "Une plateforme. Plusieurs agents IA. Des décisions plus intelligentes.",
    ctaDesc: "Runexa est une plateforme IA unifiée pour l’analyse documentaire, la finance, l’apprentissage et l’aide à la décision en entreprise.",
    ctaButton: "Créer un compte",
    disclaimer: "Les analyses générées par l’IA peuvent contenir des erreurs. Vérifiez toujours les informations avant de prendre une décision.",
    faqTitle: "Questions fréquentes",
    agents: [
      ["Runexa Legal Agent", "Analyse complète des contrats avec évaluation des risques, détection des clauses sensibles, extraction des obligations, recommandations de négociation et aide à la décision avant signature.", "/legal-ai", "legal"],
      ["Runexa Finance Intelligence Agent", "Analyse intelligente des relevés bancaires avec cashflow, catégorisation des dépenses, détection des abonnements, opportunités d’économies, budgets, risques et coach financier IA.", "/finance-ai", "finance"],
      ["Runexa Study Workspace", "Transformez vos cours, PDF, documents Word ou scans en résumés, audio, cartes mentales, quiz, flashcards et plans de révision.", "/study-ai", "study"],
      ["Runexa Business Decision Intelligence", "Importez des fichiers CSV ou Excel et obtenez vos KPI, prévisions, risques, opportunités, graphiques et rapports exportables.", "/business-ai", "business"],
    ] as Agent[],
    faqItems: [
      ["Qu’est-ce que Runexa ?", "Runexa est un workspace IA avec des agents spécialisés pour le juridique, la finance, l’étude et le business."],
      ["Comment ça marche ?", "Importez un document ou des données, choisissez un agent, puis recevez une analyse structurée et des recommandations."],
      ["Runexa est-il sécurisé ?", "Runexa est conçu autour de workflows confidentiels, de l’isolation des données et de la suppression automatique après analyse."],
      ["Runexa remplace-t-il les professionnels ?", "Non. Runexa fournit une aide à la décision. Les décisions importantes doivent être vérifiées par des professionnels qualifiés."],
    ],
  },
  ar: {
    platform: "منصة Runexa للذكاء الاصطناعي",
    title: "ارفع مستندك.\nواحصل على التحليل الذي تحتاجه لاتخاذ القرار.",
    explore: "اكتشف وكلاء Runexa",
    pricing: "الخطط والأسعار",
    blog: "المدونة",
    trustLine: "تجربة واحدة بقيمة 1 دولار لكل حساب · أرصدة موحدة · منصة مصممة لحماية الخصوصية",
    privacyIntroTitle: "معالجة مستندات تراعي الخصوصية",
    privacyIntroDesc:
      "تم تصميم Runexa لتدفقات عمل تحليل المستندات التي تتطلب الخصوصية. تُعالج الملفات المرفوعة فقط لإنشاء التحليل المطلوب. يمكن استبدال المعرّفات الشخصية بوسوم محايدة قبل المعالجة بالذكاء الاصطناعي عندما يكون ذلك مناسباً. لا تُستخدم محتويات العملاء أبداً لتدريب نماذج ذكاء اصطناعي عامة. ويتم حذف الملفات المرفوعة تلقائياً بعد اكتمال التحليل، وتبقى بيانات العملاء معزولة بين المستخدمين ومساحات العمل.",
    privacyPromises: [
      "يمكن إخفاء هوية المعرّفات الشخصية قبل المعالجة بالذكاء الاصطناعي عندما يكون ذلك مناسباً",
      "لا تُستخدم محتويات العملاء أبداً لتدريب نماذج ذكاء اصطناعي عامة",
      "يتم حذف الملفات المرفوعة تلقائياً بعد اكتمال التحليل",
      "تبقى بيانات العملاء معزولة بين المستخدمين ومساحات العمل",
    ],
    privacyFlow: ["رفع الملف", "إخفاء الهوية", "التحليل", "إنشاء التقرير", "حذف الملف"],
    available: "متاح",
    ctaTitle: "منصة واحدة. وكلاء ذكاء اصطناعي متخصصون. قرارات أكثر ذكاءً.",
    ctaDesc: "Runexa منصة موحدة لتحليل المستندات وفهم البيانات المالية وتسريع التعلم ودعم قرارات الأعمال.",
    ctaButton: "إنشاء حساب",
    disclaimer: "التحليلات مدعومة بالذكاء الاصطناعي وقد تحتوي على أخطاء. يُرجى التحقق من النتائج قبل اتخاذ أي قرار.",
    faqTitle: "الأسئلة الشائعة",
    agents: [
      ["Runexa Legal Agent", "مراجعة العقود مع تقييم المخاطر، واكتشاف البنود الحساسة، واستخراج الالتزامات، وتوصيات التفاوض، وتوجيه عملي قبل التوقيع.", "/legal-ai", "legal"],
      ["Runexa Finance Intelligence Agent", "تحليل ذكي لكشوفات الحساب البنكية يشمل التدفق النقدي، وتصنيف المصروفات، واكتشاف الاشتراكات، وفرص التوفير، والميزانية، والمخاطر، والمدرب المالي الذكي.", "/finance-ai", "finance"],
      ["Runexa Study Workspace", "حوّل الدروس وملفات PDF وWord والمستندات الممسوحة ضوئياً إلى ملخصات ودروس صوتية وخرائط ذهنية واختبارات وبطاقات مراجعة وخطط دراسة.", "/study-ai", "study"],
      ["Runexa Business Decision Intelligence", "ارفع بيانات بصيغة CSV أو Excel للحصول على مؤشرات أداء وتوقعات ومخاطر وفرص ورسوم بيانية وتقارير قابلة للتصدير.", "/business-ai", "business"],
    ] as Agent[],
    faqItems: [
      ["ما هي Runexa؟", "Runexa منصة ذكاء اصطناعي تضم وكلاء متخصصين للقانون والمالية والدراسة والأعمال."],
      ["كيف تعمل؟", "ارفع مستنداً أو بيانات، اختر الوكيل المناسب، ثم احصل على تحليل منظم وتوصيات."],
      ["هل Runexa آمنة؟", "تم تصميم Runexa حول الخصوصية وعزل بيانات العملاء والحذف التلقائي بعد التحليل."],
      ["هل تحل محل المختصين؟", "لا. توفر Runexa دعماً لاتخاذ القرار، ويجب التحقق من القرارات المهمة مع مختصين مؤهلين."],
    ],
  },
};

const agentStyles: Record<AgentKey, any> = {
  legal: { icon: Scale, card: "border-blue-100 bg-white hover:shadow-blue-100", iconBox: "bg-blue-50", iconColor: "text-blue-700", badge: "bg-blue-50 text-blue-700" },
  finance: { icon: BarChart3, card: "bg-gradient-to-br from-emerald-500 to-green-600 text-white hover:shadow-emerald-200", iconBox: "bg-white/15", iconColor: "text-white", badge: "bg-white/10 text-emerald-50" },
  study: { icon: GraduationCap, card: "border-violet-100 bg-white hover:shadow-violet-100", iconBox: "bg-violet-50", iconColor: "text-violet-700", badge: "bg-violet-50 text-violet-700" },
  business: { icon: BriefcaseBusiness, card: "border-orange-100 bg-white hover:shadow-orange-100", iconBox: "bg-orange-50", iconColor: "text-orange-700", badge: "bg-orange-50 text-orange-700" },
};

export default function HomeClient({
  initialLanguage = "en",
  lockInitialLanguage = false,
}: {
  initialLanguage?: Locale;
  lockInitialLanguage?: boolean;
}) {
  const [language, setLanguage] = useState<Locale>(initialLanguage);
  const t = labels[language] || labels.en;

  useEffect(() => {
    if (lockInitialLanguage) {
      setLanguage(initialLanguage);
      return;
    }

    const saved = localStorage.getItem("locale");
    if (saved === "en" || saved === "fr" || saved === "ar") setLanguage(saved);
    else setLanguage(initialLanguage);
  }, [initialLanguage, lockInitialLanguage]);

  const handleLanguageChange = (lang: Locale) => {
    setLanguage(lang);
    localStorage.setItem("locale", lang);
    window.dispatchEvent(new Event("locale-change"));
  };

  return (
    <main dir={language === "ar" ? "rtl" : "ltr"} className="min-h-screen bg-slate-50 text-slate-900">
      <section className="px-6 py-20">
        <div className="mx-auto max-w-6xl space-y-10 text-center">
          <select
            value={language}
            onChange={(e) => {
              const next = e.target.value;
              if (next === "en" || next === "fr" || next === "ar") handleLanguageChange(next);
            }}
            className="rounded-lg border bg-white px-3 py-2 transition-all duration-200 hover:border-blue-300 hover:shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            <option value="en">English</option>
            <option value="fr">Français</option>
            <option value="ar">العربية</option>
          </select>

          <div className="relative overflow-hidden rounded-[34px] border border-white/80 bg-white/90 p-6 text-left shadow-[0_30px_100px_rgba(37,99,235,0.16)] backdrop-blur-xl md:p-12">
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(59,130,246,0.14),transparent_34%),linear-gradient(135deg,rgba(255,255,255,0.96),rgba(239,246,255,0.68))]" />
            <div className="relative grid items-center gap-10 lg:grid-cols-[1.05fr_0.95fr]">
              <div className="space-y-7">
                <div className="inline-flex items-center gap-2 rounded-full border border-blue-200 bg-blue-50 px-4 py-2 text-xs font-bold uppercase tracking-wide text-blue-700">
                  <Sparkles className="h-4 w-4" /> {t.platform}
                </div>

                <h1 className="max-w-4xl text-4xl font-black leading-[1.05] tracking-tight text-slate-950 md:text-6xl">
                  {String(t.title).split("\n")[0]}
                  <br />
                  <span className="bg-gradient-to-r from-blue-600 via-indigo-600 to-violet-600 bg-clip-text text-transparent">
                    {String(t.title).split("\n")[1]}
                  </span>
                </h1>

                <div className="flex flex-wrap gap-3">
                  {[
                    [language === "fr" ? "Contrats" : language === "ar" ? "العقود" : "Contracts", Scale, "border-blue-100 bg-blue-50 text-blue-700"],
                    [language === "fr" ? "Finance" : language === "ar" ? "المالية" : "Finance", BarChart3, "border-emerald-100 bg-emerald-50 text-emerald-700"],
                    [language === "fr" ? "Formation" : language === "ar" ? "التعلم" : "Learning", GraduationCap, "border-violet-100 bg-violet-50 text-violet-700"],
                    [language === "fr" ? "Business" : language === "ar" ? "الأعمال" : "Business", BriefcaseBusiness, "border-orange-100 bg-orange-50 text-orange-700"],
                  ].map(([label, Icon, className]: any) => (
                    <div key={label} className={`inline-flex items-center gap-2 rounded-2xl border px-4 py-3 text-sm font-bold shadow-sm ${className}`}>
                      <Icon className="h-4 w-4" /> {label}
                    </div>
                  ))}
                </div>

                <div className="flex flex-col gap-3 sm:flex-row">
                  <a href="#agents" className="inline-flex items-center justify-center gap-2 rounded-2xl bg-blue-600 px-7 py-4 text-sm font-bold text-white shadow-xl shadow-blue-200 transition-all duration-200 ease-out hover:-translate-y-1 hover:bg-blue-700 hover:shadow-2xl active:translate-y-0 active:scale-[0.98] focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
                    {t.explore} <span>→</span>
                  </a>
                  <Link href="/pricing" className="inline-flex items-center justify-center gap-2 rounded-2xl border border-slate-200 bg-white px-7 py-4 text-sm font-bold text-slate-900 shadow-sm transition-all duration-200 ease-out hover:-translate-y-1 hover:border-blue-200 hover:bg-slate-50 hover:shadow-lg active:translate-y-0 active:scale-[0.98] focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
                    <ShieldCheck className="h-4 w-4" /> {t.pricing}
                  </Link>
                  <Link href="/blog" className="inline-flex items-center justify-center gap-2 rounded-2xl border border-slate-200 bg-white px-7 py-4 text-sm font-bold text-slate-900 shadow-sm transition-all duration-200 ease-out hover:-translate-y-1 hover:border-blue-200 hover:bg-slate-50 hover:shadow-lg active:translate-y-0 active:scale-[0.98] focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
                    <Globe className="h-4 w-4" /> {t.blog}
                  </Link>
                </div>

                <Link href="/pricing" className="block max-w-2xl rounded-3xl border border-blue-200 bg-gradient-to-r from-blue-600 to-indigo-600 p-5 text-white shadow-xl shadow-blue-200 transition-all duration-200 ease-out hover:-translate-y-1 hover:shadow-2xl active:translate-y-0 active:scale-[0.99] focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <p className="text-lg font-black">{language === "fr" ? "Essayez Runexa pour 1 $" : language === "ar" ? "جرّب Runexa مقابل دولار واحد" : "Try Runexa for $1"}</p>
                      <p className="mt-1 text-sm font-semibold text-blue-100">{language === "fr" ? "Analysez un document réel en quelques minutes." : language === "ar" ? "حلل مستنداً حقيقياً خلال دقائق." : "Analyze a real document in minutes."}</p>
                    </div>
                    <span className="text-2xl">→</span>
                  </div>
                </Link>

                <p className="rounded-2xl border border-blue-100 bg-white/85 px-5 py-4 text-sm font-semibold text-slate-700 shadow-sm">{t.trustLine}</p>
              </div>

              <div className="relative min-h-[420px]">
                <div className="absolute left-1/2 top-8 h-[380px] w-[280px] -translate-x-1/2 rounded-[34px] border border-slate-200 bg-white p-7 shadow-[0_25px_80px_rgba(37,99,235,0.24)]">
                  <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-50 text-blue-700"><Sparkles className="h-6 w-6" /></div>
                  <p className="mt-8 text-xl font-black text-slate-950">{language === "fr" ? "Votre document" : language === "ar" ? "مستندك" : "Your Document"}</p>
                  <p className="mt-1 text-sm font-semibold text-slate-400">PDF · 2.4 MB</p>
                  <div className="mt-8 space-y-3">{["w-full", "w-11/12", "w-4/5", "w-10/12", "w-7/12"].map((w) => <div key={w} className={`h-3 rounded-full bg-slate-200 ${w}`} />)}</div>
                  <div className="mt-10 inline-flex items-center gap-2 rounded-2xl bg-emerald-50 px-4 py-3 text-sm font-bold text-emerald-700">✓ {language === "fr" ? "Analyse terminée" : language === "ar" ? "اكتمل التحليل" : "Analysis Complete"}</div>
                </div>
                {[
                  [ShieldCheck, language === "fr" ? "Confidentiel" : language === "ar" ? "خصوصية" : "Private", "top-6 right-0", "bg-violet-100 text-violet-700"],
                  [BarChart3, language === "fr" ? "Insights clés" : language === "ar" ? "رؤى رئيسية" : "Key Insights", "right-0 top-40", "bg-emerald-100 text-emerald-700"],
                  [Lock, language === "fr" ? "Jamais utilisées pour l’entraînement" : language === "ar" ? "لا تُستخدم لتدريب النماذج" : "Never Used for Training", "left-2 bottom-8", "bg-blue-100 text-blue-700"],
                ].map(([Icon, label, pos, color]: any) => (
                  <div key={label} className={`absolute rounded-2xl border border-slate-100 bg-white/90 px-5 py-4 shadow-xl ${pos}`}>
                    <div className="flex items-center gap-3"><div className={`flex h-11 w-11 items-center justify-center rounded-2xl ${color}`}><Icon className="h-6 w-6" /></div><p className="text-sm font-black text-slate-900">{label}</p></div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <IntelligencePreviewCard language={language} />
          <WhyRunexa language={language} />
          <PrivacySection t={t} language={language} />
          <AgentsSection t={t} language={language} />
          <ResultTestimonialsSection language={language} />
          <PricingSection language={language} />
          <FAQSection t={t} />
          <CTASection t={t} />
        </div>
      </section>
    </main>
  );
}


function IntelligencePreviewCard({ language }: { language: Locale }) {
  const preview = {
    en: {
      eyebrow: "Runexa Intelligence Report",
      status: "Analysis Complete",
      documentLabel: "Document",
      documentName: "Employment_Contract.pdf",
      scoreLabel: "Overall Risk",
      scoreValue: "Medium",
      findingsLabel: "Key findings",
      findings: [
        "25 clauses identified",
        "1 high-risk clause detected",
        "7 medium-risk clauses found",
        "112 clause dependencies mapped",
      ],
      recommendationLabel: "Decision recommendation",
      recommendation: "Negotiate key clauses before signing.",
      footer: "Legal · Finance · Study · Business",
    },
    fr: {
      eyebrow: "Rapport d’intelligence Runexa",
      status: "Analyse terminée",
      documentLabel: "Document",
      documentName: "Contrat_de_travail.pdf",
      scoreLabel: "Risque global",
      scoreValue: "Moyen",
      findingsLabel: "Insights clés",
      findings: [
        "25 clauses identifiées",
        "1 clause à risque élevé détectée",
        "7 clauses à risque moyen trouvées",
        "112 dépendances entre clauses cartographiées",
      ],
      recommendationLabel: "Recommandation de décision",
      recommendation: "Négocier les clauses clés avant signature.",
      footer: "Juridique · Finance · Étude · Business",
    },
    ar: {
      eyebrow: "تقرير Runexa الذكي",
      status: "اكتمل التحليل",
      documentLabel: "المستند",
      documentName: "عقد_عمل.pdf",
      scoreLabel: "مستوى المخاطر",
      scoreValue: "متوسط",
      findingsLabel: "رؤى رئيسية",
      findings: [
        "تم تحديد 25 بنداً",
        "تم اكتشاف بند عالي المخاطر",
        "تم العثور على 7 بنود متوسطة المخاطر",
        "تم ربط 112 علاقة بين البنود",
      ],
      recommendationLabel: "توصية القرار",
      recommendation: "يُنصح بالتفاوض على البنود الأساسية قبل التوقيع.",
      footer: "القانون · المالية · الدراسة · الأعمال",
    },
  };

  const t = preview[language] || preview.en;

  return (
    <section className="mx-auto max-w-5xl rounded-[32px] border border-slate-200 bg-white p-5 text-left shadow-[0_24px_80px_rgba(15,23,42,0.10)] md:p-8">
      <div className="flex flex-col gap-6 md:flex-row md:items-stretch md:justify-between">
        <div className="flex-1 rounded-3xl bg-slate-950 p-6 text-white">
          <div className="flex items-center justify-between gap-4 border-b border-white/10 pb-5">
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-blue-300">
                {t.eyebrow}
              </p>
              <p className="mt-2 text-lg font-black">{t.status}</p>
            </div>
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-emerald-400/10 text-emerald-300">
              <CheckCircle2 className="h-6 w-6" />
            </div>
          </div>

          <div className="mt-5 grid gap-4 md:grid-cols-2">
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
              <p className="text-xs text-slate-400">{t.documentLabel}</p>
              <p className="mt-1 font-bold text-slate-100">{t.documentName}</p>
            </div>

            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
              <p className="text-xs text-slate-400">{t.scoreLabel}</p>
              <p className="mt-1 font-bold text-amber-300">{t.scoreValue}</p>
            </div>
          </div>

          <div className="mt-5 rounded-2xl border border-white/10 bg-white/5 p-4">
            <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
              {t.findingsLabel}
            </p>

            <div className="mt-4 grid gap-3 md:grid-cols-2">
              {t.findings.map((finding) => (
                <div key={finding} className="flex items-start gap-3 text-sm text-slate-200">
                  <span className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-blue-500/20 text-xs font-bold text-blue-200">
                    ✓
                  </span>
                  <span>{finding}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="flex min-w-0 flex-1 flex-col justify-between rounded-3xl border border-blue-100 bg-gradient-to-br from-blue-50 via-white to-indigo-50 p-6">
          <div>
            <p className="text-sm font-bold text-blue-700">{t.recommendationLabel}</p>
            <h3 className="mt-3 text-2xl font-black leading-tight text-slate-950">
              {t.recommendation}
            </h3>

            <div className="mt-6 space-y-3">
              {[
                language === "fr"
                  ? "Analyse structurée"
                  : language === "ar"
                  ? "تحليل منظم"
                  : "Structured analysis",
                language === "fr"
                  ? "Insights orientés décision"
                  : language === "ar"
                  ? "رؤى تساعد على اتخاذ القرار"
                  : "Decision-ready insights",
                language === "fr"
                  ? "Rapport exploitable"
                  : language === "ar"
                  ? "تقرير قابل للاستخدام"
                  : "Actionable report",
              ].map((item) => (
                <div key={item} className="flex items-center gap-3 rounded-2xl border border-blue-100 bg-white/80 p-3 text-sm font-semibold text-slate-700">
                  <Sparkles className="h-4 w-4 text-blue-600" />
                  {item}
                </div>
              ))}
            </div>
          </div>

          <p className="mt-6 rounded-2xl border border-slate-200 bg-white px-4 py-3 text-center text-sm font-bold text-slate-700">
            {t.footer}
          </p>
        </div>
      </div>
    </section>
  );
}

function WhyRunexa({ language }: { language: Locale }) {
  const rows = language === "fr"
    ? [["ChatGPT", "Conversation générale", "Analyse documentaire structurée"], ["Claude", "Analyse avancée nécessitant des instructions précises", "Importer → Analyser → Rapport"], ["Gemini", "IA généraliste", "Workflows spécialisés d’aide à la décision"], ["Outils génériques", "Résumé et rédaction", "Scoring des risques, KPI et aide à la décision"]]
    : language === "ar"
    ? [["ChatGPT", "محادثة عامة", "سير عمل منظم للمستندات"], ["Claude", "تحليل قوي لكنه يحتاج إلى توجيه", "رفع → تحليل → تقرير"], ["Gemini", "ذكاء اصطناعي عام", "سير عمل متخصص لدعم القرار"], ["أدوات عامة", "تلخيص وكتابة", "تقييم المخاطر والمؤشرات ودعم القرار"]]
    : [["ChatGPT", "General chat and prompting", "Structured document workflows"], ["Claude", "Powerful document analysis that requires expert prompting", "Upload → Analyze → Report"], ["Gemini", "General-purpose AI", "Specialized decision workflows"], ["Generic AI tools", "Writing and summarization", "Risk scoring, KPI analysis, decision intelligence"]];

  return <section className="rounded-[28px] border border-slate-200 bg-white p-6 text-left shadow-sm">
    <p className="text-sm font-semibold text-blue-600">{language === "fr" ? "Pourquoi Runexa plutôt qu’une IA généraliste ?" : language === "ar" ? "لماذا Runexa بدلاً من الذكاء الاصطناعي العام؟" : "Why Runexa Instead of Generic AI?"}</p>
    <h2 className="mt-3 text-2xl font-bold text-slate-900">{language === "fr" ? "La plupart des IA génèrent des réponses. Runexa automatise des workflows spécialisés." : language === "ar" ? "معظم أدوات الذكاء الاصطناعي تولد إجابات. أما Runexa فينفّذ سير عمل ذكياً ومتخصصاً." : "Most AI tools generate answers. Runexa executes specialized AI workflows."}</h2>
    <p className="mt-3 text-sm leading-6 text-slate-600">{language === "fr" ? "Importez un document. Recevez une analyse structurée. Prenez une décision." : language === "ar" ? "ارفع مستنداً. احصل على تحليل منظم. اتخذ قراراً أفضل." : "Upload a document. Receive structured analysis. Take action."}</p>
    <div className="mt-6 overflow-hidden rounded-2xl border border-slate-200">
      <div className="grid grid-cols-3 bg-slate-50 text-xs font-bold uppercase tracking-wide text-slate-500"><div className="p-3">{language === "fr" ? "Concurrent" : language === "ar" ? "المنافس" : "Competitor"}</div><div className="p-3">{language === "fr" ? "Approche" : language === "ar" ? "النهج" : "Their Approach"}</div><div className="p-3">{language === "fr" ? "Avantage Runexa" : language === "ar" ? "ميزة Runexa" : "Runexa Advantage"}</div></div>
      {rows.map((row) => <div key={row[0]} className="grid grid-cols-3 border-t border-slate-200 text-sm text-slate-700"><div className="p-3 font-semibold text-slate-900">{row[0]}</div><div className="p-3">{row[1]}</div><div className="p-3 font-medium text-blue-700">{row[2]}</div></div>)}
    </div>
  </section>;
}

function PrivacySection({ t, language }: { t: any; language: Locale }) {
  return <section className="rounded-[28px] border border-blue-100 bg-white/90 p-6 text-left shadow-sm backdrop-blur">
    <div className="inline-flex items-center gap-2 rounded-full border border-blue-200 bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-700"><ShieldCheck className="h-4 w-4" />{language === "fr" ? "Traitement des données" : language === "ar" ? "معالجة البيانات" : "Data handling"}</div>
    <h2 className="mt-3 text-2xl font-bold text-slate-900">{t.privacyIntroTitle}</h2>
    <p className="mt-3 text-sm leading-6 text-slate-600 md:text-base md:leading-7">{t.privacyIntroDesc}</p>
    <div className="mt-6 grid gap-3 md:grid-cols-5">{t.privacyFlow.map((item: string, index: number) => <div key={item} className="rounded-2xl border border-slate-200 bg-slate-50 p-4 text-center"><div className="mx-auto flex h-8 w-8 items-center justify-center rounded-full bg-blue-600 text-xs font-bold text-white">{index + 1}</div><p className="mt-3 text-sm font-semibold text-slate-800">{item}</p></div>)}</div>
    <div className="mt-5 grid gap-3 md:grid-cols-2">{t.privacyPromises.map((item: string) => <div key={item} className="flex items-start gap-3 rounded-2xl border border-slate-200 bg-white p-4"><ShieldCheck className="mt-0.5 h-5 w-5 shrink-0 text-blue-600" /><p className="text-sm font-medium text-slate-700">{item}</p></div>)}</div>
  </section>;
}

function AgentsSection({ t, language }: { t: any; language: Locale }) {
  return <section id="agents" className="scroll-mt-24 rounded-[32px] border border-slate-200/80 bg-white/80 p-6 shadow-[0_20px_80px_rgba(15,23,42,0.08)] backdrop-blur-xl md:p-10">
    <div className="mb-8 flex justify-center"><div className="inline-flex items-center gap-2 rounded-full border border-blue-200 bg-blue-50 px-5 py-2 text-sm font-semibold text-blue-700"><Users className="h-4 w-4" />{language === "fr" ? "Agents IA spécialisés" : language === "ar" ? "وكلاء ذكاء اصطناعي متخصصون" : "Specialized AI Agents"}</div></div>
    <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
      {t.agents.map((agent: Agent) => {
        const style = agentStyles[agent[3]];
        const Icon = style.icon;
        const dark = agent[3] === "finance";
        return <Link key={agent[0]} href={agent[2]} className={`group relative overflow-hidden rounded-3xl border p-5 shadow-lg transition-all duration-200 ease-out hover:-translate-y-1.5 hover:shadow-2xl active:translate-y-0 active:scale-[0.99] focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${style.card}`}>
          <div className={`flex h-12 w-12 items-center justify-center rounded-2xl ${style.iconBox}`}><Icon className={`h-6 w-6 ${style.iconColor}`} /></div>
          <h3 className={`mt-4 text-base font-bold ${dark ? "text-white" : "text-slate-900"}`}>{agent[0]}</h3>
          <p className={`mt-2 text-sm leading-6 ${dark ? "text-emerald-100" : "text-slate-500"}`}>{agent[1]}</p>
          <div className={`mt-5 inline-flex rounded-full px-3 py-1 text-xs font-medium ${style.badge}`}>{t.available}</div>
        </Link>;
      })}
    </div>
    <div className="mt-8 grid grid-cols-1 gap-4 border-t border-slate-200 pt-6 md:grid-cols-4">
      {(language === "fr"
        ? ["Confidentialité par conception", "Les données clients ne servent jamais à entraîner des modèles publics", "Suppression automatique des fichiers", "Isolation des espaces de travail"]
        : language === "ar"
        ? ["الخصوصية أولاً", "لا تُستخدم بيانات العملاء لتدريب النماذج العامة", "حذف الملفات تلقائياً", "عزل بيانات مساحات العمل"]
        : ["Privacy-first workflow", "No public model training", "Automatic file deletion", "Workspace isolation"]
      ).map((item, index) => {
        const icons = [Lock, Globe, Zap, ShieldCheck];
        const Icon = icons[index];
        return <div key={item} className="flex items-center gap-3 text-left"><div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-50 text-blue-700"><Icon className="h-6 w-6" /></div><p className="font-semibold text-slate-900">{item}</p></div>;
      })}
    </div>
  </section>;
}


function ResultTestimonialsSection({ language }: { language: Locale }) {
  const testimonials = {
    en: {
      eyebrow: "User outcomes",
      title: "Real use cases. Concrete results.",
      desc: "Runexa is designed to help users understand documents faster and make clearer decisions.",
      items: [
        {
          role: "Freelancer",
          useCase: "Contract review",
          quote:
            "I uploaded a freelance contract and Runexa highlighted 3 clauses I had completely missed, including payment terms and ownership risks.",
          result: "3 risky clauses detected",
        },
        {
          role: "Personal finance user",
          useCase: "Bank statement analysis",
          quote:
            "Runexa helped me understand where my money was going and identified recurring expenses I had not noticed.",
          result: "Subscriptions and savings opportunities found",
        },
        {
          role: "Student",
          useCase: "Study preparation",
          quote:
            "I uploaded a lesson PDF and received a summary, quiz, flashcards, and a revision plan instead of starting from a blank page.",
          result: "Complete study plan generated",
        },
      ],
    },
    fr: {
      eyebrow: "Résultats utilisateurs",
      title: "Des cas d’usage réels. Des résultats concrets.",
      desc:
        "Runexa aide les utilisateurs à comprendre leurs documents plus vite et à prendre des décisions plus claires.",
      items: [
        {
          role: "Freelance",
          useCase: "Analyse de contrat",
          quote:
            "J’ai importé un contrat freelance et Runexa a mis en évidence 3 clauses que j’avais complètement manquées, notamment sur le paiement et les droits de propriété.",
          result: "3 clauses à risque détectées",
        },
        {
          role: "Utilisateur finance",
          useCase: "Analyse de relevé bancaire",
          quote:
            "Runexa m’a aidé à comprendre où partait mon argent et a identifié des dépenses récurrentes que je n’avais pas remarquées.",
          result: "Abonnements et économies détectés",
        },
        {
          role: "Étudiant",
          useCase: "Préparation de cours",
          quote:
            "J’ai importé un PDF de cours et j’ai reçu un résumé, un quiz, des flashcards et un plan de révision au lieu de partir de zéro.",
          result: "Plan de révision complet généré",
        },
      ],
    },
    ar: {
      eyebrow: "نتائج المستخدمين",
      title: "حالات استخدام واقعية. نتائج ملموسة.",
      desc:
        "صُممت Runexa لمساعدة المستخدمين على فهم مستنداتهم بشكل أسرع واتخاذ قرارات أوضح.",
      items: [
        {
          role: "مستقل",
          useCase: "مراجعة عقد",
          quote:
            "رفعت عقد عمل حر، وساعدتني Runexa على اكتشاف 3 بنود مهمة لم أنتبه لها، خاصة ما يتعلق بالدفع وحقوق الملكية.",
          result: "تم اكتشاف 3 بنود عالية الأهمية",
        },
        {
          role: "مستخدم مالي",
          useCase: "تحليل كشف بنكي",
          quote:
            "ساعدتني Runexa على فهم أين تذهب أموالي، واكتشفت مصاريف متكررة لم أكن ألاحظها.",
          result: "اكتشاف اشتراكات وفرص توفير",
        },
        {
          role: "طالب",
          useCase: "التحضير للدراسة",
          quote:
            "رفعت ملف PDF خاصاً بالدرس، وحصلت على ملخص واختبار وبطاقات مراجعة وخطة دراسة بدل أن أبدأ من الصفر.",
          result: "إنشاء خطة دراسة كاملة",
        },
      ],
    },
  };

  const t = testimonials[language] || testimonials.en;

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-8 text-left shadow-sm md:p-12">
      <p className="text-sm font-semibold text-blue-600">{t.eyebrow}</p>

      <h2 className="mt-3 text-3xl font-bold text-slate-900">{t.title}</h2>

      <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-600 md:text-base">
        {t.desc}
      </p>

      <div className="mt-8 grid gap-5 md:grid-cols-3">
        {t.items.map((item) => (
          <div
            key={item.useCase}
            className="rounded-3xl border border-slate-200 bg-slate-50 p-6 transition-all duration-200 hover:-translate-y-1 hover:border-blue-200 hover:bg-white hover:shadow-lg"
          >
            <p className="text-xs font-bold uppercase tracking-wide text-blue-600">
              {item.useCase}
            </p>

            <blockquote className="mt-4 text-sm leading-6 text-slate-700">
              “{item.quote}”
            </blockquote>

            <div className="mt-5 rounded-2xl bg-white p-4">
              <p className="text-xs font-semibold text-slate-500">
                {item.role}
              </p>
              <p className="mt-1 text-sm font-bold text-slate-900">
                {item.result}
              </p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

function FeedbackSection({ language }: { language: Locale }) {
  const items = language === "fr" ? ["Analyse claire avant signature", "Budget plus lisible", "Révisions plus structurées"] : language === "ar" ? ["تحليل أوضح قبل التوقيع", "ميزانية أكثر وضوحاً", "تعلّم أكثر تنظيماً"] : ["Clearer analysis before signing", "More readable budget", "More structured learning"];
  return <section className="rounded-3xl border border-blue-100 bg-white p-8 text-left shadow-sm md:p-12">
    <p className="text-sm font-semibold text-blue-600">{language === "fr" ? "Ce que nos utilisateurs obtiennent" : language === "ar" ? "أمثلة على نتائج المستخدمين" : "Representative Customer Results"}</p>
    <h2 className="mt-3 text-3xl font-bold text-slate-900">{language === "fr" ? "Des workflows conçus pour aider à décider plus vite." : language === "ar" ? "سير عمل مصمم للمساعدة على اتخاذ قرارات أسرع." : "Workflows designed to help users decide faster."}</h2>
    <div className="mt-6 grid gap-4 md:grid-cols-3">{items.map((item) => <div key={item} className="rounded-2xl border border-slate-200 bg-slate-50 p-5 transition-all duration-200 hover:-translate-y-0.5 hover:border-blue-200 hover:bg-white hover:shadow-md"><MessageSquareQuote className="h-6 w-6 text-blue-600" /><p className="mt-3 font-semibold text-slate-800">{item}</p></div>)}</div>
  </section>;
}

function PricingSection({ language }: { language: Locale }) {
  return <section className="rounded-3xl border border-slate-200 bg-white p-8 text-left shadow-sm md:p-12">
    <p className="text-sm font-semibold text-blue-600">{language === "fr" ? "Plans simples" : language === "ar" ? "خطط بسيطة" : "Simple plans"}</p>
    <h2 className="mt-3 text-3xl font-bold text-slate-900">{language === "fr" ? "Commencez avec l’essai à 1 $, puis passez au plan adapté." : language === "ar" ? "ابدأ بتجربة 1 دولار ثم اختر الخطة المناسبة." : "Start with the $1 trial, then choose the plan that fits."}</h2>
    <div className="mt-6 grid gap-4 md:grid-cols-3">
      {(language === "fr" ? ["Essai", "Pro", "Entreprise"] : language === "ar" ? ["التجربة", "Pro", "المؤسسات"] : ["Trial", "Pro", "Enterprise"]).map((plan) => <div key={plan} className="rounded-2xl border border-slate-200 bg-slate-50 p-5 transition-all duration-200 hover:-translate-y-0.5 hover:border-blue-200 hover:bg-white hover:shadow-md"><p className="text-xl font-black text-slate-900">{plan}</p><p className="mt-2 text-sm text-slate-600">{language === "fr" ? "Crédits unifiés pour les agents Runexa." : language === "ar" ? "أرصدة موحدة لوكلاء Runexa." : "Unified credits for Runexa agents."}</p><CheckCircle2 className="mt-4 h-5 w-5 text-blue-600" /></div>)}
    </div>
    <Link href="/pricing" className="mt-6 inline-flex rounded-2xl bg-blue-600 px-6 py-3 text-sm font-bold text-white transition-all duration-200 ease-out hover:-translate-y-1 hover:bg-blue-700 hover:shadow-lg active:translate-y-0 active:scale-[0.98] focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">{language === "fr" ? "Voir les tarifs" : language === "ar" ? "عرض الأسعار" : "View pricing"}</Link>
  </section>;
}

function FAQSection({ t }: { t: any }) {
  return <section className="rounded-3xl border border-slate-200 bg-white p-8 text-left shadow-sm md:p-12">
    <p className="text-sm font-semibold text-blue-600">FAQ</p><h2 className="mt-3 text-3xl font-bold text-slate-900">{t.faqTitle}</h2>
    <div className="mt-6 grid gap-4 md:grid-cols-2">{t.faqItems.map(([q, a]: string[]) => <div key={q} className="rounded-2xl border border-slate-200 bg-slate-50 p-5 transition-all duration-200 hover:-translate-y-0.5 hover:border-blue-200 hover:bg-white hover:shadow-md"><h3 className="font-bold text-slate-900">{q}</h3><p className="mt-2 text-sm leading-6 text-slate-600">{a}</p></div>)}</div>
  </section>;
}

function CTASection({ t }: { t: any }) {
  return <section className="rounded-3xl bg-blue-600 p-10 text-center text-white">
    <h2 className="text-3xl font-bold">{t.ctaTitle}</h2><p className="mx-auto mt-4 max-w-2xl text-blue-100">{t.ctaDesc}</p>
    <Link href="/register" className="mt-6 inline-block rounded-xl bg-white px-6 py-3 font-semibold text-blue-600 transition-all duration-200 ease-out hover:-translate-y-1 hover:shadow-lg active:translate-y-0 active:scale-[0.98] focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-blue-600">{t.ctaButton}</Link>
    <p className="mx-auto mt-8 max-w-2xl text-sm text-blue-100">{t.disclaimer}</p>
  </section>;
}
