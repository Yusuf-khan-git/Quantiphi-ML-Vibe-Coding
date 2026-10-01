from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class ReminderSettings(BaseModel):
    enabled: bool = True
    beforeMinutes: int = Field(default=60, ge=1, le=10080)

class UserBase(BaseModel):
    name: str
    email: str
    reminderSettings: ReminderSettings = Field(default_factory=ReminderSettings)

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    reminderSettings: ReminderSettings
    createdAt: datetime

class ReminderUpdateRequest(BaseModel):
    enabled: bool
    beforeMinutes: int = Field(ge=1, le=10080)

class EventSnapshot(BaseModel):
    id: Optional[str] = None
    title: str
    venue: Optional[str] = "Venue TBD"
    city: Optional[str] = "City TBD"
    date: str
    time: Optional[str] = "TBD"
    image: Optional[str] = "https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?auto=format&fit=crop&w=800&q=80"
    category: Optional[str] = "General"

class RSVPCreateRequest(BaseModel):
    userId: str
    event: EventSnapshot

class InviteCreateRequest(BaseModel):
    userId: str

class InviteClickRequest(BaseModel):
    visitorId: str
    userId: Optional[str] = None

class InviteRSVPRequest(BaseModel):
    userId: str

class ChatRequest(BaseModel):
    message: str
    userId: Optional[str] = None
