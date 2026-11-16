# WP33 결과 보고 — Soniox context 를 고유명사 74개 · 정방향 + 역방향만으로 (D-71)

## 상태: done

- backend 워커 · 2026-11-16 · 태스크 task_b48643878a02
- 브랜치 `kknaksss/tongky-quality-re1-dict` · 커밋 `c52ec83`(push · PR 안 함)

## 수행 — 파일 · 모듈

| 파일 | 바꾼 것 |
|---|---|
| `back/app/service/glossary.py` | term 키 `proper`(bool · 선택 · 없으면 false) — `TERM_KEYS` 에 더함 · 타입 검사(`type:bool` · `$.terms[i].proper`) · `Term.proper`. `build_context` 는 `proper` 이고 그 언어 entry 가 있는 term 만 쓴다 · `terms` = ko 대표명만 · `translation_terms` = 정방향(ko → 현지) + 역방향(현지 → ko)만. `forward_alias` · `reverse_alias` 칸은 남기되 늘 비운다(로그 · `describe` 모양 그대로). `TRIM_ORDER` = `terms` → `reverse`(정방향 · general · text 는 줄지 않음) |
| `back/seed/glossary.json` | 버전 `2026-11-16.11` · ① 74 id 에 `"proper": true`(`category` 다음 자리 · 나머지 96개는 키 없음). 이름 · 별칭 · `wrong` · 순서는 `.10` 그대로 |
| `back/scripts/seed_v11.py` | 새 파일 — `.10` → `.11` 변환(74 id 목록 · 같은 입력이면 같은 바이트) |
| `back/tests/conftest.py` | `term(..., proper=True)` — 가짜 시드 기본은 proper. f-004 「마취 연고」 는 proper 아님(빠짐 시험용) |
| `back/tests/test_context.py` | 기대값을 새 규칙으로 고침 + 새 시험 4개 |
| `back/tests/test_correct.py` | 새 시험 2개(proper 아닌 term 바로잡기) |
| `back/tests/test_seed.py` · `seed_tables.py` | `V11` · `PROPER_IDS`(74) · `proper` 타입 오류 3건 · 선택 키 · 레포 시드 74 대조 |
| `back/tests/test_quality.py` | `drop_reverse` 예를 별칭(`Thermage FLX`)에서 이름(`美版热玛吉FLX`)으로 |

- `back/app/container.py` 는 손대지 않았다(`context_for` 로그 줄 그대로 — 별칭 칸은 `forward_alias=0 reverse_alias=0` 으로 찍힘).
- 바로잡기(`correct_terms`)는 그대로 시드 170개 전부 · 별칭 · `wrong` 을 쓴다. 세션 · 끊김 · 세 참여자 코드는 건드리지 않았다.
- 역방향 source 중복(처음 짝만) · yue · zh-Hant t2s · 크기 줄이기 · `invalid_request` 때 정방향만 다시 연결은 그대로다.

## 검증

```
cd back && uv run pytest -q && uv run ruff check .
536 passed, 1 warning   (전: 525)
All checks passed!
```

새 시험 · 고친 시험(브리프 A):

| # | 시험 |
|---|---|
| ① proper 아닌 term 은 context 에 0 | `test_non_proper_term_not_in_context`(가짜 · 7개 언어) · `test_real_seed_context_proper_only_no_alias_pairs`(레포 시드 · 7개 언어) |
| ② 별칭 짝 0 | `test_alias_pairs_never_in_context` · `test_reverse_same_name_first_pair_only` · 레포 시드 시험(위) |
| ③ terms = proper ko 이름 수 | 레포 시드 시험(위) — 언어마다 `terms == [proper ko 대표명]` (74) |
| ④ 바로잡기는 proper 아닌 term 도 그대로 | `test_d71_non_proper_term_still_corrected`(레포 시드 토닝 ph-012 yue 틀린 꼴) · `test_d71_fake_non_proper_term_corrected` · 기존 바로잡기 시험 전부 통과 |
| ⑤ 시드 검사 `proper` 타입 오류 | `test_validation_rules` 에 `proper="yes"` · `1` · `None` → `type:bool` · `test_proper_optional_default_false` · `test_repo_seed_proper_is_74_listed_ids` |
| 그 밖 | `test_real_seed_context_fits_language_limit_without_trim`(7개 언어 줄이기 0) · 줄이기 순서 · 로그 줄 · 재연결 시험을 새 칸 수로 고침 |

## 언어별 context 크기 (운영 인자 `context_max_chars(lang)` · `json.dumps` 글자 · `text` 포함)

