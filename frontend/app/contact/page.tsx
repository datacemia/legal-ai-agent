"use client";

import { useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export default function ContactPage() {
  const [form, setForm] = useState({
    full_name: "",
    email: "",
    company_name: "",
    company_size: "",
    use_case: "",
  });

  const [message, setMessage] = useState("");

  const handleSubmit = async () => {
    const res = await fetch(`${API_URL}/contact/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(form),
    });

    const data = await res.json();
    setMessage(data.message || "Submitted");
  };

  return (
    <main className="min-h-screen bg-white px-4 py-20">
      <div className="mx-auto max-w-2xl space-y-8">

        <div className="text-center">
          <h1 className="text-3xl font-bold">Contact Sales</h1>
          <p className="text-slate-600 mt-2">
            Get a tailored solution for your business
          </p>
        </div>

        <div className="space-y-4">
          <input
            placeholder="Full name"
            className="w-full border p-3 rounded-xl"
            onChange={(e) =>
              setForm({ ...form, full_name: e.target.value })
            }
          />

          <input
            placeholder="Work email"
            className="w-full border p-3 rounded-xl"
            onChange={(e) =>
              setForm({ ...form, email: e.target.value })
            }
          />

          <input
            placeholder="Company name"
            className="w-full border p-3 rounded-xl"
            onChange={(e) =>
              setForm({ ...form, company_name: e.target.value })
            }
          />

          <select
            className="w-full border p-3 rounded-xl"
            onChange={(e) =>
              setForm({ ...form, company_size: e.target.value })
            }
          >
            <option value="">Company size</option>
            <option>1-10</option>
            <option>10-50</option>
            <option>50-200</option>
            <option>200+</option>
          </select>

          <textarea
            placeholder="How will you use Runexa?"
            className="w-full border p-3 rounded-xl"
            onChange={(e) =>
              setForm({ ...form, use_case: e.target.value })
            }
          />

          <button
            onClick={handleSubmit}
            className="w-full bg-black text-white py-3 rounded-xl"
          >
            Contact sales
          </button>

          {message && (
            <div className="text-green-600 text-center">{message}</div>
          )}
        </div>
      </div>
    </main>
  );
}