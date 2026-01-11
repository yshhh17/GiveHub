import axios from 'axios';
import { STORAGE_KEYS } from '../utils/constants';



const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
    headers: {
        'Content-Type': 'application/json'
    },
});

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem(STORAGE_KEYS.TOKEN);
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized - clear storage and redirect to login
      localStorage.removeItem(STORAGE_KEYS.TOKEN);
      localStorage.removeItem(STORAGE_KEYS.USER);
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth services
export const authService = {
  register: async (userData) => {
    const response = await api.post('/register', userData);
    return response.data;
  },

  login: async (credentials) => {
    const formData = new URLSearchParams();
    formData.append('username', credentials.email);
    formData.append('password', credentials.password);
    
    const response = await api.post('/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  },

  verifyEmail: async (data) => {
    const response = await api.post('/verify-email', data);
    return response.data;
  },

  getCurrentUser: async () => {
    const response = await api.get('/me');
    return response.data;
  },

  logout: () => {
    localStorage.removeItem(STORAGE_KEYS.TOKEN);
    localStorage.removeItem(STORAGE_KEYS.USER);
  },
};

export const donationService = {
  createOrder: async (amount) => {
    const response = await api.post('/donations/create-order', { amount });
    return response.data;
  },

  captureOrder: async (orderId) => {
    const response = await api.post('/donations/capture-order', {
      order_id: orderId,
    });
    return response.data;
  },

  getMyDonations: async (skip = 0, limit = 10) => {
    const response = await api.get('/donations/my-donations', {
      params: { skip, limit },
    });
    console.log(response.data[0].status);
    return response.data;
  },

  verifyOrder: async (orderId) => {
    const response = await api.get(`/donations/verify/${orderId}`);
    return response.data;
  },
};

export default api;