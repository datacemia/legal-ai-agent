import type { Metadata } from "next";
import VerifyEmailClient from "./VerifyEmailClient";

export const metadata: Metadata = {
  title: "Verify Email | Runexa",

  description:
    "Verify your Runexa account email address to access AI agents and enterprise AI workspaces.",

  keywords: [
    "verify email",
    "Runexa email verification",
    "AI platform verification",
    "account verification",
    "enterprise AI account",
    "AI workspace activation",
  ],

  alternates: {
    canonical: "https://runexa.ai/verify-email",
  },

  openGraph: {
    title: "Verify Email | Runexa",

    description:
      "Verify your Runexa account email address to access AI agents and enterprise AI workspaces.",

    url: "https://runexa.ai/verify-email",

    siteName: "Runexa Systems",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Email Verification",
      },
    ],

    locale: "en_US",

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Verify Email | Runexa",

    description:
      "Verify your Runexa account email address and activate your AI workspace.",

    images: ["/og-image.png"],
  },

  robots: {
    index: false,
    follow: false,
  },
};

export default function VerifyEmailPage() {
  return (
    <>
      <VerifyEmailClient />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "Runexa Email Verification",

            description:
              "Secure email verification page for Runexa AI accounts and enterprise AI workspaces.",

            url: "https://runexa.ai/verify-email",

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
