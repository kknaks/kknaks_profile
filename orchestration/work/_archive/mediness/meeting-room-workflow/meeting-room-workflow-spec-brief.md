
# [planner] 스펙 반영 — AX 채팅 예약 승인 → 회의관리 자동 등록 체인

너는 **mediness `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/roles/mediness/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/meeting-room-workflow-spec`
base 브랜치: `origin/mediness` → 최종 PR 대상 `mediness` (PR 은 코디네이터가 올린다)

이 워크트리는 지금 planner 너 혼자다.

## 1. SSOT — 먼저 읽을 것

- `products/mediness/20-spec/spec-151-ax-assistant-reservation.md` ← **개정 대상.** 채팅 발 회의실 예약 승인 게이트의 계약 SoT. **여기 없는 건 발명하지 마라.**
- `products/mediness/20-spec/spec-150-action-runtime-workflow.md` — Action Runtime 워크플로우 공통 계약 (run·전이·감사)
- `products/mediness/20-spec/spec-030-meeting.md` — 회의 도메인 계약
- `products/mediness/30-work/work-099-meeting-v2-create-modal.md` — 모달 발 회의 생성 + 예약(WP-099). 이번 체인의 거울상 — 모달은 「회의 먼저, 예약 나중」, 이번 건은 「예약(승인) 먼저, 회의 나중」
- `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/work/meeting-room-workflow/research-meeting-create-flow.md` — **현행 코드 조사 리포트 (read-only 참조).** 요청 경로·payload shape·트랜잭션 경계·참석자 축이 파일:줄 근거로 정리돼 있다. 코드 사실은 여기서 읽고, 의심되면 아래 §4 의 앱 워크트리에서 직접 확인하라

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

지금 채팅 발 회의실 예약은 승인하면 THE CONNECT 에 방이 잡히는 데서 **끝난다** — 회의관리(`meeting_v2`)에는 아무것도 안 생긴다. 모달 발(회의관리에서 직접 생성)은 반대로 회의를 만들면서 예약까지 하는데, 채팅 발은 예약만 있고 회의가 없어 회의록·참석자·이력이 이어지지 않는다.

이번 작업은 **체인 하나를 잇는다**: 채팅 발 예약 카드가 승인되어 THE CONNECT 예약이 성공하면, 그 payload(제목·일시·참석자)로 `meeting_v2` 를 자동 생성하고 `reservation_run_id` 로 연결한다. 승인 시점 방 자동 배정(SPEC-151 §7.2)은 **이미 현행이므로 건드리지 않는다.** 당초 논의됐던 「시간대별 회의실 점유 스케줄 화면」은 **사용자 결정으로 범위에서 제외**됐다 — 스펙에 쓰지 마라.

## 3. 계약 (사용자 확정 — 재론 금지, 이대로 스펙에 반영)

2026-08-31 사용자 확정 6건:

1. **참석자**: 예약 payload 의 `participants`(이메일)를 `organization_member` 로 역해소해 `meeting_v2_attendee` 를 채운다. 예약 참석자는 현행상 전원 우리 구성원이다 — 역해소 실패 케이스의 처리 방식(생성 실패로 볼지, 제외+표기로 볼지)은 스펙이 정의하되 **기본 가정은 「전원 해소된다」**.
2. **visibility**: 자동 생성 회의는 기본 **`private`(비공개)**.
3. **원자성**: 재시도 없음. THE CONNECT 예약 실행과 회의 생성을 **all-or-nothing 으로 묶는다.** 외부 API 는 DB 트랜잭션에 못 들어가므로, 회의 생성 실패 시 **보상(예약 취소)** 으로 원자성을 만든다 — 그 순서·실패 조합·카드 상태 전이를 스펙이 정의한다 (SPEC-151 §5.3 합법 조합표와 충돌하면 안 된다).
4. **수정·취소 동기화**: 채팅 발 예약의 변경(`MEETING_UPDATE`)·취소(`MEETING_CANCEL`)가 승인·실행되면 연결된 `meeting_v2` 의 일시·참석자·존재도 따라간다. **이번 범위 포함.**
5. **발동 조건**: 체인은 **채팅 발(`source != "meeting_modal"`)에서만** 발동한다. 모달 발은 이미 회의를 먼저 만들므로 발동하면 이중 생성이다.
6. **host**: 예약 requester(`requester_id`/`requester_email`)가 생성될 회의의 host 다.

