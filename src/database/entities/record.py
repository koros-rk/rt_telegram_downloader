from datetime import datetime
from enum import Enum

from bson import ObjectId
from pydantic import BaseModel, Field


class FileType(Enum):
    VIDEO = "video"
    AUDIO = "audio"
    IMAGE = "image"


class Record(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    url: str
    file_type: FileType
    file_ids: list[str] = Field(default_factory=list)
    user_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now())
