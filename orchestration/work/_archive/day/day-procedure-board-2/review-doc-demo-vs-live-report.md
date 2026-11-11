# 리뷰 리포트 — day-procedure-board-2 / doc — 데모/운영 KOS 쓰기 구분 · dev is_demo 거르기 없앤 SPEC 개정 (2026-11-09)

- reviewer_doc · task_c851ea896a5f · read-only (리포 수정 · 커밋 · KOS 호출 없음)
- 대상: `mediness-mediness/day-procedure-board-2-spec` 워크트리 미커밋 diff 8파일(`products/day/` — 20-spec.md · spec-000 · spec-001 · spec-002 · 40-architecture/system · deployment · mobile-deployment · log.md). base `b4cd1a00`
- 근거: 사용자 결정 `_RESUME.md:35,39`(2026-11-09) · 조사 리포트 `research-demo-vs-live-report.md` §1~§5 · planner 리포트 · 원천 `procedure-board-decisions.md:117-119` · HAR 직접 확인(아래)

## 판정: WARN

FAIL 0 · WARN 3. 스펙에 닿는 자리는 빠짐없이 고쳐졌고, 환경 · 연결 종류로 가르는 문장은 남지 않았다. 확인 안 된 4개 쓰기는 「확인 안 됨」 그대로다. lint는 products/day/ 기준 ERROR 0 · WARN 0이다. WARN 3건은 모두 머지 전에 손볼 작은 것이다.

## FAIL

없음.

## WARN

- **W1 — 출처 없는 「오전」** · `products/day/20-spec/spec-002-procedure-board.md:533`(시작 취소 행 끝) 「~~시작 취소는 KOS 에 쓰지 않는다~~(사용자 2026-11-09 **오전** → 같은 날 뒤집음 …)」
  근거: 원천 `procedure-board-decisions.md:117`, `_RESUME.md:35`에는 날짜(2026-11-09)만 있고 시각은 없다. 사실 기록에 원천에 없는 시각을 넣었다. 「(사용자 2026-11-09 → 같은 날 뒤집음 …)」로 「오전」을 빼면 된다.
- **W2 — log.md 새 3행의 PR 칸** · `products/day/log.md:17-19` 「PR 미정 — 근거 `…research-demo-vs-live-report.md`」 · 「〃」
  근거: `rules/document-pipeline.md` §log.md 「PR 컬럼 — `#NNN` 또는 근거가 있는 실제 링크 … 모호한 단어 단독 금지」. 경로는 다른 레포의 파일이라 링크로 열리지 않는다. 코디가 PR을 올릴 때 `#NNN`으로 바꿔야 한다(planner도 같은 주의를 남겼다).
- **W3 — Delivery 초안 D4에 테스트 1곳 누락** · planner 리포트 D4 「바뀜(가)」
  근거: 조사 §3 `test_board_api.py:370-`(`test_재호출은_KOS_호출을_다시_보내고_앞_호출은_닫힘` — 데모 연결 전제)이 D4 목록에 없다. 픽스처의 `is_demo=` 인자를 빼면 같이 손봐야 하는 자리일 수 있으니 D4에 「데모 전제 제거 · 확인」으로 한 줄 더한다. 나머지 §3 테스트 15곳은 모두 D4에 있다.

## 단계별 확인 (브리프 §6)

### 1. 빠진 자리 — PASS
`products/day/`에서 `is_demo · demo · 데모 · trial · TRIAL · ON_LIVE · not_supported · APP_ENV · 열지 않`을 다시 grep했다(log.md 이력 행 제외). 남은 것은 모두 그대로 두어도 된다.

| 남은 자리 | 판정 |
|---|---|
| spec-000:217,223 · spec-001:306,339 · spec-002:34,38,533,631,632 · system:182 · deployment:32,76 · mobile:34,287 — `is_demo` · `KOS_TRIAL…` · 「운영에 열지 않음」 | 취소선 · 뒤집힘 기록만. 살아 있는 규칙 아님 |
| spec-000:205-214 「환경 — 데모 테넌트와 DAY 서버」 · 키 표 | KOS 호스트 사실. 연결 갈림 아님 |
| spec-000:377,849,1163-1357 「데모 지점 조회 · 데모 15/101/323 …」 | 데이터 출처 표기. 갈림 아님 |
| spec-002:350-362 권한 이름 표(데모 지점 직무 이름) | 조사 #23 (다). 플래그 분기 아님 — planner가 범위 밖으로 둔 것에 동의 |
| spec-001:137,156,244,335 `mfa_not_supported` | 2단계 인증 오탐 |
| deployment:48,51,132,133,153 · mobile:55,56,227 `APP_ENV=dev/prod` | 서버 이름 · 스키마 짝. 153행 비고는 「연결을 거르지 않는다」로 바뀜 |
| deployment:19,194 · mobile:154,259 「데모 KOS 동기화 · 데모 연결 계정 · dev 서버(KOS 데모)」 | dev 스키마의 실제 데이터 사실. 갈림 아님 |
| spec-002:521,529,535-537,644 「데모 실물로 확인」 | 확인 방법(OQ-23). 보낼지 말지를 가르지 않음 |

