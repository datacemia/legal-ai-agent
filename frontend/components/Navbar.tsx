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
    <nav className="bg-white border-b px-6 py-4 flex justify-between items-center">
      
      {/* 🔥 LOGO + NAME + SLOGAN */}
      <Link href="/" className="flex items-center gap-3">
        <Image
          src="/runexa-logo.png"
          alt="Runexa"
          width={60}   // 👈 augmenté (avant 36)
          height={60}
          className="object-contain"
        />

        <div className="leading-tight">
          <div className="font-bold text-lg">Runexa</div>
          <div className="text-xs text-gray-500">
            AI agents that get things done
          </div>
        </div>
      </Link>

      <div className="flex items-center gap-4">
        {isLogged ? (
          <>
            <a href="/dashboard" className="text-gray-700">
              Dashboard
            </a>

            <a href="/admin" className="text-gray-700">
              Admin
            </a>

            <button
              onClick={handleLogout}
              className="px-4 py-2 bg-gray-200 rounded-lg"
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <Link href="/login" className="text-gray-700">
              Login
            </Link>

            <Link
              href="/register"
              className="px-4 py-2 bg-black text-white rounded-lg"
            >
              Register
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}