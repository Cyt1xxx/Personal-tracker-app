from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class TrackerEntryCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TrackerEntryResponse(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime
    owner_id: int

    model_config = ConfigDict(from_attributes=True)

class TrackerEntryUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None