import type { Metadata } from "next";
import DevelopersClient from "./DevelopersClient";

export const metadata: Metadata = {
  title: "Developers & AI APIs | Runexa",
  description:
    "Build AI-powered workflows with Runexa APIs for legal analysis, finance intelligence, study automation, and business decision support.",
  alternates: {
    canonical: "https://runexa.ai/developers",
  },
};

export default function DevelopersPage() {
  return <DevelopersClient />;
}
