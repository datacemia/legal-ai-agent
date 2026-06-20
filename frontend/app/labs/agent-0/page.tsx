import type { Metadata } from "next";
import AgentZeroClient from "./AgentZeroClient";

const siteUrl = "https://runexa.ai";

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

  "Agent Zero",
  "Runexa AI Labs",
  "AI surveillance",
  "intelligent monitoring system",
  "computer vision AI",
  "AI-powered cameras",
  "smart security AI",
  "AI event detection",
  "real-time monitoring AI",
  "AI anomaly detection",
  "AI threat detection",
  "AI safety monitoring",
  "AI video analytics",
  "video intelligence AI",
  "AI sensor fusion",
  "edge AI monitoring",
  "IoT AI platform",
  "smart building AI",
  "smart property monitoring",
  "AI infrastructure monitoring",
  "AI automation platform",
  "AI operations center",
  "predictive monitoring AI",
  "AI alerts and notifications",
  "AI incident detection",
  "AI-powered automation",
  "security operations AI",
  "physical security AI",
  "intelligent security infrastructure",
  "AI home security",
  "AI workplace safety",
  "enterprise monitoring AI",
  "AI security analytics",
  "autonomous monitoring agent",
  "computer vision platform",
  "AI sensor network",
  "AI edge computing",
  "smart environment AI",
  "next-generation AI systems",
  "AI safety technology",
],
  alternates: {
    canonical: "https://runexa.ai/labs/agent-0",
    languages: {
      en: `${siteUrl}/en/labs/agent-0`,
      fr: `${siteUrl}/fr/labs/agent-0`,
      ar: `${siteUrl}/ar/labs/agent-0`,
      "x-default": `${siteUrl}/labs/agent-0`,
    },
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

    alternateLocale: ["fr_FR", "ar_AR"],

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
      <AgentZeroClient initialLanguage="en" />

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

            inLanguage: "en",

            creator: {
              "@type": "Organization",
              name: "Runexa Labs",
            },

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems",
              url: siteUrl,
            },
          }),
        }}
      />
    </>
  );
}
