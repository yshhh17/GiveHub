export const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount)
};

export const formatDate = (dateString) => {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date);
};

export const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

// Validate password (min 8 characters)
export const isValidPassword = (password) => {
  return password.length >= 8;
};

// Get status badge color
export const getStatusColor = (status) => {
  if (status === true || status === 'completed') {
    return 'bg-green-100 text-green-800';
  }
  if (status === false || status === 'pending') {
    return 'bg-yellow-100 text-yellow-800';
  }
  return 'bg-red-100 text-red-800';
};

// Get status text
export const getStatusText = (status) => {
  if (status === true || status === 'completed') return 'Completed';
  if (status === false || status === 'pending') return 'Pending';
  return 'Failed';
};