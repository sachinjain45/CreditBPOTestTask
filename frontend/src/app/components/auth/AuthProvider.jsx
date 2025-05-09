'use client';

import { useEffect } from 'react';
import { useAuthStore } from '../../store/authStore';
import { fetchCurrentUser } from '../../services/auth';

export default function AuthProvider({ children }) {
  const initializeAuth = useAuthStore((state) => state.initializeAuth);
  const setUser = useAuthStore((state) => state.setUser);
  const token = useAuthStore((state) => state.token);
  const user = useAuthStore((state) => state.user);
  const isLoading = useAuthStore((state) => state.isLoading);

  useEffect(() => {
    initializeAuth();
  }, [initializeAuth]);

  useEffect(() => {
    const loadUser = async () => {
      if (token && !user) {
        try {
          const currentUser = await fetchCurrentUser();
          setUser(currentUser);
        } catch (error) {
          console.error("AuthProvider: Failed to fetch current user", error);
        }
      }
    };
    if (!isLoading) {
      loadUser();
    }
  }, [token, user, setUser, isLoading]);

  return <>{children}</>;
}