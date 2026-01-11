import React, { useState } from 'react';
import { PayPalScriptProvider, PayPalButtons } from '@paypal/react-paypal-js';
import { useDonations } from '../hooks/useDonations';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { PRESET_AMOUNTS } from '../utils/constants';
import Card from '../components/Card';
import Input from '../components/Input';
import Spinner from '../components/Spinner';

const Donate = () => {
  const navigate = useNavigate();
  const { createOrder, captureOrder, loading } = useDonations();
  const [amount, setAmount] = useState(10);
  const [customAmount, setCustomAmount] = useState('');
  const [showPayPal, setShowPayPal] = useState(false);

  const handleAmountSelect = (value) => {
    setAmount(value);
    setCustomAmount('');
  };

  const handleCustomAmount = (e) => {
    const value = e.target.value;
    setCustomAmount(value);
    setAmount(parseFloat(value) || 0);
  };

  const handleProceed = () => {
    if (amount < 1) {
      toast.error('Minimum donation amount is $1');
      return;
    }
    setShowPayPal(true);
  };

  const createPayPalOrder = async () => {
    const result = await createOrder(amount);
    if (result.success) {
      return result.data.order_id;
    } else {
      toast.error('Failed to create order');
      throw new Error('Order creation failed');
    }
  };

  const onPayPalApprove = async (data) => {
    const result = await captureOrder(data. orderID);
    if (result.success) {
      toast.success('Donation successful!');
      navigate('/payment-success', { state: { orderId: data.orderID } });
    } else {
      toast.error('Payment failed');
      navigate('/payment-failure');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-2xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Make a Donation</h1>
          <p className="mt-2 text-gray-600">Every contribution makes a difference</p>
        </div>

        <Card>
          {! showPayPal ? (
            <>
              {/* Preset Amounts */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-3">
                  Select Amount
                </label>
                <div className="grid grid-cols-3 md:grid-cols-5 gap-3">
                  {PRESET_AMOUNTS.map((preset) => (
                    <button
                      key={preset}
                      onClick={() => handleAmountSelect(preset)}
                      className={`px-4 py-3 rounded-lg font-semibold transition-all ${
                        amount === preset && ! customAmount
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      ${preset}
                    </button>
                  ))}
                </div>
              </div>

              {/* Custom Amount */}
              <Input
                label="Or Enter Custom Amount"
                type="number"
                name="amount"
                value={customAmount}
                onChange={handleCustomAmount}
                placeholder="Enter amount"
                min="1"
              />

              {/* Selected Amount Display */}
              <div className="mb-6 p-4 bg-blue-50 rounded-lg">
                <p className="text-sm text-gray-600">You're donating</p>
                <p className="text-3xl font-bold text-blue-600">${amount. toFixed(2)}</p>
              </div>

              {/* Proceed Button */}
              <button
                onClick={handleProceed}
                disabled={amount < 1 || loading}
                className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                {loading ?  <Spinner size="sm" /> : 'Proceed to Payment'}
              </button>
            </>
          ) : (
            <>
              {/* PayPal Buttons */}
              <div className="mb-4 p-4 bg-blue-50 rounded-lg text-center">
                <p className="text-sm text-gray-600">Donating</p>
                <p className="text-2xl font-bold text-blue-600">${amount.toFixed(2)}</p>
              </div>

              <PayPalScriptProvider
                options={{
                  'client-id': import.meta.env.VITE_PAYPAL_CLIENT_ID,
                  currency: 'USD',
                }}
              >
                <PayPalButtons
                  createOrder={createPayPalOrder}
                  onApprove={onPayPalApprove}
                  onError={() => {
                    toast.error('Payment error occurred');
                    navigate('/payment-failure');
                  }}
                  style={{ layout: 'vertical' }}
                />
              </PayPalScriptProvider>

              <button
                onClick={() => setShowPayPal(false)}
                className="w-full mt-4 bg-gray-200 text-gray-700 py-2 rounded-lg hover:bg-gray-300 transition-all"
              >
                Back
              </button>
            </>
          )}
        </Card>
      </div>
    </div>
  );
};

export default Donate;