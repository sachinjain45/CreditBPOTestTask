import api from "../lib/api";

export const loginUser = async (credentials) => {
  const response = await api.post('/auth/login/', credentials);
  return response?.data;
};

export const registerUser = async (userData) => {
  const response = await api.post('/auth/register/', userData);
  return response?.data;
};

export const fetchCurrentUser = async () => {
  const response = await api.get('/auth/me/');
  return response?.data;
};

export const refreshTokenApi = async (currentRefreshToken) => {
  const response = await api.post('/auth/login/refresh/', {
    refresh: currentRefreshToken,
  });
  return response?.data;
};