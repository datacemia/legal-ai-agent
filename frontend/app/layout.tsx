import "./globals.css";
import Navbar from "../components/Navbar";

export const metadata = {
  title: "Legal AI Agent",
  description: "AI contract analysis tool",
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
      </body>
    </html>
  );
}