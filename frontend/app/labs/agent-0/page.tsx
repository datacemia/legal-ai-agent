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
    "Runexa Labs",
    "Agent 0",
  ],

  alternates: {
    canonical: "https://runexa.ai/labs/agent-0",
  },

  openGraph: {
    title:
      "Runexa Agent 0 | AI Safety Infrastructure & Smart Home Intelligence",

    description:
      "Future AI safety infrastructure combining cameras, sensors, GPS, and intelligent reasoning systems for smart monitoring.",

    url: "https://runexa.ai/labs/agent-0",

    siteName: "Runexa Systems",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Agent 0",
      },
    ],

    locale: "en_US",

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title:
      "Runexa Agent 0 | AI Safety Infrastructure & Smart Home Intelligence",

    description:
      "Experimental AI safety infrastructure combining cameras, sensors, GPS, and intelligent reasoning systems.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
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

            url: "https://runexa.ai/labs/agent-0",

            creator: {
              "@type": "Organization",
              name: "Runexa Labs",
            },

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems",
              url: "https://runexa.ai",
            },
          }),
        }}
      />
    </>
  );
}
