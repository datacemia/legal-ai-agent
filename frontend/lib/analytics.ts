export function getCookieConsent() {
  if (typeof window === "undefined") return null;

  try {
    const consent = localStorage.getItem("cookie-consent");
    return consent ? JSON.parse(consent) : null;
  } catch {
    return null;
  }
}

export function isAnalyticsAllowed() {
  const consent = getCookieConsent();
  return consent?.analytics === true;
}