# 결정 묶음 4 — 동의어 게이트 자료(proposed 를 사용자가 고른다)

① 부작용 문구 조각 0 · ② 부위·물질 조각 0 · ③ 시술 조각 60 — 고를 자리 60 · 추천 있음 0 · 추천 없음 60.
추천대로 고르면 닫히는 문구 자리 0 · 풀리는 ⑨ 참조 0(항목마다 가장 많이 닫는 옵션을 고르면 문구 0 · 참조 22 — 겹침 미반영 · 항목별 합).
후보 근거는 정규화 부분 일치 · 원장 병기(「A(B)」) · 영문 대응(문헌 같은 레코드)뿐 — 유사도·추정 없음. 추천은 원장 병기·영문 대응이 후보 하나만 가리킬 때만. effect 는 그 결정을 넣은 사전으로 그 자리만 다시 분해해 센 값.
고른 결과: `python3 apply_gate.py --gate out/gate/batch4.json --out decisions/batch4/ --answers answers.json`(answers = {하위 id: 옵션 key}).

| 자리 | 조각 | 후보(근거) | 추천 | 추천 effect |
|---|---|---|---|---|
| b4-prc/001 | 바디 | 인모드(paren_phrase) / 바디 전체(partial) | — | — |
| b4-prc/002 | 지방분해 | 냉각지방분해(partial) / 지방분해주사 (마케팅명)(partial) | — | — |
| b4-prc/003 | 리쥬란 | 리쥬란 힐러(partial) / 리쥬란아이(partial) | — | — |
| b4-prc/004 | 리프팅 | — | — | — |
| b4-prc/005 | 볼륨 | 쥬베룩볼륨(partial) | — | — |
| b4-prc/006 | 비타민C | 이온토포레시스(paren_phrase) | — | — |
| b4-prc/007 | 시술 | — | — | — |
| b4-prc/008 | 심부 | — | — | — |
| b4-prc/009 | 이모드 | — | — | — |
| b4-prc/010 | 810nm | — | — | — |
| b4-prc/011 | EMS | 바디 EMS(partial) / 페이셜 EMS(partial) | — | — |
| b4-prc/012 | 고주파 | — | — | — |
| b4-prc/013 | 색소 | 색소/토닝(partial) | — | — |
| b4-prc/014 | 여드름 | 여드름 전용(partial) | — | — |
| b4-prc/015 | 저출력 | — | — | — |
| b4-prc/016 | 주사 | 지방분해주사 (마케팅명)(partial) | — | — |
| b4-prc/017 | 프랙셔널 | — | — | — |
| b4-prc/018 | 리프팅기기 | — | — | — |
| b4-prc/019 | 제모레이저 | 제모(partial) | — | — |
| b4-prc/020 | 반영구화장 | — | — | — |
| b4-prc/021 | 약물치료 | — | — | — |
| b4-prc/022 | LLLT | 저출력레이저(LLLT)(partial) | — | — |
| b4-prc/023 | 모발이식 | — | — | — |
| b4-prc/024 | 미백주사 | — | — | — |
| b4-prc/025 | 병변내 | — | — | — |
| b4-prc/026 | 스테로이드주사 | — | — | — |
| b4-prc/027 | 755nm | 알렉산드라이트(paren_phrase) | — | — |
| b4-prc/028 | PDT | — | — | — |
| b4-prc/029 | 경구 | — | — | — |
| b4-prc/030 | 광선치료 | IPL(paren_phrase) | — | — |
| b4-prc/031 | 끝 | — | — | — |
| b4-prc/032 | 냉동지방분해 | 쿨스컬프팅(paren_phrase) | — | — |
| b4-prc/033 | 리포셀 | — | — | — |
| b4-prc/034 | 마이크로니들링 | — | — | — |
| b4-prc/035 | 물광주사 | — | — | — |
| b4-prc/036 | 미라드라 | — | — | — |
| b4-prc/037 | 실 | — | — | — |
| b4-prc/038 | 재생 | 재생/면역(partial) | — | — |
| b4-prc/039 | 제거 | — | — | — |
| b4-prc/040 | 제네시스 | — | — | — |
| b4-prc/041 | 주입 | 주입장비(partial) | — | — |
| b4-prc/042 | 탈모 | 탈모(비수술)(partial) | — | — |
| b4-prc/043 | 턱라인 | 울쎄라(paren_phrase) | — | — |
| b4-prc/044 | 피부결 | 프락셔널(paren_phrase) / 피부(partial) | — | — |
| b4-prc/045 | 피코레이저 | — | — | — |
| b4-prc/046 | 회복력 | — | — | — |
| b4-prc/047 | 후 | — | — | — |
| b4-prc/048 | 흉터 | 흉터 전용(partial) | — | — |
| b4-prc/049 | 복용 | — | — | — |
| b4-prc/050 | 중 | — | — | — |
| b4-prc/051 | 헤어맥스 | — | — | — |
| b4-prc/052 | CO2레이저 | CO2프락셔널(partial) | — | — |
| b4-prc/053 | PDL | — | — | — |
| b4-prc/054 | V빔 | — | — | — |
| b4-prc/055 | ±5-FU | — | — | — |
| b4-prc/056 | 트리암시놀론 | — | — | — |
| b4-prc/057 | 1064nm | — | — | — |
| b4-prc/058 | 50% | — | — | — |
| b4-prc/059 | 808nm | — | — | — |
| b4-prc/060 | ALA | — | — | — |

## adverse-phrase — ① 부작용 문구 조각 → 사건 사전 동의어(상위 0 / 조각 0)

문구 사전 unlinked 항목에서 사건을 못 찾은 미등록 조각 — 조각이 든 문구 자리 수 순. 하위 항목마다 고른다.

## site-material — ② 부작용 문구의 부위·조직·물질 조각(하위 0)

같은 미등록 조각 중 부위(site · 상대 부위) · 물질(adverse_qualifier · 성분) 사전 후보가 있는 것. 하위 항목마다 고른다.

## procedure-fragment — ③ 시술 쪽 남은 조각(⑨ open · 상위 60 / 조각 198)

⑨ open 미해결 참조의 미등록 조각 — 그 조각이 든 open ⑨ 참조 수 순. 하위 항목마다 고른다.

