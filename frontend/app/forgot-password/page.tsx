"use client";

import { useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export default function ForgotPage() {
  const [email, setEmail] = useState("");

  const handle = async () => {
    const res = await fetch(`${API_URL}/auth/forgot-password`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email }),
    });

    const data = await res.json();
    alert(data.message);
  };

  return (
    <div className="p-8">
      <input value={email} onChange={(e) => setEmail(e.target.value)} />
      <button onClick={handle}>Send reset link</button>
    </div>
  );
}