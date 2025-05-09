'use client';

import { useState, useEffect } from 'react';
import { useAuthStore } from '../../store/authStore';
import { getMatches } from '../../services/matching';

export default function MatchesPage() {
  const { user } = useAuthStore();
  const [matches, setMatches] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    industry: '',
    location: '',
  });

  useEffect(() => {
    fetchMatches();
  }, [filters]);

  const fetchMatches = async () => {
    try {
      setIsLoading(true);
      const response = await getMatches(filters);
      setMatches(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch matches. Please try again.');
      console.error('Error fetching matches:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFilterChange = (e) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
  };

  if (user?.role !== 'SEEKER') {
    return (
      <div className="bg-white shadow-lg rounded-xl p-6 md:p-10">
        <h1 className="text-2xl font-semibold text-red-600">Access Denied</h1>
        <p className="text-gray-600 mt-2">This page is only available for seekers.</p>
      </div>
    );
  }

  return (
    <div className="bg-white shadow-lg rounded-xl p-6 md:p-10">
      <h1 className="text-3xl font-semibold text-gray-800 mb-6">Find Your Perfect Match</h1>
      
      {/* Filters */}
      <div className="mb-8 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label htmlFor="industry" className="block text-sm font-medium text-gray-700 mb-1">
            Industry
          </label>
          <input
            type="text"
            id="industry"
            name="industry"
            value={filters.industry}
            onChange={handleFilterChange}
            placeholder="e.g., Manufacturing, Retail"
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
        <div>
          <label htmlFor="location" className="block text-sm font-medium text-gray-700 mb-1">
            Location
          </label>
          <input
            type="text"
            id="location"
            name="location"
            value={filters.location}
            onChange={handleFilterChange}
            placeholder="e.g., Metro Manila, Cebu"
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="mb-6 p-4 bg-red-50 rounded-md">
          <p className="text-sm text-red-700">{error}</p>
        </div>
      )}

      {/* Loading State */}
      {isLoading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
        </div>
      ) : (
        /* Matches Grid */
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {matches.map((match) => (
            <MatchCard key={match.id} match={match} />
          ))}
          {matches.length === 0 && !error && (
            <div className="col-span-full text-center py-12">
              <p className="text-gray-600">No matches found. Try adjusting your filters.</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

const MatchCard = ({ match }) => (
  <div className="bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-300">
    <div className="p-6">
      <h3 className="text-xl font-semibold text-gray-800 mb-2">{match.company_name}</h3>
      <div className="space-y-2 mb-4">
        <p className="text-gray-600">
          <span className="font-medium">Location:</span> {match.location}
        </p>
        <p className="text-gray-600">
          <span className="font-medium">Services:</span>{' '}
          {match.service_types?.join(', ') || 'Not specified'}
        </p>
        <p className="text-gray-600">
          <span className="font-medium">Areas Served:</span>{' '}
          {match.geos_served?.join(', ') || 'Not specified'}
        </p>
      </div>
      <div className="flex justify-between items-center">
        <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-indigo-100 text-indigo-800">
          {match.subscription_tier}
        </span>
        <button
          onClick={() => {/* TODO: Implement contact action */}}
          className="px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Contact
        </button>
      </div>
    </div>
  </div>
); 