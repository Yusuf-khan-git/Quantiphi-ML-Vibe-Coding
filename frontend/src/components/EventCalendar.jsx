import React, { useState } from 'react';

export default function EventCalendar({ events = [], selectedDate, onSelectDate }) {
  const [currentDate, setCurrentDate] = useState(new Date());

  const year = currentDate.getFullYear();
  const month = currentDate.getMonth();

  const monthNames = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];

  // First day of current month
  const firstDayIndex = new Date(year, month, 1).getDay();
  // Total days in current month
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  const prevMonth = () => {
    setCurrentDate(new Date(year, month - 1, 1));
  };

  const nextMonth = () => {
    setCurrentDate(new Date(year, month + 1, 1));
  };

  // Map of "YYYY-MM-DD" -> array of events
  const eventDateSet = new Set(events.map(ev => ev.date));

  const daysArray = [];
  for (let i = 0; i < firstDayIndex; i++) {
    daysArray.push(null);
  }
  for (let d = 1; d <= daysInMonth; d++) {
    daysArray.push(d);
  }

  const handleDateClick = (day) => {
    if (!day) return;
    const formattedMonth = String(month + 1).padStart(2, '0');
    const formattedDay = String(day).padStart(2, '0');
    const dateStr = `${year}-${formattedMonth}-${formattedDay}`;

    if (selectedDate === dateStr) {
      onSelectDate(null); // Clear filter if re-clicked
    } else {
      onSelectDate(dateStr);
    }
  };

  return (
    <div className="calendar-card">
      <div className="calendar-header">
        <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>
          📅 {monthNames[month]} {year}
        </h3>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button className="btn btn-secondary" onClick={prevMonth} style={{ padding: '0.3rem 0.6rem' }}>
            &lt; Prev
          </button>
          <button className="btn btn-secondary" onClick={nextMonth} style={{ padding: '0.3rem 0.6rem' }}>
            Next &gt;
          </button>
        </div>
      </div>

      <div className="calendar-grid">
        {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map(day => (
          <div key={day} className="weekday-hdr">{day}</div>
        ))}

        {daysArray.map((day, idx) => {
          if (day === null) {
            return <div key={`empty-${idx}`} className="calendar-day empty" />;
          }

          const formattedMonth = String(month + 1).padStart(2, '0');
          const formattedDay = String(day).padStart(2, '0');
          const dateStr = `${year}-${formattedMonth}-${formattedDay}`;

          const hasEvent = eventDateSet.has(dateStr);
          const isSelected = (selectedDate === dateStr);

          let className = "calendar-day";
          if (hasEvent) className += " has-event";
          if (isSelected) className += " selected";

          return (
            <div
              key={dateStr}
              className={className}
              onClick={() => handleDateClick(day)}
              title={hasEvent ? `Events scheduled on ${dateStr}` : dateStr}
            >
              <span>{day}</span>
              {hasEvent && <span className="dot-indicator" />}
            </div>
          );
        })}
      </div>
    </div>
  );
}
