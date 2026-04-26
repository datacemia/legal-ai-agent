import "./globals.css";
import AppShell from "../components/AppShell";

export const metadata = {
  title: "Runexa AI",
  description:
    "Specialized AI agents for legal, finance, HR, and business productivity",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-slate-50 text-slate-900">
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
}