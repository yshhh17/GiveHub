import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { useDonations } from '../hooks/useDonations';
import { formatCurrency, formatDate } from '../utils/helpers';
import Card from '../components/Card';
import Button from '../components/Button';
import Badge from '../components/Badge';
import Spinner from '../components/Spinner';

const Dashboard = () => {
  const { user } = useAuth();
  const { donations, loading, fetchDonations } = useDonations();
  const [stats, setStats] = useState({
    total: 0,
    count: 0,
    thisMonth: 0,
  });

  useEffect(() => {
    fetchDonations();
  }, []);

  useEffect(() => {
    if (donations.length > 0) {
      const total = donations.reduce((sum, d) => sum + d.amount, 0);
      const thisMonth = donations
        .filter(d => new Date(d.created_at).getMonth() === new Date().getMonth())
        .reduce((sum, d) => sum + d.amount, 0);
      
      setStats({
        total,
        count: donations.length,
        thisMonth,
      });
    }
  }, [donations]);

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Welcome Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome back, {user?.name}! 👋
          </h1>
          <p className="mt-2 text-gray-600">Here's your donation summary</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card>
            <h3 className="text-sm font-medium text-gray-600 mb-2">Total Donated</h3>
            <p className="text-3xl font-bold text-blue-600">
              {formatCurrency(stats.total)}
            </p>
          </Card>

          <Card>
            <h3 className="text-sm font-medium text-gray-600 mb-2">Total Donations</h3>
            <p className="text-3xl font-bold text-green-600">{stats.count}</p>
          </Card>

          <Card>
            <h3 className="text-sm font-medium text-gray-600 mb-2">This Month</h3>
            <p className="text-3xl font-bold text-purple-600">
              {formatCurrency(stats.thisMonth)}
            </p>
          </Card>
        </div>

        {/* Quick Actions */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-4">Quick Actions</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card hoverable>
              <h3 className="text-lg font-semibold mb-2">Make a Donation</h3>
              <p className="text-sm text-gray-600 mb-4">
                Support a cause you care about today
              </p>
              <Link to="/donate">
                <Button variant="primary" fullWidth>Donate Now</Button>
              </Link>
            </Card>

            <Card hoverable>
              <h3 className="text-lg font-semibold mb-2">View History</h3>
              <p className="text-sm text-gray-600 mb-4">
                See all your past donations
              </p>
              <Link to="/my-donations">
                <Button variant="secondary" fullWidth>View Donations</Button>
              </Link>
            </Card>
          </div>
        </div>

        {/* Recent Donations */}
        <div>
          <h2 className="text-2xl font-bold mb-4">Recent Donations</h2>
          <Card>
            {loading ? (
              <div className="py-8">
                <Spinner size="lg" />
              </div>
            ) : donations.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-gray-600 mb-4">No donations yet</p>
                <Link to="/donate">
                  <Button variant="primary">Make Your First Donation</Button>
                </Link>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Date
                      </th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Amount
                      </th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Status
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {donations.slice(0, 5).map((donation) => (
                      <tr key={donation.id}>
                        <td className="px-4 py-3 text-sm text-gray-900">
                          {formatDate(donation.created_at)}
                        </td>
                        <td className="px-4 py-3 text-sm font-semibold text-gray-900">
                          {formatCurrency(donation.amount)}
                        </td>
                        <td className="px-4 py-3 text-sm">
                          <Badge variant={donation.status ?  'success' : 'warning'}>
                            {donation.status ? 'Completed' : 'Pending'}
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
    </div>
  );
};

export default Dashboard;