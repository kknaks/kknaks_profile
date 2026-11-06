# 리뷰 리포트 — day-data-architecture / doc · SPEC-001 화면 절 닫음 · #232 v2 · #230 v3 (2026-11-06)

**대상**
- mediness 워크트리 `spec-001-login-session.md` · `log.md`(미커밋)
- Issue #232(contract v2 · 코멘트 1) · #230(contract v3 · 코멘트 2)
- `delivery/v2-login-page.json`(v1 사본 대조) · `v2-board-backend.json`(v2 사본 대조)
- 지시 `planner-login-board-v-instructions.md` · 작성 리포트 `planner-login-board-v-report.md`

**원천**
- `erd/04-staff.md` L133 「웹 화면 문구 · 흐름」
- `screen/procedure-board-decisions.md` L39-44 「결정 — #230 계약 검수에서 올라온 것」

**앞 검수**: `review-delivery232-report.md`(W1 ~ W5) · `review-spec001-screen-report.md`(N1 · N2 · 4절 ① ~ ⑤) · `review-delivery230-231-v2-report.md`(W6 · W8 열림)

**lint**: `--strict` → **0 error** · `products/day/` 경고 0.

## 판정: WARN (가벼움 3)

- SPEC-001 「아직 열린 것」은 원천대로 닫혔다.
- #232 v2 는 W1 ~ W5 와 4절 ① ~ ⑤ 를 모두 담았다.
- #230 v3 의 W6 은 원천 결정대로 들어갔다.
- W8 은 열린 채다.
- 두 Issue 모두 라벨이 `delivery-plan:review` · `execution-plan:ready` · `spec-baseline:pending` — **승인 없음**.

남은 것은 셋이다.
- #232 의 「#229 가 끝난 뒤」 문구가 지금 진행 중인 구현과 어긋난다(N1).
- #230 의 재호출 닫는 범위가 TD 와 A5 에서 다르다(N2).
- W6 결정이 SPEC-002 에 아직 없다(N3).

## 1. SPEC-001 「아직 열린 것」

| 원천 L133 | SPEC-001 | 판정 |
|---|---|---|
| 화면 절 추천안 그대로(13줄 · KOS 장애 문구 포함) | 대응표 머리 「문구(사용자 2026-11-06)」 · 13줄 + 로그아웃 · `kos_unavailable` = 「KOS 연결에 문제가 있어 로그인할 수 없습니다. 잠시 뒤 다시 시도해 주세요」 | 같음(앞 검수에서 「확인 때 같이 볼 것」으로 적은 KOS / DAY 방향은 사용자가 원천에서 KOS 문구로 정했다 — 닫힘) |
| 임시 토큰 = 숨은 폼 칸 | 흐름 아래 임시 토큰 줄 「(사용자 2026-11-06)」 | 같음 |
| 실패 때 이메일 유지 · 비밀번호 비움 | 흐름 그림 「— 사용자 2026-11-06」 | 같음 — **앞 검수 N1 닫힘** |
| 갈 곳 = dev 견본 / 그 밖 빈 홈 | 「로그인 뒤 갈 곳 … (사용자 2026-11-06)」 | 같음 |
| — | §5 「아직 열린 것」에서 문구 · 숨은 칸 줄 삭제 · 새 표 「웹 화면에서 정한 것」 5줄 · 머리말 개정 ⑤ · log 한 줄 | 맞다 |

- 앞 검수 N2(원천 L130 CSRF 줄이 `/api/auth/*` 만 적음)는 코디 몫으로 남았다.
- #232 Review Surface 에 그 사실이 적혀 있다. 그대로 두는 것이 맞다.

## 2. #232 v2 — W1 ~ W5 · 4절 ① ~ ⑤

