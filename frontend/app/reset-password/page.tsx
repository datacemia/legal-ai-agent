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
  ],

  alternates: {
    canonical: "https://runexa.ai/reset-password",
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
          }),
        }}
      />
    </>
  );
}
