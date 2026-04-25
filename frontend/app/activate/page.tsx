"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export default function ActivatePage() {
  const params = useSearchParams();
  const token = params.get("token");

  const [status, setStatus] = useState("loading");

  useEffect(() => {
    async function activate() {
      if (!token) {
        setStatus("error");
        return;
      }

      try {
        const res = await fetch(
          `${API_URL}/auth/activate?token=${token}`
        );

        if (res.ok) {
          setStatus("success");
        } else {
          setStatus("error");
        }
      } catch (err) {
        console.error(err);
        setStatus("error");
      }
    }

    activate();
  }, [token]);

  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white p-8 rounded-2xl shadow text-center space-y-4">
        {status === "loading" && (
          <>
            <div className="w-10 h-10 border-4 border-black border-t-transparent rounded-full animate-spin mx-auto"></div>
            <p>Activating your account...</p>
          </>
        )}

        {status === "success" && (
          <>
            <h1 className="text-xl font-bold text-green-600">
              Account activated 🎉
            </h1>
            <p>You can now login.</p>

            <a
              href="/login"
              className="inline-block mt-4 px-4 py-2 bg-black text-white rounded-lg"
            >
              Go to Login
            </a>
          </>
        )}

        {status === "error" && (
          <>
            <h1 className="text-xl font-bold text-red-600">
              Activation failed
            </h1>
            <p>Invalid or expired link.</p>
          </>
        )}
      </div>
    </main>
  );
}