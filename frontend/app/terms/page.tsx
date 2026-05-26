import type { Metadata } from "next";
import TermsClient from "./TermsClient";

export const metadata: Metadata = {
  title: "Terms of Service | Runexa",

  description:
    "Terms of Service governing the use of Runexa AI agents, APIs, enterprise workflows, credits, subscriptions, and AI-powered services.",

  keywords: [
    "terms of service",
    "AI platform terms",
    "Runexa terms",
    "AI SaaS terms",
    "AI API terms",
    "enterprise AI terms",
    "AI subscriptions",
    "AI credits",
  ],

  alternates: {
    canonical: "https://runexa.ai/terms",
  },

  openGraph: {
    title: "Runexa Terms of Service",

    description:
      "Terms governing the use of Runexa AI systems, APIs, and enterprise AI workflows.",

    url: "https://runexa.ai/terms",

    siteName: "Runexa Systems",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Terms of Service",
      },
    ],

    locale: "en_US",

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Runexa Terms of Service",

    description:
      "Terms governing the use of Runexa AI systems, APIs, and enterprise workflows.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function TermsPage() {
  return (
    <>
      <TermsClient />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "WebPage",

            name: "Runexa Terms of Service",

            description:
              "Terms governing Runexa AI agents, APIs, enterprise workflows, and AI-powered services.",

            url: "https://runexa.ai/terms",

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
