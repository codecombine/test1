from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    activities: list[dict] = []
    sources: list[dict] = []


class Activity(BaseModel):
    id: int
    name: str
    category: str
    description: str | None = None
    location_city: str
    location_district: str | None = None
    address: str | None = None
    min_age: int = 0
    max_age: int = 18
    is_indoor: bool = True
    is_free: bool = False
    price_range: str | None = None
    website_url: str | None = None
    phone: str | None = None
    tags: str | None = None
    season: str = "all"
