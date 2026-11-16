# WP26 결과 보고 — 시술명 바로잡기 · 시드 `.8` 틀린 꼴 (D-58 · D-60 · SPEC 0.9.1 §5.12 · §4.2 · §4.2.5)

## 상태: done(① ~ ⑤ + 연기 확인 + ㉒) — ⑦ 실물 ㉖ 은 이번 발주(§3)에 없어 안 돌림

## 수행 — 파일

| 파일 | 무엇 |
|---|---|
| `back/app/service/interpret/correct.py`(새) | 바로잡기 순수 함수 `correct_terms(glossary, lang, side, original, translation) → Correction(text · fixed · missed · steps · before)` — 걸리는 조건 1 · 2 · W-1(외 → 한 같은 현지명 묶음) · ① 시드 틀린 꼴 → ② 다른 언어 이름 · 별칭 → ③ 가까운 라틴 낱말(**한 → 외는 ja · zh · zh-Hant · th · yue 만 · 외 → 한 전부** · 상수 한 곳 `NEAR_MIN_LEN=4` · `NEAR_MAX_DIST=2` · `NEAR_LANGS_KO_TO_X`) · 걸린 term 전부에 ① ② 먼저 · 남은 term 만 ③ · 후보 빼기 ⓐ ⓑ · 보호 구간(다른 term 의 맞게 나온 이름 + 갈아 끼운 구간) · 라틴 낱말 경계(부호 · 성조 글자 포함 — `is_latin_alnum`) · 정규화가 글자 수를 바꾸면 `NotLengthPreserving` |
| `back/app/service/records.py` | 찾기 함수를 **같이 쓰게** 정리 — `match_spans`(term · 자리 · 걸린 이름 · 「더 긴 일치」) · `hays_of` · `_spans(…, word=)`(경계 판정만 주입 · 기록 판정은 그대로 ASCII 경계). `_hits_in` = `match_spans` 위. 발화 줄 끝 `fixed`(늘) · `translation_before`(바로잡은 줄에만) — `caption(cap, fixed, translation_before)` 로 **caption dict 밖에서** 받는다 |
| `back/app/service/glossary.py` | `Term.ko_wrong` · `Entry.wrong`(선택 · 기본 `()` · 키 자리 `ko_aliases` 다음 · `aliases` 다음) · **검사 8 `wrong_form`**(5 · 7 그대로 · 괄호 허용 · 공백 뺀 2글자 이상 · 목록 안 겹침 0 · 자기 / 다른 term 의 맞는 이름과 겹침 0 · 비교 `wrong_key` = §5.9 정규화) · `build_context` 는 두 필드를 읽지 않음(무수정) |
| `back/app/service/interpret/assembler.py` | 확정 자리(`_close`) 한 곳 — **`is_blank(원문)` 먼저** · 번체 변환 전 번역을 고친 뒤 `final:true` caption · TTS `Utterance` 를 만든다(한 번 고친 글에서 자막 · TTS · 기록) · `final:false` 는 그대로 · 예외는 삼키고 경고 1줄(종류만) · 바로잡은 표시는 `corrections[id]` 에(caption dict 에 안 실음) |
| `back/app/service/interpret/session.py` | 선택 인자 `glossary` · **`fix_terms=True`**(끄는 길은 이 인자뿐) · 로그 2종(`interpret term not corrected: term · lang · side` / `interpret term corrected: id · side · lang · terms · steps` — 문장 · 꼴 0) · 기록 쪽으로 `fixed` · `translation_before` 를 따로 넘김 |
| `back/app/api/interpret.py` **65행** | `glossary=c.glossary` **한 줄만**(코디 허용 — 세션이 메모리 시드를 알아야 바로잡기가 돈다 · 끄는 인자는 안 넘김) |
| `back/seed/glossary.json` | **`.8`(`2026-11-15.8`)** — `scripts/seed_v8.py`(새 · `.7` 입력 · 같은 바이트 재실행 확인)로: 처분 §12 표 그대로 `wrong` + **D-60** kr-014 zh-Hant(name `熱瑪吉` · 별칭 `Thermage` · ✓ · 출처 r1 대만 S1) + version. `ko_wrong` 0 |
| `back/scripts/quality_check.py` | 조합 A · B = 바로잡기 끔 · C = 켬 · `--no-fix` · 세션에 시드 넘김 · 결과 머리에 `fix_terms` |
| `back/tests/test_correct.py`(새) | §9.1 「바로잡기」 ① ~ ⑭ · 검사 8 · context 가 두 필드를 안 읽음 · 세션(자리 · TTS · 기록 · 예외 · 끄는 길 · 로그) — 32건 |
| `back/tests/test_api_surface.py` | 「api 는 시드를 읽지 않는다」 그대로 · **세션에 넘기는 그 한 줄 1개만 예외**(정확히 1개 · 그 밖 `glossary` · `.terms` · `.entries` · `load_seed` · `build_context` 0 — 코디 허용) |
| `back/tests/test_records.py` · `test_seed.py` · `seed_tables.py` · `test_quality.py` · `test_quality_script.py` | 뜻이 바뀐 줄만(발화 줄 키 · `.8` version · D-60 kr-014 zh-Hant · 조합 키 `fix_terms`) |

