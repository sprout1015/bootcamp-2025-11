import "./globals.css";
import {Metadata} from "next";

export const metadata: Metadata = {
    title: "Employee",
    description: "The Employee application"
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body>
        {children}
      </body>
    </html>
  );
}
