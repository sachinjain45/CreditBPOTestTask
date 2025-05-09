'use client';

import Link from 'next/link';
import { useAuthStore } from '../store/authStore';

export default function DashboardPage() {
  const { user } = useAuthStore();

  return (
    <div className="bg-white shadow-lg rounded-xl p-6 md:p-10">
      <h1 className="text-3xl font-semibold text-gray-800 mb-2">
        Welcome, {user?.first_name || user?.username}!
      </h1>
      <p className="text-gray-600 mb-8">Here's what you can do on the platform:</p>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <DashboardCard
          title="Your Profile"
          description="View and update your personal and professional details to get the best matches."
          linkHref="/dashboard/profile"
          linkText="Manage Profile"
          icon="👤"
        />
        {user?.role === 'seeker' && (
          <DashboardCard
            title="Find Matches"
            description="Discover providers that perfectly match your service requirements."
            linkHref="/dashboard/matches"
            linkText="View Matches"
            icon="🔗"
          />
        )}
        {user?.role === 'provider' && (
          <DashboardCard
            title="View Opportunities"
            description="See seekers whose needs align with the services you offer."
            linkHref="/dashboard/opportunities"
            linkText="Browse Opportunities"
            icon="💡"
          />
        )}
        <DashboardCard
            title="Billing & Payments"
            description="Manage your subscription, view payment history, and update billing details."
            linkHref="/dashboard/payments"
            linkText="Go to Billing"
            icon="💳"
        />
      </div>
      <div className="mt-12 pt-8 border-t border-gray-200">
        <h3 className="text-xl font-semibold text-gray-700 mb-4">Platform Activity</h3>
        <p className="text-gray-600">
          This section can display recent matches, messages, or system announcements.
        </p>
      </div>
    </div>
  );
}

const DashboardCard = ({ title, description, linkHref, linkText, icon }) => (
  <div className="bg-gradient-to-br from-gray-50 to-gray-100 p-6 rounded-lg shadow-md hover:shadow-lg transition-all duration-300 ease-in-out transform hover:-translate-y-1">
    {icon && <div className="text-3xl mb-3">{icon}</div>}
    <h2 className="text-xl font-semibold text-gray-700 mb-2">{title}</h2>
    <p className="text-gray-600 text-sm mb-4 h-20 overflow-hidden">{description}</p>
    <Link
      href={linkHref}
      className="inline-block px-6 py-2.5 bg-indigo-600 text-white text-sm font-medium rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors"
    >
      {linkText}
    </Link>
  </div>
);