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
    logout: "Logout",
    login: "Login",
    register: "Register",

    footerDesc:
      "Specialized AI agents for legal, finance, HR, and business productivity.",
    products: "Products",
    legalAgent: "Legal Agent",
    financeAgent: "Finance Agent",
    hrAgent: "HR Agent",
    businessAgent: "Business Agent",
    available: "Available",
    comingSoon: "Coming soon",
    platform: "Platform",
    exploreAgents: "Explore agents",
    tryLegalAgent: "Try Legal Agent",
    about: "About",
    aboutText:
      "Runexa AI is a platform of specialized AI agents for legal, finance, HR, and business productivity.",
    developedBy: "Developed by Dr. Rachid Ejjami",
    copyright: "© 2025 Runexa AI. All rights reserved.",
    privacy: "Privacy Policy",
    terms: "Terms of Service",
    contact: "Contact",
  },

  fr: {
    slogan: "Des agents IA qui vous aident à avancer",
    dashboard: "Tableau de bord",
    admin: "Admin",
    logout: "Déconnexion",
    login: "Connexion",
    register: "Inscription",

    footerDesc:
      "Agents IA spécialisés pour le juridique, la finance, les RH et la productivité business.",
    products: "Produits",
    legalAgent: "Agent juridique",
    financeAgent: "Agent finance",
    hrAgent: "Agent RH",
    businessAgent: "Agent business",
    available: "Disponible",
    comingSoon: "Bientôt",
    platform: "Plateforme",
    exploreAgents: "Explorer les agents",
    tryLegalAgent: "Tester l’agent juridique",
    about: "À propos",
    aboutText:
      "Runexa AI est une plateforme d’agents IA spécialisés pour le juridique, la finance, les RH et la productivité business.",
    developedBy: "Développé par Dr. Rachid Ejjami",
    copyright: "© 2025 Runexa AI. Tous droits réservés.",
    privacy: "Confidentialité",
    terms: "Conditions",
    contact: "Contact",
  },

  ar: {
    slogan: "وكلاء ذكاء اصطناعي يساعدونك على إنجاز العمل",
    dashboard: "لوحة التحكم",
    admin: "الإدارة",
    logout: "تسجيل الخروج",
    login: "تسجيل الدخول",
    register: "إنشاء حساب",

    footerDesc:
      "وكلاء ذكاء اصطناعي متخصصون للقانون والمالية والموارد البشرية والأعمال.",
    products: "المنتجات",
    legalAgent: "الوكيل القانوني",
    financeAgent: "وكيل المالية",
    hrAgent: "وكيل الموارد البشرية",
    businessAgent: "وكيل الأعمال",
    available: "متاح",
    comingSoon: "قريباً",
    platform: "المنصة",
    exploreAgents: "استكشاف الوكلاء",
    tryLegalAgent: "تجربة الوكيل القانوني",
    about: "حول",
    aboutText:
      "Runexa AI منصة لوكلاء ذكاء اصطناعي متخصصين في القانون والمالية والموارد البشرية والأعمال.",
    developedBy: "تم التطوير بواسطة Dr. Rachid Ejjami",
    copyright: "© 2025 Runexa AI. جميع الحقوق محفوظة.",
    privacy: "الخصوصية",
    terms: "الشروط",
    contact: "اتصال",
  },
};