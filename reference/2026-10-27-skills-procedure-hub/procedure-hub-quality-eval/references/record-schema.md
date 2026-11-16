# 칸 — 문항 파일 · 리포트 · 점검 출력 · 기준

## 1. `quality-eval-set.json`

| 칸 | 무엇 |
|---|---|
| `version` · `generated_by` · `rule` · `intents[]` · `n` | 문항 세트 머리 — 「문항 = 샘플(S3p 11단계) · 원천 브론즈에 있는 말만 · 정답은 원천 칸 근거(없으면 「정답 미정」) · 가상 문장 없음」 |
| `questions[]` | `id`(Q001~) · `intent`(I-01~) · `origin`(샘플 N단계 · 원천 파일) · `text` · `slots{concern_text · site · cc · cc_group · cc_detail · procedure · procedures · prior · …}` · `answer{…}` 또는 null · `answer_state` · `evidence[{file, path, text}]` |
| `answer` 칸 | I-01 `families` · `sub_families`(규칙) · `site_words`(규칙) · `must_not` · `site` / I-02~05 `families` · `must_show` / I-06 `families_each` / I-07 · 08 `same_day` · `min_days` · `first` · `ok` / I-09 `grade3` · `condition_text` · `condition_present` / I-10 `text` · `note` / I-11 `n_packages` |

문항 한 줄 예(I-01 · 원천 CC):

```json
{"id": "Q019", "intent": "I-01", "origin": "원천 problem-packages(사이트 고민별 시술 추천)", "text": "홍조/혈관 · 엑셀V",
 "slots": {"concern_text": "홍조/혈관", "cc": "엑셀V", "cc_group": "모세혈관확장", "cc_detail": "532+1064nm"},
 "answer": {"families": ["M4", "M8"], "sub_families": {"M4": ["폴리뉴클레오타이드(PN·PDRN)"], "M8": ["KTP", "엔디야그 레이저"]},
            "site_words": [], "must_not": "다른 부위 · 다른 영역 단위 시술"},
 "answer_state": "정답 있음", "evidence": [{"file": "problem-packages.json", "path": "problems[P8].complaints[3]", "text": "엑셀V [모세혈관확장] → 혈관레이저(M8, 혈관 수축/파괴) · 스킨부스터(M4, 피부 장벽 강화)"}]}
```

(`sub_families.M8` 의 「KTP」는 10-30 다파장 규칙으로 더해진 규칙 칸 — 1차는 엔디야그만)

## 2. `quality-report.json`

| 칸 | 무엇 |
|---|---|
| `version` · `seed` · `per_kind` · `inputs_sha256{파일: sha 앞 16}` | 판 · 입력 지문 |
| `goal_excluded[]` | 목표 계산에서 뺀 문항(1차 의료진 질문 — 고정) |
| `headline.M1 · M2 · M3 · M4` | 측정별 머리 지표(전 문항 기준 — 목표 계산과 문항 범위가 다르다) |
| `headline.goal.{cc · nocc · v1}` | 경로별 목표 지표 8 · `pass{지표: bool, n_pass}` · `right` · `scored` · `wrong[]` · `path` |
| `v1_compare{headline, goal}` | 1차 리포트 값 + 1차를 목표 정의로 다시 센 값 |
| `conflict_board` · `boards` · `m1_raw_diff[]` | 충돌 판(해소 · raw) · 판 사이 달라진 문항 |
| `by_intent{}` | 의도별 문항 · 맞음 · 재현율 · 정밀도 · 안전 누락 |
| `causes[]` | 원인 묶음 — `id` · `title` · `fix_rule` · `stage`(고칠 단계 결정) · `count` · `examples[]` |
| `staff_questions[]` | 의료진에게 물을 것(정답이 갈리는 문항만) — `q` · `from` |
| `m1[]` | 문항별 — `resolve[]`(말 → 노드) · `i01_mode` · `got{concerns · site · units · family_only …}` · `wrong_units[{unit, name, family, site, why}]` · `recall` · `precision` · `safety_missing[]` · `why[]` · `status` |
| `m2{rows[], by_origin, by_variant}` | 말마다 `text` · `origin` · `variant` · `mode`(완전 · 낱말 · 끝말 · 접두 · 없음) · `status` · `targets[]` · `expect` |
| `m3{엣지 종류: {rows, sample, verdicts, error_rate, checked[]}}` | 표본 판정 |
| `m4{by_group, missing[], units_zero_safety[], …}` | 묶음별 원문 · 구조 누락 |

## 3. `check_quality.py` 출력

| 칸 | 무엇 |
|---|---|
| `run{exit[2], same_ab{파일: bool}, same_work{파일: bool}}` | 두 번 실행 종료 코드 · 서로 같음 · 작업 폴더와 같음 |
| `errors[{kind, detail}]` · `warnings[]` | SKILL.md §1 |
| `scoring{scoring_checked[], path_changed[]}` | 지문 대조 결과 |
| `rule_field_changes[{id, text, field, before, after, delta{계열: {더함, 뺌}}}]` | 규칙 칸이 1차와 다른 문항 |
| `goals{경로: {n_pass, of, rows[{goal, values, pass}], right, scored, wrong[], path}}` | 목표 6 |
| `versions[{label, version, M1{…}, M2_found_pct, M3_error_pct, M4_missing, causes, goal{경로: {n_pass, right, recall, precision, i01_recall, i01_precision}}, note}]` | 판별 지표(v1 은 `goal.「1차 정의」`) |
| `version_changes[{from, to, questions[{id, text, from, to}]}]` | 판 사이 상태가 바뀐 문항 |
| `selftest[{tamper, expect, caught, got}]` | 틀린 값 13 |

## 4. `references/baseline.json`

| 칸 | 무엇 | 바꾸는 때 |
|---|---|---|
| `fixed_set` | 1차 고정 문항 파일(작업 폴더 기준 경로) | 문항 세트를 새로 정하는 사용자 결정 |
| `rule_fields[]` · `rule_fields_basis` | 규칙으로 계산되는 정답 칸 | 정답 칸 정의가 바뀔 때 |
| `goal_excluded[]` | 목표 제외 문항 | 같음 |
| `scoring{이름: 지문}` | 채점 함수 · 상수 지문 — 다르면 오류 | **사용자 결정으로 채점을 바꿀 때만** `--write-baseline` |
| `path{이름: 지문}` | 측정 경로 함수 지문 — 다르면 경고 | 측정 경로 변경을 확인(대조)한 뒤 `--write-baseline` |
| `versions[{label, report, note, goal_from_current_v1_compare?}]` | 비교할 보관 판 | 판을 보관할 때 한 줄 |
