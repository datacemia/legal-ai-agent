"use client";

import { useState } from "react";
import { trackEvent } from "../../lib/track";

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

  const passwordRules = [
    { label: "At least 12 characters", valid: password.length >= 12 },
    { label: "One uppercase letter", valid: /[A-Z]/.test(password) },
    { label: "One lowercase letter", valid: /[a-z]/.test(password) },
    { label: "One number", valid: /\d/.test(password) },
    {
      label: "One special character",
      valid: /[!@#$%^&*(),.?":{}|<>]/.test(password),
    },
  ];

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
        trackEvent("register");

        if (data.access_token) {
          localStorage.setItem("token", data.access_token);

          localStorage.setItem(
            "credits_balance",
            String(data.user?.credits_balance || 0)
          );

          localStorage.setItem(
            "plan",
            data.user?.plan || "trial"
          );

          localStorage.setItem(
            "role",
            data.user?.role || "user"
          );
        }

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
        {/* LEFT */}
        <section className="relative hidden overflow-hidden bg-gradient-to-br from-blue-50 via-white to-indigo-50 px-10 py-12 lg:flex lg:flex-col lg:justify-center xl:px-20">
          <div className="max-w-xl">
            <span className="inline-flex rounded-full bg-blue-100 px-4 py-2 text-sm font-medium text-blue-700">
              AI agents that get things done
            </span>

            <h1 className="mt-8 text-4xl font-bold text-slate-950 xl:text-5xl">
              Create one Runexa account for all AI agents
            </h1>

            <p className="mt-6 text-lg text-slate-600">
              Create one Runexa account for all AI agents. Start with a $1 trial per agent, then continue with global credits or a plan. Runexa supports legal, study, finance, business, and future security agents.
            </p>

            <div className="mt-12 space-y-7">
              <div className="flex gap-5">
                <div className="h-12 w-12 flex items-center justify-center rounded-2xl bg-blue-100 text-blue-700">
                  ⚡
                </div>
                <div>
                  <h3 className="font-semibold">Specialized AI Agents</h3>
                  <p className="text-slate-600">
                    Access powerful agents built for your business needs.
                  </p>
                </div>
              </div>

              <div className="flex gap-5">
                <div className="h-12 w-12 flex items-center justify-center rounded-2xl bg-blue-100 text-blue-700">
                  🛡️
                </div>
                <div>
                  <h3 className="font-semibold">Secure & Private</h3>
                  <p className="text-slate-600">
                    Your data is protected with enterprise-grade security.
                  </p>
                </div>
              </div>

              <div className="flex gap-5">
                <div className="h-12 w-12 flex items-center justify-center rounded-2xl bg-blue-100 text-blue-700">
                  📈
                </div>
                <div>
                  <h3 className="font-semibold">
                    Save Time, Get More Done
                  </h3>
                  <p className="text-slate-600">
                    Automate complex tasks and focus on what matters most.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* RIGHT */}
        <section className="flex items-center justify-center bg-slate-50 px-4 py-10 lg:bg-white">
          <div className="w-full max-w-xl rounded-3xl border bg-white p-6 shadow-xl">
            <div className="text-center">
              <h1 className="text-3xl font-bold">Create your account</h1>
              <p className="text-slate-500">
                Start with a $1 trial per agent, then continue with global credits or a plan.
              </p>
            </div>

            {message && (
              <div className="mt-5 text-sm">{message}</div>
            )}

            <div className="space-y-5 mt-6">
              <input
                type="email"
                placeholder="you@example.com"
                className="w-full border px-4 py-3 rounded-xl"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />

              <input
                type="password"
                placeholder="Create a strong password"
                className="w-full border px-4 py-3 rounded-xl"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />

              <div className="text-sm space-y-1">
                {passwordRules.map((rule) => (
                  <p
                    key={rule.label}
                    className={
                      rule.valid
                        ? "text-green-600"
                        : "text-slate-500"
                    }
                  >
                    {rule.valid ? "✓" : "○"} {rule.label}
                  </p>
                ))}
              </div>

              <button
                onClick={handleRegister}
                disabled={!isValid}
                className="w-full bg-black text-white py-3 rounded-xl disabled:bg-gray-400"
              >
                Create account
              </button>
            </div>

            <p className="mt-6 text-center text-sm">
              Already have an account?{" "}
              <a href="/login" className="text-blue-600">
                Log in
              </a>
            </p>
          </div>
        </section>
      </div>
    </main>
  );
}