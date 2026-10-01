from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from database import db, clean_doc
from schemas import RSVPCreateRequest
from websocket_manager import ws_manager

router = APIRouter(prefix="/api/rsvps", tags=["rsvps"])

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_rsvp(req: RSVPCreateRequest):
    users_col = db["users"]
    rsvps_col = db["rsvps"]

    # Validate User
    user = None
    try:
        user = users_col.find_one({"_id": ObjectId(req.userId)})
    except Exception:
        user = users_col.find_one({"_id": req.userId})
    
    if not user:
        # Check if userId matches by string _id
        user = users_col.find_one({"$or": [{"_id": req.userId}, {"email": req.userId}]})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_id_str = str(user["_id"])
    event_dict = req.event.model_dump()
    if not event_dict.get("id") or not event_dict.get("title") or not event_dict.get("date"):
        raise HTTPException(status_code=422, detail="Event must include valid id, title, and date")

    rsvp_doc = {
        "userId": user_id_str,
        "eventId": str(event_dict["id"]),
        "eventSnapshot": event_dict,
        "status": "confirmed",
        "inviteToken": None,
        "createdAt": datetime.utcnow()
    }

    try:
        res = rsvps_col.insert_one(rsvp_doc)
        rsvp_doc["_id"] = res.inserted_id
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="User has already RSVP'd to this event")

    return clean_doc(rsvp_doc)

@router.get("/{user_id}")
async def get_user_rsvps(user_id: str):
    rsvps_col = db["rsvps"]
    
    # Verify user exists
    users_col = db["users"]
    user = None
    try:
        user = users_col.find_one({"_id": ObjectId(user_id)})
    except Exception:
        pass
    if not user:
        user = users_col.find_one({"_id": user_id})

    user_id_str = str(user["_id"]) if user else user_id

    rsvps = list(rsvps_col.find({"userId": user_id_str, "status": "confirmed"}).sort("createdAt", -1))
    cleaned_rsvps = [clean_doc(r) for r in rsvps]

    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    total = len(cleaned_rsvps)
    upcoming = sum(1 for r in cleaned_rsvps if r.get("eventSnapshot", {}).get("date", "") >= today_str)

    return {
        "total": total,
        "upcoming": upcoming,
        "rsvps": cleaned_rsvps
    }

@router.delete("/{user_id}/{event_id}")
async def cancel_rsvp(user_id: str, event_id: str):
    rsvps_col = db["rsvps"]
    invites_col = db["invites"]

    users_col = db["users"]
    user = None
    try:
        user = users_col.find_one({"_id": ObjectId(user_id)})
    except Exception:
        pass
    if not user:
        user = users_col.find_one({"_id": user_id})

    user_id_str = str(user["_id"]) if user else user_id

    rsvp = rsvps_col.find_one({"userId": user_id_str, "eventId": event_id})
    if not rsvp:
        raise HTTPException(status_code=404, detail="RSVP not found")

    invite_token = rsvp.get("inviteToken")
    rsvps_col.delete_one({"_id": rsvp["_id"]})

    # If created through an invite link, decrement invite's friendsAttending
    if invite_token:
        invite = invites_col.find_one({"token": invite_token})
        if invite:
            new_friends_count = max(0, invite.get("friendsAttending", 0) - 1)
            invites_col.update_one(
                {"_id": invite["_id"]},
                {"$set": {"friendsAttending": new_friends_count}}
            )
            await ws_manager.broadcast_rsvp_update(
                event_id=event_id,
                creator_user_id=invite["creatorUserId"],
                friends_attending=new_friends_count,
                click_count=invite.get("clickCount", 0)
            )

    return {"message": "RSVP cancelled successfully"}
