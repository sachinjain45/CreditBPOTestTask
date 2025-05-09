import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

export const getMatches = async (filters = {}) => {
  try {
    const params = new URLSearchParams();
    if (filters.industry) params.append('industry', filters.industry);
    if (filters.location) params.append('location', filters.location);

    const response = await axios.get(`${API_BASE_URL}/matching/matches/?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching matches:', error);
    throw error;
  }
};

export const getMLMatches = async (filters = {}) => {
  try {
    const params = new URLSearchParams();
    if (filters.industry) params.append('industry', filters.industry);
    if (filters.location) params.append('location', filters.location);

    const response = await axios.get(`${API_BASE_URL}/matching/ml/?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching ML matches:', error);
    throw error;
  }
};

export const getOpportunities = async (filters = {}) => {
  try {
    const params = new URLSearchParams();
    if (filters.industry) params.append('industry', filters.industry);
    if (filters.location) params.append('location', filters.location);

    const response = await axios.get(`${API_BASE_URL}/matching/opportunities/?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching opportunities:', error);
    throw error;
  }
}; 