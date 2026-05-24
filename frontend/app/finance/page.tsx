import type { Metadata } from "next";
import FinanceClient from "./FinanceClient";

export const metadata: Metadata = {
  title:
    "AI Personal Finance Coach & Financial Intelligence | Runexa",

  description:
    "Analyze bank statements, detect subscriptions, monitor spending, discover savings opportunities, and receive AI financial coaching with Runexa Finance AI.",

  keywords: [
    "AI finance coach",
    "AI financial analysis",
    "bank statement analysis",
    "personal finance AI",
    "AI budgeting assistant",
    "subscription detection AI",
    "financial intelligence",
    "AI savings analysis",
  ],

  alternates: {
    canonical: "https://runexa.ai/finance",
  },
};

export default function FinancePage() {
  return (
    <>
      <FinanceClient />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            name: "Runexa Finance AI",
            applicationCategory: "FinanceApplication",
            operatingSystem: "Web",
            description:
              "AI financial intelligence platform for bank statement analysis, subscription detection, budgeting, and savings optimization.",
            url: "https://runexa.ai/finance",
            publisher: {
              "@type": "Organization",
              name: "Runexa Systems",
            },
          }),
        }}
      />
    </>
  );
}
