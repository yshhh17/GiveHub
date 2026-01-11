import { useState, useEffect } from 'react';
import { authService } from '../services/api';
import { STORAGE_KEYS, TOAST_MESSAGES } from '../utils/constants';

export const useAuth = () => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  // Fetch user info from backend
  const fetchUserInfo = async () => {
    try {
      const userData = await authService.getCurrentUser();
      setUser(userData);
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(userData));
    } catch (error) {
      console.error('Failed to fetch user info:', error);
      // If fetch fails, clear auth
      logout();
    }
  };

  useEffect(() => {
    // Check if user is logged in
    const storedToken = localStorage.getItem(STORAGE_KEYS.TOKEN);
    const storedUser = localStorage.getItem(STORAGE_KEYS.USER);

    if (storedToken) {
      setToken(storedToken);
      
      if (storedUser) {
        setUser(JSON.parse(storedUser));
      }
      
      // Fetch fresh user data from backend
      fetchUserInfo();
    }
    
    setLoading(false);
  }, []);

  const login = async (credentials) => {
    try {
      const data = await authService.login(credentials);
      const { access_token } = data;

      // Store token
      localStorage.setItem(STORAGE_KEYS.TOKEN, access_token);
      setToken(access_token);

      // Fetch user info from database
      const userData = await authService.getCurrentUser();
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(userData));
      setUser(userData);

      return { success: true, message: TOAST_MESSAGES.LOGIN_SUCCESS };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || TOAST_MESSAGES.LOGIN_ERROR,
      };
    }
  };

  const register = async (userData) => {
    try {
      await authService.register(userData);
      return { success: true, message: TOAST_MESSAGES. REGISTER_SUCCESS };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || TOAST_MESSAGES.REGISTER_ERROR,
      };
    }
  };

  const verifyEmail = async (email, otp) => {
    try {
      await authService.verifyEmail({ email, otp });
      return { success:  true, message: TOAST_MESSAGES.VERIFY_EMAIL_SUCCESS };
    } catch (error) {
      return {
        success: false,
        message: error.response?. data?.detail || TOAST_MESSAGES.VERIFY_EMAIL_ERROR,
      };
    }
  };

  const logout = () => {
    authService.logout();
    setToken(null);
    setUser(null);
  };

  return {
    user,
    token,
    loading,
    isAuthenticated:  !!token,
    login,
    register,
    verifyEmail,
    logout,
  };
};