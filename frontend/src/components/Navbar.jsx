import React, { useEffect, useState } from 'react';
import { NavLink } from 'react-router-dom';
import { getUsers } from '../services/api';

export default function Navbar({ currentUser, setCurrentUser }) {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    getUsers()
      .then((data) => {
        setUsers(data);
        if (!currentUser && data.length > 0) {
          const savedId = localStorage.getItem('activeUserId');
          const matched = data.find((u) => u.id === savedId) || data[0];
          setCurrentUser(matched);
          localStorage.setItem('activeUserId', matched.id);
        }
      })
      .catch((err) => console.error('Failed to load users for Navbar switcher', err));
  }, []);

  const handleUserChange = (e) => {
    const selected = users.find((u) => u.id === e.target.value);
    if (selected) {
      setCurrentUser(selected);
      localStorage.setItem('activeUserId', selected.id);
    }
  };

  return (
    <nav className="navbar">
      <div className="brand">
        ⚡ EventVibe
      </div>
      <div className="nav-links">
        <NavLink to="/" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
          Home
        </NavLink>
        <NavLink to="/dashboard" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
          Dashboard
        </NavLink>
        <NavLink to="/profile" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
          Profile
        </NavLink>

        <div className="user-switcher">
          <span style={{ fontSize: '0.8rem', color: '#94a3b8' }}>User:</span>
          <select
            className="user-select"
            value={currentUser?.id || ''}
            onChange={handleUserChange}
          >
            {users.map((u) => (
              <option key={u.id} value={u.id}>
                {u.name} ({u.email})
              </option>
            ))}
          </select>
        </div>
      </div>
    </nav>
  );
}
