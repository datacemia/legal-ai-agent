import "./globals.css";
import AppShell from "../components/AppShell";
import type { Metadata } from "next";
import { Analytics } from "@vercel/analytics/next";

export const metadata: Metadata = {
  metadataBase: new URL("https://runexa.ai"),

  title: {
    default: "Runexa Systems | Enterprise AI Workspace",
    template: "%s | Runexa Systems",
  },

  description:
    "Runexa Systems provides enterprise AI agents for legal analysis, financial analysis, study workflows, AI document analysis, and business intelligence.",

  keywords: [
    "Runexa Systems",
    "Enterprise AI",
    "AI agents",
    "AI workspace",
    "AI document analysis",
    "AI contract review",
    "AI financial analysis",
    "AI study assistant",
    "AI business intelligence",
    "AI workflow automation",
    "AI infrastructure",
  ],

  authors: [
    {
      name: "Runexa Systems LLC",
    },
  ],

  creator: "Runexa Systems LLC",

  publisher: "Runexa Systems LLC",

  applicationName: "Runexa",

  category: "technology",

  alternates: {
    canonical: "https://runexa.ai",
  },

  icons: {
    icon: "/favicon.ico",
    shortcut: "/favicon.ico",
    apple: "/apple-touch-icon.png",
  },

  openGraph: {
    title: "Runexa Systems | Enterprise AI Workspace",

    description:
      "Specialized AI agents for legal, finance, study, and enterprise business workflows.",

    url: "https://runexa.ai",

    siteName: "Runexa Systems",

    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Runexa Systems AI Workspace",
      },
    ],

    locale: "en_US",

    type: "website",
  },

  twitter: {
    card: "summary_large_image",

    title: "Runexa Systems | Enterprise AI Workspace",

    description:
      "Enterprise AI agents for legal, finance, study, and business workflows.",

    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

const jsonLd = [
  {
    "@context": "https://schema.org",

    "@type": "Organization",

    name: "Runexa Systems LLC",

    url: "https://runexa.ai",

    logo: "https://runexa.ai/logo.png",

    description:
      "Runexa Systems is an enterprise AI workspace with specialized AI agents for legal analysis, finance, study workflows, AI document analysis, and business intelligence.",

    knowsAbout: [
      "Artificial Intelligence",
      "Enterprise AI",
      "Legal AI",
      "Finance AI",
      "Study AI",
      "Business Intelligence",
      "AI Workflow Automation",
    ],
  },

  {
    "@context": "https://schema.org",

    "@type": "WebSite",

    name: "Runexa",

    url: "https://runexa.ai",

    publisher: {
      "@type": "Organization",
      name: "Runexa Systems LLC",
      url: "https://runexa.ai",
    },

    potentialAction: {
      "@type": "SearchAction",

      target:
        "https://runexa.ai/search?q={search_term_string}",

      "query-input":
        "required name=search_term_string",
    },
  },
];

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-slate-50 text-slate-900">
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify(jsonLd),
          }}
        />

        <AppShell>
          {children}
        </AppShell>

        <Analytics />
      </body>
    </html>
  );
}
