# 리뷰 리포트 — WP33 context 고유명사 74 · 정방향 + 역방향만 (D-71) / code (2026-11-16)

- 대상: 브랜치 `kknaksss/tongky-quality-re1-dict` · 커밋 `c52ec83` · `git diff origin/main...HEAD` (9 파일 · +337 / −82) · untracked 0
- 기준: 발주서 `tongky-quality-re1-be5-brief.md` §2 · DEC D-71 · `dict-classification.md` 「① 고유명사 — 74개」
- 리뷰어는 리포 파일을 고치지 않았고 Soniox 도 부르지 않았다. 아래 수치는 모두 순수 계산(시드 + `build_context`)으로 낸 것이다.

## 판정: WARN

코드는 발주서 §2 표와 같다(FAIL 0). 다만 **zh-Hant 에서 일반 낱말 「雷射(레이저)」 의 역방향 짝 target 이 `레이저` 에서 `클라리티2` 로 바뀐다**(W-1). 코드는 「처음 짝만」 규칙을 그대로 따랐다. 원인은 그전부터 있던 시드 값(고유명사 두 개의 zh-Hant name 이 `雷射`)이 이번 필터로 드러난 것이다. 손님이 실제로 만날 수 있는 자리라 결정이 필요하다.

## 검증 실행 (1회)

```
cd back && uv run pytest -q   → 536 passed, 1 warning (Starlette httpx DeprecationWarning — 무관 · 기존)
cd back && uv run ruff check . → All checks passed!
```

## 1. 발주서 §2 표 대조

| 칸 | 발주서 §2 | 코드 | 판정 |
|---|---|---|---|
| `general` · `text` | 그대로 | `back/app/service/glossary.py:309` `general=[dict(g) for g in GENERAL]` · `:312` `text=CONTEXT_TEXT if with_text else ""`(바뀌지 않음). 순수 계산으로 7개 언어 `general` · `text` 가 `.10` 시드의 조립 결과와 바이트까지 같다 | PASS |
| `terms` | proper 74 ko 대표명만 · 별칭 없음 | `glossary.py:310` `terms=[t.ko for t in rows]` · `:304` `rows = [t for t in terms if t.proper and lang in t.entries]`. 계산: 7개 언어 모두 terms 74 | PASS |
| `translation_terms` | 정방향(ko → 현지) + 역방향(현지 → ko)만 | `glossary.py:311` 정방향 · `:315-320` 역방향(name 만 · `norm` · 처음 짝만). 정방향 74 / 역방향 en 74 · ja 74 · zh 73 · zh-Hant 68 · th 74 · vi 74 · yue 74 (backend 리포트 표와 같음) | PASS |
| 별칭 짝 0 | 정방향 별칭 · 역방향 별칭 넣지 않음 | `glossary.py:312` `forward_alias=[] … reverse_alias=[]`. 칸은 남았고 늘 비어 있다(로그 모양 유지 — 발주서 §2 끝 줄과 같음) | PASS |
| 일곱 언어 같은 규칙 | 같음 | 언어 분기는 `context_norm(lang)`(t2s) 하나뿐. 74 개 proper term 이 7개 언어 entry 를 모두 가진다(빠진 entry 0 — 계산) | PASS |
| 시드 `proper` 키 | bool · 선택 · 없으면 false · 검사에 키 · 타입 | `glossary.py:30` `TERM_KEYS` 에 `"proper": False` · `:173-175` `type:bool` · `:78` `proper: bool = False` · `:205` 전달. 시험 `tests/test_seed.py` `proper="yes"/1/None` → `type:bool` | PASS |
| 시드 버전 | `2026-11-16.11` | `back/seed/glossary.json:3` | PASS |
| 바로잡기 | 170개 전부 · 별칭 · wrong 그대로 | §3 참고 | PASS |

## 2. 시드 `.11` 대조

