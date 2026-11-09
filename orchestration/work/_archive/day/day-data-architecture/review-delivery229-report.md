# 리뷰 리포트 — day-data-architecture / doc · Delivery #229 웹 기반 · medikit HTMX (2026-11-06)

대상
- Issue MediSolveAIDev/CENTURION_DAY#229(updatedAt 2026-11-06T01:49Z · 코멘트 0)
- `delivery/v2-web-kit.json`(contract v1) · plan · apply
- 작성 지시 `planner-delivery-webkit-instructions.md` · 작성 리포트 `planner-delivery-webkit-report.md`

기준
- 지시서 「사용자 결정」 3개
- CENTURION_DAY `origin/v2-dev:AGENTS.md` 「웹 화면」 · 저장소 구조
- DS 조사 `frontend-ds-research-report.md`(E01 ~ E56 판정 · G1 ~ G17)
- SPEC-002 화면 구성 절(L76-86) · U-4
- 원천 `procedure-board-decisions.md` 「화면 참고 — 의사 호출 창」

## 판정: WARN

FAIL 은 없다. 다음은 모두 맞다.
- 사용자 결정 3개가 계약에 들어갔다.
- 「하지 않는 것」(화면 · API · 키트 수정)이 들어갔다.
- 위험 L2 · 승인 대기 상태다.
- 의사 호출 모달(A8)이 원천 모양과 맞는다.

다만 **「시술 현황은 이 매크로만으로 조립한다」는 사용자 결정이 성립하려면 빠진 매크로가 있다**(W1). CSRF `hx-headers` 를 실제로 잇는 일을 맡은 Delivery 가 없다(W2). 그 밖은 작은 정리다(W3 ~ W6).

## 1. 사용자 결정 3개

| 결정 | 계약 | 판정 |
|---|---|---|
| 화면보다 medikit HTMX 기반 먼저 · 시술 현황은 그 매크로만으로 | Target Delta 1 · Non-Goal 「시술 현황 화면 — 다음 Delivery 가 이 매크로로 조립」 | 담김(단 W1) |
| 새 컴포넌트는 DAY 레포 안 · 키트는 가져다 쓰기만 · 「키트로 올릴 후보」 목록 | Target Delta 2 · 8 · A5 · Non-Goal 「키트 수정」 | 담김 |
| CRM 브랜드색 · 고객 상태 팔레트 = DAY 토큰 파일에서 medikit 토큰 확장 | Target Delta 5 · phase 2 | 담김 |

## 2. SPEC-002 화면 구성 E 번호 ↔ 계약 매크로 — 전수 대조

- 판정 칸은 DS 조사 요소 표에서 가져왔다(○ 있음 · △ 비슷 · ✗ 없음 · ― 조합).
- 「계약」 칸은 Target Delta 4(ui.html 매크로) · 3(base.html) · 5(토큰)에서 찾은 자리다.
- **빠짐** = SPEC-002 1차가 넣는데 계약 매크로 목록에 없고, DS 조사가 △ 로 「차이가 있다」고 한 것이다. 이대로면 다음 Delivery 가 손 CSS 를 쓰거나 이 Delivery 를 다시 열어야 한다.

