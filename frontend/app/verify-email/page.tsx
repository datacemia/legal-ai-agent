"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export default function VerifyEmailPage() {
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
          setMessage(data.detail || "Verification failed.");
        }
      })
      .catch(() => {
        setMessage("Error connecting to server.");
      });
  }, [token]);

  return (
    <main className="min-h-screen flex items-center justify-center">
      <div className="bg-white p-8 rounded-xl shadow text-center">
        <h1 className="text-xl font-bold mb-4">Email Verification</h1>
        <p>{message}</p>
      </div>
    </main>
  );
}