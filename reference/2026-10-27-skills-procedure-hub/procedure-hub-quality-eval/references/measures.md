# 측정 4 · 목표 · 경로 — 상세

정본은 `orchestration/work/phub-recommend/quality-eval.py` 다. 여기는 읽는 법이다. 숫자는 그날 판 예시 — 지금 값은 `check_quality.py` · 리포트에서.

## 1. M1 질문 세트

### 1-1. 문항은 어디서 오나(`build_eval_set`)

- **샘플 상담 11단계**(`reference/2026-10-30-chatry-sample/S3p-Scenario.dc.html`) — 이마 주름 · 팔자 · 턱선 처짐 → 소프웨이브 · 사우나 · 필러 2cc · 조합 A(소프웨이브 + 팔자 필러 + 이마 보톡스) · 6주 전 보톡스 · 통증 민감
- **골드 조사의 의도 12**(`gold-research.json` — I-01 고민 → 추천 ~ I-12 가격)를 고르게. 가격(I-12)은 연결 층이라 문항 0
- **원천 브론즈의 칸**만 — problem-packages CC 추천 시술(사이트 「고민별 시술 추천」) · patient-education · complications · pre-procedure-checklist · treatment-sequence(minimum_intervals · incompatible_same_day) · procedure-profiles · procedure-comparison · problem-combos · products.json
- 문항 = 원천 · 샘플에 있는 말만. 가상 문장 없음

10-30 판: 111문항 — I-01 31 · I-07 16 · I-09 14 · I-02 10 · I-04 10 · I-03 7 · I-06 7 · I-11 6 · I-05 5 · I-10 4 · I-08 1.

### 1-2. 정답

- 정답 칸 = 원천 칸 그대로 — I-01 은 `families`(원천 CC procedures 의 category) · `sub_families`(원천 제품 이름 → 2단계 하위 — **규칙 칸**) · `site_words`(원천 문구 → 3단계 부위 이름 — **규칙 칸**) · `must_not` / I-02 ~ I-05 는 `must_show`(원문) / I-07 · I-08 은 `same_day` · `min_days` · `first` / I-09 는 `grade3` · `condition_text`
- 근거 = `evidence[]`(원천 파일 · 경로 · 원문)
- 근거가 없으면 `answer: null` · `answer_state` 「정답 미정」 — 채점 밖
- 원천끼리 갈리면 「정답 있음(원천 2갈래 · 의료진 확인)」 + 의료진 질문(`staff_questions`)

### 1-3. 채점

- 재현율 = 정답(계열 · 값) 중 허브가 낸 비율 · 정밀도 = 허브가 낸 것 중 원천 계열 · 부위 · 하위와 맞는 비율 · 문항 평균
- 「계열 옮김 결정」으로 맞는 것(원천 계열 M8 → 실버 N4 「서브시전」처럼 단계 결정이 계열을 옮긴 경우)은 맞음으로 센다 — 옮김 표는 2 · 5 · 7단계 결정 파일에서 읽는다(3차 ① · 처음엔 손 표였다)
- 안전 누락 = 문항에 나와야 할 안전 항목(금기 · 같은 날 불가 · 확인 조건 …)이 허브 응답 묶음에 없음
- 상태 = 맞음 · 틀림 · 정답 미정

### 1-4. 충돌 판(I-07 · I-08)

8단계에 충돌 해소 칸(`edges[].resolved` · `by_direction` · `options`)이 있으면 **해소 판**으로 잰다(앱이 실제로 읽는 값). raw 판(원문 주장 그대로)도 같이 재서 `boards` · 달라진 문항 `m1_raw_diff` 를 낸다. 같은 날 값이 방향에 따라 갈리면(「HA 필러 → RF/HIFU 같은 날 불가 · 역순 가능」) `by_direction` 을 읽어야 한다 — 1차 해소 판은 안 읽어 「정보 없음」으로 셌다(원인 O).

