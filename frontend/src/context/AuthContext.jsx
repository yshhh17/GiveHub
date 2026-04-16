import React, { useState } from 'react';
import { authService } from '../services/api';
import { STORAGE_KEYS, TOAST_MESSAGES } from '../utils/constants';
import { AuthContext } from './authContext';

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(() => localStorage.getItem(STORAGE_KEYS.TOKEN));
  const [user, setUser] = useState(() => {
    const storedUser = localStorage.getItem(STORAGE_KEYS.USER);
    return storedUser ? JSON.parse(storedUser) : null;
  });

  const logout = () => {
    authService.logout();
    setToken(null);
    setUser(null);
  };

  const login = async (credentials) => {
    try {
      const data = await authService.login(credentials);
      const { access_token } = data;

      localStorage.setItem(STORAGE_KEYS.TOKEN, access_token);
      setToken(access_token);

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
      return { success: true, message: TOAST_MESSAGES.REGISTER_SUCCESS };
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
      return { success: true, message: TOAST_MESSAGES.VERIFY_EMAIL_SUCCESS };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || TOAST_MESSAGES.VERIFY_EMAIL_ERROR,
      };
    }
  };

  return (
    <AuthContext.Provider value={{
      user,
      token,
      loading: false,
      isAuthenticated: !!token,
      login,
      register,
      verifyEmail,
      logout
    }}>
      {children}
    </AuthContext.Provider>
  );
};
