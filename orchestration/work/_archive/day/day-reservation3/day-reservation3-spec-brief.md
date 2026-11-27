# [planner] DAY-SPEC-008 예약 요청 스레드(ext 요청 API · 현황판 「예약 요청」 · 상세 창) 새로 쓰기 + SPEC-006 · 005 · 007 · 000 맞춤 개정

너는 **day `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/orchestration/roles/day/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation3-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**너는 앞 맥락이 없다.** 이 브리프와 아래 파일이 전부다. 이 spec 워크트리는 너 혼자 쓴다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/reference/2026-11-26-reservation-request/reservation-request-decisions.md` ← **사용자 결정 RQ1 ~ RQ44. 계약의 SoT. 다시 열지 마라. 여기 없는 정책은 발명하지 마라.** 끝의 「열린 것」은 OQ 로
- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/orchestration/work/day-reservation3/design/20261126_예약현황_시연_v15.html` ← 시안 v15(한 파일 · base64 이미지). **생김새 · 문구 정본**(결정과 다르면 결정이 이긴다 — 「시안과 다른 곳」 표). 읽기 쉬운 사본: `sed -E 's#data:[a-z/+.-]+;base64,[A-Za-z0-9+/=]+#DATA#g'` 로 `/private/tmp/` 아래에 빼서 grep. 바뀐 자리 이력 = 같은 폴더 `../design-1-report.md` ~ `../design-6-report.md`(「지은 문구」 목록 = 임시 문구) · 스크린샷 `design/v15-first.png` · `v15-return.png` · `v15-done.png`
- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/orchestration/work/day-reservation3/ext-request-body-draft.md` ← 링키 요청 본문 초안(칸 이름 · 예시 — **이름은 제안**, 정책은 RQ)
- KOS 실물 근거(새로 지어내지 마라): `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/orchestration/work/_archive/day/day-reservation2/be-probe-1-report.md` ~ `be-probe-4-report.md` — 특히 be-probe-2 §6 **상담사 = `update-reservation {scheduleId, counselor{id,name}}` → `reservation.counselor`(다른 칸 안 지움)** = RQ27 「당일 지정 상담사」. `reserve` 본문에 바로 넣을 수 있는지는 실물 없음 → OQ(구현 때 실물 확인 · 안 되면 reserve 뒤 update-reservation 순서 묶음)

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

지금 링키(외부 예약 대행)는 카톡으로 예약 요청을 보내고 지점이 손으로 KOS 에 넣는다. DAY 예약 현황(SPEC-006) 오른쪽 「예약 요청」 칸은 제목만 있다(R32). 이번에 **링키가 ext API 로 완성된 예약 요청을 보내고 → 병원은 스레드(버전 · 댓글)로 주고받다가 → [예약 생성] 한 번으로 DAY · KOS 에 예약을 만든다.** 수정 · 취소도 링키가 같은 스레드에 새 버전으로 올린다. 범위 = 고객 → 링키 → 병원 요청 흐름만(RQ2).

DAY 의 ext API 는 mediness 스펙 문서가 없다(코드만 — `backend/day/routers/api/ext.py` 등 · 다른 개발자가 만든 것). 이번 SPEC 은 **새 ext 경로 · ext 키 범위 변경(RQ7)** 을 정하는 첫 문서이고, 기존 ext 경로는 인용만 한다.

산출물:
1. **새 SPEC `products/day/20-spec/spec-008-reservation-request.md`**(이름 제안 · 「예약 요청 스레드 (ext · 웹)」) — SPEC-007 모양(frontmatter · 결정 원천 인용 · 화면 구성 요소 번호 · UX Contract · 상태 전이 표 · API(ext 새 경로 · 웹 경로 — 이름 제안) · 데이터(새 표 · 칸) · KOS 쓰기 표 · 알림 · 케이스 매트릭스 · 시안과 다른 곳 · 기획안과 다른 곳 · OQ). 꼭 들어갈 것:
   - ext 경로 전부: 요청 만들기 · 새 버전 · 철회(RQ31) · 목록(전체 · `updated_since`) · 상세 · 링키 댓글 쓰기(`message`) · 예약 그룹 목록 · 유입 채널 목록 — 본문 · 응답 · 오류 코드(기존 ext 오류 모양 `ExtErrorResponse` 따름) · `Idempotency-Key`
   - ext 키 = 병원당 하나(RQ7) — `PartnerGrant.partner` 를 쓰는 곳 전수(아래 §4 grep) · 바뀌는 것 · 하위 호환(배포 때 env 바꿈) · 「누가」 헤더
   - 상태 전이(스레드: 요청됨 · 확정 · 취소됨 · 닫힘 / 버전 · `change_request`: 답변 대기 · 대체됨 · 철회) × 이벤트(새 요청 · 새 버전 · 변경 요청 · 철회 · 생성 · 수정 · 취소 · 링키 철회 · 희망 일시 지남)
   - 초진 · 재진 판정(RQ24 · RQ25) · 2명 이상이면 생성 막기
   - KOS 쓰기(RQ27 · RQ28): 버튼별 순서 묶음(새 고객 → reserve → (상담사) / update / cancel) · 메모 합치기 형식 · 1000자 · 실패 처리 = SPEC-007 쓰기 큐 · 확인 규칙 그대로 · `reservation_applied` 는 **KOS 반영 확인 뒤** 남김
   - 웹 화면: 오른쪽 「예약 요청」 목록 · 상세 창(1 · 2 · 3열 — RQ42) · 버튼 숨김 규칙(RQ35) · 제목 배지(RQ43) · 2열 시간 머리 고르기(RQ33) · 댓글 입력 막기(RQ37) · 권한(RQ41)
   - 알림(RQ39): 새 종류 · 받는 사람 · 누르면 스레드 열림