| SPEC-002 1차 요소 | DS 판정 | 계약 | 결과 |
|---|---|---|---|
| E01 · E02 · E03 셸 | ✗ G1 · △ | base.html G1 | 있음 |
| E04 병원 이름 | ― 조합 | — | 매크로 불필요 |
| E05 헤더 탭 · E16 인박스 탭 | △ → G2 | G2 | 있음 |
| E06 헤더 고객 검색(28h) | △ 28 높이 없음 | — | **빠짐**(자리만이라도 그려야 한다 — SPEC-002 「자리만」) |
| E07 페이지 머리 | △ Divider + typo 조합 | — | 조합으로 가능 · 대응표에만 적으면 된다 |
| E08 날짜 이동(꺼짐) | △ | — | 조합(글자만) |
| E09 [필터] 28×28 아이콘 버튼 + 툴팁 | △ 정사각 아이콘 버튼 프리셋 없음 | — | **빠짐** |
| E10 세그먼트 | ✗ G2 | G2 | 있음 |
| E11 툴팁 | HTMX ✗ G3 | G3 | 있음 |
| E12 토스트(+ SSE `kos_failed` 토스트 조각 — SPEC-002 개정 ④) | HTMX ✗ | 토스트 | 있음 |
| E13 포커스 · E14 스크롤바 | ○ · △ 값 다름 | — | E14 는 토큰으로(W5) |
| E15 · E19 · E20 · E21 · E37 · E38 · E31 레이아웃 | ― 조합 | — | 매크로 불필요(E31 바탕색은 §4 토큰 → Target Delta 5) |
| E17 접는 칸 | HTMX ✗ G4 | G4 아코디언 | 있음 |
| E18 · E28 · E32 · E33 밀집 카드 | ✗ G5 | G5 | 있음 |
| E22 · E23 · E42 | ○ | 기존 btn · checkbox | 있음 |
| E24 · E36 사각 배지 · 칩 버튼 | ✗ G6 | G6 | 있음 |
| E25 시술 완료 검색(+ 지우기 X) | HTMX △ | 기존 input_box | **빠짐(작음)** — X 버튼 변형 |
| E26 찾은 글자 | ✗ G7 | G7 | 있음 |
| E27 빈 상태(제목 + [조건 지우기]) | △ Figma EmptyState | — | **빠짐** |
| E29 · E30 · E35 아이콘 | ✗ G8 · △ | G8 | 있음 |
| E34 손잡이 · D&D | ✗ G9 | G9 | 있음 |
| E39 오더 메모 | ✗ G10 | G10 | 있음 |
| E40 전체 선택(혼합) | △ → G11 | G11 | 있음 |
| E41 · E45 시술 행 · 더보기 | ✗ G12 | G12 | 있음 |
| E43 · E20 · E24 · E36 실시간 경과 | ✗ G13 | G13 · day.js | 있음 |
| E44 줄 버튼 24h | △ 24 높이 없음 | — | **빠짐** — 버튼 크기 변형(G12 안에 넣을지 대응표에 적어야 함) |
| E46 하단 액션 바 | ✗ G14 | G14 | 있음 |
| E50 더보기 메뉴 · E51 수락 모드 팝오버 | HTMX ✗ G16 | G16 | 있음 |
| E51 호출 · 재호출 = 의사 호출 창(모달) | 원천 「화면 참고」 | 의사 호출 모달 · A8 | 있음 — A8 문구가 원천 L41-47 · SPEC-002 U-4 와 같다 |
| E52 의사 아바타 | ✗ G17 | G17 | 있음 |
| E55 차트 모달(읽기 전용 · 410 · 모서리 14) | △ ms-modal 변형 | Non-Goal 에 「1차는 읽기 전용 표시만 매크로로」라고만 있다 · Target Delta 에는 없음 | **빠짐** — Non-Goal 이 「만든다」고 말하는데 목록에 없는 모순 |
| E56 차트 글 칸 | HTMX △(키트에 textarea 클래스 없음) | — | **빠짐** — 읽기 전용이라도 틀 클래스가 없다 |
| 수납 필요 | 시안에 없음 | 「수납 필요」 표시 자리 | 있음 |
| E49 빈 방 · E33 방 이름 버튼 · E47 · E48 · E53 · E54 | — | A4 「안 만듦」에 **E47 · E48 · E53 · E54 만** | E49 · E33 방 이름 버튼(방 옮기기)도 「안 만듦」에 넣어야 한다(SPEC-002 L80) |

참고: 콤보박스 목록(HTMX 에 없는 6개 중 하나)은 1차에 쓰는 곳이 E53(방 옮기기 — 범위 밖)뿐이다. 사용자 결정 · 지시서가 6개를 다 만들라 했으니 문제는 아니고, 대응표에 「1차 사용처 없음」으로 적으면 된다.

## WARN

