# [researcher · 읽기만] 케이스에 닿지 않는 고민 조사 (사용자 요청 11-20)

너는 procedure-hub 조사 워커다. 앞 맥락 없음. **silver · gold · 앱 · 허브 쓰기 0** · 커밋 0 · 서브에이전트 0 · 18222 · 18105 손대지 마라(18105 는 GET 만).

`P=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇` · `W=$P/orchestration/work/phub-consult-demo` · `S=$W/silver-model/silver`(gold caa03560) · 원장 `$P/orchestration/work/_archive/procedure-hub/phub-recommend/bronze/phub-ledger/` · 명동점 매핑 `/Users/kknaks/git/clinic_chat/data/kos/myeongdong-mapping-20261120-v3.json`.

## 배경
원칙: 고민은 케이스에만(indication target_table = procedure_case + 제품 층 적응은 제품에). 앱은 고민 → (그 고민 + **아래 고민**) → 케이스 「직접」 → 진료항목으로 찾는다. 코디가 「케이스에 직접 붙은 행이 없는 고민」 을 계층을 안 보고 60 개로 셌다(제품에만 붙음 35 · 어디에도 없음 25 — 예 「볼륨」(CON-273 대분류)은 아래 「볼륨 손실」 이 케이스 40 이라 실제로는 닿음). **진짜로 닿지 않는 고민**을 가려라.

## 할 일
1. 고민 사전(`$S/concern.csv`) 전부(269)에 대해 「자기 + 아래 고민 전부」 로 케이스 「직접」 indication 이 있는지 셈 → 닿음 / 안 닿음.
2. 안 닿는 고민 하나하나를 가른다:
   - **(a) 묶음 이름**(대분류 · 아래 고민이 있는데 그 아래도 다 안 닿음 등 — 구조로 판단)
   - **(b) 같은 뜻 고민이 이미 케이스에 있음**(이름 · 별칭 · 설명 · 원장 원문으로 — 후보 고민 코드 · 근거)
   - **(c) 진짜 빈틈** — 붙을 케이스 후보(코드 · 시술 · 부위 · 조직)와 근거: ① 원장 문장 ② 그 고민이 붙은 제품을 쓰는 케이스(case_product) 중 고민 부위(concern_site) · 조직이 맞는 것 ③ 외부 근거(출처 필수 · 지어내기 금지). 후보 여럿이면 다 적고 고르지 마라.
   - **(d) 근거 못 찾음**(이유)
3. 명동점 영향: (c) 를 붙이면 그 고민으로 명동점 진료항목이 몇 개 나오는지(지금 0).

## 산출
- `$W/concern-reach.csv`(utf-8-sig): 고민 코드 · 이름 · 계층(level · parent) · 지금 닿는 케이스 수(자기 + 아래) · 판정(a/b/c/d) · 같은 뜻 고민(b) · 후보 케이스(c) · 근거 종류 · 출처 · 근거 문장 · 명동점 진료항목 수(붙인 뒤).
- `$W/research-concern-reach.md`: 판정별 수 · (b) 합치기 제안 · (c) 목록 요약 · 사람 판단 묶음(50 안쪽 · 추천 하나씩) · 데이터 검사 제안(「모든 고민이 케이스에 닿는가」 를 silver-check 에 넣는 규칙 꼴).

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_08fd3049-0cd7-4e48-9189-d68fbdbb9cef --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "researcher 완료: 고민 닿음 조사" --body "a/b/c/d 수"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] researcher 고민 닿음 조사 완료 — <한 줄>. 상세는 인박스." --enter
```
