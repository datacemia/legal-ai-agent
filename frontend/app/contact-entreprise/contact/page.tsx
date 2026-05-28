import type { Metadata } from "next";
import EnterpriseContactClient from "./EnterpriseContactClient";

export const metadata: Metadata = {
  title: "Enterprise AI Consultation | Runexa",
  description:
    "Contact Runexa to build custom enterprise AI agents, workflows, and operational intelligence systems.",
  alternates: {
    canonical: "https://runexa.ai/contact-entreprise/contact",
  },
};

export default function EnterpriseContactPage() {
  return <EnterpriseContactClient />;
}
