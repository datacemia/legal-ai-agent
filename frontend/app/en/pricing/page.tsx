import type { Metadata } from "next";
import PricingClient from "../../pricing/PricingClient";

const siteUrl = "https://runexa.ai";

export const metadata: Metadata = {
  title: "Runexa Pricing | AI Agents, Credits & API Plans",

  description:
    "Compare Runexa AI pricing plans including AI trials, global credits, Pro subscriptions, and enterprise API workflows.",

  keywords: [
  "AI pricing",
  "AI agents pricing",
  "legal AI pricing",
  "finance AI pricing",
  "AI API pricing",
  "enterprise AI pricing",
  "Runexa pricing",
  "AI credits",
  "AI subscriptions",

  "Runexa pricing plans",
  "Runexa subscriptions",
  "AI platform pricing",
  "AI software pricing",
  "enterprise AI plans",
  "AI service pricing",
  "AI usage pricing",
  "pay as you go AI",
  "AI credit pricing",
  "AI credit packages",
  "AI subscription plans",
  "monthly AI subscription",
  "annual AI subscription",
  "AI billing",
  "enterprise billing",
  "SaaS pricing",
  "SaaS subscription plans",
  "AI API pricing plans",
  "developer pricing",
  "enterprise API pricing",
  "Legal AI pricing",
  "Finance AI pricing",
  "Study AI pricing",
  "Business AI pricing",
  "Runexa Legal Agent pricing",
  "Runexa Finance Coach pricing",
  "Runexa Study Agent pricing",
  "Runexa Business Decision Agent pricing",
  "AI platform subscriptions",
  "business AI pricing",
  "AI automation pricing",
  "enterprise software pricing",
  "AI infrastructure pricing",
  "usage-based pricing",
  "consumption-based pricing",
  "AI cost calculator",
  "AI platform costs",
  "enterprise AI costs",
  "Runexa API pricing",
  "Enterprise AI Pricing",
],
  alternates: {
    canonical: "https://runexa.ai/en/pricing",
    languages: {
      en: `${siteUrl}/en/pricing`,
      fr: `${siteUrl}/fr/pricing`,
      ar: `${siteUrl}/ar/pricing`,
      "x-default": `${siteUrl}/pricing`,
    },
  },

  openGraph: {
    title: "Runexa Pricing | AI Agents, Credits & API Plans",

    description:
      "Compare Runexa AI pricing plans including AI trials, global credits, Pro subscriptions, and enterprise API workflows.",

    url: "https://runexa.ai/en/pricing",

    siteName: "Runexa Systems LLC",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Pricing",
      },
    ],

    locale: "en_US",

    alternateLocale: ["fr_FR", "ar_AR"],

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Runexa Pricing | AI Agents, Credits & API Plans",

    description:
      "Compare AI subscriptions, global credits, API workflows, and enterprise pricing plans from Runexa.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function PricingPage() {
  return (
    <>
      <PricingClient initialLanguage="en" lockInitialLanguage />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",

            "@type": "SoftwareApplication",

            name: "Runexa Pricing",

            applicationCategory: "BusinessApplication",

            operatingSystem: "Web",

            description:
              "AI platform for legal analysis, finance intelligence, study workflows, and business decision support.",

            url: "https://runexa.ai/en/pricing",

            inLanguage: "en",

            publisher: {
              "@type": "Organization",
              name: "Runexa Systems LLC",
              url: siteUrl,
            },

            offers: [
              {
                "@type": "Offer",

                name: "Pro",

                price: "49",

                priceCurrency: "USD",
              },
            ],

            knowsAbout: [
              "AI Pricing",
              "AI Agents Pricing",
              "AI Credits",
              "AI API Plans",
              "Enterprise AI Pricing",
              "AI Subscriptions",
            ],
          }),
        }}
      />
    </>
  );
}
