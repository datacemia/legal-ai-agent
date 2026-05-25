import type { Metadata } from "next";
import ActivateClient from "./ActivateClient";

export const metadata: Metadata = {
  title: "Activate Account | Runexa",
  description: "Activate your Runexa account.",
  alternates: {
    canonical: "https://runexa.ai/activate",
  },
};

export default function ActivatePage() {
  return <ActivateClient />;
}
