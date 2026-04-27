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

  const savePreferences = (value: {
    essential: boolean;
    analytics: boolean;
    marketing: boolean;
  }) => {
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
    <div className="fixed bottom-4 left-1/2 z-50 w-full max-w-2xl -translate-x-1/2 px-4">
      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xl">
        {!showSettings ? (
          <div className="flex flex-col gap-4">
            <p className="text-center text-sm leading-6 text-slate-600 sm:text-left">
              We use cookies to improve your experience, analyze traffic, and
              ensure security.{" "}
              <Link
                href="/privacy"
                className="font-medium text-slate-900 underline hover:text-black"
              >
                Privacy Policy
              </Link>{" "}
              and{" "}
              <Link
                href="/terms"
                className="font-medium text-slate-900 underline hover:text-black"
              >
                Terms
              </Link>
              . You can change your preferences at any time.
            </p>

            <div className="flex flex-wrap justify-center gap-3 sm:justify-end">
              <button
                onClick={rejectAll}
                className="rounded-xl bg-slate-100 px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-200"
              >
                Reject all
              </button>

              <button
                onClick={() => setShowSettings(true)}
                className="rounded-xl bg-slate-200 px-4 py-2 text-sm font-medium text-slate-800 transition hover:bg-slate-300"
              >
                Preferences
              </button>

              <button
                onClick={acceptAll}
                className="rounded-xl bg-slate-950 px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-800"
              >
                Accept all
              </button>
            </div>
          </div>
        ) : (
          <div className="flex flex-col gap-5">
            <div>
              <h3 className="text-base font-semibold text-slate-950">
                Cookie Preferences
              </h3>
              <p className="mt-1 text-sm text-slate-500">
                Manage optional cookies. Essential cookies are always active.
              </p>
            </div>

            <div className="space-y-4 text-sm">
              <div className="flex items-center justify-between gap-4 rounded-xl border border-slate-200 p-4">
                <div>
                  <p className="font-medium text-slate-900">
                    Essential cookies
                  </p>
                  <p className="mt-1 text-slate-500">
                    Required for security, login, and core functionality.
                  </p>
                </div>
                <span className="shrink-0 rounded-full bg-green-50 px-3 py-1 text-xs font-medium text-green-700">
                  Always active
                </span>
              </div>

              <label className="flex items-center justify-between gap-4 rounded-xl border border-slate-200 p-4">
                <div>
                  <p className="font-medium text-slate-900">
                    Analytics cookies
                  </p>
                  <p className="mt-1 text-slate-500">
                    Help us understand usage and improve the product.
                  </p>
                </div>
                <input
                  type="checkbox"
                  checked={preferences.analytics}
                  onChange={() =>
                    setPreferences({
                      ...preferences,
                      analytics: !preferences.analytics,
                    })
                  }
                  className="h-4 w-4 shrink-0"
                />
              </label>

              <label className="flex items-center justify-between gap-4 rounded-xl border border-slate-200 p-4">
                <div>
                  <p className="font-medium text-slate-900">
                    Marketing cookies
                  </p>
                  <p className="mt-1 text-slate-500">
                    Help personalize communication and measure campaigns.
                  </p>
                </div>
                <input
                  type="checkbox"
                  checked={preferences.marketing}
                  onChange={() =>
                    setPreferences({
                      ...preferences,
                      marketing: !preferences.marketing,
                    })
                  }
                  className="h-4 w-4 shrink-0"
                />
              </label>
            </div>

            <div className="flex flex-wrap justify-end gap-3">
              <button
                onClick={() => setShowSettings(false)}
                className="rounded-xl bg-slate-100 px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-200"
              >
                Back
              </button>

              <button
                onClick={rejectAll}
                className="rounded-xl bg-slate-200 px-4 py-2 text-sm font-medium text-slate-800 transition hover:bg-slate-300"
              >
                Reject all
              </button>

              <button
                onClick={saveCustom}
                className="rounded-xl bg-slate-950 px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-800"
              >
                Save preferences
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}