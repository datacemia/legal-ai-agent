"use client";

import { useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export default function ForgotPage() {
  const [email, setEmail] = useState("");

  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState<"success" | "error">("success");

  const handle = async () => {
    try {
      if (!email.trim()) {
        setMessageType("error");
        setMessage("Please enter your email");
        return;
      }

      const res = await fetch(`${API_URL}/auth/forgot-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email.trim() }),
      });

      const data = await res.json();

      setMessageType("success");
      setMessage(data.message || data.detail || "Request sent.");
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
              Reset your password with peace of mind
            </h1>

            <p className="mt-6 text-lg leading-8 text-slate-600">
              Enter your email and we’ll send you a secure link to reset your
              password.
            </p>

            <div className="mt-12 space-y-7">
              <div className="flex gap-5">
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-blue-100 text-xl text-blue-700">
                  🔒
                </div>
                <div>
                  <h3 className="font-semibold text-slate-950">
                    Secure & Private
                  </h3>
                  <p className="mt-1 text-slate-600">
                    Your data is encrypted and protected with enterprise-grade
                    security.
                  </p>
                </div>
              </div>

              <div className="flex gap-5">
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-blue-100 text-xl text-blue-700">
                  ⚡
                </div>
                <div>
                  <h3 className="font-semibold text-slate-950">
                    Quick & Easy
                  </h3>
                  <p className="mt-1 text-slate-600">
                    Reset your password in just a few simple steps.
                  </p>
                </div>
              </div>

              <div className="flex gap-5">
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-blue-100 text-xl text-blue-700">
                  🛡️
                </div>
                <div>
                  <h3 className="font-semibold text-slate-950">
                    Get Back to Work
                  </h3>
                  <p className="mt-1 text-slate-600">
                    Regain access and continue using AI agents without
                    interruption.
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
                ✉️
              </div>

              <h1 className="mt-6 text-3xl font-bold tracking-tight text-slate-950 sm:text-4xl">
                Forgot password?
              </h1>

              <p className="mx-auto mt-3 max-w-sm text-sm leading-6 text-slate-500 sm:text-base">
                Enter your email and we’ll send you a link to reset your
                password.
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

              <button
                onClick={handle}
                className="w-full rounded-xl bg-slate-950 py-3 font-semibold text-white shadow-lg transition hover:bg-slate-800"
              >
                Send reset link
              </button>
            </div>

            <div className="my-7 flex items-center gap-4">
              <div className="h-px flex-1 bg-slate-200" />
              <span className="text-xs text-slate-500">or</span>
              <div className="h-px flex-1 bg-slate-200" />
            </div>

            <p className="text-center text-sm">
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