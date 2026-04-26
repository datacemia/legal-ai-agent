"use client";

import { useSearchParams } from "next/navigation";
import { useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export default function ResetPage() {
  const params = useSearchParams();
  const token = params.get("token");

  const [password, setPassword] = useState("");

  const handle = async () => {
    const res = await fetch(`${API_URL}/auth/reset-password`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token, password }),
    });

    const data = await res.json();
    alert(data.message || data.detail);
  };

  return (
    <div className="p-8">
      <input
        type="password"
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handle}>Reset password</button>
    </div>
  );
}