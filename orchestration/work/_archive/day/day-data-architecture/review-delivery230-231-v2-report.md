# 리뷰 리포트 — day-data-architecture / doc · Delivery #230 · #231 contract v2 재검수 (2026-11-06)

**대상**
- Issue MediSolveAIDev/CENTURION_DAY#230 · #231 본문 — 메타 `contract_version=2`, 코멘트는 scope-delta v2 하나씩
- `delivery/v2-board-backend.json` · `v2-board-screen.json`(v2)
- 지시 `planner-delivery230-231-v2-instructions.md` · 작성 리포트 `planner-delivery230-231-v2-report.md`

**앞 검수**: `review-delivery230-231-report.md`(W1 ~ W8). W6 · W8 은 사용자 답을 기다리는 중이라 이번 판정에서 뺐다(지시대로).

## 판정: PASS

W1 · W2 · W3 · W4 · W5 · W7 이 모두 고칠 방향대로 닫혔다. 고치면서 새로 생긴 모순은 없다.
- 위험: #230 L3 · #231 L2
- 라벨: 둘 다 `delivery-plan:review` · `execution-plan:ready` · `spec-baseline:pending`
- **승인 없음**

## 닫혔나

| W | v2 | 판정 |
|---|---|---|
| W1 (경로 + 값) 단위 쓰기 열기 | #230 TD「KOS 쓰기」 — **(경로 + 값) 단위로 연다 · HAR 확인된 값만**<br>· `change-flow-step` 은 `step = PROCEDURE` 만<br>· `change-tasks-complete` 는 `complete = true` 만<br>· `call-tasks-doctors` 는 아직 호출 안 된 작업만<br>· 미확인 값(`PROCEDURE_WAITING` · `PROCEDURE_DONE` · `complete false` · WAITING 재호출)은 op 을 만들지 않거나 지원 안 함으로 드러낸다 — 조용히 건너뛰지 않는다<br>· 「지금 `SUPPORTED_WRITES`((api, 경로) 집합)를 이 단위를 담을 수 있게 바꾼다」<br>· A5 = 값 기준 단위 테스트 · phase · verification 에도 줄 | **닫힘** — 코드(`emr/kos/__init__.py:49` · L171)의 열기 단위 문제를 직접 짚었다 |
| W2 조각 계약 | #230 TD「화면 라우트」 — 조각 이름 · 넘기는 값 · SSE 이벤트 이름 · 오류 / `kos_failed` 토스트 조각 이름을 먼저 고정해 목록으로 남긴다<br>· **A9 신설**(Issue 코멘트 또는 코드 문서 · #231 이 의존 조건으로 인용)<br>· A3 「웹 라우트 테스트 = 최소 자리 템플릿 또는 렌더 컨텍스트」<br>· #231 TD「HTMX 연결」 · 의존 「#230 — 조각 계약 표(A9)」 | **닫힘** |
| W3 토스트 조각 주인 | 이름 고정은 **#230**(A9 표에 토스트 조각 이름 포함) · 렌더해 응답 / SSE 에 싣는 것도 #230<br>템플릿 두 개는 **#231** 이 #229 토스트 매크로로 만든다(#231 TD 새 줄 · phase · **A6 신설**)<br>#230 Non-Goal 「토스트 조각 템플릿 — #231 · #230 은 그 이름으로 렌더만」 | **닫힘** — 앞 검수 고칠 방향(#231 이 템플릿 · #230 이 이름 · 렌더)과 같다. 지시의 「주인 = #230」은 이름 · 렌더 계약의 주인으로 읽히고, 그 뜻으로 맞다 |
| W4 #229 의존 | #230 dependencies 에 「웹 기반 medikit HTMX(#229) — 웹 조립(web.py · Jinja2) · base · 토스트 매크로」 | **닫힘** |
| W5 직원 배열 | #230 TD「동기화」 — cc `[].id` 가정 매핑 · A1 「가정 fixture 로 시작 · A8 뒤 실물 fixture」 · A8 「수락 뒤 다음 조회의 `doctors` · `assignees` · `calledDoctors` 모양 확인 · OQ-12 직원 배열 부분을 닫음」 · Non-Goal 「OQ-12 의 직원 배열 부분은 A8」 | **닫힘** — TD1 ↔ Non-Goal 모순이 풀렸다(`procedureConfiguration` 은 그대로 HAR 뒤) |
| W7 자리만 요소 | #231 TD 새 줄 「E06 · E08 · E09 · E10 은 자리(모양)는 그리고 동작은 없다」 · Non-Goal 「…의 **동작**(자리 · 모양은 그린다)」 | **닫힘** — SPEC-002 L77 과 같고 A1 「넣음 요소 모두」와도 맞다 |

## 새 모순 · 발명

- **#230 ↔ #231 순서.** #230 은 #231 이 만들 토스트 조각 이름으로 렌더한다. 그런데 #231 은 #230 뒤다.
  - #230 A3 「최소 자리 템플릿 또는 렌더 컨텍스트」와 A9 「이름을 먼저 고정」 덕분에 #230 은 #231 없이도 확인할 수 있다. 순환은 아니다.
  - A7(`kos_failed` 한 번)의 테스트도 같은 자리 템플릿으로 하면 된다. 굳이 적자면 A7 에 「본문 = A9 의 토스트 조각 이름으로 렌더한 HTML」 한 마디를 더할 수 있다. 지적까지는 아니다.
- **W1 의 「아직 호출 안 된 작업만」.** 값 조건이 요청 본문이 아니라 작업 상태에 걸린다. 이것은 SPEC-002 L452(재호출로 같은 작업을 다시 부르는 것은 미확인 · OQ-09)를 그대로 옮긴 것이라 발명이 아니다. 재호출의 1 · 2단계(room · assignees)를 어떻게 할지는 W6(사용자 답) 범위라 이번에는 보지 않았다.
- SPEC-002 · 원천에 없는 동작 · 값은 새로 들어오지 않았다.

## 남은 것 (지시대로 열린 채)

- **W6**: HAR 미확인 동작 넷의 1차 처리. #230 open_question · Review Surface 와 #231 Review Surface 에 그대로 있다.
- **W8**: A8 수락 단계 — 수락할 원장 계정의 DAY 로그인.
- 사용자 답 뒤 contract v3 에서 다시 본다.
