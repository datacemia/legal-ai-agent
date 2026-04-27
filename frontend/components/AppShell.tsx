"use client";

import { usePathname } from "next/navigation";
import { useEffect } from "react";
import Navbar from "./Navbar";
import Footer from "./Footer";
import CookieBanner from "./CookieBanner";
import { isAnalyticsAllowed } from "../lib/analytics";

export default function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  const isAuthPage =
    pathname === "/login" ||
    pathname === "/register" ||
    pathname === "/forgot-password" ||
    pathname === "/reset-password";

  // 🔥 Analytics (respect cookie consent)
  useEffect(() => {
    if (isAnalyticsAllowed()) {
      console.log("Analytics enabled ✅");

      // 👉 ici on branchera Google Analytics plus tard
      // ex: window.gtag(...)
    }
  }, []);

  return (
    <>
      {/* Navbar (hidden on auth pages) */}
      {!isAuthPage && <Navbar />}

      {/* Main content */}
      {children}

      {/* Footer (hidden on auth pages) */}
      {!isAuthPage && <Footer />}

      {/* Cookie Banner (global, always visible if needed) */}
      <CookieBanner />
    </>
  );
}