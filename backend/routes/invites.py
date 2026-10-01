import os
import secrets
from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from database import db, clean_doc
from schemas import InviteCreateRequest, InviteClickRequest, InviteRSVPRequest
from websocket_manager import ws_manager

router = APIRouter(prefix="/api/invites", tags=["invites"])

CLIENT_URL = os.getenv("CLIENT_URL", "http://localhost:5173").rstrip("/")

def resolve_user_id(user_id: str) -> str:
    users_col = db["users"]
    user = None
    try:
        user = users_col.find_one({"_id": ObjectId(user_id)})
    except Exception:
        pass
    if not user:
        user = users_col.find_one({"_id": user_id})
    if not user:
        user = users_col.find_one({"email": user_id})
    return str(user["_id"]) if user else user_id

@router.post("/{event_id}")
async def create_invite(event_id: str, req: InviteCreateRequest):
    users_col = db["users"]
    rsvps_col = db["rsvps"]
    invites_col = db["invites"]

    user_id = resolve_user_id(req.userId)

    # Check user existence
    user = users_col.find_one({"_id": ObjectId(user_id)}) if ObjectId.is_valid(user_id) else users_col.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # User must already be RSVP'd to the event
    rsvp = rsvps_col.find_one({"userId": user_id, "eventId": event_id})
    if not rsvp:
        raise HTTPException(status_code=403, detail="Must be RSVP'd to the event to generate an invite link")

    # Return existing invite if it already exists
    existing_invite = invites_col.find_one({"creatorUserId": user_id, "eventId": event_id})
    if existing_invite:
        token = existing_invite["token"]
        return {
            "token": token,
            "link": f"{CLIENT_URL}/invite/{token}",
            "clickCount": existing_invite.get("clickCount", 0),
            "friendsAttending": existing_invite.get("friendsAttending", 0)
        }

    token = secrets.token_urlsafe(8)
    invite_doc = {
        "token": token,
        "eventId": event_id,
        "eventSnapshot": rsvp.get("eventSnapshot", {}),
        "creatorUserId": user_id,
        "clickCount": 0,
        "friendsAttending": 0,
        "createdAt": datetime.utcnow()
    }

    try:
        invites_col.insert_one(invite_doc)
    except DuplicateKeyError:
        existing = invites_col.find_one({"creatorUserId": user_id, "eventId": event_id})
        if existing:
            token = existing["token"]
            return {
                "token": token,
                "link": f"{CLIENT_URL}/invite/{token}",
                "clickCount": existing.get("clickCount", 0),
                "friendsAttending": existing.get("friendsAttending", 0)
            }

    return {
        "token": token,
        "link": f"{CLIENT_URL}/invite/{token}",
        "clickCount": 0,
        "friendsAttending": 0
    }

@router.get("/{token}")
async def get_invite(token: str):
    invites_col = db["invites"]
    users_col = db["users"]

    invite = invites_col.find_one({"token": token})
    if not invite:
        raise HTTPException(status_code=404, detail="Invite link not found or expired")

    creator_id = invite.get("creatorUserId")
    creator = None
    try:
        creator = users_col.find_one({"_id": ObjectId(creator_id)})
    except Exception:
        creator = users_col.find_one({"_id": creator_id})

    creator_name = creator["name"] if creator else "A friend"

    cleaned = clean_doc(invite)
    cleaned["inviterName"] = creator_name
    cleaned["link"] = f"{CLIENT_URL}/invite/{token}"
    return cleaned

@router.post("/{token}/click")
async def track_invite_click(token: str, req: InviteClickRequest):
    invites_col = db["invites"]
    clicks_col = db["invite_clicks"]

    invite = invites_col.find_one({"token": token})
    if not invite:
        raise HTTPException(status_code=404, detail="Invite link not found")

    creator_id = invite.get("creatorUserId")
    visitor_id = req.visitorId

    # Do not count click if visitor is the creator
    if visitor_id == creator_id or (req.userId and resolve_user_id(req.userId) == creator_id):
        return {
            "clickCount": invite.get("clickCount", 0),
            "friendsAttending": invite.get("friendsAttending", 0),
            "counted": False
        }

    click_doc = {
        "token": token,
        "visitorId": visitor_id,
        "clickedAt": datetime.utcnow()
    }

    try:
        clicks_col.insert_one(click_doc)
        # Increase clickCount ONLY on new insertion
        invites_col.update_one({"_id": invite["_id"]}, {"$inc": {"clickCount": 1}})
        updated_invite = invites_col.find_one({"_id": invite["_id"]})
        return {
            "clickCount": updated_invite.get("clickCount", 0),
            "friendsAttending": updated_invite.get("friendsAttending", 0),
            "counted": True
        }
    except DuplicateKeyError:
        # Already clicked by this visitor ID
        return {
            "clickCount": invite.get("clickCount", 0),
            "friendsAttending": invite.get("friendsAttending", 0),
            "counted": False
        }

@router.post("/{token}/rsvp")
async def rsvp_via_invite(token: str, req: InviteRSVPRequest):
    invites_col = db["invites"]
    rsvps_col = db["rsvps"]

    user_id = resolve_user_id(req.userId)

    invite = invites_col.find_one({"token": token})
    if not invite:
        raise HTTPException(status_code=404, detail="Invite token not found")

    creator_id = invite.get("creatorUserId")
    if user_id == creator_id:
        raise HTTPException(status_code=403, detail="Creator cannot RSVP through their own invite link")

    event_id = invite["eventId"]
    event_snapshot = invite.get("eventSnapshot", {})

    rsvp_doc = {
        "userId": user_id,
        "eventId": event_id,
        "eventSnapshot": event_snapshot,
        "status": "confirmed",
        "inviteToken": token,
        "createdAt": datetime.utcnow()
    }

    try:
        rsvps_col.insert_one(rsvp_doc)
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="User has already RSVP'd to this event")

    # Increment friendsAttending ONLY after successful new RSVP
    invites_col.update_one({"_id": invite["_id"]}, {"$inc": {"friendsAttending": 1}})
    updated_invite = invites_col.find_one({"_id": invite["_id"]})

    new_friends_count = updated_invite.get("friendsAttending", 0)
    click_count = updated_invite.get("clickCount", 0)

    # Broadcast WebSocket update
    await ws_manager.broadcast_rsvp_update(
        event_id=event_id,
        creator_user_id=creator_id,
        friends_attending=new_friends_count,
        click_count=click_count
    )

    return {
        "message": "RSVP confirmed via invite!",
        "friendsAttending": new_friends_count,
        "clickCount": click_count,
        "rsvp": clean_doc(rsvp_doc)
    }