`product_tags` 는 payload 에 없다 — 빈 배열 기본. 스펙에 그렇게 박아라.

## 4. 먼저 읽을 핵심 파일 (앱 코드 — read-only, 절대경로)

앱 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/meeting-room-workflow` (origin/dev 기준. **수정 금지 — 읽기만**)

- `back/app/services/action_runtime/workflow/meeting/surface.py:215-292` — `start_reservation` (payload 조립·source 축)
- `back/app/services/meeting_v2_service.py:206-257, 312-438` — 모달 발 생성+예약 경로 (거울상·커밋 3회 구조)
- `back/app/services/action_runtime/workflow/meeting/workflow.py:566-599` — 참석자 이름→이메일 해소 (이번엔 역방향이 필요)
- `back/app/models/meeting_v2.py:50-121` — `meeting_v2`·`meeting_v2_attendee`·`reservation_run_id`
- `back/app/clients/the_connect.py:314-368` — create/update/delete 예약 (보상 취소가 쓸 API)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `products/mediness/`
- `context/`

## 6. 구현 단계

1. §1 SSOT 4문서 + 조사 리포트를 읽고, SPEC-151 의 어느 절이 이번 체인의 소유 절인지 판단한다 (§5.3 상태 조합·§7 게이트 원칙과의 접점 포함).
2. SPEC-151 에 「승인 실행 성공 → 회의 자동 등록」 계약을 개정으로 반영한다 — 이 레포의 개정 관례(개정 노트 + 소유 절 본문 수정)를 그대로 따른다. §3 의 사용자 확정 6건이 계약의 뼈대다.
3. 원자성(§3-3)의 실패 조합 전수를 표로 정의한다 — 예약 성공·회의 실패·보상 성공/실패 각 조합에서 카드 상태·원장 기록·사용자에게 보이는 것.
4. 수정·취소 동기화(§3-4)의 계약을 정의한다 — 어느 필드가 따라가고, 회의가 이미 시작(live)·종료(ended)면 어떻게 되는지.
5. 영향받는 타 문서(spec-030 회의 도메인 등)에 필요한 최소 델타가 있으면 함께 반영하되, 새 문서 신설이 필요하다고 판단되면 만들지 말고 먼저 §9 방식으로 물어라.

## 7. 범위 제약 — 하지 말 것

- **코드를 쓰지 마라** — 이번 발주는 스펙 반영까지다. WP(구현 작업서) 작성도 **다음 발주**다 — 만들지 마라.
- 스케줄 테이블/점유 화면 관련 내용을 스펙에 넣지 마라 — 범위에서 제외됐다.
- §3 의 사용자 확정 6건을 재론하지 마라. 확정과 모순되는 사실을 발견하면 고치지 말고 §9 방식으로 물어라.
- 승인 시점 방 배정 로직(SPEC-151 §7.2)·모달 경로(WP-099)의 기존 계약을 바꾸지 마라.
- 앱 워크트리는 read-only 다.

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict  → 이번 변경 범위(mediness) ERROR 0 (타 제품 기존 WARN/ERROR 는 "무관"으로 분리 보고). 검증은 1회만
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
  --to term_e8a1a258-210f-466b-8b05-c43a7ec8a7ad --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_e8a1a258-210f-466b-8b05-c43a7ec8a7ad \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_e8a1a258-210f-466b-8b05-c43a7ec8a7ad --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
