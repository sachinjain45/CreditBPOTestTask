import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export const getPaymentHistory = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/payments/history/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching payment history:', error);
    throw error;
  }
};

export const createCheckoutSession = async (data) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/payments/create-checkout-session/`, data);
    return response.data;
  } catch (error) {
    console.error('Error creating checkout session:', error);
    throw error;
  }
};

export const getSubscriptionStatus = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/payments/subscription/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching subscription status:', error);
    throw error;
  }
};

export const cancelSubscription = async () => {
  try {
    const response = await axios.post(`${API_BASE_URL}/payments/cancel-subscription/`);
    return response.data;
  } catch (error) {
    console.error('Error canceling subscription:', error);
    throw error;
  }
};

export const updatePaymentMethod = async (paymentMethodId) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/payments/update-payment-method/`, {
      payment_method_id: paymentMethodId,
    });
    return response.data;
  } catch (error) {
    console.error('Error updating payment method:', error);
    throw error;
  }
}; 