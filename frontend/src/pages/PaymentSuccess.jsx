import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import Button from '../components/Button';
import Card from '../components/Card';

const PaymentSuccess = () => {
  const location = useLocation();
  const orderId = location.state?.orderId || 'N/A';

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-8 px-4">
      <Card className="max-w-md w-full text-center">
        {/* Success Icon */}
        <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg
            className="w-10 h-10 text-green-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M5 13l4 4L19 7"
            />
          </svg>
        </div>

        {/* Success Message */}
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Donation Successful!
        </h1>
        <p className="text-gray-600 mb-6">
          Thank you for your generous contribution.   Your donation is making a real impact!
        </p>

        {/* Order ID */}
        <div className="bg-gray-50 p-4 rounded-lg mb-6">
          <p className="text-sm text-gray-600">Order ID</p>
          <p className="font-mono text-sm font-semibold text-gray-900">{orderId}</p>
        </div>

        {/* Action Buttons */}
        <div className="space-y-3">
          <Link to="/my-donations">
            <Button variant="primary" fullWidth>
              View My Donations
            </Button>
          </Link>
          <Link to="/donate">
            <Button variant="secondary" fullWidth>
              Make Another Donation
            </Button>
          </Link>
        </div>
      </Card>
    </div>
  );
};

export default PaymentSuccess;