- **proper = 74 id 와 정확히 같다**: 분류표 「① 고유명사 — 74개」 절의 id(정규식 `(ph|kr)-\d{3}`)를 뽑은 집합과 `"proper": true` 인 집합을 비교했다. 더 0 · 덜 0. `true` 아닌 `proper` 값 0(false 는 키 없이 둠).
- **이름 · 별칭 · wrong · 순서가 `.10` 과 같다**: `origin/main:back/seed/glossary.json` 과 비교했다. `.11` 에서 `proper` 키를 빼고 version 을 맞추면 두 JSON 이 같다(`==` True · term id 순서 같음 · 170 = 170). `git diff` 의 `+` / `−` 줄은 `"proper": true` 74줄과 version 1줄뿐이다.
- 키 자리: 74개 모두 `category` 바로 다음이다. `_keys`(`glossary.py:99-108`)는 키 순서를 검사하지 않으므로, 이 자리를 지키는 것은 `tests/test_seed.py` `test_repo_seed_proper_is_74_listed_ids` 하나다(SPEC §4.2 「키 순서는 표 순서」 — 표에 `proper` 행이 아직 없다 → 문서 고칠 자리 D-1).
- 74 목록은 세 곳에 따로 있다: `scripts/seed_v11.py:21-33` · `tests/seed_tables.py` `PROPER_IDS` · 시드. 시험이 시드와 `PROPER_IDS` 를 대조하므로 어긋나면 빨개진다. PASS

## 3. 바로잡기가 `build_context` 에 기대지 않는가 — PASS

`grep -rn "build_context|\.proper|correct_terms" back/app back/scripts` 전수:

- `correct_terms`(`back/app/service/interpret/correct.py:114`)는 `g.terms` 전부를 돈다(`:124` excluded · `:126` targets). `proper` 를 읽지 않는다.
- 「걸렸다」 판정 `match_spans`(`back/app/service/records.py:98-110`)도 `glossary.terms` 전부 · `ko` · `ko_aliases` · `name` · `aliases` 를 쓴다. `build_context` · `ContextParts` 를 import 하지 않는다.
- 세션(`back/app/service/interpret/session.py:224`)은 `correct_terms(g, …)` 에 `Glossary` 를 그대로 넘긴다. context 는 `context_for` → STT 설정에만 쓰인다(`:200` · `:245`).
- `app/` 안에서 `.proper` 를 읽는 곳은 `glossary.py:304` 한 곳뿐이다.
- 시험: `tests/test_correct.py` `test_d71_non_proper_term_still_corrected`(레포 시드 · 토닝 ph-012 yue · proper 아님 · context 에 없음 · 그래도 고침) · `test_d71_fake_non_proper_term_corrected`.

## 4. 조용히 통과하는 자리

