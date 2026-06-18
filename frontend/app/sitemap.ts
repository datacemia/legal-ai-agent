import { MetadataRoute } from "next";

const routes = [
  "",

  // Languages
  "/en",
  "/fr",
  "/ar",

  "/en/legal-ai",
  "/fr/legal-ai",
  "/ar/legal-ai",

  "/en/business-ai",
  "/fr/business-ai",
  "/ar/business-ai",

  "/en/finance-ai",
  "/fr/finance-ai",
  "/ar/finance-ai",

  "/en/study-ai",
  "/fr/study-ai",
  "/ar/study-ai",

  "/en/enterprise-ai",
  "/fr/enterprise-ai",
  "/ar/enterprise-ai",

  "/en/business",
  "/fr/business",
  "/ar/business",

  "/en/upload",
  "/fr/upload",
  "/ar/upload",

  "/upload",
  "/legal-ai",
  "/finance-ai",
  "/study-ai",
  "/business-ai",
  "/enterprise-ai",

  "/enterprise",
  "/business",
  "/finance",
  "/study",

  "/blog",
  "/blog/ai-contract-analysis",
  "/blog/ai-finance-analysis",
  "/blog/ai-study-assistant",
  "/blog/enterprise-ai-workflows",
  "/blog/ai-business-intelligence",

  "/developers",
  "/api",
  "/api-dashboard",
  "/docs",
  "/pricing",

  "/contact",
  "/contact-entreprise/contact",

  "/security",
  "/privacy",
  "/terms",

  "/products/ai-legal-agent/terms",

  "/legal/acceptable-use",
  "/legal/ai-disclaimer",
  "/legal/cookies",
  "/legal/refunds",
  "/legal/company",
];

export default function sitemap(): MetadataRoute.Sitemap {
  return routes.map((route) => ({
    url: `https://runexa.ai${route}`,
    lastModified: new Date(),

    changeFrequency:
      route === ""
        ? "daily"
        : ["/en", "/fr", "/ar"].includes(route)
        ? "weekly"
        : "weekly",

    priority:
      route === ""
        ? 1.0
        : ["/en", "/fr", "/ar"].includes(route)
        ? 0.95
        : 0.8,
  }));
}