"use client";

import { useState } from "react";
import { setToken } from "../../lib/auth";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

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
        if (data.detail === "Invalid credentials") {
          alert("Incorrect email or password");
        } else if (data.detail?.includes("verify")) {
          alert("Please verify your email before login");
        } else {
          alert(data.detail || "Login failed");
        }
        return;
      }

      if (data.access_token) {
        setToken(data.access_token);
        window.location.href = "/dashboard";
      } else {
        alert("Login failed");
      }
    } catch (err) {
      console.error(err);
      alert("Error connecting to server");
    }
  };

  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white p-8 rounded-2xl shadow space-y-4 w-80">
        <h1 className="text-xl font-bold text-center">Login</h1>

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
          onClick={handleLogin}
          className="w-full bg-black text-white py-2 rounded hover:bg-gray-800 transition"
        >
          Login
        </button>

        <a
          href="/forgot-password"
          className="text-sm text-center underline block mt-2"
        >
          Forgot password?
        </a>

        <button
          onClick={async () => {
            if (!email) {
              alert("Enter your email first");
              return;
            }

            const res = await fetch(`${API_URL}/auth/resend-verification`, {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({ email: email.trim() }),
            });

            const data = await res.json();

            alert(data.message || data.detail || "Verification email request sent.");
          }}
          className="w-full text-sm text-blue-600 underline"
        >
          Resend verification email
        </button>
      </div>
    </main>
  );
}