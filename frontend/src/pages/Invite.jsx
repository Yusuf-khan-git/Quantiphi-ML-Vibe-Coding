import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getInvite, trackInviteClick, rsvpViaInvite } from '../services/api';
import Loading from '../components/Loading';

export default function Invite({ currentUser, showToast }) {
  const { token } = useParams();
  const navigate = useNavigate();

  const [invite, setInvite] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [rsvped, setRsvped] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    let visitorId = localStorage.getItem('visitorId');
    if (!visitorId) {
      visitorId = 'visitor-' + Math.random().toString(36).substring(2, 11) + Date.now();
      localStorage.setItem('visitorId', visitorId);
    }

    setLoading(true);
    getInvite(token)
      .then(async (data) => {
        setInvite(data);
        // Register click once
        try {
          const clickRes = await trackInviteClick(token, visitorId, currentUser?.id);
          setInvite((prev) => ({
            ...prev,
            clickCount: clickRes.clickCount,
            friendsAttending: clickRes.friendsAttending
          }));
        } catch (cErr) {
          console.error('Failed click tracking', cErr);
        }
      })
      .catch((err) => {
        setError(err.response?.data?.detail || 'Invalid or expired invite link.');
      })
      .finally(() => setLoading(false));
  }, [token, currentUser]);

  const handleInviteRSVP = async () => {
    if (!currentUser) return;
    setSubmitting(true);
    try {
      const res = await rsvpViaInvite(token, currentUser.id);
      setRsvped(true);
      setInvite((prev) => ({
        ...prev,
        friendsAttending: res.friendsAttending,
        clickCount: res.clickCount
      }));
      if (showToast) showToast('RSVP confirmed via invite!');
    } catch (err) {
      const msg = err.response?.data?.detail || 'Failed to RSVP via invite';
      if (showToast) showToast(msg);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <Loading text="Loading invitation..." />;

  if (error) {
    return (
      <div style={{ maxWidth: '500px', margin: '3rem auto', textAlign: 'center', background: '#1e293b', padding: '2rem', borderRadius: '16px', border: '1px solid rgba(255,255,255,0.1)' }}>
        <h2 style={{ color: '#ef4444', marginBottom: '1rem' }}>⚠️ Invalid Invitation</h2>
        <p style={{ color: '#94a3b8', marginBottom: '1.5rem' }}>{error}</p>
        <button className="btn btn-primary" onClick={() => navigate('/')}>
          Explore All Events
        </button>
      </div>
    );
  }

  const snapshot = invite.eventSnapshot || {};

  return (
    <div style={{ maxWidth: '600px', margin: '1rem auto' }}>
      <div style={{
        background: '#1e293b',
        border: '1px solid rgba(255,255,255,0.1)',
        borderRadius: '20px',
        overflow: 'hidden',
        boxShadow: '0 12px 36px rgba(0,0,0,0.4)'
      }}>
        <div style={{ position: 'relative', height: '240px' }}>
          <img
            src={snapshot.image || "https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?auto=format&fit=crop&w=800&q=80"}
            alt={snapshot.title}
            style={{ width: '100%', height: '100%', objectFit: 'cover' }}
          />
          <div style={{
            position: 'absolute',
            inset: 0,
            background: 'linear-gradient(to top, rgba(15,23,42,0.95), transparent)'
          }} />
          <div style={{ position: 'absolute', bottom: '16px', left: '20px', right: '20px' }}>
            <span className="category-badge" style={{ position: 'static' }}>
              {snapshot.category || "Event"}
            </span>
            <h1 style={{ fontSize: '1.8rem', fontWeight: 800, marginTop: '0.4rem', color: 'white' }}>
              {snapshot.title}
            </h1>
          </div>
        </div>

        <div style={{ padding: '1.5rem' }}>
          <div style={{
            background: 'rgba(139, 92, 246, 0.15)',
            border: '1px solid rgba(139, 92, 246, 0.3)',
            borderRadius: '12px',
            padding: '1rem',
            marginBottom: '1.5rem',
            textAlign: 'center'
          }}>
            <p style={{ fontSize: '1.1rem', fontWeight: 600, color: '#c084fc' }}>
              🎉 <strong>{invite.inviterName}</strong> invited you to join this event!
            </p>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem', color: '#94a3b8', fontSize: '1rem', marginBottom: '1.5rem' }}>
            <div>📍 <strong>Location:</strong> {snapshot.venue}, {snapshot.city}</div>
            <div>📅 <strong>Date & Time:</strong> {snapshot.date} • {snapshot.time}</div>
          </div>

          {/* Attendance Stats */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gap: '1rem',
            marginBottom: '1.5rem',
            background: '#0f172a',
            padding: '1rem',
            borderRadius: '12px'
          }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '1.4rem', fontWeight: 700, color: '#38bdf8' }}>
                {invite.clickCount || 0}
              </div>
              <div style={{ fontSize: '0.8rem', color: '#64748b' }}>Invite Clicks</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '1.4rem', fontWeight: 700, color: '#10b981' }}>
                {invite.friendsAttending || 0}
              </div>
              <div style={{ fontSize: '0.8rem', color: '#64748b' }}>Friends Attending</div>
            </div>
          </div>

          {/* Action */}
          {rsvped ? (
            <div style={{
              background: 'rgba(16, 185, 129, 0.2)',
              border: '1px solid #10b981',
              color: '#10b981',
              padding: '1rem',
              borderRadius: '12px',
              textAlign: 'center',
              fontWeight: 700
            }}>
              ✓ You have RSVP'd to this event via invitation!
            </div>
          ) : (
            <button
              className="btn btn-primary"
              style={{ width: '100%', padding: '0.9rem', fontSize: '1.1rem' }}
              onClick={handleInviteRSVP}
              disabled={submitting}
            >
              {submitting ? 'Confirming RSVP...' : "⭐ I'm Interested (RSVP)"}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
