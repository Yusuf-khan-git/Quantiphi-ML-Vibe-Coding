import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const getWsUrl = () => {
  const url = new URL(API_BASE_URL);
  const protocol = url.protocol === 'https:' ? 'wss:' : 'ws:';
  return `${protocol}//${url.host}/ws`;
};

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getEvents = async (params = {}) => {
  const resp = await api.get('/api/events', { params });
  return resp.data;
};

export const createRSVP = async (userId, event) => {
  const resp = await api.post('/api/rsvps', { userId, event });
  return resp.data;
};

export const getUserRSVPs = async (userId) => {
  const resp = await api.get(`/api/rsvps/${userId}`);
  return resp.data;
};

export const cancelRSVP = async (userId, eventId) => {
  const resp = await api.delete(`/api/rsvps/${userId}/${eventId}`);
  return resp.data;
};

export const createInvite = async (eventId, userId) => {
  const resp = await api.post(`/api/invites/${eventId}`, { userId });
  return resp.data;
};

export const getInvite = async (token) => {
  const resp = await api.get(`/api/invites/${token}`);
  return resp.data;
};

export const trackInviteClick = async (token, visitorId, userId = null) => {
  const resp = await api.post(`/api/invites/${token}/click`, { visitorId, userId });
  return resp.data;
};

export const rsvpViaInvite = async (token, userId) => {
  const resp = await api.post(`/api/invites/${token}/rsvp`, { userId });
  return resp.data;
};

export const getUsers = async () => {
  const resp = await api.get('/api/users');
  return resp.data;
};

export const getUserProfile = async (userId) => {
  const resp = await api.get(`/api/users/${userId}`);
  return resp.data;
};

export const updateUserReminders = async (userId, reminderSettings) => {
  const resp = await api.put(`/api/users/${userId}/reminders`, reminderSettings);
  return resp.data;
};

export const sendChatMessage = async (message, userId = null) => {
  const resp = await api.post('/api/chat', { message, userId });
  return resp.data;
};

export default api;
