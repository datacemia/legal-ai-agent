export const defaultLocale = "en";

export const locales = ["en", "fr", "ar"];

export function getSavedLocale() {
  if (typeof window === "undefined") return defaultLocale;

  const saved = localStorage.getItem("locale");

  if (saved && locales.includes(saved)) {
    return saved;
  }

  return defaultLocale;
}

export function setSavedLocale(locale: string) {
  if (!locales.includes(locale)) return;

  localStorage.setItem("locale", locale);
  window.dispatchEvent(new Event("locale-change"));
}

export const translations: any = {
  en: {
    slogan: "AI agents that get things done",
    dashboard: "Dashboard",
    admin: "Admin",
    pricing: "Pricing",
    logout: "Logout",
    login: "Login",
    register: "Register",

    footerDesc:
      "AI agents for legal analysis, learning, personal finance, and business decision-making.",

    companyAddress:
      "Runexa Systems LLC\n1309 Coffeen Avenue, Suite 1200\nSheridan, WY 82801, USA",

    products: "Products",
    legalAgent: "Legal Agent",
    studyAgent: "Study Agent",
    financeAgent: "Personal Finance Coach Agent",
    hrAgent: "HR Agent",
    businessAgent: "Business Decision Agent",
    available: "Available",
    comingSoon: "Coming soon",

    platform: "Platform",
    exploreAgents: "Explore agents",
    tryLegalAgent: "Try Legal Agent",
    tryStudyAgent: "Try Study Agent",
    tryFinanceAgent: "Try Finance Coach",

    about: "About",
    aboutText:
      "Runexa Systems is a platform of AI agents that help users analyze documents, learn faster, manage personal finance, and make smarter business decisions.",

    developedBy: "Developed by Dr. Rachid Ejjami",
    copyright: "© 2026 Runexa Systems LLC. All rights reserved.",

    privacy: "Privacy Policy",
    terms: "Terms of Service",
    contact: "Contact",
  },

  fr: {
    slogan: "Des agents IA qui vous aident à avancer",
    dashboard: "Tableau de bord",
    admin: "Admin",
    pricing: "Tarifs",
    logout: "Déconnexion",
    login: "Connexion",
    register: "Inscription",

    footerDesc:
      "Agents IA pour l’analyse juridique, l’apprentissage, la gestion financière personnelle et la prise de décision business.",

    companyAddress:
      "Runexa Systems LLC\n1309 Coffeen Avenue, Suite 1200\nSheridan, WY 82801, États-Unis",

    products: "Produits",
    legalAgent: "Agent juridique",
    studyAgent: "Agent étude",
    financeAgent: "Agent coach financier personnel",
    hrAgent: "Agent RH",
    businessAgent: "Agent décision business",
    available: "Disponible",
    comingSoon: "Bientôt",
    

    platform: "Plateforme",
    exploreAgents: "Explorer les agents",
    tryLegalAgent: "Tester l’agent juridique",
    tryStudyAgent: "Tester l’agent étude",
    tryFinanceAgent: "Tester le coach financier",

    about: "À propos",
    aboutText:
      "Runexa Systems est une plateforme d’agents IA qui aide les utilisateurs à analyser leurs documents, apprendre plus vite, gérer leurs finances personnelles et prendre de meilleures décisions business.",

    developedBy: "Développé par Dr. Rachid Ejjami",
    copyright: "© 2026 Runexa Systems LLC. Tous droits réservés.",

    privacy: "Confidentialité",
    terms: "Conditions",
    contact: "Contact",
  },

  ar: {
    slogan: "وكلاء ذكاء اصطناعي يساعدونك على إنجاز العمل",
    dashboard: "لوحة التحكم",
    admin: "الإدارة",
    pricing: "الأسعار",
    logout: "تسجيل الخروج",
    login: "تسجيل الدخول",
    register: "إنشاء حساب",

    footerDesc:
      "وكلاء ذكاء اصطناعي للتحليل القانوني والتعلم والإدارة المالية الشخصية واتخاذ قرارات الأعمال.",

    companyAddress:
      "Runexa Systems LLC\n1309 Coffeen Avenue, Suite 1200\nSheridan, WY 82801, الولايات المتحدة",

    products: "المنتجات",
    legalAgent: "الوكيل القانوني",
    studyAgent: "وكيل الدراسة",
    financeAgent: "وكيل الإدارة المالية الشخصية",
    hrAgent: "وكيل الموارد البشرية",
    businessAgent: "وكيل قرارات الأعمال",
    available: "متاح",
    comingSoon: "قريباً",

    platform: "المنصة",
    exploreAgents: "استكشاف الوكلاء",
    tryLegalAgent: "تجربة الوكيل القانوني",
    tryStudyAgent: "تجربة وكيل الدراسة",
    tryFinanceAgent: "تجربة وكيل الإدارة المالية",

    about: "حول",
    aboutText:
      "Runexa Systems منصة لوكلاء ذكاء اصطناعي تساعد المستخدمين على تحليل المستندات والتعلم بشكل أسرع وإدارة المالية الشخصية واتخاذ قرارات أعمال أكثر ذكاءً.",

    developedBy: "تم التطوير بواسطة Dr. Rachid Ejjami",
    copyright: "© 2026 Runexa Systems LLC. جميع الحقوق محفوظة.",

    privacy: "الخصوصية",
    terms: "الشروط",
    contact: "اتصال",
  },
};