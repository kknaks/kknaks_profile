
# [frontend · 기능 1] 예약 등록 창 · 예약 상세 모달 · 우클릭 메뉴 · 시술 목록 · 예약 현황 SSE 화면

너는 **day `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/orchestration/roles/day/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation2`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

⚠ **backend 워커가 같은 워크트리에서 동시에 작업 중**(`backend/day/emr/` · `dtos/` · `services/` · `routers/api/` · `migrations/` · 그 테스트). 그쪽 파일은 건드리지 마라. 너는 화면 라우터 · 템플릿 · static · styles · 화면 테스트만.

## 1. SSOT

- **SPEC-007**: `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation2-spec/products/day/20-spec/spec-007-reservation-detail.md` — §2 화면 구성(요소 번호) · 시안 요소 전수(넣음 / 뺌 / 바뀜) · UX Contract · 단계 × 날짜 경계 표 · §3 API 계약 · 화면이 읽는 칸 · 실시간 갱신(D52) · 시안과 다른 곳. **지금 판 그대로 구현**(검수 2차 중 — 바뀌면 고침으로 줌)
- SPEC-006 개정 ⑫(카드 클릭 = 상세 · 빈 칸 [+] = 등록 · 우클릭 · 끌어 묶기 없앰 · 옮기기 모드 · R41 폴링 → SSE)
- **시안(생김새 · 문구 정본)**: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/reference/2026-11-23-reservation/20261124_예약현황_시연.html`(v9 · 4MB · base64 빼고 grep): `openBook`(예약 등록) · `detailV6Html`(예약 상세) · `s5Pop`(확인 창) · `renderCtx`(우클릭) · 옮기기 끌기. **시술 목록은 시안이 아니라 결정 파일의 와이어**
- 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/reference/2026-11-24-reservation-detail/reservation-detail-decisions.md`(D1 ~ D54 · 「시술 목록 와이어」 절)
- 기존 화면: `backend/day/templates/reservations.html` · `partials/reservations_*.html` · `board.html`(SSE 본) · `static/day.js` · 레포 `AGENTS.md`(화면 = Jinja2 + HTMX + 바닐라 JS · 메디킷 부품)

## 2. 할 일 (frontend 몫 전부)

1. 예약 등록 창(기존 / 새 고객 · 같은 고객 제시 · 필수 칸 · 미리보기 카드 · [저장 후 예약 등록])
2. 예약 상세 모달: 머리(단계 이름 · 색) · 고객 정보 · 예약 정보(동행 체크 · 의사 지정) · 상담 정보 / 시술 정보(「시술만 진행」) · 오른쪽 시술 목록(와이어: 오늘 = 파란 ✓ · 상태 「시술 전」「시술 중」「시술 후」「미진행」 · n/m회 오른쪽 끝) · 수납 정보 · 이전 방문(재진 · 접기) · 단계별 아래 버튼 · 확인 창(시안 문구만) · [문진 QR] · [여권 스캔] 비활성 자리 · 딥링크 2(새 창)
3. 카드 우클릭 메뉴(예약 변경 = 옮기기 모드 점선 · 끌어 놓기 · 예약 취소 확인 창 · 동행 추가) · **카드 위 끌어 놓아 묶기 제거**
4. 예약 현황 SSE 연결(`/reservations/stream` · 시술 현황 `board.html` · `day.js` 방식) — 10초 조각 폴링 대체 · 쓰기 결과 전 버튼 잠금 · 실패 = 공용 토스트 + 「다시 시도」
5. 화면 테스트(TestClient — 전체 페이지 · 조각 렌더 · 단계별 버튼 유무)

## 3. 계약 (backend 와)

SPEC-007 §3 API 계약 · 화면이 읽는 칸 · 실시간 갱신이 계약. 조각에 넘길 값 이름이 SPEC 에 없으면 backend 와 `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/orchestration/work/day-reservation2/contract-v1.md` 에 먼저 적어 맞춰라(없으면 만들어라 · 둘 다 쓴다). backend 서비스가 아직 없을 때는 계약 모양 그대로의 가짜 값으로 화면 테스트를 짜라.

## 5. allowed_paths

- `backend/day/routers/`(api/ 제외) · `backend/day/templates/` · `backend/day/static/` · `backend/day/styles/` · `backend/tests/day/web/` · 위 `contract-v1.md`

## 7. 하지 말 것

- **화면 문구를 지어 넣지 않는다** — 시안 · 결정 · SPEC 에 있는 글자만(없으면 비움)
- 인라인 스크립트 · 손 CSS 금지(메디킷 · 기존 클래스) · backend 몫 파일 수정 · 커밋 · push · 로컬 스택 · 사용자 포트

## 8. 검증

```
uv run pytest -q <네가 만든 화면 테스트만>(TestClient 로 전체 페이지 · HX 조각 렌더 확인) — 1회. CSS 를 다시 빌드했다면 빌드 명령 1회. 인라인 스크립트 0 · 손 CSS 0(grep). 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_cd5ea51a-31a7-4f34-9cf7-ec53af90a280 --from term_9e29e1a2-3f76-45d9-9965-54b71d752552 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_cd5ea51a-31a7-4f34-9cf7-ec53af90a280 \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_cd5ea51a-31a7-4f34-9cf7-ec53af90a280 --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
