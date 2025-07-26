// frontend/src/app/layout.tsx
import React from 'react';
import './globals.css';
import ClientProvider from './client-provider';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <ClientProvider>
          <div>
            <main>{children}</main>
          </div>
        </ClientProvider>
      </body>
    </html>
  );
}
