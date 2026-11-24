# [backend · 실물 확인] KOS 데모 지점 — 예약 등록 · 새 고객 · 예약 변경 · 취소 쓰기가 실제로 들어가나

너는 **day `backend` 워커**다. 맥락이 없다고 생각하고 이 파일만 따른다. 먼저 역할 문서를 읽어라(절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/orchestration/roles/day/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- 코드 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation2` (base `origin/dev` `4bf0b4a1`) — 레포 루트 `AGENTS.md` 먼저

**이번 일은 구현이 아니다. 레포 파일을 고치거나 커밋하지 마라.** 시험 스크립트는 레포 밖 `/private/tmp/day-probe-1/` 에만 둔다. 결과는 리포트 하나.

## 1. 왜

DAY 예약 현황에 **예약 등록 창**(기존 고객 / 새 고객 [저장 후 예약 등록])과 예약 변경 · 취소를 넣는다. DAY 원칙(`backend/day/emr/kos/writes.py` 머리 주석 · SPEC-002 OQ-23)은 「KOS 쓰기는 데모 지점 실물로 확인한 뒤 연다」. 경로 · 본문은 cc-prototype 이 KOS 에 실제로 부른 것을 가져온다. 이 경로들이 **DAY 의 KOS 클라이언트로** 데모 지점에 실제로 들어가는지, 응답 모양이 무엇인지를 확인한다.

## 2. 쓸 것

- KOS 호출 = DAY 클라이언트 `backend/day/emr/kos/client.py` `KosClient`(`internal()` · `open()`) 를 그대로 써라(시스템 계정 sign-in · UA · 헤더가 거기 있다). 새 HTTP 코드를 짓지 마라.
- 데모 지점 값 = `/Users/kknaks/git/CENTURION_DAY/deploy/local.env` 의 `DAY_SEED_KOS_*` 와 `KOS_*_BASE` · `KOS_WEB_BASE`. **스크립트 안에서 읽기만 하고 값을 화면 · 로그 · 리포트에 출력하지 마라.**
- **데모 지점 확인 먼저**: 쓰기 전에 `backend/day/emr/kos/demo/board_data.py` `check_open_key_is_demo` 와 같은 확인(공개 `get-zones` 구역 id 가 데모 테넌트 예약 그룹 `intervalCapacities[].zoneId` 에 있나)을 통과해야 한다. 실패하면 **아무 쓰기도 하지 말고 멈춰서 보고**.
- 경로 · 본문 근거(cc, `git -C /Users/kknaks/git/toy_pr2/cc-prototype show origin/main:<path>`):
  - `procedure/back/app/service/reservations.py` — `create`(L779 ~) · `_new_visitor`(L896 ~) · `move`(L941 ~) · `cancel`(L991 ~) · 상수 L79 ~ 94
  - 예약 상세 읽기 = cc `app/kos/reservation_sync.py` `PATH_DETAIL`(DAY 에도 상세 조회 경로가 있으면 그것)
- 예약 그룹 · 구역 · 직원(의사 · 담당자) · 유입 코드 KOS id 는 KOS 읽기 API 로 얻어라(DAY 동기화 코드가 부르는 경로 · `backend/day/emr/kos/` 참고). 로컬 DB · docker 는 건드리지 마라.

## 3. 시험 (순서대로 · 각 단계 요청 경로 · 본문 키 모양 · 응답 코드 · 응답 키 모양 · 다시 읽은 결과를 기록)

시험 데이터 규칙: 고객 이름은 한국어 시험용 이름 + 「(시험)」 꼬리표, 연락처는 데모용 가짜 번호. 예약은 **오늘이 아닌 앞날**(내일 이후 · 영업 시간 안 · 빈 칸)로만.

1. **같은 고객 찾기** `visitor/v1/queries/find-duplicated-visitor` — 새 이름으로 「없음」 응답 모양 · 이미 있는 데모 고객 정보로 「있음」 응답 모양
2. **새 고객 만들기** `v1/visitor/commands/create-visitor` — 이름 · 한글 발음 · 성별 · 국적 · 생년월일 · 연락처 · SNS 한 번에 → 응답 고객 id → 고객 상세 다시 읽어 각 칸이 들어갔는지(칸마다 O / X)
3. **예약 만들기** `schedule/reservation/v2/commands/reserve` — 2의 고객 id · 담당자 = 시스템 계정이 아닌 **실제 직원 한 명**의 KOS id · 예약 그룹 + 구역 · 시작 / 끝(= 그룹 간격) · 유입 코드(`funnel` · `funnelDetail`) · 예약 메모 → 응답 일정 id → 예약 상세 다시 읽어 칸마다 O / X. **응답의 `visitor.isNew` 값도** 적어라.
4. **지정 의사 두 자리 시험** — 의사 직원 하나로 예약 두 건 더:
   - ⓐ 본문 최상위 `doctor: {id, name}`
   - ⓑ `occupiedResources[].reservationGroup.doctors: [{id, name}]`
   각각 다시 읽어 `reservation.doctor` 와 `occupiedResources[].reservationGroup.doctors` 중 어디에 들어갔나. 둘 다 안 들어가면 그대로 「안 들어감」. 응답이 4xx 면 코드 · 메시지(값 빼고).
5. **예약 변경** — 3의 예약을: 날짜 · 시간 바꾸기 / 예약 그룹 바꾸기 / 지정 의사 바꾸기(4에서 들어간 자리로). 경로는 cc `move` 가 쓰는 내부 `schedule/reservation/v2/commands/update-reservation`. 다시 읽어 바뀌었나.
6. **예약 취소** — 공개 `schedule/open/v1/commands/cancel-reservation`(cc `cancel`) → 다시 읽어 상태가 취소인가(KOS 상태 값 그대로 적기). 4에서 만든 두 건도 취소해서 정리.
7. 2에서 만든 시험 고객은 지우지 말고 남긴다(지우는 API 를 찾지 마라) — 리포트에 KOS 고객 id 앞 8자만.

## 4. 하지 말 것

- 레포 파일 수정 · 커밋 · push 금지. 로컬 스택 · docker · 포트 · `.run` 건드리지 마라. 로컬 DB 읽기 / 쓰기 금지.
- `~/.config/day/` 아래 파일(특히 `prod-*`) **절대 열지 마라.** 데모 지점 말고 다른 병원 키로 부르지 마라.
- 오늘 날짜 예약 · 이미 있는 데모 예약 · 이미 있는 데모 고객을 바꾸거나 취소하지 마라(네가 이번에 만든 것만).
- 비밀값 · 토큰 · 고객 개인정보 원문을 출력 · 기록하지 마라. 응답은 **키 이름과 모양**만(값은 O / X · id 앞 8자).
- 본문 칸을 지어내지 마라 — cc 본문에 없는 칸은 4번 의사 시험 말고는 넣지 마라.
- 한 단계가 실패하면 같은 요청을 반복하지 말고(최대 1회 재시도) 기록하고 다음 단계로. 2가 실패하면 3 이후는 기존 데모 고객이 아니라 **멈추고 보고**.

## 5. 리포트

`/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/orchestration/work/day-reservation2/be-probe-1-report.md`

맨 위 표: 시험 1 ~ 6 × (경로 · 응답 코드 · 들어갔나 O / X · 비고). 그 아래: 단계별 요청 본문 키 모양 · 응답 키 모양 · 다시 읽은 칸 O / X · 지정 의사 결론(ⓐ / ⓑ / 안 들어감) · `isNew` 값 · 「DAY `writes.py` 에 열 때 필요한 것」(경로 · 값 조건 · 확인 조건 후보 — 결정 아님). 시험 스크립트 경로(`/private/tmp/day-probe-1/`).

## 6. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 이 preamble 과 다르면 preamble 쪽으로만 보내라.

```bash
orca orchestration send \
  --to term_cd5ea51a-31a7-4f34-9cf7-ec53af90a280 --from term_ed3a1728-5b0e-455f-b9f2-fb76c72fd39c \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: KOS 데모 실물 확인 1" \
  --body "리포트 경로 / 시험 1~6 O·X / 지정 의사 결론 / 미결"

orca terminal send --terminal term_cd5ea51a-31a7-4f34-9cf7-ec53af90a280 \
  --text "[worker_done] backend 완료 — KOS 데모 실물 확인 1. 상세는 인박스." --enter
```

막히면: `orca terminal send --terminal term_cd5ea51a-31a7-4f34-9cf7-ec53af90a280 --text "[질문] backend: <질문>" --enter`
