# app WORK-008(SPEC-002 0.5.2) 보고

상태: WP-1 ~ WP-6 끝(실물 F1~F4 = 18221 속도 탭 API · effort low · 동시 · 허브 18106). 중간에 디스크 가득 참(ENOSPC)으로 잠시 멈췄다가 회복 뒤 마감까지 함.

## WP-1 세트 칸
- `_v052a/` 에 고치기 전 set.jsonl · calls/ · answer-key/ · key-summary.md · key-table.md **복사**(diff 0 확인). `_v052b/set.jsonl` = `_v052a` 에서 키 전용 칸 셋(Q03 · Q12 lower · Q10 upper)만 뺀 사본.
- 바꾼 줄 Q03 · Q05: Q03 `expected_kinds` = overview · mechanism · indication · outcome · lineup + 새 선택 칸 `expected_kinds_by_entry{procedure_case:CAS-016: [overview, mechanism, indication, outcome]}` · Q05 = overview · mechanism · indication · outcome · 둘 다 `key_fix1`. (다) 에서 본 세트의 `key_upper_entries` · `key_lower_entries` 지움. `loader --validate` 85 줄 오류 0.
- 코드: `loader.kinds_of_entry` · `OPTIONAL_FIELDS` 꼴 검증 · `key_calls._by_entry` / `narrow_by_entry`(읽기 호출만 좁힘 — 케이스 lineup scope 빠짐 · 판정용은 그대로) · `answer_key.kinds_met` 대상별 종류 · 키에 `expected_kinds_by_entry`(있을 때만 — 다른 키 바이트 그대로).
- A-1 grep 전수: 대상별로 고친 곳 = key_calls build_spec · spec_from_item · answer_key kinds_met · build_key. 그대로(합집합) = walk/calls.py key_calls(호출의 kinds 를 봄 — 좁혀진 kinds 를 받음) · report.py:229(종류 지표) · quality/checks.py:201(D11) · key_table.py:61(합집합을 돌되 대상별 kinds_met 으로 찍힘) · loader.py:83(코드 검증). 새 칸 = SPEC-002 0.6 되적기 후보.

## WP-2 허브 0.5.2 응답 받기
- RQ1: `required.rows_for_count` — 머리 `inherited_from` 있는 응답의 행 = inherited · `front.required[].inherited_via`. **end_state.counted_rows 가 hier=상위 행을 빼고 있어 HG1 행이 (가) 로 떨어졌다** → 같은 표지(UPPER)가 붙은 행은 센다(판정 식 아님 · 2 의 셈). 답 키 같은 함수.
- 표지: `layer_depth`(depth≥2 늘) · `layer_via`(같은 응답 depth1 holder_name → 없을 때만 label 조회 · trace `label_for: layer_via`) · `site_match`(「부위 글자로 맞음」/「그 부위의 고민으로 묶임」) · `inherited_fill` 윗고민에도. K4 = layer_depth · site_match · inherited_fill. csi_ids · inherited_from · 이름 못 얻은 via 코드는 verified_lines 에만. 묶음 열쇠 그대로(줄별 표지로 holder 안 잃음 — 시험).
- 실물 꼴 대조(18106): HG1 머리 · HG3 site_match `{by, csi_ids}` · HG2 layer.depth/via · scope depth/via · coverage 고민 {self 0, inherited 181} — 모의와 같음.
- 시험: tests/test_holes.py(11) · tests/test_set_v052.py(7) 새로 · test_walk_core N-5 단언 한 줄.

