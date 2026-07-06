import type { Metadata } from "next";
import type { ReactNode } from "react";

export const metadata: Metadata = {
  title: "Aegis — Investment Theses",
  description:
    "Form investment theses as falsifiable claims — what you believe, why, and what would prove you wrong.",
};

export default function RootLayout({
  children,
}: {
  children: ReactNode;
}): React.JSX.Element {
  return (
    <html lang="en">
      <body
        style={{
          fontFamily:
            "system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif",
          margin: 0,
          background: "#f6f7f9",
          color: "#1a1a1a",
        }}
      >
        <div style={{ maxWidth: 820, margin: "0 auto", padding: "24px 16px" }}>
          <header style={{ marginBottom: 24 }}>
            <a href="/" style={{ textDecoration: "none", color: "inherit" }}>
              <h1 style={{ margin: 0, fontSize: 22 }}>Aegis</h1>
            </a>
            <p style={{ margin: "4px 0 0", color: "#666", fontSize: 13 }}>
              Investment Theses · early build
            </p>
          </header>
          {children}
        </div>
      </body>
    </html>
  );
}