조사 §4의 절은 모두 반영됐다: SPEC-000 `crm_connection` 표(`is_demo` 행 삭제) · 「환경」 / SPEC-001 개정 ⑥ · U-2(:77) · Flow 4(:155) · 매트릭스(:242) · 시퀀스(:269) · 규칙 5(:306) · OQ-10(:339) / SPEC-002 개정 ⑤⑥⑦ 주석 · ⑫ 신설 · U-9(:166) · KOS 쓰기 표(:521-537) · 규칙 13·14·17(:580,581,584) · OQ-08~10(:631-632) / system:182-183 · deployment:32,76,153, 159행 삭제, 195행 추가 · mobile:34,60-61,229,287.
S-5 · S-6 · 상태 그림은 처음부터 데모/운영 문구가 없어 그대로 둔 것이 맞다(spec-002:219-228 · :290-300 확인). `erd.md` · `30-work.md` · `10-decision.md` · `00-baseline` · `21-*`에는 키워드가 0건이다.

### 2. 새 갈림 금지 — PASS
환경 · 연결 종류로 동작을 가르는 문장은 새로 생기지 않았고 남은 것도 없다. 「dev 는 데모 병원만 나온다」(spec-001:77)와 「prod 스키마 = 실제 병원 연결만」(mobile:229)은 데이터에서 따라 나오는 결과이고 코드 규칙이 아니다. `_RESUME.md:39`의 사용자 결정과 맞는다. 「시작 취소 — 고객 진행 그대로: DAY 만」(spec-002:534)은 고객 단계에 따른 갈림이라 이번 범위와 무관하고 base 그대로다.

### 3. 사실 — PASS (W1 제외)
- 확인 안 된 4개(재호출 재전송 · `complete=false` · `cancel-flow-tasks` · `PROCEDURE_DONE`)는 모두 「확인 안 됨 → OQ-23」이다(spec-002:529,535,536,537). 「확인됨」으로 바뀐 곳은 없다.
- 시작 취소 「확인됨」(spec-002:533)은 **HAR를 직접 대조했다**(`git/toy_pr2/kknaks_profile/reference/2026-10-23-cc-overall-board/har/방배정.har`). 내부 `schedule/v1/commands/change-flow-step` · 칸 `id, step` · `PROCEDURE_WAITING` · 200 — 표의 경로 · 칸 · 값과 같다. 데모 실물 확인은 `_RESUME.md:35`(사용자)가 근거다. 「HAR 없음 · 내부 경로 미확인」을 바로잡은 표기가 맞다.
- 귀가 `COMPLETED`(spec-002:537 · OQ-22)도 직접 대조했다: `귀가.har` 같은 경로 · `id, step` · `COMPLETED` · 200 — 맞다.
- KOS 경로 · 값은 base 표에 있던 것만 썼다. 새로 지어낸 경로 · 값 · 화면 문구는 없다. 화면 · API 계약(경로 · 응답 · 오류 코드 · 매트릭스 행)은 바뀌지 않았다 — SPEC-001 매트릭스는 비고 괄호만 지웠다(코드 · HTTP 그대로).

### 4. 뒤집힌 결정 기록 — PASS
`log.md:17` decision-add에 세 건이 취소선과 사유로 있다: ~~2026-11-06 W6~~(개정 ⑥이 이미 바꿨고 「운영에 안 엶」도 없앰) · ~~2026-11-03 `APP_ENV=dev` 는 `is_demo` 만~~ · ~~2026-11-09 시작 취소 KOS 안 씀~~. 본문에도 같은 취소선이 있다(spec-000:223 · spec-001:306,339 · spec-002:34,533,580 · system:182 · deployment:76 · mobile:34,287). 요약의 깊이는 결정 entry 규약(무엇 · 왜 · 대안)에 맞는다. 10-decision 무변경 · WP 미생성은 코디 지시(§6.2 · §6.3 변경)와 레포 규칙(ESC 아님 · 신규 WP 금지)에 맞는다.

