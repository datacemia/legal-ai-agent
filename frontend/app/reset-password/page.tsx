"use client";

import { Suspense, useState } from "react";
import { useSearchParams } from "next/navigation";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

function ResetPasswordContent() {
  const params = useSearchParams();
  const token = params.get("token");
  const [password, setPassword] = useState("");

  // ✅ NEW UI
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState<"success" | "error">("success");

  const handle = async () => {
    if (!token) {
      setMessageType("error");
      setMessage("Invalid reset link.");
      return;
    }

    if (!password || password.length < 6) {
      setMessageType("error");
      setMessage("Password must be at least 6 characters.");
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
    <main className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white p-8 rounded-2xl shadow space-y-4 w-80">
        <h1 className="text-xl font-bold text-center">Reset password</h1>

        {/* ✅ MESSAGE UI */}
        {message && (
          <div
            className={`text-sm p-3 rounded-lg text-center ${
              messageType === "success"
                ? "bg-green-50 text-green-700 border border-green-200"
                : "bg-red-50 text-red-700 border border-red-200"
            }`}
          >
            {message}
          </div>
        )}

        <input
          type="password"
          placeholder="New password"
          className="w-full border p-2 rounded"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button
          onClick={handle}
          className="w-full bg-black text-white py-2 rounded"
        >
          Reset password
        </button>
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