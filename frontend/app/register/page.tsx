"use client";

import { useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export default function RegisterPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  // ✅ NEW UI
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState<"success" | "error">("success");

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
    <main className="min-h-screen flex items-center justify-center">
      <div className="bg-white p-8 rounded-2xl shadow space-y-4 w-80">
        <h1 className="text-xl font-bold">Register</h1>

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

        <input
          type="password"
          placeholder="Password"
          className="w-full border p-2 rounded"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button
          onClick={handleRegister}
          className="w-full bg-black text-white py-2 rounded"
        >
          Register
        </button>
      </div>
    </main>
  );
}