| # | 자리 | 본 것 | 판정 |
|---|---|---|---|
| S-1 | `invalid_request` 정방향만 재연결 | `forward_only`(`glossary.py:331-334`)는 general + text + 정방향만 남긴다(그대로). `is_forward_only`(`:337-341`)는 `terms · forward_alias · reverse · reverse_alias` 가 다 비어야 참이다. 별칭 칸이 늘 비어 있어도 terms · reverse 가 남아 있으면 거짓이 되어 재연결한다. 다 줄어 정방향만 남으면 재연결하지 않는다. 시험 `test_context.py` 재연결 2건(처음 = terms · 역방향 있음 · terms 만 다 빠지고 역방향 남음)과 「넷 중 하나라도 남으면」 시험(별칭 칸은 가짜 짝으로 채워 봄)이 이것을 본다 | PASS |
| S-2 | 줄이기 순서 | `TRIM_ORDER = ("terms", "reverse")`(`glossary.py:272`). 정방향 · general · text 는 줄지 않는다. 줄일 묶음이 줄어든 것은 발주서 §2(「없어진 묶음은 빠진다」)와 같다. 지금 시드로는 7개 언어 모두 한도 안이라 뺀 수 0이다(`test_real_seed_context_fits_language_limit_without_trim`). 잠재 위험: 앞으로 별칭 칸을 다시 채우면 그 칸은 줄이기 대상이 아니다. 지금 채우는 곳은 0이다 | PASS |
| S-3 | 역방향 중복 | 처음 짝만(`glossary.py:314-320`)이고 `drop_reverse` 도 `seen` 에 미리 넣는다. 규칙은 그대로다. **그런데 재료가 proper 로 줄면서 「처음」 이 바뀐 source 가 하나 있다** → W-1 | WARN |
| S-4 | yue · zh-Hant t2s | 정방향 target · 역방향 source 모두 `norm`(`:311` · `:316`). 시험 `test_context.py` zh-Hant · yue t2s 시험이 새 기대값으로 남아 있다 | PASS |
| S-5 | 로그 줄 | `container.py:54-57` · `session.py:251-253` 모양이 그대로다. 별칭 칸은 `forward_alias=0 reverse_alias=0`. 시험이 caplog 의 두 줄을 글자 그대로 대조한다 | PASS |
| S-6 | 품질 시험 스크립트 인자 `with_text` · `drop_reverse` | `with_text` 는 그대로 동작한다. `drop_reverse` 는 이제 역방향 **이름** source 만 뺄 수 있다. **별칭 source(예 예전 시험값 `Thermage FLX`)를 주면 아무것도 빠지지 않는데 오류 없이 지나간다** → W-2 | WARN |
| S-7 | 시드 로더 기동 검사 | `container.py:35-36` `load_seed` → `validate_seed` → `proper` 타입 오류면 `SeedError` → `main.py:69` 기동 멈춤(그대로). 모르는 키 · 누락 검사도 그대로다 | PASS |
| S-8 | context `None` 조건 | 이제 「그 언어 **proper** entry 가 0」 일 때 `None` 이다(`:304-306`). 그러면 general · text 까지 STT 설정에서 빠진다. 지금 시드는 7개 언어 모두 74라 실제로 생기지 않는다. 독스트링 `:290` 은 아직 「entry 가 하나도 없으면」 이다 → W-3 · D-3 | WARN(경미) |
| S-9 | 시험 강도 | 새 시험은 묶음을 리스트 전체로 대조하고(`==`), 레포 시드 시험은 7개 언어 · 74 · 짝 수 공식(`len(pairs) == len(rows) + len(names)`)까지 본다. 빈 단언은 없다 | PASS |

## WARN

### W-1 zh-Hant 역방향 `雷射 → 클라리티2` — 일반 낱말 「레이저」 가 고유명사로 옮겨질 수 있음

- 위치: `back/seed/glossary.json` ph-020 클라리티2 · ph-023 엑셀V 의 zh-Hant `name` = `雷射`(그전부터 있던 값 · 이번 변경 아님) · 조립 `back/app/service/glossary.py:304` · `:315-320`
- 계산(리뷰어): `.10` 시드 전체를 재료로 했을 때와 `.11` 을 비교해 역방향 source 별 target 이 바뀐 것을 찾았다. 7개 언어에서 **딱 1건**: zh-Hant `雷射` 가 `레이저`(ph-014 · proper 아님)에서 **`클라리티2`**(ph-020 · proper)로 바뀌었다. ph-014 가 재료에서 빠지자 같은 이름을 가진 ph-020 이 「처음 짝」 이 됐다(ph-023 엑셀V 짝은 중복으로 빠진다).
- 뜻: 대만 손님이 「雷射」(그냥 레이저)라고 말하면, Soniox 가 이를 직원 쪽 한국어 `클라리티2` 로 옮기도록 힌트를 받는다. 정방향도 `클라리티2 → 雷射` · `엑셀V → 雷射` 로, 상표가 일반 낱말로 나간다(이것은 `.10` 에도 있던 것).
- 근거: D-71 「일반 낱말 · 분류 이름(예: … 레이저 …)은 넣지 않는다」 — `雷射` 는 일반 낱말인데 고유명사의 name 으로 `translation_terms` 에 남는다. 발주서 §2 「역방향 source 중복 처리(처음 짝만) … 지금 규칙 그대로」 — 코드는 이 규칙을 지켰다. 그래서 FAIL 이 아니라 WARN 이고, 고칠 곳은 시드 값이나 결정이다.
- 덧붙임: zh-Hant `飛梭雷射 → 프락셀` 은 ph-016 프락셔널(proper 아님)과 같은 이름이지만 `.10` 에서도 프락셀이 처음이었다(바뀐 것 없음).
- 정할 것(리뷰어가 정하지 않는다): ① ph-020 · ph-023 zh-Hant name 을 상표 꼴로 고칠지(시드) ② 일반 낱말과 같은 이름을 가진 proper 짝을 context 에서 뺄지(규칙) ③ 그대로 둘지.