## 2. M2 말 → 노드 찾기

- 말 = 샘플 · taxonomy 시술 항목 · taxonomy 제품 · 고민 대분류 · 고민 갈래 · 시장가 · problem-packages CC · products.json · patient-education 환자용 이름 · 원장 이름(10-30 판 1,489)
- 변형 = 규칙으로 만든 것만(450): V0 띄어쓰기 붙임 · V1 처짐 → 쳐짐 · V2 영문 대문자 · V3 괄호 풀기 · V4 끝 「주사 · 시술」 떼기
- 찾기 = `semantic.json dictionary.resolve_rules` 그대로(완전 → 낱말 나눔 → 끝말 → 접두) — 측정이 자기 정규화를 따로 짜지 않는다(원인 M)
- 판정 = 찾음 · 후보 여럿(정답 포함) · 찾음(계열 옮김 결정) · 못 찾음 · 틀리게 찾음 · 판정 보류. 찾음 % = 앞 셋 합 / 판정 수

## 3. M3 엣지 표본

- 엣지 종류 21(시맨틱 `edge_kinds`)마다 고정 시드(20261030)로 20개(적으면 전부) — 10-30 판 374
- 표본마다 원천 레코드를 찾아 대조(`check_edge`) → 맞음 · 틀림 · 결정 근거
- 「결정 근거」 = 원천에 직접 근거가 없고 단계 결정으로 세운 것 — 오류율에 안 넣고 따로 센다(10-30 판 110)

## 4. M4 안전 누락

- 원천 → 실버 방향 전수 — 33 묶음(동의서 금기 · 응급 징후 · 필수 고지 · 사전 체크 6갈래 · 시술↔시술 금기 · 간격 · 같은 날 불가 · 순서 원칙 · 조합 규칙 · 연령대 피함 · 고민별 금기 조합 · 합병증 4 등급 · 타임라인 · PIH · 위험지대 · extracted safety · aftercare · taxonomy safety · procedure-profiles aftercare · practicalNotes)
- 원문 대조 = 공백 · 부호 무시 부분 문자열(실버 원문이 4자 미만이면 완전 같음 — 1차는 「간독성」을 다른 긴 문장의 부분으로만 찾다 있어도 없음으로 셈) · 구조 대조 = 8단계 `row_landing`(원천 행마다 주장 · 조건 · 피함 id 또는 「원문만(규칙)」)
- 안전 정보 0 단위 시술 = 모든 안전 칸이 gap 인 단위 시술 — 0 이 목표가 아니라 「정보 없음(gap)」 상태가 명시돼 있어야 한다(8단계 `unit_gaps` · 골드 G10 「없음 = 안전」 아님)

## 5. 목표 6 과 경로 셋

SKILL.md §2-2 · §2-3. 판정 함수 = `quality-eval.py goal_stats` · `goal_pass` · `GOALS`(지표 8) → 묶음 6.

## 6. 판 보관

| 판 | 폴더 | 무엇이 있나 | 그때 |
|---|---|---|---|
| v1 | `quality-v1/` | 문항 · 스크립트 · 리포트 · 입력 실버 · 1차 실버 × 2차 측정 대조(`v1-data-v2-eval.json`) | 1차 측정만(12:20) |
| v2 | `quality-v2/inputs/` | 리포트 · 스크립트 · 바뀐 실버(5 · 7 · 8 · 시맨틱) | 원인 14 고친 뒤(12:58) |
| v3 | `quality-v3/inputs/` | 리포트 · 문항 · 실버 | 골드 전 정리 뒤 · 다파장 ⑤ 넓힘 전(13:17) |
| 지금 | 작업 폴더 | 정본 | 다파장 ⑤ 넓힘 뒤 |

v1 리포트에는 목표 판정이 없다(목표가 1차 뒤에 정해짐) — 지금 리포트의 `v1_compare.goal` 이 1차 리포트를 목표 정의로 다시 센 값이다.
