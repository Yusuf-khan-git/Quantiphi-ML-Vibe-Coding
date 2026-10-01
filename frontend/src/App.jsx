import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Chat from './components/Chat';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import Profile from './pages/Profile';
import Invite from './pages/Invite';

export default function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [toast, setToast] = useState(null);

  const showToast = (message) => {
    setToast(message);
    setTimeout(() => {
      setToast(null);
    }, 3000);
  };

  return (
    <Router>
      <div className="app-container">
        <Navbar currentUser={currentUser} setCurrentUser={setCurrentUser} />

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home currentUser={currentUser} showToast={showToast} />} />
            <Route path="/dashboard" element={<Dashboard currentUser={currentUser} showToast={showToast} />} />
            <Route path="/profile" element={<Profile currentUser={currentUser} showToast={showToast} />} />
            <Route path="/invite/:token" element={<Invite currentUser={currentUser} showToast={showToast} />} />
          </Routes>
        </main>

        <Chat currentUser={currentUser} />

        {toast && <div className="toast">{toast}</div>}
      </div>
    </Router>
  );
}
