'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuthStore } from '../store/authStore';

export default function DashboardLayout({ children }) {
  const router = useRouter();
  const { user, isAuthenticated, isLoading: authIsLoading, logout } = useAuthStore();

  useEffect(() => {
    if (!authIsLoading && !isAuthenticated) {
      router.push('/login?reason=unauthenticated');
    }
  }, [authIsLoading, isAuthenticated, router]);

  if (authIsLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-100 text-gray-700">
        Loading Dashboard...
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <Link href="/dashboard" className="text-xl font-bold text-indigo-600 hover:text-indigo-700 transition-colors">
                CreditBPO Platform
              </Link>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-700 hidden sm:block">
                Hi, {user?.first_name || user?.username}!
              </span>
              <Link
                href="/dashboard/profile"
                className="text-gray-600 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
              >
                My Profile
              </Link>
              <button
                onClick={() => {
                  logout();
                }}
                className="text-gray-600 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>
      <main className="py-10">
        <div className="max-w-7xl mx-auto sm:px-6 lg:px-8 px-4">
          {children}
        </div>
      </main>
      <footer className="bg-white border-t mt-auto">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 text-center text-gray-500 text-sm">
          © {new Date().getFullYear()} CreditBPO Matching Platform. All rights reserved.
        </div>
      </footer>
    </div>
  );
}