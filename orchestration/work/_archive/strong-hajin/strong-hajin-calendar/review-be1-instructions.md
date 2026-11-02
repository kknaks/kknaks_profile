# [reviewer] Phase BE-1 검수 지시 — 발주 시 terminal send 로 요지만 보낸다

> 코디 메모: 리뷰어 터미널은 맥락이 살아 있다(SPEC 4판 + WP 1판). 이 파일은 **발주 기록**이고,
> 실제 주입은 이 내용의 요지를 짧게 보낸다 — 3126 bytes 메시지가 잘린 적이 있다.

## 대상

- 코드 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar` 의 **uncommitted diff 전부**
- `git diff` 와 `git status --short` 로 범위를 먼저 확정하라

## 기준

- `…/30-work/work-004-calendar-scheduling.md` **Phase BE-1** — 작업 1~9 · 완료 판정
- `…/20-spec/spec-004-calendar-scheduling.md` §4 Interface Contract · §5 · §6
- `…/10-decision/decision-003-calendar.md` 증보 **K1~K14**
- 코드 레포 `AGENTS.md`

## 볼 것 — 일곱

1. **allowed_paths 준수** — `backend/` · `docker-compose.yml` · `Makefile` 밖을 건드렸나.
   `frontend/`·`para/`·`orchestration/` 에 손댔으면 **즉시 FAIL**.
2. **Phase 경계** — BE-2(D1 세 자리 검증 · `schedule_release` 응답 · 운영 대장 등록)나 FE 를
   당겨서 했나. **당겨 했으면 FAIL** — 검수 단위가 무너진다.
3. **검수 네 판이 닫은 열 자리가 코드에서 지켜졌나.** 이게 핵심이다.
   - K10 `POST` 가 `expected_version` 을 **안 받는가**. 그 날이 차면 **409** 인가
   - K12 **영수증 조회가 409 검사보다 먼저**인가. 순서를 코드에서 확인하라
   - K8 `expected_version` 이 **배정 회차**인가. 업무 `version` 을 올리지 않는가
   - K7·K11 **기간 네 경우**가 한 함수에 있고 뒤집힘이 `[min,max]` 인가
   - K14 `span_from`·`span_to` 가 **그 함수의 출력**인가 (따로 계산하면 두 벌이 된다)
   - K5 권한이 **활성 담당 관계**인가. capability 봉투로 판정하지 않는가
   - K6 읽을 수 있으나 담당 아님 → **403**, 읽을 수 없음 → **404** 인가
   - K13 `is_active_assignee` 를 **안 싣는가**
   - §C `COMPLETION_SUBMITTED` 를 **남기는가** (거르는 것은 `DONE`·`CANCELLED` 뿐)
   - K2 `from`/`to` 가 오면 **구획도 커서도 안 쓰는가**. 없으면 기존 동작 그대로인가
4. **`meetings_visible_to` 소비처 셋** — `my_meetings`·`readable_rows` 가 **안 바뀌었나**.
   선택적 인자거나 호출부 필터인가. **불변을 증명하는 테스트가 있나**
5. **부분 unique 증명 넷**이 `tests/integration/postgres/` 에 각각 한 건씩 있나 —
   ① 있고 valid ② 술어가 「닫히지 않은 행만」 ③ 살아 있는 중복 거절 ④ 닫힌 날 재배정 선다.
   **「선언했다」를 근거로 쓴 자리가 있으면 지적하라**
6. **조용히 통과하는 자리** — 테스트가 초록인데 계약이 깨진 곳. 빈 단언 · 폴백 ·
   개명으로 지나간 곳 · `try/except` 로 삼킨 곳
7. **기존 실패와 새 실패의 분리** — 워커가 기준선을 재고 「무관」을 분리했나

## 판정

**FAIL** — 계약과 다른 것이 돈다 / allowed_paths 위반 / Phase 경계 위반 / 증명 없음
**WARN** — 물어야 할 만큼 모호하다
**PASS** — BE-2 로 넘어가도 된다

지적마다 **`파일:줄` + 근거.** 근거 없는 지적은 쓰지 않는다. 취향은 지적이 아니다.
FAIL·WARN 은 **무엇을 어떻게 고쳐야 하는지**까지 — 원 워커에게 그대로 재발주된다.

## 리포트

`orchestration/work/strong-hajin-calendar/review-be1-report.md` **한 파일만** 쓴다.
코드는 **한 줄도 고치지 마라.** 테스트는 **읽기만** 한다 — 돌리지 마라(워커의 워크트리다).