### b4-prc/001 — 참조 조각 「바디」 — 인모드, 바디 전체 중 무엇인가?

⑨ open 미해결 참조 7(원장 자리 7)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `synergy.json:links[].to@20` — 「HIFES/EMS 바디」
- `synergy.json:links[].to@21` — 「M9-인모드(바디)」
- `procedure-comparison.json:comparisons[].procedures[].name@6/3` — 「바넬라 (고주파 바디)」
- `treatment-optimization.json:by_concern[].severity_levels[].optimal_combo[]@7/0/1` — 「고주파 바디 RF」
- `treatment-optimization.json:by_concern[].severity_levels[].optimal_combo[]@7/1/2` — 「바디 RF」
- `treatment-optimization.json:by_concern[].severity_levels[].optimal_combo[]@7/2/1` — 「바디 HIFU(리포셀)」
- `market-pricing.json:categories[].items[].name@9/5` — 「EMS 바디 (팔뚝/허벅지)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| map_1 | product_name 「인모드」(M9)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 1/7(원장 자리 1) · 근거 원장 이름 병기 「인모드(바디)」 | canonical_mapping `DEC-2026-11-05-B4-PRC-001a` |
| syn_2 | site 「바디 전체」 의 동의어 | 풀리는 ⑨ 참조 2/7(원장 자리 2) · 근거 「바디 전체」 ⊃ 조각 「바디」 | dictionary_add `DEC-2026-11-05-B4-PRC-001b` |
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 근거가 정규화 부분 일치·원장 문구 병기뿐 — 병기는 같은 말·원인·예시·부위를 가리지 않고 부분 일치는 표기 겹침일 뿐이라 같은 뜻이라는 원장 문장이 아니다(추천 없음 · 사람이 정한다)
이미 승인된 같은 결정: DEC-2026-11-04-B1-SYN-001, DEC-2026-11-05-B3-SIT-01, DEC-2026-11-05-B3-SIT-02, DEC-2026-11-05-B3-SIT-03, DEC-2026-11-06-B6A-SITE-01, DEC-2026-11-06-B6A-SITE-02, DEC-2026-11-06-B6A-SITE-03, DEC-2026-11-06-B6A-SITE-04, DEC-2026-11-06-B6A-SITE-05, DEC-2026-11-06-B6A-SITE-06, DEC-2026-11-06-B6A-SITE-07, DEC-2026-11-06-B6A-SITE-08, DEC-2026-11-06-B6A-SITE-09, DEC-2026-11-06-B6A-SITE-10, DEC-2026-11-06-B6A-SITE-11, DEC-2026-11-06-B6A-SITE-12, DEC-2026-11-06-B6A-SITE-13, DEC-2026-11-06-B6A-SITE-14, DEC-2026-11-06-B6A-SITE-15

### b4-prc/002 — 참조 조각 「지방분해」 — 냉각지방분해, 지방분해주사 (마케팅명) 중 무엇인가?

⑨ open 미해결 참조 4(원장 자리 8)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `problem-packages.json:problems[].complaints[].procedures[].name@10/1/0` — 「지방분해」
- `problem-packages.json:problems[].complaints[].procedures[].name@10/2/0` — 「지방분해」
- `problem-packages.json:problems[].complaints[].procedures[].name@10/4/0` — 「지방분해」
- `problem-packages.json:problems[].complaints[].combos[].combo[]@10/1/0/0` — 「지방분해」
- `problem-packages.json:problems[].complaints[].combos[].combo[]@10/2/0/0` — 「지방분해」
- `problem-packages.json:problems[].complaints[].combos[].combo[]@10/4/0/0` — 「지방분해」
- `procedure-comparison.json:comparisons[].procedures[].name@6/2` — 「스컬프슈어 (레이저 지방분해)」
- `post-procedure-timeline.json:timelines[].name@5` — 「DCA 지방분해 주사」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| map_1 | modality_subcategory_label 「냉각지방분해」(M14)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 2/4(원장 자리 6) · 근거 「냉각지방분해」 ⊃ 조각 「지방분해」 | canonical_mapping `DEC-2026-11-05-B4-PRC-002a` |
| map_2 | modality_subcategory_label 「지방분해주사 (마케팅명)」(M16)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 2/4(원장 자리 6) · 근거 「지방분해주사 (마케팅명)」 ⊃ 조각 「지방분해」 | canonical_mapping `DEC-2026-11-05-B4-PRC-002b` |
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 근거가 정규화 부분 일치·원장 문구 병기뿐 — 병기는 같은 말·원인·예시·부위를 가리지 않고 부분 일치는 표기 겹침일 뿐이라 같은 뜻이라는 원장 문장이 아니다(추천 없음 · 사람이 정한다)

### b4-prc/003 — 참조 조각 「리쥬란」 — 리쥬란 힐러, 리쥬란아이 중 무엇인가?

⑨ open 미해결 참조 4(원장 자리 4)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `procedure-comparison.json:comparisons[].procedures[].name@1/3` — 「리쥬란 (PN주사)」
- `procedure-comparison.json:comparisons[].procedures[].name@8/0` — 「스킨부스터 (쥬베룩/리쥬란)」
- `treatment-optimization.json:by_concern[].severity_levels[].optimal_combo[]@0/0/1` — 「스킨부스터(리쥬란)」
- `treatment-sequence.json:common_combos[].sequence[]@5/1` — 「스킨부스터 리쥬란」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| map_1 | product_name 「리쥬란 힐러」(M4)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 3/4(원장 자리 3) · 근거 「리쥬란 힐러」 ⊃ 조각 「리쥬란」 | canonical_mapping `DEC-2026-11-05-B4-PRC-003a` |
| map_2 | product_name 「리쥬란아이」(M4)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 3/4(원장 자리 3) · 근거 「리쥬란아이」 ⊃ 조각 「리쥬란」 | canonical_mapping `DEC-2026-11-05-B4-PRC-003b` |
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 근거가 정규화 부분 일치·원장 문구 병기뿐 — 병기는 같은 말·원인·예시·부위를 가리지 않고 부분 일치는 표기 겹침일 뿐이라 같은 뜻이라는 원장 문장이 아니다(추천 없음 · 사람이 정한다)

