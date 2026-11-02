import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "HeyTrip | AI Trip Planner",
  description:
    "Plan your next adventure with HeyTrip, your AI-powered travel companion.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