## 시드 `.8` — 틀린 꼴(개수만 · 꼴은 시드 · 로컬 대조표에만)

- 처분 §12 표 43개 → **넣음 39 · 16칸** / **뺌 4**(검사 8 ⓓ — 그 언어의 맞는 이름 · 별칭과 같음: ph-121 en 1 · zh-Hant 2 · yue 1).
- 칸별 개수: ph-121 zh 3 · zh-Hant 1 · yue 2 · th 1 · vi 1 / kr-014 zh 1 · yue 1 · ja 1 / kr-015 en · zh · th · vi · yue 각 5 · zh-Hant 1 / ph-112 zh 1 / ph-012 yue 1. `ko_wrong` 0.
- 로컬 대조표(값 포함 · git 제외): `reference/2026-11-12-interpreter-idea/quality-run/wp26-wrong-local.md`.
- 주의: SPEC §4.2.5 첫 목록 표에는 **T30 ph-042 보툴렉스 zh** 칸이 있는데 처분 §12 표에는 없다 — 발주서대로 §12 그대로 넣었다(보툴렉스 zh 틀린 꼴 0 · 연기 확인에서 T30 은 「못 찾음」).

## 연기 확인 — WP24 의 기계 FAIL 행 39개를 바로잡기 함수에 그대로(Soniox 없이 · 시드 `.8`) → 같은 규칙으로 다시 판정

| 묶음 | 바뀜 → pass | 안 바뀜(fail 그대로) |
|---|---|---|
| 조합 C · C2(T01 ~ T33 · 각 6행) | T03 zh(ph-121 · kr-014 ① ) | T07 · T18(en — 시술명 아닌 규칙 · 바로잡기 대상 아님) · T23 · T24(3절 조각) · **T30 zh(ph-042 못 찾음 — 위 주의)** |
| 손님 쪽 C · C2(각 3행) | — | T34 en · T49 vi(원문에 term 안 걸림 — 인식 · 대상 아님) · **T46 th(ph-121 못 찾음 — SPEC §4.2.5 대로 「실패로 남김」)** |
| 다국어 C(21행) | **20행**: T01 yue(ph-012 ①) · T02 zh · zh-Hant · th · vi · yue(ph-121 ①) · T03 ja(kr-014 ①) · zh(ph-121 · kr-014 ①) · zh-Hant · th · vi(ph-121 ①) · yue(ph-121 · kr-014 ①) · T04 en · zh-Hant · th · vi · yue(kr-015 ①) · zh(ph-112 · kr-015 ①) · **T05 zh · yue(ph-033 ②)** | T01 th(ph-012 못 찾음) |

- 합: **39행 중 22행이 바뀌어 기계 pass** · 17행 그대로(그중 바로잡기 대상인데 못 찾은 것 5행: T30 zh ×2(C · C2) · T46 th ×2 · 다국어 T01 th).
- **확인 부탁 — 다국어 T05 zh · yue(보톡스 ph-033)**: ② 가 zh-Hant 이름(`t2s` 뒤)을 번역 속 **뜻이 맞는 변형**(처분 §12 에서 「사람 판정 좋음」 이라 뺀 꼴) 안에서 찾아 zh · yue `name` 으로 갈아 끼웠다(로컬에서 종류만 확인 — 문자 꼴 · 다른 언어 zh-Hant 하나). SPEC §5.12 대로의 동작(번역에 zh 이름 · 별칭 0 → ② 다른 언어 이름)이지만 좋던 번역을 바꾼다 — §5.12 「잘못 바꿀 수 있는 자리」 의 실제 예. 막으려면 사전 쪽(그 변형을 zh · yue 별칭으로) 결정이 필요(워커는 안 정함).

## ㉒ — v6 · 문안 · 시드 `.8` · D-56 기준

| lang | 거절 | 보낸 글자 | 기준 | 뺀 수 | `.7` 과 |
|---|---|---|---|---|---|
| en | 0 | 20,679 | 24,892 | 0 | 바이트까지 같음 |
| ja | 0 | 21,647 | 21,962 | 0 | 같음 |
| zh | 0 | 20,401 | 22,551 | 0 | 같음 |
| zh-Hant | 0 | **21,448** | 22,685 | 0 | **+31 — D-60(name · 별칭)뿐** |
| th | 0 | 23,193 | 23,215 | 0 | 같음 |
| vi | 0 | 19,958 | 24,349 | 0 | 같음 |
| yue | 0 | 19,034 | 22,825 | 0 | 같음 |

