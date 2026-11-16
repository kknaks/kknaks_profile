
# [frontend] 웹 피드백 W1~W11 화면 수정(받은함 탭 · 카드 · 버튼 · 포커스 · 메모)

너는 **day `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web/orchestration/roles/day/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix-web`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

⚠ 같은 워크트리에서 **backend 워커가 동시에** services · queries · dtos · common · 백엔드 테스트를 고친다 — 그쪽 파일은 건드리지 마라.

## 1. SSOT — 먼저 읽을 것

### 사용자 결정 — 최종 작업 목록(2026-11-12 · 이 표가 정본)

원천: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web/orchestration/work/fix-web/e2e-feedback.md`(W1~W11 · 보충 · 결정 A) · 조사 `research-1-report.md`(같은 폴더 · 파일:줄 근거).

**백엔드**
- **W5** 확인 필요 상황 = **대기(wait) · 마취 초과(anes) · 호출 안 옴(call) · 귀가 대기 필요(home) 4가지**. **수락 뒤 미시작(accept)은 서버에서 뺀다**(결정 A — `needs()` 에서 제거 · `_accepted_unstarted` · `accept_min` · `limits.acceptMin` · env `BOARD_ACCEPT_MIN` · 관련 테스트 정리). `inbox_section` · `urgency` 는 **앱이 쓰므로 그대로**(값 이름 `need`/`startable`/`waiting` 유지). 앱 코드 수정 · 새 빌드 없음 — 앱 화면에서도 accept 가 안 보이게 되는 것은 사용자 확인.

**웹 — 왼쪽 사이드바(받은함)**
- **W2** 탭 「호출 n」 → 「수락 대기 n」 (n = 수락 안 된 호출 수 · 지금 그대로)
- **W3** 탭 「현황」 → 「확인 필요 n」 (n = 목록에 보이는 확인 필요 카드 수 = 상황 수)
- **W6** 확인 필요 탭: **아코디언 없이 확인 필요 카드만**. 시작 가능 · 시술 대기 목록 삭제(웹 전용 `rules.inbox()` 의 startable·waiting 계산 · `inbox_card` 매크로 삭제)
- **W7** 수락 대기 탭: **아코디언 없이 수락 대기 카드만**. 수락함 목록 삭제(API `calls[]` 는 앱이 쓰므로 그대로)
- **W4** **확인 필요 카드(need_card)만** 구조 변경: 머리 = 「룸 이름 · 상태 · 경과」 / 다음 줄 = 사람 이름 / 그 아래 줄 = 버튼(지금 버튼 칸 위치). 상태 글자 = 대기 · 마취 · 호출 · 귀가대기. 경과 형식은 지금 그대로(분).
- **W10** 확인 필요 카드의 [귀가 대기] 버튼 삭제 → 확인 필요 카드 버튼은 호출 상황의 [재호출] 하나뿐
- **W11** 수락 대기 카드(call_card)는 **구조 그대로**, [재호출] 버튼만 삭제 → 버튼 [수락] 하나
- **W9** 탭 변경 · 카드 밖 클릭(문서 어디든) 시 카드 선택 포커스 해제. 팝오버 · 창(dialog) 안 클릭은 해제하지 않음. 다시 그릴 때 선택 복원(`day.js` :437/:472)과 충돌 금지

**웹 — 오른쪽 방 카드**
- **W1** 오더 메모(`.day-memo__box`) 글자 10px → 12px · 접힘 높이(`--day-memo-max-h`)도 같이 늘려 5줄 유지 · `static/day.css` 재빌드
- **W8** 시술 줄 [수락] 버튼 삭제(수락은 사이드바에서만 · 팝오버 · 엔드포인트 · 권한은 그대로)

**그대로 둠**: 앱 · 「시술 완료 n」 탭 · 방 카드 [귀가 대기] · 엔드포인트 · 권한 · migration 없음.

- 스펙: `/Users/kknaks/orca/workspaces/mediness-mediness/fix-web-spec/products/day/20-spec/spec-002-procedure-board.md` (planner 가 위 결정대로 개정 — 결정 표와 다르면 **결정 표가 맞다**, 다른 곳을 리포트에 적어라)
- 조사: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web/orchestration/work/fix-web/research-1-report.md` — 고칠 곳 파일:줄 · 깨질 테스트 목록. **목록은 출발점일 뿐 — 손대기 전에 쓰는 곳을 직접 grep 으로 전부 세라.**
- 레포 규약: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix-web/AGENTS.md`

기대는 개념: 해당 없음.

## 2. 배경 / 무엇을 바꾸나

결정 표의 **웹 몫 전부**: W1 · W2 · W3 · W4 · W6(화면) · W7 · W8 · W9 · W10 · W11 + W5 의 화면 쪽(need_card 의 accept 문구 분기 삭제 · 견본 world).

## 3. 계약 (backend 와 합의 — 이대로 소비)

- 웹 `inbox` = **`{"need": [...]}` 만** — startable · waiting 키 없음(backend 가 지운다). need 항목 `why` ∈ {wait, anes, call, home} · `doctorName` 없음.
- 확인 필요 탭 개수 n = `inbox.need|length`(목록 카드 수). 수락 대기 n = 지금 `waiting_calls|length` 그대로.
- 탭 id(`now` · `call` · `done`)는 바꾸지 않는다 — 글자만(day.js 탭 기억 키 유지).

## 4. 먼저 읽을 핵심 파일

- `backend/day/templates/partials/board_regions.html` :8-10 · :20-39 · `board_parts.html` :91-95(W8) · :212-227 inbox_card · :232-259 need_card · :262-282 call_card · `ui.html` card_head :194 · tabs :168 · memo :228
- `backend/day/static/day.js` :236-251 selectTab · :437/:472 선택 복원 · :616-626 selectCard · :775-783 · `backend/day/styles/app.css` :161 · :375-401 · :448 · CSS 빌드 `scripts/build-css.sh`
- `backend/day/routers/board.py` :154-156 board_context · `routers/kit_board.py` :51,258,283 · `templates/partials/kit_page.html` · `board_main.html` :1-2
- 화면 테스트 `backend/tests/day/web/test_board_page.py`(조사 §4~§6 의 단언 목록) · `backend/tests/architecture/test_screen_copy.py`

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/day/routers/ (api/ 제외) · backend/day/templates/ · backend/day/static/ · backend/day/styles/ 중 브리프가 지정한 곳`
- `backend/tests/day/ 의 화면 테스트`

