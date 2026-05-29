"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { setToken } from "../../lib/auth";
import { trackEvent } from "../../lib/track";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  "https://api.runexa.ai";

type LoginLabels = {
  badge: string;
  welcomeBack: string;
  leftDescription: string;

  featureAgentsTitle: string;
  featureAgentsDesc: string;

  featureSecurityTitle: string;
  featureSecurityDesc: string;

  featureProductivityTitle: string;
  featureProductivityDesc: string;

  loginTitle: string;
  loginSubtitle: string;

  google: string;
  microsoft: string;
  separator: string;

  emailLabel: string;
  emailPlaceholder: string;

  passwordLabel: string;
  passwordPlaceholder: string;

  remember: string;
  forgot: string;

  loginButton: string;
  loggingIn: string;

  noAccount: string;
  createAccount: string;

  resendVerification: string;

  invalidCredentials: string;
  verifyEmail: string;
  loginFailed: string;
  serverError: string;
  enterEmailFirst: string;
  verificationSent: string;
};

const labels: Record<string, LoginLabels> = {
  en: {
    badge: "AI agents built for real work",

    welcomeBack: "Welcome back",

    leftDescription:
      "Sign in to your Runexa account and continue working with specialized AI agents for legal, finance, learning, and business decisions.",

    featureAgentsTitle: "Specialized AI Agents",

    featureAgentsDesc:
      "Access AI agents designed for document analysis, financial insights, learning support, and business workflows.",

    featureSecurityTitle: "Secure & Private",

    featureSecurityDesc:
      "Your data is protected with security-first infrastructure and privacy-focused workflows.",

    featureProductivityTitle: "Work Faster with AI",

    featureProductivityDesc:
      "Analyze documents, generate insights, and complete complex tasks faster with Runexa.",

    loginTitle: "Sign In",

    loginSubtitle:
      "Welcome back. Sign in to continue to your Runexa workspace.",

    google: "Continue with Google",

    microsoft: "Continue with Microsoft",

    separator: "or continue with email",

    emailLabel: "Email Address",

    emailPlaceholder: "you@example.com",

    passwordLabel: "Password",

    passwordPlaceholder: "Enter your password",

    remember: "Remember me",

    forgot: "Forgot password?",

    loginButton: "Sign In",

    loggingIn: "Signing in...",

    noAccount: "Don’t have an account?",

    createAccount: "Create account",

    resendVerification: "Resend verification email",

    invalidCredentials: "Incorrect email or password",

    verifyEmail:
      "Please verify your email before signing in.",

    loginFailed: "Sign-in failed",

    serverError: "Unable to connect to the server",

    enterEmailFirst: "Enter your email first",

    verificationSent:
      "Verification email sent.",
  },

  fr: {
    badge: "Des agents IA conçus pour le travail réel",

    welcomeBack: "Bon retour",

    leftDescription:
      "Connectez-vous à votre compte Runexa et continuez à travailler avec des agents IA spécialisés pour le juridique, la finance, l’apprentissage et les décisions business.",

    featureAgentsTitle: "Agents IA spécialisés",

    featureAgentsDesc:
      "Accédez à des agents IA conçus pour l’analyse documentaire, les insights financiers, l’apprentissage et les workflows métier.",

    featureSecurityTitle: "Sécurisé et confidentiel",

    featureSecurityDesc:
      "Vos données sont protégées grâce à une infrastructure sécurisée et des workflows respectueux de la confidentialité.",

    featureProductivityTitle: "Travaillez plus efficacement avec l’IA",

    featureProductivityDesc:
      "Analysez des documents, obtenez des insights et accomplissez des tâches complexes plus rapidement avec Runexa.",

    loginTitle: "Connexion",

    loginSubtitle:
      "Connectez-vous pour accéder à votre espace de travail Runexa.",

    google: "Continuer avec Google",

    microsoft: "Continuer avec Microsoft",

    separator: "ou continuer avec votre adresse e-mail",

    emailLabel: "Adresse e-mail",

    emailPlaceholder: "vous@exemple.com",

    passwordLabel: "Mot de passe",

    passwordPlaceholder: "Saisissez votre mot de passe",

    remember: "Se souvenir de moi",

    forgot: "Mot de passe oublié ?",

    loginButton: "Se connecter",

    loggingIn: "Connexion en cours...",

    noAccount: "Vous n’avez pas de compte ?",

    createAccount: "Créer un compte",

    resendVerification:
      "Renvoyer l’e-mail de vérification",

    invalidCredentials:
      "Adresse e-mail ou mot de passe incorrect",

    verifyEmail:
      "Veuillez vérifier votre adresse e-mail avant de vous connecter.",

    loginFailed: "Connexion impossible",

    serverError:
      "Impossible de se connecter au serveur",

    enterEmailFirst:
      "Veuillez d’abord saisir votre adresse e-mail",

    verificationSent:
      "E-mail de vérification envoyé.",
  },

  ar: {
    badge: "وكلاء ذكاء اصطناعي مصممون للعمل الحقيقي",
    welcomeBack: "مرحباً بعودتك",
    leftDescription:
      "سجّل الدخول إلى حساب Runexa الخاص بك وواصل العمل باستخدام وكلاء ذكاء اصطناعي متخصصين في القانون والمالية والتعلّم وقرارات الأعمال.",
    featureAgentsTitle: "وكلاء ذكاء اصطناعي متخصصون",
    featureAgentsDesc:
      "استفد من وكلاء ذكاء اصطناعي مصممين لتحليل المستندات والرؤى المالية ودعم التعلّم وسير العمل المهني.",
    featureSecurityTitle: "آمن وخاص",
    featureSecurityDesc:
      "بياناتك محمية من خلال بنية تحتية آمنة وسير عمل يركز على الخصوصية.",
    featureProductivityTitle: "اعمل بكفاءة أكبر مع الذكاء الاصطناعي",
    featureProductivityDesc:
      "حلّل المستندات واحصل على رؤى عملية وأنجز المهام المعقدة بسرعة أكبر مع Runexa.",
    loginTitle: "تسجيل الدخول",
    loginSubtitle:
      "سجّل الدخول للوصول إلى مساحة عمل Runexa الخاصة بك.",
    google: "المتابعة باستخدام Google",
    microsoft: "المتابعة باستخدام Microsoft",
    separator: "أو المتابعة باستخدام البريد الإلكتروني",
    emailLabel: "البريد الإلكتروني",
    emailPlaceholder: "you@example.com",
    passwordLabel: "كلمة المرور",
    passwordPlaceholder: "أدخل كلمة المرور",
    remember: "تذكرني",
    forgot: "هل نسيت كلمة المرور؟",
    loginButton: "تسجيل الدخول",
    loggingIn: "جارٍ تسجيل الدخول...",
    noAccount: "ليس لديك حساب؟",
    createAccount: "إنشاء حساب",
    resendVerification: "إعادة إرسال رسالة التحقق",
    invalidCredentials: "البريد الإلكتروني أو كلمة المرور غير صحيحة",
    verifyEmail: "يرجى التحقق من بريدك الإلكتروني قبل تسجيل الدخول.",
    loginFailed: "تعذر تسجيل الدخول",
    serverError: "تعذر الاتصال بالخادم",
    enterEmailFirst: "يرجى إدخال بريدك الإلكتروني أولاً",
    verificationSent: "تم إرسال رسالة التحقق.",
  },
};

