import os
import logging
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from database import init_db
from websocket_manager import ws_manager
from routes import events, rsvps, invites, users, chat

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn.error")

CLIENT_URL = os.getenv("CLIENT_URL", "http://localhost:5173").rstrip("/")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database and seeding data if needed...")
    try:
        init_db()
    except Exception as e:
        logger.error(f"Error during db initialization: {e}")
    yield

app = FastAPI(
    title="Event Discovery & Tracking Platform API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS setup
origins = [
    CLIENT_URL,
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled server error on {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected server error occurred. Please try again later."}
    )

# Include API Routers
app.include_router(events.router)
app.include_router(rsvps.router)
app.include_router(invites.router)
app.include_router(users.router)
app.include_router(chat.router)

@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            # Keep connection open and receive optional ping messages
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")
        ws_manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