| 언어 | terms | 정방향 | 역방향 | 짝 합 | 글자 | 전(c7a582f · .10) 글자 / 짝 / 뺀 수 |
|---|---|---|---|---|---|---|
| en | 74 | 74 | 74 | 148 | 7,694 | 20,679 / 395 / 0 |
| ja | 74 | 74 | 74 | 148 | 7,364 | 21,958 / 467 / terms 2 |
| zh | 74 | 74 | 73 | 147 | 7,277 | 19,917 / 431 / 0 |
| zh-Hant | 74 | 74 | 68 | 142 | 6,916 | 22,010 / 487 / 0 |
| th | 74 | 74 | 74 | 148 | 7,768 | 23,214 / 471 / terms 79 |
| vi | 74 | 74 | 74 | 148 | 7,698 | 19,958 / 385 / 0 |
| yue | 74 | 74 | 74 | 148 | 7,328 | 19,811 / 427 / 0 |

- 별칭 칸(정방향 별칭 · 역방향 별칭)은 모든 언어 0. 뺀 수 0(일곱 언어 다 한도 안).
- 역방향이 74 보다 적은 것은 같은 현지 이름 처음 짝만 남겨서다(zh `乐提葆` 1 · zh-Hant 6).
- 공식 한도 「about 10,000 characters」 안에 일곱 언어 모두 든다.

## B — 실물 측정

