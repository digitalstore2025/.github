import "./globals.css";
import type { Metadata } from "next";
import { PersistentPlayer } from "../components/PersistentPlayer";

export const metadata: Metadata = {
  title: "Quds Radio AI",
  description: "منصة إذاعية إخبارية مدعومة بالذكاء الاصطناعي"
};

export default function RootLayout({ children }: { children: React.ReactNode }): JSX.Element {
  return (
    <html lang="ar" dir="rtl">
      <body>
        <main>{children}</main>
        <PersistentPlayer />
      </body>
    </html>
  );
}
