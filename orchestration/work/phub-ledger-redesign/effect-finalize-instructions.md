# 지시서 — 효과 사전 확정: 정규화만 + silver 합치기

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/phub-ledger-redesign/silver-model/` 기준.

## 읽을 것

- `drafts/effect/` 전부(특히 `effect-notes.md` §1 · §3 · §4 · §6 판단 10건) · `effect-build.py` · `effect-check.py`
- `silver/` 전부(공통 `alias.csv` · `source_ref.csv`)
- 원장 `../../phub-recommend/bronze/phub-ledger/*.json`(확인용, 고치지 않음)

## 사용자 결정

**효과는 시술 · 케이스 쪽에서 본다 — 이번엔 효과 사전 정규화만.** 효과 → 고민 연결(`effect_concern`)은 silver 에 올리지 않는다(케이스 단계에서 케이스 → 효과 · 케이스 → 고민으로 만난다).

## 할 일

1. **effect_concern 은 silver 에 넣지 않는다.** 대신 지금 54 짝 + 원장 근거를 `notes/effect-concern-reference.csv`(effect_code · effect_name · concern_code · concern_name · ref · note)로 남긴다 — 케이스 단계 참고 자료. 말뜻으로만 맞는 후보(§6-3 의 8개 · 광대 축소 → 광대 · 주름 예방 → 주름 · 색소/톤 개선 → 색소 등)도 같은 파일에 `note = 말뜻 후보(원장 짝 없음)`으로.
2. **§6 판단은 추천대로**: 1 부위 붙은 표현 행 안 나눔 · 2 피부 재생 지금대로 · 4 「볼륨 충전」 · 5 리프팅 = 처짐 개선 별칭 · 6 항노화 아래 지금대로 · 7 전신 드문 효과는 전신항노화 언급 · 8 피부 진정 효과 · 9 「피부 개선」 · 부종 감소 등 행 안 만듦 · 10 수분 공급 → 수분 개선 언급. (§6-3 은 1번으로 대체.)
3. **빠졌을 수 있는 효과 다시 찾기** — 고민 사전(`silver/concern.csv`)의 피부질환 · 기타 · 두피/탈모 · 홍조/혈관 · 체모 · 모공 쪽 고민(백반증 · 건선 · 아토피피부염 · 지루성피부염 · 광선각화증 · 지루각화증 · 점 · 사마귀 · 편평사마귀 · 쥐젖 · 다모증 · 부종 · 손톱 약화 · 비듬 · 모공 막힘 · 혈관종 · 주사 등)에 대해, 원장에 **효과 표현**(○○ 제거 · ○○ 치료 · ○○ 완화 · ○○ 개선 …)이 있는지 찾는다.
   - 있으면 effect 행으로 추가(같은 규칙: 원장 표현 · 명사형 · 3단 · 설명 · 근거). 비슷한 것끼리 원장 말로 묶을 수 있으면 중분류(예: 원장에 「점/사마귀 제거」 같은 말이 있을 때만).
   - 없으면 `effect-notes.md` 에 「효과 표현 없음」 목록(고민 · 찾아본 말 · 결과).
4. **silver 합치기**: 고치기 전 `silver/alias.csv` · `silver/source_ref.csv` 를 `archive/silver-before-effect/` 에 복사. `silver/effect.csv` 새로 두고, 효과 계열 alias · source_ref 행을 공통 표에 덧붙인다(기존 행 변경 0, effect_concern 행은 넣지 않음). drafts/effect 의 CSV 도 최종판으로 갱신, `effect_concern.csv` 는 drafts 에서 지우고 1번 파일로 대신.

## 검증 (`effect-check.py` 갱신 — 코디가 다시 돌린다)

- 기존 검사 전부(silver 기준) — 단 effect_concern 검사는 빼고, reference 파일의 코드가 effect · concern 에 있는지만.
- silver 에 effect_concern 없음 · 고민 밖 · 효과 밖 표 바이트 불변 · alias/source_ref 의 효과 밖 행 불변.
- 보존: 반영 전 effect 이름(name_ko ∪ alias) ⊆ 후 · 반영 전 effect 근거 ⊆ 후.
- 결과를 `effect-notes.md` 끝에 「## 7. 확정(11-12)」으로(무엇을 · 새 효과 행 · 효과 표현 없음 목록 · 행 수 전/후 · 검증 출력).

## 완료 보고

범위를 넓히지 않는다(케이스 · 관계 · 외부 조사 하지 않음). preamble 의 `worker_done` 을 정확히 한 번(`--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/effect/effect-notes.md`).
그다음:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "effect 확정 완료: drafts/effect/effect-notes.md §7" --enter`
