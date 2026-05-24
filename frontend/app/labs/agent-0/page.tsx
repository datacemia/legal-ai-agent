import type { Metadata } from "next";
import AgentZeroClient from "./AgentZeroClient";

export const metadata: Metadata = {
  title:
    "Runexa Agent 0 | AI Safety Infrastructure & Smart Home Intelligence",

  description:
    "Runexa Agent 0 is a future AI safety and smart monitoring concept combining cameras, sensors, GPS, and intelligent reasoning systems.",

  keywords: [
    "AI safety system",
    "smart home AI",
    "AI monitoring",
    "AI sensors",
    "AI camera intelligence",
    "AI home automation",
    "AI security infrastructure",
  ],

  alternates: {
    canonical: "https://runexa.ai/labs/agent-0",
  },
};

export default function AgentZeroPage() {
  return (
    <>
      <AgentZeroClient />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "ResearchProject",
            name: "Runexa Agent 0",
            description:
              "Experimental AI safety infrastructure concept combining cameras, sensors, GPS, and intelligent reasoning systems.",
            creator: {
              "@type": "Organization",
              name: "Runexa Labs",
            },
          }),
        }}
      />
    </>
  );
}
