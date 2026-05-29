"use client";

import { Suspense, useEffect, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  "https://api.runexa.ai";

type ResetLabels = {
  badge: string;
  heroTitle: string;
  heroDescription: string;
  featureSecurityTitle: string;
  featureSecurityDesc: string;
  featureExperienceTitle: string;
  featureExperienceDesc: string;
  featureControlTitle: string;
  featureControlDesc: string;
  title: string;
  subtitle: string;
  newPassword: string;
  passwordPlaceholder: string;
  passwordMustContain: string;
  resetPassword: string;
  resetting: string;
  backToLogin: string;
  loading: string;
  invalidLink: string;
  passwordRequirements: string;
  success: string;
  requestFailed: string;
  serverError: string;
  rules: string[];
};

const labels: Record<string, ResetLabels> = {
 en: {
    badge: "Secure access to your Runexa account",
    heroTitle: "Create a new password",
    heroDescription:
      "Choose a strong password to keep your Runexa account secure and protect access to your AI workspace.",
    featureSecurityTitle: "Stronger Security",
    featureSecurityDesc:
      "A strong password helps protect your account, data, and AI workflows.",
    featureExperienceTitle: "Seamless Access",
    featureExperienceDesc:
      "Keep your account secure and continue working with your AI agents without interruption.",
    featureControlTitle: "Account Control",
    featureControlDesc:
      "Update your password whenever needed to stay in control of your account.",
    title: "Reset your password",
    subtitle: "Enter a new password for your Runexa account.",
    newPassword: "New password",
    passwordPlaceholder: "Enter your new password",
    passwordMustContain: "Your password must include:",
    resetPassword: "Reset password",
    resetting: "Resetting password...",
    backToLogin: "← Back to sign in",
    loading: "Loading...",
    invalidLink: "This reset link is invalid or has expired.",
    passwordRequirements:
      "Your password does not meet the requirements.",
    success:
      "Password updated successfully. Redirecting...",
    requestFailed: "Request failed",
    serverError: "Unable to connect to the server",
    rules: [
      "At least 12 characters",
      "One uppercase letter",
      "One lowercase letter",
      "One number",
      "One special character",
    ],
  },

  fr: {
    badge:
      "Accès sécurisé à votre compte Runexa",

    heroTitle:
      "Créer un nouveau mot de passe",

    heroDescription:
      "Choisissez un mot de passe sécurisé pour protéger votre compte Runexa et votre espace de travail IA.",

    featureSecurityTitle:
      "Sécurité renforcée",

    featureSecurityDesc:
      "Un mot de passe robuste contribue à protéger votre compte, vos données et vos workflows IA.",

    featureExperienceTitle:
      "Accès sans interruption",

    featureExperienceDesc:
      "Conservez un accès sécurisé à votre compte et poursuivez votre travail avec vos agents IA.",

    featureControlTitle:
      "Contrôle du compte",

    featureControlDesc:
      "Mettez à jour votre mot de passe à tout moment pour garder le contrôle de votre compte.",

    title:
      "Réinitialiser votre mot de passe",

    subtitle:
      "Saisissez un nouveau mot de passe pour votre compte Runexa.",

    newPassword:
      "Nouveau mot de passe",

    passwordPlaceholder:
      "Saisissez votre nouveau mot de passe",

    passwordMustContain:
      "Votre mot de passe doit contenir :",

    resetPassword:
      "Réinitialiser le mot de passe",

    resetting:
      "Réinitialisation en cours...",

    backToLogin:
      "← Retour à la connexion",

    loading:
      "Chargement...",

    invalidLink:
      "Ce lien de réinitialisation est invalide ou a expiré.",

    passwordRequirements:
      "Votre mot de passe ne respecte pas les exigences de sécurité.",

    success:
      "Mot de passe mis à jour avec succès. Redirection...",

    requestFailed:
      "La requête a échoué",

    serverError:
      "Impossible de se connecter au serveur",

    rules: [
      "Au moins 12 caractères",
      "Une lettre majuscule",
      "Une lettre minuscule",
      "Un chiffre",
      "Un caractère spécial",
    ],
  },

  ar: {
    badge:
      "وصول آمن إلى حساب Runexa",

    heroTitle:
      "إنشاء كلمة مرور جديدة",

    heroDescription:
      "اختر كلمة مرور قوية لحماية حساب Runexa الخاص بك وتأمين الوصول إلى مساحة العمل المدعومة بالذكاء الاصطناعي.",

    featureSecurityTitle:
      "أمان أقوى",

    featureSecurityDesc:
      "تساعد كلمة المرور القوية على حماية حسابك وبياناتك وسير العمل المدعوم بالذكاء الاصطناعي.",

    featureExperienceTitle:
      "وصول دون انقطاع",

    featureExperienceDesc:
      "حافظ على أمان حسابك وواصل العمل مع وكلاء الذكاء الاصطناعي دون انقطاع.",

    featureControlTitle:
      "التحكم في الحساب",

    featureControlDesc:
      "يمكنك تحديث كلمة المرور في أي وقت للحفاظ على التحكم الكامل في حسابك.",

    title:
      "إعادة تعيين كلمة المرور",

    subtitle:
      "أدخل كلمة مرور جديدة لحساب Runexa الخاص بك.",

    newPassword:
      "كلمة المرور الجديدة",

    passwordPlaceholder:
      "أدخل كلمة المرور الجديدة",

    passwordMustContain:
      "يجب أن تتضمن كلمة المرور:",

    resetPassword:
      "إعادة تعيين كلمة المرور",

    resetting:
      "جارٍ إعادة تعيين كلمة المرور...",

    backToLogin:
      "← العودة إلى تسجيل الدخول",

    loading:
      "جارٍ التحميل...",

    invalidLink:
      "رابط إعادة تعيين كلمة المرور غير صالح أو منتهي الصلاحية.",

    passwordRequirements:
      "كلمة المرور لا تستوفي متطلبات الأمان.",

    success:
      "تم تحديث كلمة المرور بنجاح. جارٍ إعادة التوجيه...",

    requestFailed:
      "فشل الطلب",

    serverError:
      "تعذر الاتصال بالخادم",

    rules: [
      "12 حرفاً على الأقل",
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
  const [loading, setLoading] = useState(false);

  const [message, setMessage] = useState("");
  const [messageType, setMessageType] =
    useState<"success" | "error">("success");

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
    {
      icon: "12+",
      label: t.rules[0],
      valid: password.length >= 12,
    },
    {
      icon: "Aa",
      label: t.rules[1],
      valid: /[A-Z]/.test(password),
    },
    {
      icon: "aa",
      label: t.rules[2],
      valid: /[a-z]/.test(password),
    },
    {
      icon: "1",
      label: t.rules[3],
      valid: /\d/.test(password),
    },
    {
      icon: "#",
      label: t.rules[4],
      valid: /[!@#$%^&*(),.?":{}|<>]/.test(password),
    },
  ];

  const handle = async () => {
    if (loading) return;

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

    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/auth/reset-password`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          token,
          password,
        }),
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
    } finally {
      setLoading(false);
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
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && isValid) {
                      handle();
                    }
                  }}
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
                disabled={!isValid || loading}
                className={`w-full rounded-xl py-3 font-semibold text-white shadow-lg transition ${
                  isValid && !loading
                    ? "bg-slate-950 hover:bg-slate-800"
                    : "cursor-not-allowed bg-slate-400"
                }`}
              >
                {loading ? t.resetting : t.resetPassword}
              </button>
            </div>

            <p className="mt-7 text-center text-sm">
              <Link
                href="/login"
                className="font-medium text-blue-600 hover:text-blue-700"
              >
                {t.backToLogin}
              </Link>
            </p>
          </div>
        </section>
      </div>
    </main>
  );
}

export default function ResetPasswordClient() {
  return (
    <Suspense
      fallback={
        <main className="flex min-h-screen items-center justify-center bg-white">
          <p className="text-slate-600">
            {labels.en.loading}
          </p>
        </main>
      }
    >
      <ResetPasswordContent />
    </Suspense>
  );
}
