"use client";

import { useEffect } from "react";
import { setToken } from "../../lib/auth";

export default function OAuthSuccess() {
  useEffect(() => {
    const params = new URLSearchParams(
      window.location.search
    );

    const token = params.get("token");

    const role = (
      params.get("role") || "user"
    )
      .toLowerCase()
      .trim();

    const plan = (
      params.get("plan") || "trial"
    )
      .toLowerCase()
      .trim();

    const credits =
      params.get("credits_balance") || "0";

    if (!token) return;

    setToken(token);

    window.history.replaceState(
      {},
      "",
      "/oauth-success"
    );

    localStorage.setItem("role", role);

    localStorage.setItem("plan", plan);

    localStorage.setItem(
      "credits_balance",
      credits
    );

    if (
      role === "enterprise_admin" ||
      role === "enterprise_member"
    ) {
      localStorage.setItem(
        "enterprise_member",
        "true"
      );

    } else {
      localStorage.removeItem(
        "enterprise_member"
      );
    }

    const inviteToken =
      localStorage.getItem(
        "enterprise_invite_token"
      );

    if (inviteToken) {
      localStorage.removeItem(
        "enterprise_invite_token"
      );

      window.location.href =
        `/entreprises/accept?token=${inviteToken}`;

      return;
    }

    if (role === "admin") {
      window.location.href = "/admin";

    } else if (
      role === "enterprise_admin" ||
      role === "enterprise_member"
    ) {
      window.location.href =
        "/entreprises/dashboard";

    } else if (
      ["paid", "pro", "premium"].includes(
        plan
      )
    ) {
      window.location.href =
        "/dashboard";

    } else {
      window.location.href = "/upload";
    }
  }, []);

  return (
    <main className="flex min-h-screen items-center justify-center bg-white">
      <div className="flex flex-col items-center gap-5">
        <div className="h-12 w-12 animate-spin rounded-full border-4 border-slate-200 border-t-blue-600" />

        <div className="space-y-2 text-center">
          <h1 className="text-xl font-semibold text-slate-900">
            Signing you in
          </h1>

          <p className="text-sm text-slate-600">
            Redirecting to your Runexa workspace...
          </p>
        </div>
      </div>
    </main>
  );
}
