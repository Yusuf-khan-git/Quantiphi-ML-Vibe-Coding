from fastapi import APIRouter, HTTPException
from bson import ObjectId
from database import db, clean_doc
from schemas import ReminderUpdateRequest

router = APIRouter(prefix="/api/users", tags=["users"])

def find_user_doc(user_id: str):
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
    return user

@router.get("")
async def get_all_users():
    users_col = db["users"]
    users = list(users_col.find({}))
    return [clean_doc(u) for u in users]

@router.get("/{user_id}")
async def get_user_profile(user_id: str):
    user = find_user_doc(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return clean_doc(user)

@router.put("/{user_id}/reminders")
async def update_user_reminders(user_id: str, req: ReminderUpdateRequest):
    users_col = db["users"]
    user = find_user_doc(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_settings = {
        "enabled": req.enabled,
        "beforeMinutes": req.beforeMinutes
    }

    users_col.update_one(
        {"_id": user["_id"]},
        {"$set": {"reminderSettings": new_settings}}
    )

    updated_user = users_col.find_one({"_id": user["_id"]})
    return clean_doc(updated_user)
