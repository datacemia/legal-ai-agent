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

        const role = (data.user?.role || data.role || "user")
          .toLowerCase()
          .trim();

        localStorage.setItem("role", role);

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
        </section>

        <section className="flex min-h-screen items-center justify-center bg-slate-50 px-4 py-10 sm:px-6 lg:bg-white lg:px-10">
          <div className="w-full max-w-xl rounded-3xl border border-slate-200 bg-white p-6 shadow-xl shadow-slate-200/70 sm:p-8 lg:p-10">
            <h1 className="text-3xl font-bold text-center">Login</h1>

            {message && (
              <div className="mt-4 text-center text-red-600">{message}</div>
            )}

            <input
              type="email"
              placeholder="Email"
              className="w-full mt-6 p-3 border rounded-xl"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            <input
              type="password"
              placeholder="Password"
              className="w-full mt-4 p-3 border rounded-xl"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

            <button
              onClick={handleLogin}
              className="w-full mt-6 bg-black text-white py-3 rounded-xl"
            >
              Login
            </button>
          </div>
        </section>
      </div>
    </main>
  );
}