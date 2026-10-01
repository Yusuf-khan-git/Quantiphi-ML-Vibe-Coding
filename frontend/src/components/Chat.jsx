import React, { useState } from 'react';
import { sendChatMessage } from '../services/api';

export default function Chat({ currentUser }) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      sender: 'bot',
      text: "Hi! I'm your Intelligent Event Assistant. Ask me things like:\n- Show music events\n- Events today / this week\n- Events in Mumbai\n- What events am I attending?"
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userText = input.trim();
    setInput('');
    setMessages((prev) => [...prev, { sender: 'user', text: userText }]);
    setLoading(true);

    try {
      const data = await sendChatMessage(userText, currentUser?.id);
      setMessages((prev) => [
        ...prev,
        {
          sender: 'bot',
          text: data.reply,
          events: data.events || []
        }
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: 'bot', text: 'Sorry, I ran into an error processing your query. Please try again.' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      {isOpen ? (
        <div className="chat-box">
          <div className="chat-header">
            <span>🤖 Event Assistant</span>
            <button
              onClick={() => setIsOpen(false)}
              style={{ background: 'none', border: 'none', color: '#94a3b8', cursor: 'pointer', fontSize: '1.2rem' }}
            >
              ✕
            </button>
          </div>

          <div className="chat-messages">
            {messages.map((msg, idx) => (
              <div key={idx} className={`chat-bubble ${msg.sender}`}>
                <div style={{ whitespace: 'pre-line' }}>{msg.text}</div>
                {msg.events && msg.events.length > 0 && (
                  <div style={{ marginTop: '0.5rem', display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
                    {msg.events.slice(0, 3).map((ev) => (
                      <div
                        key={ev.id}
                        style={{
                          background: 'rgba(0,0,0,0.2)',
                          padding: '0.4rem',
                          borderRadius: '6px',
                          fontSize: '0.75rem'
                        }}
                      >
                        <strong>{ev.title}</strong>
                        <div>📍 {ev.venue}, {ev.city} • 📅 {ev.date}</div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
            {loading && <div className="chat-bubble bot">Thinking...</div>}
          </div>

          <form className="chat-input-row" onSubmit={handleSend}>
            <input
              type="text"
              className="chat-input"
              placeholder="Ask assistant..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
            <button type="submit" className="btn btn-primary" style={{ padding: '0.4rem 0.8rem' }}>
              Send
            </button>
          </form>
        </div>
      ) : (
        <button className="chat-toggle-btn" onClick={() => setIsOpen(true)} title="Open Event Assistant">
          💬
        </button>
      )}
    </div>
  );
}
