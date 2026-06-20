import type { Metadata } from "next";
import EnterpriseClient from "./EnterpriseClient";

export const metadata: Metadata = {
  title:
    "Enterprise AI Agents & Custom AI Workflows | Runexa",

  description:
    "Runexa builds enterprise AI agents for legal analysis, finance intelligence, HR automation, business workflows, and document processing.",

  keywords: [
  "enterprise AI",
  "custom AI agents",
  "AI workflows",
  "enterprise AI platform",
  "business AI automation",
  "AI agents for companies",
  "legal AI enterprise",
  "finance AI enterprise",

  "Runexa enterprise AI",
  "enterprise AI solutions",
  "AI platform for enterprises",
  "specialized AI agents",
  "custom AI systems",
  "enterprise AI automation",
  "AI-powered business processes",
  "workflow automation AI",
  "business process automation",
  "AI workspace",
  "enterprise AI workspace",
  "organizational AI",
  "AI knowledge management",
  "AI document processing",
  "AI document analysis",
  "enterprise decision support",
  "AI-powered decision making",
  "business intelligence AI",
  "enterprise business intelligence",
  "AI strategy platform",
  "digital transformation",
  "AI transformation",
  "corporate AI platform",
  "AI productivity platform",
  "secure AI platform",
  "enterprise AI compliance",
  "responsible AI",
  "AI governance",
  "cloud AI infrastructure",
  "scalable AI infrastructure",
  "AI operations platform",
  "enterprise workflow intelligence",
  "legal AI for enterprises",
  "finance AI for enterprises",
  "study AI for organizations",
  "business decision AI",
  "Runexa Legal Agent",
  "Runexa Finance Coach",
  "Runexa Study Agent",
  "Runexa Business Decision Agent",
  "Enterprise AI Platform",
],

  alternates: {
    canonical: "https://runexa.ai/enterprise",
  },
};

export default function EnterprisePage() {
  return (
    <>
      <EnterpriseClient />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "Organization",
            name: "Runexa Systems",
            url: "https://runexa.ai",
            description:
              "Enterprise AI platform building custom AI agents for legal, finance, HR, business, and document workflows.",
          }),
        }}
      />
    </>
  );
}
