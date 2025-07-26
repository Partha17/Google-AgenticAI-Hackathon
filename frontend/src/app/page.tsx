// frontend/src/app/page.tsx
import React from 'react';
import Dashboard from '../components/Dashboard/Dashboard';

const Home: React.FC = () => {
  return (
    <div>
      <h1 style={{ textAlign: 'center', margin: '2rem 0' }}>Financial Dashboard</h1>
      <Dashboard />
    </div>
  );
};

export default Home;