### b4-prc/004 — 참조 조각 「리프팅」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 4(원장 자리 4)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `treatment-optimization.json:annual_plans[].schedule[].procedures[]@2/11/1` — 「연말 리프팅 관리(RF/HIFU 터치)」
- `post-procedure-timeline.json:timelines[].name@2` — 「HIFU/RF 리프팅」
- `market-pricing.json:categories[].items[].name@6/2` — 「민트 리프팅 (양쪽)」
- `market-pricing.json:categories[].items[].name@12/0` — 「플라즈마 리프팅 (전체얼굴)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/005 — 참조 조각 「볼륨」 — 쥬베룩볼륨 중 무엇인가?

⑨ open 미해결 참조 4(원장 자리 4)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `market-pricing.json:categories[].items[].name@1/1` — 「입술 볼륨 (HA 1cc)」
- `market-pricing.json:categories[].items[].name@1/3` — 「턱 끝 볼륨 (HA 1cc)」
- `market-pricing.json:categories[].items[].name@1/4` — 「이마 볼륨 (HA 2cc)」
- `market-pricing.json:categories[].items[].name@1/5` — 「볼 볼륨 (HA 1cc)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| map_1 | product_name 「쥬베룩볼륨」(M3)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 0/4(원장 자리 0) · 근거 「쥬베룩볼륨」 ⊃ 조각 「볼륨」 | canonical_mapping `DEC-2026-11-05-B4-PRC-005a` |
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 근거가 정규화 부분 일치·원장 문구 병기뿐 — 병기는 같은 말·원인·예시·부위를 가리지 않고 부분 일치는 표기 겹침일 뿐이라 같은 뜻이라는 원장 문장이 아니다(추천 없음 · 사람이 정한다)

### b4-prc/006 — 참조 조각 「비타민C」 — 이온토포레시스 중 무엇인가?

⑨ open 미해결 참조 4(원장 자리 4)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `treatment-optimization.json:by_concern[].severity_levels[].optimal_combo[]@4/0/2` — 「비타민C 이온토포레시스」
- `treatment-sequence.json:common_combos[].sequence[]@4/2` — 「비타민C 이온토포레시스」
- `market-pricing.json:categories[].items[].name@14/4` — 「이온토포레시스 (비타민C)」
- `market-pricing.json:categories[].items[].name@15/4` — 「고농도 비타민C 수액」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| map_1 | modality_subcategory_label 「이온토포레시스」(M15)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 3/4(원장 자리 3) · 근거 원장 이름 병기 「이온토포레시스(비타민C)」 | canonical_mapping `DEC-2026-11-05-B4-PRC-006a` |
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 근거가 정규화 부분 일치·원장 문구 병기뿐 — 병기는 같은 말·원인·예시·부위를 가리지 않고 부분 일치는 표기 겹침일 뿐이라 같은 뜻이라는 원장 문장이 아니다(추천 없음 · 사람이 정한다)

### b4-prc/007 — 참조 조각 「시술」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 4(원장 자리 4)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `treatment-optimization.json:by_age_group[].avoid[]@2/0` — 「과도한 시술 빈도(피부 회복력 저하 고려)」
- `treatment-optimization.json:by_age_group[].avoid[]@3/1` — 「회복력 초과 시술 빈도」
- `treatment-sequence.json:incompatible_same_day[].pair[]@6/1` — 「모든 시술」
- `market-pricing.json:categories[].items[].name@14/5` — 「진정관리 (시술 후 재생팩)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/008 — 참조 조각 「심부」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 4(원장 자리 4)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `treatment-sequence.json:incompatible_same_day[].pair[]@1/0` — 「심부 필링(페놀)」
- `treatment-sequence.json:incompatible_same_day[].pair[]@6/0` — 「심부 필링(TCA 50%+/페놀)」
- `treatment-sequence.json:minimum_intervals[].to@3` — 「박리성(ablative) 레이저/심부 필링」
- `treatment-sequence.json:minimum_intervals[].from@4` — 「심부 필링」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/009 — 참조 조각 「이모드」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 4(원장 자리 4)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `market-pricing.json:categories[].items[].name@9/0` — 「이모드 (복부)」
- `market-pricing.json:categories[].items[].name@9/1` — 「이모드 (힙)」
- `market-pricing.json:categories[].items[].name@9/2` — 「이모드 (복부+힙 동시)」
- `market-pricing.json:categories[].items[].name@9/3` — 「이모드 (4회 패키지)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/010 — 참조 조각 「810nm」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 3(원장 자리 3)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `procedure-comparison.json:comparisons[].procedures[].name@5/1` — 「다이오드 (808nm/810nm)」
- `treatment-optimization.json:by_concern[].severity_levels[].optimal_combo[]@6/0/0` — 「다이오드 레이저(810nm)」
- `treatment-optimization.json:by_concern[].severity_levels[].optimal_combo[]@6/1/1` — 「다이오드(810nm)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/011 — 참조 조각 「EMS」 — 바디 EMS, 페이셜 EMS 중 무엇인가?

⑨ open 미해결 참조 3(원장 자리 3)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `synergy.json:links[].to@20` — 「HIFES/EMS 바디」
- `market-pricing.json:categories[].items[].name@9/4` — 「안면 EMS (표정근 강화)」
- `market-pricing.json:categories[].items[].name@9/5` — 「EMS 바디 (팔뚝/허벅지)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| map_1 | modality_subcategory_label 「바디 EMS」(M10)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 0/3(원장 자리 0) · 근거 영문 낱말 「EMS」 ↔ 「바디 EMS」 | canonical_mapping `DEC-2026-11-05-B4-PRC-011a` |
| map_2 | modality_subcategory_label 「페이셜 EMS」(M10)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 0/3(원장 자리 0) · 근거 영문 낱말 「EMS」 ↔ 「페이셜 EMS」 | canonical_mapping `DEC-2026-11-05-B4-PRC-011b` |
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 근거가 정규화 부분 일치·원장 문구 병기뿐 — 병기는 같은 말·원인·예시·부위를 가리지 않고 부분 일치는 표기 겹침일 뿐이라 같은 뜻이라는 원장 문장이 아니다(추천 없음 · 사람이 정한다)

