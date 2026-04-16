import { useCallback, useState } from 'react';
import { donationService } from '../services/api';

export const useDonations = () => {
  const [donations, setDonations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchDonations = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await donationService.getMyDonations();
      setDonations(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch donations');
    } finally {
      setLoading(false);
    }
  }, []);

  const createOrder = useCallback(async (amount) => {
    setLoading(true);
    setError(null);
    try {
      const data = await donationService.createOrder(amount);
      return { success: true, data };
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create order');
      return { success:  false, error: err.response?.data?.detail };
    } finally {
      setLoading(false);
    }
  }, []);

  const captureOrder = useCallback(async (orderId) => {
    setLoading(true);
    setError(null);
    try {
      const data = await donationService.captureOrder(orderId);
      return { success: true, data };
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to capture payment');
      return { success: false, error: err.response?.data?.detail };
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    donations,
    loading,
    error,
    fetchDonations,
    createOrder,
    captureOrder,
  };
};