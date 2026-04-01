from fastapi import APIRouter, Depends

import aiosqlite
from database import get_db
from services.activity_service import search_activities

router = APIRouter()


@router.get("/activities")
async def get_activities(
    city: str | None = None,
    district: str | None = None,
    min_age: int | None = None,
    max_age: int | None = None,
    category: str | None = None,
    is_indoor: bool | None = None,
    db: aiosqlite.Connection = Depends(get_db),
):
    results = await search_activities(
        db,
        city=city,
        district=district,
        min_age=min_age,
        max_age=max_age,
        category=category,
        is_indoor=is_indoor,
    )
    return {"activities": results}