### W1. 시술 현황이 쓸 매크로 일곱 개가 계약 목록에 없다
- 빠진 것: E06 검색 28h · E09 정사각 아이콘 버튼 · E25 지우기 X · E27 빈 상태 · E44 24h 줄 버튼 · E55 차트 모달(읽기) · E56 글 칸(위 표).
- 사용자 결정은 「시술 현황 화면은 그 매크로만으로 조립한다」이고, A2 는 손 CSS 0 이다. 이대로면 다음 Delivery 가 이 요소들에서 막힌다. E55 는 계약 Non-Goal(「1차는 읽기 전용 표시만 매크로로」)이 만든다고 말하면서 Target Delta 에는 없어 계약 안에서도 어긋난다.
- 고칠 방향: Target Delta 4 매크로 목록에 이 일곱을 더한다. 기존 매크로의 크기 · 변형으로 처리해도 된다. A4 대응표에 「SPEC-002 1차 요소 전부 → 매크로 또는 조합」을 요구해 빠짐을 기계적으로 막는다. A4 「안 만듦」에 E49 · E33 방 이름 버튼도 더한다.

### W2. CSRF `hx-headers` 를 실제로 잇는 Delivery 가 없다
- #229: base.html 에 「CSRF 를 실을 hx-headers 자리」만 둔다. Review Surface 「#227 이 PR #228 에 들어온 뒤. 그 전엔 자리만」. Acceptance 에 CSRF 가 없다.
- #227 v3: code_surface 가 `routers/api` · `services` · `session.py` · `emr/kos` · `tests` · `migrations` 다. **templates 가 없다**. A7 은 API 수준(헤더가 없거나 틀리면 403)만 본다.
- 기준: SPEC-001 「CSRF (웹)」 「웹 화면(`base.html`)이 `hx-headers` 로 모든 HTMX 요청에 `X-CSRF-Token` 을 싣는다」.
- 그래서 「base.html 이 세션의 `csrf_token` 을 실제로 싣는다」는 두 Delivery 어디에도 완료 조건으로 없다. 서로 상대가 한다고 여길 자리다.
- 고칠 방향: 하나를 고른다.
  - ① #229 에 「#227 머지 뒤 base.html 이 `login_session.csrf_token` 을 `hx-headers` 로 싣는다 · 견본에서 POST 1건이 403 없이 통과」 Acceptance 와 마지막 phase 를 넣는다.
  - ② 시술 현황 화면 Delivery 의 첫 일로 넘긴다고 #229 Non-Goal 에 명시한다.
- 어느 쪽이든 순서는 #227 → 연결이다.

### W3. htmx SSE 확장 파일을 누가 벤더링하는지 없다
- system.md 「화면 실시간 갱신 — SSE · HTMX 는 SSE 확장」 · SPEC-002 SSE 계약(`hx-trigger="sse:board"`) · 개정 ④(`sse-swap` 토스트).
- #229 는 `htmx.min.js` 벤더링만 적었고, SSE 연결은 Non-Goal 이다. CDN 금지(AGENTS.md)이므로 확장 파일과 라이선스도 저장소에 들어와야 한다.
- 고칠 방향: 벤더링 목록에 SSE 확장 + 라이선스를 넣거나, 화면 Delivery 몫이라고 Non-Goal 에 적는다. 같은 자리에 두는 쪽이 자연스럽다(A6 에 한 줄).

### W4. 「토큰 확장 방식」 open question 은 레포 규칙에 답이 있다
- AGENTS.md 저장소 구조: `styles/ app.css · medikit-preset.json · tailwind.config.mjs · build.mjs` · `static/ … 빌드된 css` · 「웹 화면」 「빌드된 CSS 는 커밋하고 손으로 고치지 않는다」. DAY 레포는 **빌드 방식**을 정해 두었다. 키트 README 의 「빌드 없음」은 centurion admin 의 사정이다.
- 고칠 방향: open_question 을 「AGENTS.md 대로 빌드(tailwind preset + 토큰 확장)」로 닫거나, 사용자에게 묻더라도 레포 규칙이 그 답이라는 점을 같이 적는다.
- 빌드 방식이면 A2 의 grep 에 **tailwind 임의값 클래스(`[…]` 안의 색 · 치수)** 를 넣어야 한다. `style=` 만 보면 손 CSS 가 클래스 모양으로 빠져나간다.

### W5. A2 · A3 grep 범위가 좁다
- A3: `<script>` 본문 · `on*` 속성 · eval 만 본다. htmx `hx-on` / `hx-on:*` 도 인라인 스크립트다. 넣는다(`allowEval:false` 면 동작도 안 한다).
- A2: 템플릿 · 매크로만 본다. E14 스크롤바 값 같은 시안 값은 DAY 토큰 파일에서만 정해야 한다. 「새 값은 토큰 파일에만」으로 범위를 적는다.

