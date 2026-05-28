import type { Metadata } from "next";
import AIDisclaimerClient from "./AIDisclaimerClient";

export const revalidate = 3600;

export const metadata: Metadata = {
  title: "AI Disclaimer & Transparency | Runexa",

  description:
    "Review Runexa Systems AI disclaimer and transparency information regarding AI-generated outputs, limitations, human review requirements, and enterprise AI usage.",

  keywords: [
    "AI disclaimer",
    "AI transparency",
    "AI limitations",
    "AI compliance",
    "enterprise AI disclaimer",
    "AI governance",
    "AI risk disclosure",
    "Runexa AI policy",
  ],

  alternates: {
    canonical: "https://runexa.ai/legal/ai-disclaimer",
  },

  openGraph: {
    title: "AI Disclaimer & Transparency | Runexa",

    description:
      "Review AI transparency, limitations, and human review requirements for Runexa Systems AI services and enterprise platforms.",

    url: "https://runexa.ai/legal/ai-disclaimer",

    siteName: "Runexa Systems LLC",

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
      "Review AI limitations, transparency notices, and human review requirements for Runexa AI systems.",

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
              "AI disclaimer and transparency information governing the use of Runexa AI systems, enterprise platforms, APIs, and intelligent services.",

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
