"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

const labels: any = {
  en: {
    badge: "AI agents that get things done",
    heroTitle: "Secure your account with a new password",
    heroDescription:
      "Choose a strong password to protect your account and keep your data safe.",
    featureSecurityTitle: "Stronger Security",
    featureSecurityDesc:
      "A strong password keeps your account and data protected.",
    featureExperienceTitle: "Better Experience",
    featureExperienceDesc:
      "Secure access means uninterrupted productivity with your AI agents.",
    featureControlTitle: "You’re in Control",
    featureControlDesc:
      "Update your password anytime to stay in control.",

    title: "Reset password",
    subtitle: "Enter your new password below.",
    newPassword: "New password",
    passwordPlaceholder: "Enter new password",
    passwordMustContain: "Password must contain:",
    resetPassword: "Reset password",
    backToLogin: "← Back to login",
    loading: "Loading...",

    invalidLink: "Invalid reset link.",
    passwordRequirements: "Password does not meet the requirements.",
    success: "Password updated successfully. Redirecting...",
    requestFailed: "Request failed",
    serverError: "Error connecting to server",

    rules: [
      "At least 12 characters",
      "One uppercase letter",
      "One lowercase letter",
      "One number",
      "One special character",
    ],
  },

  fr: {
    badge: "Des agents IA pour avancer plus vite",
    heroTitle: "Sécurisez votre compte avec un nouveau mot de passe",
    heroDescription:
      "Choisissez un mot de passe fort pour protéger votre compte et garder vos données en sécurité.",
    featureSecurityTitle: "Sécurité renforcée",
    featureSecurityDesc:
      "Un mot de passe fort protège votre compte et vos données.",
    featureExperienceTitle: "Meilleure expérience",
    featureExperienceDesc:
      "Un accès sécurisé vous permet de continuer à travailler sans interruption avec vos agents IA.",
    featureControlTitle: "Vous gardez le contrôle",
    featureControlDesc:
      "Vous pouvez mettre à jour votre mot de passe à tout moment.",

    title: "Réinitialiser le mot de passe",
    subtitle: "Entrez votre nouveau mot de passe ci-dessous.",
    newPassword: "Nouveau mot de passe",
    passwordPlaceholder: "Entrez le nouveau mot de passe",
    passwordMustContain: "Le mot de passe doit contenir :",
    resetPassword: "Réinitialiser le mot de passe",
    backToLogin: "← Retour à la connexion",
    loading: "Chargement...",

    invalidLink: "Lien de réinitialisation invalide.",
    passwordRequirements: "Le mot de passe ne respecte pas les exigences.",
    success: "Mot de passe mis à jour avec succès. Redirection...",
    requestFailed: "La requête a échoué",
    serverError: "Erreur de connexion au serveur",

    rules: [
      "Au moins 12 caractères",
      "Une lettre majuscule",
      "Une lettre minuscule",
      "Un chiffre",
      "Un caractère spécial",
    ],
  },

  ar: {
    badge: "وكلاء ذكاء اصطناعي يساعدونك على الإنجاز",
    heroTitle: "أمّن حسابك بكلمة مرور جديدة",
    heroDescription:
      "اختر كلمة مرور قوية لحماية حسابك والحفاظ على أمان بياناتك.",
    featureSecurityTitle: "أمان أقوى",
    featureSecurityDesc:
      "كلمة المرور القوية تساعد على حماية حسابك وبياناتك.",
    featureExperienceTitle: "تجربة أفضل",
    featureExperienceDesc:
      "الوصول الآمن يعني إنتاجية مستمرة مع وكلاء الذكاء الاصطناعي.",
    featureControlTitle: "أنت تتحكم في حسابك",
    featureControlDesc:
      "يمكنك تحديث كلمة المرور في أي وقت للحفاظ على التحكم بحسابك.",

    title: "إعادة تعيين كلمة المرور",
    subtitle: "أدخل كلمة المرور الجديدة أدناه.",
    newPassword: "كلمة المرور الجديدة",
    passwordPlaceholder: "أدخل كلمة المرور الجديدة",
    passwordMustContain: "يجب أن تحتوي كلمة المرور على:",
    resetPassword: "إعادة تعيين كلمة المرور",
    backToLogin: "← الرجوع إلى تسجيل الدخول",
    loading: "جاري التحميل...",

    invalidLink: "رابط إعادة التعيين غير صالح.",
    passwordRequirements: "كلمة المرور لا تستوفي المتطلبات.",
    success: "تم تحديث كلمة المرور بنجاح. جارٍ إعادة التوجيه...",
    requestFailed: "فشل الطلب",
    serverError: "خطأ في الاتصال بالخادم",

    rules: [
      "12 حرفًا على الأقل",
      "حرف كبير واحد",
      "حرف صغير واحد",
      "رقم واحد",
      "رمز خاص واحد",
    ],
  },
};