- 운영 키(셸 env 에만) · `stt_config(soniox_lang(lang), to_soniox(build_context(시드 .11 terms, lang, context_max_chars(lang))))` 를 그대로 보냄(`stt-rt-v6` · two_way · 끊김 2000 / -0.3 · agent text 켬). 음성은 probe3 와 같은 합성 음성 · 같은 사례 배치 · 같은 잡음 시드.
- **144 세션 · 오류 0**(zh 108 · 다른 여섯 언어 각 6). 파일: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile--------/6b7f4a9c-bfce-487f-8c42-08de89fd57d4/scratchpad/probe4/`(`probe.py` · `analyze.py` · `run_*.jsonl` · `logs/` · `analysis.txt`)

### B.1 zh — 앞 리포트 p1 과 한 표

p1 = 앞 조사의 「① 만」(별칭 짝 포함 · 196짝 · 9,307자 · terms 74). **이번 = 정방향 + 역방향만(147짝 · 7,277자 · terms 74)**. 횟수는 같다.

| term(문장) | p1(앞) | **이번** |
|---|---|---|
| 울쎄라(SU) | 18 / 18 | **18 / 18** |
| 울쎄라(SU · 흐름) | 6 / 6 | **6 / 6** |
| 울쎄라(SS · 슈링크와 한 문장) | 0 / 6 | **0 / 6** |
| 울쎄라(SS · 흐름) | 0 / 6 | **0 / 6** |
| 써마지(ST · 단문 / 흐름) | 6 / 6 · 6 / 6 | **6 / 6 · 6 / 6** |
| 쥬베룩(ST · 단문 / 흐름) | 6 / 6 · 6 / 6 | **6 / 6 · 6 / 6** |
| 리쥬란 힐러(SR · `丽驻兰黑盒`) | 0 / 6 | **6 / 6** |
| 나보타(SN · `Nabota`) | 4 / 6 | **4 / 6** |
| 슈링크유니버스(SS · 단문 / 흐름) | 6 / 6 · 6 / 6 | **6 / 6 · 6 / 6** |
| 손님 `热玛吉` → 써마지(CT) | 6 / 6 | **6 / 6** |
| 손님 `美版超声刀` → 울쎄라(CU) | 18 / 18 | **18 / 18** |

일반 낱말(사전에 없음 · 각 6회):

| 낱말 | p1(앞) | 이번 — 받아쓰기 → 번역 |
|---|---|---|
| 혈관 | `血管激光` 6 / 6 | 「혈관」 6 / 6 → `血管激光` 6 / 6 |
| 색소 · 토닝 | `色素治疗` 6 / 6 · `色调护理` 4 · `色调护护(剂)` 2 | 「색소 · 토닝」 6 / 6 → `色素治疗` 6 / 6 · 토닝 = `色调护理` 2 · `色调护护剂` 2 · `色调护护` 2 |
| **제모** | 받아쓰기 「제목」 6 / 6 → `标题` 6 / 6 | **받아쓰기 「제목」 6 / 6** → `标题` 6 / 6 |
| 미백 | `美白针` 4 · `美白针剂` 2 | 「미백」 6 / 6 → `美白针` 3 · `美白针剂` 3 |

### B.2 zh 틀린 꼴

| term | 나온 꼴 | 지금 바로잡기가 잡나 |
|---|---|---|
| 울쎄라(SS · 단문 / 흐름) | **`Ulthera` 12 / 12** — 같은 문장의 슈링크유니버스가 `Shurink Universe` 로 나간 뒤 영문(앞 조사와 같음) | 잡음 12 / 12(ph-121 zh 틀린 꼴) |
| 나보타(SN) | `拿波塔` 2(음역) | 못 잡음 0 / 2 |

- 리쥬란 힐러는 p1 에서 `丽쥬兰…`(한글 섞임) 0 / 6 이었는데 이번에는 `丽驻兰黑盒治疗` 6 / 6 이었다. 바뀐 것은 별칭 짝 49개가 빠진 것(`丽珠兰黑盒` 등 역방향 별칭 포함)과 크기뿐이다. 왜 나아졌는지는 가르지 않았다(관찰).

### B.3 다른 여섯 언어 (직원 문장 SU · ST 각 3회)

| 언어 | 오류 | context 글자 / 짝 | 울쎄라(SU) | 써마지(ST) | 쥬베룩(ST) |
|---|---|---|---|---|---|
| en | 0 | 7,694 / 148 | 2 / 3 | 3 / 3 | 3 / 3 |
| ja | 0 | 7,364 / 148 | 3 / 3 | **0 / 3** | 3 / 3 |
| zh-Hant | 0 | 6,916 / 142 | **0 / 3** | 3 / 3 | 3 / 3 |
| th | 0 | 7,768 / 148 | **0 / 3** | 3 / 3 | 1 / 3 |
| vi | 0 | 7,698 / 148 | 1 / 3 | 3 / 3 | 3 / 3 |
| yue | 0 | 7,328 / 148 | **0 / 3** | 3 / 3 | 3 / 3 |

판정 = 그 언어 시드 **이름**(t2s · casefold · 공백 무시)이 번역에 있는가. 별칭 · 틀린 꼴은 「나옴」 으로 세지 않았다.

| 언어 · term | 나온 꼴 | 시드에서 무엇 | 지금 바로잡기 |
|---|---|---|---|
| en 울쎄라 | `Ultherra` 1 | 없음 | 못 잡음 |
| ja 써마지 | `サーマジ` 3 | ja `wrong` | 잡음 3 / 3 |
| zh-Hant 울쎄라 | `玉绒药` 2 · `美白精华` 1 | 없음 | 못 잡음 |
| th 울쎄라 | `อุลซ่า` 3 | th `wrong` | 잡음 3 / 3 |
| th 쥬베룩 | `Juvelook` 2 | th 별칭 | (별칭이라 고칠 대상 아님) |
| vi 울쎄라 | `Ulthera` 2 | vi `wrong` | 잡음 2 / 2 |
| yue 울쎄라 | `玉琥药` · `玉露` · `玉仙药` 각 1 | 없음 | 못 잡음 |

- 「지금 바로잡기」 는 기록된 원문 · 번역을 `correct_terms(시드 .11, lang, "me", …)` 에 넣어 본 결과다(세션 밖 · 같은 함수).
- 이 여섯 언어는 앞 조사에 같은 문장의 「전(170개)」 수치가 없다 — 비교는 하지 않았다. n = 3 이다.

## 계약 대조

| 브리프 항목 | 같음 / 다름 |
|---|---|
| general · text 그대로 | 같음 |
| terms = 고유명사 74 ko 이름만 · 별칭 없음 | 같음(일곱 언어 74) |
| translation_terms = 74 정방향 + 역방향만 · 별칭 짝 0 | 같음 |
| 시드 `proper` · 선택 · 없으면 false · 검사에 키 · 타입 · 74 id true · 버전 `2026-11-16.11` | 같음 |
| 바로잡기 170개 전부 · 별칭 · wrong 지우지 않음 | 같음 |
| 역방향 중복 · t2s · 줄이기 · 정방향만 재연결 · 로그 모양 | 같음(줄이기 묶음은 terms → reverse 로 줄어듦) |
| front · 문서 · 운영 서버 | 손대지 않음 |

## 정할 것

1. **「제모」 받아쓰기** — terms 를 74개로 줄인 결과 「제모 → 제목」 6 / 6(앞 p1 과 같음) · 번역 `标题`. 일반 낱말 받아쓰기 힌트를 따로 둘지.
2. **사전 이름이 안 나온 줄 중 지금 바로잡기도 못 잡는 꼴** — zh 나보타 `拿波塔` · en `Ultherra` · zh-Hant `玉绒药` · `美白精华` · yue `玉琥药` · `玉露` · `玉仙药`. 틀린 꼴로 더할지 · 다른 보장 길과 묶을지.
3. **울쎄라가 다른 영문 이름 뒤에 영문으로 나가는 것**(zh SS `Ulthera` 12 / 12) — 바로잡기가 잡고 있다. context 로 더 할 것이 있는지.
4. **zh-Hant · yue 울쎄라 0 / 3** — 사전 이름(`美國音波` · `美版超聲刀`)이 안 나오고 뜻이 다른 말이 나왔다. 횟수를 늘려 다시 잴지(n = 3).
5. **토닝** — 사전 없이 `色调护理` 류. ② 로 둔 결과를 그대로 받을지.
6. **합성 음성 · n 의 한계** — 실기기 · 실제 목소리 결과가 아니다.
