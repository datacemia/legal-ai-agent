"use client";

import Link from "next/link";

const features = [
  {
    title: "AI Camera Reasoning",
    desc: "Understand movement, visitors, unusual activity, and visual events from connected cameras.",
  },
  {
    title: "Sensor Fusion Intelligence",
    desc: "Combine door sensors, motion sensors, vibration, sound, temperature, and environmental signals.",
  },
  {
    title: "GPS Geofencing",
    desc: "Detect trusted presence, family arrival, unknown movement zones, and location-based safety rules.",
  },
  {
    title: "Real-time Smart Alerts",
    desc: "Transform raw events into clear risk levels, explanations, and recommended actions.",
  },
  {
    title: "Drone-ready Monitoring",
    desc: "Future architecture for autonomous aerial inspection and perimeter awareness.",
  },
  {
    title: "Privacy-first Architecture",
    desc: "Designed with local processing, permission control, and user-owned security data in mind.",
  },
];

export default function AgentZeroPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <section className="relative overflow-hidden px-6 py-24">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-600/20 via-slate-950 to-cyan-500/10" />
        <div className="absolute left-1/2 top-20 h-72 w-72 -translate-x-1/2 rounded-full bg-blue-500/20 blur-3xl" />

        <div className="relative mx-auto max-w-6xl">
          <span className="inline-flex rounded-full border border-white/10 bg-white/10 px-4 py-2 text-sm font-semibold text-blue-100">
            Concept Preview · Coming Soon
          </span>

          <h1 className="mt-8 max-w-4xl text-5xl font-bold tracking-tight md:text-7xl">
            Runexa Agent 0
          </h1>

          <p className="mt-6 max-w-3xl text-xl leading-8 text-slate-300">
            The future AI safety infrastructure for homes, sensors, cameras,
            GPS, and autonomous monitoring.
          </p>

          <div className="mt-10 flex flex-wrap gap-4">
            <Link
              href="/labs/agent-0/waitlist"
              className="rounded-xl bg-white px-6 py-3 font-semibold text-slate-950 hover:bg-slate-100"
            >
              Join Waitlist
            </Link>

            <a
              href="#concept"
              className="rounded-xl border border-white/10 bg-white/5 px-6 py-3 font-semibold text-white hover:bg-white/10"
            >
              View Security Concept
            </a>
          </div>
        </div>
      </section>

      <section className="px-6 py-16">
        <div className="mx-auto max-w-6xl">
          <div className="mb-10 max-w-3xl">
            <p className="text-sm font-semibold uppercase tracking-wide text-cyan-300">
              Intelligent Safety Command Center
            </p>
            <h2 className="mt-3 text-3xl font-bold md:text-4xl">
              One AI layer for cameras, sensors, GPS, alerts, and future drones.
            </h2>
          </div>

          <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
            {features.map((feature) => (
              <div
                key={feature.title}
                className="rounded-3xl border border-white/10 bg-white/[0.04] p-6 shadow-2xl shadow-blue-950/20"
              >
                <div className="mb-5 h-2 w-2 rounded-full bg-cyan-300" />
                <h3 className="text-lg font-semibold">{feature.title}</h3>
                <p className="mt-3 text-sm leading-6 text-slate-400">
                  {feature.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="concept" className="px-6 py-16">
        <div className="mx-auto grid max-w-6xl gap-8 lg:grid-cols-2">
          <div className="rounded-3xl border border-white/10 bg-white/[0.04] p-8">
            <h2 className="text-3xl font-bold">How Agent 0 thinks</h2>
            <p className="mt-5 leading-8 text-slate-300">
              Agent 0 combines camera understanding, environmental sensors, GPS
              presence detection, and AI reasoning into a unified safety
              intelligence layer designed for future autonomous homes.
            </p>

            <div className="mt-8 space-y-4 text-sm text-slate-300">
              <div className="rounded-2xl border border-white/10 bg-slate-900/80 p-4">
                Cameras detect visual activity.
              </div>
              <div className="rounded-2xl border border-white/10 bg-slate-900/80 p-4">
                Sensors confirm physical events.
              </div>
              <div className="rounded-2xl border border-white/10 bg-slate-900/80 p-4">
                GPS understands trusted presence.
              </div>
              <div className="rounded-2xl border border-cyan-400/20 bg-cyan-500/10 p-4 text-cyan-100">
                AI reasoning turns events into risk levels and actions.
              </div>
            </div>
          </div>

          <div className="rounded-3xl border border-cyan-400/20 bg-cyan-500/10 p-8">
            <p className="text-sm font-semibold uppercase tracking-wide text-cyan-200">
              System Vision
            </p>
            <h3 className="mt-4 text-2xl font-bold">
              Camera + Sensors + GPS + AI Reasoning
            </h3>
            <p className="mt-5 leading-8 text-cyan-50">
              A future command center that can help understand unusual movement,
              open doors, unknown visitors, sensor alerts, family presence,
              and security events in real time.
            </p>

            <div className="mt-8 rounded-2xl border border-white/10 bg-slate-950/70 p-5 text-sm text-slate-300">
              Agent 0 is currently a research and concept initiative from Runexa
              Labs. Features shown on this page are experimental and not publicly
              available yet.
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}