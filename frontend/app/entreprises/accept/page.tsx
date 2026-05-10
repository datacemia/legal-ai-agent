"use client";

import { useEffect, useState } from "react";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export default function AcceptEnterpriseInvitePage() {
  const [message, setMessage] = useState("Accepting invitation...");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const acceptInvite = async () => {
      try {
        const token = localStorage.getItem("token");

        if (!token) {
          window.location.href = "/login";
          return;
        }

        const params = new URLSearchParams(window.location.search);
        const inviteToken = params.get("token");

        if (!inviteToken) {
          setMessage("Invalid invitation link.");
          setLoading(false);
          return;
        }

        const res = await fetch(
          `${API_URL}/enterprise/accept-invite`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
              token: inviteToken,
            }),
          }
        );

        const data = await res.json();

        if (!res.ok) {
          setMessage(data.detail || "Unable to accept invitation.");
          setLoading(false);
          return;
        }

        localStorage.setItem("enterprise_member", "true");

        setMessage("Invitation accepted. Redirecting...");

        setTimeout(() => {
          window.location.href = "/entreprises/dashboard";
        }, 1500);

      } catch (err) {
        setMessage("Unexpected error.");
      } finally {
        setLoading(false);
      }
    };

    acceptInvite();
  }, []);

  return (
    <main className="min-h-screen flex items-center justify-center bg-slate-950 text-white px-6">
      <div className="max-w-lg w-full rounded-3xl border border-white/10 bg-white/[0.04] p-8 text-center">
        <h1 className="text-3xl font-bold">
          Enterprise Invitation
        </h1>

        <p className="mt-4 text-slate-300">
          {message}
        </p>

        {loading && (
          <div className="mt-6 text-sm text-slate-500">
            Processing...
          </div>
        )}
      </div>
    </main>
  );
}