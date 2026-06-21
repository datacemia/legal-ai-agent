"use client";

import { Suspense, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  "https://api.runexa.ai";

type VerifyEmailLabels = {
  verifying: string;
  invalidLink: string;
  success: string;
  invalidOrUsed: string;
  failed: string;
  serverError: string;
  title: string;
  subtitle: string;
  goToLogin: string;
  loading: string;
  statusSuccess: string;
  statusError: string;
};

const labels: Record<string, VerifyEmailLabels> = {
  en: {
    verifying: "Verifying your email...",
    invalidLink: "Invalid verification link.",
    success: "Email verified successfully. You can now login.",
    invalidOrUsed: "This verification link is invalid or already used.",
    failed: "Verification failed.",
    serverError: "Error connecting to server.",
    title: "Email Verification",
    subtitle:
      "We are verifying your Runexa account email address.",
    goToLogin: "Go to login",
    loading: "Loading...",
    statusSuccess: "Verified",
    statusError: "Action required",
  },

  fr: {
    verifying: "Vérification de votre e-mail...",
    invalidLink: "Lien de vérification invalide.",
    success:
      "E-mail vérifié avec succès. Vous pouvez maintenant vous connecter.",
    invalidOrUsed:
      "Ce lien de vérification est invalide ou a déjà été utilisé.",
    failed: "Échec de la vérification.",
    serverError: "Erreur de connexion au serveur.",
    title: "Vérification de l’e-mail",
    subtitle:
      "Nous vérifions l’adresse e-mail de votre compte Runexa.",
    goToLogin: "Aller à la connexion",
    loading: "Chargement...",
    statusSuccess: "Vérifié",
    statusError: "Action requise",
  },

  ar: {
    verifying: "جاري التحقق من بريدك الإلكتروني...",
    invalidLink: "رابط التحقق غير صالح.",
    success:
      "تم التحقق من البريد الإلكتروني بنجاح. يمكنك الآن تسجيل الدخول.",
    invalidOrUsed:
      "رابط التحقق هذا غير صالح أو تم استخدامه مسبقًا.",
    failed: "فشل التحقق.",
    serverError: "خطأ في الاتصال بالخادم.",
    title: "التحقق من البريد الإلكتروني",
    subtitle:
      "نحن نتحقق من عنوان البريد الإلكتروني لحساب Runexa الخاص بك.",
    goToLogin: "الذهاب إلى تسجيل الدخول",
    loading: "جاري التحميل...",
    statusSuccess: "تم التحقق",
    statusError: "إجراء مطلوب",
  },
};

function VerifyEmailContent() {
  const searchParams = useSearchParams();
  const token = searchParams.get("token");

  const hasRequestedVerification = useRef(false);

  const [language, setLanguage] = useState("en");
  const t = labels[language] || labels.en;

  const [message, setMessage] = useState(labels.en.verifying);
  const [status, setStatus] =
    useState<"loading" | "success" | "error">("loading");

  useEffect(() => {
    const saved = localStorage.getItem("locale");

    if (saved && labels[saved]) {
      setLanguage(saved);
      setMessage(labels[saved].verifying);
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

  useEffect(() => {
    const currentLabels = labels[language] || labels.en;

    if (!token) {
      setStatus("error");
      setMessage(currentLabels.invalidLink);
      return;
    }

    if (hasRequestedVerification.current) {
      return;
    }

    hasRequestedVerification.current = true;

    setStatus("loading");
    setMessage(currentLabels.verifying);

    window.history.replaceState({}, "", "/verify-email");

    fetch(`${API_URL}/auth/verify-email?token=${encodeURIComponent(token)}`)
      .then(async (res) => {
        const data = await res.json().catch(() => ({}));

        if (res.ok) {
          setStatus("success");
          setMessage(currentLabels.success);
          return;
        }

        setStatus("error");

        if (data.detail?.includes("Invalid")) {
          setMessage(currentLabels.invalidOrUsed);
        } else {
          setMessage(data.detail || currentLabels.failed);
        }
      })
      .catch(() => {
        setStatus("error");
        setMessage(currentLabels.serverError);
      });
  }, [token, language]);

  return (
    <div
      dir={language === "ar" ? "rtl" : "ltr"}
      className="w-full max-w-md rounded-3xl border border-slate-200 bg-white p-8 text-center shadow-xl shadow-slate-200/70"
    >
      <div
        className={`mx-auto flex h-16 w-16 items-center justify-center rounded-full text-3xl ${
          status === "success"
            ? "bg-green-50 text-green-700"
            : status === "error"
            ? "bg-red-50 text-red-700"
            : "bg-blue-50 text-blue-700"
        }`}
      >
        {status === "success" ? "✓" : status === "error" ? "!" : "✉️"}
      </div>

      <h1 className="mt-6 text-3xl font-bold tracking-tight text-slate-950">
        {t.title}
      </h1>

      <p className="mt-3 text-sm text-slate-500">
        {t.subtitle}
      </p>

      {status === "loading" && (
        <div className="mx-auto mt-6 h-10 w-10 animate-spin rounded-full border-4 border-slate-200 border-t-blue-600" />
      )}

      <div
        className={`mt-6 rounded-2xl border p-4 text-sm ${
          status === "success"
            ? "border-green-200 bg-green-50 text-green-700"
            : status === "error"
            ? "border-red-200 bg-red-50 text-red-700"
            : "border-blue-200 bg-blue-50 text-blue-700"
        }`}
      >
        <p className="font-semibold">
          {status === "success"
            ? t.statusSuccess
            : status === "error"
            ? t.statusError
            : t.verifying}
        </p>

        <p className="mt-1">
          {message}
        </p>
      </div>

      <Link
        href="/login"
        className="mt-7 inline-flex w-full items-center justify-center rounded-xl bg-slate-950 px-5 py-3 text-sm font-semibold text-white shadow-lg transition hover:bg-slate-800"
      >
        {t.goToLogin}
      </Link>
    </div>
  );
}

export default function VerifyEmailClient() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-50 px-4 py-10">
      <Suspense
        fallback={
          <div className="rounded-3xl border border-slate-200 bg-white p-8 text-center shadow-xl">
            <div className="mx-auto h-10 w-10 animate-spin rounded-full border-4 border-slate-200 border-t-blue-600" />
            <p className="mt-4 text-sm text-slate-600">
              {labels.en.loading}
            </p>
          </div>
        }
      >
        <VerifyEmailContent />
      </Suspense>
    </main>
  );
}
