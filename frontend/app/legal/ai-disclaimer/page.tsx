import type { Metadata } from "next";
import AIDisclaimerClient from "./AIDisclaimerClient";

export const metadata: Metadata = {
  title: "AI Disclaimer & Transparency | Runexa",

  description:
    "Transparency and AI limitation disclosures for Runexa AI systems, APIs, workflows, and intelligent agents.",

  keywords: [
    "AI disclaimer",
    "AI transparency",
    "AI limitations",
    "AI policy",
    "AI compliance",
    "enterprise AI disclaimer",
    "AI governance",
    "Runexa AI",
  ],

  alternates: {
    canonical: "https://runexa.ai/legal/ai-disclaimer",
  },

  openGraph: {
    title: "AI Disclaimer & Transparency | Runexa",

    description:
      "Review AI transparency notices, limitations, and enterprise AI governance information for Runexa AI systems.",

    url: "https://runexa.ai/legal/ai-disclaimer",

    siteName: "Runexa Systems",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa AI Disclaimer",
      },
    ],

    locale: "en_US",

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "AI Disclaimer & Transparency | Runexa",

    description:
      "Review AI transparency, limitations, and governance information for Runexa AI systems and enterprise workflows.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function AIDisclaimerPage() {
  return (
    <>
      <AIDisclaimerClient />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "Runexa AI Disclaimer & Transparency",

            description:
              "AI transparency and limitation disclosures for Runexa AI systems, APIs, enterprise workflows, and intelligent services.",

            url: "https://runexa.ai/legal/ai-disclaimer",

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: "https://runexa.ai",
            },
          }),
        }}
      />
    </>
  );
}
