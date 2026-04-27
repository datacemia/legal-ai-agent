"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

export default function CookieBanner() {
  const [visible, setVisible] = useState(false);
  const [showSettings, setShowSettings] = useState(false);

  const [preferences, setPreferences] = useState({
    analytics: false,
    marketing: false,
  });

  useEffect(() => {
    const consent = localStorage.getItem("cookie-consent");
    if (!consent) {
      setVisible(true);
    }
  }, []);

  const savePreferences = (value: any) => {
    localStorage.setItem("cookie-consent", JSON.stringify(value));
    setVisible(false);
    setShowSettings(false);
  };

  const acceptAll = () => {
    savePreferences({
      essential: true,
      analytics: true,
      marketing: true,
    });
  };

  const rejectAll = () => {
    savePreferences({
      essential: true,
      analytics: false,
      marketing: false,
    });
  };

  const saveCustom = () => {
    savePreferences({
      essential: true,
      ...preferences,
    });
  };

  if (!visible) return null;

  return (
    <div className="fixed bottom-4 left-1/2 -translate-x-1/2 z-50 w-full max-w-xl px-4">
      <div className="bg-white border shadow-lg rounded-2xl p-5 flex flex-col gap-4">

        {!showSettings ? (
          <>
            <p className="text-sm text-slate-600 text-center sm:text-left leading-5">
              We use cookies to improve your experience.{" "}
              <Link href="/privacy" className="underline font-medium">
                Privacy Policy
              </Link>{" "}
              and{" "}
              <Link href="/terms" className="underline font-medium">
                Terms
              </Link>.
            </p>

            <div className="flex flex-wrap gap-3 justify-center sm:justify-end">
              <button
                onClick={rejectAll}
                className="px-4 py-2 text-sm bg-slate-100 rounded-lg"
              >
                Reject all
              </button>

              <button
                onClick={() => setShowSettings(true)}
                className="px-4 py-2 text-sm bg-slate-200 rounded-lg"
              >
                Manage
              </button>

              <button
                onClick={acceptAll}
                className="px-4 py-2 text-sm bg-slate-900 text-white rounded-lg"
              >
                Accept all
              </button>
            </div>
          </>
        ) : (
          <>
            <h3 className="text-sm font-semibold">Cookie Preferences</h3>

            <div className="space-y-3 text-sm text-slate-600">
              <div className="flex justify-between items-center">
                <span>Essential cookies</span>
                <span className="text-green-600 font-medium">Always active</span>
              </div>

              <div className="flex justify-between items-center">
                <span>Analytics</span>
                <input
                  type="checkbox"
                  checked={preferences.analytics}
                  onChange={() =>
                    setPreferences({
                      ...preferences,
                      analytics: !preferences.analytics,
                    })
                  }
                />
              </div>

              <div className="flex justify-between items-center">
                <span>Marketing</span>
                <input
                  type="checkbox"
                  checked={preferences.marketing}
                  onChange={() =>
                    setPreferences({
                      ...preferences,
                      marketing: !preferences.marketing,
                    })
                  }
                />
              </div>
            </div>

            <div className="flex gap-3 justify-end">
              <button
                onClick={() => setShowSettings(false)}
                className="px-4 py-2 text-sm bg-slate-100 rounded-lg"
              >
                Back
              </button>

              <button
                onClick={saveCustom}
                className="px-4 py-2 text-sm bg-slate-900 text-white rounded-lg"
              >
                Save preferences
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}