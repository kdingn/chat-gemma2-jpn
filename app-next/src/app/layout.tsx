import Header from "@/components/Header";
import "@/styles/global.css";
import type { Metadata } from "next";
import { Inter, Noto_Sans_JP } from "next/font/google";

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
});

const notoSansJP = Noto_Sans_JP({
  subsets: ["latin"],
  weight: ["400", "700"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "Chat Gemma2 JPN",
  description: "Chat with Gemma2 in Japanese.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja" className={`${inter.className} ${notoSansJP.className}`}>
      <body>
        <Header />
        <div className="content-flex-center">
          <div className="content-width">{children}</div>
        </div>
      </body>
    </html>
  );
}
