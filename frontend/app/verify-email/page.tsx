import type { Metadata } from "next";
import VerifyEmailClient from "./VerifyEmailClient";

export const metadata: Metadata = {
  title: "Verify Email | Runexa",
  description: "Verify your Runexa account email address.",
  alternates: {
    canonical: "https://runexa.ai/verify-email",
  },
};

export default function VerifyEmailPage() {
  return <VerifyEmailClient />;
}
