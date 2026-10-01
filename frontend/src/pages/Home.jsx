import React, { useEffect, useState, useCallback } from 'react';
import { getEvents, getWsUrl } from '../services/api';
import EventCard from '../components/EventCard';
import EventCalendar from '../components/EventCalendar';
import Loading from '../components/Loading';

export default function Home({ currentUser, showToast }) {
  const [events, setEvents] = useState([]);
  const [source, setSource] = useState('mock');
  const [loading, setLoading] = useState(true);

  // Filters
  const [keyword, setKeyword] = useState('');
  const [city, setCity] = useState('');
  const [category, setCategory] = useState('all');
  const [selectedDate, setSelectedDate] = useState(null);

  const fetchEvents = useCallback(async () => {
    setLoading(true);
    try {
      const data = await getEvents({
        keyword,
        city,
        category,
        date: selectedDate,
        userId: currentUser?.id
      });
      setEvents(data.events || []);
      setSource(data.source || 'mock');
    } catch (err) {
      console.error('Failed to fetch events', err);
      if (showToast) showToast('Failed to load events feed');
    } finally {
      setLoading(false);
    }
  }, [keyword, city, category, selectedDate, currentUser]);

  useEffect(() => {
    fetchEvents();
  }, [fetchEvents]);

  // WebSocket Real-time listener for rsvp_updated
  useEffect(() => {
    const wsUrl = getWsUrl();
    let socket;
    try {
      socket = new WebSocket(wsUrl);
      socket.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data);
          if (payload.type === 'rsvp_updated') {
            setEvents((prevEvents) =>
              prevEvents.map((ev) => {
                if (ev.id === payload.eventId && currentUser?.id === payload.creatorUserId) {
                  return { ...ev, friendsAttending: payload.friendsAttending };
                }
                return ev;
              })
            );
          }
        } catch (ex) {
          console.error('WebSocket parse error', ex);
        }
      };
    } catch (err) {
      console.error('WebSocket setup error', err);
    }

    return () => {
      if (socket) socket.close();
    };
  }, [currentUser]);

  return (
    <div>
      <div style={{ marginBottom: '2rem', textAlign: 'center' }}>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 800, background: 'linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
          Discover & Track Events
        </h1>
        <p style={{ color: '#94a3b8', marginTop: '0.5rem' }}>
          Find concerts, tech summits, sports matches, and share invites with friends in real-time.
        </p>

        <div style={{ marginTop: '0.8rem' }}>
          <span style={{
            fontSize: '0.75rem',
            padding: '4px 10px',
            borderRadius: '12px',
            background: source === 'ticketmaster' ? 'rgba(16, 185, 129, 0.2)' : 'rgba(234, 179, 8, 0.2)',
            color: source === 'ticketmaster' ? '#10b981' : '#eab308',
            border: '1px solid rgba(255,255,255,0.1)'
          }}>
            Feed Source: {source.toUpperCase()}
          </span>
        </div>
      </div>

      {/* Filter Controls */}
      <div style={{
        background: '#1e293b',
        padding: '1.2rem',
        borderRadius: '16px',
        border: '1px solid rgba(255,255,255,0.1)',
        marginBottom: '1.5rem',
        display: 'flex',
        flexWrap: 'wrap',
        gap: '1rem',
        alignItems: 'center'
      }}>
        <div style={{ flex: 1, minWidth: '200px' }}>
          <input
            type="text"
            className="chat-input"
            style={{ width: '100%', padding: '0.6rem 1rem' }}
            placeholder="🔍 Search title, venue..."
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
          />
        </div>

        <div style={{ width: '160px' }}>
          <select
            className="user-select"
            style={{ width: '100%', background: '#0f172a', padding: '0.6rem', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.1)' }}
            value={city}
            onChange={(e) => setCity(e.target.value)}
          >
            <option value="">All Cities</option>
            <option value="Mumbai">Mumbai</option>
            <option value="Pune">Pune</option>
            <option value="New York">New York</option>
            <option value="Bangalore">Bangalore</option>
          </select>
        </div>

        <div style={{ width: '160px' }}>
          <select
            className="user-select"
            style={{ width: '100%', background: '#0f172a', padding: '0.6rem', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.1)' }}
            value={category}
            onChange={(e) => setCategory(e.target.value)}
          >
            <option value="all">All Categories</option>
            <option value="Music">Music</option>
            <option value="Technology">Technology</option>
            <option value="Sports">Sports</option>
            <option value="Arts">Arts</option>
            <option value="Food">Food</option>
          </select>
        </div>

        {selectedDate && (
          <button
            className="btn btn-secondary"
            onClick={() => setSelectedDate(null)}
            style={{ padding: '0.6rem 1rem', fontSize: '0.85rem' }}
          >
            📅 Date: {selectedDate} ✕
          </button>
        )}
      </div>

      {/* Calendar View */}
      <EventCalendar
        events={events}
        selectedDate={selectedDate}
        onSelectDate={setSelectedDate}
      />

      {/* Events Feed */}
      {loading ? (
        <Loading text="Fetching events..." />
      ) : events.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '3rem', color: '#94a3b8' }}>
          No events found matching your search filters. Try clearing filters!
        </div>
      ) : (
        <div className="events-grid">
          {events.map((ev) => (
            <EventCard
              key={ev.id}
              event={ev}
              currentUser={currentUser}
              onRSVPChange={fetchEvents}
              showToast={showToast}
            />
          ))}
        </div>
      )}
    </div>
  );
}