### b4-prc/012 — 참조 조각 「고주파」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 3(원장 자리 3)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `procedure-comparison.json:comparisons[].procedures[].name@6/3` — 「바넬라 (고주파 바디)」
- `treatment-optimization.json:by_concern[].severity_levels[].optimal_combo[]@7/0/1` — 「고주파 바디 RF」
- `post-procedure-timeline.json:timelines[].name@6` — 「니들RF (미세침 고주파)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/013 — 참조 조각 「색소」 — 색소/토닝 중 무엇인가?

⑨ open 미해결 참조 3(원장 자리 3)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `treatment-optimization.json:annual_plans[].schedule[].procedures[]@0/3/1` — 「IPL(색소 관리)」
- `treatment-optimization.json:annual_plans[].schedule[].procedures[]@0/9/1` — 「IPL(가을 색소 관리)」
- `treatment-optimization.json:annual_plans[].schedule[].procedures[]@2/9/1` — 「IPL(가을 색소)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| map_1 | modality_subcategory_label 「색소/토닝」(M8)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 0/3(원장 자리 0) · 근거 「색소/토닝」 ⊃ 조각 「색소」 | canonical_mapping `DEC-2026-11-05-B4-PRC-013a` |
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 근거가 정규화 부분 일치·원장 문구 병기뿐 — 병기는 같은 말·원인·예시·부위를 가리지 않고 부분 일치는 표기 겹침일 뿐이라 같은 뜻이라는 원장 문장이 아니다(추천 없음 · 사람이 정한다)

### b4-prc/014 — 참조 조각 「여드름」 — 여드름 전용 중 무엇인가?

⑨ open 미해결 참조 3(원장 자리 3)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `market-pricing.json:categories[].items[].name@10/4` — 「니들RF (여드름 흉터)」
- `market-pricing.json:categories[].items[].name@11/4` — 「MTS (여드름 흉터 집중)」
- `market-pricing.json:categories[].items[].name@12/2` — 「플라즈마 (여드름 치료)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| map_1 | modality_subcategory_label 「여드름 전용」(M15)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 0/3(원장 자리 0) · 근거 「여드름 전용」 ⊃ 조각 「여드름」 | canonical_mapping `DEC-2026-11-05-B4-PRC-014a` |
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 근거가 정규화 부분 일치·원장 문구 병기뿐 — 병기는 같은 말·원인·예시·부위를 가리지 않고 부분 일치는 표기 겹침일 뿐이라 같은 뜻이라는 원장 문장이 아니다(추천 없음 · 사람이 정한다)

### b4-prc/015 — 참조 조각 「저출력」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 3(원장 자리 3)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `procedure-comparison.json:comparisons[].procedures[].name@4/3` — 「레이저토닝 (저출력 Nd:YAG)」
- `treatment-optimization.json:by_concern[].severity_levels[].optimal_combo[]@4/1/3` — 「저출력 IPL(병용 보조)」
- `treatment-optimization.json:by_concern[].severity_levels[].optimal_combo[]@4/2/0` — 「저출력 피코토닝」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/016 — 참조 조각 「주사」 — 지방분해주사 (마케팅명) 중 무엇인가?

⑨ open 미해결 참조 3(원장 자리 3)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `treatment-optimization.json:by_concern[].severity_levels[].optimal_combo[]@4/2/1` — 「트라넥삼산(경구+주사)」
- `post-procedure-timeline.json:timelines[].name@5` — 「DCA 지방분해 주사」
- `market-pricing.json:categories[].items[].name@4/4` — 「PDRN 주사 (부위당)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| map_1 | modality_subcategory_label 「지방분해주사 (마케팅명)」(M16)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 0/3(원장 자리 0) · 근거 「지방분해주사 (마케팅명)」 ⊃ 조각 「주사」 | canonical_mapping `DEC-2026-11-05-B4-PRC-016a` |
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 근거가 정규화 부분 일치·원장 문구 병기뿐 — 병기는 같은 말·원인·예시·부위를 가리지 않고 부분 일치는 표기 겹침일 뿐이라 같은 뜻이라는 원장 문장이 아니다(추천 없음 · 사람이 정한다)

### b4-prc/017 — 참조 조각 「프랙셔널」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 3(원장 자리 3)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `procedure-comparison.json:comparisons[].procedures[].name@1/2` — 「프락셀 (프랙셔널 레이저)」
- `procedure-comparison.json:comparisons[].procedures[].name@3/1` — 「CO2 프랙셔널 레이저」
- `procedure-comparison.json:comparisons[].procedures[].name@3/3` — 「피코 프랙셔널」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/018 — 참조 조각 「리프팅기기」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 2(원장 자리 41)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `problem-packages.json:problems[].complaints[].procedures[].name@1/0/1` — 「리프팅기기」
- `problem-packages.json:problems[].complaints[].procedures[].name@1/1/1` — 「리프팅기기」
- `problem-packages.json:problems[].complaints[].procedures[].name@1/2/1` — 「리프팅기기」
- `problem-packages.json:problems[].complaints[].procedures[].name@1/3/2` — 「리프팅기기」
- `problem-packages.json:problems[].complaints[].procedures[].name@1/4/2` — 「리프팅기기」
- `problem-packages.json:problems[].complaints[].procedures[].name@1/5/2` — 「리프팅기기」
- `problem-packages.json:problems[].complaints[].procedures[].name@1/6/1` — 「리프팅기기」
- `problem-packages.json:problems[].complaints[].procedures[].name@10/1/1` — 「리프팅기기」
- `problem-packages.json:problems[].complaints[].procedures[].name@10/2/1` — 「리프팅기기」
- `problem-packages.json:problems[].complaints[].procedures[].name@2/0/0` — 「리프팅기기」
- … 외 31 곳(batch4.json evidence 전부)

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/019 — 참조 조각 「제모레이저」 — 제모 중 무엇인가?

