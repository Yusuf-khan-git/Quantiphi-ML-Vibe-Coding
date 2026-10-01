import React from 'react';

export default function Loading({ text = "Loading..." }) {
  return (
    <div style={{ textAlign: 'center', padding: '3rem', color: '#94a3b8' }}>
      <div style={{
        display: 'inline-block',
        width: '32px',
        height: '32px',
        border: '3px solid rgba(255,255,255,0.1)',
        borderTopColor: '#8b5cf6',
        borderRadius: '50%',
        animation: 'spin 1s linear infinite'
      }} />
      <style>{`@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }`}</style>
      <p style={{ marginTop: '0.8rem', fontSize: '0.9rem' }}>{text}</p>
    </div>
  );
}
