import { create } from 'zustand';

const LSTORAGE_AUTH_TOKEN_KEY = 'authToken';
const LSTORAGE_REFRESH_TOKEN_KEY = 'refreshToken';

const getStoredAuthToken = () => {
  if (typeof window !== 'undefined') return localStorage.getItem(LSTORAGE_AUTH_TOKEN_KEY);
  return null;
};
const setStoredAuthToken = (token) => {
  if (typeof window !== 'undefined') localStorage.setItem(LSTORAGE_AUTH_TOKEN_KEY, token);
};
const removeStoredAuthToken = () => {
  if (typeof window !== 'undefined') localStorage.removeItem(LSTORAGE_AUTH_TOKEN_KEY);
};

const getStoredRefreshToken = () => {
  if (typeof window !== 'undefined') return localStorage.getItem(LSTORAGE_REFRESH_TOKEN_KEY);
  return null;
};
const setStoredRefreshToken = (token) => {
  if (typeof window !== 'undefined') localStorage.setItem(LSTORAGE_REFRESH_TOKEN_KEY, token);
};
const removeStoredRefreshToken = () => {
  if (typeof window !== 'undefined') localStorage.removeItem(LSTORAGE_REFRESH_TOKEN_KEY);
};

export const useAuthStore = create((set, get) => ({
  user: null,
  token: null,
  refreshToken: null,
  isAuthenticated: false,
  isLoading: false,

  login: (userData, accessToken, newRefreshToken) => {
    setStoredAuthToken(accessToken);
    setStoredRefreshToken(newRefreshToken);
    set({
      user: userData,
      token: accessToken,
      refreshToken: newRefreshToken,
      isAuthenticated: true,
      isLoading: false,
    });
  },

  logout: () => {
    removeStoredAuthToken();
    removeStoredRefreshToken();
    set({
      user: null,
      token: null,
      refreshToken: null,
      isAuthenticated: false,
      isLoading: false,
    });
    if (typeof window !== 'undefined' && window.location.pathname !== '/login') {
      window.location.href = '/login';
    }
  },

  setUser: (userData) => {
    set({ user: userData });
  },

  initializeAuth: () => {
    if (typeof window !== 'undefined') {
      const storedToken = getStoredAuthToken();
      const storedRefreshToken = getStoredRefreshToken();
      if (storedToken) {
        set({
          token: storedToken,
          refreshToken: storedRefreshToken,
          isAuthenticated: true,
        });
      }
    }
    set({ isLoading: false });
  },
}));