# @mykakao-fe — 기술 스택

- HTML5 + CSS (파일 내 `<style>`) + vanilla JS (파일 내 `<script>`)
- `fetch` — REST (`/api/chats`, `/api/messages`, `/api/search`, `/api/stats`, `/api/summarize`)
- `EventSource` — SSE (`/api/stream` 실시간 메시지, `/api/summarize/stream` 요약 스트림)
- 빌드 도구 없음 · 패키지 매니저 없음 · 프레임워크 없음

## 핵심 원칙
- 최소 변경 · 의존성 0 유지 · BE 계약을 화면 쪽에서 우회하지 않는다
