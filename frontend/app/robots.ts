import { MetadataRoute } from "next";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: "*",

        allow: "/",

        disallow: [
          "/admin",
          "/api",
          "/dashboard",
          "/entreprises/dashboard",

          "/login",
          "/register",
          "/reset-password",
          "/verify-email",
          "/oauth-success",

          "/settings",
          "/billing",
        ],
      },
    ],

    sitemap: "https://runexa.ai/sitemap.xml",

    host: "https://runexa.ai",
  };
}
