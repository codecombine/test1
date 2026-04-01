import httpx
from datetime import datetime

from config import settings


async def search_web_events(query: str, location: str) -> list[dict]:
    if not settings.TAVILY_API_KEY:
        return [{"title": "웹 검색 미설정", "snippet": "TAVILY_API_KEY가 설정되지 않았습니다.", "url": ""}]

    now = datetime.now()
    month_str = f"{now.year}년 {now.month}월"
    search_query = f"{location} {query} 아이 주말 {month_str}"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": settings.TAVILY_API_KEY,
                    "query": search_query,
                    "search_depth": "advanced",
                    "include_answer": False,
                    "max_results": 5,
                },
            )
            resp.raise_for_status()
            data = resp.json()
    except Exception:
        return [{"title": "검색 실패", "snippet": "웹 검색 중 오류가 발생했습니다.", "url": ""}]

    results = data.get("results", [])
    return [
        {
            "title": r.get("title", ""),
            "snippet": r.get("content", "")[:200],
            "url": r.get("url", ""),
        }
        for r in results
    ]