⑨ open 미해결 참조 2(원장 자리 9)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `problem-packages.json:problems[].complaints[].procedures[].name@9/0/0` — 「제모레이저」
- `problem-packages.json:problems[].complaints[].procedures[].name@9/1/0` — 「제모레이저」
- `problem-packages.json:problems[].complaints[].procedures[].name@9/2/0` — 「제모레이저」
- `problem-packages.json:problems[].complaints[].procedures[].name@9/3/0` — 「제모레이저」
- `problem-packages.json:problems[].complaints[].combos[].combo[]@9/0/0/0` — 「제모레이저」
- `problem-packages.json:problems[].complaints[].combos[].combo[]@9/1/0/0` — 「제모레이저」
- `problem-packages.json:problems[].complaints[].combos[].combo[]@9/1/1/0` — 「제모레이저」
- `problem-packages.json:problems[].complaints[].combos[].combo[]@9/2/0/0` — 「제모레이저」
- `problem-packages.json:problems[].complaints[].combos[].combo[]@9/3/0/0` — 「제모레이저」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| map_1 | modality_subcategory_label 「제모」(M8)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 2/2(원장 자리 9) · 근거 조각 「제모레이저」 ⊃ 「제모」 | canonical_mapping `DEC-2026-11-05-B4-PRC-019a` |
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 근거가 정규화 부분 일치·원장 문구 병기뿐 — 병기는 같은 말·원인·예시·부위를 가리지 않고 부분 일치는 표기 겹침일 뿐이라 같은 뜻이라는 원장 문장이 아니다(추천 없음 · 사람이 정한다)

### b4-prc/020 — 참조 조각 「반영구화장」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 2(원장 자리 8)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `problem-packages.json:problems[].complaints[].procedures[].name@0/13/0` — 「반영구화장」
- `problem-packages.json:problems[].complaints[].procedures[].name@0/14/0` — 「반영구화장」
- `problem-packages.json:problems[].complaints[].procedures[].name@0/15/0` — 「반영구화장」
- `problem-packages.json:problems[].complaints[].procedures[].name@0/16/0` — 「반영구화장」
- `problem-packages.json:problems[].complaints[].combos[].combo[]@0/13/0/0` — 「반영구화장」
- `problem-packages.json:problems[].complaints[].combos[].combo[]@0/14/0/0` — 「반영구화장」
- `problem-packages.json:problems[].complaints[].combos[].combo[]@0/15/0/0` — 「반영구화장」
- `problem-packages.json:problems[].complaints[].combos[].combo[]@0/16/0/0` — 「반영구화장」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/021 — 참조 조각 「약물치료」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 2(원장 자리 6)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `problem-packages.json:problems[].complaints[].procedures[].name@12/6/0` — 「약물치료」
- `problem-packages.json:problems[].complaints[].procedures[].name@12/7/0` — 「약물치료」
- `problem-packages.json:problems[].complaints[].procedures[].name@12/8/0` — 「약물치료」
- `problem-packages.json:problems[].complaints[].combos[].combo[]@12/6/0/0` — 「약물치료」
- `problem-packages.json:problems[].complaints[].combos[].combo[]@12/7/0/0` — 「약물치료」
- `problem-packages.json:problems[].complaints[].combos[].combo[]@12/8/0/0` — 「약물치료」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/022 — 참조 조각 「LLLT」 — 저출력레이저(LLLT) 중 무엇인가?

⑨ open 미해결 참조 2(원장 자리 4)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `synergy.json:links[].to@29` — 「저출력레이저(LLLT) 두피」
- `problem-packages.json:problems[].complaints[].procedures[].products[]@12/3/0/0` — 「헤어맥스(LLLT)」
- `problem-packages.json:problems[].complaints[].procedures[].products[]@12/4/0/0` — 「헤어맥스(LLLT)」
- `problem-packages.json:problems[].complaints[].procedures[].products[]@12/5/0/0` — 「헤어맥스(LLLT)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| map_1 | product_name 「저출력레이저(LLLT)」(M8)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 0/2(원장 자리 0) · 근거 영문 낱말 「LLLT」 ↔ 「저출력레이저(LLLT)」 | canonical_mapping `DEC-2026-11-05-B4-PRC-022a` |
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 근거가 정규화 부분 일치·원장 문구 병기뿐 — 병기는 같은 말·원인·예시·부위를 가리지 않고 부분 일치는 표기 겹침일 뿐이라 같은 뜻이라는 원장 문장이 아니다(추천 없음 · 사람이 정한다)

### b4-prc/023 — 참조 조각 「모발이식」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 2(원장 자리 4)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `problem-packages.json:problems[].complaints[].procedures[].name@12/10/0` — 「모발이식」
- `problem-packages.json:problems[].complaints[].procedures[].name@12/9/0` — 「모발이식」
- `problem-packages.json:problems[].complaints[].combos[].combo[]@12/10/0/0` — 「모발이식」
- `problem-packages.json:problems[].complaints[].combos[].combo[]@12/9/0/0` — 「모발이식」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/024 — 참조 조각 「미백주사」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 2(원장 자리 4)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `problem-packages.json:problems[].complaints[].procedures[].name@4/6/2` — 「미백주사」
- `problem-packages.json:problems[].complaints[].procedures[].name@4/7/2` — 「미백주사」
- `problem-packages.json:problems[].complaints[].combos[].combo[]@4/6/1/1` — 「미백주사」
- `problem-packages.json:problems[].complaints[].combos[].combo[]@4/7/1/1` — 「미백주사」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/025 — 참조 조각 「병변내」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 2(원장 자리 4)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `problem-packages.json:problems[].complaints[].procedures[].name@8/6/0` — 「병변내 스테로이드주사」
- `problem-packages.json:problems[].complaints[].procedures[].name@8/7/0` — 「병변내 스테로이드주사」
- `problem-packages.json:problems[].complaints[].combos[].combo[]@8/6/0/0` — 「병변내 스테로이드주사」
- `problem-packages.json:problems[].complaints[].combos[].combo[]@8/7/0/0` — 「병변내 스테로이드주사」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/026 — 참조 조각 「스테로이드주사」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 2(원장 자리 4)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `problem-packages.json:problems[].complaints[].procedures[].name@8/6/0` — 「병변내 스테로이드주사」
- `problem-packages.json:problems[].complaints[].procedures[].name@8/7/0` — 「병변내 스테로이드주사」
- `problem-packages.json:problems[].complaints[].combos[].combo[]@8/6/0/0` — 「병변내 스테로이드주사」
- `problem-packages.json:problems[].complaints[].combos[].combo[]@8/7/0/0` — 「병변내 스테로이드주사」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/027 — 참조 조각 「755nm」 — 알렉산드라이트 중 무엇인가?

