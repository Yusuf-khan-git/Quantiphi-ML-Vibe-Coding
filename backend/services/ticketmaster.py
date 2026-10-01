import os
import logging
from datetime import datetime, timedelta
import httpx
from typing import List, Dict, Any, Optional

logger = logging.getLogger("uvicorn.error")

TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY", "").strip()
TICKETMASTER_BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"

def get_relative_date(days_offset: int) -> str:
    target_date = datetime.now() + timedelta(days=days_offset)
    return target_date.strftime("%Y-%m-%d")

def generate_mock_events() -> List[Dict[str, Any]]:
    today = get_relative_date(0)
    tomorrow = get_relative_date(1)
    in_3_days = get_relative_date(3)
    in_7_days = get_relative_date(7)
    in_14_days = get_relative_date(14)
    in_30_days = get_relative_date(30)
    past_date = get_relative_date(-15)

    return [
        {
            "id": "mock-1",
            "title": "TechVibe AI & ML Conference 2026",
            "venue": "Bandra Kurla Complex Auditorium",
            "city": "Mumbai",
            "date": today,
            "time": "10:00 AM",
            "category": "Technology",
            "image": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": "mock-2",
            "title": "Sunburn Live EDM Concert",
            "venue": "Mahalaxmi Racecourse",
            "city": "Mumbai",
            "date": in_3_days,
            "time": "06:30 PM",
            "category": "Music",
            "image": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": "mock-3",
            "title": "Pune Hackathon & Developer Meetup",
            "venue": "Magarpatta Cybercity Hub",
            "city": "Pune",
            "date": tomorrow,
            "time": "09:00 AM",
            "category": "Technology",
            "image": "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": "mock-4",
            "title": "Classical Symphony Night",
            "venue": "Bal Gandharva Rang Mandir",
            "city": "Pune",
            "date": in_7_days,
            "time": "07:00 PM",
            "category": "Music",
            "image": "https://images.unsplash.com/photo-1465847899084-d164df4dedc6?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": "mock-5",
            "title": "IPL T20 Cricket Championship Match",
            "venue": "Wankhede Stadium",
            "city": "Mumbai",
            "date": in_14_days,
            "time": "07:30 PM",
            "category": "Sports",
            "image": "https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": "mock-6",
            "title": "Global Tech Summit 2026",
            "venue": "Javits Center",
            "city": "New York",
            "date": in_30_days,
            "time": "09:00 AM",
            "category": "Technology",
            "image": "https://images.unsplash.com/photo-1505373877841-8d25f7d46678?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": "mock-7",
            "title": "Broadway Musical Extravaganza",
            "venue": "Majestic Theatre",
            "city": "New York",
            "date": today,
            "time": "08:00 PM",
            "category": "Arts",
            "image": "https://images.unsplash.com/photo-1507676184212-d03ab07a01bf?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": "mock-8",
            "title": "Bangalore Food & Craft Beer Festival",
            "venue": "Palace Grounds",
            "city": "Bangalore",
            "date": in_3_days,
            "time": "12:00 PM",
            "category": "Food",
            "image": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": "mock-9",
            "title": "Startup Pitch Night & Founder Expo",
            "venue": "Indiranagar Innovation Hub",
            "city": "Bangalore",
            "date": in_7_days,
            "time": "05:00 PM",
            "category": "Technology",
            "image": "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": "mock-10",
            "title": "Contemporary Modern Art Exhibition",
            "venue": "National Gallery of Modern Art",
            "city": "Mumbai",
            "date": in_14_days,
            "time": "11:00 AM",
            "category": "Arts",
            "image": "https://images.unsplash.com/photo-1561214115-f2f134cc4912?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": "mock-11",
            "title": "Marathon & Health Expo",
            "venue": "Shree Shiv Chhatrapati Sports Complex",
            "city": "Pune",
            "date": in_30_days,
            "time": "06:00 AM",
            "category": "Sports",
            "image": "https://images.unsplash.com/photo-1452626038306-9aae5e071dd3?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": "mock-12",
            "title": "Street Food Carnival 2026",
            "venue": "Juhu Beach Plaza",
            "city": "Mumbai",
            "date": past_date,
            "time": "04:00 PM",
            "category": "Food",
            "image": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": "mock-13",
            "title": "Indie Rock Night Live",
            "venue": "Hard Rock Cafe Bengaluru",
            "city": "Bangalore",
            "date": tomorrow,
            "time": "08:30 PM",
            "category": "Music",
            "image": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": "mock-14",
            "title": "New York Marathon Warmup",
            "venue": "Central Park Parkside",
            "city": "New York",
            "date": in_7_days,
            "time": "07:00 AM",
            "category": "Sports",
            "image": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?auto=format&fit=crop&w=800&q=80"
        }
    ]

