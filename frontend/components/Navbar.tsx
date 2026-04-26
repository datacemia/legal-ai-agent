"use client";

import Link from "next/link";
import Image from "next/image";
import { useEffect, useState } from "react";

export default function Navbar() {
  const [isLogged, setIsLogged] = useState(false);

  useEffect(() => {
    checkAuth();
    window.addEventListener("storage", checkAuth);

    return () => {
      window.removeEventListener("storage", checkAuth);
    };
  }, []);

  const checkAuth = () => {
    const token = localStorage.getItem("token");
    setIsLogged(!!token);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setIsLogged(false);
    window.location.href = "/login";
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b border-slate-200/70 bg-white/70 backdrop-blur-md">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">
        
        {/* LEFT */}
        <Link href="/" className="flex items-center gap-3">
          <Image
           src="/runexa-logo.png"
           alt="Runexa"
           width={140}
           height={40}
          />

          <div className="leading-tight">
            
            <div className="text-xs text-slate-500">
              AI agents that get things done
            </div>
          </div>
        </Link>

        {/* RIGHT */}
        <div className="flex items-center gap-5">
          {isLogged ? (
            <>
              <Link
                href="/dashboard"
                className="text-sm font-medium text-slate-600 hover:text-slate-900 transition"
              >
                Dashboard
              </Link>

              <Link
                href="/admin"
                className="text-sm font-medium text-slate-600 hover:text-slate-900 transition"
              >
                Admin
              </Link>

              <button
                onClick={handleLogout}
                className="rounded-xl bg-slate-100 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-200 transition"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link
                href="/login"
                className="text-sm font-medium text-slate-600 hover:text-slate-900 transition"
              >
                Login
              </Link>

              <Link
                href="/register"
                className="rounded-xl bg-slate-900 px-5 py-2 text-sm font-semibold text-white shadow-sm hover:bg-slate-800 transition"
              >
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}