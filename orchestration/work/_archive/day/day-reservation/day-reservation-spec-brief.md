
# [planner] DAY-SPEC-006 예약 현황 (조회 · 웹) 새로 쓰기

너는 **day `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/roles/day/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**너는 앞 맥락이 없다.** 이 브리프와 아래 파일이 전부다. 이 워크트리는 너 혼자 쓴다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/reference/2026-11-23-reservation/reservation-board-decisions.md` ← **사용자 결정 R1 ~ R16 · 열린 것 O1 · O2. 계약의 SoT. 다시 열지 마라. 여기 없는 정책은 발명하지 마라.**
- `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/reference/2026-11-23-reservation/20261113_예약현황_시연 (1).html` ← 시안. **화면 요소 · 문구 · 색 · 상태 생김새의 정본.** 한 파일(3MB · 이미지 data URI 포함) — grep 으로 읽어라. 범위 밖 요소(상세 모달 · 예약 요청 내용 · 근무표 등)도 들어 있다 — 결정 R1 ~ R5 · R14 ~ R16 으로 거른다
- `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec/products/day/00-baseline/planning/데이(CC)-기획안-·-예약-현황-·-예약.md` (+ 같은 폴더 `…-접수·귀가.md` · `…-확인-요청.md` · `데이(CC)-개요.md`) — 기획 원문. **고치지 않는다.** 결정 · 시안과 다르면 결정 · 시안이 이기고, 다른 곳을 SPEC 에 적는다

