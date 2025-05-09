'use client';

import { useState, useEffect } from 'react';
import { useAuthStore } from '../../store/authStore';
import { getPaymentHistory, createCheckoutSession } from '../../services/payments';

export default function PaymentsPage() {
  const { user } = useAuthStore();
  const [paymentHistory, setPaymentHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isProcessingPayment, setIsProcessingPayment] = useState(false);

  useEffect(() => {
    fetchPaymentHistory();
  }, []);

  const fetchPaymentHistory = async () => {
    try {
      setIsLoading(true);
      const response = await getPaymentHistory();
      setPaymentHistory(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch payment history. Please try again.');
      console.error('Error fetching payment history:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleUpgradeSubscription = async (tier) => {
    try {
      setIsProcessingPayment(true);
      const response = await createCheckoutSession({
        price_id: tier.priceId,
        description: `Upgrade to ${tier.name} subscription`,
      });
      
      // Redirect to Stripe Checkout
      window.location.href = response.url;
    } catch (err) {
      setError('Failed to initiate payment. Please try again.');
      console.error('Error creating checkout session:', err);
    } finally {
      setIsProcessingPayment(false);
    }
  };

  const subscriptionTiers = [
    {
      name: 'Basic',
      price: '₱999',
      period: 'month',
      features: [
        'Basic profile visibility',
        'Up to 10 matches per month',
        'Email support',
      ],
      priceId: process.env.NEXT_PUBLIC_STRIPE_BASIC_PRICE_ID,
    },
    {
      name: 'Premium',
      price: '₱2,999',
      period: 'month',
      features: [
        'Enhanced profile visibility',
        'Unlimited matches',
        'Priority support',
        'Advanced analytics',
        'Custom branding',
      ],
      priceId: process.env.NEXT_PUBLIC_STRIPE_PREMIUM_PRICE_ID,
    },
  ];

  return (
    <div className="bg-white shadow-lg rounded-xl p-6 md:p-10">
      <h1 className="text-3xl font-semibold text-gray-800 mb-6">Billing & Payments</h1>

      {/* Current Subscription */}
      <div className="mb-12">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Current Subscription</h2>
        <div className="bg-indigo-50 rounded-lg p-6">
          <div className="flex justify-between items-center">
            <div>
              <h3 className="text-lg font-medium text-indigo-900">
                {user?.provider_profile?.subscription_tier || 'No Active Subscription'}
              </h3>
              <p className="text-indigo-700 mt-1">
                {user?.provider_profile?.subscription_tier === 'NONE'
                  ? 'Upgrade your subscription to access more features'
                  : 'Your subscription is active'}
              </p>
            </div>
            {user?.provider_profile?.subscription_tier === 'NONE' && (
              <button
                onClick={() => handleUpgradeSubscription(subscriptionTiers[0])}
                disabled={isProcessingPayment}
                className="px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
              >
                {isProcessingPayment ? 'Processing...' : 'Upgrade Now'}
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Subscription Tiers */}
      <div className="mb-12">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Available Plans</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {subscriptionTiers.map((tier) => (
            <div
              key={tier.name}
              className="border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow duration-300"
            >
              <h3 className="text-xl font-semibold text-gray-800 mb-2">{tier.name}</h3>
              <p className="text-3xl font-bold text-gray-900 mb-4">
                {tier.price}
                <span className="text-base font-normal text-gray-500">/{tier.period}</span>
              </p>
              <ul className="space-y-3 mb-6">
                {tier.features.map((feature) => (
                  <li key={feature} className="flex items-center text-gray-600">
                    <svg
                      className="h-5 w-5 text-green-500 mr-2"
                      fill="none"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path d="M5 13l4 4L19 7"></path>
                    </svg>
                    {feature}
                  </li>
                ))}
              </ul>
              <button
                onClick={() => handleUpgradeSubscription(tier)}
                disabled={isProcessingPayment}
                className="w-full px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
              >
                {isProcessingPayment ? 'Processing...' : 'Upgrade to ' + tier.name}
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Payment History */}
      <div>
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Payment History</h2>
        {error && (
          <div className="mb-6 p-4 bg-red-50 rounded-md">
            <p className="text-sm text-red-700">{error}</p>
          </div>
        )}
        {isLoading ? (
          <div className="flex justify-center items-center h-32">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Description
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Amount
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {paymentHistory.map((payment) => (
                  <tr key={payment.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(payment.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {payment.description}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {payment.amount} {payment.currency}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                          payment.status === 'SUCCESSFUL'
                            ? 'bg-green-100 text-green-800'
                            : payment.status === 'PENDING'
                            ? 'bg-yellow-100 text-yellow-800'
                            : 'bg-red-100 text-red-800'
                        }`}
                      >
                        {payment.status}
                      </span>
                    </td>
                  </tr>
                ))}
                {paymentHistory.length === 0 && (
                  <tr>
                    <td colSpan="4" className="px-6 py-4 text-center text-sm text-gray-500">
                      No payment history found
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
} 