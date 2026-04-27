"use client";

import { useEffect, useState } from "react";
import Script from "next/script";
import { isAnalyticsAllowed } from "../lib/analytics";

const GA_ID = process.env.NEXT_PUBLIC_GA_ID;

export default function AnalyticsProvider() {
  const [enabled, setEnabled] = useState(false);

  useEffect(() => {
    const checkConsent = () => {
      setEnabled(isAnalyticsAllowed());
    };

    checkConsent();

    window.addEventListener("cookie-consent-change", checkConsent);

    return () => {
      window.removeEventListener("cookie-consent-change", checkConsent);
    };
  }, []);

  // 🔒 sécurité : ne charge rien si pas d'ID
  if (!enabled || !GA_ID) return null;

  return (
    <>
      <Script
        src={`https://www.googletagmanager.com/gtag/js?id=${GA_ID}`}
        strategy="afterInteractive"
      />

      <Script id="ga-init" strategy="afterInteractive">
        {`
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          window.gtag = gtag;

          gtag('js', new Date());
          gtag('config', '${GA_ID}', {
            page_path: window.location.pathname,
          });
        `}
      </Script>
    </>
  );
}