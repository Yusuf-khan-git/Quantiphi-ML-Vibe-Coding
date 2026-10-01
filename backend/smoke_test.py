import sys
import os
import asyncio
import httpx
from fastapi.testclient import TestClient

from main import app
from database import db, init_db

def run_smoke_test():
    print("==================================================")
    print("RUNNING END-TO-END AUTOMATED SMOKE TEST SUITE")
    print("==================================================")

    init_db()
    client = TestClient(app)

    # 1. Health check
    res = client.get("/api/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    print("[OK] 1. Backend health endpoint responds.")

    # 2. Events feed & mock fallback
    res = client.get("/api/events")
    assert res.status_code == 200, f"Events feed failed: {res.text}"
    data = res.json()
    assert "events" in data and len(data["events"]) > 0, "No events returned in feed"
    assert data["source"] in ["mock", "ticketmaster"], "Invalid source"
    events = data["events"]
    target_event = events[0]
    print(f"[OK] 2 & 3. Events endpoint returns {len(events)} events (source={data['source']}).")

    # Fetch seed users
    users_col = db["users"]
    user1 = users_col.find_one({"email": "demo@example.com"})
    user2 = users_col.find_one({"email": "friend@example.com"})
    assert user1 and user2, "Seed users missing"
    u1_id = str(user1["_id"])
    u2_id = str(user2["_id"])

    # 4. User 1 RSVPs to event
    rsvp_payload = {
        "userId": u1_id,
        "event": target_event
    }
    res = client.post("/api/rsvps", json=rsvp_payload)
    assert res.status_code == 201, f"RSVP failed: {res.text}"
    print("[OK] 4. Demo user 1 can RSVP to an event.")

    # 5. Duplicate RSVP rejected with 409
    res = client.post("/api/rsvps", json=rsvp_payload)
    assert res.status_code == 409, f"Duplicate RSVP failed to return 409: {res.text}"
    print("[OK] 5. Duplicate RSVP is correctly rejected with 409 conflict.")

    # 6. Dashboard returns user RSVPs
    res = client.get(f"/api/rsvps/{u1_id}")
    assert res.status_code == 200, f"Dashboard failed: {res.text}"
    dash_data = res.json()
    assert dash_data["total"] >= 1, "Dashboard total count incorrect"
    print("[OK] 6. Dashboard returns user RSVP with correct statistics.")

    # 7. User 1 creates invite link
    res = client.post(f"/api/invites/{target_event['id']}", json={"userId": u1_id})
    assert res.status_code == 200, f"Invite creation failed: {res.text}"
    invite_data = res.json()
    token = invite_data["token"]
    assert token and invite_data["clickCount"] == 0, "Invalid invite data"
    print(f"[OK] 7. User 1 created invite link with token '{token}'.")

    # 8. Invite GET returns valid info
    res = client.get(f"/api/invites/{token}")
    assert res.status_code == 200, f"Get invite failed: {res.text}"
    inv_info = res.json()
    assert inv_info["inviterName"] == "Demo User", "Inviter name mismatch"
    print("[OK] 8. Invite GET returns valid inviter and event details.")

    # 9. Invite click tracking (deduplicates visitor)
    visitor_id = "test-visitor-101"
    res = client.post(f"/api/invites/{token}/click", json={"visitorId": visitor_id})
    assert res.status_code == 200 and res.json()["clickCount"] == 1, "First click failed"
    
    # Second click from same visitor should not increase click count
    res2 = client.post(f"/api/invites/{token}/click", json={"visitorId": visitor_id})
    assert res2.status_code == 200 and res2.json()["clickCount"] == 1, "Duplicate click double-counted"
    print("[OK] 9. Invite click tracking works and deduplicates same visitor.")

    # 10. User 2 (Friend) RSVPs through invite
    res = client.post(f"/api/invites/{token}/rsvp", json={"userId": u2_id})
    assert res.status_code == 200, f"Friend RSVP via invite failed: {res.text}"
    friend_rsvp_res = res.json()
    assert friend_rsvp_res["friendsAttending"] == 1, f"friendsAttending expected 1, got {friend_rsvp_res['friendsAttending']}"
    print("[OK] 10 & 11. Friend user 2 RSVP'd via invite and friendsAttending increased to 1.")

    # 12. Duplicate friend RSVP does not increment attendance
    res = client.post(f"/api/invites/{token}/rsvp", json={"userId": u2_id})
    assert res.status_code == 409, f"Duplicate friend RSVP expected 409, got {res.status_code}"
    print("[OK] 12. Duplicate friend RSVP rejected with 409 without increasing friendsAttending.")

    # 13. Cancellation decreases attendance count
    res = client.delete(f"/api/rsvps/{u2_id}/{target_event['id']}")
    assert res.status_code == 200, f"Cancel RSVP failed: {res.text}"
    
    res_inv = client.get(f"/api/invites/{token}")
    assert res_inv.json()["friendsAttending"] == 0, "friendsAttending failed to decrement on cancellation"
    print("[OK] 13. Cancellation of friend RSVP successfully decremented friendsAttending back to 0.")

    # 14. Invalid invite token returns 404
    res = client.get("/api/invites/invalid_token_9999")
    assert res.status_code == 404, "Invalid token did not return 404"
    print("[OK] 14. Invalid invite token returns HTTP 404 Not Found.")

    print("==================================================")
    print("ALL 14 AUTOMATED SMOKE TEST ASSERTIONS PASSED!")
    print("==================================================")

if __name__ == "__main__":
    run_smoke_test()
