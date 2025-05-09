'use client';

import { useState, useEffect } from 'react';
import { useAuthStore } from '../../store/authStore';
import { getOpportunities } from '../../services/matching';

export default function OpportunitiesPage() {
  const { user } = useAuthStore();
  const [opportunities, setOpportunities] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    industry: '',
    location: '',
  });

  useEffect(() => {
    fetchOpportunities();
  }, [filters]);

  const fetchOpportunities = async () => {
    try {
      setIsLoading(true);
      const response = await getOpportunities(filters);
      setOpportunities(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch opportunities. Please try again.');
      console.error('Error fetching opportunities:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFilterChange = (e) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
  };

  if (user?.role !== 'PROVIDER') {
    return (
      <div className="bg-white shadow-lg rounded-xl p-6 md:p-10">
        <h1 className="text-2xl font-semibold text-red-600">Access Denied</h1>
        <p className="text-gray-600 mt-2">This page is only available for providers.</p>
      </div>
    );
  }

  return (
    <div className="bg-white shadow-lg rounded-xl p-6 md:p-10">
      <h1 className="text-3xl font-semibold text-gray-800 mb-6">Business Opportunities</h1>
      
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
        /* Opportunities Grid */
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {opportunities.map((opportunity) => (
            <OpportunityCard key={opportunity.id} opportunity={opportunity} />
          ))}
          {opportunities.length === 0 && !error && (
            <div className="col-span-full text-center py-12">
              <p className="text-gray-600">No opportunities found. Try adjusting your filters.</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

const OpportunityCard = ({ opportunity }) => (
  <div className="bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-300">
    <div className="p-6">
      <h3 className="text-xl font-semibold text-gray-800 mb-2">{opportunity.company_name}</h3>
      <div className="space-y-2 mb-4">
        <p className="text-gray-600">
          <span className="font-medium">Industry:</span> {opportunity.industry}
        </p>
        <p className="text-gray-600">
          <span className="font-medium">Location:</span> {opportunity.location}
        </p>
        {opportunity.rating_report_url && (
          <p className="text-gray-600">
            <span className="font-medium">Rating Report:</span>{' '}
            <a
              href={opportunity.rating_report_url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-indigo-600 hover:text-indigo-800"
            >
              View Report
            </a>
          </p>
        )}
      </div>
      <div className="flex justify-end">
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