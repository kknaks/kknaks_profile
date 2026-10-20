# [backend] WP4-BE — 예약관리 데모 API (SPEC-002 §3.1 · §3.2)

너는 **cc-prototype `backend` 워커**다. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/orchestration/roles/cc-prototype/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/cc-nav-resv`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

⚠ 같은 워크트리에서 frontend 워커가 `cc/front/` 를 작업 중이다 — `cc/front/` 는 건드리지 마라. `cc/back/data/` · `cc/back/.env` 는 코디가 로컬 확인용으로 넣어 둔 것(gitignore) — 지우거나 고치지 마라.

## 1. SSOT

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/para/projects/summer-star/cc-prototype/20-spec/spec-002-cc-nav-reservation.md` (0.2.0) ← 계약의 SoT. **여기 없는 건 발명하지 마라.**
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/para/projects/summer-star/cc-prototype/10-decision/decision-004-cc-nav-reservation.md` — 특히 **D-21 기존 디자인 무변경**
- **§3.1 모델 · §3.2 API** 가 계약. §3.3 화면은 front 몫이지만 읽어 두어라
- 화면 정본(값 · 문구 참고): `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/orchestration/work/cc-nav-resv/design-upload/Ceramique 예약관리 v1.dc.html` · 해설 `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/orchestration/work/cc-nav-resv/design-report.md` §A
- 1차 계약: `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/para/projects/summer-star/cc-prototype/20-spec/spec-001-cc-poc.md` §5 · §9(KOS 주석 형식)

## 2. 배경

예약관리는 데모다. Linky 가 보낼 예약 요청 · 수정 요청을 데모 버튼이 대신 만들고, 병원이 KOS 등록 · 변경 요청을 누르면 상태가 바뀐다. KOS 는 호출하지 않고 `kos api 연동 필요` 주석만 남긴다. 상태는 1차와 같은 관제 DB 에 둔다.

## 3. 계약 — front 워커가 이대로 쓴다

SPEC-002 §3.2 표 그대로. 응답 JSON 키는 §3.1 필드 이름(camelCase) 그대로. 추가:
- `GET /api/reservations` 응답 = `{ rows: ResvRequest[], counts: { needCheck, changeRequested, confirmed, total }, version }` — `rows` 는 묶음(`groupId`) 단위로 최신 묶음이 위, 묶음 안은 오래된 줄이 위
- `customer` 가짜 풀 = 시안 샘플 3명(LIN YA CHEN · TANAKA YUKI · CHAN MEI LING) 값 그대로 + 필요하면 같은 형식 가짜 몇 명. 다 쓰면 처음부터 돌린다. **실제 고객 값 금지**
- `demo/modify` 의 새 시간: 시안처럼 이전 시간에서 바꾼 값(예 10:00 → 14:30). 규칙은 단순하게, 리포트에 적어라
- `snapshot` = 시안 스크린샷 모달 칸 값(가짜 chart · birth · phone 포함). 예약 메모(자동 작성) 문구는 시안 그대로의 형식

## 4. 먼저 읽을 핵심 파일

- `cc/back/app/api/desk.py` · `app/api/admin.py` · `app/api/events.py` — 라우터 · reset · SSE
- `cc/back/app/repository/db.py` · `state_repo.py` — 테이블 · version
- `cc/back/app/service/board_service.py` · `app/domain/errors.py` — 서비스 · 도메인 예외 → HTTP 오류 형식
- `cc/back/app/container.py` · `app/main.py` — 조립 · 라우터 등록
- 계층 규약: router → service → repository, ORM/SQL 은 repository 밖으로 안 나간다, 아래층은 HTTP 를 모른다(도메인 예외만)

## 5. allowed_paths

- `cc/back/` (`data/` · `.env` 제외)

## 6. 구현 단계

1. 테이블 · repository · service · router(`/api/reservations`) — §3.2 네 경로 + GET
2. 상태 전이 규칙을 service 에 한 곳으로. 맞지 않는 전이 = 도메인 예외 → 409, 빈 사유 = 400
3. 조작 성공 → 1차와 같은 방식으로 version 올리고 SSE 알림
4. `POST /api/admin/reset` 에 예약 줄 비우기 추가
5. register 자리에 `kos api 연동 필요` 주석(SPEC-001 §9 형식 — 등록 = 예약 생성, 수정 = 예약 변경, 「공개 없음 — KOS 요청」 여부는 1차 HAR 리포트 범위에서 아는 만큼)
6. 테스트: 전이 전부(요청 → 등록 → 확정 / 요청 → 변경 요청 → 수정 요청 → 수정 등록 → 이전 줄 superseded / 확정 → 수정 요청 → 수정 확정) · 409 · 400 · reset

## 7. 하지 말 것

- `cc/front/` · KOS 호출 · 1차 API 동작 변경
- 사용자 포트 · 프로세스. 코디가 8610 에 띄워 둔 back 도 건드리지 마라(테스트는 pytest 로)

## 8. 검증

```
cc/back 에서 uv run pytest · uv run ruff check . — Phase 범위에 맞게 1회씩, 통과하면 반복하지 마라. 기능 폴더 밖 import 가 없는지 확인. 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending 으로 보고
```

- 보고에: 응답 JSON 예시(GET 한 번 · 각 조작 한 번) — front 워커에게 그대로 넘긴다

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_adf432d6-a97d-4457-a02d-041df0075fb7 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend(WP4) 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_adf432d6-a97d-4457-a02d-041df0075fb7 \
  --text "[worker_done] backend(WP4) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_adf432d6-a97d-4457-a02d-041df0075fb7 --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
