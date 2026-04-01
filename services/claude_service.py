import anthropic

from config import settings
from prompts.system_prompt import SYSTEM_PROMPT

client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

TOOLS = [
    {
        "name": "search_activities",
        "description": "큐레이션된 데이터베이스에서 아이와 함께할 활동을 검색합니다. 도시, 구/군, 나이, 카테고리 등으로 필터링할 수 있습니다.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "도시 이름 (예: 서울, 부산, 용인)",
                },
                "district": {
                    "type": "string",
                    "description": "구/군 이름 (예: 강남구, 해운대구)",
                },
                "min_age": {
                    "type": "integer",
                    "description": "아이의 최소 나이",
                },
                "max_age": {
                    "type": "integer",
                    "description": "아이의 최대 나이",
                },
                "category": {
                    "type": "string",
                    "description": "활동 카테고리",
                    "enum": [
                        "playground",
                        "museum",
                        "class",
                        "cafe",
                        "outdoor",
                        "event",
                        "all",
                    ],
                },
                "is_indoor": {
                    "type": "boolean",
                    "description": "실내 활동 여부 (true=실내, false=실외)",
                },
            },
            "required": ["city"],
        },
    },
    {
        "name": "search_web_events",
        "description": "웹에서 최신 어린이 행사, 이벤트, 체험 프로그램을 검색합니다. 현재 진행 중인 행사나 최신 정보를 찾을 때 사용합니다.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "검색 키워드 (예: 어린이 체험, 주말 행사)",
                },
                "location": {
                    "type": "string",
                    "description": "위치 (예: 서울 강남)",
                },
            },
            "required": ["query", "location"],
        },
    },
]


async def chat_with_claude(
    messages: list[dict],
) -> anthropic.types.Message:
    response = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        tools=TOOLS,
        messages=messages,
    )
    return response