⑨ open 미해결 참조 2(원장 자리 2)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `procedure-comparison.json:comparisons[].procedures[].name@5/0` — 「알렉산드라이트 (755nm)」
- `treatment-optimization.json:by_concern[].severity_levels[].optimal_combo[]@6/1/0` — 「알렉산드라이트(755nm)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| map_1 | product_name 「알렉산드라이트」(M8)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 2/2(원장 자리 2) · 근거 원장 이름 병기 「알렉산드라이트(755nm)」 | canonical_mapping `DEC-2026-11-05-B4-PRC-027a` |
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 근거가 정규화 부분 일치·원장 문구 병기뿐 — 병기는 같은 말·원인·예시·부위를 가리지 않고 부분 일치는 표기 겹침일 뿐이라 같은 뜻이라는 원장 문장이 아니다(추천 없음 · 사람이 정한다)

### b4-prc/028 — 참조 조각 「PDT」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 2(원장 자리 2)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `procedure-comparison.json:comparisons[].procedures[].name@7/1` — 「PDT (광역동치료)」
- `treatment-sequence.json:common_combos[].sequence[]@3/2` — 「광조사(PDT)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/029 — 참조 조각 「경구」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 2(원장 자리 2)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `treatment-optimization.json:by_concern[].severity_levels[].optimal_combo[]@4/1/1` — 「트라넥삼산(경구/국소)」
- `treatment-optimization.json:by_concern[].severity_levels[].optimal_combo[]@4/2/1` — 「트라넥삼산(경구+주사)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/030 — 참조 조각 「광선치료」 — IPL 중 무엇인가?

⑨ open 미해결 참조 2(원장 자리 2)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `procedure-comparison.json:comparisons[].procedures[].name@4/2` — 「IPL (광선치료)」
- `market-pricing.json:categories[].items[].name@14/3` — 「LED 광선치료 (전체얼굴)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| map_1 | modality_subcategory_label 「IPL」(M8)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 1/2(원장 자리 1) · 근거 원장 이름 병기 「IPL(광선치료)」 | canonical_mapping `DEC-2026-11-05-B4-PRC-030a` |
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 근거가 정규화 부분 일치·원장 문구 병기뿐 — 병기는 같은 말·원인·예시·부위를 가리지 않고 부분 일치는 표기 겹침일 뿐이라 같은 뜻이라는 원장 문장이 아니다(추천 없음 · 사람이 정한다)

### b4-prc/031 — 참조 조각 「끝」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 2(원장 자리 2)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `market-pricing.json:categories[].items[].name@1/3` — 「턱 끝 볼륨 (HA 1cc)」
- `market-pricing.json:categories[].items[].name@5/5` — 「턱 끝 지방이식」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/032 — 참조 조각 「냉동지방분해」 — 쿨스컬프팅 중 무엇인가?

⑨ open 미해결 참조 2(원장 자리 2)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `procedure-comparison.json:comparisons[].procedures[].name@6/0` — 「쿨스컬프팅 (냉동지방분해)」
- `treatment-optimization.json:by_concern[].severity_levels[].optimal_combo[]@7/0/0` — 「크라이오(냉동지방분해)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| map_1 | product_name 「쿨스컬프팅」(M14)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 2/2(원장 자리 2) · 근거 원장 이름 병기 「쿨스컬프팅(냉동지방분해)」 | canonical_mapping `DEC-2026-11-05-B4-PRC-032a` |
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 근거가 정규화 부분 일치·원장 문구 병기뿐 — 병기는 같은 말·원인·예시·부위를 가리지 않고 부분 일치는 표기 겹침일 뿐이라 같은 뜻이라는 원장 문장이 아니다(추천 없음 · 사람이 정한다)

### b4-prc/033 — 참조 조각 「리포셀」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 2(원장 자리 2)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `procedure-comparison.json:comparisons[].procedures[].name@6/1` — 「리포셀 (HIFU 지방)」
- `treatment-optimization.json:by_concern[].severity_levels[].optimal_combo[]@7/2/1` — 「바디 HIFU(리포셀)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/034 — 참조 조각 「마이크로니들링」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 2(원장 자리 2)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `synergy.json:links[].to@58` — 「마이크로니들링(MTS) 두피」
- `treatment-optimization.json:by_concern[].severity_levels[].optimal_combo[]@4/2/2` — 「마이크로니들링+미백약물」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/035 — 참조 조각 「물광주사」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 2(원장 자리 2)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `procedure-comparison.json:comparisons[].procedures[].name@8/3` — 「물광주사 (메소테라피)」
- `market-pricing.json:categories[].items[].name@3/6` — 「스킨부스터 물광주사 (전체얼굴)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/036 — 참조 조각 「미라드라」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 2(원장 자리 2)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `problem-packages.json:problems[].complaints[].procedures[].name@13/4/0` — 「미라드라이」
- `problem-packages.json:problems[].complaints[].combos[].combo[]@13/4/0/0` — 「미라드라이」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/037 — 참조 조각 「실」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 2(원장 자리 2)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `market-pricing.json:categories[].items[].name@6/0` — 「PDO 실 (10줄 기준)」
- `market-pricing.json:categories[].items[].name@6/3` — 「몰딩 실 (V라인)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/038 — 참조 조각 「재생」 — 재생/면역 중 무엇인가?

⑨ open 미해결 참조 2(원장 자리 2)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `procedure-comparison.json:comparisons[].procedures[].name@8/1` — 「PRP (자가혈 재생)」
- `market-pricing.json:categories[].items[].name@12/5` — 「플라즈마 샤워 (진정/재생)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| map_1 | modality_subcategory_label 「재생/면역」(M16)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 0/2(원장 자리 0) · 근거 「재생/면역」 ⊃ 조각 「재생」 | canonical_mapping `DEC-2026-11-05-B4-PRC-038a` |
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 근거가 정규화 부분 일치·원장 문구 병기뿐 — 병기는 같은 말·원인·예시·부위를 가리지 않고 부분 일치는 표기 겹침일 뿐이라 같은 뜻이라는 원장 문장이 아니다(추천 없음 · 사람이 정한다)

