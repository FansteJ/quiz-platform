import api from './api';

class AuthService {
    /**
     * Registracija novog korisnika
     */
    async register(userData) {
        try {
            const response = await api.post('/api/auth/register', userData);
            return response.data;
        } catch (error) {
            throw error.response?.data || { message: 'Registration failed' };
        }
    }

    /**
     * Login korisnika
     */
    async login(email, password) {
        try {
            const response = await api.post('/api/auth/login', {
                email,
                password,
            });

            const { access_token, refresh_token, user } = response.data;

            // Sačuvaj u localStorage
            localStorage.setItem('access_token', access_token);
            localStorage.setItem('refresh_token', refresh_token);
            localStorage.setItem('user', JSON.stringify(user));

            return response.data;
        } catch (error) {
            throw error.response?.data || { message: 'Login failed' };
        }
    }

    /**
     * Logout korisnika
     */
    logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
    }

    /**
     * Provera da li je korisnik ulogovan
     */
    isAuthenticated() {
        return !!localStorage.getItem('access_token');
    }

    /**
     * Uzmi trenutnog korisnika
     */
    getCurrentUser() {
        const userStr = localStorage.getItem('user');
        return userStr ? JSON.parse(userStr) : null;
    }

    /**
     * Proveri email da li postoji
     */
    async checkEmail(email) {
        try {
            const response = await api.post('/api/auth/check-email', { email });
            return response.data;
        } catch (error) {
            throw error.response?.data || { message: 'Check failed' };
        }
    }
}

export default new AuthService();