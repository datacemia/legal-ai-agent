import type { Metadata } from "next";
import ResetPasswordClient from "./ResetPasswordClient";

export const metadata: Metadata = {
  title: "Reset Password | Runexa",

  description:
    "Securely reset your Runexa account password and regain access to your AI workspace and enterprise AI agents.",

  keywords: [
    "reset password",
    "Runexa account recovery",
    "AI platform login",
    "secure password reset",
    "enterprise AI account",
    "AI workspace recovery",
  ],

  alternates: {
    canonical: "https://runexa.ai/reset-password",
  },

  openGraph: {
    title: "Reset Password | Runexa",

    description:
      "Securely reset your Runexa account password and regain access to your AI workspace and enterprise AI agents.",

    url: "https://runexa.ai/reset-password",

    siteName: "Runexa Systems",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Password Reset",
      },
    ],

    locale: "en_US",

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Reset Password | Runexa",

    description:
      "Secure password reset for Runexa AI accounts and enterprise AI workspaces.",

    images: ["/og-image.png"],
  },

  robots: {
    index: false,
    follow: false,
  },
};

export default function ResetPasswordPage() {
  return (
    <>
      <ResetPasswordClient />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "Runexa Password Reset",

            description:
              "Secure password reset page for Runexa AI accounts and enterprise AI workspaces.",

            url: "https://runexa.ai/reset-password",

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
