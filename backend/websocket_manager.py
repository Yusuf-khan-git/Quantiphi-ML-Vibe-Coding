from fastapi import WebSocket
from typing import List, Dict, Any
import logging

logger = logging.getLogger("uvicorn.error")

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info("WebSocket client connected")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info("WebSocket client disconnected")

    async def broadcast(self, message: Dict[str, Any]):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting WebSocket message: {e}")
                disconnected.append(connection)
        for conn in disconnected:
            self.disconnect(conn)

    async def broadcast_rsvp_update(self, event_id: str, creator_user_id: str, friends_attending: int, click_count: int = 0):
        payload = {
            "type": "rsvp_updated",
            "eventId": event_id,
            "creatorUserId": creator_user_id,
            "friendsAttending": friends_attending,
            "clickCount": click_count
        }
        await self.broadcast(payload)

ws_manager = ConnectionManager()
