
# [backend] WP-125 착지 — 예약 승인 실행 성공 → 회의 자동 등록 체인 (P0~P5)

너는 **mediness `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/roles/mediness/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/meeting-room-workflow`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

이 워크트리는 지금 backend 너 혼자다 (이전 조사 태스크와 같은 워크트리 — read-only 조사만 했으므로 깨끗하다).

## 1. SSOT — 먼저 읽을 것 (spec 레포 워크트리 절대경로 — read-only, 절대 수정 금지)

- `/Users/kknaks/orca/workspaces/mediness-mediness/meeting-room-workflow-spec/products/mediness/30-work/work-125-reservation-meeting-autoregister.md` ← **작업의 SoT. P0~P5 를 이대로 착지한다. 여기 없는 건 발명하지 마라.**
- `/Users/kknaks/orca/workspaces/mediness-mediness/meeting-room-workflow-spec/products/mediness/20-spec/spec-151-ax-assistant-reservation.md` §7.9 — 계약 (조합표·파생 매핑·동기화·경계)
- `/Users/kknaks/orca/workspaces/mediness-mediness/meeting-room-workflow-spec/products/mediness/20-spec/spec-031-meeting-v2-diarization.md` §3 역방향 가산 — 회의 쪽 처분 정의
- `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/work/meeting-room-workflow/research-meeting-create-flow.md` — 현행 코드 조사(파일:줄)

위 스펙 문서들은 spec 레포 브랜치(PR #665, 미머지)에 있다 — 네 워크트리 base(origin/dev)에는 없으니 **반드시 위 절대경로로 읽어라.**

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

채팅 발 회의실 예약은 승인·실행되면 THE CONNECT 에 방이 잡히는 데서 끝나고 `meeting_v2` 에는 아무것도 안 생긴다. WP-125 는 그 체인을 잇는다: 외부 예약 생성 성공 직후(모달 발 제외) 승인된 plan 에서 회의를 파생해 저장하고 `reservation_run_id` 로 연결하며, 실패하면 보상(예약 취소)으로 되돌린다. 예약의 수정·취소는 **자동 등록된 회의에 한해** 파급된다(변경→예정 일시, 취소→대기 회의 soft delete·live/ended 는 연결만 끊음).

## 3. 계약 — WP-125 가 전부다. 특히 어기기 쉬운 것:

- **P0 실사 3건을 먼저 끝내고 P1 로 가라.** P0-②에서 §7.2 문면과 코드가 어긋나면 **코드에서 정하지 말고** §9 방식으로 보고하라(SPEC 환류 선행).
- 발동·파급 판정은 **같은 source 축 하나** — 정의를 두 자리에 만들지 마라. P3 진입 가드는 2겹(연결 + source).
- 실행 축 기록은 **체인이 끝난 뒤** — 외부 예약 성공 시점에 «성공» 을 적지 않는다.
- 보상은 bound tool(room.cancel) 경유 — gateway 직접 호출 금지. 보상 대상은 방금 만든 그 예약 하나(외부 식별자), 조건 재조회로 지우지 마라.
- 새 endpoint·leaf·state enum 값·카드 명령·DELETE 표면 신설 0. **모달 발 경로 diff 0.**
- migration 은 P0-③ 결과에 따라 0 또는 인덱스 1건.

## 4. 먼저 읽을 핵심 파일

- `back/app/services/action_runtime/workflow/meeting/definitions.py` — `_execute_reserve`·`_execute_cancel`·`_execute_update` 3 훅 (착지 자리)
- `back/app/services/action_runtime/workflow/meeting/surface.py` · `workflow.py` — source 축·resolve 술어
- `back/app/services/meeting_v2_service.py` · `back/app/repositories/meeting_v2_repo.py` — 회의 저장·연결 (모달 발 함수는 무변경, 예약 발 진입 seam 신설)
- `back/app/models/meeting_v2.py` — `reservation_run_id`·`deleted_at`
- `back/app/clients/the_connect.py` — cancel (보상)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `back/`
- `mcp/`
- `docker-compose.yml`
- `docker-compose.local.yml`

## 6. 구현 단계

1. WP-125 P0 착수 실사 3건 — 결과를 완료 보고에 실어라 (②가 어긋나면 즉시 질문).
2. P1 체인 발동·역해소·회의 저장(한 트랜잭션) → P2 보상 원자성 → P3 수정·취소 파급(가드 2겹) → P4 표면(카드 facts·채팅 안내 — FE 몫 발생 여부 판정해 보고).
3. P5 테스트 — 조합표 A~D·동기화 분기 전수(모달 발 무파급 음성 단언 포함)·멱등 재진입·source 게이트·역해소 경계. **네가 만든 테스트 파일만 돌린다.**

## 7. 범위 제약 — 하지 말 것

- WP-125 비목표 전부: 모달 발 경로 수정·스케줄 화면·보상 실패 상시 탐지(OQ-9)·회의→예약 반대 방향·새 표면 일체.
- spec 레포 워크트리 수정 금지 (read-only 참조).
- 커밋·push·PR 금지 — 워크트리에 변경만 남긴다.

## 8. 검증

```
cd back && pytest -q <네가 만들거나 고친 테스트 파일만> (전체 스위트 금지 — 사용자 방침. DATABASE_URL 은 back/pyproject.toml 의 테스트 DB = localhost:25434/mediness_test). 검증은 1회만 — 통과하면 반복하지 마라
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
  --to term_ae5c9156-a854-48b7-8f65-528976906150 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_ae5c9156-a854-48b7-8f65-528976906150 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ae5c9156-a854-48b7-8f65-528976906150 --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
