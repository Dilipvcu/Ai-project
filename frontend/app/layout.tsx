import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'AI Document Analysis Engine',
  description: 'Extract insights from your documents using advanced AI',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-gray-50">{children}</body>
    </html>
  );
}
