import React from 'react';
import CashflowDashboard from './components/CashflowDashboard';

function App() {
  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Cashflow Forecast Dashboard</h1>
        <CashflowDashboard />
      </div>
    </div>
  );
}

export default App;