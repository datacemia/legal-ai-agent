import { MetadataRoute } from "next";

const routes = [
  "",
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
    changeFrequency: "weekly",
    priority: route === "" ? 1 : 0.8,
  }));
}