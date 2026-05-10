"use client";

import { useEffect } from "react";

export default function OAuthSuccess() {
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);

    const token = params.get("token");
    const role = (params.get("role") || "user")
      .toLowerCase()
      .trim();

    const plan = (params.get("plan") || "trial")
      .toLowerCase()
      .trim();

    const credits = params.get("credits_balance") || "0";

    if (token) {
      localStorage.setItem("token", token);
      localStorage.setItem("role", role);
      localStorage.setItem("plan", plan);
      localStorage.setItem("credits_balance", credits);

      if (role === "admin") {
        window.location.href = "/admin";
      } else if (role === "enterprise_admin") {
        window.location.href = "/entreprises/dashboard";
      } else if (["paid", "pro", "premium"].includes(plan)) {
        window.location.href = "/dashboard";
      } else {
        window.location.href = "/upload";
      }
    }
  }, []);

  return (
    <main className="min-h-screen flex items-center justify-center bg-white">
      <p className="text-slate-600">Logging you in...</p>
    </main>
  );
}