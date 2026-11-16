# 지시서 — ③ 관계 합치기: 시범 + A · B · C · D → silver

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/phub-ledger-redesign/silver-model/` 기준.

## 1. 배경

Procedure Hub 실버 ③ 관계(원장이 시술에 대해 하는 말 — 적응 · 효과 · 부작용 위험 · 금기 · 시술 간 관계 · 패키지 · 문헌)를 다섯 초안으로 만들었다. 모두 각자 검증 PASS:

| 초안 | 계열 |
|---|---|
| `drafts/relation-pilot/` (시범 · 표 구조 정본 = `relation-notes.md` §9-2) | M1 · M2 |
| `drafts/relation-a/` | M3 · M4 · M5 · M6 · M16 · M17 · M18 |
| `drafts/relation-b/` | M7 · M9 · M10 · M11 · M14 |
| `drafts/relation-c/` | M8 · M13 |
| `drafts/relation-d/` | M12 · M15 |

이번 일: 다섯을 **한 벌로 합쳐 silver 에 올린다.** 판정 · 값은 바꾸지 않는다(아래 §3 결정 반영과 §4 겹침 정리만).

## 2. 읽을 것

- 다섯 초안 폴더 전부(notes — 특히 각 §6 · build · check · relation-conflicts · dict-candidates · relation-judgment)
- 발주서 `../relation-pilot-brief.md` · `../relation-a-brief.md`(§0-1 겹침 규칙) · `../relation-pilot-finalize-instructions.md`
- `silver/` 전부 · `notes/combo-item-judgment.csv`(② 판정 — 원장 이름 → 시술 · 케이스 코드)
- 원장 `../../phub-recommend/bronze/phub-ledger/*.json`(확인용, 고치지 않음)

## 3. 사용자 결정 (11-15 「추천대로」)

**3-1. 표 칸 추가**(정규화 원칙 — 값 하나면 칸):
- `adverse_guidance.evidence_text` — 대처 규칙의 근거 · 합의 수준(A §6-1 · C §6-1 의 1잎씩).
- `contraindication.site_code` — 부위 금기(A §6-3 「코에 CaHA/PLLA 금기」 등 — 각 초안에서 condition 빈칸 + 이유 원문으로 둔 부위 금기를 다시 찾아 채움).
- `contraindication.polarity` — 값 3개: 금기 / 해당 없음(「안전하게 시행 가능」 같은 반대 진술) / 보고 없음. 기존 행은 금기. B §6-5 의 반대 진술 · 다른 초안의 같은 꼴을 채움.
- 관계 표의 `target_table` 에 **`package`** 허용 — 여러 시술을 묶은 메뉴에 대한 진술(B §6-1 DNA리셋프로그램 18잎 등)을 그 package 행에.

**3-2. ② 코드 없는 항목의 진술**(지금 계열 층 + note):
- **메뉴**(A §6-4 15 · D §6-1 메뉴 24 · B 몰드리프트 등): 그 메뉴의 package 행이 있으면 `target_table=package` 로 옮긴다. package 행이 없으면 만든다(package · package_item — ② 판정 코드로 항목).
- **시술 아님 · 성분**(D §6-1 시술 아님 10 · 성분 11 — 경구약 · 홈케어 · 하이드로퀴논 · 트레티노인 …): 관계 행에서 **빼고** 판정을 「안 담음 — 시술 아님 / 성분(사용자 11-15)」으로 바꾼다. 헤어셀처럼 제품 층에 붙은 것은 그대로.
- **시술 종류인데 코드 없음**(ACR · 두피스케일링 · 모노 · 볼륨실 · 그 밖 같은 꼴): 지금대로 계열 층 + note.

**3-3. 묶음 경계에서 넘긴 관계**(A §6-2 · B §6-2 · C §6-3 · §6-5 — 약 60잎): 넘긴 잎마다 맡은 묶음(또는 시범) 결과에 같은 관계가 있는지 확인. 없으면 넘긴 쪽 판정 근거로 그 몫 행을 만든다(값 · 원문 규칙 그대로). 시범 몫의 M1 ↔ M8 「당일 병행 가능」(C §6-5)도 같은 처리. 처리 표를 notes 에.

**3-4. 이소트레티노인 대기**(C RCF-C001 ↔ D RCF-D001): consent 원장이 깊이별로 나눠 적은 대로 **깊이별 행**(프락셔널/얕은 필링 · 박리성 · 비박리성 얕은 시술 — 원문 그대로 · 숫자는 원문에 있을 때만). C · D 행을 이 기준으로 맞추고, 다른 원장(사전 점검 · sequence) 행은 근거 · 충돌 표시로 남긴다.

**3-5. 그 밖 충돌**(A 8 · B 4 · C 2 · 시범 5): 각 초안 decision 그대로. 합본 `relation-conflicts.csv`(묶음 칸 추가 · id 다시 매김 · adopted/superseded 를 새 id 로).

**3-6. silver 사전 추가 1**: 제품 「사파이어레이저」(C §6-2) — product 칸 · 원칙대로(회사 · 허가 모르면 빈칸 · `notes/product-ledger-check-list.csv` 에 행 덧붙임), product_modality(원장 계열) · 그 12잎을 제품 층 관계로.
**나머지 사전 후보**(다섯 dict-candidates 합 54 — 고민 · 효과 · 부작용 · 사람 조건 · 시술/케이스)는 **사전에 넣지 않는다** — `notes/relation-dict-candidates.csv` 로 합치기만(같은 후보는 한 행 · 어느 초안 칸). 다음 단계(사전 보강)에서 처리.

## 4. 합칠 때 할 일

1. **id 다시 매김**: 표마다 `IND-0001` 꼴(시범 → A → B → C → D 순). 옛 id → 새 id 대응표 `notes/relation-id-map.csv`. 표 사이 참조(adverse_risk_id · package_id · citation_id · relation_id · indication_id · citation_link_id …)와 source_ref target_id 도 새 id 로.
2. **겹침 점검**(표를 notes 에):
   - 같은 원장 포인터를 둘 이상의 초안이 판정 — 같은 값이면 하나, 다르면 §0-1 규칙상 맡은 묶음 것, 둘 다 관계 행이면 판단 목록.
   - 같은 관계(같은 표 · 같은 target · 같은 대상 코드 · 같은 값)가 두 초안에 = 하나로(근거 합침).
   - **문헌**: pmid → doi → 제목 순으로 같은 문헌을 하나로, citation_link 는 새 citation id 로.
   - **패키지**: 같은 원장 자리(이름 · 포인터)가 두 초안에 = 하나로 · 항목 합침. D §6-2 처럼 다른 계열 항목이 이름으로만 있는 패키지는 ② 판정 코드로 항목을 채운다.
   - rating_scale 같은 척도(원장 · 칸 이름 같음)는 하나로.
3. **silver 에 새로 둘 표**: 시범 §9-2 의 20 표(+ §3-1 칸) — indication · indication_condition · outcome · adverse_risk · adverse_frequency · adverse_factor · adverse_guidance · adverse_rating · rating_scale · contraindication · procedure_relation · procedure_relation_effect · package · package_item · package_condition · package_schedule · recovery · citation · citation_link · statement_translation. 공통 `source_ref.csv` 에 관계 행 근거를 **덧붙인다**(기존 행 바이트 그대로 · 같은 행 중복 제거).
4. **silver 밖(notes/)**: `relation-judgment.csv`(다섯 합본 — 초안 · 계열 칸 추가, §3-2 로 바꾼 판정 반영) · `relation-conflicts.csv` · `relation-dict-candidates.csv` · `relation-id-map.csv` · `relation-notes.md`(아래 §6).
5. 고치기 전: `silver/` 전체를 `archive/silver-before-relation/`, 다섯 초안을 `archive/relation-drafts-before-merge/` 에 복사. 초안 폴더는 지우지 않는다.

## 5. 검증 (`drafts/relation-merge/merge-build.py` · `merge-check.py` — 코디가 다시 돌린다)

- 다섯 초안 check 기준 전부를 합본에 대해 다시: 참조 존재(target_table 5종 — modality · procedure · procedure_case · product · package) · id 중복 0 · `;`(원장 문장 통째 예외만) · 모든 행 근거 ≥ 1 · `*_text` · text · statement 원장 글자 그대로 · **`*_min` · `*_max` 숫자는 같은 행 원문에 있음** · polarity 값 3개 밖 0 · rating 값 범위.
- 판정: 다섯 초안의 판정 잎 전부가 합본 판정에 있음 · 「담을 칸 없음」 = 0(또는 notes 판단 목록과 같음) · §3-2 로 뺀 행 = 표와 같음.
- 보존: 다섯 초안의 관계 값이 합본에 전부(대응표로) — 뺀 것은 §3-2 시술 아님 · 성분과 §4-2 하나로 합친 것뿐.
- silver: 새 표 20 · product +1(사파이어레이저) · product_modality +n · source_ref 덧붙임 · 그 밖 silver 바이트 불변 · alias/source_ref 앞쪽 행 바이트 그대로.
- **입구 · 매핑 현황 집계**(notes 에 숫자로): 계열별 관계 행 수 · 시술 136(+) 중 적응 · 효과 · 부작용 위험이 하나라도 있는 시술 수(직접 + 계열에서 물려받음 따로) · **고민 사전 260 중 적응으로 시술 · 케이스에 닿는 고민 수 · 안 닿는 고민 목록** · 효과 사전 중 outcome 에 쓰인 수 · 부작용 사전 중 adverse_risk 에 쓰인 수 · 사람 조건 사전 중 금기에 쓰인 수 · 제품 층 관계가 있는 제품 수.
- `git status` 로 산출물 외 변경 없음.

## 6. notes (`notes/relation-notes.md`, 짧게)

1. 합친 결과 행 수(표별 · 계열별)
2. 겹침 점검 표 · 하나로 합친 수(관계 · 문헌 · 패키지 · 척도)
3. §3 반영(칸 추가로 담은 수 · 패키지로 옮긴 수 · 뺀 시술 아님/성분 수 · 넘긴 관계 처리 표 · 이소트레티노인 행)
4. 입구 · 매핑 현황 집계
5. 사용자 판단이 필요한 것 — 원문 · 이유 · 추천 · 선택지(합치며 새로 나온 것만)
6. 검증 출력

## 7. 하지 않는 것 · 완료 보고

새 판정 · 사전 행 추가(사파이어레이저 제외) · ② 코드 변경 · 외부 조사 · 원장 변경 · 커밋 · push 하지 않는다.
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/notes/relation-notes.md`).
그다음:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "관계 합치기 완료: silver-model/notes/relation-notes.md" --enter`
