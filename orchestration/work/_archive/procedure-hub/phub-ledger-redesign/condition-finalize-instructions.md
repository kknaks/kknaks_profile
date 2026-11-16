# 지시서 — 사람 조건 사전 확정: 의미 중복 정리 + 결정 12건 + silver 합치기

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/phub-ledger-redesign/silver-model/` 기준.

## 읽을 것

- `drafts/condition/` 전부(특히 `condition-notes.md` §3 · §6 판단 12건) · `condition-build.py` · `condition-check.py`
- `silver/` 전부(공통 `alias.csv` · `source_ref.csv` · `material.csv`)
- 원장 `../../phub-recommend/bronze/phub-ledger/*.json`(확인용, 고치지 않음)

## 사용자 결정 — 「정규화 · 중복 없게, 추천으로」

**A. 의미 중복 정리** — 원칙: **같은 뜻은 한 행**(이름 = 일반 용어, 다른 쪽은 alias — 한자어는 의학 용어), **포함 관계는 부모로**, **범위만 겹치는 것은 행 유지 + 설명에 겹침을 원장 문장으로**. 같은 뜻인지는 원장 문맥으로 확인하고, 원장이 다르게 쓰면 나눈 채로 두고 notes 에 근거.
1. 같은 뜻 후보: 면역저하 ↔ 면역 상태 변화 · 피부 염증 ↔ 피부염.
2. 포함 → 부모로: 개방성 상처 → 피부 손상 · 인공 태닝 → 자외선 노출(자외선 차단 부족도 원장 문맥이 노출의 한 형태면 그 아래, 아니면 그대로) · 마취제 알레르기 · 히알루로니다아제 알레르기 → 약물 알레르기 · 이물반응 병력 ↔ 면역 반응 민감 체질(같은 뜻이면 합침, 포함이면 부모, 다르면 그대로 — 원장대로).
3. 범위 겹침(행 유지 + 설명): 고령 ↔ 50대 이상 · 어두운 피부 ↔ Fitzpatrick IV~VI형(원장의 IV~VI / V~VI 엇갈림 그대로) · 밝은 피부 ↔ I~II형.
4. 측정값 이름 → 상태 이름: 체질량지수 · 피하지방 두께 → 원장이 말하는 상태(예: 비만 · 피하지방 얇음)로. 원장에 상태 말이 없으면 바꾸지 말고 판단 목록. 혈관 변이는 원장 문맥에 맞는 대분류로 옮길지 판단(애매하면 그대로 + notes).
5. **전수 점검**: 위 목록 밖에서도 같은 원칙으로 152행 전부를 한 번 더 본다(같은 뜻 · 포함 · 범위 겹침). 처리한 것 · 남긴 것 표를 notes 에.

**B. §6 판단 12건** — 1~10 · 12 = 지금대로. **11 = B: 「아큐탄」을 이소트레티노인 복용의 alias(별칭)로 추가**(근거 = 원장 taxonomy 아이템 이름 자리, 사용자 결정 11-11 「아큐탄 → 성분 이소트레티노인 · 사람 조건으로」).

합칠 때: 지워지는 행의 source_ref · alias · parent 참조를 남는 행으로 옮기고 중복 제거, 지워지는 행 name_ko → 남는 행 alias. 지운 → 남은 코드 대응표를 notes 에.

## silver 합치기

- 고치기 전 `silver/alias.csv` · `silver/source_ref.csv` 를 `archive/silver-before-condition/` 에, 반영 전 drafts 를 `archive/condition-before-finalize/` 에 복사.
- `silver/condition.csv` 새로 두고, 조건 계열 alias · source_ref 행을 공통 표에 덧붙인다(기존 행 바이트 그대로). drafts 도 최종판.

## 검증 (`condition-check.py` 갱신 — 코디가 다시 돌린다)

- 기존 검사 전부(silver 기준).
- 위 A-1~4 각 항목이 notes 표의 처리대로 되어 있는지(합친 것은 한 행 + alias · 부모로 이은 것은 parent · 범위 겹침은 설명에 서로 이름이 나옴).
- name_ko · alias 를 띄어쓰기 · 「복용」 「병력」 「체질」 같은 꼬리말을 떼고 비교했을 때 같은 말이 두 행에 남은 것 = notes 「남긴 것」 표와 같음.
- 보존: 반영 전 이름(name_ko ∪ alias) ⊆ 후 · 반영 전 근거 ⊆ 후.
- silver 의 조건 밖 표 바이트 불변 · alias/source_ref 앞쪽 행 바이트 그대로.
- 결과를 `condition-notes.md` 끝에 「## 9. 확정(11-12)」으로(무엇을 · 중복 점검 표 · 행 수 전/후 · 검증 출력).

## 완료 보고

범위를 넓히지 않는다(관계 · 외부 조사 하지 않음). preamble 의 `worker_done` 을 정확히 한 번(`--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/condition/condition-notes.md`).
그다음:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "condition 확정 완료: drafts/condition/condition-notes.md §9" --enter`
