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

  "/en/legal/refunds",
  "/fr/legal/refunds",
  "/ar/legal/refunds",

  "/en/blog/ai-business-intelligence",
  "/fr/blog/ai-business-intelligence",
  "/ar/blog/ai-business-intelligence",

  "/en/security",
  "/fr/security",
  "/ar/security",

  "/en/privacy",
  "/fr/privacy",
  "/ar/privacy",

  "/en/products/ai-legal-agent/terms",
  "/fr/products/ai-legal-agent/terms",
  "/ar/products/ai-legal-agent/terms",

  "/en/upload",
  "/fr/upload",
  "/ar/upload",

  "/en/labs/agent-0",
  "/fr/labs/agent-0",
  "/ar/labs/agent-0",

  "/en/legal/cookies",
  "/fr/legal/cookies",
  "/ar/legal/cookies",

  "/en/legal/company",
  "/fr/legal/company",
  "/ar/legal/company",

  "/en/legal/ai-disclaimer",
  "/fr/legal/ai-disclaimer",
  "/ar/legal/ai-disclaimer",

  "/en/docs",
  "/fr/docs",
  "/ar/docs",
  "/en/legal/acceptable-use",
  "/fr/legal/acceptable-use",
  "/ar/legal/acceptable-use",

  "/en/terms",
  "/fr/terms",
  "/ar/terms",

  "/en/api",
  "/fr/api",
  "/ar/api",

  "/en/developers",
  "/fr/developers",
  "/ar/developers",

  "/en/finance",
  "/fr/finance",
  "/ar/finance",

  "/en/pricing",
  "/fr/pricing",
  "/ar/pricing",

  "/en/study",
  "/fr/study",
  "/ar/study",

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