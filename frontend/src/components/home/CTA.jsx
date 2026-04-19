import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '../Button';

const CTA = () => {
  const navigate = useNavigate();

  return (
    <section className="w-full py-20 md:py-24 bg-gradient-to-r from-blue-600 to-blue-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center rounded-3xl border border-blue-400/30 bg-white/5 px-6 py-14 sm:px-10 backdrop-blur-sm">
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-white mb-6">
            Ready to Make an Impact?
          </h2>

          <p className="text-lg sm:text-xl text-blue-100 mb-10 max-w-2xl mx-auto">
            Join our community of donors and start making a difference today.
            Every contribution counts.
          </p>

          <Button
            size="lg"
            className="bg-white text-blue-700 hover:bg-blue-50 focus:ring-white"
            onClick={() => navigate('/register')}
          >
            Get Started Now
          </Button>
        </div>
      </div>
    </section>
  );
};

export default CTA;