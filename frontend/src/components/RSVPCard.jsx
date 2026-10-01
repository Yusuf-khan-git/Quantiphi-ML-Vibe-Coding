import React, { useState } from 'react';
import { cancelRSVP } from '../services/api';

export default function RSVPCard({ rsvp, currentUser, onCancelSuccess, showToast }) {
  const [cancelling, setCancelling] = useState(false);
  const snapshot = rsvp.eventSnapshot || {};

  const handleCancel = async () => {
    if (!currentUser) return;
    setCancelling(true);
    try {
      await cancelRSVP(currentUser.id, snapshot.id || rsvp.eventId);
      if (showToast) showToast('RSVP cancelled');
      if (onCancelSuccess) onCancelSuccess();
    } catch (err) {
      const msg = err.response?.data?.detail || 'Failed to cancel RSVP';
      if (showToast) showToast(msg);
    } finally {
      setCancelling(false);
    }
  };

  return (
    <div className="event-card">
      <div className="card-image-wrapper">
        <img
          src={snapshot.image || "https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?auto=format&fit=crop&w=800&q=80"}
          alt={snapshot.title}
          className="card-image"
          onError={(e) => {
            e.target.src = "https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?auto=format&fit=crop&w=800&q=80";
          }}
        />
        <span className="category-badge">{snapshot.category || "Confirmed"}</span>
      </div>

      <div className="card-content">
        <h3 className="card-title">{snapshot.title}</h3>
        <div className="card-meta">
          <div>📍 {snapshot.venue}, {snapshot.city}</div>
          <div>📅 {snapshot.date} • ⏰ {snapshot.time}</div>
        </div>

        <div className="card-footer">
          <span style={{ fontSize: '0.8rem', color: '#10b981', fontWeight: 600 }}>
            ✓ Confirmed
          </span>
          <button
            className="btn btn-danger"
            onClick={handleCancel}
            disabled={cancelling}
            style={{ padding: '0.4rem 0.8rem', fontSize: '0.8rem' }}
          >
            {cancelling ? 'Cancelling...' : 'Cancel RSVP'}
          </button>
        </div>
      </div>
    </div>
  );
}
