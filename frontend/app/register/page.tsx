"use client";

import { useEffect, useState } from "react";
import { trackEvent } from "../../lib/track";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

const labels: any = {
  en: {
    badge: "AI agents that get things done",
    leftTitle: "Create one Runexa account for all AI agents",
    leftDescription:
      "Create one Runexa account for all AI agents. Start with a $1 trial per agent, then continue with global credits or a plan. Runexa supports legal, study, finance, business, and future security agents.",
    featureAgentsTitle: "Specialized AI Agents",
    featureAgentsDesc:
      "Access powerful agents built for your business needs.",
    featureSecurityTitle: "Secure & Private",
    featureSecurityDesc:
      "Your data is protected with enterprise-grade security.",
    featureProductivityTitle: "Save Time, Get More Done",
    featureProductivityDesc:
      "Automate complex tasks and focus on what matters most.",

    title: "Create your account",
    subtitle:
      "Start with a $1 trial per agent, then continue with global credits or a plan.",
    emailPlaceholder: "you@example.com",
    passwordPlaceholder: "Create a strong password",
    createAccount: "Create account",
    alreadyHaveAccount: "Already have an account?",
    login: "Log in",

    enterEmailPassword: "Please enter email and password",
    accountCreated:
      "Account created. Please check your email to verify your account.",
    registrationFailed: "Registration failed",
    serverError: "Error connecting to server",

    passwordRules: [
      "At least 12 characters",
      "One uppercase letter",
      "One lowercase letter",
      "One number",
      "One special character",
    ],
  },

  fr: {
    badge: "Des agents IA pour avancer plus vite",
    leftTitle: "Un seul compte Runexa pour tous vos agents IA",
    leftDescription:
      "Créez un seul compte Runexa pour accéder à tous les agents IA. Commencez avec un essai à 1 $ par agent, puis continuez avec des crédits globaux ou un abonnement. Runexa prend en charge les agents juridique, étude, finance, business et les futurs agents sécurité.",
    featureAgentsTitle: "Agents IA spécialisés",
    featureAgentsDesc:
      "Accédez à des agents puissants conçus pour vos besoins métier.",
    featureSecurityTitle: "Sécurisé et confidentiel",
    featureSecurityDesc:
      "Vos données sont protégées avec une sécurité de niveau entreprise.",
    featureProductivityTitle: "Gagnez du temps, avancez plus vite",
    featureProductivityDesc:
      "Automatisez les tâches complexes et concentrez-vous sur l’essentiel.",

    title: "Créer votre compte",
    subtitle:
      "Commencez avec un essai à 1 $ par agent, puis continuez avec des crédits globaux ou un abonnement.",
    emailPlaceholder: "vous@exemple.com",
    passwordPlaceholder: "Créez un mot de passe sécurisé",
    createAccount: "Créer un compte",
    alreadyHaveAccount: "Vous avez déjà un compte ?",
    login: "Se connecter",

    enterEmailPassword: "Veuillez entrer votre e-mail et votre mot de passe",
    accountCreated:
      "Compte créé. Veuillez vérifier votre e-mail pour activer votre compte.",
    registrationFailed: "Échec de l’inscription",
    serverError: "Erreur de connexion au serveur",

    passwordRules: [
      "Au moins 12 caractères",
      "Une lettre majuscule",
      "Une lettre minuscule",
      "Un chiffre",
      "Un caractère spécial",
    ],
  },

  ar: {
    badge: "وكلاء ذكاء اصطناعي يساعدونك على الإنجاز",
    leftTitle: "حساب Runexa واحد لجميع وكلاء الذكاء الاصطناعي",
    leftDescription:
      "أنشئ حساب Runexa واحدًا للوصول إلى جميع وكلاء الذكاء الاصطناعي. ابدأ بتجربة بقيمة 1 دولار لكل وكيل، ثم تابع باستخدام الأرصدة العامة أو الاشتراك. يدعم Runexa الوكلاء القانونيين، الدراسة، المالية، الأعمال، ووكلاء الأمان المستقبليين.",
    featureAgentsTitle: "وكلاء ذكاء اصطناعي متخصصون",
    featureAgentsDesc:
      "استخدم وكلاء أقوياء مصممين لاحتياجات عملك.",
    featureSecurityTitle: "آمن وخاص",
    featureSecurityDesc:
      "بياناتك محمية بأمان من مستوى المؤسسات.",
    featureProductivityTitle: "وفّر الوقت وأنجز أكثر",
    featureProductivityDesc:
      "أتمت المهام المعقدة وركّز على ما يهم.",

    title: "إنشاء حسابك",
    subtitle:
      "ابدأ بتجربة بقيمة 1 دولار لكل وكيل، ثم تابع باستخدام الأرصدة العامة أو الاشتراك.",
    emailPlaceholder: "you@example.com",
    passwordPlaceholder: "أنشئ كلمة مرور قوية",
    createAccount: "إنشاء حساب",
    alreadyHaveAccount: "لديك حساب بالفعل؟",
    login: "تسجيل الدخول",

    enterEmailPassword: "يرجى إدخال البريد الإلكتروني وكلمة المرور",
    accountCreated:
      "تم إنشاء الحساب. يرجى التحقق من بريدك الإلكتروني لتفعيل الحساب.",
    registrationFailed: "فشل إنشاء الحساب",
    serverError: "خطأ في الاتصال بالخادم",

    passwordRules: [
      "12 حرفًا على الأقل",
      "حرف كبير واحد",
      "حرف صغير واحد",
      "رقم واحد",
      "رمز خاص واحد",
    ],
  },
};

