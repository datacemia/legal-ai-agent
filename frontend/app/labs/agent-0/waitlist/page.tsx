"use client";

import { useState } from "react";
import Link from "next/link";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export default function AgentZeroWaitlistPage() {
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const form = e.currentTarget;
    const formData = new FormData(form);

    const payload = {
      full_name: String(formData.get("full_name") || ""),
      email: String(formData.get("email") || ""),
      country: String(formData.get("country") || ""),
      profile: String(formData.get("profile") || ""),
      interest_level: String(formData.get("interest_level") || ""),
      protect_target: String(formData.get("protect_target") || ""),
      message: String(formData.get("message") || ""),
      consent: true,
    };

    const res = await fetch(`${API_URL}/agent0-waitlist/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const data = await res.json();

    if (!res.ok) {
      alert(data.detail || "Failed to submit waitlist form.");
      return;
    }

    setSubmitted(true);
  };

  return (
    <main className="min-h-screen bg-slate-950 px-6 py-20 text-white">
      <div className="mx-auto max-w-4xl">
        <Link
          href="/labs/agent-0"
          className="text-sm font-medium text-cyan-300 hover:text-cyan-200"
        >
          ← Back to Agent 0 concept
        </Link>

        <div className="mt-10 rounded-3xl border border-white/10 bg-white/[0.04] p-8 shadow-2xl">
          <span className="inline-flex rounded-full border border-cyan-300/20 bg-cyan-400/10 px-4 py-2 text-sm font-semibold text-cyan-200">
            Runexa Labs · Agent 0 Waitlist
          </span>

          <h1 className="mt-6 text-4xl font-bold tracking-tight md:text-5xl">
            Join the Runexa Agent 0 waitlist
          </h1>

          <p className="mt-5 max-w-2xl text-slate-300">
            Get early updates on Runexa’s future AI safety system for homes,
            cameras, sensors, GPS, and autonomous monitoring.
          </p>

          {submitted ? (
            <div className="mt-8 rounded-2xl border border-emerald-400/20 bg-emerald-500/10 p-6 text-emerald-100">
              Thank you. Your interest has been recorded. Runexa will contact
              selected early-access users when Agent 0 moves forward.
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="mt-8 grid gap-5">
              <div className="grid gap-5 md:grid-cols-2">
                <div>
                  <label className="mb-2 block text-sm font-medium text-slate-300">
                    Full name
                  </label>
                  <input
                    required
                    name="full_name"
                    className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3 text-white outline-none focus:border-cyan-300"
                    placeholder="Your name"
                  />
                </div>

                <div>
                  <label className="mb-2 block text-sm font-medium text-slate-300">
                    Email address
                  </label>
                  <input
                    required
                    type="email"
                    name="email"
                    className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3 text-white outline-none focus:border-cyan-300"
                    placeholder="you@example.com"
                  />
                </div>
              </div>

              <div className="grid gap-5 md:grid-cols-2">
                <div>
                  <label className="mb-2 block text-sm font-medium text-slate-300">
                    Country
                  </label>
                  <input
                    name="country"
                    className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3 text-white outline-none focus:border-cyan-300"
                    placeholder="United States, Morocco, France..."
                  />
                </div>

                <div>
                  <label className="mb-2 block text-sm font-medium text-slate-300">
                    Profile
                  </label>
                  <select
                    name="profile"
                    className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3 text-white outline-none focus:border-cyan-300"
                  >
                    <option>Homeowner</option>
                    <option>Parent / Family</option>
                    <option>Property manager</option>
                    <option>Smart home enthusiast</option>
                    <option>Security company</option>
                    <option>Investor / Partner</option>
                    <option>Other</option>
                  </select>
                </div>
              </div>

              <div className="grid gap-5 md:grid-cols-2">
                <div>
                  <label className="mb-2 block text-sm font-medium text-slate-300">
                    Interest level
                  </label>
                  <select
                    name="interest_level"
                    className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3 text-white outline-none focus:border-cyan-300"
                  >
                    <option>Early access</option>
                    <option>Beta tester</option>
                    <option>Partnership</option>
                    <option>Investment / Business inquiry</option>
                    <option>Just following updates</option>
                  </select>
                </div>

                <div>
                  <label className="mb-2 block text-sm font-medium text-slate-300">
                    What would you like Agent 0 to protect?
                  </label>
                  <select
                    name="protect_target"
                    className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3 text-white outline-none focus:border-cyan-300"
                  >
                    <option>Home</option>
                    <option>Apartment</option>
                    <option>Office</option>
                    <option>Warehouse</option>
                    <option>Vacation property</option>
                    <option>Multiple properties</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="mb-2 block text-sm font-medium text-slate-300">
                  Message / use case
                </label>
                <textarea
                  name="message"
                  rows={5}
                  className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3 text-white outline-none focus:border-cyan-300"
                  placeholder="Tell us what kind of safety or monitoring problem you would like Agent 0 to solve."
                />
              </div>

              <label className="flex gap-3 text-sm text-slate-300">
                <input required type="checkbox" className="mt-1" />
                <span>
                  I agree to be contacted by Runexa Systems about Agent 0
                  updates, early access, and related product information.
                </span>
              </label>

              <button
                type="submit"
                className="rounded-xl bg-cyan-300 px-6 py-3 font-semibold text-slate-950 hover:bg-cyan-200"
              >
                Request early access
              </button>

              <p className="text-xs text-slate-500">
                Agent 0 is a concept and research initiative. It is not publicly
                available yet.
              </p>
            </form>
          )}
        </div>
      </div>
    </main>
  );
}