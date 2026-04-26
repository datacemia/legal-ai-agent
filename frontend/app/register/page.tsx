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
    <main className="min-h-screen grid grid-cols-1 lg:grid-cols-2 bg-white text-slate-950">
      <section className="relative hidden lg:flex flex-col justify-between overflow-hidden border-r border-slate-200 bg-gradient-to-br from-slate-50 via-white to-blue-50 px-16 py-12">
        <div>
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-600 text-xl font-black text-white">
              R
            </div>
            <div>
              <h2 className="text-2xl font-bold">Runexa</h2>
              <p className="text-sm text-slate-500">AI agents that get things done</p>
            </div>
          </div>

          <div className="mt-28 max-w-xl">
            <span className="inline-flex rounded-full bg-blue-100 px-4 py-2 text-sm font-medium text-blue-700">
              AI agents that get things done
            </span>

            <h1 className="mt-8 text-5xl font-bold leading-tight tracking-tight">
              Create your account and start building
            </h1>

            <p className="mt-6 text-xl leading-8 text-slate-600">
              Join teams using Runexa to automate workflows, save time, and boost productivity with AI agents.
            </p>

            <div className="mt-12 space-y-8">
              <div className="flex gap-5">
                <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-100 text-blue-700">
                  ⚡
                </div>
                <div>
                  <h3 className="font-semibold">Powerful AI Agents</h3>
                  <p className="mt-1 text-slate-600">Automate complex tasks and save hours of work.</p>
                </div>
              </div>

              <div className="flex gap-5">
                <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-100 text-blue-700">
                  👥
                </div>
                <div>
                  <h3 className="font-semibold">Collaborate Seamlessly</h3>
                  <p className="mt-1 text-slate-600">Work with your team in real time.</p>
                </div>
              </div>

              <div className="flex gap-5">
                <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-100 text-blue-700">
                  🔒
                </div>
                <div>
                  <h3 className="font-semibold">Enterprise-Grade Security</h3>
                  <p className="mt-1 text-slate-600">Your data is encrypted and always protected.</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="pointer-events-none absolute -bottom-24 -left-20 h-72 w-[120%] rounded-[100%] border border-blue-300 opacity-40" />
        <div className="pointer-events-none absolute -bottom-32 -left-24 h-72 w-[120%] rounded-[100%] border border-blue-400 opacity-30" />
      </section>

      <section className="flex min-h-screen items-center justify-center px-6 py-10">
        <div className="w-full max-w-xl">
          <div className="mb-12 flex items-center justify-between">
            <div className="lg:hidden flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600 font-black text-white">
                R
              </div>
              <span className="text-xl font-bold">Runexa</span>
            </div>

            <p className="ml-auto text-sm text-slate-500">
              Already have an account?{" "}
              <a href="/login" className="font-medium text-blue-600 hover:text-blue-700">
                Log in
              </a>
            </p>
          </div>

          <div>
            <h1 className="text-4xl font-bold tracking-tight">Create an account</h1>
            <p className="mt-3 text-lg text-slate-500">Enter your details to get started</p>
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
                className="w-full rounded-xl border border-slate-300 px-4 py-3 text-slate-900 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
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
                className="w-full rounded-xl border border-slate-300 px-4 py-3 text-slate-900 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>

            <div className="rounded-2xl bg-slate-50 p-5 text-sm text-slate-600">
              <p className="mb-3 font-medium text-slate-500">Password must contain:</p>
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
        </div>
      </section>
    </main>
  );
}