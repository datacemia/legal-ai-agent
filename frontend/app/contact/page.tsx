import type { Metadata } from "next";
import ContactClient from "./ContactClient";

export const metadata: Metadata = {
  title: "Contact Sales | Runexa",
  description:
    "Contact Runexa sales to get a tailored AI solution for your business, team, or enterprise workflow.",
  alternates: {
    canonical: "https://runexa.ai/contact",
  },
};

export default function ContactPage() {
  return <ContactClient />;
}