### b4-prc/039 — 참조 조각 「제거」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 2(원장 자리 2)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `market-pricing.json:categories[].items[].name@7/8` — 「점 제거 (1개당)」
- `market-pricing.json:categories[].items[].name@7/9` — 「문신 제거 (10cm2)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/040 — 참조 조각 「제네시스」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 2(원장 자리 2)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `procedure-comparison.json:comparisons[].procedures[].name@7/4` — 「제네시스 (Nd:YAG 롱펄스)」
- `market-pricing.json:categories[].items[].name@7/3` — 「제네시스 (전체얼굴)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/041 — 참조 조각 「주입」 — 주입장비 중 무엇인가?

⑨ open 미해결 참조 2(원장 자리 2)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `treatment-sequence.json:incompatible_same_day[].pair[]@4/0` — 「HA 필러 주입 후 RF/HIFU」
- `market-pricing.json:categories[].items[].name@16/0` — 「줄기세포 배양액 주입 (전체얼굴)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| map_1 | modality_subcategory_label 「주입장비」(M15)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 0/2(원장 자리 0) · 근거 「주입장비」 ⊃ 조각 「주입」 | canonical_mapping `DEC-2026-11-05-B4-PRC-041a` |
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 근거가 정규화 부분 일치·원장 문구 병기뿐 — 병기는 같은 말·원인·예시·부위를 가리지 않고 부분 일치는 표기 겹침일 뿐이라 같은 뜻이라는 원장 문장이 아니다(추천 없음 · 사람이 정한다)

### b4-prc/042 — 참조 조각 「탈모」 — 탈모(비수술) 중 무엇인가?

⑨ open 미해결 참조 2(원장 자리 2)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `market-pricing.json:categories[].items[].name@11/5` — 「MTS (두피 탈모)」
- `market-pricing.json:categories[].items[].name@16/3` — 「줄기세포 두피치료 (탈모)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| map_1 | modality_subcategory_label 「탈모(비수술)」(M15)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 0/2(원장 자리 0) · 근거 「탈모(비수술)」 ⊃ 조각 「탈모」 | canonical_mapping `DEC-2026-11-05-B4-PRC-042a` |
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 근거가 정규화 부분 일치·원장 문구 병기뿐 — 병기는 같은 말·원인·예시·부위를 가리지 않고 부분 일치는 표기 겹침일 뿐이라 같은 뜻이라는 원장 문장이 아니다(추천 없음 · 사람이 정한다)

### b4-prc/043 — 참조 조각 「턱라인」 — 울쎄라 중 무엇인가?

⑨ open 미해결 참조 2(원장 자리 2)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `market-pricing.json:categories[].items[].name@8/1` — 「울쎄라 (턱라인)」
- `market-pricing.json:categories[].items[].name@8/3` — 「슈링크 유니버스 (턱라인)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| map_1 | product_name 「울쎄라」(M9)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 2/2(원장 자리 2) · 근거 원장 이름 병기 「울쎄라(턱라인)」 | canonical_mapping `DEC-2026-11-05-B4-PRC-043a` |
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 근거가 정규화 부분 일치·원장 문구 병기뿐 — 병기는 같은 말·원인·예시·부위를 가리지 않고 부분 일치는 표기 겹침일 뿐이라 같은 뜻이라는 원장 문장이 아니다(추천 없음 · 사람이 정한다)

### b4-prc/044 — 참조 조각 「피부결」 — 프락셔널, 피부 중 무엇인가?

⑨ open 미해결 참조 2(원장 자리 2)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `treatment-optimization.json:by_age_group[].upgrade[]@3/0` — 「프락셔널 CO2(피부결)」
- `treatment-optimization.json:annual_plans[].schedule[].procedures[]@2/6/1` — 「프락셔널(피부결)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| map_1 | modality_subcategory_label 「프락셔널」(M8)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 2/2(원장 자리 2) · 근거 원장 이름 병기 「프락셔널(피부결)」 | canonical_mapping `DEC-2026-11-05-B4-PRC-044a` |
| syn_2 | site 「피부」 의 동의어 | 풀리는 ⑨ 참조 2/2(원장 자리 2) · 근거 조각 「피부결」 ⊃ 「피부」 | dictionary_add `DEC-2026-11-05-B4-PRC-044b` |
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 근거가 정규화 부분 일치·원장 문구 병기뿐 — 병기는 같은 말·원인·예시·부위를 가리지 않고 부분 일치는 표기 겹침일 뿐이라 같은 뜻이라는 원장 문장이 아니다(추천 없음 · 사람이 정한다)
이미 승인된 같은 결정: DEC-2026-11-04-B1-SYN-001, DEC-2026-11-05-B3-SIT-01, DEC-2026-11-05-B3-SIT-02, DEC-2026-11-05-B3-SIT-03, DEC-2026-11-06-B6A-SITE-01, DEC-2026-11-06-B6A-SITE-02, DEC-2026-11-06-B6A-SITE-03, DEC-2026-11-06-B6A-SITE-04, DEC-2026-11-06-B6A-SITE-05, DEC-2026-11-06-B6A-SITE-06, DEC-2026-11-06-B6A-SITE-07, DEC-2026-11-06-B6A-SITE-08, DEC-2026-11-06-B6A-SITE-09, DEC-2026-11-06-B6A-SITE-10, DEC-2026-11-06-B6A-SITE-11, DEC-2026-11-06-B6A-SITE-12, DEC-2026-11-06-B6A-SITE-13, DEC-2026-11-06-B6A-SITE-14, DEC-2026-11-06-B6A-SITE-15

### b4-prc/045 — 참조 조각 「피코레이저」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 2(원장 자리 2)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `problem-packages.json:problems[].complaints[].procedures[].name@13/2/0` — 「피코레이저」
- `problem-packages.json:problems[].complaints[].combos[].combo[]@13/2/0/0` — 「피코레이저」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/046 — 참조 조각 「회복력」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 2(원장 자리 2)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `treatment-optimization.json:by_age_group[].avoid[]@2/0` — 「과도한 시술 빈도(피부 회복력 저하 고려)」
- `treatment-optimization.json:by_age_group[].avoid[]@3/1` — 「회복력 초과 시술 빈도」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/047 — 참조 조각 「후」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 2(원장 자리 2)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `treatment-sequence.json:incompatible_same_day[].pair[]@4/0` — 「HA 필러 주입 후 RF/HIFU」
- `market-pricing.json:categories[].items[].name@14/5` — 「진정관리 (시술 후 재생팩)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/048 — 참조 조각 「흉터」 — 흉터 전용 중 무엇인가?

