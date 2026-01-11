import React, { useEffect } from 'react';
import { useDonations } from '../hooks/useDonations';
import { formatCurrency, formatDate } from '../utils/helpers';
import Card from '../components/Card';
import Badge from '../components/Badge';
import Spinner from '../components/Spinner';

const MyDonations = () => {
  const { donations, loading, fetchDonations } = useDonations();

  useEffect(() => {
    fetchDonations();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">My Donations</h1>
          <p className="mt-2 text-gray-600">View all your donation history</p>
        </div>

        <Card>
          {loading ? (
            <div className="py-12 text-center">
              <Spinner size="lg" />
            </div>
          ) : donations.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-600 text-lg mb-4">No donations yet</p>
              <p className="text-gray-500">Start making a difference today!</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase">
                      Date
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase">
                      Order ID
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase">
                      Amount
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase">
                      Status
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {donations.map((donation) => (
                    <tr key={donation.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 text-sm text-gray-900">
                        {formatDate(donation.created_at)}
                      </td>
                      <td className="px-6 py-4 text-sm font-mono text-gray-600">
                        {donation.order_id}
                      </td>
                      <td className="px-6 py-4 text-sm font-bold text-gray-900">
                        {formatCurrency(donation.amount)}
                      </td>
                      <td className="px-6 py-4 text-sm">
                        <Badge variant={donation.status ? 'success' : 'warning'}>
                          {donation.status ? 'Completed' :  'Pending'}
                        </Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
};

export default MyDonations;