export default function LoginClient() {
  const [language, setLanguage] = useState("en");

  const t = labels[language] || labels.en;

  const [email, setEmail] = useState("");

  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);

  const [message, setMessage] = useState("");

  const [messageType, setMessageType] =
    useState<"success" | "error">("error");

  useEffect(() => {
    const saved = localStorage.getItem("locale");

    if (saved && labels[saved]) {
      setLanguage(saved);
    }

    const handleLocaleChange = () => {
      const nextLocale =
        localStorage.getItem("locale");

      if (nextLocale && labels[nextLocale]) {
        setLanguage(nextLocale);
      }
    };

    window.addEventListener(
      "locale-change",
      handleLocaleChange
    );

    return () => {
      window.removeEventListener(
        "locale-change",
        handleLocaleChange
      );
    };
  }, []);

  const handleLogin = async () => {
    if (loading) return;

    setLoading(true);

    try {
      const res = await fetch(
        `${API_URL}/auth/login`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            email: email.trim(),
            password,
          }),
        }
      );

      const data = await res.json();

      console.log("LOGIN RESPONSE:", data);

      if (!res.ok) {
        setMessageType("error");

        if (data.detail === "Invalid credentials") {
          setMessage(t.invalidCredentials);

        } else if (
          data.detail?.includes("verify")
        ) {
          setMessage(t.verifyEmail);

        } else {
          setMessage(
            data.detail || t.loginFailed
          );
        }

        setLoading(false);
        return;
      }

      if (data.access_token) {
        trackEvent("login");

        setToken(data.access_token);

        const inviteToken =
          localStorage.getItem(
            "enterprise_invite_token"
          );

        if (inviteToken) {
          localStorage.removeItem(
            "enterprise_invite_token"
          );

          window.location.href =
            `/entreprises/accept?token=${inviteToken}`;

          return;
        }

        localStorage.setItem(
          "credits_balance",
          String(
            data.user?.credits_balance || 0
          )
        );

        localStorage.setItem(
          "plan",
          data.user?.plan || "trial"
        );

        localStorage.setItem(
          "role",
          data.user?.role ||
            data.role ||
            "user"
        );

        const role = (
          data.user?.role ||
          data.role ||
          "user"
        )
          .toLowerCase()
          .trim();

        const plan = (
          data.user?.plan ||
          "trial"
        )
          .toLowerCase()
          .trim();

        let isEnterpriseMember = false;

        try {
          const enterpriseResponse =
            await fetch(
              `${API_URL}/enterprise/me`,
              {
                headers: {
                  Authorization:
                    `Bearer ${data.access_token}`,
                },
              }
            );

          if (enterpriseResponse.ok) {
            isEnterpriseMember = true;

            localStorage.setItem(
              "enterprise_member",
              "true"
            );

          } else {
            localStorage.removeItem(
              "enterprise_member"
            );
          }

        } catch {
          localStorage.removeItem(
            "enterprise_member"
          );
        }

        if (role === "admin") {
          window.location.href = "/admin";

        } else if (
          role === "enterprise_admin" ||
          isEnterpriseMember
        ) {
          window.location.href =
            "/entreprises/dashboard";

        } else if (
          ["paid", "pro", "premium"].includes(
            plan
          )
        ) {
          window.location.href =
            "/dashboard";

        } else {
          window.location.href = "/upload";
        }

      } else {
        setMessageType("error");

        setMessage(t.loginFailed);
      }

    } catch (err) {
      console.error(err);

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
              {t.welcomeBack}
            </h1>

            <p className="mt-6 text-lg leading-8 text-slate-600">
              {t.leftDescription}
            </p>

            <div className="mt-12 space-y-7">
              <div className="flex gap-5">
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-blue-100 text-xl text-blue-700">
                  ⚡
                </div>

                <div>
                  <h3 className="font-semibold text-slate-950">
                    {t.featureAgentsTitle}
                  </h3>

                  <p className="mt-1 text-slate-600">
                    {t.featureAgentsDesc}
                  </p>
                </div>
              </div>

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
                  📈
                </div>

                <div>
                  <h3 className="font-semibold text-slate-950">
                    {t.featureProductivityTitle}
                  </h3>

                  <p className="mt-1 text-slate-600">
                    {t.featureProductivityDesc}
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
              <h1 className="text-3xl font-bold tracking-tight text-slate-950 sm:text-4xl">
                {t.loginTitle}
              </h1>

              <p className="mt-3 text-sm text-slate-500 sm:text-base">
                {t.loginSubtitle}
              </p>
            </div>

            <div className="mt-8 grid gap-3">
              <button
                onClick={() => {
                  window.location.href =
                    `${API_URL}/auth/google/login`;
                }}
                className="flex w-full items-center justify-between rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm font-medium text-slate-700 hover:bg-slate-50"
              >
                <span className="flex items-center gap-3">
                  <span className="text-lg">
                    G
                  </span>

                  {t.google}
                </span>
              </button>

              <button
                onClick={() => {
                  window.location.href =
                    `${API_URL}/auth/microsoft/login`;
                }}
                className="flex w-full items-center justify-between rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm font-medium text-slate-700 hover:bg-slate-50"
              >
                <span className="flex items-center gap-3">
                  <span className="text-lg">
                    ▦
                  </span>

                  {t.microsoft}
                </span>
              </button>
            </div>

            <div className="my-7 flex items-center gap-4">
              <div className="h-px flex-1 bg-slate-200" />

              <span className="text-xs text-slate-500">
                {t.separator}
              </span>

              <div className="h-px flex-1 bg-slate-200" />
            </div>

            {message && (
              <div
                className={`mb-5 rounded-xl border p-4 text-sm ${
                  messageType === "success"
                    ? "border-green-200 bg-green-50 text-green-700"
                    : "border-red-200 bg-red-50 text-red-700"
                }`}
              >
                {message}
              </div>
            )}

            <div className="space-y-5">
              <div>
                <label className="mb-2 block text-sm font-medium text-slate-700">
                  {t.emailLabel}
                </label>

                <input
                  type="email"

                  placeholder={t.emailPlaceholder}

                  className="w-full rounded-xl border border-slate-300 px-4 py-3 text-slate-950 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"

                  value={email}

                  onChange={(e) =>
                    setEmail(e.target.value)
                  }

                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      handleLogin();
                    }
                  }}
                />
              </div>

              <div>
                <label className="mb-2 block text-sm font-medium text-slate-700">
                  {t.passwordLabel}
                </label>

                <input
                  type="password"

                  placeholder={
                    t.passwordPlaceholder
                  }

                  className="w-full rounded-xl border border-slate-300 px-4 py-3 text-slate-950 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"

                  value={password}

                  onChange={(e) =>
                    setPassword(e.target.value)
                  }

                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      handleLogin();
                    }
                  }}
                />
              </div>

              <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <label className="flex items-center gap-2 text-sm text-slate-600">
                  <input
                    type="checkbox"
                    className="h-4 w-4 rounded border-slate-300"
                  />

                  {t.remember}
                </label>

                <Link
                  href="/forgot-password"
                  className="text-sm font-medium text-blue-600 hover:text-blue-700"
                >
                  {t.forgot}
                </Link>
              </div>

              <button
                onClick={handleLogin}

                disabled={loading}

                className="w-full rounded-xl bg-slate-950 py-3 font-semibold text-white shadow-lg transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {loading
                  ? t.loggingIn
                  : t.loginButton}
              </button>
            </div>

            <div className="mt-7 space-y-4 text-center">
              <p className="text-sm text-slate-500">
                {t.noAccount}{" "}

                <Link
                  href="/register"
                  className="font-medium text-blue-600 hover:text-blue-700"
                >
                  {t.createAccount}
                </Link>
              </p>

              <button
                onClick={async () => {
                  try {
                    if (!email.trim()) {
                      setMessageType("error");

                      setMessage(
                        t.enterEmailFirst
                      );

                      return;
                    }

                    const res = await fetch(
                      `${API_URL}/auth/resend-verification`,
                      {
                        method: "POST",

                        headers: {
                          "Content-Type":
                            "application/json",
                        },

                        body: JSON.stringify({
                          email: email.trim(),
                        }),
                      }
                    );

                    const data =
                      await res.json();

                    setMessageType("success");

                    setMessage(
                      data.message ||
                        data.detail ||
                        t.verificationSent
                    );

                  } catch (err) {
                    console.error(err);

                    setMessageType("error");

                    setMessage(
                      t.serverError
                    );
                  }
                }}
                className="text-sm font-medium text-blue-600 hover:text-blue-700"
              >
                {t.resendVerification}
              </button>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
