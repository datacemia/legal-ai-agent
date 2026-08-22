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
  CheckCircle2,
  FileText,
  FileSpreadsheet,
  AlertTriangle,
  BadgeCheck,
  FileCheck,
  TrendingUp,
  CreditCard,
  PiggyBank,
  ClipboardList,
  CalendarCheck,
  Activity,
} from "lucide-react";

type Locale = "en" | "fr" | "ar";
type AgentKey = "legal" | "finance" | "study" | "business";

type Agent = [string, string, string, AgentKey];

const labels: Record<Locale, any> = {
  en: {
    platform: "Runexa AI Platform",
    title: "Turn Documents Into Decisions.\nSpecialized AI for Real-World Work.",
    heroDesc: "Specialized AI agents analyze contracts, finances, learning materials, and business data — turning complex information into structured intelligence you can act on.",
    valueLine: "One account. One credit system. Multiple specialized AI agents.",
    explore: "Explore AI Agents",
    pricing: "Plans & Pricing",
    blog: "Insights",
    trustLine: "One-time $1 trial for one AI agent per account · Unified credits · Privacy-first AI platform",
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
    ctaTitle: "Ready to Turn Your Documents Into Decisions?",
    ctaDesc:
      "Start with the specialized AI workflow you need today — and scale across Runexa when you are ready.",
    ctaButton: "Get Started",
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
      ["What is Runexa?", "Runexa is a specialized AI platform for legal, finance, study, and business workflows."],
      ["How does it work?", "Upload a document or dataset, choose an agent, and receive structured analysis, recommendations, and reports."],
      ["Is Runexa secure?", "Runexa is designed around privacy-first document workflows, customer data isolation, and automatic file deletion after analysis."],
      ["Does it replace professionals?", "No. Runexa provides decision support. Important decisions should be verified by qualified professionals."],
    ],
  },
  fr: {
    platform: "Plateforme IA Runexa",
    title: "Transformez vos documents en décisions.\nUne IA spécialisée pour le monde réel.",
    heroDesc: "Des agents IA spécialisés analysent contrats, finances, supports pédagogiques et données d’entreprise pour transformer l’information complexe en intelligence structurée et exploitable.",
    valueLine: "Un compte. Un système de crédits. Plusieurs agents IA spécialisés.",
    explore: "Découvrir les agents IA",
    pricing: "Plans et tarifs",
    blog: "Ressources",
    trustLine: "Un essai unique à 1 $ pour un agent IA par compte · Crédits unifiés · Plateforme IA conçue pour la confidentialité",
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
    ctaTitle: "Prêt à transformer vos documents en décisions ?",
    ctaDesc: "Commencez avec le workflow IA spécialisé dont vous avez besoin aujourd’hui, puis évoluez dans Runexa à votre rythme.",
    ctaButton: "Commencer",
    disclaimer: "Les analyses générées par l’IA peuvent contenir des erreurs. Vérifiez toujours les informations avant de prendre une décision.",
    faqTitle: "Questions fréquentes",
    agents: [
      ["Runexa Legal Agent", "Analyse complète des contrats avec évaluation des risques, détection des clauses sensibles, extraction des obligations, recommandations de négociation et aide à la décision avant signature.", "/legal-ai", "legal"],
      ["Runexa Finance Intelligence Agent", "Analyse intelligente des relevés bancaires avec cashflow, catégorisation des dépenses, détection des abonnements, opportunités d’économies, budgets, risques et coach financier IA.", "/finance-ai", "finance"],
      ["Runexa Study Workspace", "Transformez vos cours, PDF, documents Word ou scans en résumés, audio, cartes mentales, quiz, flashcards et plans de révision.", "/study-ai", "study"],
      ["Runexa Business Decision Intelligence", "Importez des fichiers CSV ou Excel et obtenez vos KPI, prévisions, risques, opportunités, graphiques et rapports exportables.", "/business-ai", "business"],
    ] as Agent[],
    faqItems: [
      ["Qu’est-ce que Runexa ?", "Runexa est une plateforme IA spécialisée pour les workflows juridiques, financiers, d’apprentissage et de décision d’entreprise."],
      ["Comment ça marche ?", "Importez un document ou des données, choisissez un agent, puis recevez une analyse structurée et des recommandations."],
      ["Runexa est-il sécurisé ?", "Runexa est conçu autour de workflows confidentiels, de l’isolation des données et de la suppression automatique après analyse."],
      ["Runexa remplace-t-il les professionnels ?", "Non. Runexa fournit une aide à la décision. Les décisions importantes doivent être vérifiées par des professionnels qualifiés."],
    ],
  },
  ar: {
    platform: "منصة Runexa للذكاء الاصطناعي",
    title: "حوّل مستنداتك إلى قرارات.\nذكاء اصطناعي متخصص للعمل الواقعي.",
    heroDesc: "يحلل وكلاء ذكاء اصطناعي متخصصون العقود والبيانات المالية والمواد التعليمية وبيانات الأعمال، ويحوّلون المعلومات المعقدة إلى ذكاء منظم وقابل للتنفيذ.",
    valueLine: "حساب واحد. نظام أرصدة واحد. عدة وكلاء ذكاء اصطناعي متخصصين.",
    explore: "اكتشف وكلاء Runexa",
    pricing: "الخطط والأسعار",
    blog: "المدونة",
    trustLine: "تجربة واحدة بقيمة 1 دولار لوكيل ذكاء اصطناعي واحد لكل حساب · أرصدة موحدة · منصة مصممة لحماية الخصوصية",
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
    ctaTitle: "هل أنت مستعد لتحويل مستنداتك إلى قرارات؟",
    ctaDesc: "ابدأ بسير العمل المتخصص الذي تحتاجه اليوم، ثم توسّع عبر Runexa عندما تكون مستعداً.",
    ctaButton: "ابدأ الآن",
    disclaimer: "التحليلات مدعومة بالذكاء الاصطناعي وقد تحتوي على أخطاء. يُرجى التحقق من النتائج قبل اتخاذ أي قرار.",
    faqTitle: "الأسئلة الشائعة",
    agents: [
      ["Runexa Legal Agent", "مراجعة العقود مع تقييم المخاطر، واكتشاف البنود الحساسة، واستخراج الالتزامات، وتوصيات التفاوض، وتوجيه عملي قبل التوقيع.", "/legal-ai", "legal"],
      ["Runexa Finance Intelligence Agent", "تحليل ذكي لكشوفات الحساب البنكية يشمل التدفق النقدي، وتصنيف المصروفات، واكتشاف الاشتراكات، وفرص التوفير، والميزانية، والمخاطر، والمدرب المالي الذكي.", "/finance-ai", "finance"],
      ["Runexa Study Workspace", "حوّل الدروس وملفات PDF وWord والمستندات الممسوحة ضوئياً إلى ملخصات ودروس صوتية وخرائط ذهنية واختبارات وبطاقات مراجعة وخطط دراسة.", "/study-ai", "study"],
      ["Runexa Business Decision Intelligence", "ارفع بيانات بصيغة CSV أو Excel للحصول على مؤشرات أداء وتوقعات ومخاطر وفرص ورسوم بيانية وتقارير قابلة للتصدير.", "/business-ai", "business"],
    ] as Agent[],
    faqItems: [
      ["ما هي Runexa؟", "Runexa هي منصة ذكاء اصطناعي متخصصة لسير العمل القانوني والمالي والتعليمي واتخاذ القرارات التجارية."],
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

                <p className="max-w-3xl text-base font-medium leading-7 text-slate-600 md:text-lg">{t.heroDesc}</p>
                <p className="max-w-3xl text-sm font-black text-slate-900 md:text-base">{t.valueLine}</p>

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
                      <p className="mt-1 text-sm font-semibold text-blue-100">{language === "fr" ? "Choisissez un agent IA et analysez un document réel. Un essai unique par compte." : language === "ar" ? "اختر وكيلاً واحداً وحلل مستنداً حقيقياً. تجربة واحدة لكل حساب." : "Choose one AI agent and analyze a real document. One-time trial per account."}</p>
                    </div>
                    <span className="text-2xl">→</span>
                  </div>
                </Link>

                <Link
                  href="/free-access"
                  className="block max-w-2xl rounded-3xl border border-slate-200 bg-white p-5 text-slate-900 shadow-sm transition-all duration-200 ease-out hover:-translate-y-1 hover:border-blue-200 hover:shadow-lg active:translate-y-0 active:scale-[0.99] focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <p className="text-base font-black">
                        {language === "fr"
                          ? "Vous préférez découvrir Runexa avant de payer ?"
                          : language === "ar"
                          ? "هل تفضل تجربة Runexa أولاً؟"
                          : "Prefer to try Runexa first?"}
                      </p>
                      <p className="mt-1 text-sm font-medium leading-6 text-slate-600">
                        {language === "fr"
                          ? "Demandez un accès d’évaluation offert. Aucun paiement requis. Les demandes sont examinées sous 24 heures."
                          : language === "ar"
                          ? "اطلب وصولاً مجانياً للتقييم. لا يتطلب أي دفع. تتم مراجعة الطلبات خلال 24 ساعة."
                          : "Request complimentary evaluation access. No payment required. Requests are reviewed within 24 hours."}
                      </p>
                      <p className="mt-3 text-sm font-bold text-blue-700">
                        {language === "fr"
                          ? "Demander un accès gratuit →"
                          : language === "ar"
                          ? "طلب وصول مجاني ←"
                          : "Request Free Access →"}
                      </p>
                    </div>
                    <BadgeCheck className="mt-1 h-6 w-6 shrink-0 text-blue-600" />
                  </div>
                </Link>

                <p className="rounded-2xl border border-blue-100 bg-white/85 px-5 py-4 text-sm font-semibold text-slate-700 shadow-sm">{t.trustLine}</p>
              </div>

              <div className="relative min-h-[420px] overflow-hidden sm:overflow-visible">
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
                  [Lock, language === "fr" ? "Les contenus clients ne servent jamais à entraîner des modèles IA publics" : language === "ar" ? "لا تُستخدم محتويات العملاء لتدريب نماذج الذكاء الاصطناعي العامة" : "Customer Content Never Used to Train Public AI Models", "left-2 bottom-8", "bg-blue-100 text-blue-700"],
                ].map(([Icon, label, pos, color]: any) => (
                  <div key={label} className={`absolute rounded-2xl border border-slate-100 bg-white/90 px-5 py-4 shadow-xl ${pos}`}>
                    <div className="flex items-center gap-3"><div className={`flex h-11 w-11 items-center justify-center rounded-2xl ${color}`}><Icon className="h-6 w-6" /></div><p className="text-sm font-black text-slate-900">{label}</p></div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <AgentsSection t={t} language={language} />
          <PricingSection language={language} />
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
      documentName: "SaaS_Agreement.docx",
      scoreLabel: "Overall Risk",
      scoreValue: "39/100",
      findingsLabel: "Key findings",
      findings: [
        "Risk score: 39/100",
        "1 high-risk clause detected",
        "5 medium-risk clauses found",
        "1 contradiction detected",
      ],
      recommendationLabel: "Decision recommendation",
      recommendation: "Review the highest-risk clauses and contradiction before signing.",
      footer: "Legal · Finance · Study · Business",
    },
    fr: {
      eyebrow: "Aperçu d’un rapport Runexa",
      status: "Analyse terminée",
      documentLabel: "Document",
      documentName: "Contrat_SaaS.docx",
      scoreLabel: "Risque global",
      scoreValue: "39/100",
      findingsLabel: "Insights clés",
      findings: [
        "Score de risque : 39/100",
        "1 clause à risque élevé détectée",
        "5 clauses à risque moyen trouvées",
        "1 contradiction détectée",
      ],
      recommendationLabel: "Recommandation de décision",
      recommendation: "Vérifier les clauses les plus sensibles et la contradiction avant signature.",
      footer: "Juridique · Finance · Étude · Business",
    },
    ar: {
      eyebrow: "تقرير Runexa الذكي",
      status: "اكتمل التحليل",
      documentLabel: "المستند",
      documentName: "عقد_SaaS.docx",
      scoreLabel: "مستوى المخاطر",
      scoreValue: "39/100",
      findingsLabel: "رؤى رئيسية",
      findings: [
        "تقييم المخاطر: 39/100",
        "تم اكتشاف بند واحد عالي المخاطر",
        "تم العثور على 5 بنود متوسطة المخاطر",
        "تم اكتشاف تناقض واحد",
      ],
      recommendationLabel: "توصية القرار",
      recommendation: "يُنصح بمراجعة البنود الأكثر حساسية والتناقض قبل التوقيع.",
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
  const copy = {
    en: {
      eyebrow: "Why Runexa",
      title: "Specialized workflows. Structured intelligence. Clearer decisions.",
      desc: "Runexa is built around purpose-designed AI workflows that turn documents and data into structured outputs you can review, understand, and act on.",
      items: [
        ["Specialized workflows", "Purpose-built experiences for Legal, Finance, Study, and Business — not a blank chat box."],
        ["Structured outputs", "Risk scores, financial signals, study assets, KPIs, forecasts, and reports organized for the task."],
        ["Evidence-based analysis", "Outputs are designed to stay connected to the information observed in the document or dataset."],
        ["One platform across domains", "Use one account and one unified credit system across multiple specialized AI agents."],
      ],
    },
    fr: {
      eyebrow: "Pourquoi Runexa",
      title: "Des workflows spécialisés. Une intelligence structurée. Des décisions plus claires.",
      desc: "Runexa repose sur des workflows IA conçus pour transformer documents et données en résultats structurés que vous pouvez examiner, comprendre et utiliser.",
      items: [
        ["Workflows spécialisés", "Des expériences conçues pour le juridique, la finance, l’étude et le business — pas une simple page de chat."],
        ["Résultats structurés", "Scores de risque, signaux financiers, supports d’étude, KPI, prévisions et rapports organisés selon le besoin."],
        ["Analyse fondée sur les éléments observés", "Les résultats sont conçus pour rester reliés aux informations présentes dans le document ou les données analysées."],
        ["Une plateforme, plusieurs domaines", "Utilisez un compte et un système de crédits unifié avec plusieurs agents IA spécialisés."],
      ],
    },
    ar: {
      eyebrow: "لماذا Runexa",
      title: "سير عمل متخصص. ذكاء منظم. قرارات أوضح.",
      desc: "صُممت Runexa حول مسارات ذكاء اصطناعي متخصصة تحوّل المستندات والبيانات إلى نتائج منظمة يمكنك مراجعتها وفهمها واستخدامها.",
      items: [
        ["سير عمل متخصص", "تجارب مصممة للمجالات القانونية والمالية والتعليمية والأعمال — وليست مجرد نافذة محادثة."],
        ["نتائج منظمة", "درجات مخاطر وإشارات مالية وأدوات دراسة ومؤشرات أداء وتوقعات وتقارير منظمة حسب المهمة."],
        ["تحليل قائم على الأدلة", "صُممت النتائج لتبقى مرتبطة بالمعلومات المرصودة في المستند أو مجموعة البيانات."],
        ["منصة واحدة لمجالات متعددة", "استخدم حساباً واحداً ونظام أرصدة موحداً عبر عدة وكلاء ذكاء اصطناعي متخصصين."],
      ],
    },
  };

  const t = copy[language] || copy.en;
  const icons = [BriefcaseBusiness, ClipboardList, FileCheck, Sparkles];

  return (
    <section className="rounded-[28px] border border-slate-200 bg-white p-6 text-left shadow-sm md:p-10">
      <p className="text-sm font-semibold text-blue-600">{t.eyebrow}</p>
      <h2 className="mt-3 max-w-4xl text-2xl font-bold text-slate-900 md:text-3xl">{t.title}</h2>
      <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-600 md:text-base md:leading-7">{t.desc}</p>

      <div className="mt-7 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {t.items.map(([title, desc], index) => {
          const Icon = icons[index];
          return (
            <div key={title} className="rounded-2xl border border-slate-200 bg-slate-50 p-5 transition-all duration-200 hover:-translate-y-0.5 hover:border-blue-200 hover:bg-white hover:shadow-md">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-50 text-blue-700">
                <Icon className="h-5 w-5" />
              </div>
              <h3 className="mt-4 font-bold text-slate-900">{title}</h3>
              <p className="mt-2 text-sm leading-6 text-slate-600">{desc}</p>
            </div>
          );
        })}
      </div>
    </section>
  );
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
  const agentPreviews: Record<
    Locale,
    Record<
      AgentKey,
      {
        file: string;
        rows: Array<{ icon: any; label: string; value?: string }>;
        illustrativeLabel?: string;
        outcome: string;
        cta: string;
      }
    >
  > = {
    en: {
      legal: {
        illustrativeLabel: "Illustrative contract",
        file: "SaaS_Agreement.docx",
        rows: [
          { icon: ShieldCheck, label: "Risk score", value: "39/100" },
          { icon: AlertTriangle, label: "High-risk clauses", value: "1" },
          { icon: FileCheck, label: "Medium-risk clauses", value: "5" },
          { icon: Activity, label: "Contradictions", value: "1" },
        ],
        outcome: "Review the clauses that deserve attention before signing.",
        cta: "Open Legal Agent",
      },
      finance: {
        file: "Bank_Statement.pdf",
        rows: [
          { icon: ShieldCheck, label: "Financial score", value: "78" },
          { icon: TrendingUp, label: "Monthly income", value: "€20,393" },
          { icon: CreditCard, label: "Expenses", value: "€15,481.28" },
          { icon: PiggyBank, label: "Savings balance", value: "€4,911.12" },
        ],
        outcome: "See where your money goes and what to improve.",
        cta: "Open Finance Intelligence",
      },
      study: {
        file: "Study_Material.pdf",
        rows: [
          { icon: FileText, label: "AI summary" },
          { icon: ClipboardList, label: "Flashcards" },
          { icon: CheckCircle2, label: "Quiz questions" },
          { icon: CalendarCheck, label: "Study plan" },
        ],
        outcome: "Turn one document into a complete study workspace.",
        cta: "Open Study Workspace",
      },
      business: {
        file: "Sales_Report.xlsx",
        rows: [
          { icon: TrendingUp, label: "Revenue", value: "$129,510.85" },
          { icon: Activity, label: "Business score", value: "47/100" },
          { icon: BarChart3, label: "Profit margin", value: "52.75%" },
          { icon: FileSpreadsheet, label: "Priority decision" },
        ],
        outcome: "See what changed, why it matters, and what to examine next.",
        cta: "Open Business Intelligence",
      },
    },
    fr: {
      legal: {
        illustrativeLabel: "Exemple de contrat",
        file: "Contrat_SaaS.docx",
        rows: [
          { icon: ShieldCheck, label: "Score de risque", value: "39/100" },
          { icon: AlertTriangle, label: "Clauses à risque élevé", value: "1" },
          { icon: FileCheck, label: "Clauses à risque moyen", value: "5" },
          { icon: Activity, label: "Contradictions", value: "1" },
        ],
        outcome: "Identifiez les clauses qui méritent votre attention avant de signer.",
        cta: "Accéder à l’agent juridique",
      },
      finance: {
        file: "Releve_Bancaire.pdf",
        rows: [
          { icon: ShieldCheck, label: "Score financier", value: "78/100" },
          { icon: TrendingUp, label: "Revenus mensuels", value: "20 393 €" },
          { icon: CreditCard, label: "Dépenses", value: "15 481,28 €" },
          { icon: PiggyBank, label: "Solde épargne", value: "4 911,12 €" },
        ],
        outcome: "Voyez où va votre argent et ce que vous pouvez améliorer.",
        cta: "Accéder à Finance Intelligence",
      },
      study: {
        file: "Support_Cours.pdf",
        rows: [
          { icon: FileText, label: "Résumé IA" },
          { icon: ClipboardList, label: "Flashcards" },
          { icon: CheckCircle2, label: "Questions de quiz" },
          { icon: CalendarCheck, label: "Plan de révision" },
        ],
        outcome: "Transformez un document en espace d’apprentissage complet.",
        cta: "Accéder à Study Workspace",
      },
      business: {
        file: "Rapport_Ventes.xlsx",
        rows: [
          { icon: TrendingUp, label: "Revenus", value: "129 510,85 $" },
          { icon: Activity, label: "Score business", value: "47/100" },
          { icon: BarChart3, label: "Marge", value: "52,75 %" },
          { icon: FileSpreadsheet, label: "Recommandation stratégique" },
        ],
        outcome: "Voyez ce qui change, pourquoi cela compte et quoi examiner ensuite.",
        cta: "Accéder à Business Decision Intelligence",
      },
    },
    ar: {
      legal: {
        illustrativeLabel: "عقد توضيحي",
        file: "عقد_SaaS.docx",
        rows: [
          { icon: ShieldCheck, label: "تقييم المخاطر", value: "39/100" },
          { icon: AlertTriangle, label: "بنود عالية المخاطر", value: "1" },
          { icon: FileCheck, label: "بنود متوسطة المخاطر", value: "5" },
          { icon: Activity, label: "تناقضات", value: "1" },
        ],
        outcome: "حدد البنود التي تستحق انتباهك قبل التوقيع.",
        cta: "فتح الوكيل القانوني",
      },
      finance: {
        file: "كشف_حساب.pdf",
        rows: [
          { icon: ShieldCheck, label: "الدرجة المالية", value: "78" },
          { icon: TrendingUp, label: "الدخل الشهري", value: "€20,393" },
          { icon: CreditCard, label: "المصاريف", value: "€15,481.28" },
          { icon: PiggyBank, label: "رصيد الادخار", value: "€4,911.12" },
        ],
        outcome: "اعرف أين تذهب أموالك وما الذي يمكنك تحسينه.",
        cta: "فتح وكيل الذكاء المالي",
      },
      study: {
        file: "مادة_دراسية.pdf",
        rows: [
          { icon: FileText, label: "ملخص ذكي" },
          { icon: ClipboardList, label: "بطاقات مراجعة" },
          { icon: CheckCircle2, label: "أسئلة اختبار" },
          { icon: CalendarCheck, label: "خطة مراجعة" },
        ],
        outcome: "حوّل مستنداً واحداً إلى مساحة دراسة متكاملة.",
        cta: "فتح مساحة الدراسة",
      },
      business: {
        file: "تقرير_المبيعات.xlsx",
        rows: [
          { icon: TrendingUp, label: "الإيرادات", value: "$129,510.85" },
          { icon: Activity, label: "مؤشر صحة الأعمال", value: "47/100" },
          { icon: BarChart3, label: "هامش الربح", value: "52.75%" },
          { icon: FileSpreadsheet, label: "توصية استراتيجية" },
        ],
        outcome: "اعرف ما الذي تغيّر ولماذا يهم وما الذي ينبغي فحصه بعد ذلك.",
        cta: "فتح ذكاء قرارات الأعمال",
      },
    },
  };

  const previews = agentPreviews[language] || agentPreviews.en;

  const studyDemoHref =
    language === "fr"
      ? "/fr/demo/study-agent"
      : language === "ar"
      ? "/ar/demo/study-agent"
      : "/en/demo/study-agent";

  const studyDemoLabel =
    language === "fr"
      ? "Voir la démo"
      : language === "ar"
      ? "شاهد العرض"
      : "Watch demo";

  return <section id="agents" className="scroll-mt-24 rounded-[32px] border border-slate-200/80 bg-white/80 p-6 shadow-[0_20px_80px_rgba(15,23,42,0.08)] backdrop-blur-xl md:p-10">
    <div className="mb-8 flex justify-center"><div className="inline-flex items-center gap-2 rounded-full border border-blue-200 bg-blue-50 px-5 py-2 text-sm font-semibold text-blue-700"><Users className="h-4 w-4" />{language === "fr" ? "Agents IA spécialisés" : language === "ar" ? "وكلاء ذكاء اصطناعي متخصصون" : "Specialized AI Agents"}</div></div>
    <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
      {t.agents.map((agent: Agent) => {
        const style = agentStyles[agent[3]];
        const Icon = style.icon;
        const dark = agent[3] === "finance";
        const preview = previews[agent[3]];

        return (
          <div
            key={agent[0]}
            className={`group relative overflow-hidden rounded-3xl border p-5 shadow-lg transition-all duration-200 ease-out hover:-translate-y-1.5 hover:shadow-2xl ${style.card}`}
          >
            <Link
              href={agent[2]}
              className="block rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              <div className={`flex h-12 w-12 items-center justify-center rounded-2xl ${style.iconBox}`}>
                <Icon className={`h-6 w-6 ${style.iconColor}`} />
              </div>

              <h3 className={`mt-4 text-base font-bold ${dark ? "text-white" : "text-slate-900"}`}>
                {agent[0]}
              </h3>

              <div className={`mt-4 rounded-2xl border p-4 ${dark ? "border-white/15 bg-white/10" : "border-slate-200 bg-slate-50"}`}>
                {preview.illustrativeLabel && (
                  <p
                    className={`mb-3 text-[11px] font-black uppercase tracking-wide ${
                      dark ? "text-emerald-50" : "text-blue-700"
                    }`}
                  >
                    {preview.illustrativeLabel}
                  </p>
                )}

                <div className="flex items-center gap-2">
                  {agent[3] === "business" ? (
                    <FileSpreadsheet className={`h-4 w-4 ${dark ? "text-emerald-50" : "text-slate-500"}`} />
                  ) : (
                    <FileText className={`h-4 w-4 ${dark ? "text-emerald-50" : "text-slate-500"}`} />
                  )}

                  <p className={`truncate text-xs font-bold ${dark ? "text-emerald-50" : "text-slate-700"}`}>
                    {preview.file}
                  </p>
                </div>

                <div className={`my-3 h-px ${dark ? "bg-white/15" : "bg-slate-200"}`} />

                <div className="space-y-2.5">
                  {preview.rows.map((row) => {
                    const RowIcon = row.icon;

                    return (
                      <div key={row.label} className="flex items-center justify-between gap-3">
                        <div className="flex min-w-0 items-center gap-2">
                          <RowIcon className={`h-4 w-4 shrink-0 ${dark ? "text-emerald-50" : "text-blue-600"}`} />
                          <span className={`truncate text-xs font-semibold ${dark ? "text-emerald-50" : "text-slate-700"}`}>
                            {row.label}
                          </span>
                        </div>

                        {row.value && (
                          <span className={`shrink-0 text-xs font-black ${dark ? "text-white" : "text-slate-900"}`}>
                            {row.value}
                          </span>
                        )}
                      </div>
                    );
                  })}
                </div>

                <p
                  className={`mt-4 border-t pt-4 text-sm font-black leading-5 ${
                    dark
                      ? "border-white/15 text-white"
                      : agent[3] === "study"
                      ? "border-violet-100 text-violet-900"
                      : "border-slate-200 text-slate-900"
                  }`}
                >
                  {preview.outcome}
                </p>
              </div>

              <div className={`mt-5 inline-flex items-center gap-2 rounded-full px-3 py-1 text-xs font-bold ${style.badge}`}>
                {preview.cta} <span>→</span>
              </div>
            </Link>

            {agent[3] === "study" && (
              <div className="mt-4 border-t border-violet-100 pt-4">
                <Link
                  href={studyDemoHref}
                  className="inline-flex items-center gap-2 rounded-xl px-1 py-1 text-sm font-black text-violet-700 transition hover:text-violet-900 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:ring-offset-2"
                >
                  <span aria-hidden="true">▶</span>
                  <span>{studyDemoLabel}</span>
                </Link>
              </div>
            )}
          </div>
        );
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
  const copy = {
    en: {
      eyebrow: "Example outcomes",
      title: "See What Each Workflow Can Produce.",
      desc: "Illustrative examples of the structured outputs Runexa agents are designed to generate. Actual results depend on the document or data provided.",
      items: [
        {
          useCase: "Contract review",
          input: "Contract or agreement",
          output: "Risk scoring · Critical clauses · Obligations · Review priorities",
        },
        {
          useCase: "Bank statement analysis",
          input: "Bank statement",
          output: "Cashflow · Spending categories · Recurring activity · Savings signals",
        },
        {
          useCase: "Study preparation",
          input: "Course material",
          output: "Summary · Quiz · Flashcards · Study plan",
        },
      ],
    },
    fr: {
      eyebrow: "Exemples de résultats",
      title: "Découvrez ce que chaque workflow peut produire.",
      desc: "Exemples illustratifs des résultats structurés que les agents Runexa sont conçus pour générer. Les résultats réels dépendent du document ou des données fournis.",
      items: [
        {
          useCase: "Analyse de contrat",
          input: "Contrat ou accord",
          output: "Score de risque · Clauses critiques · Obligations · Priorités de revue",
        },
        {
          useCase: "Analyse de relevé bancaire",
          input: "Relevé bancaire",
          output: "Cashflow · Catégories de dépenses · Activité récurrente · Signaux d’économies",
        },
        {
          useCase: "Préparation des révisions",
          input: "Support de cours",
          output: "Résumé · Quiz · Flashcards · Plan de révision",
        },
      ],
    },
    ar: {
      eyebrow: "أمثلة على النتائج",
      title: "اكتشف ما يمكن أن ينتجه كل سير عمل.",
      desc: "أمثلة توضيحية للنتائج المنظمة التي صُممت وكلاء Runexa لإنتاجها. تعتمد النتائج الفعلية على المستند أو البيانات المقدمة.",
      items: [
        {
          useCase: "مراجعة العقود",
          input: "عقد أو اتفاقية",
          output: "تقييم المخاطر · البنود المهمة · الالتزامات · أولويات المراجعة",
        },
        {
          useCase: "تحليل كشف بنكي",
          input: "كشف حساب بنكي",
          output: "التدفق النقدي · فئات الإنفاق · النشاط المتكرر · مؤشرات التوفير",
        },
        {
          useCase: "التحضير للدراسة",
          input: "مادة دراسية",
          output: "ملخص · اختبار · بطاقات مراجعة · خطة دراسة",
        },
      ],
    },
  };

  const t = copy[language] || copy.en;

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-8 text-left shadow-sm md:p-12">
      <p className="text-sm font-semibold text-blue-600">{t.eyebrow}</p>
      <h2 className="mt-3 text-3xl font-bold text-slate-900">{t.title}</h2>
      <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-600 md:text-base">{t.desc}</p>

      <div className="mt-8 grid gap-5 md:grid-cols-3">
        {t.items.map((item) => (
          <div
            key={item.useCase}
            className="rounded-3xl border border-slate-200 bg-slate-50 p-6 transition-all duration-200 hover:-translate-y-1 hover:border-blue-200 hover:bg-white hover:shadow-lg"
          >
            <p className="text-xs font-bold uppercase tracking-wide text-blue-600">{item.useCase}</p>
            <div className="mt-5 flex items-start gap-3">
              <FileText className="mt-0.5 h-5 w-5 shrink-0 text-slate-400" />
              <div>
                <p className="text-xs font-semibold text-slate-500">
                  {language === "fr" ? "Entrée type" : language === "ar" ? "مثال على المدخل" : "Example input"}
                </p>
                <p className="mt-1 text-sm font-bold text-slate-900">{item.input}</p>
              </div>
            </div>
            <div className="mt-5 rounded-2xl border border-blue-100 bg-white p-4">
              <p className="text-xs font-semibold text-slate-500">
                {language === "fr" ? "Résultats structurés" : language === "ar" ? "نتائج منظمة" : "Structured outputs"}
              </p>
              <p className="mt-2 text-sm font-semibold leading-6 text-slate-800">{item.output}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}


function PricingSection({ language }: { language: Locale }) {
  const copy: any = {
    en: { eyebrow: "One platform. Flexible access.", title: "Start for $1. Scale with Runexa.", desc: "Choose the access model that fits your workflow — from a one-time trial to unified credits, recurring Pro access, Enterprise workspaces, and API integration.", plans: [["$1 Trial","Try one Runexa AI agent once per account.","Low-friction start"],["Unified Credits","Buy credits once and use the same balance across Legal, Finance, Study, and Business.","Pay as you go"],["Runexa Pro","Recurring access across every Runexa agent with monthly credits and priority processing.","For regular users"],["Enterprise & API","Secure team workspaces, private workflows, integrations, and API access for organizations and developers.","For teams & products"]], cta: "Compare plans & pricing" },
    fr: { eyebrow: "Une plateforme. Un accès flexible.", title: "Commencez à 1 $. Évoluez avec Runexa.", desc: "Choisissez le modèle adapté à votre usage : essai unique, crédits unifiés, accès Pro récurrent, espaces Enterprise ou intégration API.", plans: [["Essai à 1 $","Essayez une fois un agent IA Runexa par compte.","Pour commencer simplement"],["Crédits unifiés","Achetez des crédits et utilisez le même solde sur Legal, Finance, Study et Business.","Paiement à l’usage"],["Runexa Pro","Accès récurrent à tous les agents Runexa avec crédits mensuels et traitement prioritaire.","Pour les utilisateurs réguliers"],["Enterprise & API","Espaces sécurisés, workflows privés, intégrations et API pour organisations et développeurs.","Pour les équipes et produits"]], cta: "Comparer les plans et tarifs" },
    ar: { eyebrow: "منصة واحدة. وصول مرن.", title: "ابدأ بدولار واحد. وتوسع مع Runexa.", desc: "اختر نموذج الوصول المناسب لاستخدامك: تجربة لمرة واحدة، أرصدة موحدة، وصول Pro متجدد، مساحات Enterprise أو تكامل عبر API.", plans: [["تجربة بدولار واحد","جرّب وكيل Runexa واحداً مرة واحدة لكل حساب.","بداية سهلة"],["أرصدة موحدة","اشترِ الأرصدة واستخدم الرصيد نفسه عبر Legal وFinance وStudy وBusiness.","الدفع حسب الاستخدام"],["Runexa Pro","وصول متجدد إلى جميع وكلاء Runexa مع أرصدة شهرية ومعالجة ذات أولوية.","للاستخدام المنتظم"],["Enterprise وAPI","مساحات عمل آمنة وسير عمل خاص وتكاملات وواجهات API للمؤسسات والمطورين.","للفرق والمنتجات"]], cta: "مقارنة الخطط والأسعار" },
  };
  const t = copy[language] || copy.en;
  return <section className="rounded-3xl border border-slate-200 bg-white p-8 text-left shadow-sm md:p-12">
    <p className="text-sm font-semibold text-blue-600">{t.eyebrow}</p>
    <h2 className="mt-3 text-3xl font-bold text-slate-900">{t.title}</h2>
    <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-600 md:text-base">{t.desc}</p>
    <div className="mt-6 grid gap-4 md:grid-cols-2 lg:grid-cols-4">{t.plans.map(([plan, desc, tag]: string[]) => <div key={plan} className="rounded-2xl border border-slate-200 bg-slate-50 p-5 transition-all duration-200 hover:-translate-y-0.5 hover:border-blue-200 hover:bg-white hover:shadow-md"><p className="text-xs font-bold uppercase tracking-wide text-blue-600">{tag}</p><p className="mt-2 text-xl font-black text-slate-900">{plan}</p><p className="mt-2 text-sm leading-6 text-slate-600">{desc}</p><CheckCircle2 className="mt-4 h-5 w-5 text-blue-600" /></div>)}</div>
    <Link href="/pricing" className="mt-6 inline-flex rounded-2xl bg-blue-600 px-6 py-3 text-sm font-bold text-white transition-all duration-200 ease-out hover:-translate-y-1 hover:bg-blue-700 hover:shadow-lg active:translate-y-0 active:scale-[0.98] focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">{t.cta}</Link>

    <div className="mt-5 text-sm text-slate-600">
      {language === "fr"
        ? "Pas encore prêt à acheter ? "
        : language === "ar"
        ? "لست مستعداً للشراء بعد؟ "
        : "Not ready to purchase? "}
      <Link href="/free-access" className="font-bold text-blue-700 hover:text-blue-800">
        {language === "fr"
          ? "Demandez un accès d’évaluation offert."
          : language === "ar"
          ? "اطلب وصولاً مجانياً للتقييم."
          : "Request complimentary evaluation access."}
      </Link>
    </div>
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
