# 지시서 — 부위 사전 마무리 6건 (silver 직접 수정)

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/phub-ledger-redesign/silver-model/` 기준.

## 읽을 것

- `notes/site-finalize-notes.md`(특히 §4 합칠 때 적용한 방식 · §5 후보 · §8) · `notes/site-finalize-check.py` · `notes/site-ledger-check-list.csv`
- `silver/` 의 site · anatomy · anatomy_site · alias · source_ref
- 원장 `../../phub-recommend/bronze/phub-ledger/anatomy-danger-zones.json`(확인용, 고치지 않음)

## 할 일 (사용자 결정 「추천으로」 — 그대로)

고치기 전 판을 `archive/site-before-finalize-2/` 에 site 계열 표(site · anatomy · anatomy_site · alias · source_ref)만 복사해 둔다. 합칠 때 방식은 직전 작업(§4)과 같다(참조 옮김 · 중복 제거 · 지운 행 name_ko → alias).

1. **측두선 ← 상측두융합선** 합침: 남는 이름 측두선(ANA-108), 상측두융합선은 alias kind 의학 용어. name_en 은 원장 값(Superior temporal line)을 남는 행에.
2. **다리 ← 하지** 합침: 남는 이름 다리(SITE-102), 하지는 의학 용어.
3. **체부**: 지금 전신의 alias(의학 용어)를 **체간**(SITE-006)으로 옮긴다(원장 「사지·체부 동상」 — 몸통 뜻). 체부 근거(source_ref)도 체간으로.
4. **안검 · 두부 · 하안면부** alias kind 별칭 → **의학 용어**.
5. **해부 구조 사전 행 근거**: 사전 행에 직접 근거가 없는 anatomy 행 전부에, 그 구조의 원장 이름 칸 포인터(예 `anatomy-danger-zones.json:/zones/0/vessels/0/name`, target_muscle 등 이름이 적힌 칸)를 source_ref(field 빈칸)로 추가한다. 이름 칸이 없으면 추가하지 말고 notes 에 목록. anatomy_site 근거는 그대로.
6. **관자궁**(ANA-097): 그대로 둔다. `notes/site-ledger-check-list.csv` 에 「관골궁 오기 의심」 1행 추가(원장 포인터 zones/2/clinical_pearls/6). 목선/네크라인 · 눈꼬리/외안각은 손대지 않는다.

## 검증

`notes/site-finalize-check.py` 를 이번 변경에 맞게 갱신해 돌린다: 모든 참조 존재 · `;` 0 · 괄호 0 · **모든 사전 행(site · anatomy)에 직접 source_ref ≥ 1**(5번 뒤 남는 예외는 목록) · 고치기 전 ref 집합 ⊆ 후 ref 집합 · alias 이름 보존 · site 계열 밖 표 바이트 불변.
결과를 `notes/site-finalize-notes.md` 끝에 「## 11. 마무리 6건(11-12)」으로 붙인다(무엇을 · 행 수 전/후 · 검증 출력).

## 완료 보고

범위를 넓히지 않는다. preamble 의 `worker_done` 을 정확히 한 번(`--report-path orchestration/work/phub-ledger-redesign/silver-model/notes/site-finalize-notes.md`).
그다음:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "site 마무리 6건 완료: notes/site-finalize-notes.md §11" --enter`