## 6. 구현 단계

1. 탭(W2 · W3): `("now", "확인 필요 " ~ n)` · `("call", "수락 대기 " ~ n)` · 시술 완료 그대로 · OOB 갱신 경로(`inbox_tabs(oob)`)에서도 n 이 맞게.
2. 아코디언 제거(W6 · W7): 확인 필요 탭 = need 카드 나열만 · 수락 대기 탭 = 수락 안 된 call_card 나열만. 수락함 · 시작 가능 · 시술 대기 · `inbox_card` 매크로(호출처 0 확인 뒤) 삭제. 빈 목록일 때 표시는 지금 아코디언 빈 상태 처리 방식을 따르되 **새 문구를 지어 넣지 마라**(스펙에 없으면 비움).
3. need_card(W4 · W10 · W5 화면): 머리 = 방 이름 + 상태 글자(대기 · 마취 · 호출 · 귀가대기) + 경과(분 · 지금 형식) — `ui.card_head` caller 활용 / 다음 줄 이름 / 버튼 칸은 [재호출](call 일 때만) 하나. [귀가 대기] 삭제 · accept 분기 삭제. `data-day-need` · `data-day-need-why` 속성 유지(day.js 깜빡임).
4. call_card(W11): 구조 그대로 · [재호출] 삭제 → [수락]만. `acceptedBy` 분기(수락함 전용)는 정리.
5. 방 카드 시술 줄 [수락] 삭제(W8 — `board_parts.html:91-94`). 팝오버 본체 · 엔드포인트는 사이드바가 쓰므로 유지.
6. W1: `app.css` `.day-memo__box` 12px · `--day-memo-max-h` 를 12px 기준 5줄로 · `scripts/build-css.sh` 로 `static/day.css` 재빌드.
7. W9: day.js — 탭 변경 · 카드 밖 클릭(문서 어디든 · 팝오버/dialog 안 제외) 시 `clearCards` · 다시 그릴 때 선택 복원 로직과 충돌 없게(해제된 선택이 swap 뒤 되살아나면 안 됨).
8. 견본(`kit_board.py` · `kit_page.html`)의 accept · 아코디언 견본 정리. 화면 테스트 갱신(조사 §4~§6 목록 + 직접 grep).

## 7. 범위 제약 — 하지 말 것

- `backend/day/services/` · `queries/` · `dtos/` · `common/` · `routers/api/` · `app/` 수정 금지(backend 몫 / 앱 안 고침). 인라인 스크립트 0 · 손 CSS 금지(기존 토큰 · 클래스 체계 안에서).
- 화면 문구 발명 금지 — 결정 표에 있는 글자만.
- 커밋 · push · PR 금지. 사용자 포트 · 프로세스(11040 · `day-local`) 금지.
- **backend 워커가 같은 워크트리에서 동시에 작업한다** — 그쪽 파일은 건드리지 않는다.

## 8. 검증

```
uv run pytest -q <네가 만든 화면 테스트만>(TestClient 로 전체 페이지 · HX 조각 렌더 확인) — 1회. CSS 를 다시 빌드했다면 빌드 명령 1회. 인라인 스크립트 0 · 손 CSS 0(grep). 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web/orchestration/work/fix-web/fe-1-report.md` (변경 파일 · 테스트 수치 · 견본 화면 확인 · 계약 준수 · 손 CSS/인라인 스크립트 grep 0)

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_b1db5638-c143-4f48-b35e-4550ff2d45d4 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_b1db5638-c143-4f48-b35e-4550ff2d45d4 \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_b1db5638-c143-4f48-b35e-4550ff2d45d4 --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
