# 주말 버디

부모가 주말에 아이와 함께할 활동을 추천해주는 AI 챗봇입니다.

## 기능

- 아이 나이와 위치 기반 맞춤 활동 추천
- 큐레이션 DB (50+ 전국 활동) + 실시간 웹 검색
- Claude AI를 활용한 자연스러운 한국어 대화
- 모바일 친화적 웹 채팅 인터페이스

## 설치 및 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
# .env 파일에 ANTHROPIC_API_KEY, TAVILY_API_KEY 입력

# 서버 실행
uvicorn main:app --reload
```

브라우저에서 `http://localhost:8000` 접속

## 기술 스택

- **Backend**: Python, FastAPI
- **AI**: Claude API (Anthropic SDK)
- **DB**: SQLite (aiosqlite)
- **Web Search**: Tavily API
- **Frontend**: Vanilla HTML/CSS/JS
