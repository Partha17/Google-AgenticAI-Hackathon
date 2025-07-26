// frontend/src/components/Card/Card.tsx
import React from 'react';

interface CardProps {
  title: string;
  description: string;
}

const Card: React.FC<CardProps> = ({ title, description }) => {
  return (
    <div style={{
      border: '1px solid #ccc',
      borderRadius: '8px',
      padding: '1rem',
      margin: '1rem',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
      backgroundColor: '#fff',
    }}>
      <h3 style={{ marginTop: 0 }}>{title}</h3>
      <p>{description}</p>
    </div>
  );
};

export default Card;
