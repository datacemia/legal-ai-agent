"use client";

import { useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export default function RegisterPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState<"success" | "error">("success");

  // ✅ VALIDATION LIVE (UX ONLY)
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

        {/* ✅ PASSWORD RULES UI */}
        <p className="text-xs text-gray-500">
          Password must contain:
          <br />- 12 characters
          <br />- 1 uppercase
          <br />- 1 lowercase
          <br />- 1 number
          <br />- 1 special character
        </p>

        <button
          onClick={handleRegister}
          disabled={!isValid} // ✅ BLOQUE SI PAS VALIDE
          className={`w-full py-2 rounded text-white ${
            isValid ? "bg-black" : "bg-gray-400 cursor-not-allowed"
          }`}
        >
          Register
        </button>
      </div>
    </main>
  );
}