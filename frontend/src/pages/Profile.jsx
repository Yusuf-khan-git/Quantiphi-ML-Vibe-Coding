import React, { useEffect, useState } from 'react';
import { getUserProfile, updateUserReminders } from '../services/api';
import Loading from '../components/Loading';

export default function Profile({ currentUser, showToast }) {
  const [profile, setProfile] = useState(null);
  const [enabled, setEnabled] = useState(true);
  const [beforeMinutes, setBeforeMinutes] = useState(60);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (!currentUser?.id) return;
    setLoading(true);
    getUserProfile(currentUser.id)
      .then((data) => {
        setProfile(data);
        if (data.reminderSettings) {
          setEnabled(data.reminderSettings.enabled ?? true);
          setBeforeMinutes(data.reminderSettings.beforeMinutes ?? 60);
        }
      })
      .catch((err) => {
        console.error('Failed to load profile', err);
        if (showToast) showToast('Failed to load user profile');
      })
      .finally(() => setLoading(false));
  }, [currentUser, showToast]);

  const handleSaveReminders = async (e) => {
    e.preventDefault();
    if (beforeMinutes < 1 || beforeMinutes > 10080) {
      if (showToast) showToast('Minutes must be between 1 and 10080');
      return;
    }

    setSaving(true);
    try {
      const updated = await updateUserReminders(currentUser.id, {
        enabled,
        beforeMinutes: Number(beforeMinutes)
      });
      setProfile(updated);
      if (showToast) showToast('Reminder settings saved!');
    } catch (err) {
      const msg = err.response?.data?.detail || 'Failed to update reminder settings';
      if (showToast) showToast(msg);
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <Loading text="Loading profile..." />;
  if (!profile) return <div style={{ padding: '2rem' }}>User profile not found.</div>;

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto' }}>
      <h1 style={{ fontSize: '2rem', fontWeight: 700, marginBottom: '0.5rem' }}>
        User Profile & Settings
      </h1>
      <p style={{ color: '#94a3b8', marginBottom: '1.5rem' }}>
        Manage your notification reminders and preferences.
      </p>

      {/* User Info Card */}
      <div style={{
        background: '#1e293b',
        border: '1px solid rgba(255,255,255,0.1)',
        borderRadius: '16px',
        padding: '1.5rem',
        marginBottom: '1.5rem'
      }}>
        <h3 style={{ fontSize: '1.2rem', marginBottom: '1rem', color: '#8b5cf6' }}>
          Account Details
        </h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem', fontSize: '0.95rem' }}>
          <div><strong>Name:</strong> {profile.name}</div>
          <div><strong>Email:</strong> {profile.email}</div>
          <div><strong>User ID:</strong> <code style={{ color: '#ec4899' }}>{profile.id}</code></div>
        </div>
      </div>

      {/* Reminder Settings Form */}
      <div style={{
        background: '#1e293b',
        border: '1px solid rgba(255,255,255,0.1)',
        borderRadius: '16px',
        padding: '1.5rem'
      }}>
        <h3 style={{ fontSize: '1.2rem', marginBottom: '1rem', color: '#10b981' }}>
          🔔 Event Reminders
        </h3>

        <form onSubmit={handleSaveReminders} style={{ display: 'flex', flexDirection: 'column', gap: '1.2rem' }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.8rem', cursor: 'pointer' }}>
            <input
              type="checkbox"
              checked={enabled}
              onChange={(e) => setEnabled(e.target.checked)}
              style={{ width: '18px', height: '18px', accentColor: '#8b5cf6' }}
            />
            <span style={{ fontSize: '1rem', fontWeight: 500 }}>
              Enable Event Notifications & Reminders
            </span>
          </label>

          {enabled && (
            <div>
              <label style={{ display: 'block', fontSize: '0.9rem', color: '#94a3b8', marginBottom: '0.4rem' }}>
                Notify me before event starts (Minutes):
              </label>
              <input
                type="number"
                min="1"
                max="10080"
                className="chat-input"
                style={{ width: '100%', padding: '0.6rem' }}
                value={beforeMinutes}
                onChange={(e) => setBeforeMinutes(e.target.value)}
              />
              <span style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '0.2rem', display: 'block' }}>
                Allowed range: 1 to 10,080 minutes (up to 7 days).
              </span>
            </div>
          )}

          <button type="submit" className="btn btn-primary" disabled={saving} style={{ alignSelf: 'flex-start' }}>
            {saving ? 'Saving...' : 'Save Settings'}
          </button>
        </form>
      </div>
    </div>
  );
}
