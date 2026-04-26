"use client";

import { useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export default function RegisterPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState<"success" | "error">("success");

  const isValid =
    password.length >= 12 &&
    /[A-Z]/.test(password) &&
    /[a-z]/.test(password) &&
    /\d/.test(password) &&
    /[!@#$%^&*(),.?":{}|<>]/.test(password);

  const handleRegister = async () => {
    try {
      if (!email.trim() || !password) {
        setMessageType("error");
        setMessage("Please enter email and password");
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
        setMessageType("success");
        setMessage(
          "Account created. Please check your email to verify your account."
        );

        setTimeout(() => {
          window.location.href = "/login";
        }, 1500);
      } else {
        setMessageType("error");
        setMessage(data.detail || "Registration failed");
      }
    } catch (err) {
      console.error(err);
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
              Start using AI agents to get work done faster
            </h1>

            <p className="mt-6 text-lg leading-8 text-slate-600">
              Runexa brings specialized AI agents for legal, finance, HR,
              business, and more — all in one simple platform.
            </p>

            <div className="mt-12 space-y-7">
              <div className="flex gap-5">
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-blue-100 text-xl text-blue-700">
                  ⚡
                </div>
                <div>
                  <h3 className="font-semibold text-slate-950">
                    Specialized AI Agents
                  </h3>
                  <p className="mt-1 text-slate-600">
                    Access powerful agents built for your business needs.
                  </p>
                </div>
              </div>

              <div className="flex gap-5">
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-blue-100 text-xl text-blue-700">
                  🛡️
                </div>
                <div>
                  <h3 className="font-semibold text-slate-950">
                    Secure & Private
                  </h3>
                  <p className="mt-1 text-slate-600">
                    Your data is protected with enterprise-grade security.
                  </p>
                </div>
              </div>

              <div className="flex gap-5">
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-blue-100 text-xl text-blue-700">
                  📈
                </div>
                <div>
                  <h3 className="font-semibold text-slate-950">
                    Save Time, Get More Done
                  </h3>
                  <p className="mt-1 text-slate-600">
                    Automate complex tasks and focus on what matters most.
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
                Create your account
              </h1>
              <p className="mt-3 text-sm text-slate-500 sm:text-base">
                Start using AI agents to get work done faster
              </p>
            </div>

            <div className="mt-8 grid gap-3">
              <button
                type="button"
                disabled
                className="flex w-full items-center justify-between rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm font-medium text-slate-500 cursor-not-allowed"
              >
                <span className="flex items-center gap-3">
                  <span className="text-lg">G</span>
                  Continue with Google
                </span>
                <span className="rounded-full bg-indigo-50 px-3 py-1 text-xs text-indigo-700">
                  Coming soon
                </span>
              </button>

              <button
                type="button"
                disabled
                className="flex w-full items-center justify-between rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm font-medium text-slate-500 cursor-not-allowed"
              >
                <span className="flex items-center gap-3">
                  <span className="text-lg">▦</span>
                  Continue with Microsoft
                </span>
                <span className="rounded-full bg-indigo-50 px-3 py-1 text-xs text-indigo-700">
                  Coming soon
                </span>
              </button>
            </div>

            <div className="my-7 flex items-center gap-4">
              <div className="h-px flex-1 bg-slate-200" />
              <span className="text-xs text-slate-500">
                or continue with email
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
                  Email address
                </label>
                <input
                  type="email"
                  placeholder="you@example.com"
                  className="w-full rounded-xl border border-slate-300 px-4 py-3 text-slate-950 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>

              <div>
                <label className="mb-2 block text-sm font-medium text-slate-700">
                  Password
                </label>
                <input
                  type="password"
                  placeholder="Create a strong password"
                  className="w-full rounded-xl border border-slate-300 px-4 py-3 text-slate-950 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>

              <div className="rounded-2xl bg-slate-50 p-5 text-sm text-slate-600">
                <p className="mb-3 font-medium text-slate-500">
                  Password must contain:
                </p>
                <div className="space-y-2">
                  <p>✓ At least 12 characters</p>
                  <p>✓ One uppercase letter</p>
                  <p>✓ One lowercase letter</p>
                  <p>✓ One number</p>
                  <p>✓ One special character</p>
                </div>
              </div>

              <button
                onClick={handleRegister}
                disabled={!isValid}
                className={`w-full rounded-xl py-3 font-semibold text-white shadow-lg transition ${
                  isValid
                    ? "bg-slate-950 hover:bg-slate-800"
                    : "bg-slate-400 cursor-not-allowed"
                }`}
              >
                Create account
              </button>
            </div>

            <p className="mt-7 text-center text-sm text-slate-500">
              Already have an account?{" "}
              <a
                href="/login"
                className="font-medium text-blue-600 hover:text-blue-700"
              >
                Log in
              </a>
            </p>
          </div>
        </section>
      </div>
    </main>
  );
}