### W6. A1 의 「상태별」을 무엇과 맞춰 보는지 없다
- A1 「DS 조사 요소 표의 상태」는 맞지만, 견본이 그 상태를 다 그렸는지 대조할 목록이 없다.
- 고칠 방향: A4 대응표에 「매크로 · E/G 번호 · 그린 상태」 칸을 둬서 A1 · A7(스크린샷)과 맞춰 볼 수 있게 한다.

## 3. 하지 않는 것

Non-Goals 는 다음과 같다. 지시서 「하지 않는 것」 다섯(시술 현황 화면 · 업무 라우터 · API · 로그인 화면 · 앱 · 키트 수정)을 모두 담았다. 더한 것은 SPEC-002 · 원천의 범위 밖과 맞다.
- 시술 현황 화면 · 업무 라우터 · API · 서비스 · SSE 연결
- 로그인 화면 · Flutter 앱
- centurion 키트 수정
- 방 옮기기 · 연결(G15 · U5)
- 차트 작성(U11)
- prod 배포

모순 하나는 W1(E55)이다.

## 4. Acceptance — 확인 가능한가

| A | 확인 방법 | 판정 |
|---|---|---|
| A1 견본 · 상태별 · dev 200 / prod 404 | 라우트 테스트 + 스크린샷 | 가능 — 상태 목록은 W6 |
| A2 손 CSS 0 | architecture grep 테스트 | 가능 — 범위는 W4 · W5 |
| A3 인라인 스크립트 0 | grep 테스트 | 가능 — `hx-on` 은 W5 |
| A4 대응표 | 파일 확인 | 가능 — 전수 요구는 W1 |
| A5 키트 후보 목록 | 파일 확인 | 가능 |
| A6 벤더링 · 라이선스 · config | 파일 · 값 확인 | 가능 — SSE 확장은 W3 |
| A7 브라우저 스크린샷 1280×720 이상 | 파일 | 가능(실물 조건 충족) |
| A8 의사 호출 모달 원천 모양 | 견본 스크린샷 ↔ 원천 L41-47 | 가능 |

## 5. #227 CSRF 의존 순서

- dependencies 에 「로그인 Delivery(#227) — CSRF hx-headers 연결은 그 뒤」가 있고, Review Surface 에 「그 전엔 자리만」이 있다. 순서 자체는 맞다.
- 다만 연결을 맡은 쪽이 없다 → W2.
- #224 뼈대에 `web.py` 가 없다는 것(작성 리포트 확인)을 이 Delivery 가 맡는다고 code_surface 에 넣은 것도 맞다.

## 6. 위험 · 승인

- 메타는 `risk_level=L2` · `contract_version=1` · target DAY-SPEC-002(pending)이다.
- 라벨은 `delivery-plan:review` · `execution-plan:ready` · `spec-baseline:pending` — **승인 라벨 없음** · 코멘트 0.
- L2 근거(공통 모양 계약 · migration · 외부 write · 인증 변경 없음)도 맞다.
- 다만 W2 에서 ①(이 Delivery 가 CSRF 연결)을 고르면 인증 경로를 건드리게 된다. 등급을 다시 보는 것은 코디 판단이다.

## 고칠 방향 요약

1. 매크로 목록에 E06 · E09 · E25 · E27 · E44 · E55 · E56 을 더하고, A4 대응표를 「SPEC-002 1차 요소 전부」로 바꾼다. 「안 만듦」에 E49 · E33 버튼을 더한다(W1).
2. CSRF `hx-headers` 연결 담당을 정한다 — #229 마지막 phase 또는 화면 Delivery Non-Goal 명시(W2).
3. SSE 확장 벤더링 담당(W3).
4. 빌드 방식 open question 을 AGENTS.md 로 닫는 것을 검토한다. A2 grep 에 tailwind 임의값을 넣는다(W4).
5. A3 에 `hx-on`, A2 범위에 「새 값은 토큰 파일에만」을 넣는다(W5). 대응표에 「그린 상태」 칸을 둔다(W6).
