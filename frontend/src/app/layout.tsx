import type { Metadata } from "next";
import "./globals.css";
import { DocumentProvider } from "@/providers/DocumentProviders";

export const metadata: Metadata = {
  title: "PrivacyRAG",
  description: "Private RAG Chat Application",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className="dark h-full antialiased"
    >
      <body className="min-h-full flex flex-col bg-background text-foreground">
        <DocumentProvider>
          {children}
        </DocumentProvider>
      </body>
    </html>
  );
}
