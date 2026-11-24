
# [planner] DAY-SPEC-007 예약 등록 · 예약 상세(웹 · 쓰기) 새로 쓰기 + SPEC-006 · 002 · 000 맞춤 개정

너는 **day `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/orchestration/roles/day/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation2-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**너는 앞 맥락이 없다.** 이 브리프와 아래 파일이 전부다. 이 spec 워크트리는 너 혼자 쓴다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/reference/2026-11-24-reservation-detail/reservation-detail-decisions.md` ← **사용자 결정 D1 ~ D48 + 시술 목록 와이어. 계약의 SoT. 다시 열지 마라. 아래 행이 위 행을 덮는다(취소선 = 뒤집힘). 여기 없는 정책은 발명하지 마라.**
- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/reference/2026-11-23-reservation/20261124_예약현황_시연.html` ← 시안 v9(4MB 한 파일 · base64 이미지). **생김새 · 문구 정본.** 읽기 쉬운 사본: `sed -E 's#data:[a-z/+.-]+;base64,[A-Za-z0-9+/=]+#DATA#g'` 로 `/private/tmp/` 아래에 빼서 grep. 볼 곳: `openBook`(예약 등록 창 · 약 2440줄) · `detailV6Html`(예약 상세 · 약 2133줄) · `s5Pop`(확인 창) · `s5Act` · `renderCtx` · 예약 변경 끌기(약 2891 ~ 2941줄). 시안의 시술 목록은 **D44 와이어로 대체**된다
- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/reference/2026-11-23-reservation/reservation-board-decisions.md` ← 앞 작업 결정 R1 ~ R75(SPEC-006 의 원천). D 가 R2 · R66 입구를 뒤집는다
- 근거 리포트(같은 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/orchestration/work/day-reservation2/`): `research-detail-1-report.md`(모달 칸 38 · 버튼 51 원천 전수 · 단계 경계 조건식) · `be-probe-1-report.md` · `be-probe-2-report.md` · `be-probe-3-report.md`(**KOS 데모 지점 실물 확인 — 경로 · 본문 · 응답 · 오류 · 지연. KOS 쓰기 계약은 이것만 근거로**)
- HAR: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/reference/2026-11-24-reservation-detail/` `수납시술추가.har` · `할인.har` · `시술권사용.har`(파이썬 `-I` 로 JSON 만)

## 2. 배경 / 무엇을 바꾸나

DAY 예약 현황(SPEC-006)은 조회만이다(카드 클릭 동작 없음 · R2). 이번엔 시안 v9 의 **예약 등록 창**(기존 고객 · 새 고객 [저장 후 예약 등록]) · **예약 상세 모달**(단계별 칸 · 버튼 — 예약 → 접수 → 상담 대기 · 진행 → 시술 대기 · 진행 → 귀가 대기 → 귀가) · **카드 우클릭 메뉴**(예약 변경 · 예약 취소 · 동행 추가)를 넣는다. KOS 쓰기가 여럿 생긴다(예약 만들기 · 변경 · 취소 · 새 고객 · 접수 · 방 배정 · 상담 대기 · 상담사 · 시술권 오늘 작업 · 오더 메모 · 시술 대기 · 귀가 완료) — 전부 데모 실물로 확인됐다.

산출물:
1. **새 SPEC `products/day/20-spec/spec-007-reservation-detail.md`** (이름 제안 · 「예약 등록 · 예약 상세 (웹)」) — SPEC-006 · SPEC-002 모양(frontmatter · 결정 원천 인용 · 화면 구성 요소 번호 · UX Contract · 단계 × 오늘/앞날/지난 날 경계 표 · API(이름 제안) · KOS 쓰기 표(동작 · 경로 · 본문 키 · 확인 조건 · 지연 · 실물 근거) · 케이스 매트릭스 · 시안과 다른 곳 · 기획안과 다른 곳 · OQ)
2. **SPEC-006 개정**: 카드 클릭 = 예약 상세(R2 뒤집힘) · 빈 칸 [+] = 예약 등록 · 우클릭 메뉴 · **끌어 놓아 동행 묶기 입구 없앰**(R66 입구 · D45 — 동행은 우클릭 → 예약 상세 동행 체크 · 같은 열 · 같은 시작 시각 · 묶음 통째 저장) · 예약 변경 끌기(옮기기 모드)
3. **SPEC-002 개정**: KOS 쓰기 표에 새 행(경로 + 값 조건 — `write_open` 계약) · `COMPLETED` 는 「안 끝난 작업 취소 뒤」 순서 묶음으로만 · 지정 의사 읽는 자리 = `occupiedResources[].reservationGroup.doctors`(지금 `reservation.doctor` 는 KOS 가 안 씀 — be-probe-1 §4) — 어느 SPEC 이 동기화 매핑 주인인지 확인해 그 문서에
4. **SPEC-000 개정**: `purchase_item` 할인 전 가격 칸(KOS 항목 `basePrice` 스냅샷 · D 할인 행) · 권한 키(D46 `reservation.detail` 이름 제안) · 신분 확인 기록(`identity_check` true/false — 칸 정의가 SPEC-000 에 있으면 인용)
5. `20-spec.md`(Scope · SPEC Bundle) · `10-decision.md` · `log.md` 반영. **30-work(WORK)는 이번에 쓰지 않는다** — SPEC 검수 통과 뒤 따로 발주

## 3. 계약

다른 워커와 합의된 계약 없음(문서 단계). 경로 · 칸 · 키 이름은 「이름 제안」. **KOS 경로 · 본문 · 값 · 확인 조건은 be-probe 리포트 그대로**(지어내지 마라).

## 4. 먼저 읽을 핵심 파일

문서(이 워크트리): `products/day/20-spec/spec-006-reservation-board.md` · `spec-002-procedure-board.md`(KOS 쓰기 표 · 귀가 대기 · 방 배정 · 판 카드 방 규칙) · `spec-000-data-model.md` · `20-spec.md` · `10-decision.md` · `log.md`

코드(read-only · `git -C /Users/kknaks/git/CENTURION_DAY show origin/dev:<path>` · 지금 dev = `4bf0b4a1` 이후일 수 있음 — `git fetch` 하지 말고 `origin/dev` 그대로): 레포 `AGENTS.md` · `backend/day/emr/kos/writes.py`(`write_open` · 쓰기 큐 계약) · `emr/kos/client.py` · `emr/kos/mapper.py`(:581 지정 의사 · :602 isNew) · `emr/kos/mapper_purchase.py`(:125 가격) · `emr/sync_schedule_sales.py`(`visit_task.ticket_id`) · `models/ticket.py` · `models/purchase.py` · `models/task.py` · `models/staff.py`(`job_role.tags`) · `policies/reservation_amounts.py`(원내 현황 금액 — 수납 정보가 그대로 씀) · `services/board_home.py` · `services/board_rooms.py` · `routers/reservations.py` · `templates/partials/reservations_*.html`

cc-prototype(결정 · 시안이 없는 동작만): `git -C /Users/kknaks/git/toy_pr2/cc-prototype show origin/main:procedure/back/app/service/reservations.py`(`create` · `_new_visitor` · `move` · `cancel` · `_links` 딥링크) · `service/reception.py`

## 5. allowed_paths — 이 밖은 건드리지 마라

- `products/day/`

## 6. 구현 단계

1. 결정 D1 ~ D48 을 읽고 **최종 유효 결정**(뒤집힌 것 빼고)을 화면 요소 · 동작별로 묶는다. 각 SPEC 문장 옆에 D / R 번호
2. 시안 코드에서 예약 등록 창 · 예약 상세 · 확인 창 · 우클릭의 요소 · 문구를 전수로 뽑아 **넣음 / 뺌(D 번호) / 바뀜(D 번호)** 표를 만든다. 시안에서 뺀 것(예: 「다음 차례」 배지 · 「상담중」 흐림 · 시술권 카드 · 할인 줄 · 관리실 정원 숫자 · 예약메모 덧붙이기 · 희망 시술/예산 칸)과 비활성 자리만 둔 것([문진 QR] · [여권 스캔])을 명시
3. 단계(예약 · 접수 · 상담 대기 · 상담 진행 · 시술 대기 · 시술 진행 · 귀가 대기 · 귀가 · 예약 취소 · 노쇼) × (오늘 · 앞날 · 지난 날) 경계 표 — 보이는 칸 · 고칠 수 있는 칸 · 버튼. 시안 조건식(research §4)에 D 를 덮어 적는다
4. KOS 쓰기 표(동작별): 경로 · api(internal / open) · 본문 키 · 값 조건 · 확인 조건(다시 읽기 칸) · 늦게 보이는 칸(≈1s) · 순서 묶음(예: 귀가 = 작업 CANCEL → COMPLETED · [상담 대기] = 방 배정 작업 → 방 지정 → CONSULTATION_WAITING · [시술 대기] = 시술권 작업 + 오더 메모 → PROCEDURE_WAITING) · 실패 처리(시술 현황과 같은 토스트 · 다시 시도) · 실물 근거(be-probe 번호). 쓰기 경로 = 시술 현황과 같은 쓰기 큐(D) · 새 고객은 같은 고객 찾기 → 고객 만들기 → 예약 순서 · 연락처 KOS 꼴 · 취소 reason enum
5. 화면이 읽는 칸 표(SPEC-006 처럼): 시술 목록(D44 와이어 · 연결 키 `visit_task.ticket_id → ticket → ticket_set → ticket_bundle.purchase_item_id` · 상태 4 문구 · n/m회 계산) · 수납 정보(원내 현황 금액 R49 ~ R55 + 할인 전 가격) · 수납 버튼 상태(KOS 「수납 중」 = `purchase.status initialized ∧ process pending`) · 딥링크 두 개 · 상담사 목록(직무 `counselor`) · 의사 목록(직무 `doctor` — 면허로 거르지 않음) · 관리실 목록(빈 방부터) · 이전 방문(재진 · DAY DB) · 특이사항
6. 케이스 매트릭스 — 결정 · 시안 · 실물에 없는 경우는 OQ(지어내지 마라). 동시 편집 · 쓰기 큐 대기 중 화면 · 10초 폴링과의 관계는 SPEC-006 · 002 기존 규칙 인용
7. SPEC-006 · 002 · 000 개정(위 §2) — 개정 번호 · 이력 표 형식은 각 문서 관례
8. `20-spec.md` · `10-decision.md` · `log.md`
9. §8 검증

## 7. 범위 제약 — 하지 말 것

- **화면 문구를 지어 넣지 않는다.** 시안 · 결정에 있는 문구만(상태 4 문구 「시술 전」 「시술 중」 「시술 후」 「미진행」은 결정). 없으면 비우고 OQ
- 결정 D · R 을 다시 열지 않는다. 결정끼리 어긋나 보이면 OQ 로 적고 코디에게 묻는다(아래 질문 명령)
- 범위 밖(Out Of Scope 에 「다음 스펙」으로만): 문진 · 여권 스캔 · 신분 확인 자동 접수 · 상담사 순번 · 예약 요청 · 고객 차트 · 처방 만들기 · 수납 항목 넣기(DAY 는 KOS 웹 딥링크만) · 「시술현황 차트 일부 기능 수정」(다른 사람 몫) · 외국인 신분확인(사용자 몫)
- 기획안(`00-baseline/planning/`) · 다른 제품 폴더를 고치지 않는다
- 시안 · HAR 의 사람 이름 · 전화 · id 원문을 예시로 옮기지 않는다

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict → products/day/ 범위 ERROR 0 (타 제품 기존 WARN/ERROR 는 '무관'으로 분리 보고). 근거 없는 정책 0 · 열린 것은 열린 것으로
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 보고 본문에 D1 ~ D48 중 SPEC 에 반영 안 된 번호(있으면 이유)를 적어라.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_cd5ea51a-31a7-4f34-9cf7-ec53af90a280 --from term_37ac7485-be74-4e85-aaf6-c43c0ffd8f03 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_cd5ea51a-31a7-4f34-9cf7-ec53af90a280 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_cd5ea51a-31a7-4f34-9cf7-ec53af90a280 --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
