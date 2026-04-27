import { create } from 'zustand';
import { User } from '@/types';
import { authAPI } from '@/services/api';

interface AuthStore {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, username: string, password: string, phone: string) => Promise<void>;
  logout: () => void;
  getMe: () => Promise<void>;
}

export const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  isLoading: false,
  isAuthenticated: !!localStorage.getItem('access_token'),

  login: async (email: string, password: string) => {
    set({ isLoading: true });
    try {
      const response = await authAPI.login({ email, password });
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('refresh_token', response.data.refresh_token);
      set({
        user: response.data.user,
        isAuthenticated: true,
        isLoading: false,
      });
    } catch (error) {
      set({ isLoading: false });
      throw error;
    }
  },

  register: async (email: string, username: string, password: string, phone: string) => {
    set({ isLoading: true });
    try {
      const response = await authAPI.register({
        email,
        username,
        password,
        phone,
      });
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('refresh_token', response.data.refresh_token);
      set({
        user: response.data.user,
        isAuthenticated: true,
        isLoading: false,
      });
    } catch (error) {
      set({ isLoading: false });
      throw error;
    }
  },

  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    set({ user: null, isAuthenticated: false });
  },

  getMe: async () => {
    try {
      const response = await authAPI.me();
      set({ user: response.data, isAuthenticated: true });
    } catch (error) {
      set({ isAuthenticated: false });
      throw error;
    }
  },
}));
