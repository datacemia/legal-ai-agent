"use client";

import { useEffect } from "react";

export default function OAuthSuccess() {
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);

    const token = params.get("token");
    const role = params.get("role");

    if (token) {
      localStorage.setItem("token", token);
      localStorage.setItem("role", role || "user");

      if (role === "admin" || role === "business") {
        window.location.href = "/dashboard";
      } else {
        window.location.href = "/upload";
      }
    }
  }, []);

  return <p>Logging you in...</p>;
}