| 검수 | v2 | 판정 |
|---|---|---|
| W1 SPEC 이 계약 phase | TD1 「SPEC-001 §2 「웹 화면」 절(확정)을 그대로 구현」 · phase 1 · A6(SPEC PR) · code_surface mediness 줄 · open_questions 삭제 · Non-Goal 「SPEC 문서 작성 — 이미 닫힘」 | 닫힘 |
| W2 웹 = 화면 라우트 | Review Surface 「사용자 2026-11-06 결정(원천 04) — 이 계약의 기본값이 아니다」 · SPEC-001 §3 · OQ-1 개정과 맞음 | 닫힘 |
| W3 임시 토큰 | TD8 · A7(숨은 칸 · URL · 쿠키 · 로그 없음 · 5분 / 한 번 → `session_expired`) | 닫힘 — #227 `services/auth.py:81-112 · 226-229` 와 맞다 |
| W4 13줄 | A2 「매트릭스 13줄 + 로그아웃 — 대응표와 같다(13줄 기준)」 · A3 forbidden · csrf_failed · 만료 `?reason` | 닫힘 |
| W5 A5 문장 | 「쿠키 세션 쓰기(POST /logout)만 CSRF · 로그인 전 요청(웹 둘 · 앱 둘) 미적용」 | 닫힘 |
| ① 웹 화면 라우트 | TD3 · code_surface `routers/(login)` | 담김 |
| ② 쿠키 심는 자리 · `client` 기본값 | TD4 · A6(앱 경로 회귀 테스트) · Review Surface 「JSON client 기본값 = 외부 계약」 | 담김 |
| ③ 웹 로그아웃 | TD5 | 담김 |
| ④ CSRF 미적용 주석 | TD6 | 담김 |
| ⑤ 웹 오류 응답 | TD7 · code_surface `session.py` · `runtime/main.py` | 담김 |
| 「백엔드는 라우트 · 리다이렉트만」 | 지워지고 #227 웹 쪽 손질이 Target Delta 로 | 고쳐짐 |

GitHub 제목은 v1 그대로다(CLI 한계 · 본문 목표 줄은 v2). 계약 판정과는 무관하다.

## 3. #230 v3 — W6 · W8

| | v3 | 판정 |
|---|---|---|
| W6(원천 L43) | TD 새 줄 「[귀가 대기] · 시작 취소 · 완료 취소 · 재호출의 DAY 동작은 한다 · KOS op 만 만들지 않는다 · 다음 폴링이 되돌릴 수 있음(감수) · HAR 오면 확인 값만」 · A5 「DAY 동작 성공 · op 0 · 다음 조회가 KOS 값을 따름(단위 테스트)」 · Non-Goal · Review Surface(「예: 귀가 대기 카드가 다시 시술 대기로 돌아옴」) · verification 한 줄 · open_question 에서 빠짐 | 원천과 같다 — 단 재호출 범위는 N2 |
| W8 | A8 끝 「수락 단계 원장 계정은 사용자가 준 뒤(local.env 만 · W8 대기)」 · Review Surface · open_question 「데모 지점 원장 계정(W8)」 | **열린 채 — 맞다** |

## WARN

### N1. #232 「#229 가 끝난 뒤」가 이미 진행 중인 로그인 구현과 어긋난다
- #232 v2 TD2 「medikit HTMX 기반(#229)이 **끝난 뒤** #229 매크로로만 조립한다」 · dependencies 첫 줄 #229 · Issue 실행 표의 시작 조건 「결과 계약 승인」.
- 지금 상태
  - #229 Issue 는 OPEN · `delivery-plan:review`(승인 전)이다.
  - 코드 워크트리 `CENTURION_DAY/day-data-architecture`(HEAD `fb2508e4`)에는 #229 몫(`web.py` · `main.py` · `templates/` · `static/` · `styles/` · `routers/kit.py` · `tests/architecture/test_web_rules.py`)이 **미커밋으로 진행 중**이다.
  - 로그인 몫으로 보이는 변경(`session.py` · `runtime/main.py` 수정)도 같은 워크트리에 섞여 있다.
- 사용자 지시로 로그인 구현이 계약보다 앞서 가고 있다. 그래서 문구 그대로 읽으면 구현자는 「#229 가 끝나기 전엔 시작하면 안 됨 · 승인 전엔 시작 안 함」에 걸린다.
- 같은 워크트리에서 #229 · #232 변경이 함께 쌓이므로, 나중에 어느 Delivery 의 커밋인지 가르기도 어렵다.
- 고칠 방향(코디 판단): 둘 중 하나를 고른다.
  - (가) 「#229 매크로 · base 가 있는 상태(같은 브랜치에서 #229 와 함께)」로 의존 문구를 고친다. 사용자가 앞당긴 사실을 Review Surface 에 한 줄 적는다.
  - (나) 계약은 그대로 두고, 구현이 앞선 것을 scope delta 로 기록한 뒤 승인한다.
