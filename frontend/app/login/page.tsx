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
    "secure AI workspace",
  ],

  alternates: {
    canonical: "https://runexa.ai/login",
  },

  openGraph: {
    title: "Login | Runexa AI Platform",

    description:
      "Secure login access for Runexa AI agents, enterprise AI workspace, legal AI, finance AI, and intelligent workflows.",

    url: "https://runexa.ai/login",

    siteName: "Runexa Systems",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Login",
      },
    ],

    locale: "en_US",

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Login | Runexa AI Platform",

    description:
      "Secure login page for Runexa AI agents, finance AI, legal AI, and enterprise AI workspace.",

    images: ["/og-image.png"],
  },

  robots: {
    index: false,
    follow: false,
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

            url: "https://runexa.ai/login",

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
