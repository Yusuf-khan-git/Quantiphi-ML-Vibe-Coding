import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from database import db, clean_doc
from services.ticketmaster import generate_mock_events, fetch_ticketmaster_events

def get_date_str(offset: int) -> str:
    return (datetime.now() + timedelta(days=offset)).strftime("%Y-%m-%d")

async def process_chat_message(message: str, user_id: Optional[str] = None) -> Dict[str, Any]:
    if not message or not message.strip():
        return {
            "reply": "Please ask a question about events! Try asking: 'Show music events' or 'Events today'.",
            "events": []
        }

    msg = message.strip().lower()

    # 1. User RSVP Query: "what events am i attending?", "my rsvps", "my events"
    if "attending" in msg or "my rsvp" in msg or "my events" in msg:
        if not user_id:
            return {
                "reply": "You need to be logged in to view your attending events.",
                "events": []
            }
        
        rsvps_col = db["rsvps"]
        users_col = db["users"]
        
        user = None
        try:
            from bson import ObjectId
            user = users_col.find_one({"_id": ObjectId(user_id)})
        except Exception:
            pass
        if not user:
            user = users_col.find_one({"_id": user_id})
        
        uid = str(user["_id"]) if user else user_id
        rsvps = list(rsvps_col.find({"userId": uid, "status": "confirmed"}))
        events = [r.get("eventSnapshot", {}) for r in rsvps if r.get("eventSnapshot")]
        
        count = len(events)
        if count == 0:
            return {
                "reply": "You haven't RSVP'd to any events yet! Browse events to find something interesting.",
                "events": []
            }
        return {
            "reply": f"You are currently attending {count} confirmed event{'s' if count > 1 else ''}.",
            "events": events
        }

    # 2. Extract Category, City, Date Intent from query
    category = None
    if "music" in msg or "concert" in msg or "song" in msg or "band" in msg:
        category = "Music"
    elif "tech" in msg or "technology" in msg or "ai" in msg or "developer" in msg or "hackathon" in msg:
        category = "Technology"
    elif "sport" in msg or "cricket" in msg or "match" in msg or "marathon" in msg:
        category = "Sports"
    elif "art" in msg or "theater" in msg or "broadway" in msg or "exhibition" in msg:
        category = "Arts"
    elif "food" in msg or "beer" in msg or "carnival" in msg or "eat" in msg:
        category = "Food"

    city = None
    for c in ["mumbai", "pune", "new york", "bangalore"]:
        if c in msg:
            city = c.title()
            break

    target_date = None
    date_label = None

    if "today" in msg:
        target_date = get_date_str(0)
        date_label = "today"
    elif "tomorrow" in msg:
        target_date = get_date_str(1)
        date_label = "tomorrow"
    elif "this week" in msg or "week" in msg:
        date_label = "this week"

    # Fetch events using Ticketmaster/Mock
    feed = await fetch_ticketmaster_events(city=city, category=category)
    all_events = feed["events"]

    # Filter based on parsed intent
    filtered = []
    today_dt = datetime.now().date()
    end_week_dt = today_dt + timedelta(days=7)

    for ev in all_events:
        ev_date_str = ev.get("date", "")
        
        # Date filtering
        if target_date:
            if ev_date_str != target_date:
                continue
        elif date_label == "this week":
            try:
                ev_dt = datetime.strptime(ev_date_str, "%Y-%m-%d").date()
                if not (today_dt <= ev_dt <= end_week_dt):
                    continue
            except Exception:
                pass

        # City filtering
        if city:
            if city.lower() not in ev.get("city", "").lower():
                continue

        # Category filtering
        if category:
            if category.lower() not in ev.get("category", "").lower():
                continue

        filtered.append(ev)

    # Build natural response
    count = len(filtered)
    parts = []
    if category:
        parts.append(f"{category.lower()}")
    parts.append("events")
    if city:
        parts.append(f"in {city}")
    if date_label:
        parts.append(date_label)

    query_desc = " ".join(parts) if parts else "matching events"

    if count > 0:
        reply = f"Found {count} {query_desc} for you."
    else:
        # Fallback to general search if specific query returned 0
        reply = f"No {query_desc} found, but here are some popular upcoming events you might enjoy."
        filtered = all_events[:5]

    return {
        "reply": reply,
        "events": filtered
    }