- 어느 쪽이든 **#229 커밋과 #232 커밋을 나눠** 쌓으라고 frontend 에 알리는 편이 좋다(Delivery 마감 때 「어느 계약의 커밋인가」).
- 「#229 매크로로만」 · 손 CSS 0 · 「새 매크로가 필요하면 #229 로 되돌림」은 구현을 막지 않는다. 같은 브랜치라면 #229 매크로에 더하면 된다.

### N2. #230 의 재호출 — TD 는 재호출 KOS 쓰기를 통째로 닫고, A5 는 「이미 WAITING 인 작업 재호출」만 닫는다
- 원천 L43 「HAR 로 확인 안 된 동작(… · **재호출 재전송**)」.
- 계약은 두 곳이 다르다.
  - v3 TD 「[귀가 대기] · 시작 취소 · 완료 취소 · **재호출**의 DAY 동작은 한다 — KOS 쓰기 op 만 만들지 않는다」
  - A5 「이미 WAITING 인 작업 재호출」 · KOS 쓰기 TD 「call-tasks-doctors(아직 호출 안 된 작업)」
- 재호출의 KOS 쓰기는 3단계다(SPEC-002 KOS 쓰기 표). 1 · 2단계는 HAR 로 확인됐고, 3단계를 WAITING 작업에 다시 보내는 것만 미확인(OQ-09)이다.
  - ① `change-tasks-room`(확인됨)
  - ② `change-tasks-assignees`(확인됨)
  - ③ `call-tasks-doctors`(미확인 — WAITING 재전송)
- TD 대로면 ① · ② 도 안 나가고, A5 대로면 ① · ② 는 나가고 ③ 만 막힌다. 구현자가 고르게 된다.
- 고칠 방향: 「재호출 = ③ 만 닫는다(① · ② 는 확인된 값이라 연다)」 또는 「재호출 3단계 모두 닫는다」 중 하나로 TD 와 A5 를 맞춘다. 원천의 「재전송」이란 낱말은 ③ 만 닫는 쪽으로 읽힌다. 다만 ③ 없이 ① · ② 만 보내면 KOS 에는 담당자 · 방만 바뀌고 호출은 그대로다. 그것이 괜찮은지는 사용자가 정할 일이다.

### N3. W6 결정이 SPEC-002 에 없다
- SPEC-002 KOS 쓰기 표(L437-463)는 [귀가 대기] · 시작 취소 · 완료 취소 · 재호출의 KOS 요청을 「HAR 없음 · OQ-08 · 09 · 10」으로 둔 채, 그 쓰기들을 **하는 것으로** 적고 있다. U-9 · 규칙 13 · 14 · 17 도 「+ KOS `change-flow-step(…)`」을 포함한다.
- 1차의 실제 동작(DAY 만 · KOS op 없음 · 폴링이 되돌릴 수 있음)은 #230 계약에만 있다. 계약이 SPEC 보다 구체적인 정본이 되어 버렸다.
- 사용자 눈에 보이는 결과(귀가 대기 카드가 다시 시술 대기로 돌아올 수 있음)도 SPEC-002 시나리오(S-5 · S-6)에 없다.
- 고칠 방향: SPEC-002 에 W6 결정을 한 줄로 반영한다(KOS 쓰기 표 · 해당 규칙에 「1차는 KOS 쓰기 닫음 — 원천 screen 결정 W6」 + S-5 · S-6 에 되돌아옴 감수). planner 몫이다. #230 계약은 지금 그대로 두고, 다음 판(baseline 재결속) 때 SPEC 을 인용하게 한다.

## 새 모순 · 발명

- 없음.
  - #232 v2 의 `client` 기본값 변경은 앞 검수 4절 ② 그대로다.
  - #230 v3 의 「귀가 대기 카드가 다시 시술 대기로 돌아옴」은 W6 결정(폴링이 되돌림 감수)에서 바로 나오는 결과를 예로 든 것이다.

## 고칠 방향 요약

1. **N1(코디)** — #232 의 「#229 끝난 뒤」 · 시작 조건을 진행 중인 구현과 맞추거나 scope delta 로 기록한다. frontend 에는 #229 · #232 커밋을 나누라고 알린다.
2. **N2(planner · 필요하면 사용자)** — #230 재호출 닫는 범위(③ 만 / 셋 다)를 TD 와 A5 에서 하나로 맞춘다.
3. **N3(planner)** — SPEC-002 에 W6 결정(1차 KOS 쓰기 닫음 · DAY 만 · 되돌아옴 감수)을 반영한다.
