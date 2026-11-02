# [backend] WP-132 태스크 Slack 알림 — 배정 DM 전면화 + 데일리 리포트 (BE 단독)

너는 **mediness `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/roles/mediness/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/task-slack-notify`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

워크트리 공유 없음 — BE 단독 WP 다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/mediness-mediness/task-slack-notify-spec/products/mediness/20-spec/spec-120-task-slack-notify.md` ← **계약의 SoT. 여기 없는 건 발명하지 마라.**
- `/Users/kknaks/orca/workspaces/mediness-mediness/task-slack-notify-spec/products/mediness/30-work/work-132-task-slack-notify.md` ← 빌드 계획(P1·P2·검증·한계)

**기대는 개념** — 이 작업이 따를 판단 기준:

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/para/areas/concept/cs/contract-surface-enumeration.md` — 발송 판정을 소비처마다 흩뿌리지 말고 생성 seam 한 곳에 두라는 근거. 입구 6곳(SPEC-120 §2.2)이 전부 그 seam 을 지나는지 코드로 확인하고 시작하라
- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/para/areas/concept/db/derived-predicate.md` — 요청 판정(`is_request_task`)은 파생 술어 정본이다. **한 글자도 바꾸지 마라** — 문구 분기에서 읽기만 한다

## 2. 배경 / 무엇을 바꾸나

지금 태스크 배정 DM 은 업무 요청(수동·채팅, 생성자≠담당자)에만 간다 — `notify_task_requested` 가 `manual_surface.py`·`task_draft/definitions.py` 두 호출부에 걸려 있다. 워크플로(의사결정 실행·인시던트 fanout·WBS 연동 등)가 배정한 태스크는 담당자가 보드를 열기 전까지 모른다. 그리고 개인별 하루 태스크 흐름(생성/진행/완료·마감 유무)을 공용으로 보는 자리가 없다.

이 WP 는 ① DM 발송 조건을 「담당자 존재 ∧ 생성 행위자 ≠ 담당자」로 넓혀 생성 seam 한 곳에서 판정하고 ② 매일 09:00 KST 데일리 리포트를 슬랙 채널 스레드로 발송한다. **BE 단독 · FE 0 · 마이그레이션 0.**

## 3. 계약 (합의됨 — 이대로)

- DM 발송 조건·문구 2종·graceful 규율: SPEC-120 §2 그대로. 같은 태스크 DM **최대 1통** — 기존 요청 DM 호출을 seam 판정으로 **대체**한다(이중 발송 금지).
- 데일리 리포트 5칸·창·형식: SPEC-120 §3 그대로. 채널은 **설정 키(채널 ID)** 신설, 비면 no-op(로그만). 코드에 채널 ID 하드코딩 금지.
- 시드: `back/app/seeds/decision_slack_ids.py` 의 `SLACK_ID_BY_NAME` 에 5명 추가 — 구지윤 `U0BL1NLCR6G` · 최원 `U0AD7V7E88Z` · 김사라 `U08FG90A6H1` · 박신아 `U08D3L8FSLE` · 원영진 `U08LXUY6FGD` (prod 는 2026-09-02 백필 완료 — 시드는 정본 동기화다. NULL-only 멱등 구조 유지)

## 4. 먼저 읽을 핵심 파일

- `back/app/services/action_runtime/tasks/request_axis.py` — 기존 요청 DM(`notify_task_requested`)·문구·딥링크·graceful 규율. 여기 규율을 승계해 일반화한다
- `back/app/services/action_runtime/tasks/factory.py:109` — `RuntimeTask` 생성과 `create_task_with_cc` — 발송 판정이 수렴할 생성 seam
- `back/app/services/action_runtime/tasks/manual_surface.py:253` · `back/app/services/action_runtime/workflow/task_draft/definitions.py:152` — 현행 호출부 2곳(대체 대상)
- `back/app/services/weekly_report_scheduler.py` — 스케줄러 job 배선 패턴 정본(동형으로 만들 것) + `back/app/main.py:62-74` register 자리
- `back/app/services/slack_bot_client.py` — `chat_post_message(thread_ts=…)`·`post_dm` (새 클라이언트 만들지 마라)
- `back/app/models/action_runtime.py:628,685-686` — `due`·`started_at`·`completed_at` (있는 컬럼만 쓴다)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `back/`
- `mcp/`
- `docker-compose.yml`
- `docker-compose.local.yml`

## 6. 구현 단계

1. **P0 표면 확인**: SPEC-120 §2.2 의 입구 6곳이 실제로 전부 공용 생성 seam 을 지나는지 grep 으로 확인. 안 지나는 입구가 있으면 **구현 전에 코디네이터에게 보고**(브리프 §9 채널) — 임의로 범위를 넓히지 마라.
2. **P1 DM 전면화**: 발송 판정을 생성 seam 쪽 한 곳으로 수렴(기존 2 호출부는 제거 또는 그 판정으로 위임). 문구 2종(요청 갈래는 기존 문구·항목 **불변**). 시드 5명 추가.
3. **P2 데일리 리포트**: 스케줄러 job(매일 09:00 KST, `weekly_report_scheduler` 동형) + 집계 쿼리(담당자 축 · KST 전날 창 · 열린 스냅샷 due 유무 · 삭제 제외) + 채널 본문 1건 → 개인별 스레드 댓글(이름순 · 멘션 없음 · 활동 0 ∧ 열린 0 생략 · 부분 실패 허용) + 설정 키.
4. **테스트 작성**: WP-132 §검증의 3묶음 — DM 조건 / 집계 경계 / 리포트 조립.
5. MCP 툴 설명 정합 1건: `mcp/app/tools/task_comment.py` 등 태스크 툴 설명에 「담당자 본인 고정」류 낡은 문구가 남았는지 grep — 이번 계약과 어긋나는 문구만 고친다(새 툴 만들지 마라).

## 7. 범위 제약 — 하지 말 것

- 새 컬럼·migration·새 TaskEvent·새 알림 종·발송 원장·새 스케줄 인프라 금지 (SPEC-120 「만들지 않는 것」)
- `is_request_task`·`request_predicate` 수정 금지 — 읽기만
- FE(`front/`) 금지 — BE 단독 WP
- 채널 ID·토큰 하드코딩 금지 — 설정 키만 신설
- **커밋·push·PR 금지** — 워크트리에 변경만 남긴다
- 리포트 발송의 실 슬랙 호출은 테스트에서 mock — 실채널로 쏘지 마라

## 8. 검증

```
cd back && pytest -q <네가 만들거나 고친 테스트 파일만> (전체 스위트 금지 — 사용자 방침. DATABASE_URL 은 back/pyproject.toml 의 테스트 DB = localhost:25434/mediness_test). 검증은 1회만 — 통과하면 반복하지 마라
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다. preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: WP-132 태스크 Slack 알림" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 \
  --text "[worker_done] backend 완료 — WP-132 태스크 Slack 알림. 상세는 인박스." --enter
```
