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
  const [errorMsg, setErrorMsg] = useState("");

  const isBusinessEmail = (email: string) => {
    const blockedDomains = [
      "gmail.com",
      "yahoo.com",
      "hotmail.com",
      "outlook.com",
      "live.com",
      "icloud.com",
      "aol.com",
      "protonmail.com",
      "proton.me",
      "mail.com",
      "gmx.com",
      "yandex.com",
    ];

    const domain = email.split("@")[1]?.toLowerCase();

    if (!domain) return false;

    return !blockedDomains.includes(domain);
  };

  const handleSubmit = async () => {
    setMessage("");
    setErrorMsg("");

    if (!isBusinessEmail(form.email)) {
      setErrorMsg("Please use a company email address.");
      return;
    }

    try {
      const res = await fetch(`${API_URL}/contact/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error("Failed");
      }

      setMessage(data.message || "Submitted");

      setForm({
        full_name: "",
        email: "",
        company_name: "",
        company_size: "",
        use_case: "",
      });
    } catch (error) {
      setErrorMsg("Failed to send request. Please try again.");
    }
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
            value={form.full_name}
            onChange={(e) =>
              setForm({ ...form, full_name: e.target.value })
            }
          />

          <input
            placeholder="Work email"
            className="w-full border p-3 rounded-xl"
            value={form.email}
            onChange={(e) =>
              setForm({ ...form, email: e.target.value })
            }
          />

          <input
            placeholder="Company name"
            className="w-full border p-3 rounded-xl"
            value={form.company_name}
            onChange={(e) =>
              setForm({ ...form, company_name: e.target.value })
            }
          />

          <select
            className="w-full border p-3 rounded-xl"
            value={form.company_size}
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
            value={form.use_case}
            onChange={(e) =>
              setForm({ ...form, use_case: e.target.value })
            }
          />

          {/* SUCCESS */}
          {message && (
            <div className="rounded-xl bg-green-50 border border-green-200 text-green-700 px-4 py-3 text-sm text-center">
              {message}
            </div>
          )}

          {/* ERROR */}
          {errorMsg && (
            <div className="rounded-xl bg-red-50 border border-red-200 text-red-700 px-4 py-3 text-sm text-center">
              {errorMsg}
            </div>
          )}

          <button
            onClick={handleSubmit}
            className="w-full bg-black text-white py-3 rounded-xl"
          >
            Contact sales
          </button>
        </div>
      </div>
    </main>
  );
}