from fastapi import APIRouter, Query
from typing import Optional
from services.ticketmaster import fetch_ticketmaster_events
from services.event_service import enrich_events_with_user_state

router = APIRouter(prefix="/api/events", tags=["events"])

@router.get("")
async def get_events(
    city: Optional[str] = Query(None),
    keyword: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    date: Optional[str] = Query(None),
    userId: Optional[str] = Query(None)
):
    feed = await fetch_ticketmaster_events(city=city, keyword=keyword, category=category, date=date)
    enriched_events = await enrich_events_with_user_state(feed["events"], user_id=userId)
    return {
        "events": enriched_events,
        "source": feed["source"]
    }
