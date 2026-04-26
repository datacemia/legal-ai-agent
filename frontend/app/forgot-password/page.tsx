"use client";

import { useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export default function ForgotPage() {
  const [email, setEmail] = useState("");

  // ✅ NEW (UI message)
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

      // ✅ SAME LOGIC (just UI instead of alert)
      setMessageType("success");
      setMessage(data.message || data.detail || "Request sent.");
    } catch (err) {
      console.error(err);
      setMessageType("error");
      setMessage("Error connecting to server");
    }
  };

  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white p-8 rounded-2xl shadow space-y-4 w-80">
        <h1 className="text-xl font-bold text-center">Forgot password</h1>

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
          type="email"
          placeholder="Email"
          className="w-full border p-2 rounded"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <button
          onClick={handle}
          className="w-full bg-black text-white py-2 rounded"
        >
          Send reset link
        </button>
      </div>
    </main>
  );
}