### W-2 `quality_check.py --drop-reverse` 가 맞지 않는 source 를 소리 없이 무시

- 위치: `back/scripts/quality_check.py:462` · `:609` `drop_reverse_count` = 준 인자 수(실제로 뺀 수가 아님) · `glossary.py:314`
- D-71 뒤로 역방향에는 이름 짝만 있다. 예전처럼 별칭 source(시험이 바꾼 `Thermage FLX` 가 그 예 — `tests/test_quality.py:463`)를 주면 빠지는 짝이 0인데도 결과 머리에는 `drop_reverse_count: 1` 이 찍힌다. 「짝 하나 빼고 잰 결과」 가 실제로는 빼지 않고 잰 결과가 된다. 동작 자체는 `.10` 때도 같았다(모르는 source 는 무시). 다만 이번에 뺄 수 있는 source 가 줄어 잘못 줄 가능성이 커졌다.
- 운영 경로에는 영향이 없다(품질 시험 스크립트만). 권고: 실제로 빠진 짝 수를 머리에 적거나, 맞는 source 가 없으면 멈추게 한다.

### W-3 낡은 설명 · 스크립트 칸 (경미 · 운영 영향 0)

- `back/app/service/glossary.py:290` — `build_context` 독스트링 첫 줄 「그 언어 entry 가 하나도 없으면 None」. 실제는 「proper entry 가 0이면」(`:304`).
- `back/app/service/glossary.py:277-278` — `to_soniox` 독스트링 「정방향 기본 → 정방향 별칭 → 역방향 기본 → 역방향 별칭」. 동작은 맞다(빈 칸이 이어붙을 뿐).
- `back/scripts/live_check.py:407` — 결과 칸 이름 `forward_alias_써마지` 는 「정방향 별칭 짝」 을 뜻한다. D-71 뒤로 별칭 짝은 0 이라 이름과 뜻이 맞지 않는다. 시드에서 「써마지」 는 별칭이 아니라 별도 term 의 ko 다(`.10` 도 같음). 칸이 True 가 되더라도 그 term 의 정방향 짝이 같은 target 이라서일 뿐이다.
- `back/scripts/test7.py:104-110` `expected_ko` — 이제 proper 짝만 보므로 proper 아닌 term 은 늘 `(tid, False)` 를 돌려준다. 7차 판정을 다시 돌릴 때 「겹침」 판정이 `.10` 때와 달라질 수 있다.

## 고객이 실물에서 만날 자리

1. **zh-Hant 손님 「雷射」 → 직원 화면에 `클라리티2`** 가 나올 수 있다(W-1). 실물로 재지는 않았다(브리프: Soniox 호출 금지).
2. 일반 낱말(혈관 · 제모 · 토닝 …)은 이제 context 힌트 없이 옮겨진다(D-71 이 바란 것). backend 실측에서 「제모 → 제목」 6 / 6이 나왔다(backend 리포트 B.1). 이 받아쓰기 오류는 앞 p1(terms 74)과 같다.
3. 바로잡기는 170개 그대로라 proper 아닌 term 의 틀린 꼴도 고쳐진다(§3).