def filter_mock_events(
    city: Optional[str] = None,
    keyword: Optional[str] = None,
    category: Optional[str] = None,
    date: Optional[str] = None
) -> List[Dict[str, Any]]:
    events = generate_mock_events()
    filtered = []
    for ev in events:
        if city and city.strip():
            if city.strip().lower() not in ev["city"].lower():
                continue
        if category and category.strip() and category.lower() != "all":
            if category.strip().lower() not in ev["category"].lower():
                continue
        if keyword and keyword.strip():
            kw = keyword.strip().lower()
            if kw not in ev["title"].lower() and kw not in ev["venue"].lower() and kw not in ev["category"].lower():
                continue
        if date and date.strip():
            if ev["date"] != date.strip():
                continue
        filtered.append(ev)
    return filtered

async def fetch_ticketmaster_events(
    city: Optional[str] = None,
    keyword: Optional[str] = None,
    category: Optional[str] = None,
    date: Optional[str] = None
) -> Dict[str, Any]:
    if not TICKETMASTER_API_KEY:
        logger.info("No Ticketmaster API key provided. Using mock event fallback.")
        return {"events": filter_mock_events(city, keyword, category, date), "source": "mock"}

    params = {
        "apikey": TICKETMASTER_API_KEY,
        "size": 20
    }
    if city and city.strip():
        params["city"] = city.strip()
    if keyword and keyword.strip():
        params["keyword"] = keyword.strip()
    if category and category.strip() and category.lower() != "all":
        params["classificationName"] = category.strip()
    if date and date.strip():
        # Ticketmaster expects ISO string range or startDateTime format
        params["startDateTime"] = f"{date.strip()}T00:00:00Z"

    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.get(TICKETMASTER_BASE_URL, params=params)
            if resp.status_code != 200:
                logger.warning(f"Ticketmaster API returned HTTP {resp.status_code}. Using mock fallback.")
                return {"events": filter_mock_events(city, keyword, category, date), "source": "mock"}
            data = resp.json()
            raw_events = data.get("_embedded", {}).get("events", [])
            normalized_events = []
            for item in raw_events:
                try:
                    event_id = item.get("id", f"tm-{len(normalized_events)}")
                    title = item.get("name", "Untitled Event")
                    
                    # Extract venue & city safely
                    venues = item.get("_embedded", {}).get("venues", [])
                    venue_name = venues[0].get("name", "Venue TBD") if venues else "Venue TBD"
                    city_name = venues[0].get("city", {}).get("name", "City TBD") if venues else "City TBD"

                    # Extract date & time safely
                    start_dates = item.get("dates", {}).get("start", {})
                    event_date = start_dates.get("localDate", get_relative_date(0))
                    event_time = start_dates.get("localTime", "TBD")

                    # Extract category
                    classifications = item.get("classifications", [])
                    cat_name = "General"
                    if classifications:
                        cat_name = classifications[0].get("segment", {}).get("name", "General")

                    # Extract image safely
                    images = item.get("images", [])
                    img_url = images[0].get("url") if images else "https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?auto=format&fit=crop&w=800&q=80"

                    normalized_events.append({
                        "id": event_id,
                        "title": title,
                        "venue": venue_name,
                        "city": city_name,
                        "date": event_date,
                        "time": event_time,
                        "category": cat_name,
                        "image": img_url
                    })
                except Exception as ex:
                    logger.error(f"Error normalizing single Ticketmaster event: {ex}")

            return {"events": normalized_events, "source": "ticketmaster"}
    except Exception as e:
        logger.error(f"Ticketmaster API request failed: {e}. Using mock fallback.")
        return {"events": filter_mock_events(city, keyword, category, date), "source": "mock"}
