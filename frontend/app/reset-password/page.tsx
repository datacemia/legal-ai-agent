"use client";

import { Suspense, useState } from "react";
import { useSearchParams } from "next/navigation";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

function ResetPasswordContent() {
  const params = useSearchParams();
  const token = params.get("token");
  const [password, setPassword] = useState("");

  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState<"success" | "error">("success");

  const isValid =
    password.length >= 12 &&
    /[A-Z]/.test(password) &&
    /[a-z]/.test(password) &&
    /\d/.test(password) &&
    /[!@#$%^&*(),.?":{}|<>]/.test(password);

  const passwordRules = [
    { icon: "12+", label: "At least 12 characters", valid: password.length >= 12 },
    { icon: "Aa", label: "One uppercase letter", valid: /[A-Z]/.test(password) },
    { icon: "aa", label: "One lowercase letter", valid: /[a-z]/.test(password) },
    { icon: "1", label: "One number", valid: /\d/.test(password) },
    {
      icon: "#",
      label: "One special character",
      valid: /[!@#$%^&*(),.?":{}|<>]/.test(password),
    },
  ];

  const handle = async () => {
    if (!token) {
      setMessageType("error");
      setMessage("Invalid reset link.");
      return;
    }

    if (!isValid) {
      setMessageType("error");
      setMessage("Password does not meet the requirements.");
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
        setMessage("Password updated successfully. Redirecting...");

        setTimeout(() => {
          window.location.href = "/login";
        }, 1500);

        return;
      }

      setMessageType("error");
      setMessage(data.detail || data.message || "Request failed");
    } catch (error) {
      console.error(error);
      setMessageType("error");
      setMessage("Error connecting to server");
    }
  };

  return (
    <main className="min-h-screen bg-white text-slate-950">
      <div className="grid min-h-screen grid-cols-1 lg:grid-cols-2">
        <section className="relative hidden overflow-hidden bg-gradient-to-br from-blue-50 via-white to-indigo-50 px-10 py-12 lg:flex lg:flex-col lg:justify-center xl:px-20">
          <div className="max-w-xl">
            <span className="inline-flex rounded-full bg-blue-100 px-4 py-2 text-sm font-medium text-blue-700">
              AI agents that get things done
            </span>

            <h1 className="mt-8 text-4xl font-bold leading-tight tracking-tight text-slate-950 xl:text-5xl">
              Secure your account with a new password
            </h1>

            <p className="mt-6 text-lg leading-8 text-slate-600">
              Choose a strong password to protect your account and keep your
              data safe.
            </p>

            <div className="mt-12 space-y-7">
              <div className="flex gap-5">
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-blue-100 text-xl text-blue-700">
                  🛡️
                </div>
                <div>
                  <h3 className="font-semibold text-slate-950">
                    Stronger Security
                  </h3>
                  <p className="mt-1 text-slate-600">
                    A strong password keeps your account and data protected.
                  </p>
                </div>
              </div>

              <div className="flex gap-5">
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-blue-100 text-xl text-blue-700">
                  ⚡
                </div>
                <div>
                  <h3 className="font-semibold text-slate-950">
                    Better Experience
                  </h3>
                  <p className="mt-1 text-slate-600">
                    Secure access means uninterrupted productivity with your AI
                    agents.
                  </p>
                </div>
              </div>

              <div className="flex gap-5">
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-blue-100 text-xl text-blue-700">
                  ✅
                </div>
                <div>
                  <h3 className="font-semibold text-slate-950">
                    You&apos;re in Control
                  </h3>
                  <p className="mt-1 text-slate-600">
                    Update your password anytime to stay in control.
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
                Reset password
              </h1>

              <p className="mt-3 text-sm text-slate-500 sm:text-base">
                Enter your new password below.
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
                  New password
                </label>
                <input
                  type="password"
                  placeholder="Enter new password"
                  className="w-full rounded-xl border border-slate-300 px-4 py-3 text-slate-950 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>

              <div className="rounded-2xl border border-slate-200 bg-slate-50 p-5 text-sm">
                <p className="mb-4 font-semibold text-slate-950">
                  Password must contain:
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
                Reset password
              </button>
            </div>

            <p className="mt-7 text-center text-sm">
              <a
                href="/login"
                className="font-medium text-blue-600 hover:text-blue-700"
              >
                ← Back to login
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
    <Suspense fallback={<p>Loading...</p>}>
      <ResetPasswordContent />
    </Suspense>
  );
}