import React, { useEffect, useState, useCallback } from 'react';
import { getUserRSVPs } from '../services/api';
import RSVPCard from '../components/RSVPCard';
import Loading from '../components/Loading';

export default function Dashboard({ currentUser, showToast }) {
  const [data, setData] = useState({ total: 0, upcoming: 0, rsvps: [] });
  const [loading, setLoading] = useState(true);

  const fetchRSVPs = useCallback(async () => {
    if (!currentUser?.id) return;
    setLoading(true);
    try {
      const res = await getUserRSVPs(currentUser.id);
      setData(res);
    } catch (err) {
      console.error('Failed to load user RSVPs', err);
      if (showToast) showToast('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  }, [currentUser, showToast]);

  useEffect(() => {
    fetchRSVPs();
  }, [fetchRSVPs]);

  return (
    <div>
      <h1 style={{ fontSize: '2rem', fontWeight: 700, marginBottom: '0.5rem' }}>
        My RSVP Dashboard
      </h1>
      <p style={{ color: '#94a3b8', marginBottom: '1.5rem' }}>
        Manage your confirmed event RSVPs and view upcoming schedules.
      </p>

      {/* Stats Header */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '1rem',
        marginBottom: '2rem'
      }}>
        <div style={{
          background: '#1e293b',
          border: '1px solid rgba(255,255,255,0.1)',
          borderRadius: '16px',
          padding: '1.5rem',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '2.5rem', fontWeight: 800, color: '#8b5cf6' }}>{data.total}</div>
          <div style={{ color: '#94a3b8', fontSize: '0.9rem', fontWeight: 600 }}>Total Confirmed RSVPs</div>
        </div>

        <div style={{
          background: '#1e293b',
          border: '1px solid rgba(255,255,255,0.1)',
          borderRadius: '16px',
          padding: '1.5rem',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '2.5rem', fontWeight: 800, color: '#10b981' }}>{data.upcoming}</div>
          <div style={{ color: '#94a3b8', fontSize: '0.9rem', fontWeight: 600 }}>Upcoming Events</div>
        </div>
      </div>

      {loading ? (
        <Loading text="Loading your RSVPs..." />
      ) : data.rsvps.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '3rem', color: '#94a3b8', background: '#1e293b', borderRadius: '16px' }}>
          You haven't RSVP'd to any events yet! Go to the Home feed to explore upcoming events.
        </div>
      ) : (
        <div className="events-grid">
          {data.rsvps.map((rsvp) => (
            <RSVPCard
              key={rsvp.id || rsvp._id}
              rsvp={rsvp}
              currentUser={currentUser}
              onCancelSuccess={fetchRSVPs}
              showToast={showToast}
            />
          ))}
        </div>
      )}
    </div>
  );
}