## WP-3 답 키 다시 뽑기 · 대조
- (나) `_v052b` (18106) vs `_v052a`: 같음 32 · 다름 5. Q19 14→18 · Q20 9→12 · Q25 5→6 · Q27 7→9(전부 g_pair · depth 2 — SPEC 셈과 같음) · Q03 · Q10 같음(Q10 via=CON-008 허브 inherited_from) · Q18 · 21 · 22 · 23 · 28 · 30 · 36 같음(same_day_packages 수도 같음 — Q19 10 · Q21 3) · **Q12 483→487: +4 g_adverse_detail(GAX-01510~01513 · M2 → 제품 PRD-051 → 하위 제품 PRD-052 · PRD-074 → PRD-075 · depth 2) — 옛 키 전용 하위 시술 셋으로는 안 닿던 「제품의 하위 제품」 길(N-3) · 보고(고치지 않음)**.
- (다) 본 세트: (나) 대비 Q03 · Q05 만 다름. Q03 45→434 · 상태 안 맞음(rq1) → 근거 충족 · 표본 1/7 → 7/7 · Q05 3→75 · 같은 풀림. **indication · outcome 의 met_by 는 케이스 자기(self)** — WORK 의 「inherited 로 서나」 예상과 다름(케이스에 자기 행이 있음).
- 재실행 바이트 같음 · gold_hash 8accbb21 같음 · aux_hash b7249e38 → 6435fe41. key-table.md 다시 씀(--prev _v052a · Q10 윗고민 이름 표시 고침). N-5: U-2 로 Q03 · Q05 기대 종류가 늘었다 — B 가 그 종류를 안 읽으면 빠짐으로 잡힌다(표의 두 줄 기대 정보 칸에 보임). --confirm 안 함.
- 파일(로컬): data/eval-set/_v052b/key-diff-v052.md(나) · key-diff-v052c.md(_v052a↔최종) · key-diff-v052-b-vs-c.md.

## WP-4 구멍 묶음 꼴(pick --holes → data/eval-set/pick-holes.json · question 비움 · set.jsonl 안 넣음)
- 셈: HG1 13(전부 steps 1 — silver 나무로도 13 모두 한 단 위 · **SPEC 의 9 + 4 갈림은 데이터에 없음 → H02 후보 0**) · HG1 (iii) 41 ✓ · 계열 18 ✓ · HG2 (i) 16 · (ii) 6(케이스 끝에만) · (iii) SPEC 꼴 0 ✓ · (iii-a) 16 · (iii-b) 24 짝 · 계열 7 ✓ · HG3 짝 97 ✓ · (i) 37 ✓ · (ii) 54 · (iii) 91 ✓(자기 행 0 이고 윗고민만 받는 묶인 고민 2 따로) · (iv) 표본 12.
- draft H01~H10 꼴(H06 은 (iii-a) · (iii-b) 둘 다 options — 고르지 않음).

## WP-5 되적기 확인
- 표의 「이미 있음」 그대로 확인. N-2 entry.by = noul(runs 줄에서 확인). N-5 단언 추가(이미 있음 — 0). judge.md 에 SPEC §8-3 「정답 꼴 둘」 문장 옮김(없었음). pick.py:9 주석 「적응」 고침. README 허브 전제 0.5.2 줄.

## WP-6 실물(18221 속도 탭 API · effort b=low c=low · 동시 · 허브 18106 · 단건 — 편차 큼)

| | run | B 종료 | B 재료 시술 수 / 답 이름 | C 답 이름 | B 첫 답 ms | C 첫 답 ms | 비고 |
|---|---|---|---|---|---:|---:|---|
| F1 이마 주름 | 0280114fa4d3 | 근거 충족 | 6 / 7 | 7 | 1614 | 10929 | site_match 글자 24 · 묶임 54 · 재료 98 행 |
| F1 0.5.1 | 53da717fd7a6 | 근거 충족 | 2 / 2 | 2 | 1835 | 7833 | C effort medium(옛 기록) |
| F2 볼 주름 | ba0678ffec2a | 근거 충족 | 3 / 3 | 19 | 1763 | 12432 | met_by inherited · via CON-008. 단 Jev 가 주름 CON-001 · 부위 볼 을 함께 남겨(TG2) concern_candidates(CON-012, site=볼) → 묶음 2(기대 65 아님) |
| F3 Q12 | a804a471de82 | **후보 소진**(기대 원천 미확정 (다)) | 3 / 1 | 1 | 2743 | 12731 | adverse:ADV-051 대상의 adverse 행 0(읽기가 M2 + adverse_code 필터라 ADV-051 노드로 셈 안 됨) · (다) 는 end_state 에서 1회차 미판정(O-5 ②) · depth2 재료 214 |
| F4 표정 주름 | 39f1b80cc664 | 근거 충족 | 50 / 12 | 12 | 5244 | 9396 | 0.5.1 ce5d23661812 와 같은 수(864 행 · 50 / 12) |
| F4 0.5.1 | ce5d23661812 | 근거 충족 | 50 / 12 | 12 | 10741 | 12417 | C effort medium(옛 기록) |

