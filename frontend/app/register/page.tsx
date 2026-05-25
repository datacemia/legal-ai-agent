import type { Metadata } from "next";
import RegisterClient from "./RegisterClient";

export const metadata: Metadata = {
  title: "Create Account | Runexa AI Platform",

  description:
    "Create a Runexa account to access AI agents for legal analysis, finance intelligence, study workflows, and business decision support.",

  keywords: [
    "Runexa signup",
    "AI platform account",
    "AI agents signup",
    "legal AI account",
    "finance AI signup",
    "enterprise AI workspace",
  ],

  alternates: {
    canonical: "https://runexa.ai/register",
  },
};

export default function RegisterPage() {
  return (
    <>
      <RegisterClient />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "WebPage",
            name: "Runexa Registration",
            description:
              "Create a Runexa account to access AI agents and enterprise AI workflows.",
          }),
        }}
      />
    </>
  );
}
