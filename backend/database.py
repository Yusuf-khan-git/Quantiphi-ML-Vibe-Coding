import os
import logging
from datetime import datetime
from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, ConnectionFailure, ServerSelectionTimeoutError

load_dotenv()

logger = logging.getLogger("uvicorn.error")

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017").strip()
if not MONGODB_URI:
    MONGODB_URI = "mongodb://localhost:27017"

use_mock = False
try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=2000)
    client.admin.command('ping')
    db = client.get_database("event_db")
    logger.info("Successfully connected to MongoDB server.")
except Exception as e:
    logger.warning(f"MongoDB connection failed ({e}). Falling back to in-memory mongomock database.")
    import mongomock
    client = mongomock.MongoClient()
    db = client.get_database("event_db")
    use_mock = True

# Helper to format object IDs
def clean_doc(doc):
    if not doc:
        return doc
    doc_copy = dict(doc)
    if "_id" in doc_copy:
        doc_copy["id"] = str(doc_copy["_id"])
        del doc_copy["_id"]
    return doc_copy

def init_db():
    users_col = db["users"]
    rsvps_col = db["rsvps"]
    invites_col = db["invites"]
    invite_clicks_col = db["invite_clicks"]

    # Create Indexes safely
    try:
        users_col.create_index([("email", pymongo.ASCENDING)], unique=True)
        rsvps_col.create_index([("userId", pymongo.ASCENDING), ("eventId", pymongo.ASCENDING)], unique=True)
        invites_col.create_index([("token", pymongo.ASCENDING)], unique=True)
        invites_col.create_index([("creatorUserId", pymongo.ASCENDING), ("eventId", pymongo.ASCENDING)], unique=True)
        invite_clicks_col.create_index([("token", pymongo.ASCENDING), ("visitorId", pymongo.ASCENDING)], unique=True)
    except Exception as ex:
        logger.warning(f"Index creation warning: {ex}")

    # Seed Demo Users if empty
    if users_col.count_documents({}) == 0:
        seed_users = [
            {
                "name": "Demo User",
                "email": "demo@example.com",
                "reminderSettings": {"enabled": True, "beforeMinutes": 60},
                "createdAt": datetime.utcnow()
            },
            {
                "name": "Friend User",
                "email": "friend@example.com",
                "reminderSettings": {"enabled": True, "beforeMinutes": 60},
                "createdAt": datetime.utcnow()
            },
            {
                "name": "Friend Two",
                "email": "friend2@example.com",
                "reminderSettings": {"enabled": True, "beforeMinutes": 60},
                "createdAt": datetime.utcnow()
            }
        ]
        for user_data in seed_users:
            try:
                users_col.insert_one(user_data)
            except DuplicateKeyError:
                pass
        logger.info("Demo users seeded successfully.")