- 틀린 꼴은 context 에 안 들어간다(6개 언어 조립 결과 바이트 같음 · 시험 `test_context_ignores_wrong_fields`). zh-Hant 차이는 D-60 이 바꾼 name · 별칭 때문이다.

## 검증

| 명령 | 결과 |
|---|---|
| `cd back && uv run ruff check .` | All checks passed |
| `cd back && uv run pytest -q` | **447 passed**(새 32) · 경고 1(starlette httpx — 기존 · 무관) |
| `seed_v8.py` 재실행 | 같은 바이트 · 로더 · 검사 8 통과 |
| ㉒ 실물 | 위 표 · 키는 사용자 `.env` → 프로세스 env 만 |

## 계약 대조 · 주의

- WS 메시지 키 그대로(caption 키 6개 · 시험) · 허용 경로 6개 그대로(`test_api_surface` 통과) · 로그에 문장 · 꼴 0(시험).
- **배포 순서**: 시드 `.8` 은 이 코드(검사 8 · 새 키)와 같은 PR 이어야 한다 — 0.8.x 코드는 `.8` 의 `wrong` 키를 `unknown_field` 로 거절해 기동이 멈춘다(WORK WP26).
- SPEC §9.1 「밖으로 내는 것」 문구는 api/interpret.py 65행 예외를 반영해 코디 → planner 가 맞춘다(코디 답).
- ③ 숫자(4 · 2)는 기본값 그대로(OQ-032 — 워커는 안 바꿈).

---

# 수정 1 — 처분 §13 반영(코디 · 2026-11-15)

## 수행

- `back/scripts/seed_v8.py` 상수 둘 추가 → `.7` 에서 `.8` 다시 만듦(같은 바이트 재실행 확인 · 손 수정 0):
  - **① ph-033 보톡스 zh · yue 별칭 `肉毒` 추가**(별칭 맨 뒤 · 처분만으로 고친 칸이라 `source: manual` · `note` = 「처분 §13 ① — …」 · §4.2.4 규칙).
  - **② ph-042 보툴렉스 zh 틀린 꼴 2개 추가**(처분 §12 에서 빠졌던 T30 칸 — SPEC §4.2.5 와 이제 같다).
- 틀린 꼴: **41개 · 17칸**(앞 39 · 16칸 + ph-042 zh 2) · 검사 8 로 뺀 것 4 그대로 · `ko_wrong` 0 · D-60 그대로. 로컬 대조표는 앞 판 그대로 + 이 두 항목(시드가 정본).
- 코드 · 시험 변경 없음(시험이 시드 개수를 고정하지 않는다).

## 연기 확인(다시 · WP24 FAIL 행 39 · Soniox 없이 · 시드 `.8` 새 판)

| 묶음 | 바뀜 → pass | 안 바뀜 |
|---|---|---|
| 조합 C · C2(각 6행) | T03 zh · **T30 zh(ph-042 ① — 새로 풀림)** | T07 · T18 · T23 · T24(대상 아님) |
| 손님 쪽 C · C2(각 3행) | — | T34 · T49(인식) · T46 th(ph-121 못 찾음 — SPEC 대로) |
| 다국어 C(21행) | 18행(앞 판 20행 중 T05 zh · yue 둘이 빠짐) | T01 th(ph-012 못 찾음) · **T05 zh · yue — 바로잡기를 부르지 않음**(번역의 맞는 변형이 새 별칭 `肉毒` 으로 「맞는 이름」 에 걸림 → 조건 2 · 처분 §13 ① 의 뜻대로) |

- 합: **39행 중 22행 pass**(조합 C · C2 4 · 다국어 18) · 17행 그대로 · **못 찾음 3행**(T46 th ×2 · 다국어 T01 th) · T30 은 못 찾음에서 빠졌다.
- T05 zh · yue 의 **기계 판정은 fail 로 남는다** — 다국어 규칙 파일은 시드 `.7` 로 만든 판(새 별칭 `肉毒` 이 규칙의 「이름 목록」 에 없다)이라서다. 규칙 파일은 돌린 뒤 바꾸지 않는다(§9.3) — 사람 판정은 「좋음」. 7차에서 `.8` 기준으로 규칙을 다시 만들면 통과로 잡힌다.

## ㉒ — 다시(v6 · 문안 · 시드 `.8` 새 판 · D-56)

