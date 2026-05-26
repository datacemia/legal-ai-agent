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
    "AI workspace registration",
  ],

  alternates: {
    canonical: "https://runexa.ai/register",
  },

  openGraph: {
    title: "Create Account | Runexa AI Platform",

    description:
      "Create a Runexa account to access AI agents for legal analysis, finance intelligence, study workflows, and business decision support.",

    url: "https://runexa.ai/register",

    siteName: "Runexa Systems",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Registration",
      },
    ],

    locale: "en_US",

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Create Account | Runexa AI Platform",

    description:
      "Create a Runexa account and access AI agents, enterprise workflows, and intelligent business tools.",

    images: ["/og-image.png"],
  },

  robots: {
    index: false,
    follow: false,
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

            url: "https://runexa.ai/register",

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
