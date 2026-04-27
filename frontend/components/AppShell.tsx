"use client";

import { usePathname } from "next/navigation";
import Navbar from "./Navbar";
import Footer from "./Footer";
import CookieBanner from "./CookieBanner";
import AnalyticsProvider from "./AnalyticsProvider";

export default function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  const isAuthPage =
    pathname === "/login" ||
    pathname === "/register" ||
    pathname === "/forgot-password" ||
    pathname === "/reset-password";

  return (
    <>
      {/* Navbar (hidden on auth pages) */}
      {!isAuthPage && <Navbar />}

      {/* Main content */}
      {children}

      {/* Footer (hidden on auth pages) */}
      {!isAuthPage && <Footer />}

      {/* Cookie Banner */}
      <CookieBanner />

      {/* 🔥 Google Analytics (only if consent = true) */}
      <AnalyticsProvider />
    </>
  );
}