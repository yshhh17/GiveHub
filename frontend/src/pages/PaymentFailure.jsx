import React from 'react';
import { Link } from 'react-router-dom';
import Button from '../components/Button';
import Card from '../components/Card';

const PaymentFailure = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-8 px-4">
      <Card className="max-w-md w-full text-center">
        {/* Error Icon */}
        <div className="w-20 h-20 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg
            className="w-10 h-10 text-red-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </div>

        {/* Error Message */}
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Payment Failed
        </h1>
        <p className="text-gray-600 mb-6">
          We couldn't process your donation.   Please try again or contact support if the problem persists.
        </p>

        {/* Action Buttons */}
        <div className="space-y-3">
          <Link to="/donate">
            <Button variant="primary" fullWidth>
              Try Again
            </Button>
          </Link>
          <Link to="/dashboard">
            <Button variant="secondary" fullWidth>
              Go to Dashboard
            </Button>
          </Link>
        </div>
      </Card>
    </div>
  );
};

export default PaymentFailure;