- C 종료 상태는 앱 판정 없음(옛 run 도 같음). O-29 ④: 공통 답 지시가 0.5.1 runs 와 달라 앞 판과 견줄 때 주의.
- F2 LCK-010: 허브는 두 요청(site 있음 · 없음) 다 `ledger_check` LCK-010 을 낸다 — B trace 는 읽기 조회별 ledger_check 를 줄에 남기지 않는 꼴(기존)이라 runs 줄에는 안 보임.
- F3: 0.5.1 Q12 run 은 runs.jsonl 에 없음(대조 불가). depth≥2 재료 214 · `layer_via` 이름은 전부 같은 응답 depth1 행에서(label 조회 0 건 — A-3 셈 = 0 · 되적기 후보 근거 없음).
- N-3: F3 의 거친 층 holder 표에 product 가 있다(계열 → 제품 → 하위 제품) — 그 행에 layer_depth · layer_via(제품 이름) 표지가 재료에 붙음(G4).
- 하지 않음: F2 화면 정확도 탭 확인(18221 은 디스크 사고 뒤 내림 — 화면 기록 다시 보기는 test_web 이 옛 줄 포함 통과).

## 마감(디스크 회복 뒤)
- 디스크 가득 참(ENOSPC)으로 몇 분 명령이 안 돌았다 — 지운 것 없음. 회복 뒤 이어 함.
- `uv run ruff check .` 통과 · `uv run pytest -q` **181 passed · 1 skipped**(기준선 163 · 1 + 18: test_set_v052 7 · test_holes 11 · test_walk_core 단언 한 줄) · `loader --validate` 85 오류 0 · `batch --check`(18106) 전부 됨 · 18221 내림(LISTEN 0) · 18106 · 18105 · 18220 안 건드림.
- 커밋 후보 grep: 실제 코드 · 이름 · 홈 경로 0(시험의 가짜 코드 LCK-900 · CSI-9001 · ZZ… 만) · 키 꼴 0. 커밋 안 함 · --confirm 안 함.
- 바뀐 파일(코드): clinic_chat/evalset/{loader,key_calls,answer_key,key_table,pick}.py · clinic_chat/walk/{required,end_state,verified,material,gate,breadth}.py · clinic_chat/columns/col_b.py · prompts/judge.md · README.md · tests/{test_set_v052,test_holes}.py(새) · tests/test_walk_core.py. 로컬(gitignore): data/eval-set/{set.jsonl, calls, answer-key, key-summary.md, key-table.md, key-diff-*.md/json, pick-holes.json, _v052a/, _v052b/} · runs/runs.jsonl(F1~F4 4 줄).

## 코디 확인 · 되적기 후보
1. `expected_kinds_by_entry` 세트 칸(SPEC-002 0.6).
2. HG1 「한 단 9 · 두 단 4」 — 18106 · silver 나무 모두 13 전부 한 단 → H02((ii)) 후보 0. SPEC §9-3d 셈 근거 다시 보기.
3. Q12 키 +4(제품의 하위 제품 adverse_detail) — 키 전용 하위 시술 셋이 못 닿던 길 · 허브 쪽이 맞음으로 읽힘(지적 아님 판단은 코디).
4. F2: Jev 가 「볼」 부위 · 「주름」 을 TG2 로 남겨 HG1 + HG3 이 겹친 좁은 조회(묶음 2) — 일반 규칙 건(고치지 않음).
5. F3: B 는 adverse:ADV-051 대상 required 0 → 후보 소진. (다) 는 end_state 1회차 미판정(O-5 ②)이라 기대 「원천 미확정 (다)」 와 어긋남 — 알고 가는 것인지 확인.
6. end_state.counted_rows 를 HG1 표지로 넓힌 것(Q10 (가) → 근거 충족) — SPEC §5 (가) 되적기 한 줄.
