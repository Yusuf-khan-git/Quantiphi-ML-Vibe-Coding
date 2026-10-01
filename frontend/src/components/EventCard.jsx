import React, { useState } from 'react';
import { createRSVP, createInvite } from '../services/api';

export default function EventCard({ event, currentUser, onRSVPChange, showToast }) {
  const [loadingRSVP, setLoadingRSVP] = useState(false);
  const [loadingShare, setLoadingShare] = useState(false);

  const handleRSVP = async () => {
    if (!currentUser) return;
    setLoadingRSVP(true);
    try {
      await createRSVP(currentUser.id, event);
      if (showToast) showToast('RSVP confirmed!');
      if (onRSVPChange) onRSVPChange();
    } catch (err) {
      const msg = err.response?.data?.detail || 'Failed to RSVP';
      if (showToast) showToast(msg);
    } finally {
      setLoadingRSVP(false);
    }
  };

  const handleShare = async () => {
    if (!currentUser) return;
    setLoadingShare(true);
    try {
      const data = await createInvite(event.id, currentUser.id);
      if (data.link) {
        await navigator.clipboard.writeText(data.link);
        if (showToast) showToast('Invite link copied to clipboard!');
      }
    } catch (err) {
      const msg = err.response?.data?.detail || 'Failed to create invite link';
      if (showToast) showToast(msg);
    } finally {
      setLoadingShare(false);
    }
  };

  return (
    <div className="event-card">
      <div className="card-image-wrapper">
        <img
          src={event.image || "https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?auto=format&fit=crop&w=800&q=80"}
          alt={event.title}
          className="card-image"
          onError={(e) => {
            e.target.src = "https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?auto=format&fit=crop&w=800&q=80";
          }}
        />
        <span className="category-badge">{event.category || "General"}</span>
      </div>

      <div className="card-content">
        <h3 className="card-title">{event.title}</h3>
        <div className="card-meta">
          <div>📍 {event.venue}, {event.city}</div>
          <div>📅 {event.date} • ⏰ {event.time}</div>
        </div>

        <div className="card-footer">
          <div className="friends-badge">
            👥 {event.friendsAttending || 0} Friend{(event.friendsAttending || 0) === 1 ? '' : 's'} Attending
          </div>

          <div style={{ display: 'flex', gap: '0.4rem' }}>
            {event.hasRsvped ? (
              <>
                <button className="btn btn-success" disabled style={{ cursor: 'default' }}>
                  Interested ✓
                </button>
                <button
                  className="btn btn-secondary"
                  onClick={handleShare}
                  disabled={loadingShare}
                >
                  {loadingShare ? '...' : '🔗 Share'}
                </button>
              </>
            ) : (
              <button
                className="btn btn-primary"
                onClick={handleRSVP}
                disabled={loadingRSVP}
              >
                {loadingRSVP ? 'RSVPing...' : '⭐ Interested'}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