⑨ open 미해결 참조 2(원장 자리 2)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `market-pricing.json:categories[].items[].name@10/4` — 「니들RF (여드름 흉터)」
- `market-pricing.json:categories[].items[].name@11/4` — 「MTS (여드름 흉터 집중)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| map_1 | modality_subcategory_label 「흉터 전용」(M15)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 0/2(원장 자리 0) · 근거 「흉터 전용」 ⊃ 조각 「흉터」 | canonical_mapping `DEC-2026-11-05-B4-PRC-048a` |
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 근거가 정규화 부분 일치·원장 문구 병기뿐 — 병기는 같은 말·원인·예시·부위를 가리지 않고 부분 일치는 표기 겹침일 뿐이라 같은 뜻이라는 원장 문장이 아니다(추천 없음 · 사람이 정한다)

### b4-prc/049 — 참조 조각 「복용」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 1(원장 자리 3)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `treatment-sequence.json:incompatible_same_day[].pair[]@3/0` — 「이소트레티노인 복용 중」
- `treatment-sequence.json:incompatible_same_day[].pair[]@7/0` — 「이소트레티노인 복용 중」
- `treatment-sequence.json:incompatible_same_day[].pair[]@8/0` — 「이소트레티노인 복용 중」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/050 — 참조 조각 「중」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 1(원장 자리 3)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `treatment-sequence.json:incompatible_same_day[].pair[]@3/0` — 「이소트레티노인 복용 중」
- `treatment-sequence.json:incompatible_same_day[].pair[]@7/0` — 「이소트레티노인 복용 중」
- `treatment-sequence.json:incompatible_same_day[].pair[]@8/0` — 「이소트레티노인 복용 중」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/051 — 참조 조각 「헤어맥스」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 1(원장 자리 3)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `problem-packages.json:problems[].complaints[].procedures[].products[]@12/3/0/0` — 「헤어맥스(LLLT)」
- `problem-packages.json:problems[].complaints[].procedures[].products[]@12/4/0/0` — 「헤어맥스(LLLT)」
- `problem-packages.json:problems[].complaints[].procedures[].products[]@12/5/0/0` — 「헤어맥스(LLLT)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/052 — 참조 조각 「CO2레이저」 — CO2프락셔널 중 무엇인가?

⑨ open 미해결 참조 1(원장 자리 2)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `problem-packages.json:problems[].complaints[].procedures[].products[]@13/0/0/0` — 「CO2레이저」
- `problem-packages.json:problems[].complaints[].procedures[].products[]@13/1/0/0` — 「CO2레이저」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| map_1 | product_name 「CO2프락셔널」(M8)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 1/1(원장 자리 2) · 근거 영문 낱말 「CO2레이저」 ↔ 「CO2프락셔널」 | canonical_mapping `DEC-2026-11-05-B4-PRC-052a` |
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 근거가 정규화 부분 일치·원장 문구 병기뿐 — 병기는 같은 말·원인·예시·부위를 가리지 않고 부분 일치는 표기 겹침일 뿐이라 같은 뜻이라는 원장 문장이 아니다(추천 없음 · 사람이 정한다)

### b4-prc/053 — 참조 조각 「PDL」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 1(원장 자리 2)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `problem-packages.json:problems[].complaints[].procedures[].products[]@8/6/1/0` — 「PDL(V빔)」
- `problem-packages.json:problems[].complaints[].procedures[].products[]@8/7/1/0` — 「PDL(V빔)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/054 — 참조 조각 「V빔」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 1(원장 자리 2)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `problem-packages.json:problems[].complaints[].procedures[].products[]@8/6/1/0` — 「PDL(V빔)」
- `problem-packages.json:problems[].complaints[].procedures[].products[]@8/7/1/0` — 「PDL(V빔)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/055 — 참조 조각 「±5-FU」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 1(원장 자리 2)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `problem-packages.json:problems[].complaints[].procedures[].products[]@8/6/0/0` — 「트리암시놀론(±5-FU)」
- `problem-packages.json:problems[].complaints[].procedures[].products[]@8/7/0/0` — 「트리암시놀론(±5-FU)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/056 — 참조 조각 「트리암시놀론」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 1(원장 자리 2)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `problem-packages.json:problems[].complaints[].procedures[].products[]@8/6/0/0` — 「트리암시놀론(±5-FU)」
- `problem-packages.json:problems[].complaints[].procedures[].products[]@8/7/0/0` — 「트리암시놀론(±5-FU)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/057 — 참조 조각 「1064nm」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 1(원장 자리 1)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `procedure-comparison.json:comparisons[].procedures[].name@5/2` — 「Nd:YAG (1064nm)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/058 — 참조 조각 「50%」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 1(원장 자리 1)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `treatment-sequence.json:incompatible_same_day[].pair[]@6/0` — 「심부 필링(TCA 50%+/페놀)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/059 — 참조 조각 「808nm」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 1(원장 자리 1)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `procedure-comparison.json:comparisons[].procedures[].name@5/1` — 「다이오드 (808nm/810nm)」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)

### b4-prc/060 — 참조 조각 「ALA」 — 하위분류·제품·부위·성분 사전 후보 없음

⑨ open 미해결 참조 1(원장 자리 1)가 이 미등록 조각 때문에 튜플이 못 된다. 후보는 하위분류·제품·부위·성분 사전의 정규화 부분 일치·원장 병기뿐(유사도 없음). 하위분류·제품은 그 참조 자리만 읽는 canonical_mapping(라벨 조각 · scope=REF-) — 사전 전체를 바꾸지 않는다(「HA」 B2A-MAP-001 과 같은 방식).

**원장 원문**

- `treatment-sequence.json:common_combos[].sequence[]@3/1` — 「ALA 도포·배양」

| 옵션 | 뜻 | 적용되면 | 결정 |
|---|---|---|---|
| keep | 지금대로(⑨ 미해결) | 결정 없음 | 결정 없음 |

추천: **—** — 사전 후보 근거 없음(추천 없음)
