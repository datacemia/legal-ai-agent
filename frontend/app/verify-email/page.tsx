"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

function VerifyEmailContent() {
  const searchParams = useSearchParams();
  const token = searchParams.get("token");

  const [message, setMessage] = useState("Verifying your email...");

  useEffect(() => {
    if (!token) {
      setMessage("Invalid verification link.");
      return;
    }

    fetch(`${API_URL}/auth/verify-email?token=${token}`)
      .then(async (res) => {
        const data = await res.json();

        if (res.ok) {
          setMessage("Email verified successfully. You can now login.");
        } else {
          if (data.detail?.includes("Invalid")) {
            setMessage("This verification link is invalid or already used.");
          } else {
            setMessage(data.detail || "Verification failed.");
          }
        }
      })
      .catch(() => {
        setMessage("Error connecting to server.");
      });
  }, [token]);

  return (
    <div className="bg-white p-8 rounded-xl shadow text-center space-y-4">
      <h1 className="text-xl font-bold">Email Verification</h1>
      <p>{message}</p>

      <a
        href="/login"
        className="inline-block bg-black text-white px-4 py-2 rounded-lg"
      >
        Go to login
      </a>
    </div>
  );
}

export default function VerifyEmailPage() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-50">
      <Suspense fallback={<p>Loading...</p>}>
        <VerifyEmailContent />
      </Suspense>
    </main>
  );
}