function ResetPasswordContent() {
  const params = useSearchParams();
  const token = params.get("token");
  const [language, setLanguage] = useState("en");
  const t = labels[language] || labels.en;

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
    { icon: "12+", label: t.rules[0], valid: password.length >= 12 },
    { icon: "Aa", label: t.rules[1], valid: /[A-Z]/.test(password) },
    { icon: "aa", label: t.rules[2], valid: /[a-z]/.test(password) },
    { icon: "1", label: t.rules[3], valid: /\d/.test(password) },
    {
      icon: "#",
      label: t.rules[4],
      valid: /[!@#$%^&*(),.?":{}|<>]/.test(password),
    },
  ];

  const handle = async () => {
    if (!token) {
      setMessageType("error");
      setMessage(t.invalidLink);
      return;
    }

    if (!isValid) {
      setMessageType("error");
      setMessage(t.passwordRequirements);
      return;
    }

    try {
      const res = await fetch(`${API_URL}/auth/reset-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token, password }),
      });

      const data = await res.json();

      if (res.ok) {
        setMessageType("success");
        setMessage(t.success);

        setTimeout(() => {
          window.location.href = "/login";
        }, 1500);

        return;
      }

      setMessageType("error");
      setMessage(data.detail || data.message || t.requestFailed);
    } catch (error) {
      console.error(error);
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
        <section className="relative hidden overflow-hidden bg-gradient-to-br from-blue-50 via-white to-indigo-50 px-10 py-12 lg:flex lg:flex-col lg:justify-center xl:px-20">
          <div className="max-w-xl">
            <span className="inline-flex rounded-full bg-blue-100 px-4 py-2 text-sm font-medium text-blue-700">
              {t.badge}
            </span>

            <h1 className="mt-8 text-4xl font-bold leading-tight tracking-tight text-slate-950 xl:text-5xl">
              {t.heroTitle}
            </h1>

            <p className="mt-6 text-lg leading-8 text-slate-600">
              {t.heroDescription}
            </p>

            <div className="mt-12 space-y-7">
              <div className="flex gap-5">
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-blue-100 text-xl text-blue-700">
                  🛡️
                </div>
                <div>
                  <h3 className="font-semibold text-slate-950">
                    {t.featureSecurityTitle}
                  </h3>
                  <p className="mt-1 text-slate-600">
                    {t.featureSecurityDesc}
                  </p>
                </div>
              </div>

              <div className="flex gap-5">
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-blue-100 text-xl text-blue-700">
                  ⚡
                </div>
                <div>
                  <h3 className="font-semibold text-slate-950">
                    {t.featureExperienceTitle}
                  </h3>
                  <p className="mt-1 text-slate-600">
                    {t.featureExperienceDesc}
                  </p>
                </div>
              </div>

              <div className="flex gap-5">
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-blue-100 text-xl text-blue-700">
                  ✅
                </div>
                <div>
                  <h3 className="font-semibold text-slate-950">
                    {t.featureControlTitle}
                  </h3>
                  <p className="mt-1 text-slate-600">
                    {t.featureControlDesc}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div className="pointer-events-none absolute -bottom-24 -left-24 h-72 w-[120%] rounded-[100%] border border-blue-300 opacity-40" />
          <div className="pointer-events-none absolute -bottom-36 -left-28 h-72 w-[120%] rounded-[100%] border border-indigo-300 opacity-30" />
          <div className="pointer-events-none absolute bottom-20 right-16 h-40 w-40 rounded-3xl bg-blue-200/40 blur-3xl" />
        </section>

        <section className="flex min-h-screen items-center justify-center bg-slate-50 px-4 py-10 sm:px-6 lg:bg-white lg:px-10">
          <div className="w-full max-w-xl rounded-3xl border border-slate-200 bg-white p-6 shadow-xl shadow-slate-200/70 sm:p-8 lg:p-10">
            <div className="text-center">
              <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-indigo-50 text-3xl text-blue-700">
                🔒
              </div>

              <h1 className="mt-6 text-3xl font-bold tracking-tight text-slate-950 sm:text-4xl">
                {t.title}
              </h1>

              <p className="mt-3 text-sm text-slate-500 sm:text-base">
                {t.subtitle}
              </p>
            </div>

            {message && (
              <div
                className={`mt-8 rounded-xl border p-4 text-sm ${
                  messageType === "success"
                    ? "border-green-200 bg-green-50 text-green-700"
                    : "border-red-200 bg-red-50 text-red-700"
                }`}
              >
                {message}
              </div>
            )}

            <div className="mt-8 space-y-5">
              <div>
                <label className="mb-2 block text-sm font-medium text-slate-700">
                  {t.newPassword}
                </label>
                <input
                  type="password"
                  placeholder={t.passwordPlaceholder}
                  className="w-full rounded-xl border border-slate-300 px-4 py-3 text-slate-950 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>

              <div className="rounded-2xl border border-slate-200 bg-slate-50 p-5 text-sm">
                <p className="mb-4 font-semibold text-slate-950">
                  {t.passwordMustContain}
                </p>

                <div className="space-y-3">
                  {passwordRules.map((rule) => (
                    <div
                      key={rule.label}
                      className={`flex items-center gap-3 ${
                        rule.valid ? "text-green-600" : "text-slate-500"
                      }`}
                    >
                      <span
                        className={`flex h-5 w-5 items-center justify-center rounded-full border text-xs ${
                          rule.valid
                            ? "border-green-500 bg-green-50"
                            : "border-slate-300 bg-white"
                        }`}
                      >
                        {rule.valid ? "✓" : ""}
                      </span>

                      <span className="w-8 text-xs font-semibold text-blue-600">
                        {rule.icon}
                      </span>

                      <span>{rule.label}</span>
                    </div>
                  ))}
                </div>
              </div>

              <button
                onClick={handle}
                disabled={!isValid}
                className={`w-full rounded-xl py-3 font-semibold text-white shadow-lg transition ${
                  isValid
                    ? "bg-slate-950 hover:bg-slate-800"
                    : "bg-slate-400 cursor-not-allowed"
                }`}
              >
                {t.resetPassword}
              </button>
            </div>

            <p className="mt-7 text-center text-sm">
              <a
                href="/login"
                className="font-medium text-blue-600 hover:text-blue-700"
              >
                {t.backToLogin}
              </a>
            </p>
          </div>
        </section>
      </div>
    </main>
  );
}

export default function ResetPage() {
  return (
    <Suspense fallback={<p>{labels.en.loading}</p>}>
      <ResetPasswordContent />
    </Suspense>
  );
}
