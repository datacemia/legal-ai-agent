import type { Metadata } from "next";
import LoginClient from "./LoginClient";

export const metadata: Metadata = {
  title: "Login | Runexa AI Platform",

  description:
    "Login to Runexa and access AI agents for legal analysis, finance intelligence, study workflows, and enterprise AI systems.",

  keywords: [
    "Runexa login",
    "AI platform login",
    "enterprise AI workspace",
    "AI agents login",
    "legal AI login",
    "finance AI login",
  ],

  alternates: {
    canonical: "https://runexa.ai/login",
  },
};

export default function LoginPage() {
  return (
    <>
      <LoginClient />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "WebPage",
            name: "Runexa Login",
            description:
              "Secure login page for Runexa AI agents and enterprise AI workspace.",
          }),
        }}
      />
    </>
  );
}