2. **SPEC-006 개정**: R32 「예약 요청 칸 = 제목만」 → SPEC-008 목록(RV-38) · 「예약 요청」 배지(R3) 등 관련 행
3. **SPEC-005 개정**: 알림 새 종류(웹 알림만 · 앱 푸시 없음 · 받는 사람 `ADMIN` · `COORDINATOR`)
4. **SPEC-007 개정**: KOS 예약 쓰기에 지정 상담사(`reservation.counselor`) · 유입 · 메모 합치기 — 웹 예약 등록 동작은 바꾸지 않음(SPEC-008 이 같은 쓰기 경로를 쓰는 것만)
5. **SPEC-000 개정**: 새 표 · 칸(스레드 · 버전 · 댓글 · 제안 일시 · 상태 · 링키 본문 칸별 · 판정 결과 · 만들어진 visit 연결) — 이름 제안 · 기존 표 관례
6. `20-spec.md`(Scope · SPEC Bundle) · `10-decision.md` · `log.md`. **30-work(WORK)는 이번에 쓰지 않는다** — SPEC 검수 통과 뒤 따로

## 3. 계약

다른 워커와 합의된 계약 없음(문서 단계). 경로 · 칸 · 키 이름은 「이름 제안」. KOS 경로 · 본문 · 확인 조건은 be-probe 리포트와 코드(`emr/kos/writes.py`) 그대로.

## 4. 먼저 읽을 핵심 파일

문서(이 워크트리): `products/day/20-spec/spec-006-reservation-board.md`(R3 · R14 · R32 · RV-38) · `spec-007-reservation-detail.md`(예약 등록 · KOS 쓰기 W2 ~ W5 · 쓰기 큐 · 확인) · `spec-005-notifications.md`(웹 원장 호출 알림 U-5) · `spec-000-data-model.md` · `20-spec.md` · `10-decision.md` · `log.md` · 기획안 `00-baseline/planning/` 안 예약 요청함 문서가 있으면 「기획안과 다른 곳」용으로만(고치지 마라)

코드(read-only · `git -C /Users/kknaks/git/CENTURION_DAY show origin/dev:<path>` · `git fetch` 하지 마라 — 지금 `origin/dev` 그대로): `AGENTS.md` · ext 전부 `backend/day/routers/api/ext.py` · `schemas/ext*.py` · `services/ext_*.py` · `models/ext.py` · `emr/ext_commands.py`(PartnerGrant · 한도 · outbox) — **`partner` 를 쓰는 곳은 `git -C … grep -n partner origin/dev -- backend` 로 전수** · `services/reservation_book.py`(`book()` 입력 · 같은 고객) · `dtos/emr_writes.py` · `emr/kos/writes.py`(:259 `_resource_body` · `plan_reservation`) · `enums/notification.py` · `static/day.js`(:4403 웹 알림) · `models/visit.py` · `models/customer.py` · `routers/reservations.py` · `templates/partials/reservations_*.html`

## 5. allowed_paths — 이 밖은 건드리지 마라

- `products/day/`

## 6. 구현 단계

1. RQ1 ~ RQ44 를 화면 요소 · 동작 · API 별로 묶는다. SPEC 문장마다 RQ 번호
2. 시안 v15 의 「예약 요청」 목록 · 상세 창(1 · 2 · 3열) · 알림 요소 · 문구를 전수로 뽑아 **넣음 / 뺌 / 바뀜(RQ 번호)** 표. 시안의 시연 장치(투어 · 시연 버튼)는 뺌
3. 상태 전이 표 · 케이스 매트릭스(결정 · 시안 · 실물에 없는 경우는 OQ)
4. ext API 표 · 데이터 표 · KOS 쓰기 표 · 알림 표
5. SPEC-006 · 005 · 007 · 000 개정(개정 번호 · 이력은 각 문서 관례)
6. `20-spec.md` · `10-decision.md` · `log.md`
7. §8 검증

## 7. 범위 제약 — 하지 말 것

- **화면 문구를 지어 넣지 않는다.** 시안에 있는 문구만 · 시안 리포트 「지은 문구」는 「임시(기획 확인)」 표시 · 결정 때문에 새로 필요한 문구(예: 「링키 답 기다림」)는 비우고 OQ
- 결정 RQ 를 다시 열지 않는다. 어긋나 보이면 OQ 로 적고 코디에게 묻는다(아래 질문 명령)
- 범위 밖(Out Of Scope): 앱(푸시 · 화면) · 근무 데이터 · 예약 생긴 뒤 생애(내원 · 노쇼) · 현황판 예약 카드 → 스레드 입구 · 후보 고르는 화면 · 웹 예약 등록 동작 변경 · 기존 ext 경로 동작 변경(키 범위 RQ7 빼고)
- 기획안 · 다른 제품 폴더를 고치지 않는다
- 시안 · DB 의 실제 고객 이름 · 전화 · id 를 예시로 옮기지 않는다(시안의 재진 고객은 실제 사람 — 예시는 지어낸 값)
- 비밀값(ext 키 · 비밀번호)을 문서에 쓰지 않는다

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict → products/day/ 범위 ERROR 0 (타 제품 기존 WARN/ERROR 는 '무관'으로 분리 보고). 근거 없는 정책 0 · 열린 것은 열린 것으로
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 보고 본문에 RQ1 ~ RQ44 중 SPEC 에 반영 안 된 번호(있으면 이유)를 적어라.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_5c196973-a9ec-4982-81c2-655361f18aec --from term_22be6ba1-9b24-4e82-90bf-4e7b6b4d9182 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_5c196973-a9ec-4982-81c2-655361f18aec \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_5c196973-a9ec-4982-81c2-655361f18aec --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
