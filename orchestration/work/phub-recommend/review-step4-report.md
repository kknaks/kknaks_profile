---
type: review
id: review-step4-report
title: "실버 4단계(기법) 검수"
target: step4-decisions.json · step4-apply.py · step4-techniques.json/.md · step4-source-fix.md · step4-fixtures/
basis: _RESUME §2 10-28 4단계 시작 · 반영(J1 안 1 · J2) · 해부학 용어 · source-map 승인
---

# PASS — open = 0 · FAIL 0 · WARN 2

기준은 지금 원천만(지도 4단계 칸 27). 설명 문장 · 가상 문장 · 미래 원천은 보지 않았다.

## 1. 노드 24 — PASS
- 큰 12(K01~K12) + 세부 12, 2층 넘지 않음(`step4-apply.py:103-106` 검사). 조사 `B_nodes` 24 와 id · 이름 · 상위 · 의학 용어 · 근거 전부 같음(차이 0) — J1 안 1 대로. `decided_by` S1~S3 (J1 안 1).
- 「근거 없는 노드」 open 0.

## 2. 칸 27 · 표현 181 — PASS (독립 재추출)
- 원천 `phub-stg-2026-10-26` 에서 `source-map.json` 4단계 칸 27 을 따로 짠 추출기로 다시 뽑음: 줄 215(taxonomy 68 · anatomy 52 · extracted 51 · profiles 25 · sequence 19). extracted ↔ taxonomy 글자 같은 줄 51 → 중복 묶음 17행. 남은 164 줄 (파일, 원문) 다중집합이 산출 표현 행과 **양쪽 차이 0**. 164 + 17 = 181.
- 행선지: 결정 164 행 ↔ 조사 `C_expressions` 181 대조 — verdict · destination · basis · note 차이 0. 차이 21건은 형식 변환뿐(근육 `{key,site}` → `{muscle,sites[]}` 11 · `attach_to` 문자열 → `attach[]` 9 — 값 일치 확인 · 코 `constraint_text` 1 = J2 반영).
- 묶음 셈: 속성 64 · 넘김 59 · 노드로 41 · 중복 17. 넘김 2단계 21 · 5 · 7 · 8 · 계열 밖 · 시맨틱 행선지 샘플 확인 — 「이미 정본」 · 단계 경계(U1) 대로.

## 3. 속성 · safe_layers · 계열 · 넘김 · 초안 — PASS
- 값 사전: 층 13 · 펄스 3 · 박피 2 · 도구 3 · 박피 깊이 3 · 방식 1 · 대상 근육 17(조사 16 + H15 「표정근」 = Musculi faciei @ 얼굴, _RESUME 3단계 넘김 행대로).
- **safe_layers 코**: `코(묶음)` = 골막상 · 연골막상(원문) · **콧등 = 골막상 · 코끝 = 연골막상**(`site_layer_split` · 원문 「골막상 (코뼈 부위) 또는 연골막상 (비첨부)」) — J2 대로. 결정 J2 문구 = 「HA 필러 · 코 · 주입」(조사 추천 「골막상 주입」에서 층을 뺀 이유 `user_decisions` note 에 있음) · DEC-002 는 고치지 않고 `step4-source-fix.md` DEC 문구 1줄(코디 → writer) — 결정대로.
- 계열 기본 18 = step2 계열 18 전부(누락 0) · 조사 `E_family_defaults` 와 값 같음(also 를 id 로만 줄인 형식 차이).
- 넘겨받은 것 15 = 조사 14 + H15. step3 deferred · 부위+다른 축 · handoff_note(사각턱 · 목 · 승모근 · 종아리 · 턱선) · step2 M8/M4 deferred 전수 행선지 있음(apply §5 역검사 open 0). 대상 근육 · 주입 지표가 3단계 부위 안.
- technique_hint 25 = step2 원천 hint 25 와 글자 같음 · 조사와 같음(ablative 객체화 형식 차이 · 아래 W1 제외).
- 초안 65 = 유지 4 · 합침 29 · 버림 32, 조사와 같음 · 이름 원천 일치.

## 4. open · 결정론 · 구조 · 미수정 — PASS
- `python3 step4-apply.py --out <임시>` 두 번 → 셋 산출 모두 바이트 같고 커밋본과도 같음. open 0 · stale 0.
- 고정 시험(사본 폴더에서 실행) 10/10 PASS, `result.json` 커밋본과 같음.
- 결정은 전부 `step4-decisions.json`, 스크립트에 셈 assert 없음.
- step1~3 산출 · DEC-001~003 · source-map · 원천(10-26) mtime 이 4단계 조사(18:13)보다 앞 — 고치지 않음.

## WARN
- **W1** 셀렉V(`auto-M8-1775364106103`) — 조사에 있던 구조 칸 `pulse_scope: "보조 하위 계열 엔디야그 레이저"`(`step4-research.json:3413`)가 결정 · 산출에서 빠지고 note 문장에만 남음. 5단계에서 Q스위치가 주 매질 IPL 에 붙는 것으로 읽힐 수 있음 → `pulse_scope` 칸을 결정에 되살리기 권고.
- **W2** md 셈 줄에 고정 숫자가 있음 — `step4-apply.py:372` 「조사 16 + 3단계 넘김 1」 · `:374` 「조사 14 + 브리프 추가 1」. assert 는 아니지만 결정이 바뀌어도 그대로 남음(파일 머리 「숫자는 이 파일에 적지 않는다」와 어긋남). 결정 파일 셈에서 내거나 문구를 빼기 권고.