## 문서 고칠 자리 (SPEC 은 아직 옛 규칙 — 이번 판정에는 넣지 않음)

| # | SPEC 자리 | 지금 SPEC | 코드 · 발주서 §2 |
|---|---|---|---|
| D-1 | §4.2 term 키 표(키 순서 = 표 순서) | `proper` 행 없음 | `proper` · 선택 · bool · 없으면 false · 자리 = `category` 다음 · 검사 `type:bool` |
| D-2 | §4.2.x 시드 판 절 | `.10` 까지 | `.11` = `.10` + proper 74(이름 · 별칭 · wrong · 순서 그대로) · 스크립트 `scripts/seed_v11.py` |
| D-3 | §4.5 「재료」 · 「넣는 때」 | 「`entries[L]` 이 있는 term 만」 · 「그 언어 entry 가 하나라도 있을 때」 | proper 이고 `entries[L]` 이 있는 term · proper entry 0 이면 `None` |
| D-4 | §4.5 칸 표 `terms` | ① ko 대표명 ② ko 별칭 | ko 대표명만 |
| D-5 | §4.5 칸 표 `translation_terms` · D-33 근거 칸 | 정방향 기본 → 정방향 별칭 → 역방향 기본 → 역방향 별칭 | 정방향 → 역방향만(별칭 칸은 늘 비어 있다) |
| D-6 | §4.5 역방향 중복 줄 | 「기본 짝이 별칭 짝보다 앞」 | 별칭 짝이 없으므로 「같은 현지명은 처음 짝만」 · W-1 결정 반영 |
| D-7 | §4.5 「구조로 들고 다닌다」 | 별칭 칸이 있음 | 칸은 남고 늘 비어 있음(로그 · `describe` 모양 유지) |
| D-8 | §4.6 2번 줄이기 순서 | terms(별칭 먼저) → 역방향 별칭 → 역방향 기본 → 정방향 별칭 | terms(뒤에서부터) → 역방향 |
| D-9 | §4.6 글자 수 표 | `.10` 값(ja `terms` 2 · th `terms` 79 뺌) | `.11` 값(backend 리포트: en 7,694 · ja 7,364 · zh 7,277 · zh-Hant 6,916 · th 7,768 · vi 7,698 · yue 7,328 · 뺀 수 0) · th 여유 · ja 여유 문구도 낡음 |
| D-10 | §4.5 「translation_terms 에 넣지 않는 것」 | 일반 낱말 짝 · 틀린 꼴 | + proper 아닌 term · 별칭 짝(D-71). 별칭은 바로잡기만 쓴다 |

## 경계 · 범위

- 바뀐 파일 9개는 모두 발주서 §4 allowed_paths 안이다(`back/app/service/glossary.py` · `back/seed/glossary.json` · `back/tests/**` · `back/scripts/seed_v11.py`). `container.py` · front · 바로잡기 · 끊김 · 세 참여자 코드는 diff 0 이다. PASS
- 비밀값 · 하드코딩 주소: diff 에 0. PASS

## 참고(기존 부채 · 무관)

- `pytest` 경고 1건: Starlette `httpx` DeprecationWarning — 무관 · 기존.
- 시드 zh-Hant 고유명사끼리 같은 name 묶음: `雷射`(클라리티2 · 엑셀V) · `保提拉`(레티보 · 보툴렉스) · `丽珠兰`(t2s 뒤 · 리쥬란아이 · 리쥬란 힐러 · 리쥬란 HB+) · `乔雅露`(쥬베룩 · 쥬베룩볼륨) · `ASCE+ 外泌体`(ASCEplus · EXOSOME SKIN). zh 는 `乐提葆`(레티보 · 보툴렉스). 역방향은 처음 term 으로만 간다(zh-Hant 역방향 68개의 이유). `.10` 에도 있던 것이다.