| lang | 거절 | 보낸 글자 | 기준 | 뺀 수 | 앞 판과 |
|---|---|---|---|---|---|
| en | 0 | 20,679 | 24,892 | 0 | 같음 |
| ja | 0 | 21,647 | 21,962 | 0 | 같음 |
| zh | 0 | **20,436** | 22,551 | 0 | +35(별칭 `肉毒` 역방향 짝 하나) |
| zh-Hant | 0 | 21,448 | 22,685 | 0 | 같음(D-60) |
| th | 0 | 23,193 | 23,215 | 0 | 같음 |
| vi | 0 | 19,958 | 24,349 | 0 | 같음 |
| yue | 0 | **19,069** | 22,825 | 0 | +35(같은 이유) |

거절 0 · 7개 언어 줄이기 0 · 정방향 뺀 수 0.

## 검증

`cd back && uv run ruff check .` 통과 · `uv run pytest -q` **447 passed**(경고 1 — 기존 · 무관) · `seed_v8.py` 같은 바이트 · ㉒ 실물 위 표 · 커밋 없음.

---

# 수정 2 — 처분 §14(코드 검수 W-1 ~ W-4 · 코디 · 2026-11-15)

## 수행

| # | 파일 | 무엇 |
|---|---|---|
| W-1 | `back/scripts/seed_v8.py` → `back/seed/glossary.json` | **ph-112 스컬트라 zh 틀린 꼴 1개를 뺐다**(일상 낱말 · §11 원칙). ja 써마지 틀린 꼴은 그대로. 틀린 꼴 **40개 · 16칸** · 검사 8 로 뺀 4 그대로 · 같은 바이트 재실행 확인 |
| W-2 | `back/app/service/interpret/correct.py` | 같은 현지명 묶음(W-1 계약)의 거짓 「못 찾음」 고침 — **고친 글로 W-1 을 다시 본다**(`_settled_by_group`): ① ② 를 다 돈 뒤 ③ 에 들어가기 전, 그리고 `missed` 를 셀 때. 앞 term 이 갈아 끼운 ko 로 풀린 뒤 term 은 `fixed` 도 `missed` 도 아니다(로그 0) |
| W-3 | `back/scripts/seed_v8.py` → 시드 | ph-033 zh · yue `note` = 처분 문구 + **「· 옛 출처 <옛 URL>」**(대륙 · 홍콩 표 S 사이트 URL 그대로). SPEC 문구(§4.2.5 「바뀌는 것」 · D-56 표 끝 열 · §9.1 api 한 줄)는 처분대로 planner 다음 판 |
| W-4 | `back/app/service/records.py` · `correct.py` | `_spans(…, latin_form=)` — 라틴 판정만 주입(기록 판정은 기본값 `str.isascii` 그대로). 바로잡기는 `is_latin_form`(공백 · ASCII · 부호 붙은 라틴 글자뿐)을 넘겨 **부호 · 성조 붙은 라틴 꼴도 라틴 낱말 경계**로 찾는다 — 더 긴 라틴 낱말 가운데는 안 바꿈 |
| 시험 | `back/tests/test_correct.py` | ⑫ 더함(앞 term 이 바뀐 뒤 같은 묶음의 뒤 term `missed` 0) · W-4 1건(성조 붙은 꼴이 더 긴 낱말 가운데면 안 바꿈 · 낱말이면 바꿈) — 둘 다 고치기 전 코드에서는 실패하는 모양 |

## 연기 확인(다시 · WP24 FAIL 행 39 · 시드 `.8` 새 판)

- **21행 바뀌어 pass** · **1행 바뀌었지만 fail**(다국어 T04 zh — 리투오 kr-015 는 ① 로 바뀜 · 스컬트라 ph-112 는 W-1 로 틀린 꼴을 빼 **못 찾음** — 처분대로) · 17행 그대로.
- 못 찾음 4행: T46 th ×2(ph-121 — SPEC 대로) · 다국어 T01 th(ph-012) · 다국어 T04 zh(ph-112 — W-1).
- 수정 1 대비: 다국어 T04 zh 만 pass → fail(위). 그 밖 같음.

## ㉒ — 다시(v6 · 문안 · 시드 `.8` 새 판 · D-56)

7개 언어 **거절 0 · 줄이기 0** · 정방향 뺀 수 0 · 글자 수 수정 1 과 같음(en 20,679 · ja 21,647 · zh 20,436 · zh-Hant 21,448 · th 23,193 · vi 19,958 · yue 19,069 — 틀린 꼴은 context 재료가 아니다).

## 검증

`cd back && uv run ruff check .` 통과 · `uv run pytest -q` **449 passed**(새 2) · 경고 1(기존 · 무관) · 커밋 없음.
