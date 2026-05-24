import type { Metadata } from "next";
import AcceptableUseClient from "./AcceptableUseClient";

export const metadata: Metadata = {
  title: "Acceptable Use Policy | Runexa",

  description:
    "Runexa acceptable use policy governing the lawful and responsible use of AI systems, APIs, workflows, and enterprise services.",

  keywords: [
    "acceptable use policy",
    "AI policy",
    "AI compliance",
    "enterprise AI policy",
    "AI usage rules",
    "Runexa policy",
  ],

  alternates: {
    canonical: "https://runexa.ai/acceptable-use",
  },
};

export default function AcceptableUsePage() {
  return (
    <>
      <AcceptableUseClient />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "WebPage",
            name: "Runexa Acceptable Use Policy",
            description:
              "Acceptable use policy for Runexa AI services, APIs, enterprise workflows, and intelligent systems.",
          }),
        }}
      />
    </>
  );
}
