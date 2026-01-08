import { create } from 'zustand';
import authService from '../services/authService';

const useAuthStore = create((set) => ({
    user: authService.getCurrentUser(),
    isAuthenticated: authService.isAuthenticated(),
    loading: false,
    error: null,

    // Login
    login: async (email, password) => {
        set({ loading: true, error: null });
        try {
            const data = await authService.login(email, password);
            set({
                user: data.user,
                isAuthenticated: true,
                loading: false,
            });
            return data;
        } catch (error) {
            set({ loading: false, error: error.message || 'Login failed' });
            throw error;
        }
    },

    // Register
    register: async (userData) => {
        set({ loading: true, error: null });
        try {
            const data = await authService.register(userData);
            set({ loading: false });
            return data;
        } catch (error) {
            set({ loading: false, error: error.message || 'Registration failed' });
            throw error;
        }
    },

    // Logout
    logout: () => {
        authService.logout();
        set({
            user: null,
            isAuthenticated: false,
            error: null,
        });
    },

    // Clear error
    clearError: () => set({ error: null }),
}));

export default useAuthStore;