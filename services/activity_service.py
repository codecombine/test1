import aiosqlite


async def search_activities(
    db: aiosqlite.Connection,
    city: str | None = None,
    district: str | None = None,
    min_age: int | None = None,
    max_age: int | None = None,
    category: str | None = None,
    is_indoor: bool | None = None,
    limit: int = 10,
) -> list[dict]:
    conditions = []
    params = []

    if city:
        conditions.append("location_city LIKE ?")
        params.append(f"%{city}%")
    if district:
        conditions.append("location_district LIKE ?")
        params.append(f"%{district}%")
    if min_age is not None:
        conditions.append("max_age >= ?")
        params.append(min_age)
    if max_age is not None:
        conditions.append("min_age <= ?")
        params.append(max_age)
    if category and category != "all":
        conditions.append("category = ?")
        params.append(category)
    if is_indoor is not None:
        conditions.append("is_indoor = ?")
        params.append(1 if is_indoor else 0)

    where_clause = " AND ".join(conditions) if conditions else "1=1"
    query = f"SELECT * FROM activities WHERE {where_clause} LIMIT ?"
    params.append(limit)

    cursor = await db.execute(query, params)
    columns = [desc[0] for desc in cursor.description]
    rows = await cursor.fetchall()
    return [dict(zip(columns, row)) for row in rows]
