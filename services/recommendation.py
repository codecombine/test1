import json

import aiosqlite

from services.claude_service import chat_with_claude
from services.activity_service import search_activities
from services.search_service import search_web_events


async def handle_chat(
    db: aiosqlite.Connection,
    messages: list[dict],
) -> tuple[str, list[dict], list[dict]]:
    """
    Claude tool-use 루프를 실행하여 최종 응답을 생성합니다.

    Returns:
        (reply_text, activities_used, web_sources)
    """
    activities_used = []
    web_sources = []

    response = await chat_with_claude(messages)

    # Tool use 루프: Claude가 tool 호출을 요청하면 실행 후 결과를 다시 전달
    while response.stop_reason == "tool_use":
        tool_results = []

        for block in response.content:
            if block.type != "tool_use":
                continue

            tool_name = block.name
            tool_input = block.input

            if tool_name == "search_activities":
                results = await search_activities(
                    db,
                    city=tool_input.get("city"),
                    district=tool_input.get("district"),
                    min_age=tool_input.get("min_age"),
                    max_age=tool_input.get("max_age"),
                    category=tool_input.get("category"),
                    is_indoor=tool_input.get("is_indoor"),
                )
                activities_used.extend(results)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(results, ensure_ascii=False),
                })

            elif tool_name == "search_web_events":
                results = await search_web_events(
                    query=tool_input.get("query", ""),
                    location=tool_input.get("location", ""),
                )
                web_sources.extend(results)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(results, ensure_ascii=False),
                })

        # Claude에 tool 결과 전달
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})

        response = await chat_with_claude(messages)

    # 최종 텍스트 응답 추출
    reply_text = ""
    for block in response.content:
        if hasattr(block, "text"):
            reply_text += block.text

    return reply_text, activities_used, web_sources
