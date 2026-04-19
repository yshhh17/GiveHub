import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '../Button';

const Hero = () => {
  const navigate = useNavigate();

  const metrics = [
    { value: '10K+', label: 'Donors' },
    { value: '500+', label: 'Causes Supported' },
    { value: '99.9%', label: 'Payment Success' },
  ];

  return (
    <section className="w-full bg-gradient-to-b from-blue-50 via-white to-white py-20 md:py-28">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-4xl mx-auto">
          <p className="inline-flex items-center rounded-full bg-blue-100 text-blue-700 text-sm font-semibold px-4 py-1.5 mb-6">
            Trusted donations powered by PayPal
          </p>

          <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold text-gray-900 mb-6 leading-tight">
            Make a Difference with{' '}
            <span className="text-blue-600">Every Donation</span>
          </h1>

          <p className="text-lg sm:text-xl md:text-2xl text-gray-600 mb-10 max-w-3xl mx-auto leading-relaxed">
            Join thousands of donors making a real impact. Secure, transparent,
            and instant donations powered by PayPal.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
            <Button
              variant="primary"
              size="lg"
              onClick={() => navigate('/register')}
              className="w-full sm:w-auto px-8 py-4 text-lg shadow-lg shadow-blue-200"
            >
              Start Donating
            </Button>
            <Button
              variant="secondary"
              size="lg"
              onClick={() => navigate('/login')}
              className="w-full sm:w-auto px-8 py-4 text-lg"
            >
              Login
            </Button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 sm:gap-6 max-w-3xl mx-auto">
            {metrics.map((metric) => (
              <div key={metric.label} className="rounded-xl border border-gray-200 bg-white/90 p-4">
                <p className="text-2xl font-bold text-gray-900">{metric.value}</p>
                <p className="text-sm text-gray-600">{metric.label}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;