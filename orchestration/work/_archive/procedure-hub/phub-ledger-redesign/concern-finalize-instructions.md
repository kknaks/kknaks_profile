# 지시서 — 고민 사전 확정: 사용자 결정 10건 반영 + silver 합치기

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/phub-ledger-redesign/silver-model/` 기준.

## 읽을 것

- `drafts/concern/` 전부(특히 `concern-notes.md` §3 합치지 않은 후보 · §4 · §5 판단 10건) · `concern-check.py`
- 직전 빌드 스크립트(있으면): `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile-----------/5598de84-d252-4569-9c96-23d1e187e48b/scratchpad/build.py` · `rows.py` · `zones.py`
- `silver/` 전부(공통 `alias.csv`(target_table · target_code · name · kind: 별칭/약어/의학 용어) · `source_ref.csv`(target_table · target_id · field · ref) · site)
- 원장 `../../phub-recommend/bronze/phub-ledger/*.json`(확인용, 고치지 않음)

## 할 일 (사용자 결정 「추천대로」 — notes §5 번호 그대로)

1. 이중턱: 지금대로(parent 얼굴 처짐 · kind 윤곽).
2. 제모: **「원치 않는 체모」 한 행 추가** + alias 「원하지 않는 체모」(별칭). 근거 = 원장 「원치 않는 체모 제거」 등 자리. 부모·kind 는 원장 P10 제모 자리대로 판정, 부위는 원장이 특정한 곳만.
3. 피부 타입(민감성 · 건성 · 지성 · 복합성 · 어두운 피부): 고민 아님 유지 → notes 에 「사람 조건 사전 후보」 목록(원문 · 자리)으로 남긴다.
4. 원장 확인 없는 한자어 · 동의어 별칭: 그대로.
5. 다크서클 ↔ 눈밑 꺼짐: 두 행 유지.
6. 「~경우」 절 형태: 넣지 않음 유지.
7. 전신 고민 11행: 그대로.
8. 홍조 flushing(보충) · 주사 rosacea(원장): 지금대로.
9. 흑자 · 검은 점 · 잡티: 각각 행 유지 · `notes/concern-ledger-check-list.csv`(what · 원장 포인터 · 원장 값 · note)에 올린다.
10. **같은 말 묶음 합침** — 원칙: 같은 상태를 가리키는 말은 한 행(이름 = 원장에서 가장 일반적인 말, 한자 의학 용어는 alias kind 의학 용어, 나머지 별칭). 범위·원인이 다른 것은 나눈 채로. notes §5-10 추천 목록(볼륨 손실/감소/소실/체적 감소 · 피부 탄력 저하/감소/부족 · 모공 확대/넓은 모공/모공 확장 · 피지 3행 · 복부 지방/뱃살 · 등 지방/등살 · 다한증/과다 발한증 · 튼살/스트레치마크 · 일광 흑자/태양흑자)을 합친다. 그 밖 §3 후보는 같은 원칙으로 판정하되 애매하면 나눈 채로 두고 notes 에.
   - 합칠 때: 지워지는 행의 source_ref · alias · concern_site · parent_code 참조를 남는 행으로 옮기고 중복 제거, 지워지는 행 name_ko → 남는 행 alias. 지운 코드 → 남는 코드 대응표를 notes 에.

## silver 합치기

- 고치기 전 `silver/alias.csv` · `silver/source_ref.csv` 를 `archive/silver-before-concern/` 에 복사.
- `silver/concern.csv` · `silver/concern_site.csv` 를 새로 두고, 고민 계열 alias · source_ref 행을 공통 `silver/alias.csv` · `silver/source_ref.csv` 에 덧붙인다(기존 행 변경 0).
- 빌드 스크립트를 `drafts/concern/concern-build.py` 로 레포에 둔다(scratchpad 판이 없으면 이번 반영을 재현하는 스크립트로). drafts/concern 의 CSV 는 최종판으로 갱신.

## 검증 (`drafts/concern/concern-check.py` 갱신 — 코디가 다시 돌린다)

- 기존 검사 전부 + silver 기준: 모든 참조 존재(concern parent · concern_site site_code · alias/source_ref target) · `;` 0 · 괄호 0 · name_ko 중복 0 · 모든 concern · concern_site 행 근거 ≥ 1.
- 근거 · 이름 보존: 반영 전 drafts 의 ref 집합 ⊆ 후, 반영 전 이름(name_ko ∪ alias) ⊆ 후.
- silver 의 다른 표 바이트 불변 · alias/source_ref 의 고민 밖 행 불변.
- 결과를 `drafts/concern/concern-notes.md` 끝에 「## 6. 확정(11-12)」으로(무엇을 · 행 수 전/후 · 지운→남은 코드 · 검증 출력).

## 완료 보고

범위를 넓히지 않는다. preamble 의 `worker_done` 을 정확히 한 번(`--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/concern/concern-notes.md`).
그다음:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "concern 확정 완료: drafts/concern/concern-notes.md §6" --enter`
