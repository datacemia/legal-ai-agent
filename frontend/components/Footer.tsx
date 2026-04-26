"use client";

import Link from "next/link";

export default function Footer() {
  return (
    <footer className="bg-slate-950 text-white px-6 py-14">
      <div className="max-w-7xl mx-auto">
        
        <div className="grid gap-10 md:grid-cols-4">
          
          {/* LEFT */}
          <div>
            <h3 className="text-2xl font-bold">Runexa</h3>
            <p className="mt-4 text-sm text-slate-400 leading-6">
              Specialized AI agents for legal, finance, HR, and business productivity.
            </p>
          </div>

          {/* PRODUCTS */}
          <div>
            <h4 className="font-semibold">Products</h4>
            <div className="mt-4 space-y-3 text-sm text-slate-400">
              <p>Legal Agent <span className="text-green-400">· Available</span></p>
              <p>Finance Agent <span className="text-slate-500">· Coming soon</span></p>
              <p>HR Agent <span className="text-slate-500">· Coming soon</span></p>
              <p>Business Agent <span className="text-slate-500">· Coming soon</span></p>
            </div>
          </div>

          {/* PLATFORM */}
          <div>
            <h4 className="font-semibold">Platform</h4>
            <div className="mt-4 space-y-3 text-sm text-slate-400">
              <a href="#agents" className="block hover:text-white transition">
                Explore agents
              </a>
              <Link href="/upload" className="block hover:text-white transition">
                Try Legal Agent
              </Link>
              <Link href="/login" className="block hover:text-white transition">
                Login
              </Link>
              <Link href="/register" className="block hover:text-white transition">
                Register
              </Link>
            </div>
          </div>

          {/* ABOUT */}
          <div>
            <h4 className="font-semibold">About</h4>
            <p className="mt-4 text-sm text-slate-400 leading-6">
              Runexa AI is a platform of specialized AI agents for legal,
              finance, HR, and business productivity.
            </p>

            <p className="mt-4 text-sm font-medium text-blue-400">
              Developed by Dr. Rachid Ejjami
            </p>
          </div>

        </div>

        {/* BOTTOM */}
        <div className="mt-12 border-t border-slate-800 pt-6 flex flex-col gap-4 text-sm text-slate-500 md:flex-row md:items-center md:justify-between">
          
          <p>© 2025 Runexa AI. All rights reserved.</p>

          <div className="flex gap-5">
            <a href="#" className="hover:text-white transition">
              Privacy Policy
            </a>
            <a href="#" className="hover:text-white transition">
              Terms of Service
            </a>
            <a href="#" className="hover:text-white transition">
              Contact
            </a>
          </div>

        </div>

      </div>
    </footer>
  );
}