import "./globals.css";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

export const metadata = {
  title: "Runexa AI",
  description: "Specialized AI agents for legal, finance, HR, and business productivity",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-slate-50 text-slate-900">
        <Navbar />
        {children}
        <Footer />
      </body>
    </html>
  );
}