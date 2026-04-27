"use client";

import { useState } from "react";
import { setToken } from "../../lib/auth";
import { trackEvent } from "../../lib/track";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState<"success" | "error">("error");

  const handleLogin = async () => {
    try {
      const res = await fetch(`${API_URL}/auth/login`, {
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

      console.log("LOGIN RESPONSE:", data);

      if (!res.ok) {
        setMessageType("error");

        if (data.detail === "Invalid credentials") {
          setMessage("Incorrect email or password");
        } else if (data.detail?.includes("verify")) {
          setMessage("Please verify your email before login");
        } else {
          setMessage(data.detail || "Login failed");
        }
        return;
      }

      if (data.access_token) {
        trackEvent("login");
        setToken(data.access_token);

        // ✅ FIX : sauvegarde du role
        const role = (data.user?.role || data.role || "user")
          .toLowerCase()
          .trim();

        localStorage.setItem("role", role);

        // ✅ FIX : redirection intelligente
        if (role === "admin" || role === "business") {
          window.location.href = "/dashboard";
        } else {
          window.location.href = "/upload";
        }
      } else {
        setMessageType("error");
        setMessage("Login failed");
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
              Welcome back
            </h1>

            <p className="mt-6 text-lg leading-8 text-slate-600">
              Log in to your account and continue using AI agents to get work
              done faster.
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
                Login
              </h1>
              <p className="mt-3 text-sm text-slate-500 sm:text-base">
                Welcome back! Please login to your account.
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
                  placeholder="Enter your password"
                  className="w-full rounded-xl border border-slate-300 px-4 py-3 text-slate-950 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>

              <button
                onClick={handleLogin}
                className="w-full rounded-xl bg-slate-950 py-3 font-semibold text-white shadow-lg transition hover:bg-slate-800"
              >
                Login
              </button>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}