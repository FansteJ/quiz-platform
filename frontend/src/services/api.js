import axios from 'axios';

// Base URL - backend API
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

// Kreiraj axios instancu
const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor - dodaje token u header
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor - handluje greške
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        // Ako je token istekao (401) i nije retry
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                const refreshToken = localStorage.getItem('refresh_token');

                if (refreshToken) {
                    // Pokušaj da refresh-uješ token
                    const response = await axios.post(`${API_URL}/api/auth/refresh`, {}, {
                        headers: {
                            Authorization: `Bearer ${refreshToken}`
                        }
                    });

                    const { access_token } = response.data;
                    localStorage.setItem('access_token', access_token);

                    // Ponovi originalni zahtev sa novim tokenom
                    originalRequest.headers.Authorization = `Bearer ${access_token}`;
                    return api(originalRequest);
                }
            } catch (refreshError) {
                // Refresh nije uspeo - logout
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                localStorage.removeItem('user');
                window.location.href = '/login';
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

export default api;