# @mykakao-fe — 도구 및 구조

## 작업 디렉토리
- 실제 작업 위치·base 는 dispatch brief 의 `작업 워크트리`·`base 브랜치`가 SSOT
- **첫 액션**: `git branch --show-current` → `frontend/index.html`·`frontend/summary.html` 통독

## 탐색 경로 (레포 루트 기준)
```
frontend/index.html    # 방 목록 · 메시지 · 검색 · LIVE · 날짜선택 → 요약 진입
frontend/summary.html  # 프롬프트 작성 → SSE 스트리밍 렌더
backend/main.py        # (읽기만) API·SSE 계약의 실제 모습
```

> `backend/main.py` 는 **읽어도 되고 읽어야 한다** — 계약 확인용. 고치지는 않는다.

## 자주 쓰는 명령
- `node --check <뽑아낸 script 블록>` — JS 문법 확인
- 서버 기동 금지 (코디네이터 몫)

## 금지 사항
- `backend/`·`worker/`·compose 수정 금지 · 문서 SoT 수정 금지
- git commit·push·PR 금지 — 워크트리에 변경만 남긴다
- 라이브러리·CDN·빌드 도구 추가 금지 (필요하면 보고)
