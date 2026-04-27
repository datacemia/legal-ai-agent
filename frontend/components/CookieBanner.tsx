"use client";

import { useEffect, useState } from "react";

export default function CookieBanner() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const consent = localStorage.getItem("cookie-consent");
    if (!consent) {
      setVisible(true);
    }
  }, []);

  const accept = () => {
    localStorage.setItem("cookie-consent", "accepted");
    setVisible(false);
  };

  const decline = () => {
    localStorage.setItem("cookie-consent", "declined");
    setVisible(false);
  };

  if (!visible) return null;

  return (
    <div className="fixed bottom-4 left-1/2 -translate-x-1/2 z-50 w-full max-w-xl px-4">
      <div className="bg-white border shadow-lg rounded-2xl p-5 flex flex-col sm:flex-row items-center gap-4">
        
        <p className="text-sm text-slate-600 text-center sm:text-left">
          We use cookies to improve your experience and ensure security.
        </p>

        <div className="flex gap-3">
          <button
            onClick={decline}
            className="px-4 py-2 text-sm bg-slate-100 rounded-lg"
          >
            Decline
          </button>

          <button
            onClick={accept}
            className="px-4 py-2 text-sm bg-slate-900 text-white rounded-lg"
          >
            Accept
          </button>
        </div>
      </div>
    </div>
  );
}