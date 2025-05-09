import { Inter } from 'next/font/google';
import './globals.css';
import AuthProvider from '../../src/app/components/auth/AuthProvider';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'CreditBPO Matching Platform',
  description: 'Connect Seekers and Providers Effortlessly',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={`${inter.className} antialiased`}>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
