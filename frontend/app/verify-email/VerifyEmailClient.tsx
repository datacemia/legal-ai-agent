"use client";

import { Suspense, useEffect, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

type VerifyEmailLabels = {
  verifying: string;
  invalidLink: string;
  success: string;
  invalidOrUsed: string;
  failed: string;
  serverError: string;
  title: string;
  goToLogin: string;
  loading: string;
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
    goToLogin: "Go to login",
    loading: "Loading...",
  },

  fr: {
    verifying: "Vérification de votre e-mail...",
    invalidLink: "Lien de vérification invalide.",
    success: "E-mail vérifié avec succès. Vous pouvez maintenant vous connecter.",
    invalidOrUsed: "Ce lien de vérification est invalide ou a déjà été utilisé.",
    failed: "Échec de la vérification.",
    serverError: "Erreur de connexion au serveur.",
    title: "Vérification de l’e-mail",
    goToLogin: "Aller à la connexion",
    loading: "Chargement...",
  },

  ar: {
    verifying: "جاري التحقق من بريدك الإلكتروني...",
    invalidLink: "رابط التحقق غير صالح.",
    success: "تم التحقق من البريد الإلكتروني بنجاح. يمكنك الآن تسجيل الدخول.",
    invalidOrUsed: "رابط التحقق هذا غير صالح أو تم استخدامه مسبقًا.",
    failed: "فشل التحقق.",
    serverError: "خطأ في الاتصال بالخادم.",
    title: "التحقق من البريد الإلكتروني",
    goToLogin: "الذهاب إلى تسجيل الدخول",
    loading: "جاري التحميل...",
  },
};

function VerifyEmailContent() {
  const searchParams = useSearchParams();
  const token = searchParams.get("token");

  const [language, setLanguage] = useState("en");
  const t = labels[language] || labels.en;

  const [message, setMessage] = useState(labels.en.verifying);

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
      setMessage(currentLabels.invalidLink);
      return;
    }

    setMessage(currentLabels.verifying);

    fetch(`${API_URL}/auth/verify-email?token=${token}`)
      .then(async (res) => {
        const data = await res.json();

        if (res.ok) {
          setMessage(currentLabels.success);
        } else {
          if (data.detail?.includes("Invalid")) {
            setMessage(currentLabels.invalidOrUsed);
          } else {
            setMessage(data.detail || currentLabels.failed);
          }
        }
      })
      .catch(() => {
        setMessage(currentLabels.serverError);
      });
  }, [token, language]);

  return (
    <div
      dir={language === "ar" ? "rtl" : "ltr"}
      className="bg-white p-8 rounded-xl shadow text-center space-y-4"
    >
      <h1 className="text-xl font-bold">{t.title}</h1>
      <p>{message}</p>

      <Link
        href="/login"
        className="inline-block bg-black text-white px-4 py-2 rounded-lg"
      >
        {t.goToLogin}
      </Link>
    </div>
  );
}

export default function VerifyEmailClient() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-50">
      <Suspense fallback={<p>{labels.en.loading}</p>}>
        <VerifyEmailContent />
      </Suspense>
    </main>
  );
}
