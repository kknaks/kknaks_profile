# planner-delivery229-v2 결과 보고 — done (승인 안 함)

- [CENTURION_DAY#229](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/229) 같은 Issue 갱신(apply `issue_number 229` · key `day/v2-web-kit` · `contract_version=2` · status `scope-delta-recorded`). 라벨 `delivery-plan:review` · `execution-plan:ready` · `spec-baseline:pending` 그대로 · human gate.
- **plan_digest v2 = `sha256:f2711e403e756d0dba312720fa76d0fccb51a5b02a406ba132730839a567435e`** (v1 `sha256:6847d991…` stale).
- 파일: `delivery/v2-web-kit.json`(v1 사본 `v2-web-kit.v1.json`) · `v2-web-kit.v2.plan.json` · `v2-web-kit.v2.apply.json`. mediness 워크트리 파일 수정 없음.

## 바뀐 항목 (v1 → v2)

| W | 항목 | 바뀐 것 |
|---|---|---|
| W1 | Target Delta 매크로 목록 | + E06 검색 28h · E09 정사각 아이콘 버튼 · E25 지우기 X · E27 빈 상태 · E44 24h 줄 버튼 · E55 차트 모달(읽기) · E56 글 칸(기존 매크로 크기 · 변형 허용) |
| W1 · W6 | A4 | 대응표 = SPEC-002 화면 구성 1차 「넣음」 요소 전부 → 매크로 또는 조합 · 칸 「매크로 · E · G · **그린 상태**」 · 「안 만듦」 = E33 방 이름 버튼 · E47 · E48 · **E49** · E53 · E54 방 옮기기 쓰임 |
| W2 (코디) | Target Delta 새 줄 · A9 · phase 7 · 의존 | CSRF 연결 = **마지막 phase** — #227 이 PR #228 에 들어온 뒤 base.html 한 곳에서 `login_session.csrf_token` 을 `hx-headers` 로 · A9: 견본 HTMX POST 통과 · 토큰 빼면 403 `csrf_failed` · 의존 #227 은 「마지막 phase 만」 |
| W3 (코디) | Target Delta 2 · A6 · code_surface | htmx SSE 확장(sse.js) 벤더링 + 라이선스 |
| W4 | Target Delta 5 · Review Surface · open_questions | 빌드 방식 = 레포 AGENTS.md(styles/ tailwind preset · build.mjs · 빌드된 CSS 커밋)로 닫음 · 「빌드 방식 충돌」 줄 → 「AGENTS.md 로 닫음」 · open_questions 비움 |
| W4 · W5 | A2 | + tailwind 임의값 클래스(`[...]`) 금지 · 새 값은 DAY 토큰 파일(styles/)에만 |
| W5 | A3 · verification | + `hx-on` / `hx-on:*` 금지 |

위험 L2 · target DAY-SPEC-002 · baseline pending 은 그대로.

## 주의

- Review Surface 첫 줄이 아직 「SPEC-002 는 PR #909 워크트리에 **미커밋** draft」(v1 문구)다 — 지금은 `3c14633b` 에 커밋됨(PR #909 미머지라 pending 은 맞음). 다음 v3(baseline 재결속) 때 고친다 — 이번엔 지시 범위 밖이라 digest 를 한 번 더 바꾸지 않았다.
- `gh issue list --search "day/v2-web-kit"` 는 #231 도 잡는다(#231 의존 줄에 key 문자열이 있음) — idempotency 마커는 #229 하나뿐.