### 5. planner 판단 — PASS
- **D2 #17~#20 남김** — 동의. `/dev/kit*` · `/docs` · `APP_ENV` 필수와 스키마 짝 · 로컬 기본 dev는 서버 기능 노출과 배포 안전장치다. 연결을 거르지 않고, 사용자 결정(「연결 데이터로 분리 · 같은 코드로 같게 동작」)이 겨냥한 「연결 거르기」가 아니다. 다만 브리프가 「(나) 8자리」라고 했으므로 코디가 확인하는 편이 좋다(planner도 같은 표시를 남겼다).
- **SPEC-000 `is_demo` 칸 삭제** — 맞다. 쓰던 곳은 (가)와 (나) 둘뿐이고(조사 #1-#16), 둘 다 없어졌다. 칸이 남을 근거는 원천에 없다(brief §2.3 「근거 없으면 지우는 쪽」).
- **OQ-01-2**(실제 병원 연결을 넣는 방법)는 조사 #21 · F6, **OQ-01-3**(운영 테넌트의 「같은 API」 확인)은 F7과 deployment 미결에 근거가 있다. 둘 다 열린 채로 둔 것이 맞다.
- **OQ-22**(`COMPLETED` ↔ `PROCEDURE_DONE`)는 brief §2 지시대로 판단하지 않고 열린 채로 뒀고, **OQ-23**(4개 실물 확인)은 F4에 근거가 있다. 둘 다 맞다.
- 참고: spec-002 머리 개정 순서가 ①…⑦ 다음 ⑫, 그 뒤 ⑪⑩⑨⑧(:40-48)이다. 원래부터 ⑧~⑪이 역순이었던 자리에 ⑫를 ⑦ 바로 뒤에 넣은 것이라 기존 관례 안이다. 기능 영향은 없다.

### 6. Delivery 초안 D1~D5 덮음 — PASS (W3 제외)
- 조사 §1: #1~#12 → D1(#6은 D3로), #13~#16 → D2, #17~#20 → 남김(위 5), #21 → D3, #22 · #23 → 남김. 23자리가 모두 덮였다.
- 코드 레포(`CENTURION_DAY/day-procedure-board-2` @91728737)를 다시 grep했다(`is_demo|trial_writes|TRIAL_WRITES|demo connections only`, 소스 파일 26개). 모두 D1~D4 범위다. `seed_demo_board.py:115,267`은 함수 이름 `check_open_key_is_demo`라 오탐이다. `AGENTS.md:163`은 시드 안내 줄이라 손댈 필요가 없다. `docs/development/deployment.md:114`는 D1에 있다.
- 조사 §3: 테스트 16곳 중 15곳이 D4에 있다(누락 1 → W3). F8(남은 pending)은 D1, F9는 D4가 맡는다. D5(데모 실물 확인 → OQ-22 · OQ-23 닫기)는 brief §2 「코드 뒤 QA」와 맞는다.

### 7. lint — PASS
`python3 scripts/lint-pipeline.py --strict` → exit 0 · **0 error** · 263 warning. **products/day/는 ERROR 0 · WARN 0이다.** 경고는 모두 타 제품(selly 등의 frontmatter · doc_no 누락)이라 무관하다.

## 직원이 실물에서 만날 자리

- 이번 개정으로 운영 병원 연결에서도 확인 안 된 4개 쓰기가 나간다. 데모 실물 확인(D5 · OQ-23) 전에 prod에 실제 병원 연결을 넣으면, 「완료 취소」 · [귀가 대기] · 재호출이 KOS에서 거절되거나 다른 값이 될 수 있다. 실패는 실패 토스트로 보인다(OQ-07). prod는 아직 배포되지 않았고 연결을 넣는 방법도 미정이라(OQ-01-2) 당장의 위험은 없다. 순서만 지키면 된다: D5 → prod 연결.
- [귀가 대기] 2의 `PROCEDURE_DONE` ↔ KOS 웹 「귀가」 `COMPLETED`(OQ-22) — 데스크가 KOS 화면에서 보는 단계 이름이 DAY 쪽과 다를 수 있다. D5에서 확인한다.

## 참고(기존 부채)

- spec-002 머리 개정 번호 순서가 섞여 있다(⑧~⑪ 역순 · 이번 ⑫는 ⑦ 뒤). base부터 그랬다.
- 조사 리포트가 적은 HAR 경로(`kknaks_profile/reference/2026-10-23-cc-overall-board/har/`)는 이 머신에서 `git/toy_pr2/kknaks_profile/…`에만 있다(planner가 「재확인 못 함」이라 한 이유). 이번 리뷰에서 그 사본으로 대조했다.
