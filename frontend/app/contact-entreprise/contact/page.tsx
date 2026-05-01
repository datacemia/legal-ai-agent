"use client";

import { useState } from "react";
import Link from "next/link";

export default function EnterpriseContactPage() {
  const [form, setForm] = useState({
    name: "",
    email: "",
    company: "",
    size: "",
    useCase: "",
  });

  const handleChange = (e: any) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e: any) => {
    e.preventDefault();

    console.log("Enterprise lead:", form);

    alert("Your request has been sent. Our team will contact you.");
  };

  return (
    <main className="min-h-screen bg-slate-50 px-6 py-16 text-slate-900">

      <div className="max-w-3xl mx-auto">

        {/* BACK */}
        <div className="mb-6">
          <Link href="/enterprise" className="text-sm text-blue-600">
            ← Back to Business page
          </Link>
        </div>

        {/* HEADER */}
        <div className="text-center mb-10 space-y-3">
          <h1 className="text-3xl font-bold">
            Contact Runexa for Business
          </h1>

          <p className="text-slate-600">
            Tell us about your needs. We will build custom AI agents tailored to your workflows.
          </p>
        </div>

        {/* FORM */}
        <form
          onSubmit={handleSubmit}
          className="bg-white border rounded-2xl p-8 space-y-6"
        >

          {/* NAME */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Full name
            </label>

            <input
              type="text"
              name="name"
              value={form.name}
              onChange={handleChange}
              className="w-full border rounded-xl px-4 py-3"
              required
            />
          </div>

          {/* EMAIL */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Work email
            </label>

            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              className="w-full border rounded-xl px-4 py-3"
              required
            />
          </div>

          {/* COMPANY */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Company name
            </label>

            <input
              type="text"
              name="company"
              value={form.company}
              onChange={handleChange}
              className="w-full border rounded-xl px-4 py-3"
            />
          </div>

          {/* SIZE */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Company size
            </label>

            <select
              name="size"
              value={form.size}
              onChange={handleChange}
              className="w-full border rounded-xl px-4 py-3"
            >
              <option value="">Select size</option>
              <option>1-10 employees</option>
              <option>10-50 employees</option>
              <option>50-200 employees</option>
              <option>200+ employees</option>
            </select>
          </div>

          {/* USE CASE */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Which custom AI agents do you need?
            </label>

            <textarea
              name="useCase"
              value={form.useCase}
              onChange={handleChange}
              rows={5}
              placeholder="Example: contract review, financial reporting, CV screening, document processing, business dashboards..."
              className="w-full border rounded-xl px-4 py-3"
            />
          </div>

          {/* SUBMIT */}
          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-3 rounded-xl font-semibold hover:bg-blue-700 transition"
          >
            Contact sales
          </button>
        </form>

      </div>

    </main>
  );
}