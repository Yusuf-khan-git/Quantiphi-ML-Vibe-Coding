from typing import List, Dict, Any, Optional
from database import db

async def enrich_events_with_user_state(events: List[Dict[str, Any]], user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    if not user_id:
        for ev in events:
            ev["friendsAttending"] = 0
            ev["hasRsvped"] = False
        return events

    rsvps_col = db["rsvps"]
    invites_col = db["invites"]

    # Fetch all user RSVPs in one query for efficiency
    user_rsvps = set(
        doc["eventId"] for doc in rsvps_col.find({"userId": user_id}, {"eventId": 1})
    )

    # Fetch user's created invites for these events
    event_ids = [ev["id"] for ev in events]
    user_invites = {
        doc["eventId"]: doc.get("friendsAttending", 0)
        for doc in invites_col.find({"creatorUserId": user_id, "eventId": {"$in": event_ids}})
    }

    for ev in events:
        ev_id = ev["id"]
        ev["hasRsvped"] = (ev_id in user_rsvps)
        ev["friendsAttending"] = user_invites.get(ev_id, 0)

    return events
