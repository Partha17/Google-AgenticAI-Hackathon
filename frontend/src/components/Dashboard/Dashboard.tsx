// frontend/src/components/Dashboard/Dashboard.tsx
import React from 'react';
import Card from '../Card/Card';

const features = [
  {
    title: 'Tax Optimizer',
    description: 'ELSS, HRA, harvesting',
  },
  {
    title: 'Debt Payoff',
    description: 'snowball/avalanche strategy',
  },
  {
    title: 'SIP Booster',
    description: 'detect underperformers',
  },
  {
    title: 'Subscription Killer',
    description: 'detect and analyze subscription payments',
  },
  {
    title: 'Risk Manager',
    description: 'check asset allocation',
  },
  {
    title: 'Goal Tracker',
    description: 'map goals to savings',
  },
  {
    title: 'Liquidity Agent',
    description: 'emergency buffer insights',
  },
  {
    title: 'Router Agent',
    description: 'master planner & scheduler',
  },
];

const Dashboard: React.FC = () => {
  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
      gap: '1rem',
      padding: '1rem',
      backgroundColor: '#f4f7f9',
    }}>
      {features.map((feature, index) => (
        <Card key={index} title={feature.title} description={feature.description} />
      ))}
    </div>
  );
};

export default Dashboard;
