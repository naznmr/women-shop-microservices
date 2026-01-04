import "./globals.css";
import Image from "next/image";
import TopbarActions from "./components/TopbarActions";

export const metadata = {
  title: "Rimberio | فروشگاه لباس زنانه",
  description: "فروشگاه لباس زنانه برای چهار فصل",
  icons: {
    icon: "/favicon.ico",
    apple: "/apple-touch-icon.png",
  },
};

export default function RootLayout({ children }) {
  return (
    <html lang="fa" dir="rtl">
      <body>
        <header className="topbar">
          <div className="topbar__inner">
            <a className="brand" href="/">
              <span className="brand__logo">
                <Image src="/logo.png" alt="Rimberio" width={42} height={42} priority />
              </span>
              <span className="brand__name">
                <span className="brand__title">Rimberio</span>
                <span className="brand__subtitle">فروشگاه لباس زنانه</span>
              </span>
            </a>
          
            <nav className="nav">
              <a className="nav__link" href="/cart">سبد خرید</a>
              <TopbarActions />
            </nav>
          </div>
        </header>

        <main className="container">{children}</main>
      </body>
    </html>
  );
}