**기대는 개념**

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/para/areas/concept/cs/read-side-effect.md` — 이 화면은 조회만이다. 조회 경로가 KOS 를 부르거나 DB 를 쓰는 부작용이 없어야 한다

## 2. 배경 / 무엇을 바꾸나

DAY 웹에는 지금 「시술 현황」(DAY-SPEC-002) 한 화면뿐이다. 데스크용 **「예약 현황」 화면**을 새로 만든다. 이번 판은 사용자 결정 R1 대로 **조회만** — 하루 예약 표(세로 열 = 병원 예약 그룹 · 가로 시간 칸 · 예약 카드)와 오른쪽 패널(위 공지 / 아래 예약 요청 자리 · 세로 1:1).

데이터는 새로 만들지 않는다. KOS → DAY 동기화가 이미 채우는 사본(예약 그룹 · 시간표 · 휴무 · 방문 · 고객 · 구매 · 공지 테이블)을 읽는다(R6 ~ R13 · R16). 로컬 · dev 는 KOS 데모 지점 사본이다.

산출물: **새 SPEC `products/day/20-spec/spec-006-reservation-board.md`** + 그에 맞춘 `20-spec.md` 지도(Scope · SPEC Bundle) · `10-decision.md` · `log.md` 갱신. WORK(30-work)는 이번에 쓰지 않는다 — SPEC 이 사용자 리뷰를 통과한 뒤 따로 발주한다.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

해당 없음 (문서 단계). SPEC 안의 경로 · 칸 이름은 DAY-SPEC-002 처럼 **「이름 제안」**으로 적고, 정하지 못한 것은 OQ 로 둔다.

## 4. 먼저 읽을 핵심 파일

문서 (이 워크트리):
- `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec/products/day/20-spec/spec-002-procedure-board.md` — **같은 웹(Jinja2 + HTMX) 화면 SPEC 의 본.** 모양(frontmatter · 결정 원천 인용 · 화면 구성 표 · 상태 · API · 케이스 매트릭스 · cc 와 다른 곳 · OQ)을 따라라. 「수납 필요」 판정이 여기 있다 — R13 과 맞춰라
- `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec/products/day/20-spec/spec-000-data-model.md` — `reservation_group` · capacity · timetable · `visit` · `notice` 계약(§3 · §4A). 칸 정의는 여기를 인용하고 복사하지 않는다
- `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec/products/day/20-spec.md` · `10-decision.md` · `log.md` · `40-architecture/erd.md` — 지도 · 결정 · 이력 형식

코드 (read-only · git ref 로 읽는다 — 체크아웃 · 수정 금지):
- DAY: `git -C /Users/kknaks/git/CENTURION_DAY show origin/dev:<path>` — `backend/day/models/room.py`(예약 그룹 · 시간표 · 휴무 · 점유) · `models/visit.py` · `enums/visit.py`(FlowStep 8개) · `models/customer.py`(nationality) · `models/purchase.py`(:58 수납 필요 주석) · `models/notification.py`(:96 notice) · `routers/board.py` · `templates/board.html`(화면 방식 본) · `AGENTS.md`
- cc-prototype(참고 동작): `git -C /Users/kknaks/git/toy_pr2/cc-prototype show origin/main:<path>` — `procedure/back/app/api/reservations.py`(:58 `GET /reservations/board`) · `procedure/back/app/service/reservations.py` · `procedure/back/app/schemas/reservations.py` · `procedure/front/components/reservations/ScheduleTable.tsx` · `ResvAside.tsx` · `view.tsx` · `controls.tsx`. **결정 · 시안이 없는 동작만** cc 를 따른다

## 5. allowed_paths — 이 밖은 건드리지 마라

- `products/day/`

## 6. 구현 단계

1. 결정 파일 · 시안 · 기획안을 읽고 화면 요소를 **넣음 / 뺌(R 번호)** 으로 나눈 표를 만든다(DAY-SPEC-002 「화면 구성」 표처럼 요소 번호를 붙인다)
2. 열린 것 O1(`reserved` 카드 색) · O2(「n명」의 뜻)를 **시안에서** 확인한다 — 시안 코드에서 근거 줄을 찾으면 닫고 근거를 적는다. 못 찾으면 OQ 로 남긴다
3. R12(카드 국가)를 시안과 대조한다 — 카드 아래 글자가 고객 국적인지 다른 값인지. 근거와 함께 적는다
4. 화면마다 읽는 칸을 DAY 테이블 · 칸으로 짝짓는다(R6 ~ R13 · R16). 칸이 없거나 동기화가 없는 것은 「빈 상태로 보임」 또는 OQ — 칸을 새로 만들자는 제안은 OQ 로만
5. 날짜 이동 · 오늘 · 필터 · 현재 시각 선 · 가로 넘김 · 빈 상태 · 휴무일 · 범위 밖 시간 예약 · 같은 칸 여러 건 · 취소/부도 예약 표시 여부 같은 **경우를 케이스 매트릭스로** 정리한다. 시안 · 결정 · cc 어디에도 없는 경우는 OQ
6. 조회 경로(전체 페이지 · HTMX 조각 — 이름 제안) · 권한(지금 웹 로그인과 같은지) · 갱신 방식(새로고침 / 폴링 / SSE)을 적는다. 정하지 못하면 OQ
7. `20-spec.md`(Scope In/Out · SPEC Bundle) · `10-decision.md` · `log.md` 에 이번 판을 반영한다
8. §8 검증

## 7. 범위 제약 — 하지 말 것

- 쓰기 동작 · 상세 모달 · 예약 요청 내용 · 근무표 · 고객 등록 · 원내 현황 · 앱으로 보내기(여권 스캔 · 전후 사진 · 문진)를 SPEC 범위에 넣지 않는다 — Out Of Scope 에 「다음 스펙」으로만 적는다
- **화면 문구를 지어 넣지 않는다.** 시안에 있는 문구만. 시안에 없으면 비워 두고 OQ
- 결정 R1 ~ R16 을 다시 열지 않는다. 결정과 기획안이 다르면 결정을 따르고 차이를 적는다
- 테이블 · 칸 · migration 을 새로 설계하지 않는다(필요해 보이면 OQ)
- KOS 새 API 호출 · 새 동기화 회차를 계약에 넣지 않는다(공지 동기화 필요 여부는 OQ)
- 기획안(`00-baseline/planning/`) · 다른 SPEC 본문 · 다른 제품 폴더를 고치지 않는다
- 고객 실명 · 전화번호 등 시안의 가짜 값도 SPEC 예시에 옮기지 않는다

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict → products/day/ 범위 ERROR 0 (타 제품 기존 WARN/ERROR 는 '무관'으로 분리 보고). 근거 없는 정책 0 · 열린 것은 열린 것으로
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
  --to term_28a8c525-c408-4f25-a0f2-ffd6c29fb56d --from term_871316a2-3e92-498c-874a-8dbb7f4b9ed5 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_28a8c525-c408-4f25-a0f2-ffd6c29fb56d \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_28a8c525-c408-4f25-a0f2-ffd6c29fb56d --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