export default function RegisterPage() {
  const [language, setLanguage] = useState("en");
  const t = labels[language] || labels.en;

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState<"success" | "error">("success");

  useEffect(() => {
    const saved = localStorage.getItem("locale");

    if (saved && labels[saved]) {
      setLanguage(saved);
    }

    const handleLocaleChange = () => {
      const nextLocale = localStorage.getItem("locale");

      if (nextLocale && labels[nextLocale]) {
        setLanguage(nextLocale);
      }
    };

    window.addEventListener("locale-change", handleLocaleChange);

    return () => {
      window.removeEventListener("locale-change", handleLocaleChange);
    };
  }, []);

  const isValid =
    password.length >= 12 &&
    /[A-Z]/.test(password) &&
    /[a-z]/.test(password) &&
    /\d/.test(password) &&
    /[!@#$%^&*(),.?":{}|<>]/.test(password);

  const passwordRules = [
    { label: t.passwordRules[0], valid: password.length >= 12 },
    { label: t.passwordRules[1], valid: /[A-Z]/.test(password) },
    { label: t.passwordRules[2], valid: /[a-z]/.test(password) },
    { label: t.passwordRules[3], valid: /\d/.test(password) },
    {
      label: t.passwordRules[4],
      valid: /[!@#$%^&*(),.?":{}|<>]/.test(password),
    },
  ];

  const handleRegister = async () => {
    try {
      if (!email.trim() || !password) {
        setMessageType("error");
        setMessage(t.enterEmailPassword);
        return;
      }

      const res = await fetch(`${API_URL}/auth/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email.trim(),
          password,
        }),
      });

      const data = await res.json();

      if (res.ok) {
        trackEvent("register");

        if (data.access_token) {
          localStorage.setItem("token", data.access_token);

          localStorage.setItem(
            "credits_balance",
            String(data.user?.credits_balance || 0)
          );

          localStorage.setItem(
            "plan",
            data.user?.plan || "trial"
          );

          localStorage.setItem(
            "role",
            data.user?.role || "user"
          );
        }

        setMessageType("success");
        setMessage(t.accountCreated);

        setTimeout(() => {
          window.location.href = "/login";
        }, 1500);
      } else {
        setMessageType("error");
        setMessage(data.detail || t.registrationFailed);
      }
    } catch (err) {
      console.error(err);
      setMessageType("error");
      setMessage(t.serverError);
    }
  };

  return (
    <main
      dir={language === "ar" ? "rtl" : "ltr"}
      className="min-h-screen bg-white text-slate-950"
    >
      <div className="grid min-h-screen grid-cols-1 lg:grid-cols-2">
        {/* LEFT */}
        <section className="relative hidden overflow-hidden bg-gradient-to-br from-blue-50 via-white to-indigo-50 px-10 py-12 lg:flex lg:flex-col lg:justify-center xl:px-20">
          <div className="max-w-xl">
            <span className="inline-flex rounded-full bg-blue-100 px-4 py-2 text-sm font-medium text-blue-700">
              {t.badge}
            </span>

            <h1 className="mt-8 text-4xl font-bold text-slate-950 xl:text-5xl">
              {t.leftTitle}
            </h1>

            <p className="mt-6 text-lg text-slate-600">
              {t.leftDescription}
            </p>

            <div className="mt-12 space-y-7">
              <div className="flex gap-5">
                <div className="h-12 w-12 flex items-center justify-center rounded-2xl bg-blue-100 text-blue-700">
                  ⚡
                </div>
                <div>
                  <h3 className="font-semibold">{t.featureAgentsTitle}</h3>
                  <p className="text-slate-600">
                    {t.featureAgentsDesc}
                  </p>
                </div>
              </div>

              <div className="flex gap-5">
                <div className="h-12 w-12 flex items-center justify-center rounded-2xl bg-blue-100 text-blue-700">
                  🛡️
                </div>
                <div>
                  <h3 className="font-semibold">{t.featureSecurityTitle}</h3>
                  <p className="text-slate-600">
                    {t.featureSecurityDesc}
                  </p>
                </div>
              </div>

              <div className="flex gap-5">
                <div className="h-12 w-12 flex items-center justify-center rounded-2xl bg-blue-100 text-blue-700">
                  📈
                </div>
                <div>
                  <h3 className="font-semibold">
                    {t.featureProductivityTitle}
                  </h3>
                  <p className="text-slate-600">
                    {t.featureProductivityDesc}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* RIGHT */}
        <section className="flex items-center justify-center bg-slate-50 px-4 py-10 lg:bg-white">
          <div className="w-full max-w-xl rounded-3xl border bg-white p-6 shadow-xl">
            <div className="text-center">
              <h1 className="text-3xl font-bold">{t.title}</h1>
              <p className="text-slate-500">
                {t.subtitle}
              </p>
            </div>

            {message && (
              <div
                className={`mt-5 rounded-xl border px-4 py-3 text-sm ${
                  messageType === "success"
                    ? "border-green-200 bg-green-50 text-green-700"
                    : "border-red-200 bg-red-50 text-red-700"
                }`}
              >
                {message}
              </div>
            )}

            <div className="space-y-5 mt-6">
              <input
                type="email"
                placeholder={t.emailPlaceholder}
                className="w-full border px-4 py-3 rounded-xl"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />

              <input
                type="password"
                placeholder={t.passwordPlaceholder}
                className="w-full border px-4 py-3 rounded-xl"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />

              <div className="text-sm space-y-1">
                {passwordRules.map((rule) => (
                  <p
                    key={rule.label}
                    className={
                      rule.valid
                        ? "text-green-600"
                        : "text-slate-500"
                    }
                  >
                    {rule.valid ? "✓" : "○"} {rule.label}
                  </p>
                ))}
              </div>

              <button
                onClick={handleRegister}
                disabled={!isValid}
                className="w-full bg-black text-white py-3 rounded-xl disabled:bg-gray-400"
              >
                {t.createAccount}
              </button>
            </div>

            <p className="mt-6 text-center text-sm">
              {t.alreadyHaveAccount}{" "}
              <a href="/login" className="text-blue-600">
                {t.login}
              </a>
            </p>
          </div>
        </section>
      </div>
    </main>
  );
}
